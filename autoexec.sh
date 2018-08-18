#!/bin/bash
# set the resolution to something more appropriate:
xrandr --output Virtual1 --mode 1680x1050
setxkbmap -layout de
# xsetroot -solid "#000000"
nm-applet &
mate-terminal -x ls &
