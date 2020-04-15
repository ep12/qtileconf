import os
from os import path
import subprocess
import re

from libqtile.config import Key, Screen, Group, Drag
try:
    from libqtile.lazy import lazy
except ImportError:
    from libqtile.command import lazy
from libqtile import layout, bar, widget, hook, pangocffi, utils
# from libqtile.log_utils import logger

# TODO:
# Temperature Graph
# from libqtile.widget.graph import _Graph

from util import colorscheme, PwrLine, TermCmd as _TermCmd, on_startup, import_from_file, get_state_alsa

# try:
#     from typing import List  # noqa: F401
# except ImportError:
#     pass

# hook.subscribe.startup(on_startup)
# hook.subscribe.startup_complete(on_startup)
hook.subscribe.startup_once(on_startup)  # not fired after restart
hook.subscribe.screen_change(lambda qtile, anotherarg: qtile.cmd_restart())
# hook.subscribe.client_new


class ModifiedKeyboardLayout(widget.KeyboardLayout):
    variant_shorts = {
        'NODEADKEYS': 'NDK',
        'DVORAK': 'DVO',
    }
    def poll(self):
        kbd = self.keyboard.upper()
        if ' ' in kbd:
            layout, variant = kbd.split(' ', 1)
            variant = variant.strip()
            kbds = [x.upper() for x in self.configured_keyboards]
            count = sum(x.split(' ', 1)[0] == layout for x in kbds)
            if count < 2:
                return layout
            elif variant in self.variant_shorts:
                return '%s\n%s' % (layout, self.variant_shorts[variant])
            else:
                return kbd
        return kbd


class ModifiedNotify(widget.Notify):
    def set_notif_text(self, notif):
        self.text = pangocffi.markup_escape_text(notif.summary)
        # logger.error('Notification: %r' % self.text)
        # logger.error(repr(notif))
        # if hasattr(notif, '__dict__'):
        #     logger.error(repr(notif.__dict__))
        urgency = notif.hints.get('urgency', 1)
        if urgency != 1:
            self.text = '<span color="%s">%s</span>' % (
                utils.hex(
                    self.foreground_urgent if urgency == 2
                    else self.foreground_low
                ),
                self.text
            )
        if notif.body:
            self.text = '<span weight="bold">%s</span>\n%s' % (
                self.text.replace('\n', ' '),
                pangocffi.markup_escape_text(notif.body.replace('\n', ' '))
            )
        if self.audiofile:
            if isinstance(self.audiofile, dict):
                afp = self.audiofile.get(urgency, '')
            else:
                afp = self.audiofile
            if afp and isinstance(afp, str) and path.exists(afp):
                self.qtile.cmd_spawn("aplay -q '%s'" % afp)

    def real_update(self, notif):
        self.set_notif_text(notif)
        self.current_id = notif.id - 1
        if notif.timeout and notif.timeout > 0:
            self.timeout_add(notif.timeout / 1000, self.clear)
        elif self.default_timeout:
            if isinstance(self.default_timeout, dict):
                v = self.default_timeout.get(notif.hints.get('urgency', 1), 0)
                if v:
                    self.timeout_add(v, self.clear)
            else:
                self.timeout_add(self.default_timeout, self.clear)
        self.bar.draw()
        return True


class reg_match:
    def __init__(self, rexp):
        if isinstance(rexp, str):
            self.compiled = re.compile(rexp)
        elif isinstance(rexp, re.Pattern):
            self.compiled = rexp
        else:
            raise ValueError('Must be str or compiled regex')

    def __eq__(self, other):
        if not isinstance(other, str):
            return False
        return bool(self.compiled.fullmatch(other))

    def __le__(self, other):
        if not isinstance(other, str):
            return False
        return bool(self.compiled.match(other))

    def __lt__(self, other):
        return self.__le__(other) and not self.__eq__(other)


def TermCmd(program):
    '''Wrapper for TermCmd (util module)'''
    return _TermCmd(program, D_APPS)


def get_brightness(*args, **kwargs):
    r = subprocess.run(['xbacklight', '-get'], capture_output=True)
    s = r.stdout.decode()[:-1]
    try:
        p = str(int(round(float(s))))
    except Exception:
        p = re.search(r'^(\d+)', s)
        if hasattr(p, 'group') and p.group(0):
            p = p.group(0)
        else:
            p = '?'
    return '<b>☼</b>%s' % p


