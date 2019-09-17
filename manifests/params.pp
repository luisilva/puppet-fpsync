# Class for all tunable parameters
# for this fpsync module
#
# @param fpsync_pkg_name
#   Allow you to modify the package name to install.
# @param fpart_ensure
#   Allow you to set ensure values such as installed or version numbers.
# @param epel_ensure
#   Toggle testing for epel resource as a dependancy to installing fpart.
# @param manage_repos
#   Toggle wether repo should be managed by this module.
#
class fpsync::params (
  $fpart_ensure    = 'installed',
  $fpsync_pkg_name = 'fpart',
  $epel_ensure     = 'installed',
  $manage_repos    = true,
) {
}
