Moving the OpenSim code repository from Subversion (SVN) to Git
***************************************************************
This document details the thought and procedure that went into moving OpenSim
from an SVN repository at https://simtk.org/svn/opensim to a Git repository
hosted primarily at https://github.com/opensim-org/opensim. 

The OpenSim GUI source code is NOT moved to git; it remains in SVN. Also, CFSQP
is moved into a separate repository, since we are not licensed to distribute
it.

Michael Sherman moved the Simbody code repository from SVN to Git in August,
2013. Simbody was previosly hosted at simtk.org, as well. His work provided the
groundwork for this work.

This document is written by Chris Dembia and Justin Si.

Dependencies
============
1. Ubuntu 13.10. Subsequent versions probably work fine.
2. svn2git 2.2.2 (https://github.com/nirvdrum/svn2git). Obtain via:

    $ sudo apt-get install git-core git-svn ruby rubygems
    $ sudo gem install svn2git

3. Python 2.7.
4. dos2unix command line program:

    $ sudo apt-get install dos2unix

5. curl command line program, for deleting and creating GitHub repositories:

    $ sudo apt-get install curl

Performing the conversion
=========================
1. Define the environment variable OPENSIMTOGIT_LOCAL_DIR specifying the local
   destination of the new git repository. For example:

    $ export OPENSIMTOGIT_LOCAL_DIR=~/opensim_git_repos

   In fact, if you do not set this environment variable yourself, we'll use the
   value above.

   TODO define OPENSIMTOGIT_GITHUB_USERNAME.

2. Run the python file. We actually try to obtain svn2git for you.

    $ python opensim2git.py

3. Now you have a 2 local repositories in OPENSIMTOGIT_LOCAL_DIR: (1)
   opensim-core, the OpenSim API, and (2) cfsqp, the CFSQP library. This is how
   I expect this to happen: (1) an administrator of github.com/opensim-org
   creates an 'opensim-core' and a 'cfsqp' repository in the opensim-org
   organization.

    $ cd $OPENSIMTOGIT_LOCAL_DIR/opensim-core
    $ git remote add opensim-org git@github.com:opensim-org/opensim-core
    $ git push --all opensim-org
    $ cd $OPENSIMTOGIT_LOCAL_DIR/cfsqp
    $ git remote add opensim-org git@github.com:opensim-org/opensim-core
    $ git push --all opensim-org


In revision 6663, the repository was reorganized. Thus, it seems to make sense
to start the git repository from this revision.

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

This page is especially helpful:
http://stackoverflow.com/questions/2982055/detach-many-subdirectories-into-a-new-separate-git-repository

I also think this would be a great job for kde's svn2git, as you can specify
to place things in subdirectories as such:

match /trunk/KDE/kdesdk/doc/${NAMES}/
  repository ${REPO}
  branch master
  prefix doc/
  min revision 409203
end match

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


Clean up
--------
Files to purge from the history:
Opensim/Java/opensim.jar


Information/research
====================

SVNMapper
---------
Visualize branching history of an SVN repository. http://svnmapper.tigris.org/

svn2git
-------
There are 2 things called svn2git:
1. A C++ tool developed by KDE, that may require more configuration, but is
    faster than #2. https://gitorious.org/svn2git. This might need to run
    servers-side? This has good mechanisms for splitting an svn repository into
    multiple git repositories. To learn more, see kde-svn2git below.
2. a Ruby wrapper of git-svn that assumes more about the structure of the SVN
    repository. https://github.com/nirvdrum/svn2git


kde-svn2git
-----------
Get this in Ubuntu repositories as svn-all-fast-export. See the
opensim2git.rules file, and the kde-svn2git target in the Makefile. Using this
requires that you have a local copy of the WHOLE svn repository (not a working
copy). See
http://bob.ippoli.to/archives/2006/09/14/svnsync-mirror-your-svn-repository/
to create such a copy (a mirror).

For us, do the following:

```
svnadmin create opensim-svn-mirror
echo '#!/bin/sh' > opensim-svn-mirror/hooks/pre-revprop-change
chmod +x opensim-svn-mirror/hooks/pre-revprop-change
svnsync init file://PATH_TO/opensim-svn-mirror https://simtk.org/svn/opensim
svnsync sync file://PATH_TO/opensim-svn-mirror
```

where, for me, PATH_TO is '/home/fitze/Documents/opensim2git/svnmirror'.

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


What was in the old OpenSim/Bin folder?
---------------------------------------
When we separate the repositories, and rip out the old history, how do we
decide if stuff like this is preserved, and if so, in which repository? Maybe
we don't want to edit the history.


Should we preserve history after splitting the repository?
----------------------------------------------------------
As soon as we split the repository, all history is nonfunctional; it would
just be for referencing what was done in the past. So (1) either people would
need to refer to the old svn repository to see the (functional) history, or
(2) we let people still access the history, to do blames or whatnot, but they
won't be able to run the code at that point; for that they'll need to go to
svn.

When Wrapping was just Java; should that remain in the history of
opensim-core, or in the history of Wrapping? I think the former, since it IS
somewhat functional there.


Do we actually want to split the SVN repository into multiple repositories?
---------------------------------------------------------------------------

Cons of splitting / Pro's of not splitting
1.  The repositories can be inconsistent with each other; we'd have to specify
    the commit of dependency repositories. This would be more complex. Are the
    GUI and the API too coupled?
2.  Really complicates the maintenance of history. Especially since the
    repository has been restructured quite a bit.

Pro's of splitting / Cons of not splitting
1.  We want GUI programmers to be able to hit the ground running. We can do this
    in 2 ways: (1) don't split the repositories, and track the SWIG output, or (2)
    split the repositories and distribute pre-built versions of the API. Option
    (1) violates git convention of not tracking machine-generated files, so (2)
    seems more attractive. So splitting the repositories is one way of allowing
    GUI programmers to hit the ground running.
2.  Ayman has mentioned that when preparing for a release, he must spend
    substantial time just ensuring that the GUI is consistent with the API. This
    would not be an issue if the GUI were able to depend on a specific version of
    the API. BUT, this dependence can be removed simply by relying on git
    branches to ensure that Ayman works with a 'stable' version of the API.
3.  The repository might be upwards of 1 gigabyte. Splitting would reduce the
    size needed for people working on just one project. This comes into play
    more when a developer is simultaneously working on two branches, and this
    needs two clones of the repository.

A third option: Keep everything in 1 repository, but maintain separate CMake
projects. We would only have separate repositories for really decoupled
projects. CFSQP can be in a separate repository.


Decisions
=========
1) Keep ZLoadPoint (all that existed up to rev 1028)?
2) Keep LegacyCode?
3) Keep <branch/tag>
4) Split off GUI?
5) Is it okay to lose the branches for the new CFSQP repository?
6) Naming style for git tags referring to releases? I would prefer "v3.1.0",
etc.

