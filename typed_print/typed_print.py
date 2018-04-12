from __future__ import print_function
import re
from huepy import *

try:
    import __builtin__
except ImportError:
    import builtins as __builtin__   # Python 3


# Save normal print
printr = __builtin__.print


# Custom formatters 
def format_str(x):
    '''
        This processing is applied to all arguments of all types other than the ones found in `type_map`.
        E.g. an object `obj` of type NeuralNet wighout a rule in `type_map` is first represented as string str(obj)
        and then some parts of the string are highlighted using this function.
    '''
    if TP.str_mode == HIGHLIGHT_DIGITS:    
        return TP.apply_regexp(str(x), TP.re_digits)
    
    elif TP.str_mode == HIGHLIGHT_NUMBERS:
        return TP.apply_regexp(str(x), TP.re_numbers)
    
    elif TP.str_mode == HIGHLIGHT_CUSTOM:
        return TP.apply_regexp(str(x), TP.re_custom)
    
    elif TP.str_mode == HIGHLIGHT_NOTHING:
        return str(x)
    
    else:
        assert False, 'Wrong str_mode'

def format_list(x):
    return bold(good('')) + bold('List length = {}\n\n'.format(len(x))) + TP.typed_print_format(str(x))

def format_dict(x):
    return bold(good('')) + bold('Dict size = {}\n\n'.format(len(x))) + TP.typed_print_format(str(x))



# String modes
HIGHLIGHT_NOTHING = 0
HIGHLIGHT_DIGITS = 1
HIGHLIGHT_NUMBERS = 2
HIGHLIGHT_CUSTOM = 3


class TP(object):
    
    re_digits = re.compile("\d+")
    re_numbers = re.compile("[-]?[.]?[\d]+[\.]?\d*(?:[eE][-+]?\d+)?")
    re_custom = None
    
    str_mode  = None

    # Default palettes
    palette = dict(
        light = {
            int: lightcyan,
            float: blue,
            list: format_list,
            dict: format_dict
        },
        dark = {
            int: cyan,
            float: orange,
            list: format_list,
            dict: format_dict
        }
    )

    type_map = {} 

    highlight_word_list = []

    @classmethod
    def apply_regexp(cls, x, re_compiled):
        '''
            Splits string using regexp and applies the rules from type_map to each part
        '''
        indices = []
        for m in re_compiled.finditer(str(x)):
            indices.append(m.start())
            indices.append(m.end())

        if len(indices) == 0:
            return x

        shift = 0
        if indices[0] != 0:
            indices.insert(0, 0)
            shift = 1

        parts = [x[i:j] for i,j in zip(indices, indices[1:]+[None])]

        for i in range(shift, len(parts), 2):
            parts[i] = cls.type_map[int](parts[i])

        
        return ''.join(parts)

    @classmethod
    def typed_print_format(cls, *args, **kwargs):
        """
            This function returns formatted string
        """
        
        res = ' '.join([cls.type_map.get(type(arg), format_str)(arg) for arg in args])

        for word in cls.highlight_word_list: 
            res = res.replace(str(word), bold(red(str(word))))

        return res 

    @classmethod
    def typed_print(cls, *args, **kwargs):
        res = cls.typed_print_format(*args, **kwargs)        
        return __builtin__.print(res, **kwargs)

    



def init(palette, str_mode=HIGHLIGHT_NUMBERS, custom_type_map=None, highlight_word_list=None, re_custom=None):
    '''
        
    '''

    if custom_type_map is not None:
        if not isinstance(custom_type_map, dict):
            assert False, 'custom_type_map should be a dictionary.'

        TP.type_map = custom_type_map
    else:
        if palette not in TP.palette:
            assert False, 'Please either choose from standad themes: ' \
                           + str(list(TP.palette.keys())) \
                           + ' or provide `custom_type_map`'

        TP.type_map = TP.palette[palette] 

    TP.highlight_word_list = highlight_word_list if highlight_word_list is not None else []
    
    TP.str_mode = str_mode

    if TP.str_mode == HIGHLIGHT_CUSTOM:
        if re_custom is None:
            assert False, 'Please provide custom compiled re pattern'

        TP.re_custom = re_custom

    return TP.typed_print   
