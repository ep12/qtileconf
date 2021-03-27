#!/usr/bin/env fish
set colorschemes (begin
    pushd /usr/lib/python3.*/site-packages/pywal/colorschemes/
    find . | grep -Po '(?<=^./)((dark|light)/.*)'; popd
    pushd ~/.config/wal/colorschemes/
    find . | grep -Po '(?<=^./)((dark|light)/.*)'; popd
end | sort | uniq | sed 's/.json$//g')

if test -n "$argv[1]"; and contains "$argv[1]" $colorschemes
    set selection "$argv[1]"
else
    set rofi_args -fullscreen -no-custom-no-click-to-exit -columns 5
    set selection (for c in $colorschemes
        echo $c
    end | rofi -p 'Theme' -dmenu $rofi_args 2>/dev/null)
    if test -z "$selection"
        exit 0
    end
end
set theme (echo $selection | sed 's:^(light|dark)/::g')
set light (echo $selection | grep -Pq '^light/'; and echo '-l')
wal -q --theme $theme $light >/tmp/wal.log
if test (jq -r '.wallpaper' ~/.cache/wal/colors.json) = None
    xsetroot -solid (jq -r '.special["background"]' ~/.cache/wal/colors.json)
end
echo -n "$selection" > ~/.cache/wal/theme.name # we need this in qtile
