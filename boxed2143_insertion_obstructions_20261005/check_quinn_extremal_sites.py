#!/usr/bin/env python3
"""Independent rectangle replay of the later constant-eight-site packet."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import platform
import time

from rectangle_checker import boxed_occurrences

AUTHOR = Path(__file__).resolve().parent


def child(p, gap, kind):
    if kind == 'maximum':
        return p[:gap] + (len(p)+1,) + p[gap:]
    if kind == 'minimum':
        shifted = tuple(x+1 for x in p)
        return shifted[:gap] + (1,) + shifted[gap:]
    raise ValueError('Unrecognized extremum')


def sites(p, kind):
    return tuple(g for g in range(len(p)+1) if not boxed_occurrences(child(p, g, kind)))


def run():
    started = time.perf_counter()
    manifest_path = AUTHOR/'SOURCE_MANIFEST.json'
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    for name, rec in manifest['files'].items():
        data = (AUTHOR/name).read_bytes()
        if hashlib.sha256(data).hexdigest() != rec['sha256'] or len(data) != rec['bytes']:
            raise RuntimeError('Manifest mismatch: '+name)
    certificate = json.loads((AUTHOR/'extremal_site_definition_certificate.json').read_text())
    p = tuple(certificate['parent'])
    if boxed_occurrences(p):
        raise RuntimeError('Certificate parent does not avoid')
    for row in certificate['children']:
        rebuilt = child(p, row['gap'], row['kind'])
        if rebuilt != tuple(row['child']) or boxed_occurrences(rebuilt) != tuple(tuple(o) for o in row['complete_occurrences']):
            raise RuntimeError('Certificate mismatch: '+str(row))
    family = []
    instances = 0
    for n in range(4, 17):
        p = (1,) + tuple(range(n-1, 1, -1)) + (n,)
        if boxed_occurrences(p):
            raise RuntimeError('Family parent fails avoidance')
        if p != tuple(n+1-x for x in reversed(p)):
            raise RuntimeError('Family fails reverse-complement invariance')
        maximum = sites(p, 'maximum')
        minimum = sites(p, 'minimum')
        if maximum != (0, 1, 2, n) or minimum != (0, n-2, n-1, n):
            raise RuntimeError('Family exact gap sets fail at '+str(n))
        for g in range(n+1):
            max_child = child(p, n-g, 'maximum')
            reflected = tuple(n+2-x for x in reversed(max_child))
            if reflected != child(p, g, 'minimum'):
                raise RuntimeError('Child symmetry identity fails')
            instances += 2
        for g in range(3, n):
            if (1, 2, g, n) not in boxed_occurrences(child(p, g, 'maximum')):
                raise RuntimeError('Explicit forbidden-gap witness fails')
        family.append({'n': n, 'maximum_sites': maximum, 'minimum_sites': minimum})
    minima = []
    checked = 0
    for n in range(7):
        best = 2*(n+1)
        for p in itertools.permutations(range(1, n+1)):
            if boxed_occurrences(p):
                continue
            checked += 1
            total = len(sites(p, 'maximum'))+len(sites(p, 'minimum'))
            best = min(best, total)
            if total < n+2:
                raise RuntimeError('Earlier-length n+2 failure found: '+str(p))
        minima.append({'n': n, 'minimum_total_sites': best})
    for name, rec in manifest['files'].items():
        if hashlib.sha256((AUTHOR/name).read_bytes()).hexdigest() != rec['sha256']:
            raise RuntimeError('Source changed during review')
    if manifest_path.read_bytes() != manifest_bytes:
        raise RuntimeError('Manifest changed during review')
    return {
        'reviewer':'literature-researcher-4', 'author':'literature-researcher-3',
        'decision_message_id':410, 'full_growth_target_solved':False,
        'status':'independent finite replay passed; arbitrary-n proof reviewed separately',
        'author_manifest_sha256':hashlib.sha256(manifest_bytes).hexdigest(),
        'author_file_sha256':{n:r['sha256'] for n,r in manifest['files'].items()},
        'certificate_children_compared':len(certificate['children']),
        'family_scope_n':[4,16], 'family_extremal_instances':instances,
        'family_gap_sets':family, 'smaller_avoiders_exhausted':checked,
        'smaller_length_minima':minima,
        'minimal_failure_length':7, 'lexicographic_minimality_at_7_checked':False,
        'python':platform.python_version(), 'seconds':time.perf_counter()-started,
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=run()
    rendered=json.dumps(result,indent=2)+'\n'
    if args.output:
        args.output.write_text(rendered)
    print(rendered,end='')


if __name__=='__main__':
    main()
