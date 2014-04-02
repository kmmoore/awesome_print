""" Attempt to clone https://github.com/michaeldv/awesome_print

Usage:
    from awesome_print import ap
    ap(object)
"""
import __builtin__
from types import *
from string_formatting import Align, Color, applyColor, indent, newline, format_key, formatted_key_width

NUMBER_TYPES = (IntType, LongType, FloatType, ComplexType)

def ap(*args, **kwargs):
    options = {
        'indent'     : 2,      # Indent using 2 spaces
        'index'      : True,   # Display array indices.
        'html'       : False,  # Output using HTML instead of ANSI
        'multiline'  : True,   # Display in multiple lines.
        'plain'      : False,  # Do not use colors.
        'sort_keys'  : True,   # Sort dictionary keys.
        'limit'      : False,  # Limit large output for arrays and hashes. Set to a boolean or integer.
    }

    if 'options' in kwargs:
        options.update(kwargs['options'])

    for arg in args:
        print format(arg, options)

def format(obj, options, level = 0, additional_padding = 0, align = Align.LEFT):
    obj_type = type(obj)

    if obj_type is NoneType:
        return applyColor('None', Color.Purple, False, options)

    if obj_type is TypeType:
        return applyColor(obj.__name__, Color.Cyan, False, options)

    if obj_type is BooleanType:
        applyColor(unicode(obj), Color.Green, False, options)

    if obj_type in StringTypes:
        lines = ('"' + obj + '"').split("\n")

        if align == Align.RIGHT:
            width = max(len(l) for l in lines)
            lines = ["{l:>{width}}".format(l=l, width=width) for l in lines]

        line_sep = newline(options) + " " + indent(level, options, additional_padding)

        return line_sep.join(applyColor(l, Color.Yellow, False, options) for l in lines)

    if obj_type in NUMBER_TYPES:
        return applyColor(unicode(obj), Color.Blue, False, options)

    if obj_type in (TupleType, ListType):
        if obj_type is TupleType:
            open_char, close_char = ('(', ')')
        else:
            open_char, close_char = ('[', ']')

        if len(obj) is 0:
            return open_char + close_char

        lines = []
        index_str_width = len(str(len(obj)-1))
        index_len = index_str_width + 3

        # Format all of the entries in the list/tuple with an optional index
        for i, value in enumerate(obj):
            index_str = ''
            if options['index']:
                index_str = "[{index:>{width}}] ".format(index=i, width=index_str_width)
                index_str = applyColor(index_str, Color.White, False, options)

            lines.append(('%s%s%s') % (indent(level + 1, options, additional_padding),
                                       index_str,
                                       format(value, options, level + 1, additional_padding + index_len)))

        # Print the full list
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

            # Format the key
            key_str = "{key:>{width}}".format(key=format_key(key), width=width)
            key_str = applyColor(key_str, Color.Red, True, options)

            # Add key and value together
            lines.append(('%s%s %s %s') % (indent(level + 1, options, additional_padding),
                                           key_str,
                                           applyColor(':', Color.White, False, options),
                                           format(value, options, level + 1, additional_padding + key_len)))

        return '{' + newline(options) + \
                ("," + newline(options)).join(lines) + \
                newline(options) + indent(level, options, additional_padding) + '}'
        
    return unicode(obj)