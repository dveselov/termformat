import sys; PYPY = hasattr(sys, 'pypy_version_info')

from distutils.core import setup
from distutils.extension import Extension

base = {
  'name': 'termformat',
  'url': 'https://github.com/tyrannosaurus/termformat',
  'author': 'termformat contributors',
  'author_email': 'github@require.pm',
  'version': '0.1.5',
  'description': 'Erlang External Term Format (de)serialization module',
  'license': 'MIT',
  'classifiers': (
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
  )
}

if PYPY:
  modules = {
    'packages': ['termformat'],
  }
else:
  modules = {
    'ext_modules': [
      Extension('termformat', ['termformat.c'])
    ],
  }
base.update(modules)

setup(**base)