def get_volume_pulse(*args, **kwargs):
    r = subprocess.run(['pacmd', 'list-sinks'], capture_output=True)
    s = r.stdout.decode()[:-1]
    m = re.findall(r'\* *index: (\d+)', s)
    if m and len(m) == 1:
        m = re.search(r'\* *index: (\d+)', s).span()[0] + 7
        print(m)
        if 'index' in s[m]:
            s = s[m:s[m].index('index')]
        else:
            s = s[m:]
    else:
        return '🔈?'
    m = re.search(r'muted:\s*?(no|yes)', s)
    if bool(m) and ['no', 'yes'].index(m.groups()[0]):
        return '🔇'
    r = subprocess.run(['pamixer', '--get-volume'], capture_output=True)
    s = r.stdout.decode()[:-1]
    if bool(re.fullmatch(r'\d+', s)):
        return '🔈' + s
    else:
        return '🔈?'


def get_volume_alsa(*args, **kwargs):
    tmp, s = '🔈', ''
    state = get_state_alsa()
    channels = state['playback channels']
    if len(channels) == 1:
        k = channels[0].lower()
        ch_state = state[k]
        if '[on]' in ch_state and '[off]' in ch_state:
            s = '?'
        elif '[off]' in ch_state:
            tmp = '🔇'
        else:
            for x in ch_state:
                m = re.fullmatch(r'\[(100|\d{2})%\]', x)
                if bool(m):
                    s = m.groups()[0]
                    break
                else:
                    s = '?'
    return tmp + s


hostname = os.uname()[1]
HOME = os.environ.get('HOME', os.path.expanduser('~'))
folder = os.path.dirname(os.path.realpath(__file__))
_special_config = '%s/config_%s.py' % (folder, hostname)
if os.path.isfile(_special_config):
    scfg = import_from_file(_special_config).__dict__
else:
    print('You can add a machine-specific config here:\n%r' % _special_config)
    scfg = {}


mod = scfg.get('mod', 'mod4')
mod_alt = scfg.get('mod_alt', 'mod1')


N_FONTSIZE_SMALL = 10
N_FONTSIZE = 12
N_BAR_HEIGHT = scfg.get('N_BAR_HEIGHT',      28  )
N_BORDER_WIDTH = scfg.get('N_BORDER_WIDTH',   1  )
N_PWRL_BRIGHT = scfg.get('N_PWRL_BRIGHT',     0.2)
N_GRAPH_WIDTH = scfg.get('N_GRAPH_WIDTH',    35  )
N_GRAPH_FILL = scfg.get('N_GRAPH_FILL',       1.0)
N_GRAPH_BORDER = scfg.get('N_GRAPH_BORDER',   0.2)
N_EXTRA_DISPLAYS = scfg.get('N_EXTRA_DISPLAYS', 9)

D_APPS = scfg.get('D_APPS', {  # Default apps, overwrite them all!
    'GUITERM':             'mate-terminal',
    'GUISUDO':             'lxsu',
    'GUIFILEMGR':          'pcmanfm',
    'GUIEDITOR':           'leafpad',
    'GUIBROWSER':          'firefox',
    'GUIBROWSER2':         'chromium',
    'FILEMGR':             'ranger',
    'EDITOR':              'vim',
    'BROWSER':             'lynx',
})

colors = {
    'red':                 (1.000, 0.000, 0.000), # ff0000
    'orange':              (1.000, 0.600, 0.000), # ff9900
    'theme_orange':        (1.000, 0.325, 0.102), # ff531a
    'yellow':              (1.000, 1.000, 0.000), # ffff00
    'lime':                (0.500, 1.000, 0.000), # 8fff00
    'green':               (0.000, 1.000, 0.000), # 00ff00
    'cyan':                (0.000, 0.500, 1.000), # 008fff
    'greenblue':           (0.000, 1.000, 1.000), # 00ffff
    'lightblue':           (0.000, 0.500, 1.000), # 008fff
    'blue':                (0.000, 0.000, 1.000), # 0000ff
    'purple':              (0.500, 0.000, 1.000), # 8f00ff
    'pink':                (1.000, 0.000, 1.000), # ff00ff

    'white':               (1.000, 1.000, 1.000), # ffffff
    'neutral':             (1.000, 1.000, 1.000), # ffffff
    'black':               (0.000, 0.000, 0.000), # 000000

    'active':              (0.000, 0.750, 1.000), # 00bfff
    'inactive':            (0.000, 0.000, 0.000), # 000000
    'barbackground':       (0.050, 0.050, 0.050), # 0d0d0d

    'CPU_G':               (1.000, 0.000, 0.000), # ff0000
    'RAM_G':               (0.000, 1.000, 0.000), # 00ff00
    'SWAP_G':              (1.000, 0.200, 1.000), # ff33ff
    'HDD_G':               (1.000, 0.600, 0.000), # ff9900
    'NET_G':               (0.000, 0.750, 1.000), # 00bfff
}
colors.update(scfg.get('colorscheme', {}))
colors = colorscheme(colors)

