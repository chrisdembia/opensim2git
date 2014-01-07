import os
import subprocess

# Find out where we'll be putting the local repositories.
if 'OPENSIMTOGIT_LOCAL_DIR' in os.environ:
    local_dir = os.environ['OPENSIMTOGIT_LOCAL_DIR']
else:
    local_dir = os.path.expanduser('~/opensim2git_local')

# Find out where we'll be publishing the repositories on GitHub.
if 'OPENSIMTOGIT_GITHUB_USERNAME' in os.environ:
    github_username = os.environ['OPENSIMTOGIT_GITHUB_USERNAME']
else:
    github_username = raw_input('Enter your GitHub username: ')

# This is where we'll put the git repositories.
git_repos_dir = os.path.join(local_dir, 'git_repos')

def myprint(string):
    print("\n[opensim2git] %s" % string)

def call(command, *args, **kwargs):
    subprocess.call(command, *args, shell=True, **kwargs)

# Descriptions of the repositories we'll create. We need this more than once.
cfsqp_description = ('CFSQP (C implementation of Feasible Sequential '
        'Quadratic Programming) optimization library, for use with '
            'SimTK OpenSim.')
opensim_core_description = ('SimTK OpenSim C++ libraries/applications and '
            'Java/Python wrapping.')

# To work in a different directory.
class cd(object):
    """See http://stackoverflow.com/questions/431684/how-do-i-cd-in-python"""
    def __init__(self, new_path):
        self.new_path = new_path
    def __enter__(self):
        self.orig_path = os.getcwd()
        os.chdir(self.new_path)
    def __exit__(self, etype, value, traceback):
        os.chdir(self.orig_path)
