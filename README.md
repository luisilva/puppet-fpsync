schedule
# fpsync

This module installs fpsync which is a transfer utility that comes bundled
with the fpart application. This module will simply ensure
that fpart is install and by proxy fpsync is available and provide a
mechanism to schedule jobs via crontab.


#### Table of Contents

1. [Description](#description)
3. [Usage](#usage)
5. [Limitations](#limitations)
6. [Development](#development)

## Description

The fpart utility helps you sort file trees and pack them into bags
(called "partitions").

fpsync synchronize directories in parallel using fpart and rsync.

The job define type will orchestrate the the configuration of data
synchronization jobs. This scheduler leverages the cron utility in
puppet in order to run the fpsync job on the desired interval.

### Prerequisites

This has been tested with `'torrancew/cron', '0.1.0'`. This most
cron modules use very similar parameters.

### Beginning with fpsync

including this module will ensure that fpart is install making fpsync
available for scheduling cron jobs.

## Usage

### Install fpsync

```puppet
include fpsync
```

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
More details about classes here: [INFO](INFO.md)
## Limitations

This module is designed for a CentOS 7 environment. Please feel free to make it work for your needs by contributing to this code base.

## Development

Feel free to add feature and contribute to this module.
