
import time

from common import *

start_time = time.time()

opensim_complete_history_dir = os.path.join(git_repos_dir,
        'opensim-complete-history')

opensim_complete_history_tempcopy_dir = os.path.join(git_repos_dir,
        'opensim-complete-history-temp')

opensim_models_dir = os.path.join(git_repos_dir, 'opensim-models')

prompt_delete_dir(opensim_models_dir)

myprint('Splitting Models from opensim-complete-history into opensim-models')

call('cp -r %s %s' % (opensim_complete_history_dir,
        opensim_complete_history_tempcopy_dir))

with cd(opensim_complete_history_tempcopy_dir):
    call('git subtree split -P Models -b models-only')

call('mkdir %s' % opensim_models_dir)

with cd(opensim_models_dir):
    call('git init')
    call('git pull file://%s models-only' %
            opensim_complete_history_tempcopy_dir)

call('rm -rf %s' % opensim_complete_history_tempcopy_dir)

repository_size(opensim_models_dir)

# Tell the user how long opensim2git ran for.
elapsed_time = time.time() - start_time
myprint("Took %.1f minutes." % (elapsed_time / 60.0))
