"""Mathematical corruption, scope and finite-model checks."""
import argparse
import copy
from itertools import combinations,product
import json
from pathlib import Path
import tempfile
import base_verify
import check_core
import check_probe
import compact
import verify

HERE=Path(__file__).absolute().parent


def run():
    rejected=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,TypeError,KeyError,IndexError):rejected.append(name);return
        raise ValueError('Corruption accepted: '+name)

    manifest=json.loads((HERE/'manifest.json').read_text())
    with tempfile.TemporaryDirectory(prefix='vdw617-controls-') as tasktmp:
        temp=Path(tasktmp)
        for row in manifest['cases']:
            base=HERE/row['base'];proof=json.loads((HERE/row['proof']).read_text());s=row['phase']
            def test(data,kind=row['kind'],base=base):
                path=temp/'proof.json';path.write_text(json.dumps(data));return verify.case(base,path,kind)
            if row['kind']=='forcing_core':
                data=copy.deepcopy(proof);data['units'].pop();reject(f'{s}: missing necessary terminal ancestor',lambda d=data:test(d))
                data=copy.deepcopy(proof);data['terminal_AP'][1]=0;reject(f'{s}: constant AP',lambda d=data:test(d))
                data=copy.deepcopy(proof);data['seed'].append(data['seed'][0]);reject(f'{s}: duplicate seed',lambda d=data:test(d))
                data=copy.deepcopy(proof);data['units'][0][3]^=1;reject(f'{s}: reversed implication',lambda d=data:test(d))
                data=copy.deepcopy(proof);data['units'][0][2]=3704;reject(f'{s}: outside actual geometry',lambda d=data:test(d))
            else:
                verify.need(compact.encode(compact.decode(proof))==proof,'Every compact row round-trips entry by entry')
                data=copy.deepcopy(proof);data['caps'][1]=198;reject(f'{s}: hidden opposite cap',lambda d=data:test(d))
                data=copy.deepcopy(proof);data['root']=0;reject(f'{s}: hidden root assumption',lambda d=data:test(d))
                data=copy.deepcopy(proof);data['steps'][-1:]=[];reject(f'{s}: missing required top fact',lambda d=data:test(d))
                first=next(i for i,r in enumerate(proof['steps']) if r[0]==2)
                data=copy.deepcopy(proof);data['steps'][first][3]=[];reject(f'{s}: unproved failed literal',lambda d=data:test(d))
                data=copy.deepcopy(proof);data['steps'][first][4]=None;reject(f'{s}: missing trial contradiction',lambda d=data:test(d))
                data=copy.deepcopy(proof);data['steps'][first][2]^=1;reject(f'{s}: wrong discharged literal',lambda d=data:test(d))
                data=copy.deepcopy(proof);data['steps'][first][3].append([2,0,1,[],[0,0,1]]);reject(f'{s}: unscoped nested trial',lambda d=data:test(d))
                data=copy.deepcopy(proof);data['terminal']=[2,1];reject(f'{s}: unrestricted class terminal',lambda d=data:test(d))
                data=copy.deepcopy(proof);data['steps'][first][0]=True;reject(f'{s}: boolean tag',lambda d=data:test(d))
                data=copy.deepcopy(proof);data['invented_assumption']=[0,0];reject(f'{s}: extra premise',lambda d=data:test(d))
        basepath=HERE/'base/phase-170.json';original=json.loads(basepath.read_text())
        def checkbase(data):
            path=temp/'base.json';path.write_text(json.dumps(data));base_verify.base_premise(path)
        changes=[('wrong N','N',3705),('wrong seam','seam',1853),('wrong prime','P',619),
                 ('wrong terms','terms',6),('wrong orientation','g',0),('wrong reflected phase','t',1),
                 ('nonpositive capacity','denominator',0),('small capacity','denominator',1)]
        for name,key,value in changes:
            data=copy.deepcopy(original);data[key]=value;reject(name,lambda d=data:checkbase(d))
        data=copy.deepcopy(original);data['color0_APs'].append(data['color0_APs'][0]);reject('duplicate weighted AP',lambda:checkbase(data))
        data=copy.deepcopy(original);data['color0_APs'][0][2]=-1;reject('negative AP weight',lambda:checkbase(data))
        data=copy.deepcopy(original);data['color0_APs'][0][1]=0;reject('constant weighted AP',lambda:checkbase(data))
        data=copy.deepcopy(original);data['color0_APs'][0][0]=3704;reject('out-of-range weighted AP',lambda:checkbase(data))

    # Independent exhaustive small nonnegative-defect models for the budget rule.
    budget_models=0;universe=set(range(3))
    for defects in product(range(3),repeat=3):
        for K in range(4):
            for R in range(7):
                for bits in range(8):
                    E={x for x in universe if bits>>x&1}
                    if len(E)>K or sum(defects[x] for x in E)>R:continue
                    for tbits in range(8):
                        T={x for x in universe if tbits>>x&1}
                        if not T<=E:continue
                        spent=sum(defects[x] for x in T)
                        for x in universe-T:
                            if len(T)>=K or defects[x]>R-spent:
                                verify.need(x not in E,'The aggregate budget fixes this unknown point unchanged')
                                budget_models+=1
    # Packing+forcing transfer, including zero loads and nonminimal hitting sets.
    transfer_models=0
    for n in [3,4,5]:
        universe=set(range(n));edges=[set(p) for p in combinations(range(n),2)]
        for edge_count in range(1,min(4,len(edges))+1):
            family=edges[:edge_count]
            for weights in product([1,2],repeat=edge_count):
                loads=[sum(w for A,w in zip(family,weights) if x in A) for x in range(n)]
                D=max(loads);S=sum(weights)
                for hbits in range(1,1<<n):
                    H={x for x in universe if hbits>>x&1};minimum=min(D-loads[x] for x in H)
                    for ebits in range(1,1<<n):
                        E={x for x in universe if ebits>>x&1}
                        if not(E&H) or any(not(E&A) for A in family):continue
                        verify.need(D*len(E)>=S+minimum,'Exact forcing-set defect transfer')
                        transfer_models+=1
    # Actual AP preservation and both count identities, with free pole positions.
    identity_models=0;T=[0,1,-1,0,1,-1,0,1];N=8
    def valid(f):return all(len({f[x] for x in check_core.ap(a,1,N)})>1 for a in [0,1])
    for f in product([0,1],repeat=N):
        if not valid(f):continue
        reflected=[1-f[N-1-x] for x in range(N)];complemented=[1-b for b in f]
        verify.need(valid(reflected) and valid(complemented),'Actual AP-free preservation')
        edits=[sum(T[x]==c and f[x]!=c for x in range(N)) for c in [0,1]]
        opposite=[sum(T[x]==c and reflected[x]!=c for x in range(N)) for c in [0,1]]
        comp=[sum(T[x]==c and complemented[x]!=c for x in range(N)) for c in [0,1]]
        verify.need(opposite==edits[::-1] and comp==[3-k for k in edits],'No candidate symmetry; poles uncounted')
        identity_models+=1
    return {'agent':'six-vdw-3','role':'researcher','status':'ALL_MATHEMATICAL_CONTROLS_PASSED',
            'rejections':len(rejected),'rejected_cases':rejected,'budget_fix_models':budget_models,
            'forcing_transfer_models':transfer_models,'actual_reflection_complement_models':identity_models,
            'compact_rows_compared_entry_by_entry':True}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);a=p.parse_args();result=run()
    if a.output:a.output.write_text(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps(result,sort_keys=True))