D_WINDOW_SETTINGS = {
    'border_focus':        colors('active'),
    'border_normal':       colors('inactive'),
    'border_width':        N_BORDER_WIDTH,
}
D_WINDOW_SETTINGS.update(scfg.get('D_WINDOW_SETTINGS', {}))

graphbar = [
    # widget.TextBox('C', foreground=colors('CPU_G'), background=colors('CPU_G', N_PWRL_BRIGHT)),
    widget.CPUGraph(
        width=N_GRAPH_WIDTH,
        line_width=1,
        border_width=1,
        border_color=colors('CPU_G', N_GRAPH_BORDER),
        background=colors('CPU_G', N_PWRL_BRIGHT),
        graph_color=colors('CPU_G'),
        fill_color=colors('CPU_G', N_GRAPH_FILL),
    ),
    PwrLine(colors('CPU_G', N_PWRL_BRIGHT),
            colors('RAM_G', N_PWRL_BRIGHT),
            rtl=True,
            fontsize=N_BAR_HEIGHT),
    # widget.TextBox('R', foreground=colors('RAM_G'), background=colors('RAM_G', N_PWRL_BRIGHT)),
    widget.MemoryGraph(
        width=N_GRAPH_WIDTH,
        line_width=1,
        border_width=1,
        border_color=colors('RAM_G', N_GRAPH_BORDER),
        background=colors('RAM_G', N_PWRL_BRIGHT),
        graph_color=colors('RAM_G'),
        fill_color=colors('RAM_G', N_GRAPH_FILL),
    ),
    PwrLine(colors('RAM_G', N_PWRL_BRIGHT),
            colors('SWAP_G', N_PWRL_BRIGHT),
            rtl=True,
            fontsize=N_BAR_HEIGHT),
    # widget.TextBox('S', foreground=colors('SWAP_G'), background=colors('SWAP_G', N_PWRL_BRIGHT)),
    # widget.SwapGraph(
    #     width=N_GRAPH_WIDTH,
    #     line_width=1,
    #     border_width=1,
    #     border_color=colors('SWAP_G', N_GRAPH_BORDER),
    #     background=colors('SWAP_G', N_PWRL_BRIGHT),
    #     graph_color=colors('SWAP_G'),
    #     fill_color=colors('SWAP_G', N_GRAPH_FILL),
    # ),
    widget.ThermalSensor(
        background=colors('SWAP_G', N_GRAPH_BORDER),
        foreground=colors('SWAP_G'),
        foreground_alert=colors('CPU_G'),
        metric=True,
        tag_sensor='Package id 0',
        threshold=70,
        update_interval=5
    ),
    PwrLine(colors('SWAP_G', N_PWRL_BRIGHT),
            colors('HDD_G', N_PWRL_BRIGHT),
            rtl=True,
            fontsize=N_BAR_HEIGHT),
    # widget.TextBox('H', foreground=colors('HDD_G'), background=colors('HDD_G', N_PWRL_BRIGHT)),
    widget.HDDBusyGraph(
        device='sda',
        width=N_GRAPH_WIDTH,
        line_width=1,
        border_width=1,
        border_color=colors('HDD_G', N_GRAPH_BORDER),
        background=colors('HDD_G', N_PWRL_BRIGHT),
        graph_color=colors('HDD_G'),
        fill_color=colors('HDD_G', N_GRAPH_FILL),
    ),
    PwrLine(colors('HDD_G', N_PWRL_BRIGHT),
            colors('NET_G', N_PWRL_BRIGHT),
            rtl=True,
            fontsize=N_BAR_HEIGHT),
    # widget.TextBox('N', foreground=colors('NET_G'), background=colors('NET_G', N_PWRL_BRIGHT)),
    widget.NetGraph(
        interface='wlo1',
        bandwidth_type='up',
        line_width=1,
        width=N_GRAPH_WIDTH,
        border_width=1,
        border_color=colors('NET_G', N_GRAPH_BORDER),
        background=colors('NET_G', N_PWRL_BRIGHT),
        graph_color=colors('NET_G'),
        fill_color=colors('NET_G', N_GRAPH_FILL),
    ),
    widget.NetGraph(
        interface='wlo1',
        bandwidth_type='down',
        line_width=1,
        width=N_GRAPH_WIDTH,
        border_width=1,
        border_color=colors('NET_G', N_GRAPH_BORDER),
        background=colors('NET_G', N_PWRL_BRIGHT),
        graph_color=colors('NET_G'),
        fill_color=colors('NET_G', N_GRAPH_FILL),
    ),
]

