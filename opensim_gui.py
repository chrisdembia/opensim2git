
import os
import time

from common import *

# Preliminaries.
# --------------
start_time = time.time()

# For debugging and development:
normalize_line_endings = True
opensim_gui_tag_prefix = 'v'

opensim_legacy_dir = os.path.join(git_repos_dir,
        'opensim-legacy')

opensim_gui_dir = os.path.join(git_repos_dir, 'opensim-gui')

prompt_delete_dir(opensim_gui_dir)

myprint('Making a copy of opensim-gui.')

call('cp -r %s %s' % (opensim_legacy_dir,
        opensim_gui_dir))

with cd(opensim_gui_dir):

    # Edit 'description' file, which is used by GitWeb (run `$ git instaweb`).
    call('echo "opensim-gui: %s" '
            '> %s/.git/description' % (
                opensim_gui_description, opensim_gui_dir))

myprint('Ripping out parts of the history.')


swig_java_path = os.path.join(opensim_gui_dir,
        'Gui/opensim/modeling', 'src/org/opensim/modeling')

list_of_current_folders_to_gitrm = [
        'Applications',
        'OpenSim',
        'Models',
        'Documentation',
        'Gui/Documentation',
        'Vendors/lepton',
        'Vendors/CFSQP',
        'Vendors/vtk_dll',
        ]
list_of_folders_to_delete = [
        'Examples',
        'webstart',
        'UI',
        'SimtkUI',
        'Simulation',
        'OpenSimJNI',
        'API',
        'Applications',
        'OpenSim',
        'Models',
        'Documentation',
        'html',
        'xerces-c*',
        'Specs',
        'lepton',
        'CFSQP',
        'NMBLTK',
        'SimTK',
        'Gait*',
        'Arm26',
        'Leg39',
        'DemoFiles',
        'vtk_dll',
        ]
list_of_files_to_delete = [
        'ieee_fig03_OpenSim_SimTK_v2.ai',
        'ApiDoxygen.cmake',
        'CTestConfig.cmake',
        'Doxyfile.in',
        'FindSimbody.cmake',
        'OpenSimAPI.html',
        '*.psd',
        '*.lib',
        '*.dll',
        '*.dylib',
        '*.so',
        #'*.jar',
        '*.exe',
        'SimTK*.dll',
        'OpenSim*.dll',
        'OpenSim',
        '*_wrap.cxx',
        '*_wrap.h',
        ] #+ swig_java_output
folders_to_delete = '{%s}' % ','.join(list_of_folders_to_delete)
files_to_delete = '{%s}' % ','.join(list_of_files_to_delete)

with cd(opensim_gui_dir):

    for item in list_of_current_folders_to_gitrm:
        call('git rm -rf --quiet %s' % item)
    for item in list_of_files_to_delete:
        call('git rm -rf --quiet *%s' % item)

    call('git commit --quiet '
            '-am"Normalize line endings."')
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

with cd(opensim_gui_dir):
    # TODO take care of pre-r6663 branches.
    # TODO just rename existing tags.
    # TODO convert_branch_to_tag('CableWrapping', 'cable-wrapping')
    # TODO convert_branch_to_tag('ModelBuilding', 'model-building')
    # TODO try to remove these branches beforehand.
    rename_tag('Release_02_04_00', '%s2.4.0' % opensim_gui_tag_prefix)
    rename_tag('Release_03_00_00', '%s3.0.0' % opensim_gui_tag_prefix)
    rename_tag('Release_03_01_00', '%s3.1.0' % opensim_gui_tag_prefix)
    rename_tag('Release_03_02_00', '%s3.2.0' % opensim_gui_tag_prefix)

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
    filter_branch_tasks(opensim_gui_dir, active_branches)

# Make opensim-gui a standalone project with a reasonably clean install.
with cd(opensim_gui_dir):

# TODO    for branch in active_branches:
# TODO        myprint('Applying patch to %s' % branch)
# TODO        call('git checkout %s' % branch)
# TODO        call('git apply %s/opensim-core.patch' % homebase_dir)
# TODO        call('git commit -am"Edit CMake files to reflect split from SVN."')
    for branch in active_branches:
        call('git checkout %s' % branch)
        swig_java_output = []
        for fname in os.listdir(swig_java_path):
            if fname.endswith('java'):
                with open(os.path.join(swig_java_path, fname)) as f:
                    if f.read().find('automatically generated by SWIG') != -1:
                        swig_java_output += [fname]
        for fname in swig_java_output:
            call('git rm -rf --quiet %s/%s' % (swig_java_path, fname))
        call('git commit -am"Remove SWIG java output."')

    call('git checkout master')

git_garbage_collection(opensim_gui_dir)

with cd(opensim_gui_dir):
    call("%s/git_diet/bin/find_fattest_objects.sh -n 100 " % (
                homebase_dir))

repository_size(opensim_gui_dir)

# Tell the user how long opensim2git ran for.
elapsed_time = time.time() - start_time
myprint("Took %.1f minutes." % (elapsed_time / 60.0))

