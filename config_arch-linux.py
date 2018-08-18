from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook

from util import PwrLine

D_APPS = {
    'GUITERM':             'mate-terminal',
    'GUITERM-EXECARG':     '-x',
    'GUISUDO':             'lxsu',
    'GUIFILEMGR':          'pcmanfm',
    'GUIEDITOR':           'leafpad',
    'GUIBROWSER':          'firefox',
    'GUIBROWSER2':         'chromium',
    'FILEMGR':             'ranger',
    'EDITOR':              'vim',
    'BROWSER':             'lynx',
    'M1':                  'lyx',
    'M2':                  'blender',
    'M3':                  'gimp',
    'M4':                  'krita',
    'M0':                  'atom',
}
