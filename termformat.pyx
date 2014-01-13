from struct import pack, unpack

try:
  # Python 2.7
  long = long
except NameError:
  # Python 3.3
  long = int

cdef str DEFAULT_ENCODING
cdef bytes ERL_NEW_FLOAT, ERL_COMPRESSED, ERL_SMALL_INT, ERL_INT, ERL_FLOAT, ERL_ATOM, ERL_SMALL_TUPLE, ERL_LARGE_TUPLE, ERL_NIL, ERL_STRING, ERL_BINARY, ERL_SMALL_BIGNUM, ERL_LARGE_BIGNUM, ERL_MAGIC

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
ERL_MAGIC = pack('>B', 131)


cdef bytes encode_term(object term):
  term_type = type(term)
  if term is False:
    return encode_term(":false")
  elif term is True:
    return encode_term(":true")
  elif term is None:
    return encode_term(":nil")
  elif term_type in (int, long):
    if 0 <= term <= 255:
      return ERL_SMALL_INT + pack('>B', term)
    elif -2147483648 <= term <= 2147483647:
      return ERL_INT + pack('>l', term)
    else:
      sign, term = (0, term) if term >= 0 else (1, -term)
      body = b""
      while term:
        body += pack('>B', term & 0xff)
        term >>= 8
      length = len(body)
      sign = pack('>B', sign)
      if length <= 255:
        return ERL_SMALL_BIGNUM + pack('>B', length) + sign + body
      elif length <= 4294967295:
        return ERL_LARGE_BIGNUM + pack('>L', length) + sign + body
      else:
        raise ValueError("Invalid integer length: {0}".format(length))
  elif term_type is float:
    return ERL_NEW_FLOAT + pack('>d', term)
  elif term_type is bytes:
    if term.startswith(b":"):
      atom_name = term[1:]
      length = len(atom_name)
      if not length or length > 255:
        raise ValueError("Invalid atom length: {0}".format(term))
      else:
        return ERL_ATOM + pack('>H', length) + atom_name
    else:
      length = len(term)
      if length <= 4294967295:
        return ERL_BINARY + pack('>L', length) + term
      else:
        raise ValueError("Invalid binary length: {0}".format(length))
  elif term_type in (str, unicode):
    new_term = term.encode(DEFAULT_ENCODING)
    return encode_term(new_term)
  elif term_type is tuple:
    length = len(term)
    if length <= 255:
      tuple_type, length = ERL_SMALL_TUPLE, pack('>B', length)
    elif length <= 4294967295:
      tuple_type, length = ERL_LARGE_TUPLE, pack('>L', length)
    else:
      raise ValueError("Invalid tuple length: {0}".format(length))
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
      raise ValueError("Invalid list length: {0}".format(length))
  else:
    raise ValueError("Unknown data type: {0}".format(term_type))

def encode(object term):
  BODY = encode_term(term)
  return ERL_MAGIC + BODY
