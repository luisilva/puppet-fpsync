# @summary init class to prepare a host for running.
#
# @param manage_repos
#   Choose where to manage the repo or except what ever the os already has.
#
class fpsync (
  $manage_repos = fpsync::params::manage_repos,
  ){
  #Get fpsync from epel-release via fpart package
  if $manage_repos {
    include fpsync::install
  }
}
