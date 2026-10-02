#!/usr/bin/env python3
"""Independent exact joint-functional audit; regenerate the complete frozen record."""
import argparse
import json
from pathlib import Path
import resource
import signal
import sys
import time


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--vendor',type=Path,help='Optional directory with SymPy1.14.0 and mpmath1.3.0')
    p.add_argument('--expected',type=Path,default=Path(__file__).with_name('expected.json'))
    p.add_argument('--author-expected',type=Path,help='Optional original9111 frozen record; no author code import')
    args=p.parse_args();signal.alarm(90)
    if args.vendor:sys.path.insert(0,str(args.vendor.resolve()))
    sys.path.insert(0,str(Path(__file__).resolve().parent))
    from derive import derive,need,canonical,digest
    start=time.monotonic();actual=derive();expected=json.loads(args.expected.read_text())
    def compare(e):need(canonical(e)==canonical(actual),'complete frozen independent record mismatch')
    compare(expected);rejected=[]
    for label in ('missing-polynomial','wrong-weight','omitted-Bernstein-coefficient','changed-phase-bound',
                  'missing-heavy-bound','wrong-boundary','noncanonical-type','extra-field'):
        bad=json.loads(canonical(expected))
        if label=='missing-polynomial':bad['author_polynomials'].pop('joint_cross_numerator')
        elif label=='wrong-weight':bad['mu']='1'
        elif label=='omitted-Bernstein-coefficient':bad['improved_collective_bounds']['determinant']['bernstein'].pop()
        elif label=='changed-phase-bound':bad['proved_constants']['tuple_phase']='1/10'
        elif label=='missing-heavy-bound':bad.pop('heavy_9_8_bound')
        elif label=='wrong-boundary':bad['boundary']['polar_types'][0]='9/8'
        elif label=='noncanonical-type':bad['joint_full_matrix_entries']=64.0
        else:bad['unverified_extra']=True
        try:compare(bad)
        except ValueError:rejected.append(label)
        else:raise ValueError('fixture damage accepted: '+label)
    comparisons={}
    if args.author_expected:
        author=json.loads(args.author_expected.read_text())
        need(canonical(author['polynomials'])==canonical(actual['author_polynomials']),'whole20 original polynomials')
        mapping={'joint_slack_numerator_quotient':'U','joint_transverse_numerator_quotient':'V',
                 'shifted_heavy':'B_h','shifted_collective_determinant':'B_det'}
        for k,v in mapping.items():need(canonical(author['whole_interval_bounds'][k])==canonical(actual['original_bounds'][v]),'whole original interval expansion '+k)
        for k in ('origin','polar'):
            need(author[k+'_phase_identity_count']==64,'complete original directional count')
            need(author[k+'_phase_identity_digest']==actual['directional_hashes'][k],'whole original directional record '+k)
        need(author['fixed_weight']==actual['mu'] and author['cutoff']=='5/8','original weight/cutoff')
        comparisons={'polynomials':20,'interval_expansions':4,'Bernstein_coefficients':85,'directional_records':128}
    print(json.dumps({'status':'PASS','agent':'six-reviewer-1','role':'independent mathematical reviewer',
        'record_sha256':digest(actual),'matrix_entries':128,'full_joint_entries':64,
        'original_Bernstein_coefficients':85,'improved_Bernstein_coefficients':sum(len(z['bernstein']) for z in actual['improved_collective_bounds'].values())+len(actual['heavy_9_8_bound']['bernstein']),
        'mathematical_damage_rejections':len(actual['mathematical_damage_rejections']),
        'fixture_damage_rejections':rejected,'author_comparisons':comparisons,
        'tuple_slack':'3/10','tuple_phase':'1/100','seconds':time.monotonic()-start,
        'rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},sort_keys=True))


if __name__=='__main__':
    try:main()
    except (ValueError,OSError,TypeError,KeyError,json.JSONDecodeError) as error:
        print('FAIL: '+str(error),file=sys.stderr);raise SystemExit(1)
