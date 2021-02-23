#!/bin/bash

echo $(date -R) Running autoexec.sh >>~/.config/qtile/autoexec.log

killall -SIGKILL pulseaudio
killall jackd
pulseaudio -D
# mft
termite &

# wacom_ff --log-level 10 --device 'Wacom Intuos BT S Pen stylus' &
# wacom_ff service: https://www.github.com/ep12/wacom_follow_focus

cadence-session-start --maybe-system-start &

env GDK_BACKEND=x11 safeeyes &

/usr/bin/gnome-keyring-daemon --start --components=pkcs11 &
/usr/bin/gnome-keyring-daemon --start --components=secrets &
/usr/bin/gnome-keyring-daemon --start --components=ssh &

# ibus-daemon &

# set the resolution to something more appropriate:
# xrandr --output Virtual1 --mode 1680x1050

# setxkbmap -layout de

# xsetroot -solid "#000000"
# xrdb -merge /home/simon/.Xresources

# network manager
pgrep nm-applet || nm-applet &

# temporarily disabled
# amixer set Master off
# amixer -c PCH set Headphone on
# amixer -c PCH set Speaker on
# amixer -c PCH set Capture nocap
###  amixer -D pulse set Capture nocap

# redshift night color filter
redshift -m randr -v -t 6500:4000 -l 52.24:9.66 &
# use `pkill -x redshift` to stop daemon
# start-pulseaudio-x11 &

# sleep 3
# if nmcli -o --wait 5 | grep -P "connected to FRITZ\!Box \d+ Cable" >/dev/null; then
# 	# echo "YES!";
# 	safeeyes && echo "";
# else
# 	echo "No wifi connection :(";
# fi

#if xrandr --listactivemonitors | egrep "Monitors: 1"; then
#	echo "int monitor only";
#else
#	arandr & echo "";
#fi
# TODO: xrandr --listactivemonitors


xset s off
xset -dpms

hsetroot -solid "#2f0000"
xsetroot -solid black

# 2nd monitor
#if xrandr --listmonitors | grep -o 'DP1 1920/940x1080/530+0+0  DP1'
hwinfo --monitor --short | grep "DELL P4317Q" && ~/.screenlayout/HDMI\ FHD\ left
#end
# lsusb | grep "BLUE USB" && cadence --minimised &
seafile-applet &

# pause wacom_ff
# kill -SIGUSR1 $(pgrep wacom_ff)
#sleep 5
#systemctl start --user mpd

echo $(date -R) Ran autoexec.sh >>~/.config/qtile/autoexec.log.old

dunst &

if jack_connect x y 2>&1 | grep -o "jack server not running"; then
	 killall cadence
	 killall pulseaudio
	 killall jackd
	 cadence-session-start --maybe-system-start &
	 pulseaudio -D
fi

sleep 2
## lsusb | grep "BLUE USB" && non-mixer ~/.config/non-mixer/mpv-live-input &
lsusb | grep "BLUE USB" && non-mixer ~/.config/non-mixer/QuadruMix &
# pavucontrol &
# sleep 1
# restore jack connections
## lsusb | grep "BLUE USB" && aj-snapshot -jxr ~/.config/aj-snapshots/Non-Mixer\ Route.xml
lsusb | grep "BLUE USB" && aj-snapshot -jxr ~/.config/aj-snapshots/QuadruMix.xml


lsusb | grep "BLUE USB" && emacs --daemon
test $(pacmd list-sinks | grep index | wc -l) -gt 4 && systemctl start --user mpd
