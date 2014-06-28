import termformat
from unittest import TestCase


class UtilsTestCase(TestCase):

  def test_is_valid_atom(self):
    self.assertTrue(termformat.is_atom(":foo"))
    self.assertTrue(termformat.is_atom(u":foo"))
    self.assertTrue(termformat.is_atom(":Bar"))

  def test_is_invalid_atom(self):
    self.assertFalse(termformat.is_atom("foo"))
    self.assertFalse(termformat.is_atom(12))
    self.assertFalse(termformat.is_atom(3.14))
    self.assertFalse(termformat.is_atom([":foo", ":bar"]))
    self.assertFalse(termformat.is_atom({1, 2, 3}))
    self.assertFalse(termformat.is_atom((4, 5, 6)))

  def test_success_binary_to_atom(self):
    result = termformat.binary_to_atom("foo")
    self.assertEqual(result, ":foo")

  def test_pass_invalid_value_to_binary_to_atom(self):
    with self.assertRaises(ValueError):
      termformat.binary_to_atom(":foo")

  def test_success_atom_to_binary(self):
    result = termformat.atom_to_binary(":foo")
    self.assertEqual(result, "foo")

  def test_pass_invalid_value_to_atom_to_binary(self):
    with self.assertRaises(ValueError):
      termformat.atom_to_binary("foo")
    with self.assertRaises(ValueError):
      termformat.atom_to_binary(3.14)
