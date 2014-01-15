import termformat
from unittest import TestCase

class LargeMock:
  def __len__(self):
    return 4294967296

class LargeAtomMock(LargeMock, str):
  pass

class LargeListMock(LargeMock, list):
  pass

class LargeTupleMock(LargeMock, tuple):
  pass

class LargeStringMock(LargeMock, str):
  pass

class TermFormatEncoderTest(TestCase):

  def test_encode_false(self):
    bytes = termformat.encode(False)
    self.assertEqual(bytes, b'\x83d\x00\x05false')

  def test_encode_true(self):
    bytes = termformat.encode(True)
    self.assertEqual(bytes, b'\x83d\x00\x04true')

  def test_encode_none(self):
    bytes = termformat.encode(None)
    self.assertEqual(bytes, b'\x83d\x00\x03nil')

  def test_encode_small_int(self):
    bytes = termformat.encode(20)
    self.assertEqual(bytes, b'\x83a\x14')

  def test_encode_medium_int(self):
    bytes = termformat.encode(300)
    self.assertEqual(bytes, b'\x83b\x00\x00\x01,')

  def test_encode_large_int(self):
    bytes = termformat.encode(4294967296)
    self.assertEqual(bytes, b'\x83n\x05\x00\x00\x00\x00\x00\x01')

  def test_encode_large_negative_int(self):
    bytes = termformat.encode(-4294967296)
    self.assertEqual(bytes, b'\x83n\x05\x01\x00\x00\x00\x00\x01')

  def test_encode_new_float(self):
    bytes = termformat.encode(3.14)
    self.assertEqual(bytes, b'\x83F@\t\x1e\xb8Q\xeb\x85\x1f')

  def test_encode_list(self):
    bytes = termformat.encode([1, 2, 3])
    self.assertEqual(bytes, b'\x83l\x00\x00\x00\x03a\x01a\x02a\x03j')

  def test_encode_empty_list(self):
    bytes = termformat.encode([])
    self.assertEqual(bytes, b'\x83j')

  def test_encode_large_list(self):
    with self.assertRaises(ValueError):
      list = LargeListMock()
      bytes = termformat.encode(list)

  def test_encode_small_tuple(self):
    bytes = termformat.encode((1, 2, 3))
    self.assertEqual(bytes, b'\x83h\x03a\x01a\x02a\x03')

  def test_encode_large_tuple(self):
    bytes = termformat.encode((1, 2, 3) * 256)
    self.assertEqual(bytes[:5], b'\x83i\x00\x00\x03')

  def test_encode_very_large_tuple(self):
    with self.assertRaises(ValueError):
      tuple = LargeTupleMock()
      bytes = termformat.encode(tuple)

  def test_encode_atom(self):
    bytes = termformat.encode(":foo")
    self.assertEqual(bytes, b'\x83d\x00\x03foo')

  def test_encode_atom_without_name(self):
    with self.assertRaises(ValueError):
      bytes = termformat.encode(":")

  def test_encode_large_atom(self):
    with self.assertRaises(ValueError):
      atom = LargeAtomMock()
      bytes = termformat.encode(atom)

  def test_encode_not_supported_data_type(self):
    with self.assertRaises(ValueError):
      bytes = termformat.encode({'dictionary': 'item'})

  def test_encode_binary(self):
    bytes = termformat.encode('foo')
    self.assertEqual(bytes, b'\x83m\x00\x00\x00\x03foo')

  def test_encode_empty_binary(self):
    bytes = termformat.encode('')
    self.assertEqual(bytes, b'\x83m\x00\x00\x00\x00')

  def test_encode_large_binary(self):
    with self.assertRaises(ValueError):
      string = LargeStringMock()
      bytes = termformat.encode(string)

  def test_encode_unicode(self):
    bytes = termformat.encode(u'foo')
    self.assertEqual(bytes, b'\x83m\x00\x00\x00\x03foo')

  def test_encode_bytes(self):
    bytes = termformat.encode(b'foo')
    self.assertEqual(bytes, b'\x83m\x00\x00\x00\x03foo')
