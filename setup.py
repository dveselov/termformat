import platform
from distutils.core import setup
from distutils.extension import Extension

base = {
  'name': 'termformat',
  'url': 'https://github.com/tyrannosaurus/termformat',
  'author': 'termformat contributors',
  'author_email': 'github@require.pm',
  'version': '0.1.7',
  'description': 'Erlang External Term Format (de)serialization module',
  'license': 'MIT',
  'classifiers': (
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy',
  )
}

implementation = platform.python_implementation()

if implementation == "CPython":
  packages = {
    'ext_modules': [
      Extension('termformat', ['termformat.c'])
    ],
  }
else:
  packages = {
    'packages': ['termformat'],
  }

base.update(packages)
setup(**base)
