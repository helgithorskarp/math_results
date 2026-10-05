"""Integrity-only source publication check; does not run mathematical children."""
import hashlib
import json
from pathlib import Path
import sys


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def check(root):
    root = Path(root)
    declared = {}
    for line in (root / 'MANIFEST.sha256').read_text().splitlines():
        sha, name = line.split('  ', 1)
        need(len(sha) == 64 and all(c in '0123456789abcdef' for c in sha), 'digest syntax')
        need(name not in declared and '/' not in name and name != 'MANIFEST.sha256', 'sealed file paths')
        data = (root / name).read_bytes()
        need(digest(data) == sha, 'whole public source seal: ' + name)
        declared[name] = sha
    need({p.name for p in root.iterdir()} == set(declared) | {'MANIFEST.sha256'}, 'entire public file census')
    expected = {'.gitignore', 'check.py', 'validate.py', 'PROOF.md', 'REVIEW.md',
                'README.md', 'RECORD.json', 'SOURCE.json', 'EDITORIAL.json',
                'VALIDATION.json', 'SHA256SUMS', 'publish_check.py'}
    need(set(declared) == expected, 'exact intended compact publication')
    editorial = json.loads((root / 'EDITORIAL.json').read_text())
    baseline = editorial['baseline']
    need({r['name'] for r in baseline} == {'check.py', 'validate.py', 'PROOF.md',
                                          'REVIEW.md', 'README.md', 'RECORD.json', 'SOURCE.json'},
         'private baseline census')
    need(editorial['unchanged'] == ['check.py', 'validate.py', 'PROOF.md', 'RECORD.json'], 'unchanged mathematics')
    old_manifest = ''
    primary_manifest = ''
    for row in baseline:
        name = row['name']
        actual = (root / name).read_bytes()
        restored = actual
        if name in editorial['changes']:
            text = actual.decode()
            for change in reversed(editorial['changes'][name]):
                need(text.count(change['after']) == 1, 'exact reverse editorial occurrence')
                text = text.replace(change['after'], change['before'])
            restored = text.encode()
        need(len(restored) == row['bytes'] and digest(restored) == row['sha256'],
             'ENTIRE private source restoration: ' + name)
        if name in editorial['unchanged']:
            need(actual == restored, 'no mathematical source edit')
        old_manifest += row['sha256'] + '  ' + name + '\n'
        primary_manifest += digest(actual) + '  ' + name + '\n'
    need(digest(old_manifest.encode()) == editorial['baseline_manifest_sha256'], 'entire old source seal')
    need((root / 'SHA256SUMS').read_bytes() == primary_manifest.encode(), 'complete primary validator seal')
    record = (root / 'RECORD.json').read_bytes()
    validation = json.loads((root / 'VALIDATION.json').read_text())
    need(len(record) == validation['whole_record_bytes'] == 12353, 'entire evidence record length')
    need(digest(record) == validation['whole_record_sha256'] ==
         '3a5346354fdf42c11ec41e8371f0243d589a1094dbbac18cecf7256dabaf6920', 'entire paid evidence record')
    need(validation['positive_replays'] == 4 and validation['semantic_rejection_executions'] == 24
         and validation['preimport_rejections'] == 4, 'paid evidence provenance')
    need('## Strengthening and improvement opportunities' in (root / 'REVIEW.md').read_text(), 'required review section')
    return dict(actual_agent='six-reviewer-5', role='independent mathematical reviewer',
                public_files=len(expected) + 1, whole_record_bytes=len(record), whole_record_sha256=digest(record),
                original_source_manifest_sha256=editorial['baseline_manifest_sha256'],
                entire_private_math_and_record_unchanged=True, entire_editorial_reversal_exact=True,
                closed_math_replays=0)


if __name__ == '__main__':
    need(len(sys.argv) <= 2, 'publication verifier arguments')
    root = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).resolve().parent
    print(json.dumps(check(root), sort_keys=True, indent=2))
