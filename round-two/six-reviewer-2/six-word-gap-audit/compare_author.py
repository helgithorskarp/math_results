"""Optional entry-level comparison; independent audit.py imports no author code."""
from pathlib import Path
import argparse
import json
import sys
import audit


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('author_directory', type=Path)
    args = parser.parse_args()
    given = json.loads(Path(__file__).with_name('INPUT.json').read_text())
    result, arrays = audit.run(given)
    sys.path.insert(0, str(args.author_directory.resolve()))
    import produce
    import verify
    from common import compact_manifest
    a, b = produce.run(given), verify.run(given)
    for key in set(a) - {'execution'}:
        audit.require(a[key] == b[key], 'author arrays differ: ' + key)
    keys = ['noncontained', 'orbit', 'partners', 'edges', 'frames', 'sharp_code', 'sharp_gaps']
    for key in keys:
        normalized = json.loads(json.dumps(a[key]))
        audit.require(normalized == json.loads(json.dumps(arrays[key])),
                      'independent array differs: ' + key)
    expected = json.loads((args.author_directory / 'manifest.json').read_text())
    audit.require(compact_manifest(a) == expected, 'author manifest mismatch')
    print(json.dumps({'status': result['status'], 'arrays_compared_entrywise': keys,
                      'author_implementations_agree': True}, sort_keys=True))


if __name__ == '__main__':
    main()
