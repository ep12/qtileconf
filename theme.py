#!/usr/bin/env python3
from __future__ import annotations
import colorsys
from itertools import starmap
import json
import os
import re
import subprocess
import typing as T

from libqtile import hook, widget, qtile
from libqtile.utils import logger

try:
    from watchdog.observers import Observer  # type: ignore
    from watchdog.events import FileSystemEventHandler  # type: ignore
    WATCHDOG = False  # XXX: cairo out of mem error?

    class WalFSEHandler(FileSystemEventHandler):
        """File system event handler for (py)?wal."""
        def __init__(self, factory: 'WalThemeFactory'):
            self.factory = factory

        def on_modified(self, event):
            self.factory.reload_theme()

        on_created = on_modified
except ImportError:
    WATCHDOG = False

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
            _t_factory: T.Optional[T.Dict[str, T.Any]] = None,
            **kwargs):
    """Returns a libqtile.widget.TextBox with the correct powerline symbol."""
    assert isinstance(rtl, bool)
    # logger.info('PwrLine 1: _t_factory = %r', _t_factory)
    char = _PWRLINECHARS.get(pwrtype, '??')[rtl]
    if rtl:
        fg, bg = right_color, left_color
        if isinstance(_t_factory, dict):
            if 'left_color' in _t_factory:
                _t_factory['background'] = _t_factory.pop('left_color')
            if 'right_color' in _t_factory:
                _t_factory['foreground'] = _t_factory.pop('right_color')
    else:
        fg, bg = left_color, right_color
        if isinstance(_t_factory, dict):
            if 'left_color' in _t_factory:
                _t_factory['foreground'] = _t_factory.pop('left_color')
            if 'right_color' in _t_factory:
                _t_factory['background'] = _t_factory.pop('right_color')
    # if isinstance(_t_factory, dict):
    #     kwargs['_t_factory'] = _t_factory
    # logger.info('PwrLine 2: _t_factory = %r', _t_factory)
    return widget.TextBox(prefix + char + suffix, fontsize=fontsize, font=font,
                          foreground=fg, background=bg, margin=0, padding=0,
                          _t_factory=_t_factory, **kwargs)


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

NAMED_COLORS = {
    'black': 'color0',
    'red': 'color1',
    'green': 'color2',
    'orange': 'color3',
    'blue': 'color4',
    'magenta': 'color5',
    'cyan': 'color6',
    'gray': 'color7',
    'dim gray': 'color8',
    'b red': 'color9',
    'b green': 'color10',
    'yellow': 'color11',
    'b blue': 'color12',
    'b magenta': 'color13',
    'b cyan': 'color14',
    'white': 'color15'
}


