#!/usr/bin/env python3
"""Complete replay: native literal domains, both Python modes, and controls."""
import argparse
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path


def main():
    p=argparse.ArgumentParser();p.add_argument('out',type=Path);p.add_argument('--sanitizers',action='store_true')
    args=p.parse_args();here=Path(__file__).resolve().parent
    manifest=json.loads((here/'MANIFEST.json').read_text())
    files={x.name for x in here.iterdir() if x.is_file() and x.name!='MANIFEST.json'}
    if files!=set(manifest):raise ValueError('package file set mismatch')
    for name,rec in manifest.items():
        data=(here/name).read_bytes()
        if len(data)!=rec['bytes'] or hashlib.sha256(data).hexdigest()!=rec['sha256']:
            raise ValueError('source checksum: '+name)
    args.out.mkdir(parents=True,exist_ok=False)
    def run(cmd,name):
        r=subprocess.run(list(map(str,cmd)),capture_output=True,text=True,check=True)
        (args.out/(name+'.stdout')).write_text(r.stdout)
        (args.out/(name+'.stderr')).write_text(r.stderr)
        return r.stdout
    binary=args.out/'native_domains';native=args.out/'native.json'
    run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Werror',here/'native_domains.cpp','-o',binary],'compile')
    run([binary,native],'native')
    if args.sanitizers:
        san=args.out/'native_sanitized';san_json=args.out/'native-sanitized.json'
        run(['g++','-std=c++17','-O1','-g','-fsanitize=undefined,bounds','-fno-sanitize-recover=all',
             here/'native_domains.cpp','-o',san],'compile-sanitized')
        run([san,san_json],'native-sanitized')
        if native.read_bytes()!=san_json.read_bytes():raise ValueError('native sanitizer result differs')
    expected=json.loads((here/'EXPECTED.json').read_text());audits=[];controls=[];rejections=0
    for options,tag in (([],'normal'),(['-O'],'optimized')):
        base=[sys.executable,*options,'-B'];result=args.out/(tag+'-result.json');audit=args.out/(tag+'-audit.json')
        run([*base,here/'engine.py',result],tag+'-engine')
        if json.loads(result.read_text())!=expected:raise ValueError('marginal replay differs')
        run([*base,here/'independent_check.py',here,native,'--out',audit],tag+'-audit')
        audits.append(json.loads(audit.read_text()))
        controls.append(json.loads(run([*base,here/'controls.py'],tag+'-controls')))
        for mutation in ('marginal','sorted_transfer'):
            altered=copy.deepcopy(expected)
            if mutation=='marginal':
                altered['classes'][0]['blocks'][0]['choices'][0]['accepted']+=1
            else:
                altered['ordered_transfer']['classes'][0]['sorted_fraction_bound']['numerator']=0
            package=args.out/(tag+'-corrupt-'+mutation);package.mkdir()
            for name in ('DOMAIN_PINS.json','CARRIER_PINS.json','SUMMARY.json'):
                (package/name).write_bytes((here/name).read_bytes())
            (package/'EXPECTED.json').write_text(json.dumps(altered))
            failed=subprocess.run([*base,str(here/'independent_check.py'),str(package),str(native),
                                   '--out',str(package/'should-not-exist.json')],capture_output=True,text=True)
            (package/'rejection.stderr').write_text(failed.stderr)
            if failed.returncode==0 or 'ValueError' not in failed.stderr:
                raise ValueError('numeric corruption was not rejected as expected')
            rejections+=1
    if audits[0]!=audits[1] or controls[0]!=controls[1]:raise ValueError('Python modes differ')
    receipt={'status':'REPRODUCED_CURRENT_Q8_CARRIER_REDUCTION','current_h3887_q8_factor16':True,
             'aggregate_fraction_below':'681/12500','aggregate_reduction_more_than18':True,
             'normal_and_optimized':True,'sanitizers':args.sanitizers,'solver_calls':0,
             'numeric_corruptions_rejected':rejections,
             'independent_audit':audits[0],'controls':controls[0]}
    (args.out/'RECEIPT.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if k not in ('independent_audit','controls')},sort_keys=True))


if __name__=='__main__':main()
