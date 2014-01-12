from struct import pack, unpack

cdef str DEFAULT_ENCODING
cdef bytes ERL_NEW_FLOAT, ERL_COMPRESSED, ERL_SMALL_INT, ERL_INT, ERL_FLOAT, ERL_ATOM, ERL_SMALL_TUPLE, ERL_LARGE_TUPLE, ERL_NIL, ERL_STRING, ERL_BINARY, ERL_SMALL_BIGNUM, ERL_LARGE_BIGNUM, ERL_VERSION

DEFAULT_ENCODING = "utf-8"

ERL_NEW_FLOAT = pack('>B', 70)
ERL_COMPRESSED = pack('>B', 80)
ERL_SMALL_INT = pack('>B', 97)
ERL_INT = pack('>B', 98)
ERL_FLOAT = pack('>B', 99)
ERL_ATOM = pack('>B', 100)
ERL_SMALL_TUPLE = pack('>B', 104)
ERL_LARGE_TUPLE = pack('>B', 105)
ERL_NIL = pack('>B', 106)
ERL_STRING = pack('>B', 107)
ERL_LIST = pack('>B', 108)
ERL_BINARY = pack('>B', 109)
ERL_SMALL_BIGNUM = pack('>B', 110)
ERL_LARGE_BIGNUM = pack('>B', 111)
ERL_VERSION = pack('>B', 131)


cdef bytes encode_term(object term):
  term_type = type(term)
  if term is False:
    return encode_term(":false")
  elif term is True:
    return encode_term(":true")
  elif term is None:
    return encode_term(":nil")
  elif term_type is int:
    if 0 <= term <= 255:
      return ERL_SMALL_INT + pack('>B', term)
    elif -2147483648 <= term <= 2147483647:
      return ERL_INT + pack('>l', term)
    else:
      raise NotImplementedError(term_type)
  elif term_type is float:
    return ERL_NEW_FLOAT + pack('>d', term)
  elif term_type is str:
    term = term.encode(DEFAULT_ENCODING)
    if term.startswith(b":"):
      atom_name = term[1:]
      length = len(atom_name)
      if not length or length > 255:
        raise ValueError("Invalid atom length: {}".format(term))
      else:
        return ERL_ATOM + pack('>H', length) + atom_name
    else:
      length = len(term)
      if length > 4294967295:
        raise ValueError("Invalid binary length: {}".format(length))
      else:
        return ERL_BINARY + pack('>L', length) + term
  elif term_type is tuple:
    length = len(term)
    if length < 256:
      tuple_type, length = ERL_SMALL_TUPLE, pack('>B', length)
    elif length <= 4294967295:
      tuple_type, length = ERL_LARGE_TUPLE, pack('>L', length)
    else:
      raise ValueError("Invalid tuple length: {}".format(length))
    content = tuple_type + length
    for item in term:
      content += encode_term(item)
    return content
  elif term_type is list:
    length = len(term)
    if not length:
      return ERL_NIL
    elif length <= 4294967295:
      body = pack('>L', length)
      for item in term:
        body += encode_term(item)
      return ERL_LIST + body + ERL_NIL
    else:
      raise ValueError("Invalid list length: {}".format(length))
  elif term_type is unicode:
    new_term = term.encode(DEFAULT_ENCODING)
    return encode_term(new_term)
  elif term_type is bytes:
    new_term = term.decode(DEFAULT_ENCODING)
    return encode_term(new_term)
  else:
    raise ValueError("Unknown data type: {}".format(term_type))

def encode(object term):
  BODY = encode_term(term)
  return ERL_VERSION + BODY
