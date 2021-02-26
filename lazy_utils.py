#!/usr/bin/env python3
import re
import subprocess
from time import sleep
import typing as T
from libqtile.lazy import lazy
from libqtile.utils import logger


def prompt_and_run(prompt: str, callback: T.Callable, complete: str = None,
                   strict_completer: bool = False, widget: str = 'prompt'):
    """Prompt for input and call the callback function with the result."""
    @lazy.function
    def wrapped(qtile):
        qtile.widgets_map[widget].start_input(
            prompt=prompt, callback=callback(qtile),
            complete=complete, strict_completer=strict_completer)
    return wrapped


def tick_widget(widget_name: str, delay: float = 0.1):
    """Tick a widget if possible."""
    @lazy.function
    def wrapped(qtile):
        sleep(delay)
        if hasattr(qtile.widgets_map.get(widget_name), 'tick'):
            qtile.widgets_map.get(widget_name).tick()
    return wrapped


# class ChordModeFix:
#     def __init__(self):
#         self.qtile = None
#         self.stack = []

#     def enter_callback(self, chord):
#         logger.info('ChordModeFix: entering, %r', chord)
#         self.stack.append(chord)
#         logger.info('ChordModeFix: stack %r', self.stack)

#     def leave_callback(self):
#         logger.info('ChordModeFix: leaving')
#         self.stack.pop()
#         if self.stack[-1] != True:
#             logger.info('ChordModeFix: was %r', self.qtile.current_chord)
#             self.qtile.current_chord = self.stack[-1]
#             logger.info('ChordModeFix: is %r', self.qtile.current_chord)
#             self.qtile.widgets_map.get('chord_display').tick()
#         logger.info('ChordModeFix: stack %r', self.stack)

#     def get_qtile(self, qtile):
#         logger.info('ChordModeFix: %s', qtile)
#         self.qtile = qtile


class ProgramFilter:
    """Use this class to filter key/mouse callbacks by program properties."""
    def __init__(self, **kwargs):
        self.filter_dict = kwargs

    def __str__(self):
        return f'<ProgramFilter {self.filter_dict!r}>'

    def __repr__(self):
        return f'ProgramFilter (%s)' % ', '.join('%s=%r' % x for x in
                                                 self.filter_dict.items())

    def __call__(self, qtile):
        cw = qtile.current_window
        d = {'window_type': cw.window_type, **cw.info()}
        for k, v in self.filter_dict.items():
            if isinstance(v, tuple):
                v, default = v
            else:
                default = 'None'
            v2 = d.get(k, default)
            if isinstance(v, type(v2)) and v != v2:
                return False
            if callable(v) and not v(v2):
                return False
            if isinstance(v, re.Pattern) and not bool(v.fullmatch(v2)):
                return False
        return True


def match_prog(prog: ProgramFilter, func: T.Callable, *args, **kwargs):
    """
    Return lazy.function(func, *args, **kwargs) such that func is only
    executed if the currrently focussed program matches prog.
    """
    if not isinstance(prog, ProgramFilter):
        raise TypeError(f'prog must be of type ProgramFilter')

    def wrapper(qtile, *a, **kw):
        if not prog(qtile):
            return
        func(qtile, *a, **kw)
    return lazy.function(wrapper, *args, **kwargs)


def get_active_window(qtile=None):
    if qtile is not None:
        return qtile.current_window.window.wid
    return int(subprocess.check_output(['xdotool', 'getactivewindow']))


def send_key_xsk(qtile, key_combo):
    w = hex(get_active_window(qtile))
    logger.info('send_key_xsk: %s @ %s', key_combo, w)
    subprocess.run(['xsendkey', '-window', w, key_combo], check=True)


def send_key_xdt(qtile, key_combo):
    sleep(0.15)
    logger.info('send_key_xdt: %s', key_combo)
    subprocess.run(['xdotool', 'getactivewindow', 'key', key_combo],
                   check=True)
