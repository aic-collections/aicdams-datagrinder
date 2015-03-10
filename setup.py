import sys

from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = {
    'packages' : ['cherrypy'],
    'excludes' : [],
    'path' : sys.path,
    'compressed' : True,
}

import sys
base = 'Win32Service' if sys.platform=='win32' else None

executables = [
    Executable('server.py', base=base, targetName = 'datagrinder')
]

setup(name='Datagrinder',
      version = '1.0beta1',
      description = 'Data processing service for the AIC DAMS',
      options = dict(build_exe = buildOptions),
      executables = executables)
