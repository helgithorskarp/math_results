"""Late corroboration. First own normal records predate author-engine inspection.

Scalar records: own reconstructed budgets, leading-determinant ratios, no
researcher engine. Matrix comparison: explicitly imports byte-pinned author
build ONLY for corroboration against already frozen independently ordered
whole Gram/H hashes. This comparison is not a third independent audit.
"""
from pathlib import Path
from itertools import combinations
import argparse,hashlib,importlib.util,json,sys
from linear import F,need,digest,canonical,inverse
from scalars import profile
from check import FIXTURES
ROOT=Path(__file__).resolve().parent

def det(A):
    B=[row[:] for row in A];out=F(1)
    for j in range(len(B)):
        p=next((i for i in range(j,len(B)) if B[i][j]),None)
        if p is None:return F(0)
        if p!=j:B[p],B[j]=B[j],B[p];out=-out
        out*=B[j][j]
        for i in range(j+1,len(B)):
            ratio=B[i][j]/B[j][j]
            B[i]=[x-ratio*y for x,y in zip(B[i],B[j])]
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--author-dir',type=Path,required=True);args=ap.parse_args();root=args.author_dir
    inputs=json.loads((ROOT/'AUTHOR-INPUTS.json').read_text())
    for item in inputs['files']:
        p=root/Path(item['path']).name
        need(p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256'],'byte-pinned author input before import/parse')
    result=json.loads((root/'RESULTS.json').read_text());rows=[]
    for row in result['bounds']['cases']:
        p=profile(row['q'],row['loads']);R=p['R'];B=[[a-F(1,6)*b for a,b in zip(x,y)] for x,y in zip(p['budget'],p['metric'])]
        determinants=[F(1)]+[det([r[:i] for r in B[:i]]) for i in range(1,R)]
        need(all(z>0 for z in determinants),'all independently computed leading determinants')
        pivots=[determinants[i]/determinants[i-1] for i in range(1,R)]
        mean=sum(d*c*n for d,c,n in zip(p['loads'],p['c'],p['nu']))/p['m']
        variance=sum(d*(c*n-mean)**2 for d,c,n in zip(p['loads'],p['c'],p['nu']))
        ours={'q':p['q'],'loads':p['loads'],'Kgap':str(p['Kgap']),'minimum_internal_slack':str(min(1-z/p['h']-c*c*F(p['w']+1,p['h'])/(1-F(p['w']+1,p['h'])) for c,z in zip(p['c'],p['zeta']))),'maximum_variance_loss':str(variance/p['Kgap']),'balanced_budget_dimension':R-1,'positive_budget_pivots_sha256':hashlib.sha256(json.dumps(list(map(str,pivots)),separators=(',',':')).encode()).hexdigest(),'every_budget_pivot_checked':True}
        need(ours==row,'every shared scalar record field reconstructed');rows.append(ours)
    # The target program is imported here, explicitly AFTER all independent
    # normal matrices/budgets were frozen. No imports occur in literal.py.
    sys.path.insert(0,str(root.resolve()));spec=importlib.util.spec_from_file_location('pinned_author9305',root/'verify_full.py');author=importlib.util.module_from_spec(spec);spec.loader.exec_module(author)
    matrices=[]
    for case,(q,loads,marks) in enumerate(FIXTURES):
        n=q.bit_length();order=sorted(range(len(loads)),key=lambda i:(-loads[i],i));sortedloads=[loads[i] for i in order]
        family,s,seed,raw,Traw,params=author.build(n,sortedloads)
        oldmap=[marks[i] for i in order]+[j for j in range(n) if j not in marks]
        freshmap=[n+sum(loads[:i])+u for i in order for u in range(loads[i])];mapping=oldmap+freshmap
        aset=[frozenset(mapping[j] for j in range(len(mapping)) if mask>>j&1) for mask in family]
        old=[frozenset(A) for r in range(1,n+1) for A in combinations(range(n),r)];old.reverse()
        ylist=[(i,u,n+sum(loads[:i])+u) for i,d in enumerate(loads) for u in range(d)]
        ownsets=[frozenset()]+old+[frozenset([marks[i],y]) for i,u,y in ylist]+[frozenset([y]) for i,u,y in ylist]
        need(len(set(aset))==len(aset) and set(aset)==set(ownsets),'literal full-domain relabelling bijection')
        indices=[aset.index(A) for A in ownsets];N=len(family)
        def lift(C):
            sums=list(map(sum,C));Q=[[sum(sums)]+[-v for v in sums]]+[[-sums[i]]+row for i,row in enumerate(C)]
            return [[Q[i][j] for j in indices] for i in indices]
        qs,qr=lift(seed),lift(raw);eps=F(1,2*(1+Traw));M=[[(1+(1-eps)*qs[i][j]+eps*qr[i][j]-s*int(i==j))/(N-s) for j in range(N)] for i in range(N)]
        name='case0' if case==0 else str(case);expected=json.loads((ROOT/f'EXPECTED-{name}.json').read_text())['record']
        hashes={'seed_Gram_sha256':digest(qs),'raw_Gram_sha256':digest(qr),'mixed_H_sha256':digest(M)}
        need(all(v==expected[k] for k,v in hashes.items()) and str(Traw)==expected['Traw'] and str(eps)==expected['epsilon'],'ALL reordered original whole matrix entries via first-freeze exact hashes')
        matrices.append({'case':case,'N':N,'positions_per_matrix':N*N,**hashes})
    out={'shared_scalar_records':len(rows),'every_shared_scalar_field_equal':True,'scalar_case_record_sha256':digest(rows),'whole_matrix_comparisons':matrices,'every_original_whole_hash_equal':True,'author_build_used_only_for_late_matrix_corroboration':True,'independent_engine_imports_no_author_module':True};out['record_sha256']=digest(out);print(json.dumps(canonical(out),sort_keys=True,indent=2))
if __name__=='__main__':main()
