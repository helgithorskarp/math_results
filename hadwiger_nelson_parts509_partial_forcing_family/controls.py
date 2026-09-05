#!/usr/bin/env python3
"""Definition-level PB decoding and exhaustive local degree semantics."""
from itertools import product
from engine import require


def check(facts,supports):
    out=[]
    for fact in facts:
        q=fact['q'];s=supports[q];adj=s['adj'];F=s['fixed'];R=set(s['free']);rows=[]
        for line in s['opb'].decode().splitlines()[1:]:
            left,right=line.split(' >= ');rhs=int(right.removesuffix(' ;'));tokens=left.split()
            require(len(tokens)%2==0,'OPB syntax');row={}
            for c,v in zip(tokens[::2],tokens[1::2],strict=True):
                require(v.startswith('x') and 1<=int(v[1:])<=len(R),'OPB index')
                label=s['free'][int(v[1:])-1];require(label not in row,'duplicate variable');row[label]=int(c)
            rows.append((row,rhs))
        n=len(s['hitting_sets'])
        for (row,rhs),D in zip(rows[:n],s['hitting_sets'],strict=True):
            require(set(row)==D and set(row.values())=={1} and rhs==1,'hitting row semantics')
        require(rows[n]==(dict.fromkeys(s['pool'],1),3),'pool quota')
        require(rows[n+1]==(dict.fromkeys(s['free'],-1),-s['budget']),'free budget')
        newly_optional=set(fact['missing_forced'])
        require(all(not (set(row)&newly_optional) for i,(row,rhs) in enumerate(rows) if i!=n+1),
                'newly optional labels occur only in the budget')
        degree_rows=rows[n+2:];require(len(degree_rows)==len(s['degree']),'degree coverage')
        exceptions={entry['v'] for entry in s['degree']}
        require(exceptions=={v for v in adj if len(adj[v]&F)<4},'complete degree inventory')
        cases=degree_checks=0;stars=[]
        for (row,rhs),entry in zip(degree_rows,s['degree'],strict=True):
            v=entry['v'];need=4-len(adj[v]&F);optional=adj[v]&R
            if v in F:
                require(set(row)==optional and set(row.values())<={1} and rhs==need,'fixed degree row')
            else:
                require(set(row)==optional|{v} and row[v]==-need and rhs==0,'optional degree row')
                require(all(c==1 for u,c in row.items() if u!=v),'neighbour coefficients')
            local=sorted(optional|({v} if v in R else set()));require(len(local)<=16,'truth table bound')
            for bits in product([False,True],repeat=len(local)):
                chosen={u for u,b in zip(local,bits,strict=True) if b}
                for remainder in [set(),R-set(local)]:
                    S=F|chosen|remainder
                    require((v not in S or len(adj[v]&S)>=4)==(sum(c for u,c in row.items() if u in S)>=rhs),'local degree equivalence')
                    cases+=1
            stars.append(dict(v=v,local_vertices=local,cases=2**(len(local)+1)))
        # Additional global fixtures check conjunction and vacuous optional rows.
        for X in [set(),R]+[{v} for v in sorted(R)]+[R-{v} for v in sorted(R)]:
            S=F|X;degrees=[len(adj[v]&S) for v in S]
            require((min(degrees)>=4)==all(sum(c for v,c in row.items() if v in S)>=rhs for row,rhs in degree_rows),'global degree fixture')
            degree_checks+=len(degrees)
        out.append(dict(q=q,decoded_PB_rows=len(rows),exhaustive_star_cases=cases,
                        global_cases=2+2*len(R),direct_global_vertex_degree_checks=degree_checks,stars=stars,
                        newly_optional_labels_occur_only_in_budget=True,projected_primary_variables=len(R-newly_optional)))
    return out
