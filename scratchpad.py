#!/usr/bin/env python3

from libqtile.config import Click, Drag, Key, Match, ScratchPad, DropDown
from libqtile.lazy import lazy

from base_config import mod, mod_alt, HOME

scratchpad = ScratchPad('scratchpad', [
    DropDown('files', 'pcmanfm',
             opacity=1, x=0, y=0, width=0.999, height=1),
    DropDown('term', 'termite',
             opacity=0.85, x=0.05, y=0.05, width=0.9, height=0.9),

    DropDown('htop', 'termite -e htop',
             opacity=0.8, x=0.05, y=0.05, width=0.9, height=0.9),
    DropDown('glances', 'termite -e glances',
             opacity=0.8, x=0.05, y=0.05, width=0.9, height=0.9),

    # DropDown('discord',
    #          'google-chrome-stable --app=https://www.discord.com/app',
    #          opacity=1, x=0, y=0, width=0.999, height=1),
    DropDown('skype', 'skypeforlinux',
             opacity=1, x=0, y=0, width=0.999, height=1),
    DropDown('zulip',
             'google-chrome-stable --app=https://physstgrp.zulipchat.com',
             opacity=1, x=0, y=0, width=0.999, height=1),

    DropDown('music', 'termite -e ncmpcpp',
             opacity=0.8, x=0.05, y=0.05, width=0.9, height=0.9),
    DropDown('pa-mixer', 'pavucontrol',
             opacity=1, x=0.02, y=0.02, width=0.96, height=0.96),
])

scratchpad_bindings = [
    Key([mod], 'f',
        lazy.group['scratchpad'].dropdown_toggle('files')),
    Key([mod], 'd',
        lazy.group['scratchpad'].dropdown_toggle('term')),

    Key([mod, 'shift'], 'Escape',
        lazy.group['scratchpad'].dropdown_toggle('htop')),
    Key([mod], 'Escape',
        lazy.group['scratchpad'].dropdown_toggle('glances')),

    Key([mod, 'shift'], 's',
        lazy.group['scratchpad'].dropdown_toggle('skype')),
    Key([mod, 'shift'], 'z',
        lazy.group['scratchpad'].dropdown_toggle('zulip')),

    Key([mod], 'XF86AudioPlay',
        lazy.group['scratchpad'].dropdown_toggle('music')),
    Key([mod, 'shift'], 'm',
        lazy.group['scratchpad'].dropdown_toggle('pa-mixer')),
]
