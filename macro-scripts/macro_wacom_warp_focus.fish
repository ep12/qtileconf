#!/usr/bin/env fish
set sd (dirname (status filename))
pushd "$sd"

# echo >>wwf.log
# echo (date) "Engage!" >>wwf.log
# xdotool getactivewindow getwindowname getwindowgeometry >>wwf.log

set pos (xdotool getactivewindow getwindowgeometry \
    | grep -Po '(?<=Position: )\\d+,\\d+')
set x (echo $pos | grep -Po '\\d+(?=,)')
set y (echo $pos | grep -Po '(?<=,)\\d+')
set display_list (xrandr --listmonitors | grep -Po ' \\d+: [+*]*\\S+')
set display_geom (xrandr --listmonitors \
    | grep -Po '\d+/\d+x\d+/\d+\+\d+\+\d+')
echo $display_geom

for j in (seq 1 (count $display_list))
    set -l disp $display_list[$j]
    echo $display_geom[$j] \
        | sed 's|/[0-9]+||g;s|x|+|g' \
        | read -d + width height xmin ymin
    set xmax (math "$xmin+$width-1")
    set ymax (math "$ymin+$height-1")

    set -l i (echo $disp | grep -Po '\\d+(?=:\\s+\\S+)')

    if test $x -ge $xmin -a $x -le $xmax -a $y -ge $ymin -a $y -le $ymax
        echo $disp
        set -l n (echo $disp | sed "s/\\s*$i:\\s*[+*]*//g")
        # echo "Warping to $n" >>wwf.log
        xsetwacom set "Wacom Intuos BT S Pen stylus" MapToOutput "$n"
        popd
        exit 0
    end
end