keys = [
    # NOTE:
    # better control: layout dependant keys:
    # Key([mod], 'A',
    #     lazy.spawn('some_command').when(layout='floating'))
    # Key([mod], 'A',
    #     lazy.spawn('some_command').when(layout=layout.Max))
    # NOTE:
    # libqtile/command.py:def check(self, q):
    # possible simplification:
    #   return q.currentWindow.floating
    # NOTE: system
    Key([mod, 'control', 'shift'], 'F4',
        lazy.spawn('shutdown -h +1')),
    Key([mod, 'control', 'shift'], 'F5',
        lazy.spawn('reboot')),

    # NOTE: qtile
    Key([mod, 'control'], 'F5', lazy.restart()),
    Key([mod, 'control'], 'F4', lazy.shutdown()),
    Key([mod], 'F1', lazy.spawn(TermCmd(
        'bash -c "cat %r; read -n 10 -rs -p \'Press any key to quit\'"' %
        (HOME + '/.config/qtile/keybindings.md')))),

    # NOTE: Workspace
    Key([mod, 'control'], 'Left', lazy.screen.prev_group()),
    Key([mod, 'control'], 'Right', lazy.screen.next_group()),

    # NOTE: Layout
    Key([mod_alt], 'Tab', lazy.layout.next()),
    Key([mod_alt, 'shift'], 'Tab', lazy.layout.previous()),
    Key([mod], 'Down', lazy.layout.down()),
    Key([mod], 'Up', lazy.layout.up()),
    Key([mod], 'Left', lazy.layout.left()),
    Key([mod], 'Right', lazy.layout.right()),
    Key([mod, 'control'], 'Down', lazy.layout.section_down().when('treetab')),
    Key([mod, 'control'], 'Up', lazy.layout.section_up().when('treetab')),
    #Key([mod, 'control'], 'Left', lazy.layout.move_left().when('treetab')),
    #Key([mod, 'control'], 'Right', lazy.layout.move_right().when('treetab')),
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
    # Toggle between split and unsplit sides of stack: Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with multiple stack panes
    # Key([mod, 'shift'], 'Return', lazy.layout.toggle_split()),
    Key([mod], 'Tab', lazy.next_layout()),
    #Key([mod, 'shift'], 'Tab', lazy.previous_layout()),

    # NOTE: window
    Key([mod], 'F11', lazy.window.toggle_fullscreen()),
    Key([mod, 'shift'], 'F11', lazy.window.toggle_floating()),
    # Key([mod], 'F4', lazy.window.kill()),
    Key([mod_alt], 'F4', lazy.window.kill()),

    # NOTE: launch
    Key([mod], 't',
        lazy.spawn(D_APPS['GUITERM'])),
    Key(['control', 'shift'], 'Escape',
        lazy.spawn(TermCmd('htop'))),
    Key([mod, 'control', 'shift'], 'Escape',
        lazy.spawn(TermCmd('sudo htop'))),
    Key([mod], 'f',
        lazy.spawn(D_APPS['GUIFILEMGR'])),
    Key([mod, 'shift'], 'f',
        lazy.spawn('%s %s' % (D_APPS['GUISUDO'], D_APPS['GUIFILEMGR']))),
    Key([mod, 'control'], 'f',
        lazy.spawn(TermCmd(D_APPS['FILEMGR']))),
    Key([mod, 'control', 'shift'], 'f',
        lazy.spawn(TermCmd('sudo %s' % D_APPS['FILEMGR']))),
    Key([], 'XF86WWW',
        lazy.spawn(D_APPS['GUIBROWSER'])),
    Key(['shift'], 'XF86WWW',
        lazy.spawn(D_APPS['GUIBROWSER2'])),
    Key(['control'], 'XF86WWW',
        lazy.spawn(TermCmd(D_APPS['BROWSER']))),
    Key([mod], 'w',
        lazy.spawn('firefox -P default')),
    Key([mod, 'shift'], 'w',
        lazy.spawn(D_APPS['GUIBROWSER2'])),
    Key([mod, 'control'], 'w',
        lazy.spawn('firefox -P Work')),

    # NOTE: prompt
    Key([mod], 'e',
        lazy.spawncmd(prompt=u'$\U0001F589',
                      complete='file',
                      command='{} -x {} %s'.format(D_APPS['GUITERM'], D_APPS['EDITOR']))),
    Key([mod, 'shift'], 'e',
        lazy.spawncmd(prompt=u'#\U0001F589',
                      complete='file',
                      command='{} {} -x {} %s'.format(
                          D_APPS['GUISUDO'], D_APPS['GUITERM'], D_APPS['EDITOR']))),
    Key([mod, 'control'], 'e',
        lazy.spawncmd(prompt=u'\U0001F589',
                      complete='file',
                      command='{} %s'.format(D_APPS['GUIEDITOR']))),
    Key([mod, 'control', 'shift'], 'e',
        lazy.spawncmd(prompt=u'\u26a1\U0001F589',
                      complete='file',
                      command='{} {} %s'.format(
                          D_APPS['GUISUDO'], D_APPS['GUIEDITOR']))),
    Key([mod, 'control'], 'm',
        lazy.spawncmd(prompt=u'man ',
                      command='{} -e man %s'.format(D_APPS['GUITERM']))),
    Key([mod], 'r',
        lazy.spawncmd(prompt='$')),
    Key([mod, 'shift'], 'r',
        lazy.spawncmd(prompt='#',
                      command='{} %s'.format(D_APPS['GUISUDO']))),
    Key([mod, 'control'], 'r',
        lazy.spawn('rofi -show drun')),
    Key([mod], 'l',
        lazy.spawn('i3lock -c 000000')),
    # TODO: LOCKER :TODO XXX
]

