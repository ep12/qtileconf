import os
import subprocess

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook

from util import colorscheme, PwrLine, TermCmd as _TermCmd, on_startup, import_from_file
# try:
#     from typing import List  # noqa: F401
# except ImportError:
#     pass

# hook.subscribe.startup_complete(on_startup)
hook.subscribe.startup_once(on_startup)


def TermCmd(program):
    '''Wrapper for TermCmd (util module)'''
    return _TermCmd(program, D_APPS)


hostname = os.uname()[1]
HOME = os.environ.get('HOME', '')
folder = os.path.dirname(os.path.realpath(__file__))
scfg = import_from_file('%s/config_%s.py' % (folder, hostname)).__dict__


mod = scfg.get('mod', 'mod4')
mod_alt = scfg.get('mod_alt', 'mod1')


N_BAR_HEIGHT = scfg.get('N_BAR_HEIGHT',      28  )
N_BORDER_WIDTH = scfg.get('N_BORDER_WIDTH',   1  )
N_PWRL_BRIGHT = scfg.get('N_PWRL_BRIGHT',     0.2)
N_GRAPH_WIDTH = scfg.get('N_GRAPH_WIDTH',    35  )
N_GRAPH_FILL = scfg.get('N_GRAPH_FILL',       1.0)
N_GRAPH_BORDER = scfg.get('N_GRAPH_BORDER',   0.2)

D_APPS = scfg.get('D_APPS', {  # Default apps
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

colors = colorscheme(scfg.get('colorscheme', {
    'red':                 (1.000, 0.000, 0.000),
    'orange':              (1.000, 0.600, 0.000),
    'yellow':              (1.000, 1.000, 0.000),
    'lime':                (0.500, 1.000, 0.000),
    'green':               (0.000, 1.000, 0.000),
    'cyan':                (0.000, 0.500, 1.000),
    'greenblue':           (0.000, 1.000, 1.000),
    'lightblue':           (0.000, 0.500, 1.000),
    'blue':                (0.000, 0.000, 1.000),
    'purple':              (0.500, 0.000, 1.000),
    'pink':                (1.000, 0.000, 1.000),

    'white':               (1.000, 1.000, 1.000),
    'neutral':             (1.000, 1.000, 1.000),
    'black':               (0.000, 0.000, 0.000),

    'active':              (0.000, 0.750, 1.000),
    'inactive':            (0.000, 0.000, 0.000),
    'barbackground':       (0.050, 0.050, 0.050),

    'CPU_G':               (1.000, 0.000, 0.000),
    'RAM_G':               (0.000, 1.000, 0.000),
    'SWAP_G':              (1.000, 0.200, 1.000),
    'HDD_G':               (1.000, 0.600, 0.000),
    'NET_G':               (0.000, 0.750, 1.000),
}))

D_WINDOW_SETTINGS = scfg.get('D_WINDOW_SETTINGS', {
    'border_focus':        colors('active'),
    'border_normal':       colors('inactive'),
    'border_width':        N_BORDER_WIDTH,
})

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
    widget.SwapGraph(
        width=N_GRAPH_WIDTH,
        line_width=1,
        border_width=1,
        border_color=colors('SWAP_G', N_GRAPH_BORDER),
        background=colors('SWAP_G', N_PWRL_BRIGHT),
        graph_color=colors('SWAP_G'),
        fill_color=colors('SWAP_G', N_GRAPH_FILL),
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
    #NOTE: system
    Key([mod, 'control', 'shift'], 'F4',
        lazy.spawn(D_APPS['GUISUDO'] + ' shutdown -h +0')),
    Key([mod, 'control', 'shift'], 'F5',
        lazy.spawn(D_APPS['GUISUDO'] + ' reboot')),

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
    Key([mod, 'shift'], 'Down', lazy.layout.shuffle_down()),
    Key([mod, 'shift'], 'Up', lazy.layout.shuffle_up()),
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
    Key([mod, 'shift'], 'Tab', lazy.previous_layout()),

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
        lazy.spawn(D_APPS['GUIBROWSER'])),
    Key([mod, 'shift'], 'w',
        lazy.spawn(D_APPS['GUIBROWSER2'])),
    Key([mod, 'control'], 'w',
        lazy.spawn(TermCmd(D_APPS['BROWSER']))),

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
    Key([mod], 'r',
        lazy.spawncmd(prompt='$')),
    Key([mod, 'shift'], 'r',
        lazy.spawncmd(prompt='#',
                      command='{} %s'.format(D_APPS['GUISUDO']))),
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

groups = [Group(i) for i in '1234567890']
for i in groups:
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
        change_ratio=0.05,
        change_size=10,
        **D_WINDOW_SETTINGS
    ),
    layout.MonadWide(
        ratio=0.5,
        min_ratio=0.01,
        max_ratio=0.99,
        change_ratio=0.05,
        change_size=10,
        **D_WINDOW_SETTINGS
    ),
    # layout.Max(),
    # layout.Floating(
    #     max_border_width=0,
    #     fullscreen_border_width=0,
    #     change_ratio=0.05,
    #     change_size=10,
    #     **D_WINDOW_SETTINGS
    # ),
    # layout.Stack(num_stacks=2),
])

