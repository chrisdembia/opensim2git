
import os
import time

from common import *

# Preliminaries.
# --------------
start_time = time.time()

# For debugging and development:
normalize_line_endings = True
opensim_core_tag_prefix = 'v'

opensim_legacy_dir = os.path.join(git_repos_dir,
        'opensim-legacy')

opensim_core_dir = os.path.join(git_repos_dir, 'opensim-core')

prompt_delete_dir(opensim_core_dir)

myprint('Making a copy of opensim-legacy.')

call('cp -r %s %s' % (opensim_legacy_dir,
        opensim_core_dir))

with cd(opensim_core_dir):

    # Edit 'description' file, which is used by GitWeb (run `$ git instaweb`).
    call('echo "opensim-core: %s" '
            '> %s/.git/description' % (
                opensim_core_description, opensim_core_dir))

myprint('Ripping out parts of the history.')

list_of_current_folders_to_gitrm = [
        'OpenSim/Utilities/importOldModels',
        'Models',
        'Installer',
        'Documentation',
        'Vendors/vtk_dll',
        'Vendors/CFSQP',
        'Gui',
        'OpenSim/doc/extra_html/si',
        ]
list_of_folders_to_delete = [
        'importOldModels',
        'Models',
        'Installer',
        'Documentation',
        'html',
        'xerces-c*',
        'Specs',
        'vtk_dll',
        'CFSQP',
        'NMBLTK',
        'SimTK',
        'Gui',
        'Gait*',
        'Arm26',
        'Leg39',
        'si',
        ]
list_of_files_to_delete = [
        'NSIS.InstallOptions.ini.in',
        'NSIS.template.in',
        'WriteEnvStr.nsh',
        '*_wrap.cxx',
        '*.psd',
        '*.java',
        '*.dll',
        '*.lib',
        '*.dylib',
        '*.so',
        '*.jar',
        'pyOpenSim.py',
        'opensimModel.py',
        'opensim.py',
        'OpenSimJNI_wrap.cxx',
        '*.exe',
        ]
folders_to_delete = '{%s}' % ','.join(list_of_folders_to_delete)
files_to_delete = '{%s}' % ','.join(list_of_files_to_delete)

with cd(opensim_core_dir):

    for item in list_of_current_folders_to_gitrm:
        call('git rm -rf --quiet %s' % item)
    for item in list_of_files_to_delete:
        call('git rm -rf --quiet *%s' % item)

    call('git commit --quiet '
            '-am"Preparing to remove certain files from history."')
    call("java -jar %s/bfg-1.11.3.jar "
            "--delete-folders %s --delete-files %s" % (
                homebase_dir, folders_to_delete, files_to_delete))

# Clean up OpenSim branches.
# --------------------------
# 1. Convert previous branches to tags.
# 2. Delete branches that we are not interested in.

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
    rename_tag('Release_02_04_00', '%s2.4.0' % opensim_core_tag_prefix)
    rename_tag('Release_03_00_00', '%s3.0.0' % opensim_core_tag_prefix)
    rename_tag('Release_03_01_00', '%s3.1.0' % opensim_core_tag_prefix)
    rename_tag('Release_03_02_00', '%s3.2.0' % opensim_core_tag_prefix)

    delete_branch('1728Branch')
    delete_branch('CableWrapping')
    delete_branch('Engines')
    delete_branch('Integrator')
    delete_branch('Integrator@1105')
    delete_branch('JasonEmel485Project')
    delete_branch('JasonEmel485Project@1683')
    delete_branch('JasonEmel485Project@1741')
    delete_branch('JasonEmel485Project@1755')
    delete_branch('JasonEmel485Project@4133')
    delete_branch('ModelBuilding')
    delete_branch('OpenSim')
    delete_branch('OpenSim15')
    delete_branch('OpenSim18')
    delete_branch('OpenSim19')
    delete_branch('OpenSim20')
    delete_branch('OpenSim21')
    delete_branch('OpenSim22')
    delete_branch('OpenSim23')
    delete_branch('OpenSim23_1')
    delete_branch('OpenSim23_1_NB7')
    delete_branch('OpenSim24')
    delete_branch('OpenSim30')
    delete_branch('OpenSim30GUI')
    delete_branch('OpenSim31')
    delete_branch('OpenSimGUIProto')
    delete_branch('OpenSimWW01')
    delete_branch('OpenSim_BuiltOn_SimTK_1_1')
    delete_branch('OpenSim_BuiltOn_SimTK_1_1@1683')
    delete_branch('OpenSim_BuiltOn_SimTK_1_1@1741')
    delete_branch('OpenSim_BuiltOn_SimTK_1_1@1755')
    delete_branch('OpenSim_BuiltOn_SimTK_1_1@4056')
    delete_branch('OpenSim_exhibit')
    delete_branch('Remove_Xerces')
    delete_branch('Restructure')
    delete_branch('UseSimTKLibs')
    delete_branch('migrate2NmbltkBr')

    delete_tag('NMBLTK')
    delete_tag('NMBLTK@1095')
    delete_tag('Release0.1')
    delete_tag('Release0.1@1096')
    delete_tag('Release_00_00')
    delete_tag('Release_00_06_00')
    delete_tag('Release_00_07_08')
    delete_tag('Release_00_08_02')
    delete_tag('Release_01_00_00')
    delete_tag('Release_01_01_00')
    delete_tag('Release_01_05_05')
    delete_tag('Release_01_06_Jamboree')
    delete_tag('Release_01_07_00')
    delete_tag('Release_02_00')
    delete_tag('Release_02_00_01')
    delete_tag('Release_02_00_02')
    delete_tag('Release_02_00_Jamboree')
    delete_tag('Release_02_02_00')
    delete_tag('Release_02_02_01')
    delete_tag('Release_02_03_02')
    delete_tag('Release_03_00_Dev')
    delete_tag('Before_Directory_Restructure_2007-03-16')
    
active_branches = ['master', 'Visualizer', 'OpenSim32']
if normalize_line_endings:
    filter_branch_tasks(opensim_core_dir, active_branches)

# Make opensim-core a standalone project with a reasonably clean install.
with cd(opensim_core_dir):

    for branch in active_branches:
        myprint('Applying patch to %s' % branch)
        call('git checkout %s' % branch)
        call('git apply %s/opensim-core.patch' % homebase_dir)
        call('git commit -am"Edit CMake files to reflect split from SVN."')

    call('git checkout master')

git_garbage_collection(opensim_core_dir)

repository_size(opensim_core_dir)

# Tell the user how long opensim2git ran for.
elapsed_time = time.time() - start_time
myprint("Took %.1f minutes." % (elapsed_time / 60.0))

# TODO 6665 or 6666?
