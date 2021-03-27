#!/usr/bin/env python3
from libqtile.config import Screen, Match
from libqtile import bar, layout, widget as w
from theme import colors, PwrLine

N_BAR_HEIGHT = 28
N_PWRL_BRIGHT = 0.2
N_GRAPH_FILL = 1.0
N_GRAPH_BORDER = 0.2
GRAPH_OPTS = {
    'width': 35,
    'border_width': 1,
    'line_width': 1,
}

widget_defaults = {
    'font': 'Ubuntu Sans Bold',
    'fontsize': 12,
    'padding': 4,
}
extension_defaults = widget_defaults.copy()
window_defaults = {
    'border_width': 1,
    '_t_factory': {'border_focus': 'Active', 'border_normal': 'Bar.bg'},
}

layouts = [
    layout.MonadTall(ratio=0.5, min_ratio=0.05, max_ratio=0.95, change_ratio=0.02, change_size=10,
                     **window_defaults),
    layout.MonadWide(ratio=0.5, min_ratio=0.05, max_ratio=0.95,
                     change_ratio=0.02, change_size=10, **window_defaults),
    layout.Tile(add_after_last=True, ratio=0.55, ratio_increment=0.02,
                shift_windows=True, **window_defaults),
    # layout.Bsp(grow_amount=0.02, ratio=1.6, lower_right=False,
    #            **window_defaults),
    layout.Matrix(columns=2, margin=0, name='matrix2', **window_defaults),
    layout.Matrix(columns=3, margin=0, name='matrix3', **window_defaults),
    layout.TreeTab(level_shift=4, panel_width=250, section_fontsize=widget_defaults['fontsize'],
                   fontsize=widget_defaults['fontsize'], previous_on_rm=True, section=['Default'],
                   border_width=window_defaults.get('border_width', 1), margin_left=4, margin_y=4,
                   padding_left=4, padding_x=4, padding_y=2, vspace=2,
                   section_bottom=4, section_left=4, section_padding=4, section_top=4,
                   _t_factory={'active_bg': 'Active', 'active_fg': 'Text.bold',
                               'inactive_bg': 'Bar.bg', 'inactive_fg': 'Text.bold',
                               'section_fg': 'Text.bold', 'bg_color': 'Bar.bg'}),
]
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class / name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class='confirmreset'),  # gitk
        Match(wm_class='makebranch'),  # gitk
        Match(wm_class='maketag'),  # gitk
        Match(wm_class='ssh-askpass'),  # ssh-askpass
        Match(title='branchdialog'),  # gitk
        Match(title='pinentry'),  # GPG key password entry
    ],
    no_reposition_rules=None,
    **window_defaults
)


screen_0 = Screen(
    bottom=bar.Bar([
        w.GroupBox(name='main_group_box', rounded=False, highlight_method='block',
                   urgent_method='block', margin=0, padding=6, borderwidth=1,
                   _t_factory={'background': 'GroupBox.bg', 'active': 'Text.bold',
                               'this_current_screen_border': 'GroupBox.csb',
                               'inactive': 'Text.gray', 'this_screen_border': 'GroupBox.sb',
                               'other_screen_border': 'GroupBox.sb', 'urgent_text': 'Alert.bold',
                               'urgent_border': 'Alert.bold'}),
        w.Prompt(bell_style='audible', prompt=' {prompt} ',
                 _t_factory={'background': 'GroupBox.bg', 'foreground': 'Text.bold',
                             'cursor_color': 'red'}),
        PwrLine(fontsize=N_BAR_HEIGHT, right_color=None, _t_factory={'left_color': 'GroupBox.bg'}),
        w.TaskList(name='internal_monitor_tasklist', highlight_method='block', rounded=False,
                   urgent_method='block', margin=0, padding=6.5, border_width=1, icon_size=16,
                   txt_minimized='\U0001F5D5 ', txt_maximized='\U0001F5D6 ',
                   txt_floating='\U0001F5D7 ',
                   _t_factory={'foreground': 'Text.bold', 'border': 'Active',
                               'urgent_border': 'Alert.dim'}),
        PwrLine(left_color=None, rtl=True, fontsize=N_BAR_HEIGHT,
                _t_factory={'right_color': 'Systray.bg'}),
        w.Systray(_t_factory={'background': 'Systray.bg'}),
        # PwrLine(colors('neutral', N_PWRL_BRIGHT),
        #         colors('CPU_G', N_PWRL_BRIGHT),
        #         rtl=True, fontsize=N_BAR_HEIGHT),
        w.DF(name='diskfree_root', partition='/', update_interval=3600, warn_space=5,
             _t_factory={'background': 'Systray.bg'}),  # CPU_G
        w.DF(name='diskfree_home', partition='/home', update_interval=3600, warn_space=10,
                  _t_factory={'background': 'Systray.bg'}),  # CPU_G
        # BEGIN: GRAPHBAR
        # w.CPUGraph(**GRAPH_OPTS,
        #                 border_color=colors('CPU_G', N_GRAPH_BORDER),
        #                 background=colors('CPU_G', N_PWRL_BRIGHT),
        #                 graph_color=colors('CPU_G'),
        #                 fill_color=colors('CPU_G', N_GRAPH_FILL)),
        # PwrLine(colors('CPU_G', N_PWRL_BRIGHT), colors('RAM_G', N_PWRL_BRIGHT),
        #         rtl=True, fontsize=N_BAR_HEIGHT),
        # w.MemoryGraph(**GRAPH_OPTS,
        #                    border_color=colors('RAM_G', N_GRAPH_BORDER),
        #                    background=colors('RAM_G', N_PWRL_BRIGHT),
        #                    graph_color=colors('RAM_G'),
        #                    fill_color=colors('RAM_G', N_GRAPH_FILL)),
        # END: GRAPHBAR
        PwrLine(rtl=True, fontsize=N_BAR_HEIGHT, prefix='\u2009',
                _t_factory={'left_color': 'Systray.bg', 'right_color': 'KBLayout.bg'}),
        w.KeyboardLayout(update_interval=30, markup=False, fontsize=10,
                         configured_keyboards=['de nodeadkeys', 'de dvorak', 'de neo',
                                               'us', 'us dvorak'],
                         display_map={'de nodeadkeys': 'DE\nNDK', 'de dvorak': 'DE\nDVO',
                                      'de neo': 'DE\nNEO', 'us': 'US', 'us dvorak': 'US\nDVO'},
                         _t_factory={'background': 'KBLayout.bg', 'foreground': 'KBLayout.fg'}),
        PwrLine(rtl=True, fontsize=N_BAR_HEIGHT,
                _t_factory={'left_color': 'KBLayout.bg', 'right_color': 'Trailer.bg'}),
        w.Backlight(name='internal_brightness_indicator', change_command='light -S {0}', fmt='{}',
                    format='{percent:2.0%}', backlight_name='intel_backlight', update_interval=30,
                    _t_factory={'foreground': 'Trailer.fg', 'background': 'Trailer.bg'}),
        w.Battery(notify_below=0.3, charge_char='↑', discharge_char='↓', error_message='⚠',
                  hide_threshold=0.99, low_percentage=0.15, markup=True, fontsize=10,
                  update_delay=30, format=('<b>{char}{percent:2.0%}\n{hour:d}:{min:02d}</b>'),
                  _t_factory={'foreground': 'Trailer.fg', 'background': 'Trailer.bg'}),
        w.Chord(name='chord_display',
                _t_factory={'foreground': 'Alert.bold', 'background': 'Trailer.bg'}),
        w.CurrentLayoutIcon(scale=0.7,
                            _t_factory={'foreground': 'Trailer.fg', 'background': 'Trailer.bg'}),
        w.Clock(format='%Y/%m/%d\n<b>%2H:%2M:%2S</b>', markup=True, fontsize=10,
                _t_factory={'foreground': 'Trailer.fg', 'background': 'Trailer.bg'}),
    ], N_BAR_HEIGHT, _t_factory={'background': 'Bar.bg'})
)


