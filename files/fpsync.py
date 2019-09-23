#! /usr/bin/python
# This script is designed to run as a scheduled cron job to ensure data is
# backed up. This will wrap fpsync in order to spawn a multithreaded job for
# syncing data.
#
# Author: Luis Siilva
#
import os
import sys
import argparse
import logging
import time
import shlex
import psutil
from subprocess import Popen, PIPE, call


class fpsync:

    def __init__(self):
        '''
        Order of function operations here
        '''
        self.parse_inputs = self.parse_inputs()
        self.check_lock_file = self.check_lock_file()
        self.validate_args = self.validate_args()
        self.run_fpsync = self.run_fpsync()
        self.process_return_code = self.process_return_code()
        self.release_lock = self.release_lock()

    def check_lock_file(self):
        '''
        Create lock file to ensure that these jobs run only one at a time.
        '''
        self.lock_file = os.path.join('/tmp', '%s.lock') \
                        % self.arg_dict['nickname']
        self.pid = str(os.getpid())
        logger.info("pid file and pid: %s %s" % (self.lock_file, self.pid))
        if os.path.isfile(self.lock_file):
            self.findProcessIdByPID = self.findProcessIdByPID()
            if self.pid_active:
                logger.critical("%s already exists, exiting with pid %s"
                            % (self.lock_file, self.pid))
                self.rc = 2
                self.process_return_code()
                sys.exit()
        else:
            file(self.lock_file, 'w').write(self.pid)
        logger.info("%s %s" % (self.lock_file, self.pid))

    def findProcessIdByPID(self):
        '''
        Get a list of all the PIDs of a all the running process whose name
        contains the given string processName
        '''
        self.pid_active = False
        try:
            # Check if process name contains the given name string.
            last_pid = int(open(self.lock_file).readline())
            if  last_pid in psutil.pids():
                self.pid_active = True
        except (psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess), e:
            logger.critical("we got problems!: %s" % e)
            pass

    def validate_args(self):
        which_fpsync = 'which fpsync'
        try:
            fp_cmd_path = Popen(which_fpsync,
                                    shell=True,
                                    stdout=PIPE,
                                    stderr=PIPE)
            fp_out, fp_err = fp_cmd_path.communicate()
        except OSError, e:
            logger.critical("OSError: %s" %e)
        if not fp_err and fp_out:
            cmd_list = [fp_out.rstrip()]
        else:
            logger.critical("can't find fpsync executable output: %s \
                            error: %s") % (fp_out, fp_err)
        for key in self.arg_dict:
            if key == 'verbose' and self.arg_dict[key]:
                cmd_list.append("-v")
            if key == 'nthreads':
                cmd_list.append(("-n %s") % self.arg_dict[key])
            if key == 'file_per_sync':
                cmd_list.append(("-f %s") % self.arg_dict[key])
            if key == 'bytes_per_sync':
                cmd_list.append(("-s %s") % self.arg_dict[key])
            if key == 'workers':
                for w in self.arg_dict[key]:
                    cmd_list.append(("-w %s") % w)
            if key == 'shared_dir':
                cmd_list.append(("-d %s") % self.arg_dict[key])
            if key == 'temp_dir':
                cmd_list.append(("-t %s") % self.arg_dict[key])
            if key == 'rsync_opts':
                cmd_list.append(("-o %s") % self.arg_dict[key])
            if key == 'fpart_opts':
                cmd_list.append(("-O %s") % self.arg_dict[key])
            if key == 'resume':
                cmd_list.append(("-r %s") % self.arg_dict[key])
            if key == 'sudo' and self.arg_dict[key]:
                cmd_list.append("-S")
        cmd_list.append(self.arg_dict["source"])
        cmd_list.append(self.arg_dict["dest"])
        logger.info("sending command: %s" % cmd_list)
        self.cmd_list = cmd_list

    def run_fpsync(self):
        '''
        Fire up fpsync with all our paramerters
        '''
        cmd = " ".join(self.cmd_list)
        print cmd
        try:
            fp_cmd = Popen(cmd,
                           shell=True,
                           stdout=PIPE,
                           stderr=PIPE)
            fp_out, fp_err = fp_cmd.communicate()
        except OSError, e:
            logger.critical("OSError: %s" %e)
        if not fp_err and fp_out:
            print fp_out
        elif fp_err:
            logger.critical("error output: %s" % fp_err)
        self.rc = fp_cmd.returncode

    def release_lock(self):
        logger.info("removing lock file: %s" % self.lock_file)
        os.remove(self.lock_file)

    def process_return_code(self):
        '''
        Drop exit status in facter file for puppet reporting
        '''
        facts_dir = '/etc/facter/facts.d'
        fact_file_name = self.arg_dict["nickname"] + ".yaml"
        fact_file = os.path.join(facts_dir, fact_file_name)
        logger.info("processing rc: %s" % self.rc)
        if self.rc == 0:
            logger.critical("exit 0")
            with open(fact_file, "w") as f:
                f.write("rsnap_%s_backup=success")
        elif self.rc == 1:
            logger.critical("exit 1")
            with open(fact_file, "w") as f:
                f.write("rsnap_%s_backup=failed")
        elif self.rc == 2:
            logger.critical("exit 2")
            with open(fact_file, "w") as f:
                f.write("rsnap_%s_backup=warnning")
        else:
            logger.critical("no exit code!")

    def parse_inputs(self):
        '''
        defining all the command line arguments and parsing those arguments
        into a useable dictionary as well as setting up logger.
        '''
        parser = argparse.ArgumentParser(description="Script to orchestrate \
                                         fpsync jobs from puppet module.")
        parser.add_argument("-a", "--nickname",
                            required=True,
                            default=False,
                            help="Job name or filesystem name")
        parser.add_argument("-s", "--source",
                            required=True,
                            default=False,
                            help="source filesystem")
        parser.add_argument("-d", "--destination",
                            required=True,
                            default=False,
                            help="destination directory")
        parser.add_argument("-n", "--nthreads",
                            required=False,
                            default=None,
                            help="number of threads to pass to fpsync")
        parser.add_argument("-w", "--workers",
                            required=False,
                            default=None,
                            nargs='*',
                            action='append',
                            help="List of worker nodes")
        parser.add_argument("-r", "--rsync_opts",
                            required=False,
                            default=None,
                            help="rsync options to pass")
        parser.add_argument("-p", "--fpart_opts",
                            required=False,
                            default=None,
                            help="fpart options to pass")
        parser.add_argument("-f", "--file_per_sync",
                            required=False,
                            default=None,
                            help="number of files per sync to queue")
        parser.add_argument("-b", "--bytes_per_sync",
                            required=False,
                            default=None,
                            help="number of bytes per sync to queue")
        parser.add_argument("-i", "--shared_dir",
                            required=False,
                            default=None,
                            help="shared dir for use with worker nodes")
        parser.add_argument("-m", "--temp_dir",
                            required=False,
                            default=None,
                            help="shared dir for use with worker nodes")
        parser.add_argument("-e", "--resume",
                            required=False,
                            default=None,
                            help="id to resume a previous transfer")
        parser.add_argument("-o", "--sudo",
                            required=False,
                            default=None,
                            action='store_true',
                            help="use sudo")
        parser.add_argument("-v", "--verbose",
                            required=False,
                            default=False,
                            action='store_true',
                            help="add verbosity")

        args = parser.parse_args()

        # creating a key value dictionary of all the arguments collected.
        arg_dict = {}
        arg_dict['nickname'] = args.nickname
        arg_dict['source'] = args.source
        arg_dict['dest'] = args.destination
        arg_dict['nthreads']= args.nthreads
        worker_list = args.workers
        if worker_list is not None:
            flat_list = []
            for sublist in worker_list:
                for item in sublist:
                    flat_list.append(item)
            arg_dict['workers'] = flat_list
        arg_dict['rsync_opts'] = args.rsync_opts
        arg_dict['fpart_opts'] = args.fpart_opts
        arg_dict['file_per_sync'] = args.file_per_sync
        arg_dict['bytes_per_sync'] = args.bytes_per_sync
        arg_dict['shared_dir'] = args.shared_dir
        arg_dict['temp_dir'] = args.shared_dir
        arg_dict['resume'] = args.resume
        arg_dict['sudo'] = args.sudo
        arg_dict['verbose'] = args.verbose
        # Culling Any arguments that were not set or have "None" value.
        self.arg_dict = {k: v for k, v in arg_dict.items() if v is not None}

        #setting up log location and verbosity
        log_level = logging.INFO
        if args.verbose:
            log_level = logging.DEBUG
        if not os.path.isdir(log_location):
            os.makedirs(log_location)
        log_file = os.path.join(log_location, 'fpsync.log')
        logging.basicConfig(filename=log_file, level=log_level,
                            format=LOG_FORMAT)
        logger.debug(" ".join(sys.argv))


if __name__ == "__main__":
    log_location = '/var/log/fpsync_job'
    LOG_FORMAT = "[%(asctime)s][%(levelname)s] - %(name)s - %(message)s"
    current_date = time.strftime("%Y-%m-%d")
    logger = logging.getLogger(log_location)
    fpsync()
