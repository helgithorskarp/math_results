"""Exhaustive exact necessary-category compositions at the three boundaries."""
import argparse
import hashlib
import itertools
import json
from math import comb
from pathlib import Path
import time

FIELDS=('e','k','q','eligible','h','g1_S','psi','margin','ss_excess')
CASES=((2,3),(3,9),(4,19))
def require(test, message):
    if not test:
        raise ValueError(message)
def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':')).encode()
def derive(rows):
    result=[]
    for m,P in CASES:
        n=18-m
        B=4*n-comb(n,3)-120*m+740
        w0=20+10*m-5*m*m
        C=w0-2*B
        slack=4*P-C
        require(slack in (0,1), 'wrong target boundary slack')
        for T,X,tau,Q in itertools.product(range(slack+1),repeat=4):
            if 2*T+2*X+4*tau+Q > slack:
                continue
            E=B+3*P-T-2*tau-Q
            W=w0+2*P
            K=W-E+2*X
            budget=3*(E+Q-K)
            require(T==X==tau==0 and budget>=0, 'unexpected boundary branch')
            types=sorted({tuple(r[f] for f in FIELDS) for r in rows
                if r['k']<=m and r['q']<=Q and r['ss_excess']==0 and r['margin']<=budget})
            templates=[]
            nodes=0
            start=time.monotonic()
            def visit(i,counts,left,e,k,q,margin):
                nonlocal nodes
                nodes+=1
                require(nodes<=100000 and time.monotonic()-start<=10,
                    'INCOMPLETE boundary composition guard hit')
                if min(left,E-e,K-k,Q-q,budget-margin)<0:
                    return
                if i==len(types):
                    if (left,e,k,q)==(0,E,K,Q):
                        templates.append(counts)
                    return
                row=dict(zip(FIELDS,types[i]))
                for count in range(left+1):
                    visit(i+1,counts+[count],left-count,e+count*row['e'],
                          k+count*row['k'],q+count*row['q'],margin+count*row['margin'])
            visit(0,[],n,0,0,0,0)
            parity=[]
            for counts in templates:
                mixed=[(dict(zip(FIELDS,t)),count) for t,count in zip(types,counts)
                       if t[0] and count]
                require(all(r['e']==1 and r['eligible'] and r['k']==1
                            and r['h']==4 and r['g1_S']==3 for r,count in mixed),
                        'surviving category template needs a different ordinary proof')
                M=sum(count for r,count in mixed)
                require(M%2==1,'even survivor is not closed by parity')
                parity.append(dict(nonunit_rows=M,degree_per_nonunit_row=3,degree_sum=3*M,
                    odd_degree_sum=True,ordinary_bridge='All these nonunit rows are eligible; local9249 forbids their deficit-one saturated neighbors from being unit.'))
            result.append(dict(m=m,n=n,P=P,T=T,X=X,tau=tau,Q=Q,E=E,W=W,K=K,
                margin_budget=budget,category_fields=FIELDS,types=types,templates=templates,
                parity=parity,status='NO_NECESSARY_CATEGORY_INVENTORY' if not templates
                    else 'ALL_TEMPLATES_HAVE_ODD_THREE_REGULAR_NONUNIT_BLOCK'))
    return dict(status='PASS_EXACT_BOUNDARY_CATEGORY_AND_PARITY_REDUCTIONS',branches=result,
        branches_sha256=hashlib.sha256(canonical(result)).hexdigest())
def main():
    p=argparse.ArgumentParser()
    p.add_argument('--catalog',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    result=derive(json.loads(a.catalog.read_text())['rows'])
    a.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__':
    main()
