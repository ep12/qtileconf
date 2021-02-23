#!/usr/bin/env python3
from libqtile.config import Screen, Match
from libqtile import bar, layout, widget
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
window_defaults = {  # non-standard
    'border_focus': colors('active'),
    'border_normal': colors('inactive'),
    'border_width': 1,
}

layouts = [
    layout.MonadTall(ratio=0.5, min_ratio=0.05, max_ratio=0.95,
                     change_ratio=0.02, change_size=10, **window_defaults),
    layout.MonadWide(ratio=0.5, min_ratio=0.05, max_ratio=0.95,
                     change_ratio=0.02, change_size=10, **window_defaults),
    layout.Bsp(grow_amount=0.02, ratio=1.6, lower_right=False,
               **window_defaults),
    layout.Matrix(columns=2, margin=0, **window_defaults),
    layout.Matrix(columns=3, margin=0, **window_defaults),
    layout.TreeTab(active_bg=colors('active'),
                   active_fg=colors('barbackground'),
                   inactive_bg=colors('barbackground'),
                   inactive_fg=colors('white'),
                   section_fg=colors('active'),
                   bg_color=colors('barbackground'),
                   section_fontsize=widget_defaults['fontsize'],
                   fontsize=widget_defaults['fontsize'],
                   level_shift=4, margin_left=4, margin_y=4,
                   padding_left=4, padding_x=4, padding_y=2,
                   panel_width=250, previous_on_rm=True,
                   section_bottom=4, section_left=4, section_padding=4,
                   section_top=4, section=['Default'],
                   vpace=2, **window_defaults),
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
        widget.GroupBox(name='main_group_box', rounded=False,
                        highlight_method='block', urgent_method='block',
                        margin=0, padding=6, borderwidth=1,
                        background=colors('active', N_PWRL_BRIGHT),
                        active=colors('white'), inactive=colors('white', 0.25),
                        this_current_screen_border=colors('active'),
                        this_screen_border=colors('active', 0.5),
                        other_screen_border=colors('theme_orange', 0.5),
                        urgent_text=colors('red', 0.8),
                        urgent_border=colors('red', 0.8)),
        widget.Prompt(bell_style='audible', prompt=' {prompt} ',
                      background=colors('active', N_PWRL_BRIGHT),
                      foreground=colors('active'),
                      cursor_color=colors('white')),
        PwrLine(colors('NET_G', N_PWRL_BRIGHT), None, fontsize=N_BAR_HEIGHT),
        widget.TaskList(name='internal_monitor_tasklist',
                        highlight_method='block', urgent_method='block',
                        margin=0, padding=6.5, border_width=1,
                        rounded=False, icon_size=16,
                        txt_minimized='\U0001F5D5 ',
                        txt_maximized='\U0001F5D6 ',
                        txt_floating='\U0001F5D7 ',
                        foreground=colors('white'), border=colors('active', 0.8),
                        urgent_border=colors('red', 0.8)),
        PwrLine(None, colors('neutral', N_PWRL_BRIGHT), rtl=True,
                fontsize=N_BAR_HEIGHT),
        widget.Systray(background=colors('neutral', N_PWRL_BRIGHT)),
        # PwrLine(colors('neutral', N_PWRL_BRIGHT),
        #         colors('CPU_G', N_PWRL_BRIGHT),
        #         rtl=True, fontsize=N_BAR_HEIGHT),
        widget.DF(name='diskfree_root', partition='/',
                  update_interval=3600, warn_space=5,
                  background=colors('neutral', N_PWRL_BRIGHT)),  # CPU_G
        widget.DF(name='diskfree_home', partition='/home',
                  update_interval=3600, warn_space=10,
                  background=colors('neutral', N_PWRL_BRIGHT)),  # CPU_G
        # BEGIN: GRAPHBAR
        # widget.CPUGraph(**GRAPH_OPTS,
        #                 border_color=colors('CPU_G', N_GRAPH_BORDER),
        #                 background=colors('CPU_G', N_PWRL_BRIGHT),
        #                 graph_color=colors('CPU_G'),
        #                 fill_color=colors('CPU_G', N_GRAPH_FILL)),
        # PwrLine(colors('CPU_G', N_PWRL_BRIGHT), colors('RAM_G', N_PWRL_BRIGHT),
        #         rtl=True, fontsize=N_BAR_HEIGHT),
        # widget.MemoryGraph(**GRAPH_OPTS,
        #                    border_color=colors('RAM_G', N_GRAPH_BORDER),
        #                    background=colors('RAM_G', N_PWRL_BRIGHT),
        #                    graph_color=colors('RAM_G'),
        #                    fill_color=colors('RAM_G', N_GRAPH_FILL)),
        # END: GRAPHBAR
        PwrLine(colors('neutral', N_PWRL_BRIGHT), colors('white'),  # NET_G
                rtl=True, fontsize=N_BAR_HEIGHT, prefix='\u2009'),
        widget.KeyboardLayout(configured_keyboards=['de nodeadkeys',
                                                    'de dvorak',
                                                    'us', 'us dvorak'],
                              update_interval=30, markup=False,
                              fontsize=10, foreground=colors('active'),
                              background=colors('white'),
                              display_map={'de nodeadkeys': 'DE\nNDK',
                                           'de dvorak': 'DE\nDVO', 'us': 'US',
                                           'us dvorak': 'US\nDVO'}),
        PwrLine(colors('white'), colors('active'),
                rtl=True, fontsize=N_BAR_HEIGHT),
        widget.Backlight(name='internal_brightness_indicator',
                         change_command='light -S {0}',
                         backlight_name='intel_backlight',
                         fmt='{}', format='{percent:2.0%}',
                         update_interval=30,
                         foreground=colors('yellow'),
                         background=colors('active')),
        widget.Battery(notify_below=0.3,
                       charge_char='↑', discharge_char='↓', error_message='⚠',
                       hide_threshold=0.99, low_percentage=0.15,
                       markup=True, fontsize=10, update_delay=30,
                       format=('<b>{char}{percent:2.0%}\n'
                               '{hour:d}:{min:02d}</b>'),
                       background=colors('active'),
                       foreground=colors('white')),
        widget.Chord(name='chord_display',
                     background=colors('active'), foreground=colors('red')),
        widget.CurrentLayoutIcon(scale=0.7, background=colors('active'),
                                 foreground=colors('white')),
        widget.Clock(format='%Y/%m/%d\n<b>%2H:%2M:%2S</b>', markup=True,
                     fontsize=10, foreground=colors('white'),
                     background=colors('active')),
    ],
                   N_BAR_HEIGHT, background=colors('barbackground'))
)


