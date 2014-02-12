from distutils.core import setup
from distutils.extension import Extension


setup(
  name = 'termformat',
  url = 'https://github.com/dieselpoweredkitten/termformat',
  author = 'termformat contributors',
  author_email = 'github@require.pm',
  version = '0.1.1',
  description = 'Erlang External Term Format (de)serialization module',
  license = 'MIT',
  ext_modules = [
    Extension('termformat', ['termformat.c'])
  ],
  classifiers = (
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
  ),
)
