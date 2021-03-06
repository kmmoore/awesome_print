# encoding: utf-8
import sys
sys.path.insert(0, 'awesome_print')

import unittest
from awesome_print import format

class Test_awesome_print(unittest.TestCase):
    options = {
        'indent'     : 2,      # Indent using 4 spaces.
        'index'      : True,   # Display array indices.
        'html'       : False,  # Use ANSI color codes rather than HTML.
        'multiline'  : True,   # Display in multiple lines.
        'plain'      : False,  # Use colors.
        'raw'        : False,  # Do not recursively format object instance variables.
        'sort_keys'  : False,  # Do not sort hash keys.
        'limit'      : False,  # Limit large output for arrays and hashes. Set to a boolean or integer.
    }

    def test_None(self):
        self.assertEqual(format(None, self.options), '\x1b[0;31mNone\x1b[0m')

    def test_True(self):
        self.assertEqual(format(True, self.options), '\x1b[1;32mTrue\x1b[0m')

    def test_False(self):
        self.assertEqual(format(False, self.options), '\x1b[1;32mFalse\x1b[0m')

    def test_String_plain(self):
        self.assertEqual(format('plain string', self.options), '\x1b[0;33mplain string\x1b[0m')

    def test_String_with_escapes(self):
        self.assertEqual(format("with\n's", self.options), '\x1b[0;33mwith\n\'s\x1b[0m')

    def test_String_unicode(self):
        self.assertEqual(format(u'plain \u2014 string', self.options), u'\x1b[0;33mplain \u2014 string\x1b[0m')

    def test_Int_positive(self):
        self.assertEqual(format(12345, self.options), '\x1b[1;34m12345\x1b[0m')

    def test_Int_negative(self):
        self.assertEqual(format(-12345, self.options), '\x1b[1;34m-12345\x1b[0m')

    def test_Long_positive(self):
        self.assertEqual(format(12345l, self.options), '\x1b[1;34m12345\x1b[0m')

    def test_Long_negative(self):
        self.assertEqual(format(-12345l, self.options), '\x1b[1;34m-12345\x1b[0m')

    def test_Float_positive(self):
        self.assertEqual(format(123.45, self.options), '\x1b[1;34m123.45\x1b[0m')

    def test_Float_negative(self):
        self.assertEqual(format(-123.45, self.options), '\x1b[1;34m-123.45\x1b[0m')

    def test_Complex_positive(self):
        self.assertEqual(format(complex('1.2+3.45j'), self.options),
                '\x1b[1;34m(1.2+3.45j)\x1b[0m')

    def test_Complex_negative(self):
        self.assertEqual(format(complex('-1.2+3.45j'), self.options),
                '\x1b[1;34m(-1.2+3.45j)\x1b[0m')

    def test_Tuple_empty(self):
        self.assertEqual(format((), self.options), '()')

    def test_Tuple_Int(self):
        self.assertEqual(format((1,), self.options), '(\n  [0] \x1b[1;34m1\x1b[0m\n)')

    def test_Tuple_mixed(self):
        self.assertEqual(format((1,True,'string'), self.options),
            '(\n' +
            '  [0] \x1b[1;34m1\x1b[0m,\n' +
            '  [1] \x1b[1;32mTrue\x1b[0m,\n' +
            '  [2] \x1b[0;33mstring\x1b[0m\n' +
            ')')

    def test_List_empty(self):
        self.assertEqual(format([], self.options), '[]')

    def test_List_Int(self):
        self.assertEqual(format([1], self.options), '[\n  [0] \x1b[1;34m1\x1b[0m\n]')

    def test_List_mixed(self):
        self.assertEqual(format([1,True,'string'], self.options),
            '[\n' +
            '  [0] \x1b[1;34m1\x1b[0m,\n' +
            '  [1] \x1b[1;32mTrue\x1b[0m,\n' +
            '  [2] \x1b[0;33mstring\x1b[0m\n' +
            ']')

    def test_Dict_empty(self):
        self.assertEqual(format({}, self.options), '{}')

    def test_Dict_Int(self):
        self.assertEqual(format({1:2}, self.options),
                '{\n  \x1b[1;34m1\x1b[0m: \x1b[1;34m2\x1b[0m\n}')

    def test_Dict_mixed(self):
        self.assertEqual(format({None:False,'key':'value',2:5}, self.options),
                '{\n' +
                '     \x1b[1;34m2\x1b[0m: \x1b[1;34m5\x1b[0m,\n' +
                '  \x1b[0;31mNone\x1b[0m: \x1b[1;32mFalse\x1b[0m,\n' +
                '   \x1b[0;33mkey\x1b[0m: \x1b[0;33mvalue\x1b[0m\n' +
                '}')

    def test_List_in_List(self):
        self.assertEqual(format(
            [
                [1,2,3],
            ], self.options),
            '[\n' +
            '  [0] [\n' +
            '    [0] \x1b[1;34m1\x1b[0m,\n' +
            '    [1] \x1b[1;34m2\x1b[0m,\n' +
            '    [2] \x1b[1;34m3\x1b[0m\n' +
            '  ]\n' +
            ']'
            )

    def test_Dict_in_List(self):
        self.assertEqual(format(
            [
                {
                    'a': 'b'
                }
            ], self.options),
            '[\n' +
            '  [0] {\n' +
            '    \x1b[0;33ma\x1b[0m: \x1b[0;33mb\x1b[0m\n' +
            '  }\n' +
            ']'
            )


if __name__ == '__main__':
    unittest.main()
