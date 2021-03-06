# coding: utf-8
import termformat
from unittest import TestCase


class TermFormatDecoderTest(TestCase):

  def test_decode_atom(self):
    result = termformat.decode(b"\x83d\x00\x03foo")
    self.assertEqual(result, ":foo")

  def test_decode_incomplete_atom(self):
    with self.assertRaises(ValueError):
      result = termformat.decode(b"\x83d\x00\x03fo")
      self.assertEqual(result, ":foo")

  def test_decode_small_int(self):
    result = termformat.decode(b"\x83a\x14")
    self.assertEqual(result, 20)

  def test_decode_incomplete_small_int(self):
    with self.assertRaises(ValueError):
      result = termformat.decode(b"\x83a")
      self.assertEqual(result, 20)

  def test_decode_medium_int(self):
    result = termformat.decode(b"\x83b\x00\x00\x01,")
    self.assertEqual(result, 300)

  def test_decode_incomplete_medium_int(self):
    with self.assertRaises(ValueError):
      result = termformat.decode(b"\x83b\x00\x00\x01")
      self.assertEqual(result, 300)

  def test_decode_large_int(self):
    result = termformat.decode(b"\x83n\x05\x00\x00\x00\x00\x00\x01")
    self.assertEqual(result, 4294967296)

  def test_decode_large_negative_int(self):
    result = termformat.decode(b"\x83n\x05\x01\x00\x00\x00\x00\x01")
    self.assertEqual(result, -4294967296)

  def test_decode_new_float(self):
    result = termformat.decode(b"\x83F@\t\x1e\xb8Q\xeb\x85\x1f")
    self.assertEqual(result, 3.14)

  def test_decode_float(self):
    result = termformat.decode(b"\x83c3.14000000000000012434e+00\x00\x00\x00\x00\x00")
    self.assertEqual(result, 3.14)

  def test_encode_zero_float(self):
    bytes = termformat.decode(b"\x83c0.00000000000000000000e+00\x00\x00\x00\x00\x00")
    self.assertEqual(bytes, 0.0)

  def test_decode_incomplete_float(self):
    with self.assertRaises(ValueError):
      result = termformat.decode(b"\x83F@\t\x1e\xb8Q\xeb\x85")
      self.assertEqual(result, 3.14)

  def test_decode_binary(self):
    result = termformat.decode(b"\x83m\x00\x00\x00\x03foo")
    self.assertEqual(result, "foo")

  def test_decode_unicode_binary(self):
    bytes = termformat.decode(b"\x83m\x00\x00\x00\x08\xd1\x82\xd0\xb5\xd1\x81\xd1\x82")
    self.assertEqual(bytes, u"тест")

  def test_decode_incomplete_binary(self):
    with self.assertRaises(ValueError):
      result = termformat.decode(b"\x83m\x00\x00\x00\x03fo")
      self.assertEqual(result, "foo")

  def test_decode_binary_with_negative_length(self):
    with self.assertRaises(ValueError):
      result = termformat.decode(b"\x83m\xff\xff\xff\xfdfoo")
      self.assertEqual(result, "foo")

  def test_decode_string(self):
    result = termformat.decode(b"\x83k\x00\x03foo")
    self.assertEqual(result, "foo")

  def test_decode_incomplete_string(self):
    with self.assertRaises(ValueError):
      result = termformat.decode(b"\x83k\x00\x03fo")
      self.assertEqual(result, "foo")

  def test_decode_empty_list(self):
    result = termformat.decode(b"\x83j")
    self.assertEqual(result, [])

  def test_decode_small_tuple(self):
    result = termformat.decode(b"\x83h\x03a\x01a\x02a\x03")
    self.assertEqual(result, (1, 2, 3))

  def test_decode_complex_tuple(self):
    result = termformat.decode(b"\x83h\na\x01b\x00\x00\x059c3.14000000000000012434e+00"
                               b"\x00\x00\x00\x00\x00m\x00\x00\x00\x06binaryd\x00\x04"
                               b"atomd\x00\x04trued\x00\x05falsed\x00\tundefinedl\x00"
                               b"\x00\x00\x02a\x02l\x00\x00\x00\x01a\x02jjh\x03a\x01a"
                               b"\x02a\x03")
    self.assertEqual(result, (1, 1337, 3.14, "binary", ":atom", ":true", ":false", ":undefined", [2, [2]], (1, 2, 3)))

  def test_decode_large_tuple(self):
    bytes = termformat.encode((1, 2, 3) * 256)
    result = termformat.decode(bytes)
    self.assertEqual(result, (1, 2, 3) * 256)

  def test_decode_incomplete_tuple(self):
    with self.assertRaises(ValueError):
      result = termformat.decode(b"\x83h\x03a\x01a\x02")
      self.assertEqual(result, (1, 2, 3))

  def test_decode_list(self):
    result = termformat.decode(b"\x83l\x00\x00\x00\x03a\x01a\x02a\x03j")
    self.assertEqual(result, [1, 2, 3])

  def test_decode_incomplete_list(self):
    with self.assertRaises(ValueError):
      result = termformat.decode(b"\x83l\x00\x00\x00\x03a\x01j")
      self.assertEqual(result, [1, 2, 3])

  def test_decode_unknown_type(self):
    with self.assertRaises(ValueError):
      result = termformat.decode(b"\x83z")
      self.assertEqual(result, None)

  def test_decode_invalid_magic(self):
    with self.assertRaises(ValueError):
      result = termformat.decode(b"\x84")
      self.assertEqual(result, None)

  def test_decode_compressed(self):
    bytes = termformat.encode([[1, 2, 3]] * 10, 6)
    self.assertEqual(termformat.decode(bytes), [[1, 2, 3]] * 10) 

  def test_decode_incomplete_compressed(self):
    bytes = termformat.encode([[1, 2, 3]] * 10, 6)
    with self.assertRaises(ValueError):
      self.assertEqual(termformat.decode(bytes[:-1]), [[1, 2, 3]] * 10) 
