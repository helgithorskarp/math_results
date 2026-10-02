"""Independent point-mask row reconstruction and iterative category checker.

No producer, boundary enumerator, solver or earlier research code is imported.
The ordinary packing-to-capacity and parity bridges remain written proofs.
"""
import argparse
import hashlib
import itertools
import json
from math import comb
from pathlib import Path
import time

PIN='c188200792c201bdb44ea1667a8a70255c4e40f04fee6c334c98ecfa650113e7'
FIELDS=('e','k','q','eligible','h','g1_S','psi','margin','ss_excess')
CASES=((2,3),(3,9),(4,19))
def require(test,message):
    if not test:
        raise ValueError(message)
def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':')).encode()
def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()

def literal_rows(data):
    require(len(data['stars'])==len(data['groups'])==23,'complete literal input required')
    output=[]
    for fi,blocks in enumerate(data['stars']):
        require(len(blocks)==20,'twenty quadruples required')
        words=[]
        owned=set()
        for block in blocks:
            require(len(block)==4 and all(type(p) is int and 0<=p<17 for p in block),
                    'invalid literal point')
            w=sum(1<<p for p in set(block))
            require(w.bit_count()==4 and w not in words,'invalid or repeated literal quadruple')
            words.append(w)
            for p,t in itertools.combinations(block,2):
                pair=(1<<p)|(1<<t)
                require(pair not in owned,'repeated literal pair')
                owned.add(pair)
        rho=[sum(w>>p&1 for w in words) for p in range(17)]
        require(max(rho)<=5 and sum(5-r for r in rho)==5,'invalid literal link replications')
        high=[p for p,r in enumerate(rho) if r<5]
        highbits=sum(1<<p for p in high)
        lowbits=((1<<17)-1)^highbits
        leave=[(1<<p)|(1<<t) for p,t in itertools.combinations(range(17),2)
               if ((1<<p)|(1<<t)) not in owned]
        require(len(leave)==16,'literal leave size')
        require(all(pair&highbits for pair in leave),'literal low-low leave')
        require(all(sum(bool(pair&(1<<p)) for pair in leave)==1
                    for p,r in enumerate(rho) if r==5),'literal low degree')
        HH=[pair for pair in leave if not(pair&lowbits)]
        require(len(HH)==len(high)-1,'literal high-high leave count')
        isolated={p for p in high if not any(pair&(1<<p) for pair in HH)}
        for size in range(len(high)+1):
            for positions in itertools.combinations(high,size):
                hubbits=sum(1<<p for p in positions)
                e=5-len(high)
                eligible=any(p in isolated for p in positions)
                g1=sum(rho[p]==4 and not(hubbits>>p&1) for p in high)
                sigma=sum(max(0,4-rho[p]) for p in range(17) if not(hubbits>>p&1))
                w=sum(5-rho[p] for p in positions)
                q=sum(bool(pair&hubbits) for pair in HH)
                psi=0
                if not e and eligible:
                    psi=g1
                if e and not eligible:
                    psi=-g1
                require(e==w-size+sigma,'literal support identity')
                output.append(dict(fixture=fi,hub_high=list(positions),h=len(high),e=e,
                    k=size,q=q,eligible=eligible,g1_S=g1,ss_excess=sigma,
                    hub_weight=w,psi=psi,margin=psi-3*(size-e-q)))
    return sorted(output,key=lambda r:(r['fixture'],r['hub_high']))

def check_catalog(catalog,data,scope=4):
    actual=literal_rows(data)
    require(catalog['rows']==actual,'whole actual row universe or coordinate differs')
    require(all(r['margin']>=0 for r in actual if r['k']<=scope),
            'actual row inequality fails in requested scope')
    within=[r for r in actual if r['k']<=4]
    expected=dict(status='PASS_ALL_LITERAL_ROWS_WITH_K_LE_FOUR',total_rows=len(actual),
        within_scope_rows=len(within),row_records_sha256=digest(actual),
        within_scope_sha256=digest(within),minimum_margin=min(r['margin'] for r in within),
        outside_scope_actual_failures=[r for r in actual if r['k']==5],
        fixture_populations=[sum(r['fixture']==fi for r in actual) for fi in range(23)])
    require(catalog['summary']==expected,'catalog summary differs from literal rows')
    return actual,expected

