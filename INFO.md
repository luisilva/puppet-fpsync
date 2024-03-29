# Reference
<!-- DO NOT EDIT: This document was generated by Puppet Strings -->

## Table of Contents

**Classes**

* [`fpsync`](#fpsync): init class to prepare a host for running.
* [`fpsync::install`](#fpsyncinstall): Class to install the dependancies of
fpsync which is part of the fpart package
fpart require epel-release repo be available
* [`fpsync::params`](#fpsyncparams): Class for all tunable parameters for this fpsync module

**Defined types**

* [`fpsync::job`](#fpsyncjob): Scheduale a cronjob to move data between
source and destination while locking a
pid to avoid overruns backup job definition.

## Classes

### fpsync

init class to prepare a host for running.

#### Parameters

The following parameters are available in the `fpsync` class.

##### `manage_repos`

Data type: `Any`

Choose where to manage the repo or except what ever the os already has.

Default value: fpsync::params::manage_repos

### fpsync::install

Class to install the dependancies of
fpsync which is part of the fpart package
fpart require epel-release repo be available

#### Parameters

The following parameters are available in the `fpsync::install` class.

##### `fpsync_pkg_name`

Data type: `Any`

Allow you to modify the package name to install.

Default value: fpsync::params::fpsync_pkg_name

##### `fpart_ensure`

Data type: `Any`

Allow you to set ensure values such as installed or version numbers.

Default value: fpsync::params::fpart_ensure

##### `epel_ensure`

Data type: `Any`

Toggle testing for epel resource as a dependancy to installing fpart.

Default value: fpsync::params::epel_ensure

### fpsync::params

Class for all tunable parameters
for this fpsync module

#### Parameters

The following parameters are available in the `fpsync::params` class.

##### `fpsync_pkg_name`

Data type: `Any`

Allow you to modify the package name to install.

Default value: 'fpart'

##### `fpart_ensure`

Data type: `Any`

Allow you to set ensure values such as installed or version numbers.

Default value: 'installed'

##### `epel_ensure`

Data type: `Any`

Toggle testing for epel resource as a dependancy to installing fpart.

Default value: 'installed'

##### `manage_repos`

Data type: `Any`

Toggle wether repo should be managed by this module.

Default value: `true`

## Defined types

### fpsync::job

Define: fpsync::job

#### Examples

##### Basic usage

```puppet
class { 'fpsync::job':
  source      => '/mnt/source'
  destination => '/backup/destination'
  workers     => ['worker01','worker02']
  hour        => 1
  minute      => 0
}
```

#### Parameters

The following parameters are available in the `fpsync::job` defined type.

##### `source`

Data type: `Any`

source location of the data that will be sync'd. When using fpsync workers
this path must exsist on all worker nodes (Avoid Autofs paths here).

##### `destination`

Data type: `Any`

destination or target of location that the data syncronized to.
 When using fpsync workers this path must exsist on all worker
 nodes (Avoid Autofs paths here).

##### `nthreads`

Data type: `Any`

Integer number of threads you want the job to use for each worker. If
there are no workers assign it will run n threads on localhost.

Default value: 4

##### `workers`

Data type: `Any`

List of remote worker nodes that you would like the fpsync jobs to run on.

Default value: []

##### `rsync_opts`

Data type: `Any`

All options that you would like passed to the rsync application. See
man page for rsync and fpsync for more details.

Default value: '-az --delete --numeric-ids --relative --delete-excluded --exclude=.snapshot --exclude=.glusterfs'

##### `fpart_opts`

Data type: `Any`

All fpart options that would like fpart to run with on execution. please
see fpart man pages for details on all the available options.

Default value: ''

##### `files_per_sync`

Data type: `Any`

[Default: 2000] maximum number of files per sync.

Default value: ''

##### `bytes_per_sync`

Data type: `Any`

[Default: 4294967296 (4 GB)] maximum number of bytes per sync.

Default value: ''

##### `dir`

Data type: `Any`



Default value: ''

##### `temp_dir`

Data type: `Any`

Temp directory that all the rsync logs go into. An empty value there
will default to /tmp/fpsync i perfer the default go in /var/log so it's
colocated with all the other logs and dose not get wiped on reboots.

Default value: '/var/log/fpsync'

##### `resume`

Data type: `Any`

This is a numic id you can set to resume an fpsync job where it last left
off. Not a whole lot of need for this parameter.

Default value: ''

##### `use_sudo`

Data type: `Any`

Tells fpsync to sudo before running command.

Default value: `false`

##### `verbose`

Data type: `Any`

More verbosity to stdout.

Default value: `false`

##### `template`

Data type: `Any`

What template to build script against. This is in the event we want
flip between scripts in future.

Default value: 'fpsync/fpsync.sh.erb'

##### `minute`

Data type: `Any`

Cron job minute parameter.

Default value: fqdn_rand(60)

##### `hour`

Data type: `Any`

Cron job hour parameter.

Default value: fqdn_rand(60)

##### `monthday`

Data type: `Any`

Cron job monthday parameter.

Default value: '*'

##### `month`

Data type: `Any`

Cron job month parameter.

Default value: '*'

##### `weekday`

Data type: `Any`

Cron job minute parameter.

Default value: '*'

##### `ensure`

Data type: `Any`

[default: True] adds and removes the fpsync job.

Default value: present

