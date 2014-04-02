""" Attempt to clone https://github.com/michaeldv/awesome_print

Usage:
    from awesome_print import ap
    ap(object)
"""
import __builtin__
from types import *
from formatted_string import applyColor, FormattedString, FormattedBlock, Color

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

Align = enum('RIGHT', 'LEFT')

STRING_TYPES = (StringType, UnicodeType)
NUMBER_TYPES = (IntType, LongType, FloatType, ComplexType)

def ap(*args, **kwargs):
    options = {
        'indent'     : 2,      # Indent using 4 spaces.
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

def indent(level, options, additional_padding = 0):
    if options['html']:
        space = '&nbsp;'
    else:
        space = ' '

    return space * (options['indent'] * level + additional_padding)

def newline(options):
    if not options['multiline']:
        return ' '

    if options['html']:
        return '<br>'

    return "\n"

def format(obj, options, level = 0, additional_padding = 0, align = Align.LEFT):
    type = __builtin__.type(obj)

    if type is NoneType:
        return applyColor('None', Color.PURPLE, options)

    if type is TypeType:
        pass

    if type is BooleanType:
        applyColor(unicode(obj), Color.GREEN, options)

    if type in STRING_TYPES:
        lines = ('"' + obj + '"').split("\n")


        if align == Align.RIGHT:
            width = max(len(l) for l in lines)
            lines = ["{l:>{width}}".format(l=l, width=width) for l in lines]

        line_sep = newline(options) + " " + indent(level, options, additional_padding)

        return line_sep.join(applyColor(l, Color.YELLOW, options) for l in lines)

    if type in NUMBER_TYPES:
        return applyColor(unicode(obj), Color.BOLD_BLUE, options)

    if type in (TupleType, ListType):
        open_char, close_char = ('(', ')') if type is TupleType else ('[', ']')
        if len(obj) is 0:
            return open_char + close_char

        lines = []
        width = len(str(len(obj)-1))
        index_len = width + 3
        for i, value in enumerate(obj):
            index_str = ''
            if options['index']:
                index_str = applyColor(('[%' + str(width) + 'd] ') % i, Color.LIGHT_GREY, options)

            lines.append(('%s%s%s') % (indent(level + 1, options, additional_padding), index_str, format(value, options, level + 1, additional_padding + index_len)))

        return open_char + newline(options) + \
               ("," + newline(options)).join(lines) + \
               newline(options) + indent(level, options, additional_padding) + close_char

    if isinstance(obj, DictType):
        if len(obj) is 0:
            return '{}'

        lines = []
        width = max(formatted_key_width(key, options) for key in obj)
        key_len = width + 3

        keys = obj.keys()
        if options['sort_keys']:
            keys = sorted(keys)

        for key in keys:
            value = obj[key]
            key_str = "{key:>{width}}".format(key=format_key(key, options), width=width)
            key_str = applyColor(key_str, Color.BOLD_RED, options)

            lines.append(('%s%s %s %s') % \
                    (indent(level + 1, options, additional_padding), key_str, applyColor(':', Color.LIGHT_GREY, options), format(value, options, level + 1, additional_padding + key_len)))

        return '{' + newline(options) + \
                        ("," + newline(options)).join(lines) + \
               newline(options) + indent(level, options, additional_padding) + '}'

    if type is LambdaType:
        return unicode(obj)

    return unicode(obj)

def format_key(key_obj, options, level = 0, additional_padding = 0):
    """ Returns the formatted representation of `key_obj` when it is a key in a dictionary. """

    key_type = __builtin__.type(key_obj)

    key_str = unicode(key_obj)
    if key_type in STRING_TYPES:
        key_str = '"' + key_str + '"' 
    return key_str.replace("\n", "\\n")

def formatted_key_width(obj, options):
    """ Returns the width of the formatted key (without the ANSI color code characters). """

    plain_options = options.copy()
    plain_options['plain'] = True

    return max(len(l) for l in format_key(obj, plain_options).split("\n"));
