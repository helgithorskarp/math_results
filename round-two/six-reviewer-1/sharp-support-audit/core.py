"""six-reviewer-1: new exact n24 certificate checker; no author program imports."""
from fractions import Fraction as Q
from itertools import combinations,product
from math import comb,gcd,lcm
from pathlib import Path
import hashlib,json

def need(ok,why):
    if not ok:raise ValueError(why)
def choose(n,k):
    return comb(n,k) if 0<=k<=n else 0
def canonical(x):
    return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)
def rational(x):
    if isinstance(x,Q):return str(x)
    if isinstance(x,list):return [rational(y) for y in x]
    if isinstance(x,tuple):return [rational(y) for y in x]
    if isinstance(x,dict):return {str(k):rational(v) for k,v in x.items()}
    return x
def digest(x):return hashlib.sha256(canonical(rational(x)).encode()).hexdigest()
def pairs(n):return [(a,b) for a in range(1,n-1) for b in range(a,n-1) if a+b<=n]
def complete(n,free):
    s=2**(n-1)-n
    t={(a,b):Q(v) for (a,b),v in free.items()}
    t.update({(b,a):v for (a,b),v in list(t.items())})
    for a in range(2,n-1):
        v=((n-a)*s-sum(b*t.get((a,b),0)*choose(n-a,b) for b in range(2,n-1)))/(n-a)
        t[1,a]=t[a,1]=v
    t[1,1]=Q((n-1)*s-sum(b*t.get((1,b),0)*choose(n-1,b) for b in range(2,n-1)),n-1)
    for a in range(1,n-1):
        need(sum(b*t.get((a,b),0)*choose(n-a,b) for b in range(1,n-1))==(n-a)*s,'whole star equation')
        need(sum(t.get((a,b),0)*choose(n-a-1,b-1) for b in range(1,n-1))==s,'individual excluding-point row')
    return t
def sector(n,t,j):
    N=2**n-n-1;s=2**(n-1)-n
    layers=list(range(max(1,j),min(n-2,n-j)+1))
    metric=[choose(n-2*j,a-j) for a in layers]
    k=[[Q(s*(a==b)-(choose(n,b) if j==0 else 0))+(-1)**j*t.get((a,b),0)*choose(n-a-j,b-j) for b in layers] for a in layers]
    u=[[Q(N*(a==b)-(choose(n,b) if j==0 else 0))-k[i][h] for h,b in enumerate(layers)] for i,a in enumerate(layers)]
    return layers,metric,k,u
def weighted(k,g,shift=Q(0)):
    m=[[g[i]*(k[i][j]-shift*(i==j)) for j in range(len(k))] for i in range(len(k))]
    need(all(m[i][j]==m[j][i] for i in range(len(m)) for j in range(len(m))),'entire weighted symmetry')
    return m
def psd(m):
    """Pivoted integer fraction-free congruence; exact divisions are checked."""
    d=len(m);need(all(len(r)==d for r in m),'square form')
    need(all(m[i][j]==m[j][i] for i in range(d) for j in range(d)),'PSD input symmetry')
    scale=lcm(*(Q(x).denominator for row in m for x in row))
    a=[[int(Q(x)*scale) for x in row] for row in m];order=list(range(d));previous=1;pivots=[]
    while a:
        if any(a[i][i]<0 for i in range(len(a))):return {'psd':False,'rank':None}
        p=next((i for i in range(len(a)) if a[i][i]>0),None)
        if p is None:
            if any(x for row in a for x in row):return {'psd':False,'rank':None}
            break
        if p:
            a[0],a[p]=a[p],a[0]
            for row in a:row[0],row[p]=row[p],row[0]
            order[0],order[p]=order[p],order[0]
        pivot=a[0][0];pivots.append([order.pop(0),pivot])
        b=[]
        for i in range(1,len(a)):
            row=[]
            for j in range(1,len(a)):
                num=pivot*a[i][j]-a[i][0]*a[0][j]
                v,r=divmod(num,previous);need(r==0,'Bareiss exact division')
                row.append(v)
            b.append(row)
        a=b;previous=pivot
    return {'psd':True,'rank':len(pivots),'scale':scale,'full_pivots_sha256':digest(pivots),'zero_residual_order':len(a)}