for mods in ['M', 'MS']:
    modl = [mod]
    if 'C' in mods:
        modl.append('control')
    if 'S' in mods:
        modl.append('shift')
    for n in '1234567890':
        if mods + n in D_APPS:
            keys.append(Key(modl, n, lazy.spawn(D_APPS[mods + n])))

groups = [Group(i) for i in '0123456789abcdef']
for i in groups:
    if not i.name in '12345567890':
        continue
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod, 'control'], i.name, lazy.group[i.name].toscreen()),
        # mod1 + control + letter of group = switch to & move focused window to group
        Key([mod, 'control', 'shift'], i.name, lazy.window.togroup(i.name)),
    ])

layouts = scfg.get('layouts', [
    layout.MonadTall(
        ratio=0.5,
        min_ratio=0.01,
        max_ratio=0.99,
        change_ratio=0.02,
        change_size=10,
        **D_WINDOW_SETTINGS
    ),
    layout.MonadWide(
        ratio=0.5,
        min_ratio=0.01,
        max_ratio=0.99,
        change_ratio=0.02,
        change_size=10,
        **D_WINDOW_SETTINGS
    ),
    layout.Matrix(
        columns=2,
        margin=0,
        **D_WINDOW_SETTINGS
    ),
    layout.Matrix(
        columns=3,
        margin=0,
        **D_WINDOW_SETTINGS
    ),
    # layout.Max(**D_WINDOW_SETTINGS),
    layout.TreeTab(
        active_bg=colors('active'),
        active_fg=colors('barbackground'),
        inactive_bg=colors('barbackground'),
        inactive_fg=colors('white'),
        section_fg=colors('active'),
        bg_color=colors('barbackground'),
        section_fontsize=N_FONTSIZE,
        fontsize=N_FONTSIZE,
        # font
        level_shift=4,
        margin_left=4,
        margin_y=4,
        padding_left=4,
        padding_x=4,
        padding_y=2,
        panel_width=250,
        previous_on_rm=True,
        section_bottom=4,
        section_left=4,
        section_padding=4,
        section_top=4,
        section=['Default'],
        vpace=2,
        **D_WINDOW_SETTINGS
    ),
])

