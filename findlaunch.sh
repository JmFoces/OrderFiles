#!/bin/bash
find $1/ -mindepth 1 -maxdepth 1 -type d ! -ipath "$1/debian/*" ! -ipath "*pypi*" ! -ipath "*hp*" ! -ipath "*debian_security*" 
