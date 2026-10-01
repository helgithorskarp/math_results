#!/usr/bin/env python3
"""Reconstruct independent phase and quartic evidence; compare the full frozen record."""
import argparse
import json
from pathlib import Path
import resource
import signal
import sys
import time


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--vendor',type=Path,help='Optional directory containing pinned SymPy1.14.0 and mpmath1.3.0')
    parser.add_argument('--expected',type=Path,default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--record',type=Path,help='Optional private full record output')
    parser.add_argument('--author-expected',type=Path,help='Optional corroboration of complete author coefficient lists')
    args=parser.parse_args()
    signal.alarm(90)
    if args.vendor:sys.path.insert(0,str(args.vendor.resolve()))
    sys.path.insert(0,str(Path(__file__).resolve().parent))
    import sympy
    from derive import derive,need,canonical,digest
    need(sympy.__version__=='1.14.0','unpinned SymPy version')
    start=time.monotonic();result=derive()
    if args.record:args.record.write_bytes(canonical(result)+b'\n')
    expected=json.loads(args.expected.read_text())
    need(canonical(result)==canonical(expected),'complete frozen independent record mismatch')
    controls=[]
    for label in ['omitted-entry','wrong-quartic','missing-bound','noncanonical-type']:
        bad=json.loads(canonical(expected))
        if label=='omitted-entry':bad['full_phase_matrix'][0].pop()
        elif label=='wrong-quartic':bad['quartic']['pair_P9'][0]='0'
        elif label=='missing-bound':bad['bounds'].pop('H_le_one')
        else:bad['bernstein_count']=float(bad['bernstein_count'])
        need(canonical(bad)!=canonical(result),'damaged fixture accepted')
        controls.append(label)
    comparisons=0
    if args.author_expected:
        author=json.loads(args.author_expected.read_text())
        for key in ['polynomials','modulus_determinant','threshold','bounds','bernstein_count']:
            need(canonical(author[key])==canonical(result[key]),'author whole coefficient mismatch '+key)
            comparisons+=1
        need({k:list(map(str,v)) for k,v in author['a_polynomials'].items()}==result['a_polynomials'],
             'author all a coefficients mismatch');comparisons+=1
    print(json.dumps({'status':'PASS','record_sha256':digest(result),'full_matrix_entries':64,
        'whole_interval_original_coefficients':result['bernstein_count'],
        'threshold_quartic_negative_coefficients':len(result['quartic']['negative_P9']['bernstein']),
        'mathematical_damage_rejections':len(result['mathematical_damage_rejections']),
        'fixture_damage_rejections':controls,'whole_author_record_fields_compared':comparisons,
        'seconds':time.monotonic()-start,'rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},sort_keys=True))


if __name__=='__main__':
    try:main()
    except (ValueError,OSError,TypeError,KeyError,json.JSONDecodeError) as error:
        print('FAIL: '+str(error),file=sys.stderr);raise SystemExit(1)
