find /debianMirror/ -mindepth 1 -maxdepth 1 -type d ! -ipath "/debianMirror/debian/*" ! -ipath "*pypi*" ! -ipath "*hp*" ! -ipath "*debian_security*" 