class Color:
    """Represent a color as a tuple of r, g and b coordinates."""
    def __init__(self, spec: T.Union[T.Tuple[float, float, float], str]):
        r, g, b = 0., 0., 0.
        if isinstance(spec, tuple):
            assert len(spec) == 3
            r, g, b = spec
        elif m := re.match('#([0-9A-Za-z]{2})([0-9A-Za-z]{2})([0-9A-Za-z]{2})', spec):
            r, g, b = tuple(map(lambda x: int(x, 16) / 255, m.groups()))
        elif m := re.match(r'(?P<type>RGB|rgb|hsv)\(([\d\.]+),\s*([\d\.]+),\s*([\d\.]+)\)', spec):
            u, v, w = tuple(map(int, m.groups()[1:]))
            t = m.groupdict()['type']
            if t == 'RGB':
                r, g, b = u / 255, v / 255, w / 255
            if t == 'hsv':
                r, g, b = colorsys.hsv_to_rgb(u, v, w)
        for c in (r, g, b):
            if c < 0 or c > 1:
                raise ValueError('rgb coordinates must be in the unit interval')
        self.r, self.g, self.b = r, g, b

    def __str__(self):
        return self.s

    def __repr__(self):
        return f'Color({self.s!r})'

    def c(self, r, g, b):
        return Color(tuple(map(lambda c: max(0, min(1, c)), (r, g, b))))

    @property
    def s(self):
        return ''.join(map(lambda c: '%02x' % max(0, min(255, int(round(255 * c)))), self.t))

    @property
    def t(self):
        return self.r, self.g, self.b

    @property
    def hsv(self):
        return colorsys.rgb_to_hsv(*self.t)

    def brightness(self, value) -> Color:
        return self.c(self.r * value, self.g * value, self.b * value)

    def saturate(self, saturation) -> Color:
        h, s, v = self.hsv
        return self.c(*colorsys.hsv_to_rgb(h, max(0, min(1, s * saturation)), v))

    def hue_rotate(self, angle) -> Color:
        h, s, v = self.hsv
        return self.c(*colorsys.hsv_to_rgb((h + angle) % 1, s, v))

    def set_hsv_coord(self, *, h=None, s=None, v=None,
                      min_h=0, max_h=1, min_s=0, max_s=1, min_v=0, max_v=1) -> Color:
        h2, s2, v2 = self.hsv
        return self.c(*colorsys.hsv_to_rgb(max(min_h, min(max_h, h or h2)),
                                           max(min_s, min(max_s, s or s2)),
                                           max(min_v, min(max_v, v or v2))))

    def rgb_dist(self, other: Color) -> float:
        return sum(starmap(lambda x, y: (x - y) ** 2, zip(self.t, other.t)))

    def h_dist(self, other: Color) -> float:
        return abs(other.hsv[0] - self.hsv[0])

    def s_dist(self, other: Color) -> float:
        return abs(other.hsv[1] - self.hsv[1])

    def v_dist(self, other: Color) -> float:
        return abs(other.hsv[2] - self.hsv[2])

    def contrast_enforce(self, other: Color, v_contrast: float) -> Color:
        v, other_v = self.hsv[2], other.hsv[2]
        if abs(v - other_v) >= v_contrast:
            return self
        # Not ideal:
        new_v = min(1, other_v + v_contrast) if v > other_v else max(0, other_v - v_contrast)
        return self.set_hsv_coord(v=new_v)


DEF_VAL_TYPE = T.Union[str, T.Callable[['WalThemeFactory'], Color]]
DEF_TYPE = T.Dict[str, DEF_VAL_TYPE]


