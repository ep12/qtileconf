#!/usr/bin/env python3
import os
HOME = os.environ.get('HOME', os.path.expanduser('~'))

# this might be useful with lazy.something().when(layouts: set[str])
# import that in keys.py etc. if necessary, keep up to date with layouts.py
CONFIGURED_LAYOUTS = {
    'tile',
    'monadtall',
    'monadwide',
    # 'bsp',
    'matrix2',
    'matrix3',
    'treetab',
}

mod = 'mod4'
mod_alt = 'mod1'
terminal = 'termite'
terminal_eflag = '-e'
browser = 'firefox'  # non-standard

group_chars = '0123456789abcdef'  # non-standard

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
# main = None  # WARNING: this is deprecated and will be removed soon.
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

auto_fullscreen = True
focus_on_window_activation = "smart"

# Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
