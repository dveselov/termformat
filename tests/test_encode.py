# coding: utf-8
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
    with self.assertRaises(ValueError):
      bytes = termformat.encode(False)
      self.assertEqual(bytes, b'\x83d\x00\x05false')

  def test_encode_true(self):
    with self.assertRaises(ValueError):
      bytes = termformat.encode(True)
      self.assertEqual(bytes, b'\x83d\x00\x04true')

  def test_encode_none(self):
    with self.assertRaises(ValueError):
      bytes = termformat.encode(None)
      self.assertEqual(bytes, b'\x83d\x00\tundefined')

  def test_encode_small_int(self):
    bytes = termformat.encode(20)
    self.assertEqual(bytes, b'\x83a\x14')

  def test_encode_medium_int(self):
    bytes = termformat.encode(300)
    self.assertEqual(bytes, b'\x83b\x00\x00\x01,')

  def test_encode_big_int(self):
    bytes = termformat.encode(4294967295)
    self.assertEqual(bytes, b'\x83n\x04\x00\xff\xff\xff\xff')

  def test_encode_large_int(self):
    bytes = termformat.encode(4294967295 ** 1000)
    self.assertEqual(bytes[:2], b'\x83o')

  def test_encode_big_negative_int(self):
    bytes = termformat.encode(-4294967296)
    self.assertEqual(bytes, b'\x83n\x05\x01\x00\x00\x00\x00\x01')

  def test_encode_float(self):
    bytes = termformat.encode(3.14)
    self.assertEqual(bytes, b'\x83c3.14000000000000012434e+00\x00\x00\x00\x00\x00')

  def test_encode_zero_float(self):
    bytes = termformat.encode(0.0)
    self.assertEqual(bytes, b'\x83c0.00000000000000000000e+00\x00\x00\x00\x00\x00')

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

  def test_encode_small_set(self):
    bytes = termformat.encode({1, 2, 3})
    self.assertIn(bytes, [b'\x83h\x03a\x01a\x02a\x03', b'\x83h\x03a\x03a\x02a\x01'])

  def test_encode_large_set(self):
    bytes = termformat.encode(set(range(1024)))
    self.assertEqual(bytes[:5], b'\x83i\x00\x00\x04')

  def test_encode_complex_tuple(self):
    bytes = termformat.encode((1, 1337, 3.14, "binary", ":atom", ":true", ":false", ":undefined",
                               [2, [2]], (1, 2, 3)))
    self.assertEqual(bytes, b'\x83h\na\x01b\x00\x00\x059c3.14000000000000012434e+00'
                            b'\x00\x00\x00\x00\x00m\x00\x00\x00\x06binaryd\x00\x04'
                            b'atomd\x00\x04trued\x00\x05falsed\x00\tundefinedl\x00'
                            b'\x00\x00\x02a\x02l\x00\x00\x00\x01a\x02jjh\x03a\x01a'
                            b'\x02a\x03')

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
      self.assertEqual(bytes, b'\x83m\x00\x00\x00\x01:')

  def test_encode_large_atom(self):
    with self.assertRaises(ValueError):
      atom = LargeAtomMock()
      bytes = termformat.encode(atom)

  def test_encode_atom_with_upper_chars(self):
    bytes = termformat.encode(":Foo")
    self.assertEqual(bytes, b'\x83d\x00\x03Foo')

  def test_encode_not_supported_data_type(self):
    with self.assertRaises(ValueError):
      bytes = termformat.encode({'dictionary': 'item'})

  def test_encode_binary(self):
    bytes = termformat.encode('foo')
    self.assertEqual(bytes, b'\x83m\x00\x00\x00\x03foo')

  def test_encode_unicode_binary(self):
    bytes = termformat.encode(u'тест')
    self.assertEqual(bytes, b'\x83m\x00\x00\x00\x08\xd1\x82\xd0\xb5\xd1\x81\xd1\x82')

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

  def test_encode_with_compression(self):
    plain, compressed = termformat.encode([[1, 2, 3]] * 10), termformat.encode([[1, 2, 3]] * 10, 6)
    self.assertTrue(len(plain) > len(compressed))
