
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
    out = open('%s/svn2git_progress_log.txt' % cfsqp_dir, 'w')
    err = open('%s/svn2git_error_log.txt' % cfsqp_dir, 'w')

    # TODO subprocess.call may be causing the threading issues.
    call("svn2git %s "
            "--trunk Trunk/Vendors/CFSQP "
            "--authors %s/authors.txt "
            "--verbose "
            "--username %s "
            "--nobranches " # TODO YES branches once svn2git is fixed.
            "--notags "
            "--revision 1053 "
            "--metadata " % (svn_repo_path, homebase_dir, username),
            stdout=out,
            stderr=err)
    out.close()
    err.close()

    call('echo "cfsqp: %s" > %s/.git/description' % (
        cfsqp_description, cfsqp_dir))
    
filter_branch_tasks(cfsqp_dir)

git_garbage_collection(cfsqp_dir)

# Make CFSQP a standalone project.
# --------------------------------
with cd(cfsqp_dir):
    call('cp %s/CMakeLists_cfsqp_standalone.txt CMakeLists.txt' % homebase_dir)
    call('git add CMakeLists.txt')
    call('git commit -m"Edit CMake files to make this project standalone."')

repository_size(cfsqp_dir)

# Tell the user how long opensim2git ran for.
elapsed_time = time.time() - start_time
myprint("Took %.1f minutes." % (elapsed_time / 60.0))

