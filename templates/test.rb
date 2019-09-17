require 'erb'

class Test_erb
  def initialize( source, destination, nthreads, workers, rsync_opts, fpart_opts, files_per_sync, bytes_per_sync, dir, temp_dir, resume, use_sudo, verbose)
    @source = source
    @destination = destination
    @nthreads = nthreads
    @workers = workers
    @rsync_opts = rsync_opts
    @fpart_opts = fpart_opts
    @files_per_sync = files_per_sync
    @bytes_per_sync = bytes_per_sync
    @dir = dir
    @temp_dir = temp_dir
    @resume = resume
    @use_sudo = use_sudo
    @verbose = verbose
    temp = ERB.new File.read("fpsync.sh.erb")
    puts temp.result(binding)
  end
end

test1 = Test_erb.new('/source/1',
                     '/dest/1',
                     4,
                     (["root@bulfsbu01", "root@lfsbu02"]),
                     '-az --delete --numeric-ids --relative --delete-excluded --exclude=.snapshot --exclude=.glusterfs',
                     '-f 10000',
                     '',
                     '',
                     '',
                     '/var/log/fpsync',
                     '',
                     false,
                     true )
