#!/usr/bin/env python3

from libqtile import hook
from libqtile.config import Click, Drag, Key, KeyChord, Match
from libqtile.lazy import lazy

from base_config import mod, mod_alt, HOME

from lazy_utils import (ProgramFilter, match_prog, send_key_xdt)
#, ChordModeFix)

# chord_mode_fix = ChordModeFix()
# hook.subscribe.enter_chord(chord_mode_fix.enter_callback)
# hook.subscribe.leave_chord(chord_mode_fix.leave_callback)

xournal_bindings = []

xournalpp_bindings = [
    # Key([mod, 'shift'], 'x', lazy.function(chord_mode_fix.get_qtile)),
    KeyChord([mod], 'x', [
        KeyChord([], 't', [
            Key([], 'p',
                lazy.function(send_key_xdt, 'Control+Shift+P')),
            Key(['control'], 'g',
                lazy.function(lambda q: q.ungrab_chord())),
        ]),
        Key(['control'], 'g',
            lazy.function(lambda q: q.ungrab_chord())),
    ], mode='xournalpp'),
]
