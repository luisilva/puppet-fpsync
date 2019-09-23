# Define: fpsync::job
#
# @summary
#   Scheduale a cronjob to move data between
#   source and destination while locking a
#   pid to avoid overruns backup job definition.
#
# @example Basic usage
#   class { 'fpsync::job':
#     source      => '/mnt/source'
#     destination => '/backup/destination'
#     workers     => ['worker01','worker02']
#     hour        => 1
#     minute      => 0
#   }
#
# @param source
#   source location of the data that will be sync'd. When using fpsync workers
#   this path must exsist on all worker nodes (Avoid Autofs paths here).
# @param destination
#   destination or target of location that the data syncronized to.
#    When using fpsync workers this path must exsist on all worker
#    nodes (Avoid Autofs paths here).
# @param nthreads
#   Integer number of threads you want the job to use for each worker. If
#   there are no workers assign it will run n threads on localhost.
# @param workers
#   List of remote worker nodes that you would like the fpsync jobs to run on.
# @param rsync_opts
#   All options that you would like passed to the rsync application. See
#   man page for rsync and fpsync for more details.
# @param fpart_opts
#   All fpart options that would like fpart to run with on execution. please
#   see fpart man pages for details on all the available options.
# @param files_per_sync
#   [Default: 2000] maximum number of files per sync.
# @param bytes_per_sync
#   [Default: 4294967296 (4 GB)] maximum number of bytes per sync.
# @param dir
#   set fpsync shared dir to </dir/> (absolute path)
#   This option is mandatory when using SSH workers.
# @param temp_dir
#   Temp directory that all the rsync logs go into. An empty value there
#   will default to /tmp/fpsync i perfer the default go in /var/log so it's
#   colocated with all the other logs and dose not get wiped on reboots.
# @param resume
#   This is a numic id you can set to resume an fpsync job where it last left
#   off. Not a whole lot of need for this parameter.
# @param use_sudo
#   Tells fpsync to sudo before running command.
# @param verbose
#   More verbosity to stdout.
# @param template
#   What template to build script against. This is in the event we want
#   flip between scripts in future.
# @param minute
#   Cron job minute parameter.
# @param hour
#   Cron job hour parameter.
# @param monthday
#   Cron job monthday parameter.
# @param month
#   Cron job month parameter.
# @param weekday
#   Cron job minute parameter.
# @param ensure
#   [default: True] adds and removes the fpsync job.
#
define fpsync::job (
  $source,
  $destination,
  $nthreads         = 4,
  $workers          = [],
  $rsync_opts       = '-az --delete --numeric-ids --relative --delete-excluded --exclude=.snapshot --exclude=.glusterfs',
  $fpart_opts       = '',
  $files_per_sync   = '',
  $bytes_per_sync   = '',
  $dir              = '',
  $temp_dir         = '/var/log/fpsync',
  $resume           = '',
  $use_sudo         = false,
  $verbose          = false,
  $template         = 'fpsync/fpsync.sh.erb',
  $minute          = fqdn_rand(60),
  $hour            = fqdn_rand(60),
  $monthday        = '*',
  $month           = '*',
  $weekday         = '*',
  $ensure           = present,
  ) {

  # ensure fpart is installed and available
  include fpsync

  # Make sure destination doesn't end in /, since we use the basename of it
  # to construct the nickname used in filenames.
  if $destination =~ /^.*\/$/ {
    fail("destination [${destination}] must not end with / character")
  }

  # subdir must always have a leading ./
  if $source !~ /^\.\// {
    fail("source path ${source} must start with './'")
  }
  # The simple name used in the config, log, pid, etc. files.
  $nickname = regsubst($destination, '.*/', '')  # basename($destination)
  file { "/etc/fpsync/${nickname}.sh":
  ensure         => $ensure,
  content        => template($template),
  source         => $source,
  destination    => $destination,
  nthreads       => $nthreads,
  workers        => $workers,
  rsync_opts     => $rsync_opts,
  fpart_opts     => $fpart_opts,
  files_per_sync => $files_per_sync,
  bytes_per_sync => $bytes_per_sync,
  dir            => $dir,
  temp_dir       => $temp_dir,
  resume         => $resume,
  use_sudo       => $use_sudo,
  verbose        => $verbose,
  }

  cron { "storage_backup_job_${nickname}":
    ensure   => $ensure,
    command  => "/etc/fpsync/${nickname}.sh",
    minute   => $minute,
    hour     => $hour,
    monthday => $monthday,
    month    => $month,
    weekday  => $weekday,
  }
}
