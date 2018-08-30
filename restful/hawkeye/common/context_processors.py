# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./common/context_processors.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 599 bytes
import os
from django.conf import settings
_VERSION_FILE = os.path.join(settings.BASE_DIR, '.version.info')
VERSION_HASH = ''
if os.path.isfile(_VERSION_FILE):
    with open(_VERSION_FILE) as (file):
        VERSION_HASH = file.read()
_GIT_LIB_EXISTS = True
try:
    import git
except ImportError:
    _GIT_LIB_EXISTS = False

if _GIT_LIB_EXISTS:
    try:
        repo = git.Repo()
        if repo is not None:
            VERSION_HASH = repo.head.object.hexsha
    except git.InvalidGitRepositoryError:
        pass

    def build_info(request):
        return {'git_hash': VERSION_HASH}
# okay decompiling ./restful/hawkeye/common/context_processors.pyc
