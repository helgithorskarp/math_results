#!/usr/bin/env python3
"""Fetch two pinned Debian amd64 tools into a fresh external directory."""
import json
from pathlib import Path
import subprocess
import sys
import urllib.request
import runtime

dest = runtime.external(sys.argv[1])
dest.mkdir(parents=True, exist_ok=False)
out = {}
for item in json.loads((runtime.SOURCE/'tools.json').read_text()):
    name = item['name']
    package = dest/(name+'.deb')
    with urllib.request.urlopen(item['url'], timeout=60) as response:
        package.write_bytes(response.read())
    if runtime.sha(package) != item['package_sha256']:
        raise ValueError('download identity')
    subprocess.run(['dpkg-deb','-x',str(package),str(dest/name)], check=True)
    binary = runtime.check_tool(dest/name/'usr/bin'/name, name)
    out[name] = str(binary)
print(json.dumps(out, sort_keys=True))
