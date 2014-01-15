#!/bin/sh
# Convert all files from DOS to UNIX line endings, but skip the .git directory.
# http://stackoverflow.com/questions/2228039/how-to-run-a-command-recursively-on-all-files-except-for-those-under-svn-direct
find . -type f \! -path \*/\.git/\* -exec dos2unix --quiet {} \;