if 'keys' in scfg and isinstance(scfg['keys'], list):
    keys.extend(scfg['keys'])

widget_defaults = {
    'font':'Ubuntu Sans Bold',
    'fontsize': N_FONTSIZE,
    'padding': 4,
}
widget_defaults.update(scfg.get('widget_defaults', {}))
extension_defaults = scfg.get('extension_defaults', widget_defaults.copy())

screens = scfg.get('screens', [
    Screen(
        bottom=bar.Bar([
            widget.GroupBox(
                name='main_group_box',
                background=colors('active', N_PWRL_BRIGHT),
                active=colors('white'),
                inactive=colors('white', 0.25),
                highlight_method='block',
                rounded=False,
                this_current_screen_border=colors('active'),               # this screen's group, focussed
                this_screen_border=colors('active', 0.5),                  # this screen's group, not focussed
                other_current_screen_border=colors('theme_orange', 0.75),  # other screen, focussed
                other_screen_border=colors('theme_orange', 0.5),           # other screen, not focussed
                borderwidth=1,
                urgent_method='block',
                urgent_text=colors('red', 0.8),
                urgent_border=colors('red', 0.8),
                margin=0,
                padding=6,
            ),
            widget.Prompt(
                cursor_color=colors('white'),
                background=colors('active', N_PWRL_BRIGHT),
                foreground=colors('active'),
                bell_style='audible',
                prompt=' {prompt} ',
            ),
            PwrLine(colors('NET_G', N_PWRL_BRIGHT), None,
                           suffix=' '*0, fontsize=N_BAR_HEIGHT),
            widget.TaskList(
                name='internal_monitor_tasklist',
                # font='Ubuntu Bold',
                border=colors('active', 0.8),
                urgend_border=colors('red', 0.8),
                highlight_method='block',
                urgent_method='block',
                border_width=1,
                rounded=False,
                max_title_width=500,
                icon_size=16,
                txt_minimized='\U0001F5D5 ',  # [_] \U0001F5D5
                txt_maximized='\U0001F5D6 ',  # [M] \U0001F5D6
                txt_floating='\U0001F5D7 ',   # [F] \U0001F5D7
                margin=0,
                padding=6.5,
            ),
            PwrLine(None, colors('neutral', N_PWRL_BRIGHT),
                    rtl=True, prefix=' '*0, fontsize=N_BAR_HEIGHT),
            widget.Systray(background=colors('neutral', N_PWRL_BRIGHT)),
            PwrLine(colors('neutral', N_PWRL_BRIGHT), colors('CPU_G', N_PWRL_BRIGHT),
                    rtl=True, fontsize=N_BAR_HEIGHT),
            widget.DF(
                name='diskfree_root',
                background=colors('CPU_G', N_PWRL_BRIGHT),
                update_interval=3600,
                warn_space=5,
                partition='/'
            ),
            widget.DF(
                name='diskfree_home',
                background=colors('CPU_G', N_PWRL_BRIGHT),
                update_interval=3600,
                warn_space=10,
                partition='/home'
            ),
            *graphbar,
            PwrLine(colors('NET_G', N_PWRL_BRIGHT), colors('white'),
                    rtl=True, fontsize=N_BAR_HEIGHT),
            ModifiedNotify(
                default_timeout={
                    0: 15,  # low
                    1: 30,  # normal
                    2: 0,  # critical
                }, # s
                audiofile={
                    0: None,
                    1: None,
                    2: HOME + '/Documents/Multimedia/typewriter_bell.wav'
                },
                background=colors('white'),
                foreground=colors('black'),
                foreground_low=colors('black'),
                foreground_urgent=colors('red'),
                markup=True,
                fontsize=N_FONTSIZE_SMALL,
            ),
            # widget.CheckUpdates(
            #     distro='Arch',
            #     update_interval=60*15,
            #     colour_have_updates=colors('red'),
            #     colour_no_updates=colors('barbackground'),
            #     # display_format=u'\u27f3 {updates}',
            #     display_format=u'\u2b6e {updates}',
            #     execute='%s %s' % (D_APPS['GUISUDO'], 'pacman -Syu --noconfirm'),
            #     background=colors('white'),
            # ),
            ModifiedKeyboardLayout(
                update_interval=30,
                markup=False,
                fontsize=N_FONTSIZE_SMALL,
                configured_keyboards=[
                                      'de nodeadkeys',
                                      'de dvorak',
                                      'us',
                                      'us dvorak'
                                      ],
                foreground=colors('active'),
                background=colors('white'),
            ),
            # widget.BatteryIcon(
            #     theme_path=HOME+'/.config/qtile/battery-icons',
            #     background=colors('neutral', N_PWRL_BRIGHT),
            # ),
            # widget.DebugInfo(background=colors('neutral', N_PWRL_BRIGHT)),
            # widget.Wlan(
            #     interface='wlo1',
            #     update_interval=3,
            #     format='{essid}: {percent:3.0%}',
            #     disconnected_message='not connected'
            # ),
            PwrLine(colors('white'), colors('active'), rtl=True, fontsize=N_BAR_HEIGHT),
            widget.GenPollText(
                name='internal_brightness_indicator',
                func=get_brightness,
                background=colors('active'),
                foreground=colors('yellow'),
                update_interval=3600,
                markup=True,
            ),
            widget.GenPollText(
                name='volume_indicator',
                func=get_volume_alsa,
                background=colors('active'),
                foreground=colors('white'),
                update_interval=3600,
                markup=True,
            ),
            widget.Battery(
                background=colors('active'),
                foreground=colors('white'),
                charge_char='↑',
                discharge_char='↓',
                error_message='⚠',
                hide_threshold=None,
                low_percentage=0.15,
                markup=True,
                fontsize=N_FONTSIZE_SMALL,
                # format=u'\u2393{char}{percent:2.0%} {hour:d}:{min:02d}',
                # format='<u>{char}{percent:2.0%}\n{hour:d}:{min:02d}</u>',
                format='<b>{char}{percent:2.0%}\n{hour:d}:{min:02d}</b>',
                # battery='BAT0',
                #energy_now_file='charge_now',
                #energy_full_file='charge_full',
                #power_now_file='current_now',
                update_delay=30,
            ),
            widget.CurrentLayoutIcon(
                background=colors('active'),
                foreground=colors('white'),
                scale=0.7
            ),
            widget.Clock(
                format='%Y/%m/%d\n<b>%2H:%2M:%2S</b>',
                foreground=colors('white'),
                background=colors('active'),
                markup=True,
                fontsize=N_FONTSIZE_SMALL,
            ),
        ], N_BAR_HEIGHT, background=colors('barbackground')),
    )
])

