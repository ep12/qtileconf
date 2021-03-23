#!/usr/bin/env python3

from libqtile.config import Click, Drag, Key, Match, ScratchPad, DropDown
from libqtile.lazy import lazy

from base_config import mod, mod_alt, HOME, terminal, terminal_eflag


TCMD = f'{terminal} {terminal_eflag}'

scratchpad = ScratchPad('scratchpad', [
    DropDown('files', 'pcmanfm',
             opacity=1, x=0.025, y=0.025, width=0.95, height=0.95),
    DropDown('term', 'termite',
             opacity=0.85, x=0.05, y=0.05, width=0.9, height=0.9),

    DropDown('htop', f'{TCMD} stupid-test',  # TODO!
             opacity=0.8, x=0.05, y=0.05, width=0.9, height=0.9),
    DropDown('glances', f'{TCMD} glances',  # TODO!
             opacity=0.8, x=0.05, y=0.05, width=0.9, height=0.9),

    # DropDown('discord',
    #          'google-chrome-stable --app=https://www.discord.com/app',
    #          opacity=1, x=0, y=0, width=0.999, height=1),
    # DropDown('skype', 'skypeforlinux',
    #          opacity=1, x=0, y=0, width=0.999, height=1),
    DropDown('zulip',
             'google-chrome-stable --app=https://physstgrp.zulipchat.com',
             opacity=1, x=0, y=0, width=0.999, height=1),

    DropDown('music', f'{TCMD} ncmpcpp',  # TODO!
             opacity=0.8, x=0.05, y=0.05, width=0.9, height=0.9),
    DropDown('pa-mixer', 'pavucontrol',
             opacity=1, x=0.02, y=0.02, width=0.96, height=0.96),
])

scratchpad_bindings = [
    Key([mod], 'f',
        lazy.group['scratchpad'].dropdown_toggle('files')),
    Key([mod], 'd',
        lazy.group['scratchpad'].dropdown_toggle('term')),

    Key(['control', 'shift'], 'Escape',
        lazy.group['scratchpad'].dropdown_toggle('htop')),
    Key(['control'], 'Escape',
        lazy.group['scratchpad'].dropdown_toggle('glances')),

    # Key([mod, 'shift'], 's',
    #     lazy.group['scratchpad'].dropdown_toggle('skype')),
    Key([mod, 'shift'], 'z',
        lazy.group['scratchpad'].dropdown_toggle('zulip')),

    Key([mod], 'XF86AudioPlay',
        lazy.group['scratchpad'].dropdown_toggle('music')),
    Key([mod, 'shift'], 'm',
        lazy.group['scratchpad'].dropdown_toggle('pa-mixer')),
]
