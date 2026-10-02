#!/usr/bin/env python3
"""Regenerate every finite field; malformed or altered fixtures reject."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from algebra import regenerate_record, reject
from polynomials import digest, require

def same(actual,expected,path='root'):
    require(type(actual) is type(expected),'fixture type: '+path)
    if isinstance(actual,dict):
        require(actual.keys()==expected.keys(),'fixture fields: '+path)
        for k,v in actual.items(): same(v,expected[k],path+'.'+k)
    elif isinstance(actual,list):
        require(len(actual)==len(expected),'fixture list size: '+path)
        for i,v in enumerate(actual): same(v,expected[i],path+'.'+str(i))
    else: require(actual==expected,'fixture value: '+path)

def fixture_controls(r):
    x=deepcopy(r); x['schema']=True
    reject(lambda:same(r,x),'integer replaced by bool')
    x=deepcopy(r); x['bounds']['heavy_B_shift'].pop()
    reject(lambda:same(r,x),'omitted Bernstein coefficient')
    x=deepcopy(r); x['derivative_values']['M4']='1'
    reject(lambda:same(r,x),'changed derivative value')
    x=deepcopy(r); x['slack_denominator']=8
    reject(lambda:same(r,x),'enlarged domain')

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--expected',type=Path,default=Path(__file__).with_name('expected.json'))
    p.add_argument('--write-fixture',type=Path)
    args=p.parse_args()
    r=regenerate_record()
    fixture_controls(r)
    if args.write_fixture:
        args.write_fixture.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    else:
        try: e=json.loads(args.expected.read_text())
        except (OSError,json.JSONDecodeError) as exc: raise ValueError('fixture cannot be read') from exc
        same(r,e)
    print(json.dumps({'status':'PASS','record_sha256':digest(r),
        'rational_caps':30,'bernstein_coefficients':r['bernstein_coefficients'],
        'full_basis_reconstructions':r['full_basis_reconstructions'],
        'derivative_caps':r['derivative_caps'],'controls':{k:r['controls'][k] for k in
            ['whole_primitive_identities','monomial_jets','retained_entries_per_jet','reciprocal_entries']},
        'mathematical_damage_controls':4,'fixture_damage_controls':4},sort_keys=True))

if __name__=='__main__': main()
