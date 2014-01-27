Moving the OpenSim code repository from Subversion (SVN) to Git
===============================================================
This document details the thought and procedure that went into moving OpenSim
from an SVN repository at https://simtk.org/svn/opensim to a Git repository
hosted primarily at https://github.com/opensim-org/opensim. 

The OpenSim GUI source code is NOT moved to git; it remains in SVN. Also, CFSQP
is moved into a separate repository, since we are not licensed to distribute
it. This package contains a script that creates two git repositories, cfsqp,
and opensim-core. The package also contains a script to push these repositories
to GitHub.

Michael Sherman moved the Simbody code repository from SVN to Git in August,
2013. Simbody was previosly hosted at simtk.org, as well. His conversino
provided the groundwork for this conversion.

This document is written by Chris Dembia and Justin Si.

Dependencies
============
1. Ubuntu 13.10. Subsequent versions probably work fine.
2. Python 2.7.

The remaining dependencies are installed automatically:

    * curl: for deleting and creating repositories on the GitHub website.
    * git-core, git-svn, ruby, rubygems: for instaling svn2git.
    * svn2git: a submodule in this repo, which we install automatically.

Note that the version of svn2git we use is our own fork of svn2git. We made a
fork to implement a bugfix that was mentioned in the svn2git issues, but was
never fixed in an official release of svn2git.


Performing the conversion
=========================
1. Define the following environment variables (if not, defaults will be used):

    * OPENSIMTOGIT_LOCAL_DIR: We'll write the new git repositories to this
      location on your disk. Default: ~/opensim2git_local
    * OPENSIMTOGIT_GITHUB_USERNAME: We will create and push the new
      repositories to this account.

You can temporarily set environment variables by running the following in a
terminal::

    $ export OPENSIMTOGIT_LOCAL_DIR=~/opensim_git_repos


2. Run the script that does the svn2git conversion and creates git repositories
   on your local machine::

        $ python opensim2git.py

   This script does the following:

   * Runs svn2git twice; once for cfsqp, and once for opensim-core. Excludes
     files various from the new openism-core repository.
   * Runs filter-branch to ensure that line endings are ALWAYS only LF (\n,
     UNIX line endings). The reason why this is important is that some files
     have Windows line endings (CRLF, \r\n).
   * Delete old SVN branches/tags, convert some of them to git tags.
   * Repair merge history (SVN merges are not picked up by git).
   * Run git garbage collection on the local git repositories.
   * Add commits to both git repos that modify CMake files so that when the
     repos are pushed to GitHub, they are functional (the projects don't expect
     the now-missing directories).

3. Run the script that pushes the local git repositories to GitHub::

        $ python push_repositories_to_github.py

4. Transfer the git repositories to opensim-org.

In revision 6663, the repository was reorganized. Thus, it seems to make sense
to start the git repository from this revision.

Historical sections
===================
Below are old parts of this README that could have been deleted. However, I
decied to keep these here just so the thoughts aren't lost.

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


 Keep models or not?
 ===================
 The OutputReference left in repo: 217M, 820M with working copy
 Remove OutputReference from history: 141M, 383M with working copy
 (with only Trunk; no branches)
