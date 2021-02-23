#!/usr/bin/env python3
from libqtile import widget

PWRLINE_DEFAULT_SIZE = 16
_PWRLINECHARS = {
    'hortriangle': [u'\ue0b0', u'\ue0b2'],
    'horarrow':    [u'\ue0b1', u'\ue0b3'],
}


def PwrLine(left_color='#ffff00',
            right_color='#ff00ff', *,
            rtl=False,
            pwrtype='hortriangle',
            prefix='',
            suffix='',
            fontsize=PWRLINE_DEFAULT_SIZE,
            font='Source Code Pro Medium',
            **kwargs):
    """Returns a libqtile.widget.TextBox with the correct powerline symbol."""
    assert isinstance(rtl, bool)
    char = _PWRLINECHARS.get(pwrtype, '??')[rtl]
    if rtl:
        fg, bg = right_color, left_color
    else:
        fg, bg = left_color, right_color
    return widget.TextBox(prefix + char + suffix, fontsize=fontsize, font=font,
                          foreground=fg, background=bg, margin=0, padding=0,
                          **kwargs)


def _crop(f):
    f = min(max(float(f), 0.0), 1.0)
    return '{:0>2x}'.format(int(round(255 * f)))


class ColorScheme:
    """Provide a palette storage and calculation functions."""
    def __init__(self, names: dict = None):
        if names is None:
            self.names = {}
        else:
            assert isinstance(names, dict)
            assert all(isinstance(x, str) for x in names.keys())
            assert all(isinstance(x, tuple) and len(x) == 3
                       and all(isinstance(y, (float, int)) and 0 <= y <= 1 for y in x)
                       for x in names.values())
            self.names = names

    def __call__(self, *args, **kwargs):
        args = list(args)
        r, g, b = kwargs.get('r'), kwargs.get('g'), kwargs.get('b')
        l = kwargs.get('l')
        if isinstance(args[0], str) and args[0] in self.names.keys():
            r, g, b = self.names[args[0]]
            args.pop(0)
        else:
            if r is None and args:
                r = float(args.pop(0))
            else:
                r = 0.0
            if g is None and args:
                g = float(args.pop(0))
            else:
                g = 0.0
            if b is None and args:
                b = float(args.pop(0))
            else:
                b = 0.0
        if l is None:
            if args:
                l = float(args.pop(0))
            else:
                l = 1.0
        return '#' + ''.join(_crop(x * l) for x in [r, g, b])


palette = {
    'red':                 (1.000, 0.000, 0.000),  # ff0000
    'orange':              (1.000, 0.600, 0.000),  # ff9900
    'theme_orange':        (1.000, 0.325, 0.102),  # ff531a
    'yellow':              (1.000, 1.000, 0.000),  # ffff00
    'lime':                (0.500, 1.000, 0.000),  # 8fff00
    'green':               (0.000, 1.000, 0.000),  # 00ff00
    'cyan':                (0.000, 0.500, 1.000),  # 008fff
    'greenblue':           (0.000, 1.000, 1.000),  # 00ffff
    'lightblue':           (0.000, 0.500, 1.000),  # 008fff
    'blue':                (0.000, 0.000, 1.000),  # 0000ff
    'purple':              (0.500, 0.000, 1.000),  # 8f00ff
    'pink':                (1.000, 0.000, 1.000),  # ff00ff

    'white':               (1.000, 1.000, 1.000),  # ffffff
    'neutral':             (1.000, 1.000, 1.000),  # ffffff
    'black':               (0.000, 0.000, 0.000),  # 000000

    'active':              (0.000, 0.750, 1.000),  # 00bfff
    'inactive':            (0.000, 0.000, 0.000),  # 000000
    'barbackground':       (0.050, 0.050, 0.050),  # 0d0d0d

    'CPU_G':               (1.000, 0.000, 0.000),  # ff0000
    'RAM_G':               (0.000, 1.000, 0.000),  # 00ff00
    'SWAP_G':              (1.000, 0.200, 1.000),  # ff33ff
    'HDD_G':               (1.000, 0.600, 0.000),  # ff9900
    'NET_G':               (0.000, 0.750, 1.000),  # 00bfff
}
colors = ColorScheme(palette)