for i in range(1, N_EXTRA_DISPLAYS + 1):
    screens.append(
    Screen(
        bottom=bar.Bar([
            widget.TextBox(
                text=' %d' % i,
                background=colors('white'),
                foreground=colors('black'),
                name='monitor_id_%i_left' % i,
            ),
            PwrLine(colors('white'),
                    None,  # colors('active', N_PWRL_BRIGHT),
                    suffix=' '*0, fontsize=N_BAR_HEIGHT),
            # widget.GroupBox(
            #     background=colors('active', N_PWRL_BRIGHT),
            #     active=colors('white'),
            #     inactive=colors('white', 0.25),
            #     highlight_method='block',
            #     rounded=False,
            #     this_current_screen_border=colors('active'),               # this screen's group, focussed
            #     this_screen_border=colors('active', 0.5),                  # this screen's group, not focussed
            #     other_current_screen_border=colors('theme_orange', 0.75),  # other screen, focussed
            #     other_screen_border=colors('theme_orange', 0.5),           # other screen, not focussed
            #     borderwidth=1,
            #     urgent_method='block',
            #     urgent_text=colors('red', 0.8),
            #     urgent_border=colors('red', 0.8),
            #     margin=0,
            #     padding=6,
            # ),
            widget.WindowName(
                background=None,  # colors('active', N_PWRL_BRIGHT),
                padding=6,
            ),
            # PwrLine(colors('active', N_PWRL_BRIGHT), None,
            #                suffix=' '*0, fontsize=N_BAR_HEIGHT),
            # widget.Spacer(), # -> crash!
            # widget.TaskList(
            #     name='external_monitor_tasklist_%d' % i,
            #     # font='Ubuntu Bold',
            #     border=colors('active', 0.8),
            #     urgend_border=colors('red', 0.8),
            #     highlight_method='block',
            #     urgent_method='block',
            #     border_width=1,
            #     rounded=False,
            #     max_title_width=2500,
            #     icon_size=16,
            #     txt_minimized='\U0001F5D5 ',  # [_] \U0001F5D5
            #     txt_maximized='\U0001F5D6 ',  # [M] \U0001F5D6
            #     txt_floating='\U0001F5D7 ',   # [F] \U0001F5D7
            #     margin=0,
            #     padding=6.5,
            # ),
            PwrLine(None, colors('active', N_PWRL_BRIGHT),
                    rtl=True, prefix=' '*0, fontsize=N_BAR_HEIGHT),
            widget.Battery(
                background=colors('active', N_PWRL_BRIGHT),
                foreground=colors('white'),
                charge_char='↑',
                discharge_char='↓',
                error_message='⚠',
                hide_threshold=25,  # 0 ≤ x ≤ 100
                low_percentage=0.15,  # 0 ≤ x ≤ 1
                markup=True,
                fontsize=N_FONTSIZE_SMALL,
                # format=u'\u2393{char}{percent:2.0%} {hour:d}:{min:02d}',
                # format='<u>{char}{percent:2.0%}\n{hour:d}:{min:02d}</u>',
                format='<b>{char}{percent:2.0%}</b>',
                update_delay=30,
            ),
            widget.CurrentLayoutIcon(
                background=colors('active', N_PWRL_BRIGHT),
                foreground=colors('white'),
                scale=0.7,
            ),
            widget.Clock(
                # format='%Y/%m/%d <b>%2H:%2M:%2S</b>',
                format='%Y/%m/%d',
                foreground=colors('white'),
                background=colors('active', N_PWRL_BRIGHT),
                markup=True,
                # fontsize=N_FONTSIZE_SMALL,
            ),
            PwrLine(colors('active', N_PWRL_BRIGHT),
                    colors('white'), rtl=True,
                    suffix=' '*0, fontsize=N_BAR_HEIGHT),
            widget.TextBox(
                text='%d ' % i,
                background=colors('white'),
                foreground=colors('black'),
                name='monitor_id_%i_right' % i,
            ),
        ], N_BAR_HEIGHT, background=colors('barbackground')),
        ),
    )

