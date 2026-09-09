"""Replay all certificates and formula audits; never rerun the solver."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
import urllib.request
from encode import catalogue, dimacs, formula, require, PAIRS
from verify import FIELDS

HERE=Path(__file__).resolve().parent

def run(command,log,success=True):
    p=subprocess.run(list(map(str,command)),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    log.write_bytes(p.stdout+p.stderr)
    require((p.returncode==0)==success,'unexpected command result: '+str(command))
    return p

def ledger(path,rows):
    with path.open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=FIELDS,delimiter='\t',lineterminator='\n')
        writer.writeheader();writer.writerows(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--data',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--fetch',action='store_true')
    args=ap.parse_args()
    require(not args.out.exists(),'output already exists')
    args.out.mkdir(parents=True)
    begin=time.monotonic()
    if not args.data.exists():
        require(args.fetch,'missing catalogue; supply --fetch')
        spec=json.loads((HERE/'INPUT.json').read_text())
        data=urllib.request.urlopen(spec['url'],timeout=30).read()
        require(hashlib.sha256(data).hexdigest()==spec['sha256'],'download hash')
        args.data.parent.mkdir(parents=True,exist_ok=True);args.data.write_bytes(data)
    cores=catalogue(args.data)
    expected=json.loads((HERE/'EXPECTED.json').read_text())
    with (HERE/'LEDGER.tsv').open() as f: rows=list(csv.DictReader(f,delimiter='\t'))
    require(len(rows)==362,'complete ledger')
    # Both Python modes check every literal certificate, including labels.
    for suffix,flags in [('normal',[]),('optimized',['-O'])]:
        p=run([sys.executable,*flags,'-B',HERE/'verify.py','--data',args.data],args.out/('python-'+suffix+'.json'))
        require(json.loads(p.stdout)==expected['certificate_check'],'certificate summary mismatch')
    models=args.out/'WITNESSES.tsv'
    models.write_text(''.join(r['index']+'\t'+r['residual_edgeword']+'\n' for r in rows))
    cnfs=args.out/'cases';cnfs.mkdir();total=0
    for i,core in enumerate(cores):
        clauses=formula(core)[2];data=dimacs(clauses);d=cnfs/f'{i:06d}';d.mkdir();(d/'input.cnf').write_bytes(data)
        require(str(len(clauses))==rows[i]['clauses'],'formula clause count')
        require(hashlib.sha256(data).hexdigest()==rows[i]['cnf_sha256'],'formula hash')
        total+=len(clauses)
    require(total==9603776,'all formula clauses')
    release=args.out/'check';san=args.out/'check-san'
    run(['g++','-std=c++17','-O3','-Wall','-Wextra','-Werror',HERE/'check.cpp','-o',release],args.out/'compile-release.log')
    run(['g++','-std=c++17','-O1','-g','-fsanitize=address,undefined','-fno-omit-frame-pointer','-fno-pie','-no-pie',HERE/'check.cpp','-o',san],args.out/'compile-san.log')
    p=run([release,args.data,cnfs,models],args.out/'native-full.json')
    require(json.loads(p.stdout)=={'audited_formulas':362,'audited_clauses':9603776,'literal_witnesses':362},'native full audit')
    p=run([san,args.data,'--models',models],args.out/'native-sanitized-models.json')
    require(json.loads(p.stdout)=={'audited_formulas':0,'audited_clauses':0,'literal_witnesses':362},'native sanitized witnesses')
    for i in [0,181,361]:run([san,args.data,cnfs,'--case',i],args.out/f'native-san-formula-{i}.json')
    controls=args.out/'controls';controls.mkdir()
    original=(cnfs/'000000/input.cnf').read_text().splitlines();n=len(original)-1
    clause_controls={
      'missing_clause':[f'p cnf 208 {n-1}']+original[2:],
      'duplicate_clause':[f'p cnf 208 {n+1}']+original[1:]+[original[1]],
      'mixed_color':original[:1]+[' '.join([str(-int(original[1].split()[0]))]+original[1].split()[1:])]+original[2:],
      'bad_variable':[f'p cnf 207 {n}']+original[1:],
      'extra_payload':original+['1 0'],
      'truncated_clause':original[:-1]+[original[-1][:-2]],
      'out_of_range':original[:1]+['209 0']+original[2:]}
    for name,lines in clause_controls.items():
        d=controls/name;(d/'000000').mkdir(parents=True);(d/'000000/input.cnf').write_text('\n'.join(lines)+'\n')
        p=run([san,args.data,d,'--case',0],d/'check.log',False)
        require(b'REJECT:' in p.stderr,'non-validation failure')
    word=int(rows[0]['residual_edgeword'],16)
    red_four=(0,4,8,12);blue_five=(0,4,8,12,16)
    red=word;blue=word
    for i,(u,v) in enumerate(PAIRS):
        if u in red_four and v in red_four:red |= 1<<i
        if u in blue_five and v in blue_five:blue &= ~(1<<i)
    wrong_words={'fixed_edge':f'{word^1:064x}','padding':f'{word|(1<<253):064x}',
                 'red_four':f'{red:064x}','blue_five':f'{blue:064x}'}
    for name,bad in wrong_words.items():
        badrows=[dict(r) for r in rows];badrows[0]['residual_edgeword']=bad
        file=controls/(name+'.tsv');ledger(file,badrows)
        for suffix,flags in [('normal',[]),('optimized',['-O'])]:
            p=run([sys.executable,*flags,'-B',HERE/'verify.py','--data',args.data,'--ledger',file],controls/(name+'-'+suffix+'.log'),False)
            require(b'ValueError' in p.stderr,'unexpected Python rejection')
        file=controls/(name+'-models.tsv');file.write_text(''.join(r['index']+'\t'+r['residual_edgeword']+'\n' for r in badrows))
        p=run([san,args.data,'--models',file],controls/(name+'-native.log'),False)
        require(b'REJECT:' in p.stderr,'unexpected native rejection')
    for name,badrows in [('missing_record',rows[:-1]),('duplicate_record',[rows[0],rows[0],*rows[2:]])]:
        file=controls/(name+'.tsv');ledger(file,badrows)
        for suffix,flags in [('normal',[]),('optimized',['-O'])]:
            run([sys.executable,*flags,'-B',HERE/'verify.py','--data',args.data,'--ledger',file],controls/(name+'-'+suffix+'.log'),False)
        file=controls/(name+'-models.tsv');file.write_text(''.join(r['index']+'\t'+r['residual_edgeword']+'\n' for r in badrows))
        p=run([san,args.data,'--models',file],controls/(name+'-native.log'),False)
        require(b'REJECT:' in p.stderr,'unexpected record rejection')
    result={'certificate_check':expected['certificate_check'],'audited_formulas':362,'audited_clauses':total,
            'sanitized_witnesses':362,'sanitized_positive_formulas':[0,181,361],
            'formula_corruptions_rejected':7,'witness_or_registry_corruptions_rejected_per_checker':6,
            'solvers_run':0}
    require(result==expected,'complete expected result')
    (args.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    (args.out/'TIMING.json').write_text(json.dumps({'seconds':time.monotonic()-begin})+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
