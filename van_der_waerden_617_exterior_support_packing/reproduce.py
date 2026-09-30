#!/usr/bin/env python3
"""Single-thread source regeneration, then independent exact verification."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import time

from check import (implications, load_binary, load_supplement, opposed, qr, verify)
from controls import run as rejection_controls

SOURCE=Path(__file__).resolve().parent


def keys():
    for s in range(617):
        for t in range(617):
            for g in (0,1):
                if s!=t or g:
                    yield s,t,g


def compact(result):
    return {k:v for k,v in result.items() if k not in ['seconds','uncovered_phase_keys']}


def compare(actual, expected):
    actual=json.loads(json.dumps(actual))
    for key,value in expected.items():
        if actual.get(key)!=value:
            raise ValueError('expected field differs: '+key)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--workdir',type=Path,required=True)
    parser.add_argument('--record-expected',action='store_true',help='development only: create absent expected.json after successful exact checking')
    args=parser.parse_args();out=args.workdir.resolve()
    if out.is_relative_to(SOURCE):parser.error('keep generated state outside source directory')
    expected_path=SOURCE/'expected.json'
    if args.record_expected and expected_path.exists():parser.error('refusing to replace existing expected evidence')
    if not args.record_expected and not expected_path.is_file():parser.error('missing expected.json')
    out.mkdir(parents=True,exist_ok=True);env=os.environ.copy()
    for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:env[name]='1'
    flags=['-std=c++17','-O2','-Wall','-Wextra','-Wpedantic','-Wconversion','-Wshadow']
    start=time.monotonic();compiler=os.environ.get('CXX','g++')
    for name in ['first','second','implications']:
        subprocess.run([compiler,*flags,str(SOURCE/f'generate_{name}.cpp'),'-o',str(out/f'generate_{name}')],check=True,env=env)
    generation={}
    def generate(name,arguments):
        r=subprocess.run([str(out/f'generate_{name}'),*map(str,arguments)],check=True,text=True,capture_output=True,env=env)
        d=json.loads(r.stdout);(out/f'generation_{name}.json').write_text(json.dumps(d,indent=2)+'\n');generation[name]=d
        return d
    first,second=out/'first.bin',out/'second.bin'
    if not first.exists():generate('first',[565,first])
    stars=SOURCE/'first_stars.json';q=qr();seeds=load_supplement(stars,'QR617_AP_IMPLICATIONS_V1')
    lines=[]
    for key,r in sorted(seeds.items()):
        support=sorted(implications(r,key,q));lines.append(' '.join(map(str,[*key,len(support),*support])))
    star_supports=out/'first_star_supports.txt';star_supports.write_text('\n'.join(lines)+'\n')
    if not second.exists():generate('second',[first,star_supports,second,90])
    _,it1=load_binary(first,b'QRD617P1');_,it2=load_binary(second,b'QRD617P2');lines=[]
    holes=set()
    for key,a,b in zip(keys(),it1,it2,strict=True):
        if b!=(0,0,0):continue
        support=sorted(implications(seeds[key],key,q) if a==(0,0,0) else opposed(a,key,q))
        holes.add(key);lines.append(' '.join(map(str,[*key,len(support),*support])))
    unit_input=out/'residual_input.txt';unit_input.write_text('\n'.join(lines)+'\n')
    proofs=out/'implication_proofs';g=generate('implications',[unit_input,proofs,90,0])
    if g['pending'] or g['not_refuted']:raise ValueError('Incomplete implication generation: no uniform mathematical claim')
    records=[]
    for file in proofs.glob('proof-*.json'):
        r=json.loads(file.read_text())
        if r['status']!='UNIT_CONTRADICTION_CERTIFICATE':raise ValueError('Unrefuted proof input')
        records.append({k:r[k] for k in ['key','steps','final_ap']})
    records.sort(key=lambda r:r['key'])
    if len(records)!=len(holes) or {tuple(r['key']) for r in records}!=holes:raise ValueError('Missing, duplicate or surplus residual proofs')
    supplement=out/'second_implications.json'
    supplement.write_text(json.dumps({'format':'QR617_SECOND_SUPPORT_IMPLICATIONS_V1','length':3704,'half_width':565,'records':records},separators=(',',':'))+'\n')
    result=verify(first,second,stars,supplement)
    controls=rejection_controls(first,second,stars,supplement,out)
    hashes={name:hashlib.sha256(file.read_bytes()).hexdigest() for name,file in [('first',first),('second',second),('second_implications',supplement),('first_stars',stars)]}
    evidence={'verification':compact(result),'hashes':hashes,'controls':controls}
    if args.record_expected:expected_path.write_text(json.dumps(evidence,indent=2)+'\n')
    else:
        expected=json.loads(expected_path.read_text())
        for key in expected:compare(evidence[key],expected[key])
    output={'agent':'six-vdw-3','role':'researcher','status':'VERIFIED_ALL_EXTERIOR_SUPPORT_CLAIMS',
            **evidence,'generation':generation,'seconds':time.monotonic()-start,
            'child_peak_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
            'checker_peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    (out/'reproduction.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'status':output['status'],'phase_cases_checked':result['two_disjoint_supports_checked'],
                      'exterior_edits_required':2,'geographic_profile':[18,2],
                      'second_opposed_pairs':result['second_opposed_pairs_checked'],
                      'second_implications':result['second_implication_proofs_checked'],
                      'corruption_rejections':controls['rejections_checked'],'seconds':output['seconds'],
                      'child_peak_rss_kib':output['child_peak_rss_kib'],'checker_peak_rss_kib':output['checker_peak_rss_kib']},indent=2))


if __name__=='__main__':main()
