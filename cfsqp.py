
import os
import time

from common import *

# Preliminaries.
# --------------
start_time = time.time()

cfsqp_dir = os.path.join(git_repos_dir, 'cfsqp')

prompt_delete_dir(cfsqp_dir)
os.makedirs(cfsqp_dir)

# svn2git
# -------
myprint('Running svn2git for cfsqp.')
with cd(cfsqp_dir):

    # Write output to log files.
    out = open('%s/svn2git_cfsqp_progress_log.txt' % cfsqp_dir, 'w')
    err = open('%s/svn2git_cfsqp_error_log.txt' % cfsqp_dir, 'w')

    # TODO subprocess.call may be causing the threading issues.
    call("svn2git file://%s "
            "--trunk Trunk/Vendors/CFSQP "
            "--authors %s/authors.txt "
            "--verbose "
            "--username %s "
            "--nobranches " # TODO YES branches once svn2git is fixed.
            "--notags "
            "--revision 1053 "
            "--metadata " % (svn_mirror_dir, homebase_dir, username),
            stdout=out,
            stderr=err)
    out.close()
    err.close()

    call('echo "cfsqp: %s" > %s/.git/description' % (
        cfsqp_description, cfsqp_dir))
    
filter_branch_tasks(cfsqp_dir, ['master'])

git_garbage_collection(cfsqp_dir)

# Make CFSQP a standalone project.
# --------------------------------
with cd(cfsqp_dir):
    call('git apply %s/cfsqp_standalone.patch' % homebase_dir)
    call('git commit -am"Edit CMake files to make this project standalone."')

repository_size(cfsqp_dir)

# Save svn2git log to this repo.
call('cp %s/svn2git_* %s' % (cfsqp_dir, homebase_dir))
with cd(homebase_dir):
    call("git add 'svn2git_*'")
    call('git commit -m"Update cfsqp svn2git logs."')

# Tell the user how long opensim2git ran for.
elapsed_time = time.time() - start_time
myprint("Took %.1f minutes." % (elapsed_time / 60.0))

