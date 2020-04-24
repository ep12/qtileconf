#!/bin/bash

echo $(date -R) Running autoexec.sh >>~/.config/qtile/autoexec.log.old

# set the resolution to something more appropriate:
# xrandr --output Virtual1 --mode 1680x1050

# setxkbmap -layout de

xsetroot -solid "#000000"
#xrdb -merge /home/simon/.Xresources

# network manager
pgrep nm-applet || nm-applet &

# mft
#roxterm &
urxvt &

amixer set Master off
amixer -c PCH set Headphone on
amixer -c PCH set Speaker on
amixer -c PCH set Capture nocap
amixer -D pulse set Capture nocap

# redshift night color filter
redshift -m randr -v -t 6500:4000 -l 52.24:9.66 &
# use `pkill -x redshift` to stop daemon
# start-pulseaudio-x11 &

sleep 3
if nmcli -o --wait 5 | grep -P "connected to FRITZ\!Box \d+ Cable" >/dev/null; then
	# echo "YES!";
	safeeyes && echo "";
else
	echo "No wifi connection :(";
fi

#if xrandr --listactivemonitors | egrep "Monitors: 1"; then
#	echo "int monitor only";
#else
#	arandr & echo "";
#fi
# TODO: xrandr --listactivemonitors

echo $(date -R) Ran autoexec.sh >>~/.config/qtile/autoexec.log.old
