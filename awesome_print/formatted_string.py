def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

Color = enum('DEFAULT', 'BLACK', 'WHITE', 'DARK_GREY', 'LIGHT_GREY', 'RED', 'BOLD_RED', 'GREEN', 'BOLD_GREEN', 'YELLOW', 'BOLD_YELLOW', 'BLUE', 'BOLD_BLUE', 'PURPLE', 'BOLD_PURPLE', 'CYAN', 'BOLD_CYAN', 'NONE')
Align = enum('RIGHT', 'LEFT', 'CENTER')

ansi_color_map = ((0,0), (30,0), (37,1), (30,1), (37,0), (31,0), (31,1), (32,0), (32,1), (33,0), (33,1), (34,0), (34,1), (35,0), (35,1), (36,0), (36,1))

def applyColor(string, color, options):
    if options['plain']:
        return string
    
    if color == Color.NONE:
        return string

    mapped = ansi_color_map[color]

    return '\033['+str(mapped[1])+';'+str(mapped[0])+'m'+string+'\033[0m'


class FormattedString():
    """Represents a string and a color"""

    ansi_color_map = ((0,0), (30,0), (37,1), (30,1), (37,0), (31,0), (31,1), (32,0), (32,1), (33,0), (33,1), (34,0), (34,1), (35,0), (35,1), (36,0), (36,1))

    def __init__(self, string, color):
        self.lines = string.split("\n")
        self.color = color

    @staticmethod
    def addColor(string, color, intensity):
        return '\033['+str(intensity)+';'+str(color)+'m'+string+'\033[0m'

    def length(self):
        return sum(len(l) for l in self.lines)

    def lines(self):
        return self.lines

    def ansi_lines(self):
        if self.color == Color.NONE:
            return self.lines

        mapped = FormattedString.ansi_color_map[self.color]

        return [FormattedString.addColor(s, mapped[0], mapped[1]) for s in self.lines]

    def html_lines(self):
        return '<b>' + self.string + '</b>'

class FormattedBlock():

    def __init__(self, indent, align):
        self.indent = indent
        self.align = align
        self.formatted_strings = []

    def add_formatted_string(self, formatted_string):
        self.formatted_strings.append(formatted_string)

    def representation(self, options):
        final = ''
        indent = ' ' * self.indent

        for formatted_string in self.formatted_strings:
            final += "\n".join(formatted_string.ansi_lines())

        return final