#!/bin/bash

# Get the list of all 5 letter words
cat /usr/share/dict/words   |
    # Remove everything except lowercase ascii characters a-z
    sed 's/[^a-z]//g'       |
    # Remove words < 4 characters
    sed -E 's/^\w{,4}$//g'  |
    # Remove words > 5 characters
    sed -E 's/^\w{6,}$//g'  |
    # Remove emtpy lines
    awk NF