def rank(a):
    """Separate rational rectangular row reduction; used for literal spans."""
    a=[[Q(x) for x in row] for row in a];r=0
    if not a:return 0
    for c in range(len(a[0])):
        p=next((i for i in range(r,len(a)) if a[i][c]),None)
        if p is None:continue
        a[r],a[p]=a[p],a[r];v=a[r][c];a[r]=[x/v for x in a[r]]
        for i in range(r+1,len(a)):
            v=a[i][c]
            if v:a[i]=[x-v*y for x,y in zip(a[i],a[r])]
        r+=1
        if r==len(a):break
    return r
def schur_psd(m):
    """Separately normalized rational congruences, without Bareiss scaling."""
    a=[[Q(x) for x in row] for row in m];pivots=[]
    while a:
        if any(a[i][i]<0 for i in range(len(a))):return {'psd':False,'rank':None}
        k=next((i for i in range(len(a)) if a[i][i]),None)
        if k is None:
            if any(x for row in a for x in row):return {'psd':False,'rank':None}
            break
        active=[i for i in range(len(a)) if i!=k];p=a[k][k];pivots.append(p)
        a=[[a[i][j]-a[i][k]*a[k][j]/p for j in active] for i in active]
    return {'psd':True,'rank':len(pivots),'full_rational_pivots_sha256':digest(pivots)}
def null(m,v):return [sum(x*y for x,y in zip(row,v)) for row in m]
def star_face(n):
    """Entire real affine decoder, by independent symbolic elimination."""
    pp=pairs(n);ff=[p for p in pp if p[0]>=2];width=len(ff)+1;s=2**(n-1)-n
    table={p:[Q(0)]*width for p in pp}
    for i,p in enumerate(ff):table[p][i+1]=1
    rows=[]
    for a in range(1,n-1):
        row=[]
        for x,y in pp:
            coeff=(y*choose(n-a,y) if x==a else 0)+(x*choose(n-a,x) if y==a and x!=y else 0)
            row.append(Q(coeff))
        rows.append(row+[Q((n-a)*s)])
    # Singleton coordinates are the first n-2 variables, but all143 columns remain.
    for p in range(n-2):
        k=next(i for i in range(p,len(rows)) if rows[i][p])
        rows[k],rows[p]=rows[p],rows[k];v=rows[p][p];rows[p]=[x/v for x in rows[p]]
        for i in range(len(rows)):
            v=rows[i][p]
            if i!=p and v:rows[i]=[x-v*y for x,y in zip(rows[i],rows[p])]
    for i,p in enumerate(pp[:n-2]):table[p]=[rows[i][-1]]+[-x for x in rows[i][n-2:-1]]
    need(all(rows[i][j]==int(i==j) for i in range(n-2) for j in range(n-2)),'whole affine pivots')
    # The direct completion differentiated on every free-coordinate axis.
    origin=complete(n,{p:Q(0) for p in ff})
    for k,p in enumerate(ff):
        one=complete(n,{q:Q(q==p) for q in ff})
        for q in pp:need(one.get(q,0)-origin.get(q,0)==table[q][k+1],'entire affine derivative agreement')
    for q in pp:need(table[q][0]==origin.get(q,0),'whole affine constants')
    return {'variables':len(pp),'rank':n-2,'free':len(ff),'entire_affine_map_sha256':digest(table)}
def matchings(points):
    if not points:
        yield ()
        return
    a=points[0]
    for b in points[1:]:
        for rest in matchings(tuple(x for x in points[1:] if x!=b)):
            yield ((a,b),)+rest
def value(mask,matching):
    out=1
    for a,b in matching:out*=((mask>>a)&1)-((mask>>b)&1)
    return out