# Drag floating layouts.
mouse = scfg.get('mouse', [
    Drag([mod], 'Button1', lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], 'Button3', lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
])

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False # True
floating_layout = layout.Floating(
    float_rules=[{'wmclass': 'confirm'},
                 {'wmclass': 'dialog'},
                 {'wmclass': 'download'},
                 {'wmclass': 'error'},
                 {'wmclass': 'file_progress'},
                 {'wmclass': 'notification'},
                 {'wmclass': 'splash'},
                 {'wmclass': 'toolbar'},
                 {'wmclass': 'confirmreset'},  # gitk
                 {'wmclass': 'makebranch'},  # gitk
                 {'wmclass': 'maketag'},  # gitk
                 {'wname': 'branchdialog'},  # gitk
                 {'wname': 'pinentry'},  # GPG key password entry
                 {'wmclass': 'gcolor3'},
                 {'wmclass': 'ssh-askpass'},  # ssh-askpass
                 #{'wmclass': 'Mathematica', 'wname': 'Welcome to Wolfram Mathematica'},
                 {'wname': 'Welcome to Wolfram Mathematica'},
                 {'wmclass': 'keepass2', 'wname': reg_match('Open Database - .*')},
                 {'wmclass': 'zynaddsubfx'},
                 {'wname': 'Timeline Preferences'},
                 # {'wmtype': 'menu'}, # ardour
                 {'wname': 'Ardour'},
                 {'wname': 'Emulator'},
                 {'wname': 'Android Emulator - '},
                 # not {'wmclass': 'Mathematica'}
                 #{'wname': None},
                ],
                **D_WINDOW_SETTINGS)
auto_fullscreen = True
focus_on_window_activation = 'urgent' # urgent (urgent flag) |smart (same group) | focus (always)
wmname = 'LG3D'  # Java UI support (who cares?)
# wmname = scfg.get('wmname', 'qtile')

floating_types = ["notification", "toolbar", "splash", "dialog", "utility",
                  "menu", "dropdown_menu", "popup_menu", "tooltip,dock"]
