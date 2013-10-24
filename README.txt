Moving the OpenSim code repository from Subversion (SVN) to Git
***************************************************************
This document details the thought and procedure that went into moving OpenSim
from an SVN repository at https://simtk.org/svn/opensim to a Git repository
hosted primarily at https://github.com/opensim-org/opensim.

Michael Sherman moved the Simbody code repository from SVN to Git in August,
2013. Simbody was previosly hosted at simtk.org, as well. His work provided the
groundwork for this work.

This document is written by Chris Dembia and Justin Si.

Tasks
=====
This conversion requires a few tasks beyond what one would normally assume a
Git conversion would entail. Some of these tasks are done during the svn2git
conversion, while others are performed after the svn2git conversion and before
the repository is pushed to Github.

1. Remove CFSQP from the core repository.
2. Normalize all line endings to UNIX line endings.
3. Split the repository into multiple repositories (core, gui, models,
        wrapping, cfsqp).
4. Convert branches into tags, and decide which branches can be deleted
        (irreversibly).
5. Check that history is how we want it.
6. Clean up history, if necessary (to reduce repository size).
7. Push the repositories to github.com/opensim-org.

The hope is to have a Makefile that, when running `$ make`, will take care of
all these tasks for us.

Removing CFSQP
--------------
-CFSQP enters the code repository at r1052
-try using nominimizeurl option to svn2git
-Can do this in three ways:
    1. svn2git --exclude/--ignore flag
    2. git filter-branch after cloning.
    3. git subtree (see GitHub help page about this).


Normalize line endings
----------------------
This is easy to do; Sherm has done it, but I'm not sure at what point it should
occur, relative too everything else. The reason why this is important is that
some files have windows line endings (LFCR or something), while some have unix
line endings (CR). See
http://blog.gyoshev.net/2013/08/normalizing-line-endings-in-git-repositories/.
Chris advises that we use filter-branch.


Split the repository into multiple
----------------------------------
It may be that we don't want to split the repositories for a few weeks after
we've moved to git, so that we only have to adapt to 1 thing at a time. An
alternative is that we split into multiple projects while we're still using
SVN. However, I think that makes it harder to maintain the history in git.

git filter-branch --subdirectory would be useful, if we already had separate
folders. But instead this might mean cloning the full repository for each of
the 5 separate repos, and then moving files, and deleting the rest of the
files. Is there one repository (GUI) that we want to not delete the history
for?

