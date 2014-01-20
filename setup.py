from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
  name = 'termformat',
  version = '0.1',
  description = 'Erlang External Term Format (de)serialization module',
  license = 'MIT',
  cmdclass = {'build_ext': build_ext},
  ext_modules = [Extension('termformat', ['termformat.pyx'])],
  classifiers = (
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
  )
)
