from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING, Dict, Optional, overload

from typing_extensions import Literal

if TYPE_CHECKING:
    from .element import Element

Color = Literal[
    # basic colors
    'black',
    'silver',
    'gray',
    'white',
    'maroon',
    'red',
    'purple',
    'fuchsia',
    'green',
    'lime',
    'olive',
    'yellow',
    'navy',
    'blue',
    'teal',
    'aqua',
    # extended colors
    'aliceblue',
    'antiquewhite',
    'aqua',
    'aquamarine',
    'azure',
    'beige',
    'bisque',
    'black',
    'blanchedalmond',
    'blue',
    'blueviolet',
    'brown',
    'burlywood',
    'cadetblue',
    'chartreuse',
    'chocolate',
    'coral',
    'cornflowerblue',
    'cornsilk',
    'crimson',
    'cyan',
    'darkblue',
    'darkcyan',
    'darkgoldenrod',
    'darkgray',
    'darkgreen',
    'darkgrey',
    'darkkhaki',
    'darkmagenta',
    'darkolivegreen',
    'darkorange',
    'darkorchid',
    'darkred',
    'darksalmon',
    'darkseagreen',
    'darkslateblue',
    'darkslategray',
    'darkslategrey',
    'darkturquoise',
    'darkviolet',
    'deeppink',
    'deepskyblue',
    'dimgray',
    'dimgrey',
    'dodgerblue',
    'firebrick',
    'floralwhite',
    'forestgreen',
    'fuchsia',
    'gainsboro',
    'ghostwhite',
    'gold',
    'goldenrod',
    'gray',
    'green',
    'greenyellow',
    'grey',
    'honeydew',
    'hotpink',
    'indianred',
    'indigo',
    'ivory',
    'khaki',
    'lavender',
    'lavenderblush',
    'lawngreen',
    'lemonchiffon',
    'lightblue',
    'lightcoral',
    'lightcyan',
    'lightgoldenrodyellow',
    'lightgray',
    'lightgreen',
    'lightgrey',
    'lightpink',
    'lightsalmon',
    'lightseagreen',
    'lightskyblue',
    'lightslategray',
    'lightslategrey',
    'lightsteelblue',
    'lightyellow',
    'lime',
    'limegreen',
    'linen',
    'magenta',
    'maroon',
    'mediumaquamarine',
    'mediumblue',
    'mediumorchid',
    'mediumpurple',
    'mediumseagreen',
    'mediumslateblue',
    'mediumspringgreen',
    'mediumturquoise',
    'mediumvioletred',
    'midnightblue',
    'mintcream',
    'mistyrose',
    'moccasin',
    'navajowhite',
    'navy',
    'oldlace',
    'olive',
    'olivedrab',
    'orange',
    'orangered',
    'orchid',
    'palegoldenrod',
    'palegreen',
    'paleturquoise',
    'palevioletred',
    'papayawhip',
    'peachpuff',
    'peru',
    'pink',
    'plum',
    'powderblue',
    'purple',
    'red',
    'rosybrown',
    'royalblue',
    'saddlebrown',
    'salmon',
    'sandybrown',
    'seagreen',
    'seashell',
    'sienna',
    'silver',
    'skyblue',
    'slateblue',
    'slategray',
    'slategrey',
    'snow',
    'springgreen',
    'steelblue',
    'tan',
    'teal',
    'thistle',
    'tomato',
    'turquoise',
    'violet',
    'wheat',
    'white',
    'whitesmoke',
    'yellow',
    'yellowgreen',
]


class ColorProperty:

    def __init__(self, style: Style, key: str) -> None:
        self.style = style
        self.key = key

    @overload
    def __call__(self, color: Color) -> Style:
        '''Use a predefined color name.'''

    @overload
    def __call__(self, value: str) -> Style:
        '''Use an arbitrary value.'''

    def __call__(self, value: str) -> Style:
        self.style.element._style[self.key] = value
        return self.style


class DimensionProperty:

    def __init__(self, style: Style, key: str) -> None:
        self.style = style
        self.key = key

    @overload
    def __call__(self, px: float) -> Style:
        '''Use a value in pixels.'''

    @overload
    def __call__(self, rem: float) -> Style:
        '''Use a value in rem.'''

    @overload
    def __call__(self, percent: float) -> Style:
        '''Use a value in percent.'''

    @overload
    def __call__(self, value: Literal['auto', 'max-content', 'min-content', 'fit-content']) -> Style:
        '''Use a predefined value.'''

    @overload
    def __call__(self, value: str) -> Style:
        '''Use an arbitrary value.'''

    def __call__(self, value: str = ..., *, px: float = ..., rem: float = ..., percent: float = ...) -> Style:
        if value is not ...:
            self.style.element._style[self.key] = value
        elif px is not ...:
            self.style.element._style[self.key] = f'{px}px'
        elif rem is not ...:
            self.style.element._style[self.key] = f'{rem}rem'
        elif percent is not ...:
            self.style.element._style[self.key] = f'{percent}%'
        else:
            raise TypeError(f'{self.key} dimension requires either px, rem or percent')
        return self.style


class Style:

    def __init__(self, element: 'Element') -> None:
        self.element = element

        self.color = ColorProperty(self, 'color')
        '''Set the color of the element.'''

        self.background_color = ColorProperty(self, 'background-color')
        '''Set the background color of the element.'''

        self.width = DimensionProperty(self, 'width')
        '''Set the width of the element.'''

        self.height = DimensionProperty(self, 'height')
        '''Set the height of the element.'''

        self.margin = DimensionProperty(self, 'margin')
        '''Set the margin of the element.'''

        self.padding = DimensionProperty(self, 'padding')
        '''Set the padding of the element.'''

    def __call__(self, add: Optional[str] = None, *, remove: Optional[str] = None, replace: Optional[str] = None):
        '''CSS style sheet definitions to modify the look of the element.
        Every style in the `remove` parameter will be removed from the element.
        Styles are separated with a semicolon.
        This can be helpful if the predefined style sheet definitions by NiceGUI are not wanted in a particular styling.
        '''
        style_dict = deepcopy(self.element._style) if replace is None else {}
        for key in self._parse(remove):
            if key in style_dict:
                del style_dict[key]
        style_dict.update(self._parse(add))
        style_dict.update(self._parse(replace))
        if self.element._style != style_dict:
            self.element._style = style_dict
            self.element.update()
        return self.element

    @staticmethod
    def _parse(text: Optional[str]) -> Dict[str, str]:
        result = {}
        for word in (text or '').split(';'):
            word = word.strip()
            if word:
                key, value = word.split(':', 1)
                result[key.strip()] = value.strip()
        return result
