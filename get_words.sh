#!/bin/bash
#cat /etc/dictionaries-common/words |
cat /usr/share/dict/words |
    sed 's/\W//g' |
    sed -E 's/^\w{,4}$//g' |
    sed -E 's/^\w{6,}$//g' |
    awk NF
