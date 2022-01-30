#!/bin/bash
cat /usr/share/dict/american-english |
    sed 's/\W//g' |
    sed -E 's/^\w{,4}$//g' |
    sed -E 's/^\w{6,}$//g' |
    awk NF
