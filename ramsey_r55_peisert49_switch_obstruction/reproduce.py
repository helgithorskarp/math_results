"""Replay the compact proof and its bounded independent controls."""
import hashlib
import json
from pathlib import Path

import build
import check
import controls


def main():
    root = Path(__file__).parent
    for line in (root/'SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ', 1)
        check.need(hashlib.sha256((root/name).read_bytes()).hexdigest() == digest, 'manifest: '+name)
    raw = (json.dumps(build.build(), separators=(',', ':'))+'\n').encode()
    check.need(raw == (root/'certificate.json').read_bytes(), 'entrywise certificate reproduction')
    result = check.check(json.loads(raw))
    check.need(result == json.loads((root/'expected.json').read_text()), 'expected certificate result')
    check.need(controls.run() == json.loads((root/'expected_controls.json').read_text()), 'expected controls')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
