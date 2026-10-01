"""Fetch only the two public exact inputs, authenticate before writing."""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.request


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dest', required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / 'INPUTS.json').read_text())
    dest = Path(args.dest)
    dest.mkdir(parents=True, exist_ok=True)
    for item in manifest['files']:
        with urllib.request.urlopen(item['download_url'], timeout=30) as response:
            raw = response.read()
        if len(raw) != item['bytes'] or hashlib.sha256(raw).hexdigest() != item['sha256']:
            raise ValueError('Public source input changed: ' + item['name'])
        target = dest / item['name']
        if target.exists() and target.read_bytes() != raw:
            raise ValueError('Existing destination has different contents: ' + str(target))
        target.write_bytes(raw)
        print(item['name'], item['sha256'])


if __name__ == '__main__':
    main()
