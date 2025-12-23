from distutils.core import setup
from Cython.Build import cythonize  # @UnresolvedImport
import os
import numpy

if 'QSWAT_PROJECT' in os.environ and 'Linux' in os.environ['QSWAT_PROJECT']:
    includePath = '/usr/include/python3.'
    sep = ':'
    is32 = '_32' in os.environ['QSWAT_PROJECT']
elif 'QSWAT_PROJECT' in os.environ and 'Mac' in os.environ['QSWAT_PROJECT']:
    includePath = '/usr/local/opt/python@3.9/Frameworks/Python.framework/Versions/3.9/include/python3.9'
    sep = ':'
    is32 = '_32' in os.environ['QSWAT_PROJECT']
else:
    # Windows
    osgeo_root = os.environ.get('OSGEO4W_ROOT', '')
    includePath = osgeo_root + r'/apps/Python37/include'
    sep = ';'
    is32 = False

numpyInclude = numpy.get_include()

if 'INCLUDE' in os.environ:
    os.environ['INCLUDE'] = os.environ['INCLUDE'] + sep + includePath + sep + numpyInclude
else:
    os.environ['INCLUDE'] = includePath + sep + numpyInclude

print('include path is {0}'.format(os.environ['INCLUDE']))

extensions = cythonize('*.pyx', include_path = [os.environ['INCLUDE']])

for ext in extensions:
    if ext.include_dirs is None:
        ext.include_dirs = []
    ext.include_dirs.append(numpyInclude)

if is32:
    pass
else:
    setup(
        name = "pyxes",
        package_dir = {'QSWATPlus': ''},
        ext_modules = extensions,
    )
