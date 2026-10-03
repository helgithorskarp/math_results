#!/usr/bin/env python3
"""Late native comparison, explicitly outside the sealed primary derivation."""
import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import time
import audit as A

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod

def mask(s):return sum(1<<i for i in s)

def run(native):
    start=time.monotonic()
    here=Path(__file__).resolve().parent
    seals=json.loads((here/'PRIMARY_SEAL.json').read_text())
    for f,rec in seals['files'].items():
        b=(here/f).read_bytes()
        A.require(len(b)==rec['bytes'] and hashlib.sha256(b).hexdigest()==rec['sha256'],
                  'primary seal unchanged')
    pins=json.loads((here/'NATIVE_INPUTS.json').read_text())
    for f in pins['files']:
        b=(native/Path(f['path']).name).read_bytes()
        A.require(len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'],
                  'all ten immutable native inputs')
    literal=load(native/'literal.py','target_literal')
    rules=load(native/'rules.py','target_rules')
    native_record=json.loads((native/'RESULTS.json').read_text())
    own=json.loads((here/'PRIMARY.json').read_text())
    expected_covers={mask(s) for s in A.COVERS}
    A.require(expected_covers==set(native_record['whole_C6_covers']), 'entire cover domain')
    A.require({63^w for w in expected_covers}==set(native_record['whole_independent_missing_sets']),
              'entire missing-set domain')
    A.require({mask(s) for s in own['T_cover']['classes'][0]}==set(native_record['T0_path_cover_rows']) and
              {mask(s) for s in own['T_cover']['classes'][1]}==set(native_record['T1_path_cover_rows']),
              'both whole T classes')
    A.require({tuple(map(mask,p)) for p in own['T_cover']['pairs']}==
              {tuple(p) for p in native_record['whole_T_pairs']},'all T pairs')
    A.require({tuple(map(mask,p)) for p in own['SY_final']['all_eight']}==
              {tuple(p) for p in native_record['whole_eight_SY_cases']},'all eight SY cases')
    A.require({mask(s) for s in own['SY_classes']['SY0']}==set(native_record['SY0_six_covers']) and
              {mask(s) for s in own['SY_classes']['SY1']}==set(native_record['SY1_three_covers']),
              'both whole SY classes')
    expected_terminal={tuple(map(mask,p)) for p in own['SY_final']['terminal']}
    A.require(expected_terminal=={tuple(p) for p in native_record['terminal_SY_rows']},
              'entire terminal SY domain')
    image=hashlib.sha256();count=0;spines=0;imagebytes=0
    for r in (0,1):
        for a,d in ((A.P,A.S),(A.S,A.P),(A.H,A.K)):
            if r and (a,d)==(A.H,A.K):a,d=A.K,A.H
            for u,v in itertools.product(A.COVERS,repeat=2):
                rr=A.rows(u,v,a,d);g=A.core(r,rr)
                twords=(mask(a),mask(d),mask(A.C));swords=(mask(u),mask(v))
                nr,nd,nq=literal.build(r,twords,swords)
                br,bd,bq=rules.build(r,twords,swords)
                native_adj={n:{A.NAMES[j] for j in nr[i]} for i,n in enumerate(A.NAMES)}
                A.require(native_adj==g[0] and dict(zip(A.NAMES,nd))==g[1] and
                          dict(zip(A.NAMES,nq))==g[2], 'all original adjacency/degrees/Q ranks')
                A.require(tuple(sum(1<<j for j in ss) for ss in nr)==br and nd==bd and nq==bq,
                          'second native core encoding')
                lc=literal.allowances(nr,nd);rc=rules.allowances(br,bd)
                physical=[]
                for i,j in itertools.combinations(range(16),2):
                    s=A.spine(g,A.NAMES[i],A.NAMES[j])
                    A.require(s['allowance']==lc[i,j]==rc[i,j], 'every colored allowance')
                    A.require(s['pages']==sorted(A.NAMES[k] for k in nr[i]&nr[j]),
                              'every complete physical page list')
                    physical.append(s);spines+=1
                b=A.encode([r,[sorted(rr[e]) for e in A.END],physical])+b'\n'
                image.update(b);imagebytes+=len(b);count+=1
    A.require(count==1944 and spines==233280, 'full stated late domain complete')
    terminal=[]
    for r,t,sy in native_record['terminal_cores']:
        terminal.append([r,t,sy])
    independently_terminal=[[r,[mask(A.H),mask(A.K),mask(A.C)] if r==0 else
                            [mask(A.K),mask(A.H),mask(A.C)],list(sy)]
                           for r in (0,1) for sy in sorted(expected_terminal)]
    A.require(sorted(terminal)==sorted(independently_terminal), 'all four dependency inputs')
    A.require(time.monotonic()-start<30,'late thirty-second guard')
    return {'agent':'six-reviewer-2','role':'independent mathematical reviewer',
            'exposure':'late after unchanged primary seal; no native data establishes primary proof',
            'native_commit':pins['commit'],'all_native_files_pinned':len(pins['files']),
            'original_core_records':count,'entire_physical_spines':spines,
            'whole_original_image_bytes':imagebytes,'whole_original_image_sha256':image.hexdigest(),
            'native_record_bytes':(native/'RESULTS.json').stat().st_size,
            'native_record_sha256':hashlib.sha256((native/'RESULTS.json').read_bytes()).hexdigest(),
            'complete_semantic_domains_match':True,'all_four_dependency_inputs_match':True,
            'all_primary_seals_unchanged':True}

def main():
    p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--check',type=Path)
    args=p.parse_args();data=A.encode(run(args.native))
    if args.check:A.require(A.encode(json.loads(args.check.read_text()))==data,'whole late record mismatch')
    args.output.write_bytes(data+b'\n');print(json.dumps({'bytes_without_LF':len(data),'sha256_without_LF':hashlib.sha256(data).hexdigest()}))

if __name__=='__main__':main()
