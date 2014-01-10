import os
from os.path import join
import shutil
import sys
import time

from common import *

# Preliminaries.
# --------------
start_time = time.time()

# This is where we'll put the git repositories.
git_repos_dir = os.path.join(local_dir, 'kde_git_repos')

opensim_svn_url = 'https://simtk.org/svn/opensim'

# We need a local mirror of the svn repository.
svn_mirror_dir = join(local_dir, 'svn_mirror')

# Obtain dependencies. Requires sudo access.
myprint('Obtaining dependencies...')
call('sudo apt-get install svn-all-fast-export dos2unix curl')

# svn mirror.
# -----------
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
    call('chmod +x %s/hooks/pre-revprop-change' % svn_mirror_dir)

    # Set up the synchronization.
    call('svnsync init --username %s file://%s %s' % (username, svn_mirror_dir,
        opensim_svn_url))

# Sync the mirror.
call('svnsync sync file://%s' % svn_mirror_dir)


# Create git repositories.
# ------------------------
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

# We want the repo to end up in git_repos_dir, so we cd there.
with cd(git_repos_dir):

    # Run svn-all-fast-export.
    myprint('Creating git repositories...')

    # Write output to log files.
    out = open('svn-all-fast-export_progress_log.txt', 'w')
    err = open('svn-all-fast-export_error_log.txt', 'w')

    call("svn-all-fast-export "
            "--rules {0}/rules.conf "
            "--debug-rules "
            "--add-metadata "
            "--identity-map {0}/authors.txt "
            "--stats "
#            "--resume-from 8400 "
#            "--max-rev 1095 "
            "{1}".format(homebase_dir, svn_mirror_dir),
            stdout=out,
            stderr=err,
            )

    # TODO the resulting cfsqp repository does not contain sampl files.

    out.close()
    err.close()


    # Get working copies.
    myprint('Create working-copy clones of new git repositories...')
    call("git clone cfsqp cfsqp-working-copy")
    call("git clone opensim-core opensim-core-working-copy")

    # Edit 'description' file, which is used by GitWeb (run `$ git instaweb`).
    call('echo "opensim-core: %s" '
            '> %s/opensim-core-working-copy/.git/description' % (
                opensim_core_description, git_repos_dir))

    call('echo "cfsqp: %s" > %s/cfsqp-working-copy/.git/description' % (
        cfsqp_description, git_repos_dir))

# Normalize line endings.
# Convert all line endings from CRLF (windows) to LF (unix).
# http://blog.gyoshev.net/2013/08/normalizing-line-endings-in-git-repositories/
# There's an easy way to do this, but it has a significant downside: if you
# use blame on any line after this change, it'll point to this one commit
# that changed the line endings. We use a different method: rewrite the
# history.
myprint('Normalizing line endings...')
fspath = '/dev/shm/opensim2git_temp_repo'
class cd_normalize(cd):
    def __enter__(self, *args):
        if os.path.exists(fspath): os.removedirs(fspath)
        super(cd_normalize, self).__enter__(*args)
    def __exit__(self, *args):
        if os.path.exists(fspath): os.removedirs(fspath)
        super(cd_normalize, self).__exit__(*args)

def filter_branch_tasks(repo_name):
    repo_path = join(git_repos_dir, repo_name)
    with cd_normalize(repo_path):
        # Fix all inconsistent line endings from the history.
        # '-d' flag makes in-memory file system: should speed up the operation.

        # Also, remove certain files from the history.
        # https://help.github.com/articles/remove-sensitive-data
        call("git filter-branch "
                "--force "
                "--tree-filter '%s/normalize_line_endings.sh' "
                "--index-filter "
                "'git rm -r --cached --ignore unmatch "
                "OpenSim/Wrapping/Java/OpenSimJNI/OpenSimJNI_wrap.* "
                "OpenSim/Java/OpenSimJNI/OpenSimJNI_wrap.* "
                #"Vendors/CFSQP "
                "' "
                "--prune-empty "
                "--tag-name-filter cat "
                "-d %s "
                "-- --all" % (homebase_dir, fspath),
                )

        #  Ensure consistent line endings in the future.
        # http://stackoverflow.com/questions/1510798/trying-to-fix-line-endings-with-git-filter-branch-but-having-no-luck/1511273#1511273
        call('echo "* text=auto" >> .gitattributes')
        call('git add .gitattributes')
        call('git commit -m "Introduce end-of-line normalization."')

filter_branch_tasks('cfsqp-working-copy')
filter_branch_tasks('opensim-core-working-copy')

# Garbage collect.
# ----------------
# Make the repositories smaller.
myprint('Running git garbage collection to reduce repository size...')
def git_garbage_collection(repo_name):
    repo_path = join(git_repos_dir, repo_name)
    with cd(repo_path):
        # Remove backup of the files we deleted from the history.
        call('rm -rf .git/refs/original')
        call('git reflog expire --expire=now --all')
        call('git gc --prune=now')
        call('git gc --aggressive --prune=now')

git_garbage_collection('cfsqp-working-copy')
git_garbage_collection('opensim-core-working-copy')

# Make CFSQP a standalone project.
# --------------------------------
with cd(join(git_repos_dir, 'cfsqp-working-copy')):
    call('cp %s/CMakeLists_cfsqp_standalone.txt CMakeLists.txt' % homebase_dir)
    call('git add CMakeLists.txt')
    call('git commit -m"Make this project standalone."')

# Tell the user how long opensim2git ran for.
elapsed_time = time.time() - start_time
myprint("Took %.1f minutes." % (elapsed_time / 60.0))
