"""Late public packaging helper; checks the whole source and expected result."""
import argparse
import hashlib
import json
from pathlib import Path
from field import need
from reproduce import reproduce

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    manifest = json.loads((source/'MANIFEST.json').read_text())
    for name, pin in manifest['files'].items():
        raw = (source/name).read_bytes()
        need(hashlib.sha256(raw).hexdigest() == pin['sha256'] and len(raw) == pin['bytes'], 'public whole source pin: '+name)
    reproduce(args.work)
    need((args.work/'RESULT.json').read_bytes() == (source/'RESULT.json').read_bytes(), 'whole published expected result')
    print('PUBLIC_SOURCE_AND_ENTIRE_EXPECTED_RESULT_MATCH')