def literal():
    """Full paired-harmonic basis and original affine matrices at n6."""
    n=6;F=[x for x in range(1,1<<n) if x.bit_count()<=n-2];N=len(F)+1;s=26
    cols=[];spec=[];layer_dim=[];all_matches=0
    for j in range(4):
        jsets=[x for x in range(1<<n) if x.bit_count()==j];chosen=[];vecs=[]
        for points in combinations(range(n),2*j):
            for matching in matchings(points):
                all_matches+=1;v=[value(mask,matching) for mask in jsets]
                if rank(vecs+[v])>len(vecs):vecs.append(v);chosen.append(matching)
        need(len(chosen)==choose(n,j)-choose(n,j-1),'literal harmonic dimension')
        layer_dim.append(len(chosen))
        for matching in chosen:
            norm=sum(value(mask,matching)**2 for mask in jsets)
            for b in range(max(1,j),min(n-2,n-j)+1):
                col=[value(mask,matching) if mask.bit_count()==b else 0 for mask in F]
                need(sum(x*x for x in col)==choose(n-2*j,b-j)*norm,'literal harmonic metric')
                cols.append(col);spec.append((j,b,matching))
    need(len(cols)==len(F) and rank(cols)==len(F),'entire literal harmonic span')
    records=[]
    for variant in [0,1]:
        free={(a,b):Q((-1)**(a+b)*(a*a+b*b+1+variant*(a==2 and b==2)),17) for a,b in pairs(n) if a>=2}
        t=complete(n,free)
        C=[[Q(s*(A==B)-1)+(t.get((A.bit_count(),B.bit_count()),0) if A&B==0 else 0) for B in F] for A in F]
        U=[[Q(N*(i==k)-1)-C[i][k] for k in range(len(F))] for i in range(len(F))]
        action=[]
        for j,b,matching in spec:
            layers,g,k,u=sector(n,t,j);h=layers.index(b)
            col=[value(mask,matching) if mask.bit_count()==b else 0 for mask in F]
            for m,coeff in [(C,k),(U,u)]:
                actual=null(m,col)
                predicted=[coeff[layers.index(A.bit_count())][h]*value(A,matching) if A.bit_count() in layers else 0 for A in F]
                need(actual==predicted,'all original literal harmonic action coordinates')
                action.append(actual)
        rowsums=[sum(row) for row in C];empty=1+sum(rowsums)
        L=[[Q(empty)]+[1-x for x in rowsums]]+[[1-rowsums[i]]+[1+x for x in C[i]] for i in range(len(F))]
        allF=[0]+F
        need(all(sum(row)==N for row in L),'whole actual original row sums')
        need(all(L[i][k]==s*(i==k) for i,A in enumerate(allF) for k,B in enumerate(allF) if A&B),'whole original intersection support')
        need(all(null(L,[int(A&(1<<point)!=0) for A in allF])==[s]*N for point in range(n)),'all original point star equations')
        E=[[-1]*len(F)]+[[int(i==k) for k in range(len(F))] for i in range(len(F))]
        # Every original position of the cap congruence, retaining actual empty row.
        EU=[[sum(E[i][h]*U[h][k] for h in range(len(F))) for k in range(len(F))] for i in range(N)]
        cap=[[sum(EU[i][h]*E[k][h] for h in range(len(F))) for k in range(N)] for i in range(N)]
        need(all(cap[i][k]==N*(i==k)-L[i][k] for i in range(N) for k in range(N)),'whole original empty cap lift')
        records.append({'variant':variant,'table':[[a,b,t[a,b]] for a,b in pairs(n)],'whole_actions_sha256':digest(action),'whole_original_lower_sha256':digest(L),'whole_original_upper_sha256':digest(cap),'actual_empty_loop':empty,'action_columns':len(action),'action_positions':len(action)*len(F)})
    return {'n':n,'nonempty':len(F),'dimension_by_degree':layer_dim,'all_pairings_scanned':all_matches,'basis_columns':len(cols),'controls':records,'PSD_or_cap_feasibility_claimed_for_affine_controls':False}
def arithmetic_controls():
    records=[]
    for x in product([-1,0,1],repeat=6):
        a,b,c,d,e,f=x;m=[[a,b,c],[b,d,e],[c,e,f]]
        determinant=a*d*f+2*b*c*e-a*e*e-d*c*c-f*b*b
        criterion=min(a,d,f,a*d-b*b,a*f-c*c,d*f-e*e,determinant)>=0
        result=psd(m)
        need(result['psd']==criterion,'all ternary principal-minor controls')
        alternate=schur_psd(m)
        need(alternate['psd']==result['psd'] and alternate['rank']==result['rank'],'all ternary algorithms agree')
        if criterion:need(result['rank']==rank(m),'all ternary rank controls')
        records.append([list(x),criterion,result['rank']])
    return {'all729_sha256':digest(records),'count':len(records),'PSD':sum(row[1] for row in records)}
