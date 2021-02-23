#!/usr/bin/env python3

from libqtile.config import Click, Drag, Key, Match, ScratchPad, DropDown
from libqtile.lazy import lazy

from base_config import mod, mod_alt, HOME

ROFI_HOME = HOME + '/.config/qtile/rofi-scripts'
MACRO_HOME = HOME + '/.config/qtile/macro-scripts'


rofi_script_bindings = [
    Key([mod, 'shift'], 'w',
        lazy.spawn(ROFI_HOME + '/browser-select')),
    Key([mod], 'j',
        lazy.spawn(ROFI_HOME + '/jc-load')),
    Key([mod, 'shift'], 'j',
        lazy.spawn(ROFI_HOME + '/jc-save')),
    Key([mod], 'm',
        lazy.spawn(ROFI_HOME + '/mixer-select')),
    Key([mod], 'p',
        lazy.spawn(ROFI_HOME + '/screenlayouts'))
]

tool_bindings = [
    Key([mod], 'Print', lazy.spawn('lximage-qt --screenshot')),
    Key([mod, 'control', 'shift'], 'r',
        lazy.spawn(MACRO_HOME + '/macro_toggle_redshift.sh')),
    Key([mod, 'shift'], 'n',
        lazy.spawn('dunstctl set-paused toggle'),
        lazy.spawn('notify-send -u normal -i info '
                   '"toggled notification visibility"'),
        desc='Toggle the visibility of dunst notification popups'),
    Key([mod], 's',
        lazy.spawn(MACRO_HOME + '/macro_wacom_warp_focus.fish')),
]