class WalThemeFactory:
    """Generate a theme on-the-fly using the selected (py)?wal colorscheme."""
    def __init__(self, default_theme_name: str,
                 cache_folder: str = os.path.expanduser('~/.cache/wal')):
        assert re.match(r'^(light|dark)/', default_theme_name)
        assert os.path.isdir(cache_folder)
        self.theme = default_theme_name
        self.cache_folder = cache_folder
        self.tdata: T.Dict[str, T.Any] = {}
        self.definitions_dark: DEF_TYPE = {}
        self.definitions_light: DEF_TYPE = {}
        self.load_json()
        hook.subscribe.startup_complete(self.apply_theme)
        self.observer: T.Optional[Observer] = None
        if WATCHDOG:  # THIS CAUSES AN ERROR: CAIRO_STATUS_NO_MEMORY
            self.observer = Observer()
            self.observer.schedule(WalFSEHandler(self), path=cache_folder, recursive=True)
            self.observer.start()

    def __del__(self):
        if self.observer is not None:
            self.observer.stop()
            self.observer.join()

    def load_theme_name(self) -> str:
        try:
            with open(os.path.join(self.cache_folder, 'theme.name')) as f:
                self.theme = f.read()
        except Exception as e:
            logger.error('Failed to load theme name: %r', e)
        return self.theme

    def __getitem__(self, item: str):
        if item in {'foreground', 'background', 'cursor'}:
            return self.tdata.get('special', {})[item]
        if item in NAMED_COLORS:
            try:
                return self.tdata.get('colors', {})[NAMED_COLORS[item]]
            except KeyError:
                pass
        try:
            return self.tdata.get('colors', {})[item]
        except KeyError:
            pass
        return self.tdata[item]

    def update_definitions(self, def_light: DEF_TYPE, def_dark: DEF_TYPE):
        k1, k2 = set(def_light), set(def_dark)
        if k1 != k2:
            logger.warning('Some definitions only appear in one variant: %r',
                           (k1 | k2) - (k1 & k2))
        self.definitions_light.update(def_light)
        self.definitions_dark.update(def_dark)
        self.run_definitions()

    @property
    def is_light_theme(self) -> bool:
        return self.theme.split('/', 1)[0] == 'light'

    # @lazy.function
    def switch_light(self, *_):
        variant, name = self.theme.split('/', 1)
        self.select_theme(('light' if variant == 'dark' else 'dark') + '/' + name)

    # @lazy.function
    def select_theme_interactively(self, *_):
        self.select_theme()

    def select_theme(self, name: T.Optional[str] = None):  # qtile
        cmd = [os.path.expanduser('~/.config/qtile/rofi-scripts/wal-select.fish')]
        if name is not None:
            cmd.append(name)
        try:
            subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            logger.error('Failed to run %r ~> %d:\n%r\n%r', cmd, e.returncode, e.stdout, e.stderr)
        self.reload_theme()

    def reload_theme(self):
        self.load_json()
        self.apply_theme()

    def load_json(self):
        self.load_theme_name()
        with open(os.path.join(self.cache_folder, 'colors.json')) as f:
            d = json.load(f)
        if not set(d).issuperset({'colors', 'special', 'wallpaper', 'alpha'}):
            logger.warning('Incomplete theme specification. Not reloading.')
            return
        d['colors'] = {k: Color(v) for k, v in d['colors'].items()}
        d['special'] = {k: Color(v) for k, v in d['special'].items()}
        self.tdata = d  # don't update: make sure all definitions are re-exec'd

    def run_definitions(self):
        self.tdata['colors'] = {k: v for k, v in self.tdata['colors'].items()
                                if re.fullmatch('color(\d|1[0-5])', k)}
        definitions = (self.definitions_light if self.is_light_theme
                       else self.definitions_dark).copy()
        while definitions:  # deal with dependencies correctly
            s = len(definitions)
            for k, v in definitions.copy().items():
                try:
                    self.tdata['colors'][k] = self.run_definition(v, raise_exception=True)
                    del definitions[k]
                except KeyError:
                    pass
            if s == len(definitions):
                logger.error('cyclic definition dependency detected: %r', definitions)
                break

    def run_definition(self, definition: DEF_VAL_TYPE, *, raise_exception: bool = False) -> Color:
        if callable(definition):
            return definition(self)
        if isinstance(definition, str):
            try:
                return self[definition]
            except KeyError:
                if raise_exception:
                    raise KeyError(definition) from None
        if isinstance(definition, Color):
            return definition
        logger.warning('definition failed: %r', definition)
        return Color((1, 0, 1))

    def apply_theme(self):  # qtile
        self.run_definitions()
        for screen in qtile.screens:
            for pos in ('top', 'bottom', 'left', 'right'):
                bar = getattr(screen, pos, None)
                if bar is not None:
                    self.apply_theme_to_bar(bar)
        for g in qtile.groups_map.values():
            self.apply_theme_to_group(g)
        self.apply_theme_to_element(qtile.config.floating_layout)
        # TODO: maybe flash a qtile popup to force systray icons to be redrawn?

    def apply_theme_to_bar(self, bar):
        self.apply_theme_to_element(bar)
        for widget in bar.widgets:
            self.apply_theme_to_element(widget)
        bar.draw()

    def apply_theme_to_group(self, group):
        for layout in group.layouts:
            self.apply_theme_to_element(layout)
        group.layout = group.layout.name  # trigger redraw.

    def apply_theme_to_element(self, element):
        # pylint: disable=protected-access
        if '_t_factory' not in element._user_config:
            return
        spec = element._user_config['_t_factory']
        if spec is None:
            return
        for prop, gen in spec.items():
            v = self.run_definition(gen).s
            if len(v) not in (6, 8):
                logger.error('malformed color for %r, %r: %r ~> %r', element, prop, gen, v)
                continue
            setattr(element, prop, v)
        if isinstance(element, widget.Systray):
            element.draw()


