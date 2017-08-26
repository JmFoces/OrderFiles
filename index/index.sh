#!/bin/bash
find /debianMirror/ -type f ! \( -path "/debianMirror/debian*" -or -path "/debianMirror/pypi*" -or -path "/debianMirror/hp*" -or -path "/debianMirror/linux-malware-detector*"  \) -exec ./add_to_index.sh "{}" \;
