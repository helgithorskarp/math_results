"""Optional bounded selection with every distinct-type pair/triple local cut."""
import argparse
from functools import lru_cache
import itertools
import itertools as it
import json
from pathlib import Path
import time

MASKS = (5388912, 5404008, 5683824)  # red R(3,4;8), complemented below


def need(ok, msg):
    if not ok:
        raise ValueError(msg)


@lru_cache(None)
def upper(p, q):
    if min(p, q) == 1:
        return 1
    a, b = upper(p-1, q), upper(p, q-1)
    return a + b - int(a % 2 == 0 and b % 2 == 0)


def core(mask):
    pairs = list(itertools.combinations(range(8), 2))
    red = {(0, 1), (0, 2)} | {(0, v) for v in range(3, 11)}
    red |= {(u+3, v+3) for i, (u, v) in enumerate(pairs) if not(mask >> i & 1)}
    rows = [0]*11
    for u, v in red:
        rows[u] |= 1 << v
        rows[v] |= 1 << u
    return rows


def selection_rows(mask):
    g = core(mask)
    cliques = {}
    for color in (False, True):
        cliques[color] = {0: [0]}
        for k in range(1, 6):
            cliques[color][k] = [sum(1 << v for v in vs)
                for vs in itertools.combinations(range(11), k)
                if all(bool(g[u] >> v & 1) == color for u,v in itertools.combinations(vs,2))]
        need(not cliques[color][5], 'fixed core K5')
    domain = []
    for x in range(2048):
        if (x & 7) not in range(2, 8):
            continue
        if any(x & t == t for t in cliques[True][4]):
            continue
        if any(x & t == 0 for t in cliques[False][4]):
            continue
        domain.append(x)
    rows = []
    def add(coeff, bound, label):
        rows.append((tuple(coeff), bound, label))
    targets = [32] + [d-g[v].bit_count() for v,d in enumerate([20]*3+[21]*8)]
    equality = [[1]*len(domain)] + [[(x >> v)&1 for x in domain] for v in range(11)]
    for j,(row,b) in enumerate(zip(equality,targets)):
        add(row,b,['eq+',j]);add([-a for a in row],-b,['eq-',j])
    # Every actual extension obeys the full common-neighborhood union bounds.
    for a in range(4):
        for b in range(4):
            if a+b == 0:
                continue
            for A in cliques[True][a]:
                for B in cliques[False][b]:
                    if A & B:
                        continue
                    fixed = sum(not((A|B) >> v & 1) and g[v] & A == A and g[v] & B == 0
                                for v in range(11))
                    cap = upper(5-a,5-b)-1-fixed
                    coeff = [int(x & A == A and x & B == 0) for x in domain]
                    if any(coeff) or cap < 0:
                        add(coeff,cap,['root',A,B])
    # Identical rows are merged at the tightest bound, preserving a root label.
    merged = {}
    for a,b,label in rows:
        if a not in merged or b < merged[a][0]:
            merged[a] = (b,label)
    ordered = [(a,*merged[a]) for a in sorted(merged)]
    return g,domain,ordered


def interface(g, domain):
    full = (1 << len(g))-1
    has = {}
    for c in (False, True):
        for k in (2, 3):
            cliques = [sum(1 << v for v in vs) for vs in it.combinations(range(len(g)), k)
                       if all(bool(g[u] >> v & 1) == c for u,v in it.combinations(vs, 2))]
            has[c,k] = [any(x & t == t for t in cliques) for x in range(full+1)]
    n = len(domain)
    force = {False:[0]*n, True:[0]*n}
    bad = []
    loops = []
    for i,x in enumerate(domain):
        for j in range(i,n):
            y = domain[j]
            nr, nb = has[True,3][x & y], has[False,3][full ^ (x | y)]
            if nr and nb:
                (loops if i==j else bad).append((i,j))
            elif nr or nb:
                c = nb
                force[c][i] |= 1 << j
                force[c][j] |= 1 << i
    return full,has,force,bad,loops


def triples(domain, full, has, force):
    for c in (False, True):
        rows=force[c]
        for i,x in enumerate(domain):
            later=rows[i] & ~((1 << (i+1))-1)
            todo=later
            while todo:
                bj=todo & -todo; todo-=bj; j=bj.bit_length()-1
                candidates=later & rows[j] & ~((1 << (j+1))-1)
                while candidates:
                    bk=candidates & -candidates;candidates-=bk;k=bk.bit_length()-1
                    common=x & domain[j] & domain[k] if c else full ^ (x | domain[j] | domain[k])
                    if has[c,2][common]:
                        yield c,(i,j,k)


