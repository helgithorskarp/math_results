"""Fresh exact ENTRY-POSITIVE q18 capped-H verifier: standard library only.

Adapted from public D3 q16 check.py at52ce9643a4eb700056e37c0df6e3ed3736f71808.
No q16 certificate, executable or PSD margin is imported.

No numerical optimizer, original affine table, author repair generator,
sector decoder, or approximate Cholesky routine is imported.  Every
original matrix entry, actual-empty completion, and all277 basis images
are reconstructed.  Small dyadic factors are treated as untrusted data.
"""
from fractions import Fraction as F
from itertools import combinations
from math import lcm
from pathlib import Path
import argparse
import hashlib
import json
import sys

BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE))


def require(ok,msg):
    if not ok:raise ValueError(msg)


def carrier():
    # A separate core/outside census, followed by complete downclosure checks.
    X=[]
    for c in range(8):
        allowed=range(1,3) if c==0 else (0,1) if c.bit_count() in (1,2) else (0,)
        for r in allowed:
            for T in combinations(range(18),r):
                if c==6 and r==1 and T[0]<9:continue
                X.append(c+sum(1<<(t+3) for t in T))
    X.sort();require(len(X)==277 and X[0]==1,'fresh proper carrier N278')
    require(all(B in X or B==0 for A in X for B in (A^(1<<j) for j in range(21) if A&(1<<j))),
            'entire fresh downward closure')
    O=[(A&7,((A>>3)&511).bit_count(),(A>>12).bit_count()) for A in X]
    K=sorted(set(O));require(len(K)==23,'all fresh physical member orbits')
    return X,O,K


def original_matrix(data,X,O):
    n=len(X);D=data['free_original_entry_denominator']
    require(D==148635648 and type(D) is int,'explicit common endpoint denominator148635648')
    keys=sorted({tuple(sorted((O[i],O[j]))) for i in range(n) for j in range(i+1,n)
                 if not X[i]&X[j] and X[i]!=1 and X[j]!=1})
    require(data['free_original_entry_orbit_keys']==[[list(x) for x in key] for key in keys]
            and len(keys)==143,'EVERY actual free orbit in canonical order, no missing/extras')
    values=data['free_original_entry_numerators']
    require(len(values)==143 and all(type(x) is int for x in values),'all143 exact original coefficients')
    weights=dict(zip(keys,values));a=X.index(1);S=[i for i,A in enumerate(X) if A&1]
    C=[[0]*n for _ in X]
    for i,A in enumerate(X):
        for j,B in enumerate(X):
            C[i][j]=(57*D if A==B else -D if A&B else
                     0 if A==1 or B==1 else weights[tuple(sorted((O[i],O[j])))])
    for i,A in enumerate(X):
        if A&1:continue
        C[i][a]=C[a][i]=-sum(C[i][j] for j in S if j!=a)
    require(all(C[i][j]==C[j][i] and (A!=B or C[i][j]==57*D)
                and (A==B or not A&B or C[i][j]==-D)
                for i,A in enumerate(X) for j,B in enumerate(X)), 'ALL original symmetry/diagonal/support positions')
    require(all(sum(C[i][j] for j in S)==0 for i in range(n)), 'ALL original maximum-star kernel rows')
    U=[[278*D*int(i==j)-D-C[i][j] for j in range(n)] for i in range(n)]
    return C,U,D,S


def sparse(v):return {i:x for i,x in enumerate(v) if x}


def dot(v,w):return sum(x*w.get(i,0) for i,x in v.items())