def run():
    root=Path(__file__).resolve().parent;seed=json.loads((root/'seed.json').read_text())
    need(seed['n']==24 and type(seed['n']) is int and seed['r']==22 and seed['N']==16777191 and seed['s']==8388584 and seed['proper_support_cutoff']==6 and seed['star_only'] is True,'exact seed domain')
    ff=[p for p in pairs(24) if p[0]>=2]
    need(seed['free_pairs']==[list(p) for p in ff] and len(seed['free_values'])==len(ff),'entire free face census')
    need(all(isinstance(x,str) and str(Q(x))==x for x in seed['free_values']),'canonical rational seed')
    free=dict(zip(ff,map(Q,seed['free_values'])));t=complete(24,free)
    need(all(10**9%v.denominator==0 for v in free.values()),'rational denominator')
    excluded=[p for p in ff if min(p)>6 and sum(p)<24]
    need(len(excluded)==30 and all(free[p]==0 for p in excluded),'every proper S6 zero')
    need(free[6,6]>0,'S5 violation of this witness')
    N=16777191;s=8388584;h=N-s;sectors=[];total=0;nullity=0
    for j in range(13):
        layers,g,k,u=sector(24,t,j);d=len(layers);multiplicity=choose(24,j)-choose(24,j-1);total+=d*multiplicity
        lower=weighted(k,g);upper=weighted(u,g);gap=weighted(u,g,Q(1,64))
        a,b,c=psd(lower),psd(upper),psd(gap)
        need(a['psd'] and a['rank']==d-(j<2),'every full lower sector')
        need(b['psd'] and b['rank']==d and c['psd'] and c['rank']==d,'every full upper and cap gap')
        if j<2:need(not any(null(k,layers if j==0 else [1]*d)),'whole required kernel vector')
        nullity+=(d-a['rank'])*multiplicity
        improvement=psd(weighted(u,g,Q(1,32)))
        alternate=[schur_psd(form) for form in [lower,upper,gap,weighted(u,g,Q(1,32))]]
        need(all(x['psd']==y['psd'] and x['rank']==y['rank'] for x,y in zip([a,b,c,improvement],alternate)),'every whole n24 form agrees between algorithms')
        sectors.append({'degree':j,'layers':layers,'metric':g,'multiplicity':multiplicity,'lower':a,'upper':b,'gap1_64':c,'complete_four_forms_sha256':digest([lower,upper,gap,weighted(u,g,Q(1,32))]),'gap1_32':improvement,'separate_schur':alternate})
    need(total==N-1 and nullity==24,'entire original harmonic count')
    rows=[s-(N-1)+sum(t.get((a,b),0)*choose(24-a,b) for b in range(1,23)) for a in range(1,23)]
    empty=1+sum(choose(24,a)*rows[a-1] for a in range(1,23))
    need(empty==Q(195179316200979,25000000),'actual n24 empty scaled diagonal')
    mass=[];positive=0
    for a,b in pairs(24):
        if a>=6 and a+b<24 and t[a,b]>0:
            count=choose(24,a)*choose(24-a,b)//(1+(a==b))
            contribution=count*t[a,b]/h;positive+=contribution;mass.append([a,b,count,t[a,b],contribution])
            need(a==6,'every positive near-middle class touches layer6')
    need(positive==Q(166653712846621,131071984375000),'entire original unordered positive mass')
    need(6*sum(a*a*choose(24,a) for a in range(3,6))<=s-12*24**2,'imported all-real S5 scalar')
    damages=[]
    for label,bad in [('negative-diagonal',[[-1,0],[0,1]]),('zero-diagonal-nonzero-offdiagonal',[[0,1],[1,1]]),('negative-Schur',[[1,2],[2,1]])]:
        need(not psd(bad)['psd'],'PSD damage rejection');damages.append(label)
    wrong=dict(t);wrong[7,7]=Q(1)
    need(any(wrong.get(p,0)!=0 for p in excluded),'missing proper S6 condition damage');damages.append('excluded-proper-pair')
    need(sum(choose(24,j)-choose(24,j-1) for j in range(13))>0,'harmonic census sanity')
    return rational({'domain':{'n':24,'N':N,'s':s,'h':h,'cutoff':6,'rank_lower':N-nullity,'rank_upper':N-1,'full_original_gap':str(Q(1,64)),'certified_gap1_32':all(x['gap1_32']['psd'] and x['gap1_32']['rank']==len(x['layers']) for x in sectors)},'whole_seed_sha256':hashlib.sha256((root/'seed.json').read_bytes()).hexdigest(),'whole_table':[[a,b,t[a,b]] for a,b in pairs(24)],'affine':star_face(24),'excluded_pairs':excluded,'sectors':sectors,'core_rows':rows,'actual_empty_diagonal':empty,'positive_original_classes':mass,'total_original_positive_mass':positive,'literal':literal(),'arithmetic':arithmetic_controls(),'mathematical_damages':damages})
