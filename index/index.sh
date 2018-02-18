#!/bin/bash
find $1/ -type f ! \( -path "$1/debian*" -or -path "$1/pypi*" -or -path "$1/hp*" -or -path "$1/linux-malware-detector*"  \) -exec ./add_to_index.sh "{}" \;
