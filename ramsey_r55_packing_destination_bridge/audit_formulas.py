"""Independent physical suffix specification and hash-pinned full CNF replay."""
from itertools import combinations
from pathlib import Path
from types import SimpleNamespace
import argparse
import hashlib
import json
import time
import compile_family
from check_census import graph_lines, parse_line, require

HERE=Path(__file__).resolve().parent

def number(u,v):
    if u>v:u,v=v,u
    return u*(85-u)//2+v-u

def run(cache,out,full=True):
    out=Path(out);out.mkdir(parents=True,exist_ok=True);start=time.monotonic()
    clauses=literals=patterns=0;digest=hashlib.sha256();summary=[]
    for q,n in ((8,11),(9,7)):
        representatives={}
        for line in graph_lines(cache,n):
            g=parse_line(line,n);used=set();chosen=[]
            for e in sorted(g):
                if not used.intersection(e):chosen.append(e);used.update(e)
            chosen=tuple(chosen[:4 if q==8 else 2])
            require(len(chosen)==(4 if q==8 else 2),'matching coverage')
            if chosen not in representatives:representatives[chosen]=g
        # The source core controls the suffix only through this matching tuple.
        # Exhaust all tuples actually present; every core index has been visited.
        for chosen,g in sorted(representatives.items()):
            rows=[sum(1<<v for v in range(n) if tuple(sorted((u,v))) in g) for u in range(n)]
            for r in range(5,q+1):
                expected=[]
                for b in range(r):
                    for e,f in combinations(chosen,2):
                        for s in combinations(range(4),2):
                            t=set(range(4))-set(s)
                            pairs={(4*b+u,4*q+v) for u in s for v in e}
                            pairs|={(4*b+u,4*q+v) for u in t for v in f}
                            require(len(pairs)==8,'literal support')
                            expected.append(tuple(sorted(-number(u,v) for u,v in pairs)))
                actual=list(compile_family.physical_suffix(q,r,rows))
                require([tuple(sorted(c)) for c in actual]==expected,'physical suffix identity')
                fixed={e for b in range(q) for e in combinations(range(4*b,4*b+4),2)}
                fixed.update(combinations(range(4*q,43),2))
                free=[e for e in combinations(range(43),2) if e not in fixed]
                mapping={e:k+2 for k,e in enumerate(free)}
                by_physical={number(*e):v for e,v in mapping.items()}
                task=SimpleNamespace(q=q,r=r,core=rows,variables=mapping)
                local=list(compile_family.local_suffix(task))
                wanted=[tuple(-by_physical[-x] for x in c) for c in actual]
                require(local==wanted,'local variable suffix identity')
                require(len(actual)==(36*r if q==8 else 6*r),'macro suffix count')
                for c in actual:
                    raw=(' '.join(map(str,c))+' 0\n').encode();digest.update(raw)
                clauses+=len(actual);literals+=8*len(actual)
            patterns+=1
        summary.append({'q':q,'distinct_selected_matchings':len(representatives)})
    compiled=[]
    if full:
        old=json.loads((HERE.parent/'ramsey_r55_maximal_block_order'/'FORMULAS.json').read_text())
        for row in old:
            if row['triangles'] or not any(row['task'].startswith(f'bo1-q{q}-') for q in (8,9)):continue
            result=compile_family.compile_task(row['task'],cache)
            require(result['upstream_cnf_sha256']==row['sha256'],'pinned whole upstream formula')
            require(result['variables']==row['variables'],'variable header')
            require(result['clauses']==row['clauses']+result['added_clauses'],'clause header')
            compiled.append(result)
            print(json.dumps({'checked_complete_formula':row['task'],'sha256':result['sha256']}),flush=True)
        require(len(compiled)==9,'all affected macro formula representatives')
    result={'status':'PHYSICAL_FAMILY_SUFFIX_AND_CNF_PASS','matching_patterns':patterns,
            'clauses_checked':clauses,'literals_checked':literals,'suffix_stream_sha256':digest.hexdigest(),
            'per_order':summary,'full_formula_representatives':compiled,'seconds':time.monotonic()-start}
    (out/'FORMULAS_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('cache');p.add_argument('out');p.add_argument('--suffix-only',action='store_true');args=p.parse_args()
    result=run(args.cache,args.out,not args.suffix_only)
    print(json.dumps({k:v for k,v in result.items() if k!='full_formula_representatives'},sort_keys=True))
