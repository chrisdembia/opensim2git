
import os
import time

from common import *

# Preliminaries.
# --------------
start_time = time.time()

# For debugging and development:
normalize_line_endings = True
opensim_core_tag_prefix = 'v'

opensim_core_dir = os.path.join(git_repos_dir, 'opensim-core')

prompt_delete_dir(opensim_core_dir)

os.makedirs(opensim_core_dir)

# opensim-core
# ============
myprint('Running svn2git for opensim-core.')
with cd(opensim_core_dir):

    # Write output to log files.
    out = open('%s/svn2git_progress_log.txt' % opensim_core_dir, 'w')
    err = open('%s/svn2git_error_log.txt' % opensim_core_dir, 'w')

    # I found most of these files using lines like: 
    # $ git verify-pack -v .git/objects/pack/<PACKFILE>.idx | sort -k 3 -n | \
    #      tail -20
    # % git rev-list --objects --all | grep <COMMIT HASH>
    # from
    # http://git-scm.com/book/ca/Git-Internals-Maintenance-and-Data-Recovery
    # Here's another good blog post:
    # http://blog.jessitron.com/2013/08/finding-and-removing-large-files-in-git.html
    call("svn2git file://%s "
            "--trunk Trunk "
            "--tags Tags "
            "--branches Branches "
            "--authors %s/authors.txt "
            "--verbose "
            "--username %s "
            "--exclude '.*CFSQP.*' "
            "--exclude 'Gui' "
            "--exclude 'OpenSim/Applications/Gui' "
            "--exclude 'Installer' "
            "--exclude 'NSIS.InstallOptions.ini.in' "
            "--exclude 'NSIS.template.in' "
            "--exclude 'WriteEnvStr.nsh' "
            "--exclude 'OpenSim/doc/html' "
            "--exclude 'API/doc/html' "
            "--exclude 'Documentation/OpenSim_Splash.psd' "
            "--exclude 'Documentation/OpenSim_Splash_2_2_1.psd' "
            "--exclude 'OpenSim/Java/src' "
            "--exclude 'OpenSim/Java/OpenSimJNI/OpenSimJNI_wrap.*' "
            "--exclude 'OpenSim/Wrapping/Java/OpenSimJNI/OpenSimJNI_wrap.*' "
            "--exclude 'OpenSim/Wrapping/Python/pyOpenSim_wrap.cxx' "
            "--exclude 'OpenSim/Wrapping/Python/pyOpenSim_wrap.h' "
            "--exclude 'OpenSim/Wrapping/Python/pyOpenSim.py' "
            "--exclude 'OpenSim/Utilities/importOldModels/SimTKlapack.dll' "
            "--exclude 'OpenSim/Utilities/importOldModels/xerces-c_2_7.dll' "
            "--exclude 'Vendors/xerces-c_2_8_0' "
            "--exclude 'Vendors/vtk_dll' "
            "--exclude 'OpenSim/Examples/ControllerExample/OutputReference/*.sto' "
            "--exclude 'OpenSim/Examples/ControllerExample/OutputReference/*.mot' "
            "--exclude 'OpenSim/Examples/ControllerExample/OutputReference/*.osim' "
            "--exclude 'OpenSim/Examples/CustomActuatorExample/OutputReference/*.sto' "
            "--exclude 'OpenSim/Examples/CustomActuatorExample/OutputReference/*.mot' "
            "--exclude 'OpenSim/Examples/CustomActuatorExample/OutputReference/*.osim' "
            "--exclude 'OpenSim/Examples/OptimizationExample_Arm26/OutputReference/*.sto' "
            "--exclude 'OpenSim/Examples/OptimizationExample_Arm26/OutputReference/*.mot' "
            "--exclude 'OpenSim/Examples/OptimizationExample_Arm26/OutputReference/*.osim' "
            "--exclude 'OpenSim/Examples/ExampleMain/OutputReference/*.sto' "
            "--exclude 'OpenSim/Examples/ExampleMain/OutputReference/*.mot' "
            "--exclude 'OpenSim/Examples/ExampleMain/OutputReference/*.osim' "
            "--exclude 'Models' "
            # Above exclude's are for r6665 and after.
            # Below exclude's are for r6664 and earlier.
            "--exclude 'Documentation' "
            "--exclude 'Vendors/xerces-c-src_2_7_0' "
            "--exclude 'Vendors/xerces-c-src_2_4_0' "
            "--exclude 'Vendors/xerces-c-src2_4_0' "
            "--exclude 'Vendors/lib' "
            "--exclude 'Vendors/core' "
            "--exclude 'Vendors/SimTK' "
            "--exclude 'Specs' "
            "--exclude 'Examples' "
            "--exclude 'OpenSim/Examples/Gait2354_Simbody/OutputReference' "
            "--exclude 'OpenSim/Examples/Gait2392_Simbody/OutputReference' "
            "--exclude 'OpenSim/Examples/Gait/OutputReference' "
            "--exclude 'OpenSim/Examples/Leg39/OutputReference' "
            "--exclude 'OpenSim/Examples/Gait2354/OutputReference' "
            "--revision 6665 "
            "--metadata " % (svn_mirror_dir, homebase_dir, username),
            stdout=out,
            stderr=err)
    out.close()
    err.close()

    # Edit 'description' file, which is used by GitWeb (run `$ git instaweb`).
    call('echo "opensim-core: %s" '
            '> %s/.git/description' % (
                opensim_core_description, opensim_core_dir))

# Clean up OpenSim branches.
# --------------------------
# 0. TODO branches are merged in at some point.
# 1. Convert previous branches to tags.
# 2. Delete branches that we are not interested in.

# Before deleting anything, fix the merge history.
# ------------------------------------------------
# http://blog.agavi.org/post/16865375185/fixing-svn-merge-history-in-git-repositories
# TODO not doing this anymore.

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

with cd(opensim_core_dir):
    # TODO take care of pre-r6663 branches.
    # TODO just rename existing tags.
    # TODO convert_branch_to_tag('CableWrapping', 'cable-wrapping')
    # TODO convert_branch_to_tag('ModelBuilding', 'model-building')
    # TODO try to remove these branches beforehand.
    delete_branch('OpenSim30')
    delete_branch('OpenSim31')
    #rename_tag('Release_02_04_00', '%s2.4' % opensim_core_tag_prefix)
    rename_tag('Release_03_00_00', '%s3.0.0' % opensim_core_tag_prefix)
    rename_tag('Release_03_01_00', '%s3.1.0' % opensim_core_tag_prefix)
    rename_tag('Release_03_02_00', '%s3.2.0' % opensim_core_tag_prefix)

    delete_branch('OpenSimWW01')
    delete_branch('OpenSim30GUI')
    delete_branch('Remove_Xerces')
    delete_branch('ModelBuilding')
    delete_branch('CableWrapping')
    delete_tag('Release_03_00_Dev')
    
if normalize_line_endings:
    filter_branch_tasks(opensim_core_dir)

git_garbage_collection(opensim_core_dir)

repository_size(opensim_core_dir)

# Tell the user how long opensim2git ran for.
elapsed_time = time.time() - start_time
myprint("Took %.1f minutes." % (elapsed_time / 60.0))

# TODO 6665 or 6666?
