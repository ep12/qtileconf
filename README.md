# About this config

This config uses:
+ Ubuntu fonts, powerline-patched:
+ debian-based: install *fonts-powerline*
+ dunst
+ termite, alacritty

Summary:

+ Not much eyecandy, a lot of functionality: keybindings, startup script (alsa+pulseaudio or alsa+JACK+pulseaudio depending on the connection state)

# Screenshots

## Demo windows

![Desktop with some programs](images/desktop-demo.png)  

## Second monitor

![Empty second monitor](images/desktop-external-empty.png)

# Keybindings

This section is outdated and will not be updated soon. Read the source code ([keys.py](keys.py), …) to find out what actually works. The complete overhaul should have increased the readability quite a lot.

MACS | Key            | Action                                 | Status
:----|:---------------|:---------------------------------------|:-------
M=CS | F4             | system: shutdown                       | commented out 
M=CS | F5             | system: reboot                         | commented out 
M=C= | F5             | qtile: restart                         | ✓
M=C= | F4             | qtile: quit                            | ✓
M=C= | Left, Right    | workspace: move to prev/next workspace | ✓
M=C= | 1-0            | workspace: goto workspace              | ✓
M=CS | 1-0            | workspace: move window to workspace    | ✓
=A== | Tab            | layout: cycle windows                  | ✓
=A=S | Tab            | layout: cycle windows (reverse)        | ⚠
M=== | *arrows*       | layout: focus windows                  | ✓
M==S | *arrows*       | layout: move window                    | ✓
M==S | KP_Insert      | layout: rotate windows                 | ⚠  
M=== | +, -           | layout: Resize window                  | ✓
M=== | Return         | layout: maximize/minimize window       | ✓
M==S | Return         | layout: normalize window               | ⚠
M=== | Tab            | layout: cycle layout                   | ✓
M==S | Tab            | layout: cycle layout (reverse)         | ⚠
M=== | F11            | window: toggle fullscreen              | ✓
M==S | F11            | window: toggle floating                | ✓
M=== | F4             | window: quit                           | 👴
=A== | F4             | window: quit                           | ✓
M=== | 1-0            | launch: custom hotkeys 1               | ✓
M==S | 1-0            | launch: custom hotkeys 2               | ✓
M=== | t              | launch: GUI terminal emulator (termite) | ✓
==CS | Escape         | launch: htop (dropdown)                | ✓
M=== | f              | launch: GUI file manager               | ✓
==== | XF86WWW        | launch: GUI WWW browser                | ?
===S | XF86WWW        | launch: GUI WWW browser 2              | ?
==C= | XF86WWW        | launch: text WWW browser               | ?
M=== | W              | launch: firefox (default profile) | ✓
M==S | W              | launch: browser selector (rofi menu) | ✓
M=C= | W              | launch: firefox (work profile) | ✓
M=== | r              | prompt: run                            | ✓

# Graphs
Currently not implemented: https://github.com/qtile/qtile/issues/2175

1. CPU
1. RAM
1. SWAP
1. HDD
1. NET
