import os
import subprocess

# Where are we right now? This SHOULD be the location of the opensim2git git
# repository.
homebase_dir = os.getcwd()

# Find out where we'll be putting the local repositories.
if 'OPENSIMTOGIT_LOCAL_DIR' in os.environ:
    local_dir = os.environ['OPENSIMTOGIT_LOCAL_DIR']
else:
    local_dir = os.path.expanduser('~/opensim2git_local')

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
