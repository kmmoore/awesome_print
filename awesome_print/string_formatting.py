from lib import enum
import types

__colors = { # (ANSI Code, Hex color)
    'Default': (0, '#000'),
    'Black': (30, '#000'),
    'White': (37, '#FFF'),
    'Red': (31, '#F00'),
    'Green': (32, '#0F0'),
    'Yellow': (33, '#FF0'),
    'Blue': (34, '#00F'),
    'Purple': (35, '#F0F'),
    'Cyan': (36, '#0FF'),
    'None': ()
}

__colors_items = __colors.items()
__color_list = [i[1] for i in __colors_items]

Color = enum(*[i[0] for i in __colors_items])
Align = enum('RIGHT', 'LEFT', 'CENTER')

def applyColor(string, color, strong, options):
    """ Returns a string that will be displayed as `string` in the color `color` """
    if options['plain']:
        return string
    
    if color == Color.None:
        return string

    if not color in range(len(__color_list)):
        raise Exception("Invalid color name.")

    color_value = __color_list[color]

    if options['html']:
        tag = 'b' if strong else 'span'
        return u'<{tag} style="color:{color}">{string}</{tag}>'.format(tag=tag, color=color_value[1], string=string)
    else:
        intensity = '1' if strong else '0'
        return u'\033[{intensity};{code}m{string}\033[0m'.format(code=color_value[0], intensity=intensity, string=string)


def indent(level, options, additional_padding = 0):
    """ Returns the appropriate indentation string for the given level and options.
        `additional_padding` is added to the end of the necessary indentation. """
    if not options['multiline']:
        return ''

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

def format_key(key_obj):
    """ Returns the formatted representation of `key_obj` when it is a key in a dictionary. """

    key_type = type(key_obj)

    key_str = unicode(key_obj)
    if key_type in types.StringTypes:
        key_str = '"' + key_str + '"' 
    return key_str.replace("\n", "\\n")

def formatted_key_width(obj, options):
    """ Returns the width of the formatted key (without the ANSI color code characters). """

    return len(format_key(obj))
