#!/usr/bin/env python3
"""Cold census, literal comparison, controls and complete native sanitizers.

Run normal and Python -O separately in empty work directories. Each mathematical
child is direct and has a fixed 60-second guard; no nested timeout wrapper.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
from reproduce import ROOT, canonical, require, stage, summarize

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--author-full',type=Path,required=True);a=ap.parse_args()
    out=a.out.resolve();out.mkdir(parents=True,exist_ok=True)
    expected=json.loads((ROOT/'RESULTS.json').read_text());runs={}
    def execute(name,argv):
        r=stage(argv,ROOT);runs[name]={k:v for k,v in r.items() if k!='stdout'}
        (out/(name+'-stdout.txt')).write_text(r['stdout'])
        return r['stdout']
    execute('build',['g++','-std=c++17','-O2','-Wall','-Wextra','-Wpedantic',str(ROOT/'census.cpp'),'-o',str(out/'native')])
    execute('native',[str(out/'native'),str(out/'census')])
    summary=summarize(out/'census');require(canonical(summary)==canonical(expected),'fresh complete native summary mismatch')
    mode=['-O'] if sys.flags.optimize else []
    execute('literal-comparison',[sys.executable,*mode,str(ROOT/'compare.py'),'--independent',str(out/'census-full.json'),
                                 '--author',str(a.author_full.resolve()),'--out',str(out/'comparison.json')])
    execute('controls',[sys.executable,*mode,str(ROOT/'controls.py'),'--full',str(out/'census-full.json'),'--out',str(out/'controls.json')])
    execute('sanitizer-build',['g++','-std=c++17','-O1','-g','-Wall','-Wextra','-Wpedantic',
                              '-fsanitize=address,undefined','-fno-omit-frame-pointer',str(ROOT/'census.cpp'),'-o',str(out/'sanitized')])
    execute('sanitizer-whole',[str(out/'sanitized'),str(out/'sanitized')])
    sanitized=summarize(out/'sanitized');require(canonical(sanitized)==canonical(expected),'whole sanitizer census differs')
    for name in ['x','frames','joins','meta','full']:
        extension='json' if name=='full' else 'txt'
        require((out/('census-'+name+'.'+extension)).read_bytes()==(out/('sanitized-'+name+'.'+extension)).read_bytes(),
                'whole native stream sanitizer mismatch '+name)
    seal=json.loads((ROOT/'first-seal.json').read_text())
    for name,sha in seal['core_sha256'].items():
        require(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha,'sealed core mutated')
    math={'summary':summary,'comparison':json.loads((out/'comparison.json').read_text()),
          'controls':json.loads((out/'controls.json').read_text()),'whole_native_sanitizers_equal':True,
          'sealed_core_unchanged':True}
    (out/'mathematics.json').write_bytes(canonical(math))
    evidence={'complete':True,'python_optimized':bool(sys.flags.optimize),'guard_seconds_per_direct_child':60,
              'one_intensive_child_at_a_time':True,'mathematics_sha256':hashlib.sha256(canonical(math)).hexdigest(),
              'runs':runs}
    (out/'evidence.json').write_bytes(canonical(evidence));print(json.dumps(evidence,indent=2))

if __name__=='__main__':main()
