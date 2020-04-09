import os
import re
import subprocess
from subprocess import run, getoutput, getstatusoutput
from importlib.util import spec_from_file_location, module_from_spec

from libqtile.log_utils import logger
from libqtile import widget

PWRLINE_DEFAULT_SIZE = 16  # NOTE: change that after importing util if necessary
_PWRLINECHARS = {
    'hortriangle': [u'\ue0b0', u'\ue0b2'],
    'horarrow':    [u'\ue0b1', u'\ue0b3'],
}


CHANGED_WITH_OFF = []
MIXER_SLOTS = [x[1:-1] for x in getoutput('amixer scontrols | egrep -o "\'.*\'"').split('\n')]


def get_state_alsa(mixer_slot='Master'):
    r = run(['amixer', 'get', mixer_slot],
            capture_output=True)
    lines = r.stdout[:-r.stdout.endswith(b'\n')].decode().split('\n')[1:]
    d = {}
    for line in lines:
        k, v = tuple(line.strip().split(':', 1))
        k = k.strip().lower()
        p = [x.strip() for x in v.split(' -'[' - ' in v]) if x.strip()]
        d[k] = p
    return d


def state_snapshot():
    d = {}
    for scont in MIXER_SLOTS:
        s = get_state_alsa(scont)
        if 'front right' in s or 'front left' in s:
            d[scont] = '[on]' in s.get('front right', []) or '[on]' in s.get('front left', [])
        else:
            d[scont] = '[on]' in s.get('mono', [])
    return d


def set_volume_alsa(qtile, level: str):
    global CHANGED_WITH_OFF
    special_mute = ['mute', 'unmute', 'toggle mute']
    setv = level not in special_mute
    if setv:
        if level[0] in '+-':
            level = level[1:].strip() + level[0]
        r = run(['amixer', 'set', 'Master', level],
                capture_output=True)
        if r.returncode:
            # print(r.stdout)
            # print(r.stderr)
            raise RuntimeWarning('ALSA set volume failed.')
    else:
        s_ind = special_mute.index(level.lower())
        r = run(['amixer', 'get', 'Master'],
                capture_output=True)
        ll = r.stdout[:-1].split(b'\n')[-1].decode()
        m = re.search(r'\[(on|off)\]', ll)
        s = ['[off]', '[on]'].index(m.group())
        # print('Currently on?', bool(s))
        if (level == 'mute' and not s) or (level == 'unmute' and s):
            return
        arg = ['off', 'on', ['on', 'off'][s]][s_ind]
        if arg == 'off':
            snap1 = state_snapshot()
        run(['amixer', 'sset', 'Master', arg])
        if arg == 'on':
            for x in CHANGED_WITH_OFF:
                run(['amixer', 'sset', x, 'on'])
        if arg == 'off':
            snap2 = state_snapshot()
            CHANGED_WITH_OFF = [k for k, v in snap1.items() if v == True and snap2[k] == False and k != 'Master']
        # print(r2.stdout)
    if hasattr(qtile.widgets_map.get('volume_indicator'), 'tick'):
        qtile.widgets_map.get('volume_indicator').tick()
    if arg == 'off':
        raise ValueError(CHANGED_WITH_OFF, snap1, snap2)


def PwrLine(left_color='#ffff00',
            right_color='#ff00ff', *,
            rtl=False,
            pwrtype='hortriangle',
            prefix='',
            suffix='',
            fontsize=PWRLINE_DEFAULT_SIZE,
            font='Source Code Pro Medium',
            **kwargs):
    '''Returns a libqtile.widget.TextBox with the correct powerline symbol'''
    assert isinstance(rtl, bool)
    char = _PWRLINECHARS.get(pwrtype, '??')[rtl]
    if rtl:
        fg = right_color
        bg = left_color
    else:
        fg = left_color
        bg = right_color
    return widget.TextBox(prefix+char+suffix, fontsize=fontsize, font=font,
                          foreground=fg, background=bg, margin=0, padding=0,
                          **kwargs)


