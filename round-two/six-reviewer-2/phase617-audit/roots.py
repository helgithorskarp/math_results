"""Whole actual APs yield literal root clauses for each common projection."""
import sys,json,hashlib
from field import inputs,root_positions,OPTIONS,progressions,require

def run(N):
    data=inputs(N);roots=root_positions(N);root_index={n:i for i,n in enumerate(roots)};clauses=[{}for _ in OPTIONS];aps=0
    for a,d in progressions(N):
        aps+=1;pts=tuple(a+j*d for j in range(7));unknown=tuple(root_index[n]for n in pts if data[n]is None)
        for choice,(j,b) in enumerate(OPTIONS):
            colors={data[n][j]^b for n in pts if data[n]is not None}
            if len(colors)==2:continue
            for color in [0,1] if not colors else colors:
                # Tuple (indices,color) forbids setting all listed roots to color.
                key=(unknown,color);old=clauses[choice].get(key);leaf=(a+6*d,a,d)
                if old is None or leaf<old:clauses[choice][key]=leaf
    records=[]
    for i,(j,b)in enumerate(OPTIONS):
        C=clauses[i];assignment={};implications=[];conflict=None
        changed=True
        while changed and conflict is None:
            changed=False
            for (vars,color),leaf in sorted(C.items()):
                if any(v in assignment and assignment[v]!=color for v in vars):continue
                unset=[v for v in vars if v not in assignment]
                if not unset:conflict=dict(variables=list(vars),forbidden_color=color,leaf=list(leaf));break
                if len(unset)==1:
                    v=unset[0];assignment[v]=1-color;implications.append(dict(variable=v,value=1-color,variables=list(vars),forbidden_color=color,leaf=list(leaf)));changed=True
        remaining=sorted({((tuple(v for v in vs if v not in assignment)),c)for (vs,c)in C if not any(v in assignment and assignment[v]!=c for v in vs)})if conflict is None else []
        records.append(dict(choice=i,coordinate=j,palette=b,all_distinct_root_clauses=len(C),fixed=sorted([v,c]for v,c in assignment.items()),implications=implications,conflict=conflict,residual_clauses=[[list(v),c]for v,c in remaining],leaves=[[list(v),c,list(leaf)]for (v,c),leaf in sorted(C.items())]))
    return dict(N=N,all_actual_aps=aps,root_positions=list(roots),phase_options=[list(p)for p in OPTIONS],records=records)
if __name__=='__main__':print(json.dumps(run(int(sys.argv[1])),sort_keys=True,separators=(',',':')))
