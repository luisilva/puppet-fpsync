schedule
# fpsync

This module installs fpsync which is a transfer utility that comes bundled
with the fpart application. This module will simply ensure
that fpart is install and by proxy fpsync is available and provide a
mechanism to schedule jobs.


#### Table of Contents

1. [Description](#description)
2. [Setup - The basics of getting started with fpsync](#setup)
    * [What fpsync affects](#what-fpsync-affects)
    * [Setup requirements](#setup-requirements)
    * [Beginning with fpsync](#beginning-with-fpsync)
3. [Usage - Configuration options and additional functionality](#usage)
4. [Reference - An under-the-hood peek at what the module is doing and how](#reference)
5. [Limitations - OS compatibility, etc.](#limitations)
6. [Development - Guide for contributing to the module](#development)

## Description

The fpart utility helps you sort file trees and pack them into bags
(called "partitions").

fpsync synchronize directories in parallel using fpart and rsync.

The job define type will orchestrate the the configuration of data
synchronization jobs. This scheduler leverages the cron utility in
puppet in order to run the fpsync job on the desired interval.

## Setup


### Prerequisites

This has been tested with `'torrancew/cron', '0.1.0'`. This most
cron modules use very similar parameters.

### Beginning with fpsync

including this module will ensure that fpart is install making fpsync
available for scheduling cron jobs.

## Usage

### Install and enable NTP

```puppet
include fpsync
```
## Reference

### fpsync jobs

* Using job defined type to schedule a cron job to repeatedly attempt file
synchronization.
#### puppet
```puppet
class { 'fpsync::job':
    source      => '/mnt/source'
    destination => '/backup/destination'
    workers     => ['worker01','worker02']
    hour        => 1
    minute      => 0
}
```
#### Hiera
```yaml
fpsync::job:
    source: '/mnt/source'
    destination: '/backup/destination'
    workers:
      - 'worker01'
      - 'worker02'
    hour: 1
    minute: 0
```

* If you are not using Puppet Strings, include a list of all of your classes, defined types, and so on, along with their parameters. Each element in this listing should include:

  * The data type, if applicable.
  * A description of what the element does.
  * Valid values, if the data type doesn't make it obvious.
  * Default value, if any.

## Limitations

This is where you list OS compatibility, version compatibility, etc. If there are Known Issues, you might want to include them under their own heading here.

## Development

Since your module is awesome, other users will want to play with it. Let them know what the ground rules for contributing are.

## Release Notes/Contributors/Etc. **Optional**

If you aren't using changelog, put your release notes here (though you should consider using changelog). You can also add any additional sections you feel are necessary or important to include here. Please use the `## ` header.
