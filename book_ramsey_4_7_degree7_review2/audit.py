#!/usr/bin/env python3
"""Independent block decomposition and principal-minor audit. No author imports."""
from itertools import combinations, permutations
from functools import lru_cache
from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import argparse
from sharp_window import run as sharp_window_audit


def require(condition,message):
    if not condition: raise ValueError(message)


def rooted_cubic(n):
    require(n in (6,8),'unsupported cubic order')
    inner=list(combinations(range(1,4),2))
    outside=list(combinations(range(4,n),2))
    full=list(combinations(range(n),2))
    pos={e:i for i,e in enumerate(full)}
    graphs=[]
    for left in range(1<<len(inner)):
        a=[2]*3
        le=[e for i,e in enumerate(inner) if left>>i&1]
        for u,v in le:a[u-1]-=1;a[v-1]-=1
        for right in range(1<<len(outside)):
            b=[3]*(n-4)
            re=[e for i,e in enumerate(outside) if right>>i&1]
            for u,v in re:b[u-4]-=1;b[v-4]-=1
            if sum(a)!=sum(b) or min(b)<0:continue
            choices=[list(combinations(range(n-4),d)) for d in a]
            def fill(i,remaining,edges):
                if i==3:
                    if any(remaining):return
                    es=[(0,j) for j in range(1,4)]+le+re+edges
                    graphs.append(sum(1<<pos[e] for e in es))
                    return
                for selected in choices[i]:
                    if any(remaining[j]<=0 for j in selected):continue
                    nxt=remaining[:]
                    for j in selected:nxt[j]-=1
                    fill(i+1,nxt,edges+[(i+1,j+4) for j in selected])
            fill(0,b,[])
    require(len(graphs)==len(set(graphs)),'duplicate block graph')
    return sorted(graphs)


