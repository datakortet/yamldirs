import os
import sys

# oschmod can only barely be argued to do the right thing on windows...
# but windows permissions are so much more advanced that linux that there 
# is really not much overlap... punting for now.
import oschmod


def get_mode(path):
    """Return the mode attributes of the file.
    """
    # return oct(os.stat(path).st_mode & 0o7777)
    return oct(oschmod.get_mode(path))


def get_owner(path):
    owner = oschmod.get_owner(path)
    if sys.platform == 'win32':
        return f'{owner[1]}\\\\{owner[0]}'
    return owner


def get_group(path):
    grp = oschmod.get_group(path)
    if sys.platform == 'win32':
        return f'{grp[1]}\\\\{grp[0]}'
    return owner
