""" Attempt to clone https://github.com/michaeldv/awesome_print

Usage:
    from awesome_print import ap
    ap(object)
"""
import __builtin__
from types import *

STRING_TYPES = (StringType, UnicodeType)
NUMBER_TYPES = (IntType, LongType, FloatType, ComplexType)

def ap(*args, **kwargs):
    options = {
        'indent'     : 4,      # Indent using 4 spaces.
        'index'      : True,   # Display array indices.
        'html'       : False,  # Use ANSI color codes rather than HTML.
        'multiline'  : True,   # Display in multiple lines.
        'plain'      : False,  # Use colors.
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
        return red('None', options)

    if type is TypeType:
        pass

    if type is BooleanType:
        return green(unicode(obj), options)

    if type in STRING_TYPES:
        print level, obj
        return yellow('"' + unicode(obj) + '"', options)

    if type in NUMBER_TYPES:
        return bold_blue(unicode(obj), options)

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
                index_str = light_gray(('[%' + width + 'd] ') % i, options)

            lines.append(('%s%s%s') % (indent(level + 1, options), index_str, format(value, options, level + 1)))

        return open_char + newline(options) + \
               ("," + newline(options)).join(lines) + \
               newline(options) + indent(level, options) + close_char

    if type is DictType:
        if len(obj) is 0:
            return '{}'

        width = max(len(str(key)) for key in obj)
        lines = []

        keys = obj.keys()
        if options['sort_keys']:
            keys = sorted(keys)

        for key in keys:
            value = obj[key]
            formatted_key = format_key(key, options)
            format_padding = len(formatted_key) - len(str(key))

            lines.append(('%s%' + str(width + format_padding) + 's %s %s') % \
                    (indent(level + 1, options), format_key(key, options), light_gray(':', options), format(value, options, level + 1)))

        return '{' + newline(options) + \
                        ("," + newline(options)).join(lines) + \
               newline(options) + indent(level, options) + '}'

    if type is LambdaType:
        return unicode(obj)

    return unicode(obj)

def format_key(key_obj, options):
    key_type = __builtin__.type(key_obj)

    if key_type in STRING_TYPES + NUMBER_TYPES:
        return format(key_obj, options)

    return str(key_obj)

def max_line_len(str):
    return max(len(line) for line in str.split("\n"))

def black(str, options):
    return color(str, '30', options)

def dark_gray(str, options):
    return bold(str, '30', options)

def red(str, options):
    return color(str, '31', options)

def bold_red(str, options):
    return bold(str, '31', options)

def green(str, options):
    return color(str, '32', options)

def green(str, options):
    return bold(str, '32', options)

def yellow(str, options):
    return color(str, '33', options)

def bold_yellow(str, options):
    return bold(str, '33', options)

def blue(str, options):
    return color(str, '34', options)

def bold_blue(str, options):
    return bold(str, '34', options)

def purple(str, options):
    return color(str, '35', options)

def bold_purple(str, options):
    return bold(str, '35', options)

def cyan(str, options):
    return color(str, '36', options)

def bold_cyan(str, options):
    return bold(str, '36', options)

def light_gray(str, options):
    return color(str, '37', options)

def white(str, options):
    return bold(str, '37', options)

def color(str, color, options, intensity='0'):
    if options['plain']:
    	return str
    return '\033['+intensity+';'+color+'m'+str+'\033[0m'

def bold(str, col, options):
    if options['plain']:
    	return str
    return color(str, col, options, '1')
