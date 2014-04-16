import os
from os.path import join
import shutil
import subprocess
import sys
import datetime

date = datetime.date.today()
datestr = date.strftime('%Y %B %d')

if len(sys.argv) >= 2 and sys.argv[1] == '--auton':
    auto_delete = True
else:
    auto_delete = False


# Where are we right now? This SHOULD be the location of the opensim2git git
# repository.
homebase_dir = os.getcwd()

svn_repo_path = 'https://simtk.org/svn/opensim'

# Find out where we'll be putting the local repositories.
if 'OPENSIMTOGIT_LOCAL_DIR' in os.environ:
    local_dir = os.environ['OPENSIMTOGIT_LOCAL_DIR']
else:
    local_dir = os.path.expanduser('~/opensim2git_local')

# Creating an svn mirror requires a simtk user name.
if 'OPENSIMTOGIT_SIMTK_USERNAME' in os.environ:
    username = os.environ['OPENSIMTOGIT_SIMTK_USERNAME']
else:
    username = raw_input('Enter your simtk username: ')

def myprint(string):
    print("\n[opensim2git] %s" % string)

def call(command, *args, **kwargs):
    print('Running: %s' % command)
    subprocess.call(command, *args, shell=True, **kwargs)

# Descriptions of the repositories we'll create. We need this more than once.
cfsqp_description = ('CFSQP (C implementation of Feasible Sequential '
        'Quadratic Programming) optimization library, for use with '
            'SimTK OpenSim.')
opensim_core_description = ('SimTK OpenSim C++ libraries/applications and '
            'Java/Python wrapping.')
opensim_models_description = ('SimTK OpenSim models (.osim) and related example '
        'files that are distributed with OpenSim.')
opensim_legacy_description = ('Complete history of the '
        "OpenSim project up through %s . This repository is not for "
        "development; it is "
        "only for reference." % datestr)

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

def prompt_delete_dir(my_dir):
    myprint('Deleting pre-existing %s. ' % my_dir)
    # To prevent weird overwriting from occurring, remove the previous work.
    if os.path.exists(my_dir):
        if auto_delete:
            shutil.rmtree(my_dir)
        else:
            input = raw_input('Okay? (y/n) ')
            if input[0] == 'y':
                shutil.rmtree(my_dir)
            else:
                sys.exit('Aborting. Will not overwrite pre-existing work.')

# Normalize line endings.
# -----------------------
# Convert all line endings from CRLF (windows) to LF (unix).
# http://blog.gyoshev.net/2013/08/normalizing-line-endings-in-git-repositories/
# There's an easy way to do this, but it has a significant downside: if you
# use blame on any line after this change, it'll point to this one commit
# that changed the line endings. We use a different method: rewrite the
# history.
# List all files in a dir with CRLF:
# http://stackoverflow.com/questions/73833/how-do-you-search-for-files-containing-dos-line-endings-crlf-with-grep-on-linu
# http://stackoverflow.com/questions/1532405/how-to-view-git-objects-and-index-without-using-git
# The history:
# http://adaptivepatchwork.com/2012/03/01/mind-the-end-of-your-line/
fspath = '/dev/shm/opensim2git_temp_repo'
class cd_normalize(cd):
    def __enter__(self, *args):
        if os.path.exists(fspath): os.removedirs(fspath)
        super(cd_normalize, self).__enter__(*args)
    def __exit__(self, *args):
        if os.path.exists(fspath): os.removedirs(fspath)
        super(cd_normalize, self).__exit__(*args)

def filter_branch_tasks(repo_path):
    myprint('Normalizing line endings...')
    with cd_normalize(repo_path):
        # Fix all inconsistent line endings from the history.
        # '-d' flag makes in-memory file system: should speed up the operation.
        call("git filter-branch "
                "--force "
                "--tree-filter '%s/normalize_line_endings.sh' "
                "--prune-empty "
                "--tag-name-filter cat "
                "-d %s "
                "-- --all" % (homebase_dir, fspath),
                )

        #  Ensure consistent line endings in the future.
        # http://stackoverflow.com/questions/1510798/trying-to-fix-line-endings-with-git-filter-branch-but-having-no-luck/1511273#1511273
        call('echo "* text=auto" >> .gitattributes')
        call('git add .gitattributes')
        call('git commit -am "Introduce end-of-line normalization."')

# Garbage collect.
# ----------------
# Make the repositories smaller.
def git_garbage_collection(repo_path):
    myprint('Running git garbage collection to reduce repository size...')
    with cd(repo_path):
        # Remove backup of the files we deleted from the history (may not be
        # necessary here, because we do not delete files from the history).
        call('rm -rf .git/refs/original')
        call('git reflog expire --expire=now --all')
        call('git gc --prune=now')
        call('git gc --aggressive --prune=now')

# How big are the repositories?
# -----------------------------
def repository_size(repo_path):
    with cd(repo_path):
        myprint('Size of %s/.git:' % os.path.split(repo_path)[-1])
        call('du .git -s -h')
        myprint('Size of %s:' % os.path.split(repo_path)[-1])
        call('du . -s -h')


# Preliminaries.
# --------------
git_repos_dir = os.path.join(local_dir, 'ruby_git_repos')

# Try to install svn2git.
myprint('Obtaining dependencies...')
os.system('sudo apt-get install git-core git-svn ruby rubygems')

with cd('svn2git'):
    os.system('git submodule init')
    os.system('git submodule update')
    os.system('gem build svn2git.gemspec')
    os.system('sudo gem install svn2git-2.2.2.gem')

# svn mirror.
# -----------

# We need a local mirror of the svn repository.
svn_mirror_dir = join(local_dir, 'svn_mirror')

myprint('Setting up svn mirror of original OpenSim repository...')
if not os.path.exists(join(svn_mirror_dir, 'hooks', 'pre-revprop-change')):
    # http://cournape.wordpress.com/2007/12/18/making-a-local-mirror-of-a-subversion-repository-using-svnsync/
    os.makedirs(svn_mirror_dir)

    # Create the repository.
    call('svnadmin create %s' % svn_mirror_dir)

    # Just to see if the repository is in the correct location.
    call('svn info file://%s' % svn_mirror_dir)

    # Create a hook so that you can modify revprops, which is necessary for the
    # mirror.

    # If the mirror hasn't been made yet, make it.
    # We'll use this in a bit:
    revprop_hook_content = """#!/bin/sh
USER="$3"
if [ "$USER" = "{0}" ]; then exit 0; fi
echo "Only the {0} user can change revprops" >&2
exit 1
""".format(username)

    hook = open(join(svn_mirror_dir, 'hooks', 'pre-revprop-change'), 'w')
    hook.write(revprop_hook_content)
    hook.close()

    # Make the hook executable.
    call('chmod +x %s/hooks/pre-revprop-change' % svn_mirror_dir)

    # Set up the synchronization.
    call('svnsync init --username %s file://%s %s' % (username, svn_mirror_dir,
        opensim_svn_url))

# Sync the mirror.
call('svnsync sync file://%s' % svn_mirror_dir)