def full_basis(X,O,K):
    TT=[[int(o==key) for o in O] for key in K]
    standard={};orders={}
    for name,offset,countpos in (('Z',3,1),('W',12,2)):
        orders[name]=[o for o in K if o[countpos]>0]
        standard[name]=[[[(int(bool(A&(1<<offset)))-int(bool(A&(1<<(offset+j)))))*int(o==key)
                           for A,o in zip(X,O)] for key in orders[name]] for j in range(1,9)]
    pair={};free_pair=list(e for e in combinations(range(1,9),2) if e!=(1,2))
    for name,offset in (('ZZ',3),('WW',12)):
        cols=[]
        for i,j in free_pair:
            edge={(i,j):2,(1,2):-2}
            for t in range(1,9):edge[0,t]=-2*int(t in (i,j))+2*int(t in (1,2))
            cols.append([edge.get(tuple(t for t in range(9) if A&(1<<(offset+t))),0)
                         if A&7==0 and A.bit_count()==2 else 0 for A in X])
        pair[name]=cols
        # Unique free-edge coordinate2 certifies all27 columns independent.
        require(all(cols[i][X.index(sum(1<<(offset+t) for t in edge))]==2*int(i==j)
                    for i in range(27) for j,edge in enumerate(free_pair)), 'entire pair-basis independence decoder')
        require(all(sum(col[X.index((1<<(offset+t))+(1<<(offset+r)))] for r in range(9) if r!=t)==0
                    for col in cols for t in range(9)), 'entire pair-basis zero incidence')
    mixed=[[(int(bool(A&8))-int(bool(A&(1<<(3+i)))))*
            (int(bool(A&(1<<12)))-int(bool(A&(1<<(12+j)))))
            if A&7==0 and A.bit_count()==2 else 0 for A in X] for i in range(1,9) for j in range(1,9)]
    require(all(mixed[(i-1)*8+j-1][X.index((1<<(3+r))+(1<<(12+t)))]==int(i==r and j==t)
                for i in range(1,9) for j in range(1,9) for r in range(1,9) for t in range(1,9)),
            'whole64 rectangle independence decoder')
    blocks={'TT':TT,'Z':[v for B in standard['Z'] for v in B],
            'W':[v for B in standard['W'] for v in B],**pair,'ZW':mixed}
    require({k:len(v) for k,v in blocks.items()}=={'TT':23,'Z':64,'W':72,'ZZ':27,'WW':27,'ZW':64},
            'exact full277 coordinate dimensions')
    sp={name:list(map(sparse,B)) for name,B in blocks.items()}
    require(all(dot(v,w)==0 for name,B in sp.items() for other,E in sp.items() if name<other
                for v in B for w in E), 'ALL cross-sector original Gram entries zero')
    require(all(dot(v,w)==(dot(v,v) if i==j else 0) for i,v in enumerate(sp['TT']) for j,w in enumerate(sp['TT'])),
            'whole TT orthogonal independence')
    norms={name:[dot(sparse(v),sparse(v)) for v in standard[name][0]] for name in ('Z','W')}
    for name in ('Z','W'):
        d=len(standard[name][0]);require(d==len(norms[name]) and all(v>0 and v%2==0 for v in norms[name]),'standard positive norms')
        require(all(dot(sparse(standard[name][r][i]),sparse(standard[name][t][j]))==
                    (norms[name][i]//2)*(1+int(r==t))*int(i==j)
                    for r in range(8) for t in range(8) for i in range(d) for j in range(d)),
                'ENTIRE standard Gram: positive norm times(I+J) on every physical orbit')
    seeds={'TT':TT,'Z':standard['Z'][0],'W':standard['W'][0]}
    for name,offset in (('ZZ',3),('WW',12)):
        weights={(0,1):1,(2,3):1,(0,2):-1,(1,3):-1}
        seeds[name]=[[weights.get(tuple(t for t in range(9) if A&(1<<(offset+t))),0)
                      if A&7==0 and A.bit_count()==2 else 0 for A in X]]
    seeds['ZW']=[mixed[0]]
    norms={name:[sum(x*x for x in v) for v in B] for name,B in seeds.items()}
    return blocks,standard,seeds,norms


def gram(A,B):
    sp=list(map(sparse,B))
    return [[sum(x*A[i][j]*y for i,x in v.items() for j,y in w.items()) for w in sp] for v in sp]


def image(A,v):
    sp=sparse(v)
    return [sum(row[j]*x for j,x in sp.items()) for row in A]


def action_block(A,B,G,norm):
    clear=lcm(*norm);count=0
    for c,v in enumerate(B):
        Av=image(A,v)
        for i in range(len(A)):
            require(clear*Av[i]==sum(B[b][i]*G[b][c]*(clear//norm[b]) for b in range(len(B))),
                    'ENTIRE original block action at EACH coordinate')
            count+=1
    return count


def exact_factor(A,D,certificate,norms,floor):
    Q=certificate['factor_denominator'];V=certificate['factor_lower_triangle_numerators'];n=len(A)
    require(type(Q) is int and Q==1<<32 and len(V)==n and all(len(row)==i+1 for i,row in enumerate(V))
            and all(type(x) is int for row in V for x in row),'all fresh dyadic factor values')
    clear=lcm(D,Q*Q);scale=clear//D;fscale=clear//(Q*Q)
    E=[[scale*A[i][j]-fscale*sum(V[i][k]*V[j][k] for k in range(min(i,j)+1)) for j in range(n)] for i in range(n)]
    margins=[E[i][i]-sum(abs(E[i][j]) for j in range(n) if j!=i) for i in range(n)]
    require(min(margins)>0 and margins==certificate['whole_residual_row_margin_numerators']
            and certificate['whole_residual_denominator']==clear,'ALL exact fresh residual margins')
    require(all(F(v,clear*mass)>=floor for v,mass in zip(margins,norms)),
            'EVERY original physical-norm lower bound')
    return min(F(v,clear*mass) for v,mass in zip(margins,norms))


def lift_and_check(C,U,D,X,S,tau):
    """Reconstruct every actual position, at each of the two endpoints."""
    rows=list(map(sum,C));n=len(X);actual=[0]+X
    L=[[D+sum(rows)]+[D-r for r in rows]]+[[D-rows[i]]+[D+x for x in row] for i,row in enumerate(C)]
    M=[[L[i][j]-58*D*int(i==j) for j in range(278)] for i in range(278)]
    require(all(sum(row)==278*D for row in L) and all(sum(row)==220*D for row in M),
            'EVERY actual lower and M row at BOTH endpoints')
    require(all(L[i][j]==L[j][i] and (not A&B or M[i][j]==0)
                for i,A in enumerate(actual) for j,B in enumerate(actual)),
            'EVERY actual symmetry and support position at BOTH endpoints')
    ur=list(map(sum,U));EU=[[sum(ur)]+[-r for r in ur]]+[[-ur[i]]+row for i,row in enumerate(U)]
    require(all(EU[i][j]==278*D*int(i==j)-L[i][j] for i in range(278) for j in range(278)),
            'EVERY actual upper endpoint is EUE transpose')
    centered=[278*int(bool(A&1))-58 for A in actual]
    require(sum(centered)==0 and all(sum(x*y for x,y in zip(row,centered))==0 for row in L),
            'entire centered maximum-star kernel at BOTH endpoints')
    allowed=[M[i][j] for i,A in enumerate(actual) for j,B in enumerate(actual) if not A&B]
    require(len(allowed)==60597 and min(allowed)==D*tau,
            'ALL actual admissible entries attain the claimed endpoint minimum in C units')
    require(M[0][0]==D*tau,'actual EMPTY LOOP has the same exact endpoint floor')
    require(all(M[0][i+1]==D*tau for i,A in enumerate(X)
                if (A&7,((A>>3)&511).bit_count(),(A>>12).bit_count()) in
                ((0,2,0),(0,0,2),(6,0,1),(7,0,0))),
            'ALL82 formerly negative empty incidences have the prescribed endpoint floor')
    return L,M,{'minimum_admissible_M':str(F(min(allowed),220*D)),
                'admissible_ordered_positions':len(allowed),'zero_admissible_positions':allowed.count(0),
                'actual_empty_M_loop':str(F(M[0][0],220*D))}


def line_and_dual(data,C1,U1,D,X,O,S):
    comparison=json.loads((BASE/'COMPARISON.json').read_bytes());old=comparison['comparison_free_numerators']
    require(comparison['comparison_source_commit']=='2bd233ac02ac1c4fc162e7fb4a9a5be8930882d9'
            and comparison['comparison_graph_ref']=='bafkreifday7rxlfyxs2bsab3npasbwbb65sbfv7wslsp3zbz3c774sjway'
            and comparison['comparison_free_denominator']==16384 and len(old)==143
            and all(type(x) is int for x in old)
            and hashlib.sha256(json.dumps(old,separators=(',',':')).encode()).hexdigest()==
            '14cca17e8c9dcf4be01d7abe5700745fc120ea782e84bcc73d25b7df176a4e7d',
            'entire defining comparison table only, no old PSD facts')
    require(data['real_tau_interval']==['0','1/128'],'exact closed REAL parameter interval')
    tauMax=F(1,128);P0=F(476335,32768)
    # Independent expanded constants and slope; not imported from producer.
    terms=[('Zpair-Wpair',(0,2,0),(0,0,2),-F(43503,786432),-F(1,48),1296),
           ('Zpair-bcW',(0,2,0),(6,0,1),-F(999,589824),-F(1,36),324),
           ('Wpair-Wpair',(0,0,2),(0,0,2),-F(14527,1376256),-F(1,84),378),
           ('Zsingle-Wsingle',(0,1,0),(0,0,1),F(476335,2654208),F(41,81),81),
           ('Zsingle-abc',(0,1,0),(7,0,0),-F(20819,147456),-F(1,9),9)]
    recipe={tuple(sorted((x,y))):(name,c,k,count) for name,x,y,c,k,count in terms}
    keys=[tuple(tuple(x) for x in key) for key in data['free_original_entry_orbit_keys']]
    original=dict(data,free_original_entry_numerators=[v*(D//16384) for v in old])
    Cold,_,_,_=original_matrix(original,X,O)
    v0=[];v1=[]
    for key,v in zip(keys,old):
        _,c,k,_=recipe.get(key,('',F(0),F(0),0))
        v0.append(F(v,16384)+c);v1.append(F(v,16384)+c+tauMax*k)
    require(all((v*D).denominator==1 for v in v0+v1),'exact common denominator of BOTH endpoint tables')
    require([int(v*D) for v in v1]==data['free_original_entry_numerators'],
            'EVERY supplied endpoint coefficient equals the literal sparse recipe')
    C0,U0,_,_=original_matrix(dict(data,free_original_entry_numerators=[int(v*D) for v in v0]),X,O)
    KD=lcm(*(k.denominator for _,_,_,_,k,_ in terms));require(KD==9072,'exact original slope denominator')
    K=[[0]*277 for _ in X];counts={name:0 for name,_,_,_,_,_ in terms};a=X.index(1)
    for i,A in enumerate(X):
        for j in range(i+1,277):
            if A&X[j] or A==1 or X[j]==1:continue
            key=tuple(sorted((O[i],O[j])))
            if key in recipe:
                name,c,k,count=recipe[key];K[i][j]=K[j][i]=int(k*KD);counts[name]+=1
    for i,A in enumerate(X):
        if not A&1:K[i][a]=K[a][i]=-sum(K[i][j] for j in S if j!=a)
    require(counts=={name:count for name,_,_,_,_,count in terms},'ENTIRE five orbit edge census')
    require(sum(K[i][a]!=0 for i in range(277))==9
            and all(K[i][a]==(KD//9 if O[i]==(0,1,0) else 0) for i,A in enumerate(X) if not A&1),
            'ALL slope anchors, including exactly nine compensated trades')
    require(all(sum(K[i][j] for j in S)==0 for i in range(277)),'every derivative star-kernel row')
    require(D%(128*KD)==0 and all(C1[i][j]-C0[i][j]==(D//(128*KD))*K[i][j]
                and U1[i][j]-U0[i][j]==-(D//(128*KD))*K[i][j] for i in range(277) for j in range(277)),
            'EVERY original endpoint difference equals tauMax times the literal derivative')
    frob=F(sum(x*x for row in K for x in row),KD*KD)
    require(frob==F(data['claimed_slope_Frobenius_squared'])==F(198145,4536) and frob<49,
            'FULL original derivative Frobenius sum, no orbit-only inference')
    require(F(data['claimed_tauMax_original_floor'])==F(1,16)
            and F(data['claimed_uniform_original_floor'])==F(1,128)
            and F(1,16)-7*tauMax==F(1,128),'ordinary spectral-norm transfer constants')
    L0,M0,rec0=lift_and_check(C0,U0,D,X,S,F(0));L1,M1,rec1=lift_and_check(C1,U1,D,X,S,tauMax)
    kr=list(map(sum,K));LK=[[sum(kr)]+[-r for r in kr]]+[[-kr[i]]+row for i,row in enumerate(K)]
    require(all(L1[i][j]-L0[i][j]==(D//(128*KD))*LK[i][j]
                for i in range(278) for j in range(278)),'ALL actual affine derivative positions')
    rowsold=list(map(sum,Cold));emptyold=[D-r for r in rowsold]
    bad=[i for i,A in enumerate(X) if not A&1 and emptyold[i]<0];badset=set(bad)
    deficit=-sum(emptyold[i] for i in bad);loopold=D+sum(rowsold)-58*D
    require(len(bad)==81 and {O[i] for i in bad}=={(0,2,0),(0,0,2),(6,0,1)}
            and F(deficit,D)==F(2497887,16384) and F(loopold,D)==F(2021552,16384),
            'ALL bad nonstar rows and original empty-loop dual capacities')
    require(F(deficit-loopold,2*D)==P0==F(data['claimed_sharp_positive_NN_mass_intercept'])
            and data['claimed_sharp_positive_NN_mass_slope']==41 and (len(bad)+1)==82,
            'sharp dual intercept and slope from literal original capacities')
    NN=[(i,j) for i,A in enumerate(X) for j in range(i+1,277) if not A&1 and not X[j]&1 and not A&X[j]]
    multiplicities={k:sum(int(i in badset)+int(j in badset)==k for i,j in NN) for k in range(3)}
    accounting={}
    for tau,C,M in ((F(0),C0,M0),(tauMax,C1,M1)):
        P=T=penalty=positive=negative=zero=0
        for i,j in NN:
            r=C[i][j]-Cold[i][j];k=int(i in badset)+int(j in badset)
            P+=max(r,0);T+=max(-r,0);penalty+=k*max(r,0)+(2-k)*max(-r,0)
            positive+=int(r>0);negative+=int(r<0);zero+=int(r==0)
        bslack=sum(M[0][i+1]-D*tau for i in bad);lslack=M[0][0]-D*tau
        require(M[0][0]-loopold==2*(P-T),'ALL original NN changes bind exact empty-loop change')
        require(2*P-(deficit-loopold+82*D*tau)==bslack+lslack+penalty,
                'exact dual identity on the original sparse endpoint')
        require(bslack==lslack==penalty==0 and F(P,D)==P0+41*tau
                and F(T,D)==F(deficit,2*D)+F(81,2)*tau,
                'primal attains every endpoint dual equality condition')
        accounting[str(tau)]={'increasing_unordered_NN_C_mass':str(F(P,D)),
                             'decreasing_unordered_NN_C_mass':str(F(T,D)),
                             'positive_NN_edges':positive,'negative_NN_edges':negative,'zero_NN_edges':zero,
                             'dual_bad_row_slack':str(F(bslack,D)),'dual_loop_slack':str(F(lslack,D)),
                             'dual_edge_penalty':str(F(penalty,D))}
    # Full nonsymmetric REAL affine domain: each nonanchor edge is free,
    # and every forced anchor is recovered by Rh=0. Bind all literal lifts.
    allowed=[(i,j) for i,A in enumerate(X) for j in range(i+1,277) if not A&X[j]]
    free=[(i,j) for i,j in allowed if X[i]!=1 and X[j]!=1]
    require((len(allowed),len(free),len(X)-len(S),len(NN))==(30021,29802,219,19522),
            'full original affine domain and complete NN edge count')
    actual=[0]+X;generators=0
    for i,j in free:
        if not X[i]&1 and not X[j]&1:
            pos={(i+1,j+1):1,(j+1,i+1):1,(0,i+1):-1,(i+1,0):-1,(0,j+1):-1,(j+1,0):-1,(0,0):2}
        else:
            nn=j if X[i]&1 else i;st=i if X[i]&1 else j
            pos={(nn+1,st+1):1,(st+1,nn+1):1,(nn+1,a+1):-1,(a+1,nn+1):-1,
                 (0,st+1):-1,(st+1,0):-1,(0,a+1):1,(a+1,0):1}
        require(all(not actual[r]&actual[c] for r,c in pos)
                and all(sum(v for (r,c),v in pos.items() if r==row)==0 for row in {r for r,c in pos}),
                'EVERY independent real generator full support and actual row identities')
        generators+=1
    hashes={name:hashlib.sha256(json.dumps(A,separators=(',',':')).encode()).hexdigest()
            for name,A in (('original_signed_C',Cold),('tau0_C',C0),('tauMax_C',C1),
                           ('tauMax_U',U1),('tau0_L',L0),('tauMax_L',L1),('slope_K',K))}
    return {'endpoint_entry_checks':{'0':rec0,'1/128':rec1},'five_original_edge_counts':counts,
            'entire_slope_ordered_positions':277**2,'slope_denominator':KD,'slope_Frobenius_squared':str(frob),
            'complete_real_affine_dimension':generators,'complete_unordered_NN_edge_count':len(NN),
            'NN_bad_endpoint_multiplicity_census':multiplicities,'bad_nonstar_rows':len(bad),
            'old_total_bad_nonstar_C_deficit':str(F(deficit,D)),'old_empty_loop_C_capacity':str(F(loopold,D)),
            'endpoint_mass_and_dual_equality':accounting,'sharp_mass_intercept_C_units':str(P0),
            'sharp_mass_slope_C_units':41,'entire_original_matrix_SHA256':hashes,
            'ordinary_universal_REAL_dual_and_equality_characterization_bridge_unformalized':True}


def verify(data):
    require((data['actual_agent'],data['role'],data['q'],data['k'],data['actual_empty_N'],data['maximum_star_s'])==
            ('six-downset-3','researcher',18,9,278,58),'exact finite carrier and authorship')
    X,O,K=carrier();C,U,D,S=original_matrix(data,X,O)
    floor=F(data['claimed_tauMax_original_floor']);require(floor==F(1,16),'exact new endpoint floor')
    stars=[sum(bool(A&(1<<i)) for A in X) for i in range(21)]
    require(stars==[58,49,49]+[23]*9+[24]*9,'all21 exact original stars and unique maximum')
    blocks,standard,seeds,norms=full_basis(X,O,K);actions=0;bounds={};certs=data['positive_sector_certificates']
    require(set(certs)=={a+'_'+b for a in seeds for b in ('lower','upper')},'all12 fresh endpoint certificates')
    for endpoint,A in (('lower',C),('upper',U)):
        for name,B in seeds.items():
            G=gram(A,B)
            if name=='TT':actions+=action_block(A,B,G,norms[name])
            elif name in ('Z','W'):
                for full in standard[name]:actions+=action_block(A,full,G,norms[name])
            else:
                require(len(G)==1 and norms[name]==[4],'actual scalar prototype norm4')
                for v in blocks[name]:
                    Av=image(A,v);require(all(4*x==G[0][0]*y for x,y in zip(Av,v)),
                                         'ENTIRE original scalar basis action')
                    actions+=len(A)
            key=name+'_'+endpoint
            ix=[i for i in range(len(G)) if not(name=='TT' and endpoint=='lower' and K[i]==(1,0,0))]
            H=[[G[i][j] for j in ix] for i in ix]
            if len(H)==1:
                require(certs[key]['scalar_gram_numerator']==H[0][0] and certs[key]['scalar_gram_denominator']==D
                        and F(H[0][0],D*norms[name][0])>=floor,'fresh exact scalar original bound')
                bounds[key]=str(F(H[0][0],D*norms[name][0]))
            else:bounds[key]=str(exact_factor(H,D,certs[key],[norms[name][i] for i in ix],floor))
    require(actions==153458,'both FULL277 original basis actions, no omitted sector')
    line=line_and_dual(data,C,U,D,X,O,S)
    return {'actual_agent':'six-downset-3','role':'researcher','q':18,'k':9,'actual_empty_N':278,'s':58,
            'common_endpoint_denominator':D,'all21_original_star_sizes':stars,
            'complete_original_basis_columns':277,'complete_sector_dimensions':{n:len(B) for n,B in blocks.items()},
            'fresh_tauMax_full_original_basis_actions':actions,'all12_fresh_exact_block_bounds':bounds,
            'tauMax_original_C_on_star_perpendicular_and_U_floor':'1/16',
            'uniform_REAL_parameter_interval':['0','1/128'],'uniform_original_C_and_U_floor':'1/128',
            'uniform_all_admissible_M_floor':'tau/220','strict_entry_positivity_for':'0<tau<=1/128',
            'both_actual_endpoint_ranks_for_ALL_real_tau':277,
            'simple_minimum_M_eigenvalue':'-29/110','simple_maximum_M_eigenvalue':'1',
            'uniform_other276_M_eigenvalue_lower_bound':str(-F(29,110)+F(1,28160)),
            'uniform_other276_M_eigenvalue_upper_bound':str(1-F(1,28160)),
            'sharp_mass_feasible_domain':'ALL real symmetric disjointness-supported M with M1=1, 220M+58I PSD, and every allowed entry>=tau/220',
            'mass_comparison_definition':'positive unordered NONSTAR proper-core changes from the full143 old table',
            'sharp_unrestricted_REAL_H_repair_NN_mass':'476335/32768+41*tau',
            'strict_positive_H_repair_mass_infimum':'476335/32768','strict_positive_infimum_attained':False,
            **line,'ordinary_PSD_basis_norm_lift_line_star_face_and_dual_bridges_unformalized':True,
            'independent_reviewer_verdict':'UNREVIEWED'}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,default=BASE/'CERTIFICATE.json')
    ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    result=verify(json.loads(args.certificate.read_bytes()));raw=(json.dumps(result,sort_keys=True,indent=2)+'\n').encode()
    args.out.write_bytes(raw)
    print(json.dumps({'completed':True,'original_actions':result['fresh_tauMax_full_original_basis_actions'],
                      'uniform_real_floor':result['uniform_original_C_and_U_floor'],
                      'sharp_mass':result['sharp_unrestricted_REAL_H_repair_NN_mass'],
                      'record_SHA256':hashlib.sha256(raw).hexdigest()},sort_keys=True))


if __name__=='__main__':main()
