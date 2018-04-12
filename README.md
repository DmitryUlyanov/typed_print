# Example
The output is colorized based on the argument's type. Additionally some keywords can be highlighted (like `Epoch` here). If you are printing a sting the numbers are still getting highlighted (`loss` argument).
```
e = 4
print(f'Epoch [{e}/{300}]', 3, 3231.32, 'loss=-22.4e-9 time=121mc')
```
<table style="border-width:0px; width:100%">
  <th>Light palette</th>
  <th>Dark palette</th>
  <tr>
    <td width=50%><img src="https://raw.githubusercontent.com/DmitryUlyanov/dmitryulyanov.github.io/master/assets/typed_print/args_light.png"/></td>
    <td width=50%><img src="https://raw.githubusercontent.com/DmitryUlyanov/dmitryulyanov.github.io/master/assets/typed_print/args_dark.png"/></td>
  </tr>
</table>


Of course everything is customizable. For example you can override list printing like that:
```
print([131, 'I love cats', 'String with number 9'])
```
<table style="border-width:0px; width:100%">
  <th>Light palette</th>
  <th>Dark palette</th>
  <tr>
    <td width=50%><img src="https://raw.githubusercontent.com/DmitryUlyanov/dmitryulyanov.github.io/master/assets/typed_print/list_light.png"/></td>
    <td width=50%><img src="https://raw.githubusercontent.com/DmitryUlyanov/dmitryulyanov.github.io/master/assets/typed_print/list_dark.png"/></td>
  </tr>
</table>


# Features

- Type based coloring and printing layout.
- Automatic highlighting guided by regexp or list of keywords.
- Extensible and customizable framework: easily change representation for any type of objects including the default types like `int`, `list`, `dict`, etc.

# Install

```
pip install typed_print
```

Tested with Ubuntu 14.04 and Python 3.6.

# Usage

For the examples above The printing function is initialized as follows:
```
import typed_print as tp

print = tp.init(palette='light', str_mode=tp.HIGHLIGHT_NUMBERS, highlight_word_list=['Epoch'])
```

## Arguments

- `palette`: highlighting palette. Use `dark` if background of your terminal is dark and `light` otherwise
- `str_mode`: what to highlight in string and sting representations of objects of unknown types. Possible values:
  - `tp.HIGHLIGHT_NOTHING`
  - `tp.HIGHLIGHT_DIGITS`
  - `tp.HIGHLIGHT_NUMBERS`
  - `tp.HIGHLIGHT_CUSTOM`: in this case you should pass a compiled regex extractor as `re_custom` argument to `tp.init`, e.g.
    - `re_custom=re.compile("\d+")`
- `custom_type_map`: a dictionary with correspondence `type:processor_fn`. `processor_fn` should return string representation for the object, like `__str__` or `__repr__`.
  - `highlight_word_list`: a list of words to highlight. In the example above `highlight_word_list=['Epoch']`

## Why overriding print function?
 I did not find a way to override  `__str__` or `__repr__` for default types. Thus the only way to change the way the objects of default type are printed using custom print function.