theme_factory = WalThemeFactory('dark/google')
theme_factory.update_definitions({  # light:
    'Active': lambda s: (s['orange']
                         .set_hsv_coord(min_v=0.8, max_s=0.5)
                         .contrast_enforce(s['Text.bold'], 0.5)),
    'Alert.bold': lambda s: s['b red'].set_hsv_coord(min_v=0.9, min_s=0.5),
    'Alert.dim': lambda s: s['b red'].set_hsv_coord(min_v=0.4, max_v=0.6),
    'Text.bold': lambda s: s['white'].set_hsv_coord(max_v=0.1),
    'Text.bold.i': lambda s: s['black'].set_hsv_coord(min_v=0.9, max_s=0.1),
    'Text.gray': lambda s: s['white'].set_hsv_coord(min_v=0.4, max_v=0.6),
    'Bar.bg': lambda s: s['background'].set_hsv_coord(min_v=0.9),
    'GroupBox.bg': lambda s: (c if ((c := s['blue'].set_hsv_coord(min_v=0.9, max_s=0.3))
                                    .h_dist(s['background']) > 0.1) else s['background']),
    'GroupBox.csb': 'Active',
    'GroupBox.sb': lambda s: s['Active'].set_hsv_coord(min_v=0.7, max_s=0.2),
    'Systray.bg': lambda s: s['gray'],
    'KBLayout.bg': 'Trailer.fg',
    'KBLayout.fg': 'Trailer.bg',
    'Trailer.fg': lambda s: s['white'].set_hsv_coord(v=1, max_s=0.1),
    'Trailer.bg_alt': lambda s: s['cyan'].set_hsv_coord(min_s=0.7, max_v=0.7),
    'Trailer.bg': lambda s: (s['Active'] if (s['Active'].h_dist(s['Trailer.bg_alt']) < 0.1
                                             and s['Active'].s_dist(s['Trailer.bg_alt']) < 0.1)
                             else s['Trailer.bg_alt']),
}, {  # dark:
    'Active': lambda s: (s['b cyan']
                         .set_hsv_coord(min_v=0.4, min_s=0.6)
                         .contrast_enforce(s['Text.bold'], 0.5)),
    'Alert.bold': lambda s: s['b red'].set_hsv_coord(min_v=0.9, min_s=0.5),
    'Alert.dim': lambda s: s['b red'].set_hsv_coord(v=0.4),
    'Text.bold': lambda s: s['white'].set_hsv_coord(v=1, max_s=0.1),
    'Text.bold.i': lambda s: s['black'].set_hsv_coord(max_v=0.1, max_s=0.1),
    'Text.gray': lambda s: s['white'].set_hsv_coord(max_v=0.6, max_s=0.1),
    'Bar.bg': lambda s: s['background'].set_hsv_coord(max_v=0.1),
    'GroupBox.bg': lambda s: (c if ((c := s['b blue'].set_hsv_coord(max_v=0.3))
                                    .h_dist(s['background']) > 0.1) else s['background']),
    'GroupBox.csb': 'Active',
    'GroupBox.sb': lambda s: s['Active'].set_hsv_coord(v=0.4, max_s=0.2),
    'Systray.bg': lambda s: s['dim gray'].set_hsv_coord(max_v=0.3),
    'KBLayout.bg': 'Trailer.fg',
    'KBLayout.fg': 'Trailer.bg',
    'Trailer.fg': lambda s: s['white'].set_hsv_coord(min_v=0.95),
    'Trailer.bg_alt': lambda s: s['b cyan'].set_hsv_coord(min_s=0.8, max_v=0.6),
    'Trailer.bg': lambda s: (s['Active'] if (s['Active'].h_dist(s['Trailer.bg_alt']) < 0.1
                                             and s['Active'].s_dist(s['Trailer.bg_alt']) < 0.1)
                             else s['Trailer.bg_alt']),
})