def main():
    import numpy as np
    from scipy.optimize import milp, Bounds, LinearConstraint
    from scipy.sparse import coo_array, vstack, csc_matrix
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True)
    p.add_argument('--seconds',type=float,default=30);a=p.parse_args();a.work.mkdir(exist_ok=False)
    start=time.monotonic();g,domain,rows=selection_rows(5388912)
    full,has,force,bad,loops=interface(g,domain)
    cuts=list(triples(domain,full,has,force))
    counts={'types':len(domain),'incompatible_pairs':len(bad),'self_incompatible_types':len(loops),
            'forced_distinct_pairs':{str(c):(sum(v.bit_count() for v in force[c])-sum(bool(v>>i&1) for i,v in enumerate(force[c])))//2 for c in (False,True)},
            'forced_repeat_types':{str(c):sum(bool(v>>i&1) for i,v in enumerate(force[c])) for c in (False,True)},
            'forbidden_distinct_triples':{str(c):sum(cc==c for cc,t in cuts) for c in (False,True)}}
    print('interface',json.dumps(counts),'seconds',time.monotonic()-start,flush=True)
    (a.work/'interface.json').write_text(json.dumps(counts,indent=2,sort_keys=True)+'\n')
    # Distinct types are an explicit experimental restriction, not a universal cut.
    ii=[];jj=[];vv=[];bounds=[]
    for pair in bad:
        for j in pair:ii.append(len(bounds));jj.append(j);vv.append(1)
        bounds.append(1)
    for c,t in cuts:
        for j in t:ii.append(len(bounds));jj.append(j);vv.append(1)
        bounds.append(2)
    extra=coo_array((vv,(ii,jj)),shape=(len(bounds),len(domain)))
    A=csc_matrix(vstack([np.array([x for x,b,l in rows]),extra]))
    b=np.array([b for x,b,l in rows]+bounds)
    r=milp(np.zeros(len(domain)),integrality=np.ones(len(domain)),bounds=Bounds(0,1),
           constraints=LinearConstraint(A,-np.inf,b),options={'time_limit':a.seconds})
    report={'interface':counts,'selection_status':int(r.status),'selection_message':r.message}
    if r.x is not None:
        vals=np.rint(r.x).astype(int)
        if not (np.all((vals==0)|(vals==1)) and np.all(A@vals<=b)):raise ValueError('bad selection')
        types=[t for t,v in zip(domain,vals) if v]
        if len(types)!=32:raise ValueError('count')
        report['types']=types
        fixed={};free=[]
        for i,j in it.combinations(range(32),2):
            nr=has[True,3][types[i]&types[j]];nb=has[False,3][full^(types[i]|types[j])]
            if nr and nb:raise ValueError('incompatible selected pair')
            if nr or nb:fixed[i,j]=int(nb)
            else:free.append((i,j))
        index={e:k for k,e in enumerate(free)}
        coeff=[];lb=[];ub=[]
        for i,t in enumerate(types):
            coeff.append([int(i in e) for e in free])
            debt=21-t.bit_count()-sum(v for e,v in fixed.items() if i in e)
            lb.append(debt);ub.append(debt)
        triangle_counts={False:0,True:0}
        for vs in it.combinations(range(32),3):
            es=list(it.combinations(vs,2));ts=[types[v] for v in vs]
            for c in (False,True):
                common=ts[0]&ts[1]&ts[2] if c else full^(ts[0]|ts[1]|ts[2])
                if not has[c,2][common] or any(e in fixed and fixed[e]!=c for e in es):continue
                row=[0]*len(free);constant=sum(fixed.get(e,0) for e in es if e in fixed)
                for e in es:
                    if e in index:row[index[e]]=1
                if not any(row):raise ValueError('forbidden selected triple')
                coeff.append(row);lb.append(-np.inf if c else 1-constant);ub.append(2-constant if c else np.inf)
                triangle_counts[c]+=1
        D=csc_matrix(np.array(coeff));lb=np.array(lb);ub=np.array(ub)
        print('tail',len(free),triangle_counts,'elapsed',time.monotonic()-start,flush=True)
        s=milp(np.zeros(len(free)),integrality=np.ones(len(free)),bounds=Bounds(0,1),
               constraints=LinearConstraint(D,lb,ub),options={'time_limit':a.seconds})
        report.update(tail_status=int(s.status),tail_message=s.message,free_edges=len(free),
                      forced_red=sum(fixed.values()),forced_blue=len(fixed)-sum(fixed.values()),
                      triangle_constraints={str(c):triangle_counts[c] for c in (False,True)})
        if s.x is not None:
            val=np.rint(s.x).astype(int);actual=D@val
            if not(np.all((val==0)|(val==1)) and np.all(actual>=lb) and np.all(actual<=ub)):raise ValueError('bad tail')
            red={(u,v) for u,v in it.combinations(range(11),2) if g[u]>>v&1}
            red|={(v,11+i) for i,t in enumerate(types) for v in range(11) if t>>v&1}
            red|={(11+u,11+v) for (u,v),c in fixed.items() if c}
            red|={(11+u,11+v) for (u,v),c in zip(free,val) if c}
            (a.work/'graph.json').write_text(json.dumps({'n':43,'red_edges':sorted(red)},indent=2,sort_keys=True)+'\n')
            report['status']='EXACT_THREE_OUTSIDE_PRIMAL_PENDING_LITERAL_CHECK'
    report['elapsed_seconds']=time.monotonic()-start
    (a.work/'result.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report),flush=True)


if __name__=='__main__':main()
