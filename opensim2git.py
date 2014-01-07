import os
import shutil
from subprocess import call
import sys

# Find out where we'll be putting the local repositories.
if 'OPENSIMTOGIT_LOCAL_DIR' in os.environ:
    local_dir = os.environ['OPENSIMTOGIT_LOCAL_DIR']
else:
    local_dir = os.path.expanduser('~/opensim_git_repos')

# To prevent weird overwriting from occurring, remove the previous work.
if os.path.exists(local_dir):
    input = raw_input('Deleting pre-existing %s. Okay? (y/n) ' % local_dir)
    if input[0] == 'y':
        shutil.rmtree(local_dir)
    else:
        sys.exit('Aborting. Will not overwrite pre-existing work.')
else:
    # Make local_dir. Do this before we require the user to `sudo`, so that we
    # know the user has permission to write in local_dir.
    os.makedirs(local_dir)

# Try to install svn2git.
os.system('sudo apt-get install git-core git-svn ruby rubygems')
os.system('sudo gem install svn2git')

# Do the rest of the operations in the OPENSIMTOGIT_LOCAL_DIR.
class cd:
    """See http://stackoverflow.com/questions/431684/how-do-i-cd-in-python"""
    def __init__(self, new_path):
        self.new_path = new_path
    def __enter__(self):
        self.orig_path = os.getcwd()
        os.chdir(self.new_path)
        return self.orig_path
    def __exit__(self, etype, value, traceback):
        os.chdir(self.orig_path)

# Make the directory where we'll run svn2git.
core_dir = "%s/opensim-core" % local_dir
if not os.path.exists(core_dir): os.makedirs(core_dir)

# Get username and password.
username = raw_input('Enter your simtk username: ')

# We want the repo to end up in core_dir, so we cd there.
with cd(core_dir) as orig_path:

    # Run svn2git.
    print('Running svn2git.')
    print("Enter your simtk password, hit enter, then enter your "
            "password again, and hit enter (there's a bug). "
            "Then, nothing will appear to happen, but don't worry, "
            "it's working. See %s for progress." % core_dir)

    # Write output to log files.
    out = open('%s/svn2git_progress_log.txt' % core_dir, 'w')
    err = open('%s/svn2git_error_log.txt' % core_dir, 'w')

    # We have to do some funky stuff to give the repo password to svn2git,
    # because its own prompt is unclear.
    # https://github.com/nirvdrum/svn2git/issues/59
    call("svn2git https://simtk.org/svn/opensim "
            "--trunk Trunk "
            "--tags Tags "
            "--branches Branches "
            "--authors %s/authors.txt "
            "--verbose "
            "--username %s "
            "--exclude '.*CFSQP.*' "
            "--exclude 'Gui' "
            "--nobranches " # TODO YES branches once svn2git is fixed.
            "--notags "
            "--revision 6663 "
            "--metadata " % (orig_path, username),
            shell=True,
            stdout=out,
            stderr=err)
    out.close()
    err.close()