This is how we might rearrange the repositories:
opensim-core:
Applications -> opensim-core/applications
ApiDoxygen.cmake -> opensim-core/APIDoxygen.cmake
CMakeLists.txt -> opensim-core/
Copyright.txt -> opensim-core/
CTestConfig.cmake -> opensim-core/
Doxyfile.in -> opensim-core/doc/
FindSimbody.cmake -> opensim-core/cmake
NOTICE -> opensim-core/LICENSE.txt
OpenSimAPI.html -> opensim-core/doc
ReadMe.txt -> opensim-core/README.txt
OpenSim/Actuators -> opensim-core/OpenSim/
OpenSim/Analyses -> opensim-core/OpenSim/
OpenSim/Common -> opensim-core/OpenSim/
OpenSim/Simulation -> opensim-core/OpenSim/
OpenSim/Tools -> opensim-core/OpenSim/
OpenSim/Utilities -> opensim-core/utilities
OpenSim/Tests -> opensim-core/tests
OpenSim/Examples -> opensim-core/examples
OpenSim/Auxiliary -> opensim-core/tests
OpenSim/OpenSimDoxygenMain.h -> opensim-core/doc/ [isn't actually code]
OpenSim/doc -> opensim-core/doc
OpenSim/Vendors/lepton -> opensim-core/external/lepton

opensim-gui:
Gui/Documentation -> opensim-gui/documentation
Gui/Internal -> opensim-gui/internal
Gui/opensim -> opensim-gui/opensim
Gui/plugins -> opensim-gui/plugins
Gui/CMakeLists.txt -> opensim-gui/CMakeLists.txt
Installer/* -> opensim-gui/installer
Vendors/vtk_dll -> opensim-gui/external/vtk
NSIS.* -> opensim-gui/installer
WriteEnvStr.nsh -> opensim-gui/installer

opensim-wrapping:
Wrapping -> opensim-wrapping

opensim-models:
Models -> opensim-models

opensim-cfsqp (can we just name this 'cfsqp'?):
Models -> opensim-cfsqp


Many changes would need to be made immediately to the CMakeLists files in order
for the repositories to work. Should these changes be made before the
repositories are put up online? Maybe it doesn't matter.

Branches to tags
----------------
svn2git converts all SVN branches into git branches, but we really don't want
to keep any of these "svn->git" branches as git branches.  Therefore, there are
2 types of "svn->git" branches:

1. Should become git tags. There are 2 reasons why this could be the case:
    a. They represent a release of OpenSim (e.g., OpenSim31).
    b. They do not represent a release, but we want to hold onto the code
        because we may want to go back to it, AND the branch (in SVN) was never
        merged back into Trunk. That is, if we don't make it into a tag (and
        just delete the git branch), git will eventually garbage-collect it.

2. Should be deleted. That is, we don't care for the history.

We must categorize all the "svn->git" branches. into the two categories above.


Check that history is how we want it
------------------------------------
See http://techbase.kde.org/Projects/MoveToGit/UsingSvn2Git. Also, SVN merge history may not be carried over correctly: http://blog.agavi.org/post/16865375185/fixing-svn-merge-history-in-git-repositories.


Information/research
====================

svn2git
-------
There are 2 things called svn2git:
1. A C++ tool developed by KDE, that may require more configuration, but is
    faster than #2. https://gitorious.org/svn2git. This might need to run
    servers-side? This has good mechanisms for splitting an svn repository into
    multiple git repositories.
2. a Ruby wrapper of git-svn that assumes more about the structure of the SVN
    repository. https://github.com/nirvdrum/svn2git

Useful websites
---------------
http://stackoverflow.com/questions/3009738/what-does-this-svn2git-error-mean/4434188#4434188

http://stackoverflow.com/questions/1216733/remove-a-directory-permanently-from-git

http://stackoverflow.com/questions/359424/detach-subdirectory-into-separate-git-repository

http://gitorious.org/svn2git/svn2git/source/539de0386876ed470f2ae6be90a98421493b3c90:samples

http://git-scm.com/book/en/Git-and-Other-Systems-Migrating-to-Git

http://cogumbreiro.blogspot.com/2013/05/how-to-install-git-subtree-in-ubuntu.html

# mutliple directories to split off:
http://stackoverflow.com/questions/3910412/split-large-git-repository-into-many-smaller-ones

Split apart a monolithic repo into several smaller ones while preserving commit
history:
https://gist.github.com/ChrisLundquist/4341033

Removing large files from the history:
http://git-scm.com/book/ch9-7.html

http://stackoverflow.com/questions/7067015/svn2git-with-exclude-any-way-to-ignore-the-empty-blank-commits

Working with nonstandard SVN directory structure:
http://lostincode.net/posts/git-svn-stitching

Check integrity of git repository:
git fsck --full to check integrity


contributors_from_log.txt
-------------------------
List of all (simtk) usernames for people who have contributed to the SVN
repository. Generated using the following from
https://github.com/nirvdrum/svn2git:
`$ svn log --quiet http://path/to/root/of/project | grep -E "r[0-9]+ \| .+ \|" | awk '{print $3}' | sort | uniq`

Git subtree split
-----------------


Questions
=========

Why does git svn start at revision 1029?
----------------------------------------
That's when Trunk started; all previous revisions were to ZLoadPoint.


Why do some of the "svn->git" branches have "@<svn-revision-#>" at the end?
---------------------------------------------------------------------------
Look at `$ man git svn`: "These additional branches are created if git svn
cannot find a parent commit for the first commit in an SVN branch, to connect
the branch to the history of the other branches."



Decisions
=========
1) Keep ZLoadPoint (all that existed up to rev 1028)?
2) Keep LegacyCode?
3) Keep <branch/tag>
4) Split off GUI?
5) Is it okay to lose the branches for the new CFSQP repository?
6) Naming style for git tags referring to releases? I would prefer "v3.1.0",
etc.
