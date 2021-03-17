#!/usr/bin/env python3

from libqtile.config import Click, Drag, Key, Match
from libqtile.lazy import lazy

from base_config import (mod, mod_alt, HOME, browser,
                         terminal, terminal_eflag)

from lazy_utils import tick_widget  # , prompt_and_run

from scratchpad import scratchpad_bindings  # dropdown etc.
from macro_scripts import rofi_script_bindings, tool_bindings
from launch_bindings import launch_bindings
from xournal_bindings import xournal_bindings, xournalpp_bindings

system_keys = [
    # Key([mod, 'control', 'shift'], 'F4',
    #     lazy.spawn('shutdown -h +1'),
    #     desc='Shutdown the computer'),
    # Key([mod, 'control', 'shift'], 'F5',
    #     lazy.spawn('reboot'),
    #     desc='Reboot the computer'),
    Key([mod], 'l',
        lazy.spawn('i3lock -c 000000')),
    Key([], 'XF86Sleep',
        lazy.spawn('i3lock -c 000000 -f'),
        lazy.spawn('systemctl suspend'),
        desc='Lock and suspend'),
    Key([mod], 'XF86Sleep',
        lazy.spawn('systemctl suspend'),
        desc='Suspend'),
]

qtile_keys = [
    # NOTE: Session
    Key([mod, 'control'], 'F5', lazy.restart(), desc='Restart qtile'),
    Key([mod, 'control'], 'F4', lazy.shutdown(), desc='Kill qtile'),
    # Key([mod], 'F1', lazy.spawn(TermCmd(
    #     'bash -c "cat %r; read -n 10 -rs -p \'Press any key to quit\'"' %
    #     (HOME + '/.config/qtile/keybindings.md'))),
    #     desc='Show keybindings'),

    # NOTE: Screen
    Key([mod], 'comma', lazy.next_screen(), desc='Focus next screen'),
    # Key([mod], 'period', lazy.prev_screen(), desc='Focus previous screen'),

    # NOTE: Workspace
    Key([mod, 'control'], 'Left', lazy.screen.prev_group()),
    Key([mod, 'control'], 'Right', lazy.screen.next_group()),

    # NOTE: Layout
    Key([mod_alt], 'Tab', lazy.group.next_window()),
    Key([mod_alt, 'shift'], 'Tab', lazy.group.prev_window()),
    Key([mod], 'Down', lazy.layout.down()),
    Key([mod], 'Up', lazy.layout.up()),
    Key([mod], 'Left', lazy.layout.left()),
    Key([mod], 'Right', lazy.layout.right()),
    Key([mod, 'control'], 'Down', lazy.layout.section_down().when('treetab')),
    Key([mod, 'control'], 'Up', lazy.layout.section_up().when('treetab')),
    #Key([mod, 'control'], 'Left', lazy.layout.move_left().when('treetab')),
    #Key([mod, 'control'], 'Right', lazy.layout.move_right().when('treetab')),
    Key([mod], 'less', lazy.layout.flip()),
    Key([mod, 'shift'], 'Down',
        lazy.layout.shuffle_down(),
        lazy.layout.move_down().when('treetab')),
    Key([mod, 'shift'], 'Up',
        lazy.layout.shuffle_up(),
        lazy.layout.move_up().when('treetab')),
    Key([mod, 'shift'], 'Left', lazy.layout.swap_left()),
    Key([mod, 'shift'], 'Right', lazy.layout.swap_right()),
    Key([mod, 'shift'], 'KP_Insert', lazy.layout.rotate()),
    Key([mod], 'plus', lazy.layout.grow()),
    Key([mod], 'minus', lazy.layout.shrink()),
    Key([mod], 'Return', lazy.layout.maximize()),
    Key([mod, 'shift'], 'Return', lazy.layout.normalize()),
    # Toggle between split and unsplit sides of stack:
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but with multiple panes
    # Key([mod, 'shift'], 'Return', lazy.layout.toggle_split()),
    Key([mod], 'Tab', lazy.next_layout()),
    Key([mod, 'shift'], 'Tab', lazy.prev_layout()),

    # NOTE: window
    Key([mod], 'F11', lazy.window.toggle_fullscreen()),
    Key([mod, 'shift'], 'F11', lazy.window.toggle_floating()),
    Key([mod], 'period', lazy.window.toggle_minimize()),  # .
    Key([mod], 'numbersign', lazy.window.toggle_maximize()),  # #
    Key([mod, 'control'], 'numbersign', lazy.group.unminimize_all()),
    # Key([mod], 'F4', lazy.window.kill()),
    Key([mod_alt], 'F4', lazy.window.kill()),

    # NOTE: fancy goto prompt:
    Key([mod], 'g', lazy.switchgroup(prompt='g')),
    Key([mod, 'shift'], 'g', lazy.togroup(prompt='g>'))
]

basic_launch_keys = [
    Key([mod], 't', lazy.spawn(terminal),
        desc='Launch your favourite terminal.'),
    Key([], 'XF86WWW', lazy.spawn(browser),
        desc='Launch your favourite web browser.'),
    Key([mod], 'r', lazy.spawncmd(prompt='$')),
    Key([mod, 'control'], 'r', lazy.spawn('rofi -show drun')),
    Key([], 'XF86Search', lazy.spawn('rofi -show drun')),

    Key([mod], 'F4', lazy.spawn('xkill')),

    Key([mod, 'control'], 'm',
        lazy.spawncmd(prompt='man ',
                      command=f'{terminal} {terminal_eflag} man %s')),
]

audio_keys = [
    # TODO: wrapper with playerctl
    Key([], 'XF86AudioPlay', lazy.spawn('mpc toggle')),
    Key([], 'XF86AudioNext', lazy.spawn('mpc next')),
    Key([], 'XF86AudioPrev', lazy.spawn('mpc prev')),

    Key([], 'XF86AudioRaiseVolume', lazy.spawn('mpc volume +1')),
    Key([], 'XF86AudioLowerVolume', lazy.spawn('mpc volume -1')),

    # 'XF86AudioMute'
    # 'XF86AudioMicMute'
]

backlight_keys = [
    Key(['control'], 'XF86MonBrightnessDown',
        lazy.spawn('light -U 1'),
        tick_widget('internal_brightness_indicator')),
    Key(['control'], 'XF86MonBrightnessUp',
        lazy.spawn('light -A 1'),
        tick_widget('internal_brightness_indicator')),
    Key([], 'XF86MonBrightnessDown',
        lazy.spawn('light -U 5'),
        tick_widget('internal_brightness_indicator')),
    Key([], 'XF86MonBrightnessUp',
        lazy.spawn('light -A 5'),
        tick_widget('internal_brightness_indicator')),
    Key([mod], 'XF86MonBrightnessDown',
        lazy.spawn('light -S 5'),
        tick_widget('internal_brightness_indicator')),
    Key([mod], 'XF86MonBrightnessUp',
        lazy.spawn('light -S 100'),
        tick_widget('internal_brightness_indicator')),
]


# NOTE: The final definition.
keys = [
    *system_keys,
    *qtile_keys,
    *basic_launch_keys,
    *audio_keys,
    *backlight_keys,
    # external:
    *scratchpad_bindings,
    *rofi_script_bindings,
    *tool_bindings,
    *launch_bindings,
    *xournal_bindings,
    *xournalpp_bindings,
]
