"""Literal clause, palette, interval-prefix and difference-capacity audits."""
import hashlib
import itertools
import json
from pathlib import Path

from model import encoding, decode, dimacs
from verify import verify_word


def symbolic_table(a,p):
    n,t=a*p,(p-1)//2
    table={}
    for q in range(1,a):
        for c in range(6):table[p*q,c]=('E',min(q,a-q),c)
    for q in range(a):
        for b in range(1,t+1):
            for x in (p*q+b,n-p*q-b):
                table[x,b-1]=('Q',q,0)
                for c in range(t,6):table[x,c]=('Q',q,c)
    return table


def clause_audit(a,p):
    m,cnf=encoding(a,p,symmetry=False)
    table=symbolic_table(a,p);n=a*p;literal=set()
    for z in range(1,n):
        for x in range(1,n):
            y=(z-x)%n
            if not y:continue
            for c in range(6):
                labels=[table.get((v,c)) for v in (x,y,z)]
                if None not in labels:
                    literal.add(tuple(sorted({-m[k][u,d] for k,u,d in labels})))
    assert literal==m['criterion_clauses']
    return dict(axis_factor=a,short_factor=p,modular_pairs=(n-1)**2//2,
                distinct_schur_clauses=len(literal))


def small_audit():
    a,p=5,7;m,plain=encoding(a,p,symmetry=False)
    _,normal=encoding(a,p,symmetry=True)
    table=symbolic_table(a,p);checked=valid=0
    def assignment(e,q):
        return {m['E'][u,e[u-1]] for u in range(1,m['h']+1)} | {
            m['Q'][u,q[u]] for u in range(a)}
    def accepts(cnf,values):
        return all(any((v in values) if v>0 else (-v not in values) for v in cl) for cl in cnf)
    for e in itertools.product(range(6),repeat=2):
        for tail in itertools.product(m['labels'],repeat=4):
            q=(0,*tail);truth=assignment(e,q);row=[-1]*(a*p)
            for (x,c),(key,u,d) in table.items():
                if (e[u-1] if key=='E' else q[u])==d:
                    assert row[x]==-1;row[x]=c
            assert row[1:]==decode(m,truth) and -1 not in row[1:]
            literal_ok=not any(row[x]==row[y]==row[(x+y)%(a*p)]
                               for x in range(1,a*p) for y in range(x,a*p)
                               if (x+y)%(a*p))
            assert literal_ok==accepts(plain,truth)
            checked+=1
            if not literal_ok:continue
            valid+=1;common={};special={}
            for c in [*q,*e]:
                if c>=3 and c not in common:common[c]=3+len(common)
            for c in e:
                if c<3 and c not in special:special[c]=len(special)
            ee=[common[c] if c>=3 else special[c] for c in e]
            qq=[common[c] if c>=3 else c for c in q]
            image=assignment(ee,qq)
            assert accepts(normal,image)
            verify_word(dict(axis_factor=a,short_factor=p,word=decode(m,image)))
    return dict(assignments=checked,valid=valid,all_valid_normalized=True)


def prefix_audit(a,p):
    assert a%6==1
    m=(a-1)//3;I=set(range(m+1,2*m+1));difference={(x-y)%a for x in I for y in I}
    table=symbolic_table(a,p);colour=(p-1)//2
    # Under C_colour=I, every possible indicator in this prefix is false.
    for x in range(1,p*m):
        key,u,c=table[x,colour]
        if key=='Q':assert u not in I
        else:assert u in difference
    return dict(axis_factor=a,short_factor=p,omitted_colour_prefix=p*m-1)


def capacity_audit():
    # The difference-d graph on 36 consecutive points is a disjoint union
    # of paths; each path of length ell has independence number ceil(ell/2).
    capacities=[sum((1+(35-r)//d+1)//2 for r in range(d)) for d in range(1,33)]
    assert max(capacities)==32 and all(v<32 for v in capacities[:-1])
    # Exhaust every size-32 subset, independently using integer bit shifts.
    full=(1<<36)-1;accepted=[];count=0
    for holes in itertools.combinations(range(36),4):
        bits=full-sum(1<<x for x in holes);count+=1
        absent=[d for d in range(1,33) if not bits&(bits>>d)]
        if absent:
            assert absent==[32]
            accepted.append(tuple(37+x for x in holes))
    expected=sorted(tuple(sorted(69+i if mask>>i&1 else 37+i for i in range(4)))
                    for mask in range(16))
    assert sorted(accepted)==expected
    table=symbolic_table(109,5)
    early_axis=[]
    for x in range(1,162):
        key,u,c=table[x,2]
        if key=='Q':assert u not in range(37,73)
        else:early_axis.append(x)
    assert early_axis==list(range(5,161,5))
    return dict(interval_length=36,differences=list(range(1,33)),
                independence_numbers=capacities,size32_subsets_checked=count,
                admissible_size32_supports=len(accepted),removed_sets=expected,
                only_missing_difference_for_size32=32,forced_axis_position=32)


def run():
    return dict(clause_audits=[clause_audit(a,p) for a,p in [(5,7),(13,7),(77,7),(5,5),(109,5)]],
                small_audit=small_audit(),
                prefix_audits=[prefix_audit(a,p) for a,p in [(61,5),(97,5),(109,5),(67,7),(79,7)]],
                interval_capacity=capacity_audit(),
                models=[dict(axis_factor=a,short_factor=p,bytes=len(dimacs(a,p)),
                             sha256=hashlib.sha256(dimacs(a,p)).hexdigest(),status='UNRESOLVED')
                        for a,p in [(77,7),(109,5)]])


if __name__=='__main__':
    result=run()
    expected=json.loads(Path(__file__).with_name('expected.json').read_text())
    # JSON represents the removed-set tuples as lists.
    assert json.loads(json.dumps(result))==expected['audits']
    print(json.dumps({'status':'PASS','audits':result},indent=2))
