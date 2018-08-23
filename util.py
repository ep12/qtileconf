import os
import subprocess
from importlib.util import spec_from_file_location, module_from_spec

from libqtile import widget

PWRLINE_DEFAULT_SIZE = 16  # NOTE: change that after importing util if necessary
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
                font='Source Code Pro Medium'):
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
                          foreground=fg, background=bg, margin=0, padding=0)


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
            assert all(isinstance(x, tuple) and len(x) is 3
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
    startupscript = os.path.expanduser('~/.config/qtile/autoexec.sh')
    subprocess.call([startupscript])
    # hook.fire('screen_change')


def import_from_file(file: str, module_name: str = 'mymodule'):
    '''Imports a module from a file'''
    assert os.path.isfile(file), '%r is not a file' % file
    spec = spec_from_file_location(module_name, file)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
