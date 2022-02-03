#!/bin/bash

# Get the list of all 5 letter words
cat /usr/share/dict/words | grep -E '^[a-z]{5}$'