screens = [screen_0]
for i in range(1, 4):
    screens.append(Screen(
        bottom=bar.Bar(
            [
                widget.TextBox(text=f' {i}', name=f'monitor_id_{i}_left',
                               background=colors('white'),
                               foreground=colors('black')),
                PwrLine(colors('white'), colors('active', N_PWRL_BRIGHT),
                        fontsize=N_BAR_HEIGHT),
                widget.GroupBox(name=f'group_box_{i}', rounded=False,
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
                widget.TaskList(name=f'tasklist_{i}', rounded=False,
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
                widget.Battery(charge_char='↑', discharge_char='↓',
                               error_message='⚠', hide_threshold=0.5,
                               low_percentage=0.15, markup=True, fontsize=10,
                               update_delay=30,
                               format='<b>{char}{percent:2.0%}</b>',
                               background=colors('active'),
                               foreground=colors('white')),
                widget.CurrentLayoutIcon(scale=0.7, foreground=colors('white'),
                                         background=colors('active',
                                                           N_PWRL_BRIGHT)),
                widget.Clock(format='%Y/%m/%d', markup=True,
                             foreground=colors('white'),
                             background=colors('active', N_PWRL_BRIGHT)),
                PwrLine(colors('active', N_PWRL_BRIGHT), colors('white'),
                        rtl=True, fontsize=N_BAR_HEIGHT),
                widget.TextBox(text=f' {i}', name=f'monitor_id_{i}_left',
                               background=colors('white'),
                               foreground=colors('black')),
            ],
            N_BAR_HEIGHT,
            background=colors('barbackground')
        )
    ))
