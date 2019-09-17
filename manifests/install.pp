# @summary
#   Class to install the dependancies of
#   fpsync which is part of the fpart package
#   fpart require epel-release repo be available
#
# @param fpsync_pkg_name
#   Allow you to modify the package name to install.
# @param fpart_ensure
#   Allow you to set ensure values such as installed or version numbers.
# @param epel_ensure
#   Toggle testing for epel resource as a dependancy to installing fpart.
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
}
