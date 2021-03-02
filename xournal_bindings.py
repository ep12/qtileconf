#!/usr/bin/env python3

from libqtile import hook
from libqtile.config import Click, Drag, Key, KeyChord, Match
from libqtile.lazy import lazy

from base_config import mod, mod_alt, HOME
from macro_scripts import MACRO_HOME
from lazy_utils import (ProgramFilter, match_prog, send_key_xdt)

xournal_bindings = [
    KeyChord([mod, 'shift'], 'x', [
        # ...
    ], mode='xournal'),
]

xournalpp_bindings = [
    KeyChord([mod], 'x', [
        Key([mod], 's',
            lazy.spawn(MACRO_HOME + '/macro_wacom_warp_focus.fish')),
        KeyChord([], 't', [
            Key([], 't', lazy.function(send_key_xdt, 'Ctrl+Shift+P')),  # pen
            Key([], 'p', lazy.function(send_key_xdt, 'Ctrl+Shift+P')),  # pen
            Key([], 'e', lazy.function(send_key_xdt, 'Ctrl+Shift+E')),  # er..
            Key([], 'h', lazy.function(send_key_xdt, 'Ctrl+Shift+H')),  # high
            Key(['shift'], 't',
                lazy.ungrab_all_chords(),
                lazy.function(send_key_xdt, 'Ctrl+Shift+T')),  # text
            Key([], 'i',
                lazy.ungrab_all_chords(),
                lazy.function(send_key_xdt, 'Ctrl+Shift+I')),  # img
            Key([], 'x',
                lazy.ungrab_all_chords(),
                lazy.function(send_key_xdt, 'Ctrl+Shift+X')),  # TeX
        ]),
        KeyChord([], 's', [
            Key([], 's', lazy.function(send_key_xdt, 'Ctrl+Shift+G')),  # free
            Key([], 'b', lazy.function(send_key_xdt, 'Ctrl+Shift+R')),  # box
            Key([], 'o', lazy.function(send_key_xdt, 'Ctrl+Shift+O')),  # obj
            Key([], 'v', lazy.function(send_key_xdt, 'Ctrl+Shift+V')),  # vert
        ]),
        KeyChord([], 'r', [
            Key([], 's', lazy.function(send_key_xdt, 'Ctrl+1')),  # smart
            Key([], 'r', lazy.function(send_key_xdt, 'Ctrl+2')),  # rectangle
            Key([], 'c', lazy.function(send_key_xdt, 'Ctrl+3')),  # circle
            Key([], 'a', lazy.function(send_key_xdt, 'Ctrl+4')),  # arrow
            Key([], 'x', lazy.function(send_key_xdt, 'Ctrl+5')),  # axis
            Key([], 'l', lazy.function(send_key_xdt, 'Ctrl+6')),  # line
        ]),
        KeyChord([], 'p', [
            Key([], 'a', lazy.function(send_key_xdt, 'Ctrl+D')),  # page after
            Key(['control'], 'd',  # delete current page
                lazy.function(send_key_xdt, 'Ctrl+Delete')),
        ]),
        Key([], 'f', lazy.function(send_key_xdt, 'Ctrl+Shift+F')),
        Key(['control'], 'g', lazy.ungrab_chord()),
    ], mode='xournalpp'),
]
