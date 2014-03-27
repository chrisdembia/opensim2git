import os
from os.path import join
import shutil
import sys
import time

from common import *

# Preliminaries.
# --------------
start_time = time.time()

# For debugging and development:
normalize_line_endings = True
use_opensim_core_svn_version_branches_as_git_tags = False
opensim_core_tag_prefix = 'v'

# To prevent weird overwriting from occurring, remove the previous work.
if os.path.exists(git_repos_dir):
    input = raw_input('Deleting pre-existing %s. Okay? (y/n) ' % git_repos_dir)
    if input[0] == 'y':
        shutil.rmtree(git_repos_dir)
    else:
        sys.exit('Aborting. Will not overwrite pre-existing work.')

# TODO Since we've already required root access, we may be working in a
# write-protected area.
os.makedirs(git_repos_dir)

opensim_core_dir = os.path.join(git_repos_dir, 'opensim-core')
opensim_complete_history_dir = os.path.join(git_repos_dir,
        'opensim-complete-history')

os.makedirs(opensim_core_dir)
os.makedirs(opensim_complete_history_dir)


# Create git repositories.
# ------------------------
# We have to do some funky stuff to give the repo password to svn2git,
# because its own prompt is unclear.
# https://github.com/nirvdrum/svn2git/issues/59
password_message = ("Enter your simtk password, hit enter, then enter your "
            "password again, and hit enter (there's a bug). "
            "Then, nothing will appear to happen, but don't worry, "
            "it's working. See %s for progress.")


# opensim-core
# ============
myprint('Running svn2git for opensim-core.')
with cd(opensim_core_dir):

    # Run svn2git.
    myprint(password_message % opensim_core_dir)

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
    call("svn2git %s "
            "--trunk Trunk "
            "--tags Tags "
            "--branches Branches "
            "--authors %s/authors.txt "
            "--verbose "
            "--username %s "
            "--exclude '.*CFSQP.*' "
            "--exclude 'Gui' "
            #"--exclude '.*genfiles.properties' "
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
            "--exclude 'Models/Arm26/OutputReference' "
            "--exclude 'Models/Leg39/OutputReference' "
            "--exclude 'Models/Gait10dof18musc/OutputReference' "
            "--exclude 'Models/Gait2354_Simbody/OutputReference' "
            "--exclude 'Models/Gait2392_Simbody/OutputReference' "
            "--exclude 'Models/Leg6Dof9Musc/Stance/Reference' "
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
            "--exclude 'OpenSim/Examples/Gait2354_Simbody/OutputReference' "
            "--exclude 'OpenSim/Examples/Gait2392_Simbody/OutputReference' "
            "--exclude 'OpenSim/Examples/Gait/OutputReference' "
            "--exclude 'OpenSim/Examples/Leg39/OutputReference' "
            "--exclude 'OpenSim/Examples/Gait2354/OutputReference' "
            "--ignore 'Tags/Release_02_00_Jamboree' "
            "--ignore 'Tags/OpenSim_BuiltOn_SimTK_1_1' "
            #"--ignore 'Trunk/NMBLTK' "
            #"--revision 6665 "
            "--metadata " % (svn_repo_path, homebase_dir, username),
            stdout=out,
            stderr=err)
    out.close()
    err.close()

    # Edit 'description' file, which is used by GitWeb (run `$ git instaweb`).
    call('echo "opensim-core: %s" '
            '> %s/.git/description' % (
                opensim_core_description, opensim_core_dir))

# opensim-complete-history
# ========================
myprint('Running svn2git for opensim-complete-history.')
with cd(opensim_complete_history_dir):

    # Run svn2git.
    myprint(password_message % opensim_complete_history_dir)

    # Write output to log files.
    out = open('%s/svn2git_progress_log.txt' % opensim_complete_history_dir, 'w')
    err = open('%s/svn2git_error_log.txt' % opensim_complete_history_dir, 'w')

    call("svn2git %s "
            "--trunk Trunk "
            "--tags Tags "
            "--branches Branches "
            "--authors %s/authors.txt "
            "--verbose "
            "--username %s "
            "--metadata " % (svn_repo_path, homebase_dir, username),
            stdout=out,
            stderr=err)
    out.close()
    err.close()

    # Edit 'description' file, which is used by GitWeb (run `$ git instaweb`).
    call('echo "opensim_complete_history: %s" '
            '> %s/.git/description' % (
                opensim_complete_history_description,
                opensim_complete_history_dir))

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
    if use_opensim_core_svn_version_branches_as_git_tags:
        convert_branch_to_tag('OpenSim30', '%s3.0' % opensim_core_tag_prefix)
        convert_branch_to_tag('OpenSim31', '%s3.1' % opensim_core_tag_prefix)
        convert_branch_to_tag('OpenSim32', '%s3.2' % opensim_core_tag_prefix)
        #delete_tag('Release_02_04_00')
        delete_tag('Release_03_00_00')
        delete_tag('Release_03_01_00')
        delete_tag('Release_03_02_00')
    else:
        delete_branch('OpenSim30')
        delete_branch('OpenSim31')
        #rename_tag('Release_02_04_00', '%s2.4' % opensim_core_tag_prefix)
        rename_tag('Release_03_00_00', '%s3.0' % opensim_core_tag_prefix)
        rename_tag('Release_03_01_00', '%s3.1' % opensim_core_tag_prefix)
        rename_tag('Release_03_02_00', '%s3.2' % opensim_core_tag_prefix)

    delete_branch('OpenSimWW01')
    delete_branch('OpenSim30GUI')
    delete_branch('Remove_Xerces')
    delete_branch('ModelBuilding')
    delete_branch('CableWrapping')
    delete_tag('Release_03_00_Dev')
    
if normalize_line_endings:
    if not only_cfsqp:
        filter_branch_tasks(opensim_core_dir)
        filter_branch_tasks(opensim_complete_history_dir)

if not only_cfsqp:
    git_garbage_collection(opensim_core_dir)
    git_garbage_collection(opensim_complete_history_dir)


repository_size(opensim_core_dir)
repository_size(opensim_complete_history_dir)

# Tell the user how long opensim2git ran for.
elapsed_time = time.time() - start_time
myprint("Took %.1f minutes." % (elapsed_time / 60.0))

# TODO 6665 or 6666?