def iterative_boundaries(rows):
    out=[]
    for m,P in CASES:
        n=18-m
        B=4*n-comb(n,3)-120*m+740
        w0=20+10*m-5*m*m
        slack=4*P-(w0-2*B)
        for T,X,tau,Q in itertools.product(range(slack+1),repeat=4):
            if 2*T+2*X+4*tau+Q>slack:
                continue
            E=B+3*P-T-2*tau-Q
            W=w0+2*P
            K=W-E+2*X
            budget=3*(E+Q-K)
            require(T==X==tau==0 and budget>=0,'literal boundary domain')
            types=sorted({tuple(r[f] for f in FIELDS) for r in rows
                if r['k']<=m and r['q']<=Q and r['ss_excess']==0 and r['margin']<=budget})
            states=[((),0,0,0,0,0)]
            start=time.monotonic()
            for coordinates in types:
                row=dict(zip(FIELDS,coordinates))
                next_states=[]
                for counts,used,se,sk,sq,smargin in states:
                    for c in range(n-used+1):
                        totals=(used+c,se+c*row['e'],sk+c*row['k'],sq+c*row['q'],
                                smargin+c*row['margin'])
                        if any(a>b for a,b in zip(totals,(n,E,K,Q,budget))):
                            continue
                        next_states.append((counts+(c,),*totals))
                require(len(next_states)<=100000 and time.monotonic()-start<=10,
                        'INCOMPLETE iterative category guard hit')
                states=next_states
            templates=sorted([list(c) for c,u,se,sk,sq,sm in states
                              if (u,se,sk,sq)==(n,E,K,Q)])
            parity=[]
            for counts in templates:
                mixed=[(dict(zip(FIELDS,t)),c) for t,c in zip(types,counts) if t[0] and c]
                require(all(r['e']==1 and r['eligible'] and r['k']==1
                            and r['h']==4 and r['g1_S']==3 for r,c in mixed),
                        'ordinary parity premise is not forced')
                M=sum(c for r,c in mixed)
                require(M%2==1,'even block cannot be closed by odd handshake')
                parity.append(dict(nonunit_rows=M,degree_per_nonunit_row=3,degree_sum=3*M,
                    odd_degree_sum=True,ordinary_bridge='All these nonunit rows are eligible; local9249 forbids their deficit-one saturated neighbors from being unit.'))
            out.append(dict(m=m,n=n,P=P,T=T,X=X,tau=tau,Q=Q,E=E,W=W,K=K,
                margin_budget=budget,category_fields=list(FIELDS),types=[list(t) for t in types],
                templates=templates,parity=parity,status='NO_NECESSARY_CATEGORY_INVENTORY'
                    if not templates else 'ALL_TEMPLATES_HAVE_ODD_THREE_REGULAR_NONUNIT_BLOCK'))
    return dict(status='PASS_EXACT_BOUNDARY_CATEGORY_AND_PARITY_REDUCTIONS',branches=out,
                branches_sha256=digest(out))

def check_boundaries(boundaries,rows):
    actual=iterative_boundaries(rows)
    require(boundaries==actual,'whole category, template, arithmetic or parity record differs')
    return actual

def algebra_checks():
    require(all(comb(5-j,3)==10-6*j+3*comb(j,2)-comb(j,3)
                for j in range(6)),'homogeneous triple polynomial')
    table=[]
    for m in range(1,5):
        n=18-m
        B=4*n-comb(n,3)-120*m+740
        w0=20+10*m-5*m*m
        table.append(dict(m=m,n=n,B=B,C=w0-2*B))
    require([r['B'] for r in table]==[8,4,-15,-48] and
            [r['C'] for r in table]==[9,12,35,76],'exact coefficient table')
    return dict(homogeneous_word_hub_counts_checked=6,table=table)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--fixtures',type=Path,default=Path(__file__).with_name('fixtures.json'))
    p.add_argument('--primary',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    raw=a.fixtures.read_bytes()
    require(hashlib.sha256(raw).hexdigest()==PIN,'pinned literal fixture bytes differ')
    rows,catalog=check_catalog(json.loads((a.primary/'catalog.json').read_text()),json.loads(raw))
    boundary=check_boundaries(json.loads((a.primary/'boundaries.json').read_text()),rows)
    result=dict(status='PASS_COMPLETE_INDEPENDENT_MASK_ROWS_AND_CATEGORY_TEMPLATES',
                catalog_summary=catalog,boundary_summary=boundary,algebra=algebra_checks())
    a.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],actual_rows=len(rows),
        within_scope_rows=catalog['within_scope_rows'],row_sha256=catalog['row_records_sha256'],
        boundary_branches=len(boundary['branches']),boundary_sha256=boundary['branches_sha256'])))
if __name__=='__main__':
    main()
