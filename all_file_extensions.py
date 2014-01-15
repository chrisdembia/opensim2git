"""Prints a list of all the file extensions found in the current directory,
and in all subdirectories.

"""
import os

exts = []
for dirpath, dirnames, filenames in os.walk('.'):
    if '.git' in dirnames:
        dirnames.remove('.git')
    for fname in filenames:
        ext = os.path.splitext(os.path.join(dirpath, fname))[1]
        if ext not in exts:
            exts.append(ext)
print exts

