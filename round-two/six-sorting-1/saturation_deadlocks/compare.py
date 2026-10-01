#!/usr/bin/env python3
"""Independent complete seven-family comparisons for the four literal prefixes.

The small standalone verify.py suffices for their mathematical exclusions.
This slower optional replay verifies that all seven specified scalar potential
tests pass before the event/activity argument is applied. It uses the pinned
published scalar implementation, not the producer or construction engine.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import time

ROOT=Path(__file__).resolve().parent
PIN='62942073dd9b335f71e3ad2e55fd18d5cd9831f668ff8dc734de0a86fec33c29'

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scalar-module',type=Path,default=ROOT.parent.parent/'six-sorting-2/native24-kernel-cover/verify.py')
    args=parser.parse_args();start=time.monotonic()
    if hashlib.sha256(args.scalar_module.read_bytes()).hexdigest()!=PIN:
        raise ValueError('published scalar dependency changed')
    spec=importlib.util.spec_from_file_location('independent_clamped_scalar',args.scalar_module)
    v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
    fixture=json.loads((ROOT/'fixture.json').read_text())
    certificate=json.loads((ROOT/'certificate.json').read_text())
    base_prefix=fixture['cases'][0]['prefix'][:24]
    v.need(all(case['prefix'][:24]==base_prefix for case in fixture['cases']),'base prefixes differ')
    families=list(v.FAMILIES)+[('three_minima_one_maximum',3,1),('four_maxima',0,4)]
    anchor_rows=[]
    for name,lo,hi in families:
        originals=v.clamped_family(base_prefix,lo,hi)
        for case,claimed in zip(fixture['cases'],certificate['cases']):
            v.need(v.sha(case['prefix'])==claimed['prefix_sha256'],'literal prefix changed')
            members=v.extend(originals,case['prefix'][24:],24)
            actual=v.family_summary(members,lo,hi)
            actual['semantic_cost_sum']=sum(row[4]+row[5] for row,_ in members)
            v.need(actual==claimed['comparison_profiles'][name],'complete scalar profile differs')
            allowance=5 if lo+hi==1 else 9 if lo+hi==2 else 19
            v.need(actual['summary']['semantic_mass']<=1<<allowance,'standalone potential rejects fixture')
        print('COMPLETE_FAMILY_COMPARED',name,len(originals),flush=True)
    for claimed in certificate['cases']:
        profiles=claimed['comparison_profiles'];anchors={}
        for side,unary,paired,index in [('low','one_minimum','two_minima',0),('high','one_maximum','two_maxima',1)]:
            total=0
            for row in profiles[unary]['envelope']:
                port=row[index];units=(1<<row[3])*16
                for family in [paired,'mixed_pair']:
                    mass=sum(1<<r[3] for r in profiles[family]['envelope'] if r[index]&port)
                    units=max(units,1<<(mass-1).bit_length())
                total+=units
            anchors[side]=total
            v.need(total<=512,'old anchor rejects fixture')
        anchor_rows.append({'kernel_id':claimed['kernel_id'],'anchors':anchors,
                            'four_high_mass':profiles['four_maxima']['summary']['semantic_mass']})
    print(json.dumps({'agent':'six-sorting-1','role':'researcher',
                      'status':'ALL_SEVEN_COMPLETE_COMPARISON_PROFILES_PASSED',
                      'scalar_dependency_agent':'six-sorting-2','scalar_dependency_sha256':PIN,
                      'cases':4,'families':7,'anchors':anchor_rows,
                      'seconds':time.monotonic()-start,
                      'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      **v.METRICS},sort_keys=True))

if __name__=='__main__':main()
