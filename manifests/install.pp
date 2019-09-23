# @summary
#   Class to install the dependancies of
#   fpsync which is part of the fpart package
#   fpart require epel-release repo be available
#
class fpsync::install (
  $fpsync_pkg_name = fpsync::params::fpsync_pkg_name,
  $fpart_ensure    = fpsync::params::fpart_ensure,
  $epel_ensure     = fpsync::params::epel_ensure,
  ){
  if $params::manage_repos {
    package { 'epel-release':
      ensure => $epel_ensure,
    }
    package { '$fpsync_pkg_name':
      ensure  => $fpart_ensure,
      require => Package['epel-release']
    }
  }
  file { '/usr/local/bin/fpsync.py':
    source => 'puppet:///modules/fpsync/fpsync.py',
    owner  => root,
    group  => root,
    mode   => '0755',
    backup => true,
  }
}
