#!/usr/bin/env python3
"""Optional comparison only; target code is never used by independent replay."""
import argparse
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--author-directory', type=Path, required=True)
    parser.add_argument('--events', type=Path, required=True)
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location('author_two_tail_check',
                                                args.author_directory/'check.py')
    author = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(author)
    original, events = author.event_bytes, []

    def capture(*values):
        row = original(*values)
        events.append(row.decode('ascii').rstrip('\n'))
        return row

    author.event_bytes = capture
    result = author.search(args.author_directory/'weights.json')
    if result != json.loads((args.author_directory/'expected.json').read_text()):
        raise RuntimeError('target production manifest differs')
    independent = json.loads(args.events.read_text())
    if sorted(events) != independent:
        raise RuntimeError('normalized terminal records differ')
    print(json.dumps({'records': len(events), 'every_terminal_record_matches': True,
                      'author_ordered_sha256': result['proof_events_sha256'],
                      'independent_sorted_sha256':
                          sha256(('\n'.join(independent)+'\n').encode()).hexdigest()},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
