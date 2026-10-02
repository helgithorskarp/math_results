#!/usr/bin/env python3
"""Later unmodified author corroboration, optional and not the independent proof.
Supply a separately obtained pinned directory; every full source hash is checked.
"""
from pathlib import Path
import argparse, hashlib, json, sys
from reproduce import ROOT, child, canonical
from controls import strict, unique

def main():
    p=argparse.ArgumentParser();p.add_argument('--author',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    author=a.author.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=True)
    provenance=json.loads((ROOT/'AUTHOR_SOURCE.json').read_text(),object_pairs_hook=unique)
    for f in provenance['files']:
        data=(author/Path(f['path']).name).read_bytes()
        if len(data)!=f['bytes'] or hashlib.sha256(data).hexdigest()!=f['sha256']:raise RuntimeError('author source hash')
    expected=(author/'EXPECTED.json').read_bytes();target=json.loads(expected,object_pairs_hook=unique);runs={}
    for optimized in (False,True):
        py=[sys.executable]+(['-O']if optimized else []);mode='optimized'if optimized else'normal'
        for name,args in (('rows',['derive.py']),('columns',['verify.py','--emit']),('damage',['verify.py','--damage-controls','EXPECTED.json'])):
            key=mode+'-'+name;runs[key]=child([*py,*args],cwd=author)
            if name!='damage':
                data=runs[key]['stdout'].encode()
                if data!=expected:raise RuntimeError('entire author record differs')
                (out/(key+'.json')).write_bytes(data)
            elif json.loads(runs[key]['stdout'])!={'verified':True,'damages_rejected':14}:raise RuntimeError('author corruption result')
    own=json.loads((ROOT/'RESULTS.json').read_text(),object_pairs_hook=unique)
    decoded=[]
    for f in own['interfaces']:
        columns=[sum(((r>>i)&1)<<t for t,r in enumerate(f['T_rows']))for i in range(6)]+[5,3]
        decoded.append({'low_T1_T2_SY0_SY1':[f['flag']>>j&1 for j in (1,2,3,4)],'T_columns':columns,
                        'SY_cross_OX':f['SY_rows'],'beta':[q-3 for q in f['Q_ranks_X']]})
    key=lambda x:json.dumps(x,sort_keys=True)
    strict(sorted(decoded,key=key),sorted(target['X_interfaces'],key=key))
    for p in target['actual_low_placements']:
        flag=1+sum(l<<j for j,l in zip((1,2,3,4),p['low_T1_T2_SY0_SY1']))
        count=sum(f['flag']==flag for f in own['interfaces'])
        if count!=p['surviving_X_interfaces']:raise RuntimeError('all11 author flag counts')
    result={'complete':True,'author_record_bytes':len(expected),'author_record_sha256':hashlib.sha256(expected).hexdigest(),
            'all_four_emitted_records_equal_expected':True,'all_six_interfaces_and_eleven_flag_survivor_counts_equal':True,
            'methodology':'later unmodified author corroboration; no author premise/code in independent drivers', 'runs':runs}
    (out/'receipt.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k!='runs'}))
if __name__=='__main__':main()
