from awesome_print import ap

ap([{"a\nb": 1, (1,2,3):2, 'b':4, 'q':[1,2,[1,2,3]]}, 2, u"A unicode\nstring\nmore stuff!", [1,2,3,4,5,6,6,7,8,9,9,{'a': u"An em dash: \u2014\nMore characters! \u2192", 'b': -1.445}]], options={'indent': 2})