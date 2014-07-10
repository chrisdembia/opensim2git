"""
Example:
    $ ipython push_repositories_to_github.py ~/opensim2git_local/ruby_git_repos

"""

import os
import sys

from common import *

# Preliminaries.
# --------------
myprint('Obtaining dependencies...')
call('sudo apt-get install curl')

git_repos_dir = os.path.join(local_dir, 'ruby_git_repos')

# Find out where we'll be publishing the repositories on GitHub.
if 'OPENSIMTOGIT_GITHUB_USERNAME' in os.environ:
    github_username = os.environ['OPENSIMTOGIT_GITHUB_USERNAME']
else:
    github_username = raw_input('Enter your GitHub username: ')

# Put the repositories on GitHub.
# -------------------------------
def push_to_github(local_relpath, description, private):
    # For background, see `man curl` and
    # http://developer.github.com/v3/repos/.

    myprint('Pushing %s' % local_relpath)

    github_name = local_relpath

    # Delete the repository on GitHub, in case it already exists.
    #call("curl -u {0} -X DELETE "
    #        "'https://api.github.com/repos/opensim-org/{1}'".format(github_username,
    #            github_name))

    # Create the new repository.
    # http://developer.github.com/guides/getting-started/#create-a-repository
    json_parameters = ('{"name":"%s", '
            '"description": "%s", '
            '"auto_init": false, '
            '"private": %s, '
            '"homepage": "opensim.stanford.edu", '
            '"team_id": 501023, '
            '"gitignore_template": "C++"}' % (github_name, description,
                private))
    call("curl -u {0} -d '{1}' https://api.github.com/orgs/opensim-org/repos".format(
        github_username, json_parameters))

    with cd(os.path.join(git_repos_dir, local_relpath)):
        call('git remote rm opensim-org')
        call('git remote add opensim-org git@github.com:opensim-org/{0}.git'.format(
            github_name))
        call('git push opensim-org --all')
        call('git push opensim-org --tags')

#push_to_github('cfsqp', cfsqp_description, 'true')
#push_to_github('opensim-core', opensim_core_description, 'true')
#push_to_github('opensim-legacy',
#        opensim_legacy_description, 'true')
#push_to_github('opensim-models', opensim_models_description, 'true')
push_to_github('opensim-gui', opensim_gui_description, 'true')
