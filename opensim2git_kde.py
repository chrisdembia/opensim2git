import os
from os.path import join
import shutil
from subprocess import call
import sys
import time

start_time = time.clock()

# Preliminaries.
# --------------
opensim_svn_url = 'https://simtk.org/svn/opensim'

# Find out where we'll be putting the local repositories.
if 'OPENSIMTOGIT_LOCAL_DIR' in os.environ:
    local_dir = os.environ['OPENSIMTOGIT_LOCAL_DIR']
else:
    local_dir = os.path.expanduser('~/opensim2git_local')

# Where are we right now? This SHOULD be the location of the opensim2git git
# repository.
homebase_dir = os.getcwd()

# This is where we'll put the git repositories.
git_repos_dir = join(local_dir, 'git_repos')

# We need a local mirror of the svn repository.
svn_mirror_dir = join(local_dir, 'svn_mirror')

def myprint(string):
    print("\n[opensim2git] %s" % string)

# svn mirror.
# -----------
myprint('Setting up svn mirror of original OpenSim repository...')
if not os.path.exists(join(svn_mirror_dir, 'hooks', 'pre-revprop-change')):
    # http://cournape.wordpress.com/2007/12/18/making-a-local-mirror-of-a-subversion-repository-using-svnsync/
    os.makedirs(svn_mirror_dir)

    # Create the repository.
    call('svnadmin create %s' % svn_mirror_dir, shell=True)

    # Just to see if the repository is in the correct location.
    call('svn info file://%s' % svn_mirror_dir, shell=True)

    # Create a hook so that you can modify revprops, which is necessary for the
    # mirror.

    # Creating an svn mirror requires a simtk user name.
    username = raw_input('Enter your simtk username: ')

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
    call('chmod +x %s/hooks/pre-revprop-change' % svn_mirror_dir, shell=True)

    # Set up the synchronization.
    call('svnsync init --username %s file://%s %s' % (username, svn_mirror_dir,
        opensim_svn_url), shell=True)

# Sync the mirror.
call('svnsync sync file://%s' % svn_mirror_dir, shell=True)

# To prevent weird overwriting from occurring, remove the previous work.
if os.path.exists(git_repos_dir):
    input = raw_input('Deleting pre-existing %s. Okay? (y/n) ' % git_repos_dir)
    if input[0] == 'y':
        shutil.rmtree(git_repos_dir)
    else:
        sys.exit('Aborting. Will not overwrite pre-existing work.')

# Make git_repos_dir. Do this before we require the user to `sudo`, so that
# we know the user has permission to write in git_repos_dir.
os.makedirs(git_repos_dir)

# Obtain dependencies. Requires sudo access.
myprint('Obtaining dependencies...')
call('sudo apt-get install svn-all-fast-export dos2unix', shell=True)

# Do the rest of the operations in the OPENSIMTOGIT_LOCAL_DIR.
class cd:
    """See http://stackoverflow.com/questions/431684/how-do-i-cd-in-python"""
    def __init__(self, new_path):
        self.new_path = new_path
    def __enter__(self):
        self.orig_path = os.getcwd()
        os.chdir(self.new_path)
    def __exit__(self, etype, value, traceback):
        os.chdir(self.orig_path)

# We want the repo to end up in git_repos_dir, so we cd there.
with cd(git_repos_dir):

    # Run svn-all-fast-export.
    myprint('Creating git repositories...')

    # Write output to log files.
    out = open('svn-all-fast-export_progress_log.txt', 'w')
    err = open('svn-all-fast-export_error_log.txt', 'w')

    call("svn-all-fast-export "
            "--rules {0}/opensim2git.rules "
            "--debug-rules "
            "--add-metadata "
            "--identity-map {0}/authors.txt "
            "--stats "
            "{1}".format(homebase_dir, svn_mirror_dir),
            shell=True,
            stdout=out,
            stderr=err,
            )

    # TODO the resulting cfsqp repository does not contain sampl files.

    out.close()
    err.close()

    # Get working copies.
    myprint('Create working-copy clones of new git repositories...')
    call("git clone cfsqp cfsqp-working-copy", shell=True)
    call("git clone opensim-core opensim-core-working-copy", shell=True)

# Normalize line endings.
# Convert all line endings from CRLF (windows) to LF (unix).
# http://blog.gyoshev.net/2013/08/normalizing-line-endings-in-git-repositories/
# There's an easy way to do this, but it has a significant downside: if you
# use blame on any line after this change, it'll point to this one commit
# that changed the line endings. We use a different method: rewrite the
# history.
myprint('Normalizing line endings...')
def normalize_line_endings(repo_name):
    repo_path = join(git_repos_dir, repo_name)
    with cd(repo_path):
        fspath = '/dev/shm/repo_temp'
        if os.path.exists(fspath):
            os.removedirs(fspath)
        # Fix all inconsistent line endings from the history.
        # In-memory file system: should speed up the operation.
        call("git filter-branch --tree-filter '%s/normalize_line_endings.sh' "
                "-d %s "
                "-- --all" % (homebase_dir, fspath),
                shell=True)
        if os.path.exists(fspath): os.removedirs(fspath)

        #  Ensure consistent line endings in the future.
        # http://stackoverflow.com/questions/1510798/trying-to-fix-line-endings-with-git-filter-branch-but-having-no-luck/1511273#1511273
        call('echo "* text=auto" >> .gitattributes', shell=True)
        call('git add .gitattributes', shell=True)
        call('git commit -m "Introduce end-of-line normalization"', shell=True)

normalize_line_endings('cfsqp-working-copy')
normalize_line_endings('opensim-core-working-copy')

# Tell the user how long opensim2git ran for.
elapsed_time = time.clock() - start_time
myprint("Took %.1f seconds." % elapsed_time)
