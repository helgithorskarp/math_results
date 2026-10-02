#!/usr/bin/env python3
"""Complete independent census, eight set strata, literal controls and sanitizers.
Every CPU child is serial and directly guarded at60s; generated files stay in --out.
"""
from pathlib import Path
import argparse, hashlib, json, sys
from reproduce import ROOT, child, record, canonical
from controls import strict, unique

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    out=a.out.resolve();out.mkdir(parents=True,exist_ok=True);runs={}
    expected=json.loads((ROOT/'RESULTS.json').read_text(),object_pairs_hook=unique)
    binary=out/'census';prefix=out/'native'
    runs['build']=child(['g++','-std=c++17','-O2','-Wall','-Wextra','-pedantic',ROOT/'census.cpp','-o',binary])
    runs['native']=child([binary,prefix]);native=record(prefix);strict(native,expected)
    (out/'record.json').write_bytes(canonical(native))
    xs=[]
    py=[sys.executable]+(['-O']if not __debug__ else [])
    for tf in range(8):
        dest=out/f'set-{tf}.json'
        runs[f'set-{tf}']=child([*py,ROOT/'audit.py','--tflag',tf,'--out',dest]);xs.append(json.loads(dest.read_text(),object_pairs_hook=unique))
        if not xs[-1]['complete']:raise RuntimeError('incomplete set stratum')
    independent={'complete':True,'counts':[x['T_count']for x in xs]+sorted(sum((x['F_counts']for x in xs),[]),key=lambda r:r[1])+[['complete',sum(len(x['interfaces'])for x in xs)]],
                 'interfaces':sorted(sum((x['interfaces']for x in xs),[]),key=lambda x:json.dumps(x,sort_keys=True))}
    strict(independent,expected);(out/'set-record.json').write_bytes(canonical(independent))
    runs['controls']=child([*py,ROOT/'controls.py',out/'record.json'])
    controls=json.loads(runs['controls']['stdout'],object_pairs_hook=unique)
    san=out/'sanitized';sp=out/'sanitized-record'
    runs['sanitizer-build']=child(['g++','-std=c++17','-O1','-g','-fsanitize=address,undefined','-fno-omit-frame-pointer','-no-pie',ROOT/'census.cpp','-o',san])
    runs['sanitizer-whole']=child([san,sp]);strict(record(sp),expected)
    mathematics={'complete':True,'record_sha256':hashlib.sha256(canonical(native)).hexdigest(),'entire_native_set_sanitizer_records_equal':True,'controls':controls}
    (out/'mathematics.json').write_bytes(canonical(mathematics))
    result={'complete':True,'python_optimized':not __debug__,'guard_seconds_per_direct_child':60,'one_intensive_child_at_a_time':True,'native_threads':1,
            'mathematics_sha256':hashlib.sha256(canonical(mathematics)).hexdigest(),'runs':runs}
    (out/'run.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'complete':True,'python_optimized':not __debug__,'mathematics_sha256':result['mathematics_sha256'],'longest_child_seconds':max(x['seconds']for x in runs.values())}))
if __name__=='__main__':main()
