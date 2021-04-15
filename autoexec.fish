#!/usr/bin/env fish

set sd (dirname (status filename))
pushd "$sd"

function stamp
    echo -n "["(date +"%T").(printf '%03d' (math --scale 0 (date +%N)/1e6))"]"
end
function log
    echo -e (stamp) $argv >>autoexec.log
end


set home_bssids (cat home_bssids.list)
function check_inet_home
    set -l tmp (nmcli c show --active \
        | tail -n +2 \
        | awk --field-separator '\\\\s{2,}' '{print $2}')
    for bssid in $tmp
        contains $bssid $home_bssids; and return 0
    end
    return 1
end

echo >>autoexec.log
log "Running autoexec.fish"

log "Early start: gnome-keyring-daemon"
/usr/bin/gnome-keyring-daemon --start --components=pkcs11 &
/usr/bin/gnome-keyring-daemon --start --components=secrets &
/usr/bin/gnome-keyring-daemon --start --components=ssh &

set bluemic (lsusb | grep "BLUE USB" >/dev/null; \
    and echo 'connected')
set home_monitor (hwinfo --monitor --short | grep "DELL P4317Q" >/dev/null; \
    and echo 'connected')

log "BLUE: $bluemic"
log "DELL: $home_monitor"

log "Audio setup"
function fix_pulseaudio_if_necessary
    set -l fail_count 0
    while not pamixer --list-sinks
        set -l fail_count (math "$fail_count+1")
        if test "$fail_count" -ge 10
            log "A: [ FAIL ] Failed to fix pulseaudio. Fix it manually!"
            log "A: [ INFO ] pulseaudio:" (pgrep pulseaudio)
            break
        end
        log "A: try $fail_count to get pulseaudio working"
        while pgrep pulseaudio
            killall -SIGSEGV pulseaudio
        end
        pulseaudio -D
        sleep 0.2
    end
end
if test -n "$bluemic"
    # get ready: fire up JACK and pulseaudio
    log "A: JACK+pulseaudio"
    touch /tmp/enable-jack-setup &
    log "A: jackd running:" (pgrep jack; and echo yes; or echo no)
    log "A: pulse running:" (pgrep pulseaudio; and echo yes; or echo no)
    if pgrep pulseaudio
        log "A: Found" (pacmd list-sinks | grep index | wc -l) "pulse sinks"
        log "A: Found" (pacmd list-sources | grep index | wc -l) "pulse sources"
    end
    pgrep jack; or jackdbus auto &
    pgrep pulseaudio; and killall -SIGSEGV pulseaudio &

    log "A: jack_control"
    jack_control start
    jack_control ds alsa
    jack_control dps device hw:PCH,0
    jack_control dps rate 48000
    jack_control dps nperiods 2
    jack_control dps period 1024
    jack_control dps duplex True
    jack_control dps midi-driver raw

    jack_wait -c
    log "A: JACK is ready"

    log "A: cadence-session-start"
    cadence-session-start --maybe-system-start &

    log "A: non-mixer"
    non-mixer ~/.config/non-mixer/QuadruMix &
    pulseaudio -D
    sleep 0.2
    set -l fail_count 0
    fix_pulseaudio_if_necessary
    log "A: Found" (pacmd list-sinks | grep index | wc -l) "pulse sinks"
    log "A: Found" (pacmd list-sources | grep index | wc -l) "pulse sources"
    log "A: Connecting (QuadruMix)"
    aj-snapshot -jxr ~/.config/aj-snapshots/QuadruMix.xml
    log "A: Setup done"
else
    log "A: pulseaudio"
    rm -f /tmp/enable-jack-setup
    pgrep pulseaudio; or pulseaudio -D
    sleep 0.2
    fix_pulseaudio_if_necessary
    log "A: Setup done"
end

log "Starting backup terminal"
termite --directory ~ &

log "dmps+screensaver: off"
xset s off
xset -dmps
log "desktop background"
hsetroot -solid "#2f0000"
xsetroot -solid black

if test -n "$home_monitor"
    log "screen layout"
    ~/.screenlayout/HDMI\ FHD\ left &
end

log "Various daemons"
dunst &
pgrep nm-applet; or nm-applet &
redshift -m randr -v -t 6500:4000 -l 52.24:9.66 &
set home_inet (check_inet_home; and echo "connected")
log "INET: $home_inet"
if test -n "$bluemic" -o -n "$home_monitor" -o -n "$home_inet"
    log "Starting @Home daemons and applets"
    skypeforlinux &
    seafile-applet &
    systemctl start --user mpd &
    emacs --daemon &
    safeeyes &

    if lsusb | egrep "debug" >/dev/null
        for l in (adb devices)
            log "ADB: $l"
        end
    end
end
wal -R
if test (jq -r '.wallpaper' ~/.cache/wal/colors.json) = None
    xsetroot -solid (jq -r '.special["background"]' ~/.cache/wal/colors.json)
end

log "Reached end of autoexec.fish"
log "Bye"
