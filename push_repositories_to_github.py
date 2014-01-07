import os

from common import *

# Preliminaries.
# --------------
myprint('Obtaining dependencies...')
call('sudo apt-get install curl')

# Put the repositories on GitHub.
# -------------------------------
def push_to_github(local_relpath, github_name, description, private):
    # For background, see `man curl` and
    # http://developer.github.com/v3/repos/.

    # Delete the repository on GitHub, in case it already exists.
    call("curl -u {0} -X DELETE "
            "'https://api.github.com/repos/{0}/{1}'".format(github_username,
                github_name))

    # Create the new repository.
    # http://developer.github.com/guides/getting-started/#create-a-repository
    json_parameters = ('{"name":"%s", '
            '"description": "%s", '
            '"auto_init": false, '
            '"private": %s, '
            '"gitignore_template": "C++"}' % (github_name, description,
                private))
    call("curl -u {0} -d '{1}' https://api.github.com/user/repos".format(
        github_username, json_parameters))

    with cd(os.path.join(git_repos_dir, local_relpath)):
        call('git remote add {0} git@github.com:{0}/{1}.git'.format(
            github_username, github_name))
        call('git push {0} --all'.format(github_username))

push_to_github('cfsqp-working-copy', 'cfsqp', cfsqp_description,
        'true')
push_to_github('opensim-core-working-copy', 'opensim-core',
        opensim_core_description, 'true')