def TermCmd(program, default_apps: dict):
    argprefix = default_apps.get('GUITERM-EXECARG')
    assert 'GUITERM' in default_apps
    if argprefix:
        return '%s %s %s' % (default_apps['GUITERM'], argprefix, program)
    return '%s %s' % (default_apps['GUITERM'], program)


### COLORS ####################################################################

def _crop(f):
    if f < 0:
        f = 0.0
    if f > 1:
        f = 1.0
    return '{:0>2x}'.format(int(round(255 * f)))


class colorscheme:
    '''color scheme provides a color storage and calculations'''
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


def on_startup():
    '''Run autoexec.sh on startup'''
    logger.error(os.path.expanduser('~/.config/qtile/autoexec.sh'))
    startupscript = os.path.expanduser('~/.config/qtile/autoexec.sh')
    subprocess.Popen([startupscript])
    # hook.fire('screen_change')


def import_from_file(file: str, module_name: str = 'mymodule'):
    '''Imports a module from a file'''
    assert os.path.isfile(file), '%r is not a file' % file
    spec = spec_from_file_location(module_name, file)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def xdotool_get_cursor_position():
    r, output = getstatusoutput('xdotool getmouselocation')
    if r:
        raise ValueError(f'xdotool exited with code {r}', output)
    m = re.fullmatch(r'x:(?P<x>\d+) y:(?P<y>\d+) screen:(?P<screen>\d+)'
                     r' window:(?P<window_id>\d+)', output.strip())
    if not m:
        raise ValueError(f'xdotool returned invalid data: {output!r}')
    d = m.groupdict()
    return int(d['x']), int(d['y'])


class PseudoRange:
    def __init__(self, start: int, stop: int, step: int = 1):
        self.start, self.stop, self.step = start, stop, step

    def __contains__(self, value: int):
        return (isinstance(value, int)
                and value >= self.start <= value < self.stop
                and (value - self.start) % self.step == 0)

    def __repr__(self):
        return f'range({self.start}, {self.stop}, {self.step})'


class MonitorDummy:
    def __init__(self, id_num: int, name: str, name_1: str,
                 width_px: int, height_px: int,
                 x_offset: int = 0, y_offset: int = 0,
                 width_phys: float = None, height_phys: float = None):
        self.name, self.name_1, self.id_num = name, name_1, id_num
        self.width_px, self.height_px = width_px, height_px
        self.width_phys, self.height_phys = width_phys, height_phys
        self.x_offset, self.y_offset = x_offset, y_offset

    @property
    def x_range(self):
        return PseudoRange(self.x_offset, self.x_offset + self.width_px)

    @property
    def y_range(self):
        return PseudoRange(self.y_offset, self.y_offset + self.height_px)

    def __contains__(self, location: tuple):
        x, y = location
        return x in self.x_range and y in self.y_range


class MonitorConfiguration:
    def __init__(self, *monitors):
        self.monitors = list(monitors)

    def __len__(self):
        return len(self.monitors)

    def get_monitor_from_position(self, position: tuple = None):
        if position is None:
            position = xdotool_get_cursor_position()
        x, y = position
        for m in self.monitors:
            if (x, y) in m:
                return m
        return None


def get_xrandr_monitor_data():
    line_re = (r'\s*(?P<id_num>\d+): (?:\+|.)(?P<name_1>.+) (?P<width_px>\d+)'
               r'/(?P<width_phys>\d+)x(?P<height_px>\d+)/(?P<height_phys>\d+)'
               r'\+(?P<x_offset>\d+)\+(?P<y_offset>\d+)\s+(?P<name>.+)')
    intify = {'id_num', 'width_px', 'height_px', 'x_offset', 'y_offset'}
    floatify = {'width_phys', 'height_phys'}
    r, output = getstatusoutput('xrandr --listactivemonitors')
    if r:
        raise ValueError(f'xrandr failed with code {r}', output)
    lines = list(map(str.strip, output.split('\n')))
    out = {}
    for l in lines:
        m = re.fullmatch(line_re, l)
        if not m:
            continue
        d = m.groupdict()
        for k in intify:
            d[k] = int(d[k])
        for k in floatify:
            d[k] = float(d[k])
        out[d['id_num']] = MonitorDummy(**d)
    return MonitorConfiguration(*out.values())
