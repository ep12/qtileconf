#!/usr/bin/env python3

from libqtile.config import Click, Drag, Key, Match
from libqtile.lazy import lazy

from base_config import mod, mod_alt, terminal, browser, HOME


cool_retro_term_base = 'cool-retro-term --fullscreen -e fish'

launch_bindings = [
    Key([mod, 'shift'], 'f', lazy.spawn('pcmanfm')),
    Key([mod, 'shift'], 't', lazy.spawn('alacritty')),
    Key([mod, 'control'], 't', lazy.spawn('xterm')),
    Key([mod, 'control', 'shift'], 't', lazy.spawn('urxvt')),

    Key([mod], 'w', lazy.spawn('firefox -P default')),
    Key([mod, 'control'], 'w', lazy.spawn('firefox -P work')),
    # mod+shift+w: rofi script: browser selection

    # Favourites:
    Key([mod], '0', lazy.spawn('okular')),
    Key([mod, 'shift'], '0', lazy.spawn('evince')),

    Key([mod], '1', lazy.spawn('lyx')),
    Key([mod, 'shift'], '1', lazy.spawn('typora')),

    Key([mod], '2', lazy.spawn('xournalpp')),
    Key([mod, 'shift'], '2', lazy.spawn('xournal')),

    Key([mod], '3', lazy.spawn('emacs')),
    Key([mod, 'shift'], '3', lazy.spawn('gedit')),

    Key([mod], '4', lazy.spawn('ardour6')),
    Key([mod, 'shift'], '4', lazy.spawn('audacity')),

    Key([mod], '5', lazy.spawn('blender')),
    Key([mod, 'shift'], '5', lazy.spawn('shotcut')),

    Key([mod], '6', lazy.spawn('olive-editor')),
    Key([mod, 'shift'], '6', lazy.spawn('/opt/resolve/bin/resolve')),

    Key([mod], '7', lazy.spawn('gimp')),
    Key([mod, 'shift'], '7', lazy.spawn('krita')),

    Key([mod], '8', lazy.spawn('darktable')),
    Key([mod, 'shift'], '8',
        lazy.spawn('google-chrome-stable --app=https://photos.google.com/')),

    Key([mod], '9',
        lazy.spawn(f'{cool_retro_term_base} --profile Vintage')),
    Key([mod, 'shift'], '9',
        lazy.spawn(f'{cool_retro_term_base} --profile Futuristic')),
]
