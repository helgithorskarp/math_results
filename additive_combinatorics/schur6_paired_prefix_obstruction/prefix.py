"""Five-colour ordinary prefixes with paired short residues modulo five.

Each (5q+1,5q+2) is (0,1) or one repeated common colour.
Each (5q+3,5q+4) is (1,0) or one repeated common colour.
Multiples of five are unrestricted. These are prefixes, not full cyclic words.
"""
import itertools


def encoding(N,colours=5,symmetry=True):
    rows={};table={};v=0
    common=tuple(range(2,colours))
    for x in range(1,N+1):
        q,b=divmod(x,5)
        key=('axis',q) if b==0 else ('low' if b<=2 else 'high',q)
        if key not in rows:
            states=tuple(range(colours)) if b==0 else (0,*common)
            rows[key]={}
            for c in states:v+=1;rows[key][c]=v
        if b==0:
            for c in range(colours):table[x,c]=rows[key][c]
        else:
            for c in common:table[x,c]=rows[key][c]
            table[x,0 if b in (1,4) else 1]=rows[key][0]
    clauses=set()
    for row in rows.values():
        clauses.add(tuple(row.values()))
        for a,b in itertools.combinations(row.values(),2):clauses.add(tuple(sorted((-a,-b))))
    schur=set()
    for x in range(1,N+1):
        for y in range(x,N+1-x):
            for c in range(colours):
                if all((z,c) in table for z in (x,y,x+y)):
                    schur.add(tuple(sorted({-table[z,c] for z in (x,y,x+y)})))
    clauses.update(schur)
    if symmetry:
        seen={c:[] for c in common}
        for row in rows.values():
            for c in common[1:]:clauses.add(tuple([-row[c],*seen[c-1]]))
            for c in common:seen[c].append(row[c])
    return dict(N=N,colours=colours,common=common,rows=rows,table=table,variables=v,
                schur=schur),sorted(clauses,key=lambda cl:(len(cl),cl))


def decode(m,truth):
    result=[]
    for x in range(1,m['N']+1):
        values=[c for c in range(m['colours']) if m['table'].get((x,c)) in truth]
        assert len(values)==1
        result.append(values[0])
    return result
