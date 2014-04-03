
import os
import time

from common import *

# Preliminaries.
# --------------
start_time = time.time()

# For debugging and development:
normalize_line_endings = False

opensim_complete_history_dir = os.path.join(git_repos_dir,
        'opensim-complete-history')

prompt_delete_dir(opensim_complete_history_dir)

os.makedirs(opensim_complete_history_dir)


# svn2git
# -------
myprint('Running svn2git for opensim-complete-history.')
with cd(opensim_complete_history_dir):

    # Write output to log files.
    out = open('%s/svn2git_progress_log.txt' % opensim_complete_history_dir,
            'w')
    err = open('%s/svn2git_error_log.txt' % opensim_complete_history_dir, 'w')

    call("svn2git file://%s "
            "--trunk Trunk "
            "--tags Tags "
            "--branches Branches "
            "--authors %s/authors.txt "
            "--verbose "
            "--username %s "
            "--exclude '.*CFSQP.*' "
            "--metadata " % (svn_mirror_dir, homebase_dir, username),
            stdout=out,
            stderr=err)
    out.close()
    err.close()

    # Edit 'description' file, which is used by GitWeb (run `$ git instaweb`).
    call('echo "opensim_complete_history: %s" '
            '> %s/.git/description' % (
                opensim_complete_history_description,
                opensim_complete_history_dir))


def convert_branch_to_tag(branch_name, tag_name):
    call('git checkout %s' % branch_name)
    call('git tag %s' % tag_name)
    call('git checkout master')
    call('git branch %s -D' % branch_name)
def delete_branch(branch_name):
    call('git branch %s -D' % branch_name)
def delete_tag(tag_name):
    call('git tag -d %s' % tag_name)
def rename_tag(old, new):
    call('git tag %s %s' % (new, old))
    delete_tag(old)
    
if normalize_line_endings:
    filter_branch_tasks(opensim_complete_history_dir)

git_garbage_collection(opensim_complete_history_dir)

repository_size(opensim_complete_history_dir)

# Tell the user how long opensim2git ran for.
elapsed_time = time.time() - start_time
myprint("Took %.1f minutes." % (elapsed_time / 60.0))