def adjacency(n,mask):
    require(type(mask) is int and 0<=mask<(1<<(n*(n-1)//2)),'bad graph mask')
    p=[[0]*n for _ in range(n)]
    for bit,(u,v) in enumerate(combinations(range(n),2)):
        if mask>>bit&1:p[u][v]=p[v][u]=1
    require(all(sum(row)==3 for row in p),'noncubic graph')
    require([j for j in range(n) if p[0][j]]==[1,2,3],'unnormalized graph')
    return p


def determinant(a):
    # Laplace expansion cached by used columns. Exact integers; no elimination.
    n=len(a)
    require(all(len(row)==n for row in a),'nonsquare matrix')
    @lru_cache(None)
    def expand(columns):
        row=columns.bit_count()
        if row==n:return 1
        total=0;rank=0
        for j in range(n):
            if columns>>j&1:continue
            total+=(-1 if rank%2 else 1)*a[row][j]*expand(columns|(1<<j))
            rank+=1
        return total
    return expand(0)


def psd_witness(p):
    n=len(p)
    m=[[p[i][j]+2*(i==j) for j in range(n)] for i in range(n)]
    for size in range(1,n+1):
        for subset in combinations(range(n),size):
            value=determinant([[m[i][j] for j in subset] for i in subset])
            if value<0:return list(subset),value
    return None



def validate_negative_minor(p,subset,claimed):
    n=len(p)
    require(type(subset) is list and subset and all(type(x) is int for x in subset),'bad minor indices')
    require(len(set(subset))==len(subset) and all(0<=x<n for x in subset),'bad minor domain')
    require(type(claimed) is int,'noninteger determinant')
    require(all(len(row)==n for row in p),'nonsquare adjacency')
    require(all(type(p[i][j]) is int and p[i][j] in (0,1) and p[i][j]==p[j][i] and (i!=j or p[i][j]==0) for i in range(n) for j in range(n)),'bad adjacency')
    value=determinant([[p[i][j]+2*(i==j) for j in subset] for i in subset])
    require(value==claimed and value<0,'invalid negative minor')
    return value


@lru_cache(None)
def canonical_minor(n,mask):
    pairs=list(combinations(range(n),2))
    p=[[0]*n for _ in range(n)]
    for bit,(i,j) in enumerate(pairs):
        if mask>>bit&1:p[i][j]=p[j][i]=1
    return min(sum(p[order[i]][order[j]]<<bit for bit,(i,j) in enumerate(pairs)) for order in permutations(range(n)))


def characteristic(a):
    n=len(a);coeff=[1]
    for k in range(1,n+1):
        value=sum(determinant([[a[i][j] for j in subset] for i in subset]) for subset in combinations(range(n),k))
        coeff.append((-1)**k*value)
    return coeff


def multiply(left,right):
    out=[0]*(len(left)+len(right)-1)
    for i,a in enumerate(left):
        for j,b in enumerate(right):out[i+j]+=a*b
    return out


def roots_polynomial(roots):
    coeff=[1]
    for root in roots:coeff=multiply(coeff,[1,-root])
    return coeff


def classify_eight():
    masks=rooted_cubic(8);require(len(masks)==553,'incomplete cubic8 cohort')
    stream=sha256();negative=[];retained=[];patterns=Counter();checked_entries=0
    for mask in masks:
        p=adjacency(8,mask);w=psd_witness(p)
        stream.update((json.dumps([mask,w],separators=(',',':'))+'\n').encode())
        if w is None:retained.append(mask)
        else:
            sub,value=w;validate_negative_minor(p,sub,value);negative.append([mask,w])
            small=sum(p[i][j]<<bit for bit,(i,j) in enumerate(combinations(sub,2)))
            patterns[len(sub),canonical_minor(len(sub),small),value]+=1
        # Derive every saturated common-red entry directly from C and H.
        for i in range(8):
            for j in range(8):
                if i==j:direct=6
                elif p[i][j]:
                    common_blue_c=sum(p[i][k]*p[j][k] for k in range(8))
                    # Blue pair: four blue pages remain in W=12, each red row6.
                    direct=4-common_blue_c
                else:
                    # Red pair: total3 pages minus common-red pages in C.
                    common_red_c=sum((k not in (i,j)) and not p[i][k] and not p[j][k] for k in range(8))
                    direct=3-common_red_c
                formula=3+6*(i==j)+p[i][j]-sum(p[i][k]*p[k][j] for k in range(8))
                require(direct==formula,'saturated cubic Gram entry mismatch')
                checked_entries+=1
    require(len(negative)==552 and retained==[264249735],'wrong cubic8 PSD classification')
    p=adjacency(8,retained[0]);require(all(p[i][j]==int(i!=j and i//4==j//4) for i in range(8) for j in range(8)),'retained graph is not2K4')
    # P+2I=(J4+I4) direct quadratic form proves strict positivity.
    require(characteristic([[p[i][j]+2*(i==j) for j in range(8)] for i in range(8)])==roots_polynomial([5,5]+[1]*6),'retained positive spectrum mismatch')
    expect={(5,62,-4):456,(5,126,-16):24,(7,48560,-6):72}
    require(dict(patterns)==expect,'principal obstruction cover mismatch')
    return {'graphs':len(masks),'negative_principal_minors':len(negative),'retained':retained,'witness_sha256':stream.hexdigest(),'masks_sha256':sha256((''.join(str(x)+'\n' for x in masks)).encode()).hexdigest(),'obstructions':[{'order':n,'canonical_mask':mask,'determinant':value,'covered_graphs':num} for (n,mask,value),num in sorted(patterns.items())],'saturated_Gram_entries':checked_entries}


def classify_six():
    masks=rooted_cubic(6);require(len(masks)==7,'incomplete cubic6 cohort')
    types=Counter();spectra={}
    for mask in masks:
        p=adjacency(6,mask);q=[[p[i][j]+(i==j) for j in range(6)] for i in range(6)]
        char=characteristic(q)
        if char==roots_polynomial([4,1,1,1,1,-2]):kind='K3,3';positive=5
        elif char==roots_polynomial([4,2,1,1,-1,-1]):kind='triangular prism';positive=4
        else:raise ValueError('unexpected exact cubic6 spectrum')
        types[kind]+=1;spectra[kind]={'characteristic_polynomial_descending':char,'positive_dimension':positive}
    require(dict(types)=={'K3,3':1,'triangular prism':6},'incorrect cubic6 types')
    return {'graphs':len(masks),'type_counts':dict(sorted(types.items())),'spectra':spectra,'Z_positive_dimension_lower_bound_by_number_K33_blocks':[8,9,10],'Z_nullity_upper_bound_by_number_K33_blocks':[4,3,2]}


def moment_checks():
    checks=0
    # General polynomial sum identity, tested by literal common-neighbor counts.
    for n in range(6):
        pairs=list(combinations(range(n),2))
        for mask in range(1<<len(pairs)):
            p=[[0]*n for _ in range(n)]
            for bit,(i,j) in enumerate(pairs):
                if mask>>bit&1:p[i][j]=p[j][i]=1
            h=list(map(sum,p));S=sum(h);T=sum(x*x for x in h)
            total=2*S
            for i,j in pairs:
                common=sum(p[i][k]*p[j][k] for k in range(n))
                entry=(2*h[i]+2*h[j]-8-common) if p[i][j] else (h[i]+h[j]-3-common)
                total+=2*entry
            require(total==T+(2*n-4)*S-3*n*(n-1),'two-root moment identity failed')
            checks+=1
    red=[]
    for threes in range(9):
        S=8+2*threes;T=8+8*threes
        require(T==4*S-24,'odd degree identity')
        value=T+12*S-168
        require(value-16*S+192==0,'square identity failed')
        # Every outside degree equals4, forcing2S=12*4.
        red.append({'degree_three_count':threes,'row_sum':2*S,'square_sum':value,'allowed_after_zero_square_identity':2*S==48})
    require([x['degree_three_count'] for x in red if x['allowed_after_zero_square_identity']]==[8],'wrong red survivor')
    # Sharp integer Cauchy cost using a generating recurrence, not inequality5r-6.
    cost={0:0}
    for _ in range(14):
        nxt={}
        for total,value in cost.items():
            for r in range(7):
                key=total+r;nxt[key]=min(nxt.get(key,10**9),value+r*r)
        cost=nxt
    require(cost[36]==96,'wrong blue minimum square sum')
    return {'generic_moment_graphs':checks,'blue_required_square_sum':72,'blue_minimum_square_sum':cost[36],'red_cases':red}


def centered_rank():
    gram=[[4*(i==j)-(i//4==j//4) for j in range(8)] for i in range(8)]
    subset=[0,1,2,4,5,6];minor=determinant([[gram[i][j] for j in subset] for i in subset])
    require(minor==256,'wrong centered rank minor')
    require(characteristic(gram)==roots_polynomial([4]*6+[0]*2),'wrong centered rank spectrum')
    # Direct local blue-pair and red-pair saturated Gram algebra on6C and8C.
    matching={(0,1),(2,3),(4,5)};blue=[]
    for i in range(6):
        row=[]
        for j in range(6):
            if i==j:value=6
            elif tuple(sorted((i,j))) in matching:value=2
            else:value=1
            row.append(value)
        blue.append(row)
    require(sum(map(sum,blue))==72,'blue Gram moment')
    return {'centered_rank':6,'centered_positive_minor':minor,'centered_Gram_entries':64,'blue_Gram_total':72}


def edge_window():
    feasible=[(t,e) for t in range(8) for e in range(11) if 2*e+t>=7]
    edges=[98+t+e for t,e in feasible]
    require(len(feasible)==72 and min(edges)==102 and max(edges)==115,'conditional edge bounds failed')
    return {'integer_cases':72,'edges':[min(edges),max(edges)],'endpoint_scalar_cases':{'lower':[[t,e] for t,e in feasible if 98+t+e==102],'upper':[[t,e] for t,e in feasible if 98+t+e==115]},'not_endpoint_realizability':True}


def controls():
    tests=[lambda:adjacency(8,0),lambda:adjacency(8,1<<28),lambda:determinant([[1,2],[3]])]
    p=[[0]*5 for _ in range(5)]
    for bit,(i,j) in enumerate(combinations(range(5),2)):
        if 62>>bit&1:p[i][j]=p[j][i]=1
    validate_negative_minor(p,list(range(5)),-4)
    tests +=[lambda:validate_negative_minor(p,[0,0],-4),lambda:validate_negative_minor(p,list(range(5)),-5),lambda:validate_negative_minor(p,[0,1],1),lambda:validate_negative_minor(p,[0,1,5],-4)]
    wrong=[row[:] for row in p];wrong[0][2]=wrong[2][0]=0
    tests.append(lambda:validate_negative_minor(wrong,list(range(5)),-4))
    def bad_coverage():require(rooted_cubic(8)[:-1]==rooted_cubic(8),'omitted cubic graph')
    tests.append(bad_coverage)
    for test in tests:
        try:test()
        except ValueError:pass
        else:raise ValueError('malformed evidence accepted')
    return len(tests)


def run():
    result={'agent':'six-reviewer-2','role':'independent mathematical reviewer','scope':'At most one degree-seven vertex in any22-vertex ordinary red-B4/blue-B7 witness; conditional105..115edge window (older102..115also audited)','status':'exact independent local audit plus written unformalized proof; unrestricted Ramsey gap unresolved','cubic8':classify_eight(),'cubic6':classify_six(),'moments':moment_checks(),'rank':centered_rank(),'conditional_edges':edge_window(),'negative_controls':controls(),'sharp_window':sharp_window_audit()}
    parser=argparse.ArgumentParser();parser.add_argument('--expected',type=Path);args=parser.parse_args()
    if args.expected is not None:
        require(result==json.loads(args.expected.read_text()),'expected output mismatch')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':run()