TODO When we push our repository to GitHub, we get a few notices about how big the
repository is:
remote: warning: GH001: Large files detected.                                       
remote: warning: See http://git.io/iEPt8g for more information.                     
remote: warning: File Documentation/OpenSim_Splash.psd is 65.68 MB; this is
larger t
han GitHub's recommended maximum file size of 50 MB                                 
remote: warning: File Documentation/OpenSim_Splash_2_2_1.psd is 65.66 MB; this
is la
rger than GitHub's recommended maximum file size of 50 MB                          
remote: warning: File Documentation/Figures/CoverArt/OpenSim_Layers.psd is
65.05 MB;
 this is larger than GitHub's recommended maximum file size of 50 MB                
 remote: warning: File Documentation/OpenSim_Splash_2_2_1.psd is 65.79 MB; this
 is la
 rger than GitHub's recommended maximum file size of 50 MB                           
 remote: warning: File Vendors/lib/Win32/VC8/OpenSim_SimTKmath_static_d.lib is
 53.92 
 remote: warning: File Vendors/lib/Win32/VC8/OpenSim_SimTKsimbody_static_d.lib
 is 50.
 86 MB; this is larger than GitHub's recommended maximum file size of 50 MB          
 remote: warning: File Vendors/lib/Win32/VC8/OpenSim_SimTKmath_static_d.lib is
 60.48 
 MB; this is larger than GitHub's recommended maximum file size of 50 MB             
 remote: warning: File Vendors/lib/Win32/VC8/OpenSim_SimTKsimbody_static_d.lib
 is 50.
 49 MB; this is larger than GitHub's recommended maximum file size of 50 MB          
 remote: warning: File Vendors/lib/OpenSim_SimTKmath_static_d.lib is 60.48 MB;
 this i
 s larger than GitHub's recommended maximum file size of 50 MB                       
 remote: warning: File Vendors/lib/OpenSim_SimTKsimbody_static_d.lib is 50.46
 MB; thi
 s is larger than GitHub's recommended maximum file size of 50 MB


 Keep models or not?
 ===================
 The OutputReference left in repo: 217M, 820M with working copy
 Remove OutputReference from history: 141M, 383M with working copy
 (with only Trunk; no branches)
