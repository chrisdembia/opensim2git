
import os
import time

from common import *

# Preliminaries.
# --------------
start_time = time.time()

# For debugging and development:
normalize_line_endings = False

opensim_legacy_dir = os.path.join(git_repos_dir,
        'opensim-legacy')

opensim_legacy_fs_dir = '/dev/shm/opensim-legacy'

prompt_delete_dir(opensim_legacy_dir)

# Copying svn over to temporary in-memory file system.
# This path ends up in all commit messages as the svn2git metadata.
fspath = '/dev/shm/opensim'

if os.path.exists(fspath): call('rm -rf %s' % fspath)
call('cp -r %s %s' % (svn_mirror_dir, fspath))

if os.path.exists(opensim_legacy_fs_dir):
    call('rm -rf %' % opensim_legacy_fs_dir)
call('mkdir %s' % opensim_legacy_fs_dir)

# svn2git
# -------
myprint('Running svn2git for opensim-legacy.')
with cd(opensim_legacy_fs_dir):

    # Write output to log files.
    out = open('%s/svn2git_progress_log.txt' % opensim_legacy_fs_dir,
            'w')
    err = open('%s/svn2git_error_log.txt' % opensim_legacy_fs_dir, 'w')

    call("svn2git file://%s "
            "--trunk Trunk "
            "--tags Tags "
            "--branches Branches "
            "--authors %s/authors.txt "
            "--verbose "
            "--username %s "
            "--metadata " % (fspath, homebase_dir, username),
            stdout=out,
            stderr=err)
    out.close()
    err.close()

    # Edit 'description' file, which is used by GitWeb (run `$ git instaweb`).
    call('echo "opensim-legacy: %s" '
            '> %s/.git/description' % (
                opensim_legacy_description,
                opensim_legacy_fs_dir))

call('cp -r %s %s' % (opensim_legacy_fs_dir, opensim_legacy_dir))

myprint('Clean up in-memory files')
call('rm -rf %s' % fspath)
call('rm -rf %s' % opensim_legacy_fs_dir)
    
if normalize_line_endings:
    filter_branch_tasks(opensim_legacy_dir)

git_garbage_collection(opensim_legacy_dir)

repository_size(opensim_legacy_dir)

# Tell the user how long opensim2git ran for.
elapsed_time = time.time() - start_time
myprint("Took %.1f minutes." % (elapsed_time / 60.0))
