"""Configure the Qtile WM."""
import os
import subprocess

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal, logger

from base_config import (mod, terminal, dgroups_key_binder, dgroups_app_rules,
                         follow_mouse_focus, bring_front_click, cursor_warp,
                         auto_fullscreen, focus_on_window_activation, wmname,
                         group_chars, reconfigure_screens)
from scratchpad import scratchpad
from keys import keys

from layout import (layouts, screens, widget_defaults, extension_defaults,
                    floating_layout)

logger.setLevel(10)  # DEBUG

groups = [
    *[Group(i) for i in group_chars],
    scratchpad
]

for i in group_chars:
    if not i.isdigit():
        continue
    keys.extend([
        Key([mod, 'control'], i, lazy.group[i].toscreen(),
            desc=f'Switch to group {i}'),
        Key([mod, 'control', 'shift'], i,
            lazy.window.togroup(i, switch_group=False),
            desc=f'Move focused window to group {i}'),
    ])

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]


@hook.subscribe.startup_once
def on_startup():
    """Run autoexec.sh on startup"""
    startupscript = os.path.expanduser('~/.config/qtile/autoexec.fish')
    logger.info('Running {} once', startupscript)
    subprocess.Popen([startupscript],
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL)
