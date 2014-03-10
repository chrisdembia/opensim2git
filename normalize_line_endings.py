import os
import mimetypes

def is_text(fpath):
    print fpath, mimetypes.guess_type(fpath)
    return mimetypes.guess_type(fpath)[0].startswith('text')

for dirpath, dirnames, filenames in os.walk('.'):
    for fpath in filenames:
        if is_text('%s/%s' % (dirpath, fpath)):
            os.system('fromdos %s/%s' % (dirpath, fpath))
            
