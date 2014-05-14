# termformat [![Build Status](https://travis-ci.org/tyrannosaurus/termformat.svg?branch=master)](https://travis-ci.org/tyrannosaurus/termformat)

[Erlang External Term Format](http://erlang.org/doc/apps/erts/erl_ext_dist.html) (de)serialization module.

# Installation

`termformat` can be installed as any other python module, e.g. with `pip`:
```bash
$ pip install termformat
```
But make sure that you have `python-devel` package installed.

# Usage

```python
import termformat

binary = termformat.encode(20) # => b'\x83a\x14'
print termformat.decode(binary) # => 20
```

# Datatypes representation

<table>
    <tr>
        <td>Type</td>
        <td>Python</td>
        <td>Erlang</td>
    </tr>
    <tr>
        <td>Integer</td>
        <td>int, long</td>
        <td>SMALL_INT_EXT, INT_EXT, SMALL_BIG_EXT, LARGE_BIG_EXT</td>
    </tr>
    <tr>
        <td>Float</td>
        <td>float</td>
        <td>FLOAT_EXT, NEW_FLOAT_EXT*</td>
    </tr>
    <tr>
        <td>String</td>
        <td>str, unicode, bytes</td>
        <td>BINARY_EXT, STRING_EXT*</td>
    </tr>
    <tr>
        <td>Atom</td>
        <td>String with ":" prefix</td>
        <td>ATOM_EXT</td>
    </tr>
    <tr>
        <td>Tuple</td>
        <td>tuple</td>
        <td>SMALL_TUPLE_EXT, LARGE_TUPLE_EXT</td>
    </tr>
    <tr>
        <td>List</td>
        <td>list</td>
        <td>LIST_EXT, NIL_EXT</td>
    </tr>
</table>

[1] Only decoding support  
[2] If you need to encode/decode more complex types (such as booleans, datetime objects and dictionaries), see [beretta](https://github.com/tyrannosaurus/beretta)  
