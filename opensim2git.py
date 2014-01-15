import os
import shutil
import sys
import time

from common import *

# Preliminaries.
# --------------
start_time = time.time()

git_repos_dir = os.path.join(local_dir, 'ruby_git_repos')

# Try to install svn2git.
myprint('Obtaining dependencies...')
os.system('sudo apt-get install git-core git-svn ruby rubygems')
os.system('sudo gem install svn2git')

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
cfsqp_dir = os.path.join(git_repos_dir, 'cfsqp')

os.makedirs(opensim_core_dir)
os.makedirs(cfsqp_dir)

# Get username and password.
username = raw_input('Enter your simtk username: ')


# Create git repositories.
# ------------------------
# We have to do some funky stuff to give the repo password to svn2git,
# because its own prompt is unclear.
# https://github.com/nirvdrum/svn2git/issues/59
password_message = ("Enter your simtk password, hit enter, then enter your "
            "password again, and hit enter (there's a bug). "
            "Then, nothing will appear to happen, but don't worry, "
            "it's working. See %s for progress.")
# cfsqp
myprint('Running svn2git for cfsqp.')
with cd(cfsqp_dir):

    # Run svn2git.
    myprint(password_message % cfsqp_dir)

    # Write output to log files.
    out = open('%s/svn2git_progress_log.txt' % cfsqp_dir, 'w')
    err = open('%s/svn2git_error_log.txt' % cfsqp_dir, 'w')

    # TODO subprocess.call may be causing the threading issues.
    call("svn2git https://simtk.org/svn/opensim "
            "--trunk Trunk/Vendors/CFSQP "
            "--authors %s/authors.txt "
            "--verbose "
            "--username %s "
            "--nobranches " # TODO YES branches once svn2git is fixed.
            "--notags "
            "--revision 1053 "
            "--metadata " % (homebase_dir, username),
            stdout=out,
            stderr=err)
    out.close()
    err.close()

    call('echo "cfsqp: %s" > %s/.git/description' % (
        cfsqp_description, cfsqp_dir))

# opensim-core
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
    call("svn2git https://simtk.org/svn/opensim "
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
            "--exclude 'OpenSim/Java/src' "
            "--exclude 'OpenSim/Java/OpenSimJNI/OpenSimJNI_wrap.*' "
            "--exclude 'OpenSim/Wrapping/Java/OpenSimJNI/OpenSimJNI_wrap.*' "
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
            "--exclude 'Documentation/OpenSim_Splash.psd' "
            "--exclude 'Documentation/OpenSim_Splash_2_2_1.psd' "
            "--exclude 'OpenSim/Wrapping/Python/pyOpenSim_wrap.cxx' "
            "--exclude 'OpenSim/Wrapping/Python/pyOpenSim_wrap.h' "
            "--exclude 'OpenSim/Wrapping/Python/pyOpenSim.py' "
            "--exclude 'OpenSim/Utilities/importOldModels/SimTKlapack.dll' "
            "--exclude 'OpenSim/Utilities/importOldModels/xerces-c_2_7.dll' "
            "--exclude 'Vendors/xerces-c_2_8_0' "
            "--exclude 'Vendors/vtk_dll' "
            # Above exclude's are for r6665 and after.
            # Below exclude's are for r6664 and earlier.
            "--exclude 'Vendors/xerces-c-src_2_7_0' "
            "--exclude 'Vendors/xerces-c-src_2_4_0' "
            "--exclude 'Vendors/xerces-c-src2_4_0' "
            "--exclude 'OpenSim/Examples/Gait2354_Simbody/OutputReference' "
            "--exclude 'OpenSim/Examples/Gait2392_Simbody/OutputReference' "
            "--exclude 'Documentation' "
            "--exclude 'Vendors/lib' "
            "--exclude 'Vendors/core' "
            "--exclude 'Vendors/SimTK' "
            "--exclude 'OpenSim/Examples/Gait/OutputReference' "
            "--exclude 'OpenSim/Examples/Leg39/OutputReference' "
            "--exclude 'OpenSim/Examples/Gait2354/OutputReference' "
            "--exclude 'Specs' "
            "--nobranches " # TODO YES branches once svn2git is fixed.
            "--notags "
            #"--revision 6665 "
            "--metadata " % (homebase_dir, username),
            stdout=out,
            stderr=err)
    out.close()
    err.close()

    # Edit 'description' file, which is used by GitWeb (run `$ git instaweb`).
    call('echo "opensim-core: %s" '
            '> %s/.git/description' % (
                opensim_core_description, opensim_core_dir))

# Normalize line endings.
# -----------------------
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

def filter_branch_tasks(repo_path):
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
        call('git commit -m "Introduce end-of-line normalization."')

filter_branch_tasks(cfsqp_dir)
filter_branch_tasks(opensim_core_dir)

# Garbage collect.
# ----------------
# Make the repositories smaller.
myprint('Running git garbage collection to reduce repository size...')
def git_garbage_collection(repo_path):
    with cd(repo_path):
        # Remove backup of the files we deleted from the history (may not be
        # necessary here, because we do not delete files from the history).
        call('rm -rf .git/refs/original')
        call('git reflog expire --expire=now --all')
        call('git gc --prune=now')
        call('git gc --aggressive --prune=now')

git_garbage_collection(cfsqp_dir)
git_garbage_collection(opensim_core_dir)

# Make CFSQP a standalone project.
# --------------------------------
with cd(cfsqp_dir):
    call('cp %s/CMakeLists_cfsqp_standalone.txt CMakeLists.txt' % homebase_dir)
    call('git add CMakeLists.txt')
    call('git commit -m"Make this project standalone."')

# Tell the user how long opensim2git ran for.
elapsed_time = time.time() - start_time
myprint("Took %.1f minutes." % (elapsed_time / 60.0))