screens = [screen_0]
for i in range(1, 4):
    screens.append(Screen(
        bottom=bar.Bar([
            w.TextBox(text=f' {i}', name=f'monitor_id_{i}_left',
                      background=colors('white'),
                      foreground=colors('black')),
            PwrLine(colors('white'), colors('active', N_PWRL_BRIGHT),
                    fontsize=N_BAR_HEIGHT),
            w.GroupBox(name=f'group_box_{i}', rounded=False,
                       highlight_method='block', urgent_method='block',
                       margin=0, padding=4, borderwidth=1,
                       background=colors('active', N_PWRL_BRIGHT),
                       active=colors('white'),
                       inactive=colors('white', 0.25),
                       this_current_screen_border=colors('active'),
                       this_screen_border=colors('active', 0.5),
                       other_screen_border=colors('theme_orange', 0.5),
                       urgent_text=colors('red', 0.8),
                       urgent_border=colors('red', 0.8)),
            PwrLine(colors('active', N_PWRL_BRIGHT), None,
                    fontsize=N_BAR_HEIGHT),
            w.TaskList(name=f'tasklist_{i}', rounded=False,
                       highlight_method='block', urgent_method='block',
                       margin=0, padding=6.5, border_width=1,
                       icon_size=16,
                       txt_minimized='\U0001F5D5 ',
                       txt_maximized='\U0001F5D6 ',
                       txt_floating='\U0001F5D7 ',
                       foreground=colors('white'),
                       border=colors('active', 0.8),
                       urgent_border=colors('red', 0.8)),
            PwrLine(None, colors('active', N_PWRL_BRIGHT),
                    rtl=True, fontsize=N_BAR_HEIGHT),
            w.Battery(charge_char='↑', discharge_char='↓',
                      error_message='⚠', hide_threshold=0.5,
                      low_percentage=0.15, markup=True, fontsize=10,
                      update_delay=30,
                      format='<b>{char}{percent:2.0%}</b>',
                      background=colors('active'),
                      foreground=colors('white')),
            w.CurrentLayoutIcon(scale=0.7, foreground=colors('white'),
                                background=colors('active',
                                                  N_PWRL_BRIGHT)),
            w.Clock(format='%Y/%m/%d', markup=True,
                    foreground=colors('white'),
                    background=colors('active', N_PWRL_BRIGHT)),
            PwrLine(colors('active', N_PWRL_BRIGHT), colors('white'),
                    rtl=True, fontsize=N_BAR_HEIGHT),
            w.TextBox(text=f' {i}', name=f'monitor_id_{i}_left',
                      background=colors('white'),
                      foreground=colors('black')),
            ],
            N_BAR_HEIGHT,
            _t_factory={'background': 'Bar.bg'},
        )
    ))
