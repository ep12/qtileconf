#!/bin/bash
if ps -A | grep redshift >/dev/null; then
    # echo "runs";
    pkill -x redshift
else
    # echo "does not run";
    redshift -m randr -v -t 6500:4000 -l 52.24:9.66 &
fi
