"""Strict source seals and whole typed-record verification; works under -O."""
from pathlib import Path
import argparse
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
DAMAGES = ('wrong_root_second_coefficient','wrong_projection_mixed_sign',
           'too_large_lower_secant','wrong_endpoint','wrong_reciprocal_power',
           'wrong_actual_anchor')


def unique_object(pairs):
    out = {}
    for k,v in pairs:
        if k in out:
            raise ValueError('Duplicate JSON key')
        out[k] = v
    return out


def read_json(path):
    return json.loads(path.read_text(),object_pairs_hook=unique_object)


def canonical(value):
    return (json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--expected',type=Path,default=ROOT/'EXPECTED.json')
    parser.add_argument('--damage',choices=DAMAGES)
    parser.add_argument('--record',action='store_true')
    args = parser.parse_args()
    manifest = read_json(ROOT/'MANIFEST.json')
    required = {'exact.py','audit.py','verify.py','controls.py','EXPECTED.json','PROOF.md'}
    if set(manifest['core_files']) != required:
        raise ValueError('Core source seal census mismatch')
    for n,want in manifest['core_files'].items():
        data = (ROOT/n).read_bytes()
        if len(data)!=want['bytes'] or hashlib.sha256(data).hexdigest()!=want['sha256']:
            raise ValueError('Core source seal mismatch: '+n)
    from audit import run
    record = run(args.damage)
    actual = canonical(record)
    expected = canonical(read_json(args.expected))
    if actual != expected:
        raise ValueError('Entire typed mathematical record mismatch')
    digest = hashlib.sha256(actual).hexdigest()
    if digest != manifest['canonical_record_sha256']:
        raise ValueError('Canonical record seal mismatch')
    if args.record:
        sys.stdout.buffer.write(actual)
    else:
        print('PASS: entire independent moving-budget record; '+str(len(actual))+' bytes; SHA256 '+digest)


if __name__=='__main__':
    main()
