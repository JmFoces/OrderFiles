#!/bin/bash
head -1 "$@" | awk -F" " '{print $2}' | perl -pe 's/\\012-//'
