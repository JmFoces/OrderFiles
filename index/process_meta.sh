#!/bin/bash

find /srv -name "*.meta" -exec ./get_mime.sh {} \; >> metas.log

cat metas.log | sort|uniq > metas.log.uniq 
