""" Attempt to clone https://github.com/michaeldv/awesome_print

Usage:
    from awesome_print import ap
    ap(object)
"""
import __builtin__
from types import *

def ap(*args, **kwargs):
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

    if 'options' in kwargs:
        options.update(kwargs['options'])

    for arg in args:
        print format(arg, options)

def indent(level, options):
    if options['html']:
        space = '&nbsp;'
    else:
        space = ' '

    return space * options['indent'] * level

def newline(options):
    if not options['multiline']:
        return ' '

    if options['html']:
        return '<br>'

    return "\n"

def format(obj, options, level = 0):
    type = __builtin__.type(obj)

    if type is NoneType:
        return red('None')

    if type is TypeType:
        pass

    if type is BooleanType:
        return green(unicode(obj))

    if type in [StringType, UnicodeType]:
        return yellow(unicode(obj))

    if type in [IntType, LongType, FloatType, ComplexType]:
        return bold_blue(unicode(obj))

    if type in (TupleType, ListType):
        open_char, close_char = ('(', ')') if type is TupleType else ('[', ']')
        if len(obj) is 0:
            return open_char + close_char

        lines = []
        index = 0
        width = str(len(str(len(obj))))
        for i, value in enumerate(obj):
            index_str = ''
            if options['index']:
                index_str = ('[%' + width + 'd] ') % i

            lines.append(('%s%s%s') % (indent(level + 1, options), index_str, format(value, options, level + 1)))

        return open_char + newline(options) + \
               ("," + newline(options)).join(lines) + \
               newline(options) + indent(level, options) + close_char

    if type is DictType:
        if len(obj) is 0:
            return '{}'

        width = str(max([flen(format(k, options)) for k in obj.keys()]))
        s = []
        for k in obj.keys():
            v = obj[k]
            s.append(('%s%' + width + 's: %s') % \
                    (indent(level + 1, options), format(k, options), format(v, options, level + 1)))

        return '{' + newline(options) + \
                        ("," + newline(options)).join(s) + \
               newline(options) + indent(level, options) + '}'

    if type is LambdaType:
        return unicode(obj)

    return unicode(obj)

def flen(str):
    return max(len(s) for s in str.split("\n"))

def black(str):
    return color(str, '30')

def dark_gray(str):
    return bold(str, '30')

def red(str):
    return color(str, '31')

def bold_red(str):
    return bold(str, '31')

def green(str):
    return color(str, '32')

def green(str):
    return bold(str, '32')

def yellow(str):
    return color(str, '33')

def bold_yellow(str):
    return bold(str, '33')

def blue(str):
    return color(str, '34')

def bold_blue(str):
    return bold(str, '34')

def purple(str):
    return color(str, '35')

def bold_purple(str):
    return bold(str, '35')

def cyan(str):
    return color(str, '36')

def bold_cyan(str):
    return bold(str, '36')

def light_gray(str):
    return color(str, '37')

def white(str):
    return bold(str, '37')

def color(str, color, intensity='0'):
    # if mode == 'plain':
    # 	return str
    return '\033['+intensity+';'+color+'m'+str+'\033[0m'

def bold(str, col):
    # if mode == 'plain':
    # 	return str
    return color(str, col, '1')
