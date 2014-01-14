import termformat
from unittest import TestCase


class TermFormatDecoderTest(TestCase):

  def test_decode_atom(self):
    pass

  def test_decode_false(self):
    result = termformat.decode(b'\x83d\x00\x05false')
    self.assertEqual(result, False)

  def test_decode_true(self):
    result = termformat.decode(b'\x83d\x00\x04true')
    self.assertEqual(result, True)

  def test_decode_none(self):
    result = termformat.decode(b'\x83d\x00\x03nil')
    self.assertEqual(result, None)

  def test_decode_small_int(self):
    result = termformat.decode(b'\x83a\x14')
    self.assertEqual(result, 20)

  def test_decode_medium_int(self):
    result = termformat.decode(b'\x83b\x00\x00\x01,')
    self.assertEqual(result, 300)

  def test_decode_large_int(self):
    result = termformat.decode(b'\x83n\x05\x00\x00\x00\x00\x00\x01')
    self.assertEqual(result, 4294967296)

  def test_decode_large_negative_int(self):
    result = termformat.decode(b'\x83n\x05\x01\x00\x00\x00\x00\x01')
    self.assertEqual(result, -4294967296)