if 'keys' in scfg and isinstance(scfg['keys'], list):
    keys.extend(scfg['keys'])

widget_defaults = dict(
    font='Ubuntu Sans Bold',
    fontsize=12,
    padding=4,
    border_focus=colors('active'),
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        bottom=bar.Bar([
            widget.GroupBox(
                background=colors('active', N_PWRL_BRIGHT),
                active=colors('white'),
                inactive=colors('white', 0.25),
                highlight_method='block',
                rounded=False,
                this_current_screen_border=colors('active'),
                this_screen_border=colors('active'),
                other_current_screen_border=colors('neutral'),
                other_screen_border=colors('neutral'),
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
                           suffix=' ', fontsize=N_BAR_HEIGHT),
            widget.TaskList(
                # font='Ubuntu Bold',
                border=colors('active', 0.8),
                urgend_border=colors('red', 0.8),
                highlight_method='block',
                urgent_method='block',
                border_width=1,
                rounded=False,
                max_title_width=150,
                icon_size=16,
                txt_minimized='\U0001F5D5 ',  # [_] \U0001F5D5
                txt_maximized='\U0001F5D6 ',  # [M] \U0001F5D6
                txt_floating='\U0001F5D7 ',   # [F] \U0001F5D7
                margin=0,
                padding=6.5,
            ),
            PwrLine(None, colors('neutral', N_PWRL_BRIGHT),
                    rtl=True, prefix=' ', fontsize=N_BAR_HEIGHT),
            widget.Systray(background=colors('neutral', N_PWRL_BRIGHT)),
            widget.BatteryIcon(
                theme_path=HOME+'/.config/qtile/battery-icons',
                background=colors('neutral', N_PWRL_BRIGHT),
            ),
            # widget.Wlan(
            #     update_interval=3,
            #     format='{essid}: {percent:3.0%}',
            #     disconnected_message='not connected'
            # ),
            PwrLine(colors('neutral', N_PWRL_BRIGHT), colors('CPU_G', N_PWRL_BRIGHT),
                    rtl=True, fontsize=N_BAR_HEIGHT),
            *graphbar,
            PwrLine(colors('NET_G', N_PWRL_BRIGHT), colors('white'),
                    rtl=True, fontsize=N_BAR_HEIGHT),
            widget.CheckUpdates(
                distro='Arch',
                update_interval=60*15,
                colour_have_updates=colors('red'),
                colour_no_updates=colors('barbackground'),
                # display_format=u'\u27f3 {updates}',
                display_format=u'\u2b6e {updates}',
                execute='%s %s' % (D_APPS['GUISUDO'], 'pacman -Syu --noconfirm'),
                background=colors('white'),
            ),
            widget.KeyboardLayout(
                update_interval=10,
                configured_keyboards=['de', 'de dvorak', 'us', 'us dvorak'],
                foreground=colors('active'),
                background=colors('white'),
            ),
            PwrLine(colors('white'), colors('active'), rtl=True, fontsize=N_BAR_HEIGHT),
            widget.Clock(
                format='%2H:%2M:%2S',
                foreground=colors('white'),
                background=colors('active')
            ),
        ], N_BAR_HEIGHT, background=colors('barbackground')),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], 'Button1', lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], 'Button3', lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = True
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
                 {'wmclass': 'ssh-askpass'},  # ssh-askpass
                ],
                **D_WINDOW_SETTINGS)
auto_fullscreen = True
focus_on_window_activation = 'smart'
# wmname = 'LG3D'  # Java UI support (who cares?)
wmname = 'qtile'
