"""Independent original q19 witness audit; exact stdlib arithmetic only.

Input is attributed defining mathematical data, not an author certificate.
No author code, validator, factor or EXPECTED file is imported or executed.
"""
from fractions import Fraction as F
from itertools import combinations
from math import comb, lcm
import hashlib
import json
from pathlib import Path
import sys

from literal import need, pair_kernel, rank_mod

ROOT = Path(__file__).resolve().parent
TAU_MAX = F(219061, 3080192)
P0 = F(8421443, 65536)
RESIDUAL_FLOOR = F(1,512)
N, S, H = 303, 61, 242
X = tuple(range(3, 12))
Y = tuple(range(12, 22))
XM = sum(1 << i for i in X)
YM = sum(1 << i for i in Y)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def rat(value):
    value = F(value)
    return [value.numerator, value.denominator]


def choose(n, r):
    return comb(n, r) if 0 <= r <= n else 0


def vtype(a):
    return (a & 7, (a & XM).bit_count(), (a & YM).bit_count())


def source_table(damage):
    raw = (ROOT/'COEFFICIENTS.json').read_bytes()
    need(len(raw) == 26316 and hashlib.sha256(raw).hexdigest() ==
         '65f2b0a5170e0a7585d4892c33d72aca7e4479d0e3484dc98ee32b0ad27f1105',
         'entire attributed defining input')
    data = json.loads(raw)
    need((data['q'], data['k'], data['N'], data['s'], data['h'],
          data['denominator'], data['free_pair_type_count']) ==
         (17, 8, 255, 55, 200, 32768, 143), 'defining q17 metadata, not a PSD premise')
    rows = data['free_pair_values']
    if damage == 'duplicate-key':
        rows = rows[:-1] + [rows[0]]
    table = {}
    for row in rows:
        pair = tuple(sorted(tuple(t) for t in row['types']))
        need(len(pair) == 2 and pair not in table, 'unique complete unordered table keys')
        numerator = row['numerator']
        need(type(numerator) is int and numerator % 31 == 0, 'exact31 division')
        table[pair] = F(29 * (numerator // 31), 32768)
    need(len(table) == 143, 'all143 defining parameters')
    if damage == 'coefficient':
        table[min(table)] += F(1, 32768)
    return table


def build(damage=None):
    vertices = [0] + [1 << i for i in range(22)]
    vertices += [(1 << i) | (1 << j) for i, j in combinations(range(22), 2)]
    vertices += [7]
    vertices += [3 | (1 << i) for i in X + Y]
    vertices += [5 | (1 << i) for i in X + Y]
    vertices += [6 | (1 << i) for i in Y]
    vertices.sort(key=lambda a: (a.bit_count(), a))
    need(len(vertices) == len(set(vertices)) == N, 'complete literal downset303')
    star_sizes = [sum(bool(a & (1 << i)) for a in vertices) for i in range(22)]
    need(star_sizes == [61, 52, 52] + [24]*9 + [25]*10, 'every original star, unique maximum')
    q = [a for a in vertices if a not in (0, 1)]
    proper = [a for a in vertices if a]
    need(len(q) == 301 and len(proper) == 302, 'entire original residual and proper dimensions')
    qi = {a:i for i,a in enumerate(q)}
    pi = {a:i for i,a in enumerate(proper)}
    table = source_table(damage)
    types = sorted(set(map(vtype, q)))
    active = {tuple(sorted((vtype(a), vtype(b)))) for i,a in enumerate(q) for b in q[i+1:] if not a&b}
    need(len(types) == 22 and set(table) == active, 'literal active143 pair-type census')
    c = [[F(0) for _ in proper] for _ in proper]
    slope = [[F(0) for _ in proper] for _ in proper]
    for a in q:
        for b in q:
            c[pi[a]][pi[b]] = F(60) if a == b else F(-1) if a&b else table[tuple(sorted((vtype(a),vtype(b))))]
    for a in q:
        c[pi[a]][pi[1]] = c[pi[1]][pi[a]] = -sum(c[pi[a]][pi[b]] for b in q if b&1)
    c[pi[1]][pi[1]] = F(60)
    for i,a in enumerate(proper):
        need(sum(c[i][pi[b]] for b in proper if b&1) == 0, 'literal comparison whole-star kernel')
        for j,b in enumerate(proper):
            need(c[i][j] == c[j][i] and (a == b or not a&b or c[i][j] == -1), 'comparison proper support/symmetry')
    baseline = [[x for x in row] for row in c]
    budgets = [1-sum(row) for row in baseline]
    loop = 1 + sum(map(sum, baseline)) - S
    bad = {a for a in proper if not a&1 and budgets[pi[a]] < 0}
    need(len(bad) == 75, 'complete bad nonstar census')
    deficits = {(0,0,2):F(362147,32768),(2,0,1):F(10683,32768),
                (4,0,1):F(10683,32768),(6,0,1):F(13379,16384)}
    for a in proper:
        if not a&1:
            need((a in bad) == (vtype(a) in deficits), 'all individual bad types')
            if a in bad:
                need(budgets[pi[a]] == -deficits[vtype(a)], 'each original comparison deficit')
    need(loop == F(2089103,8192) and sum(-budgets[pi[a]] for a in bad) == F(16777855,32768), 'original loop and every bad degree')
    need((sum(-budgets[pi[a]] for a in bad)-loop)/2 == P0, 'original cost lower bound')
    special = {(1,0,1):F(18079,32768),(3,0,1):F(-11507,16384),
               (5,0,1):F(-11507,16384),(7,0,0):F(-66079,32768)}
    for a in proper:
        if vtype(a) in special:
            need(budgets[pi[a]] == special[vtype(a)], 'each stated star budget')
    need(budgets[pi[1]] == F(527991,32768), 'comparison anchor budget')

    def change(a, b, intercept, gradient):
        need(a != b and not a&b, 'proper trade is supported offdiagonal')
        i,j = pi[a],pi[b]
        c[i][j] += intercept
        c[j][i] += intercept
        slope[i][j] += gradient
        slope[j][i] += gradient

    beta0, beta1 = F(13379,16384*36), F(1,36)
    eta0, eta1 = F(10683,32768*9), F(1,9)
    alpha0, alpha1 = (F(362147,32768)-8*beta0)/28, (1-8*beta1)/28
    counts = {'YY/YY':0,'YY/bcY':0,'bY/cY':0,'XX/XX':0,'X/X':0,'Y/Y':0,'anchored':0,'release':0}
    for i,a in enumerate(q):
        for b in q[i+1:]:
            if a&b:
                continue
            pair=tuple(sorted((vtype(a),vtype(b))))
            if pair == ((0,0,2),(0,0,2)):
                change(a,b,-alpha0,-alpha1);counts['YY/YY']+=1
            elif pair == ((0,0,2),(6,0,1)):
                change(a,b,-beta0,-beta1);counts['YY/bcY']+=1
            elif pair == ((2,0,1),(4,0,1)):
                change(a,b,-eta0,-eta1);counts['bY/cY']+=1
            elif pair == ((0,2,0),(0,2,0)):
                change(a,b,P0/1512,F(38,1512));counts['XX/XX']+=1
            elif pair == ((0,1,0),(0,1,0)):
                change(a,b,P0/72,F(38,72));counts['X/X']+=1
            elif pair == ((0,0,1),(0,0,1)):
                change(a,b,P0/180,F(38,180));counts['Y/Y']+=1
    for a in proper:
        if vtype(a) not in special:
            continue
        if damage == 'omit-aY' and vtype(a) == (1,0,1):
            continue
        for x in X:
            change(a,1<<x,special[vtype(a)]/9,F(-1,9))
            change(1,1<<x,-special[vtype(a)]/9,F(1,9))
            counts['anchored']+=1
    for a in proper:
        if vtype(a) == (0,0,2):
            if damage != 'release-sign':
                change(7,a,F(0),F(-1))
            else:
                change(7,a,F(0),F(1))
            change(1,a,F(0),F(1));counts['release']+=1
    need(counts == {'YY/YY':630,'YY/bcY':360,'bY/cY':90,'XX/XX':378,'X/X':36,'Y/Y':45,'anchored':279,'release':45}, 'all literal affine trade coordinates')
    for i,a in enumerate(proper):
        need(sum(c[i][pi[b]] for b in proper if b&1) == 0 and sum(slope[i][pi[b]] for b in proper if b&1) == 0, 'affine original whole-star kernel')
    denominators = [x.denominator for matrix in (c,slope,baseline) for row in matrix for x in row]
    denominator = lcm(*denominators)
    c0 = [[int(x*denominator) for x in row] for row in c]
    c1 = [[int(x*denominator) for x in row] for row in slope]
    original0 = [[0 for _ in vertices] for _ in vertices]
    original1 = [[0 for _ in vertices] for _ in vertices]
    vi = {a:i for i,a in enumerate(vertices)}
    for i,a in enumerate(proper):
        ii = vi[a]
        for j,b in enumerate(proper):
            jj=vi[b]
            original0[ii][jj]=c0[i][j]+denominator-S*denominator*int(a==b)
            original1[ii][jj]=c1[i][j]
        original0[0][ii]=original0[ii][0]=denominator-sum(c0[i])
        original1[0][ii]=original1[ii][0]=-sum(c1[i])
    original0[0][0]=(1-S)*denominator+sum(map(sum,c0))
    original1[0][0]=sum(map(sum,c1))
    if damage == 'empty-loop':
        original0[0][0] -= 1
    return dict(V=vertices,Q=q,proper=proper,qi=qi,pi=pi,types=types,table=table,baseline=baseline,bad=bad,
                c0=c0,c1=c1,hM0=original0,hM1=original1,den=denominator,counts=counts)


def physical_basis(data, damage):
    q=data['Q'];types=data['types']
    orbits=[[i for i,a in enumerate(q) if vtype(a)==t] for t in types]
    basis=[]
    def put(sector,t,values,aux=None):
        v={i:x for i,x in zip(orbits[t],values) if x}
        need(bool(v), 'nonzero physical vector')
        basis.append(dict(sector=sector,t=t,v=v,aux=aux))
    for t,o in enumerate(orbits):put('constant',t,[1]*len(o))
    for sector,pool,slot in (('X',X,1),('Y',Y,2)):
        for t,o in enumerate(orbits):
            if not types[t][slot]:continue
            for x in pool[:-1]:
                put(sector,t,[int(bool(q[i]&(1<<x)))-int(bool(q[i]&(1<<pool[-1]))) for i in o],x)
    for sector,pool,typ in (('XX',X,(0,2,0)),('YY',Y,(0,0,2))):
        t=types.index(typ)
        for kernel in pair_kernel(len(pool)):
            put(sector,t,[kernel[tuple(z for z,x in enumerate(pool) if q[i]&(1<<x))] for i in orbits[t]])
    t=types.index((0,1,1))
    for x in X[:-1]:
        for y in Y[:-1]:
            put('XY',t,[(int(bool(q[i]&(1<<x)))-int(bool(q[i]&(1<<X[-1])))) *
                        (int(bool(q[i]&(1<<y)))-int(bool(q[i]&(1<<Y[-1])))) for i in orbits[t]])
    if damage == 'basis':basis[-1]=basis[-2]
    need(len(basis)==301 and rank_mod([[b['v'].get(i,0) for b in basis] for i in range(301)])==301, 'full physical determinant modulo1009')
    census={sector:sum(b['sector']==sector for b in basis) for sector in ('constant','X','Y','XX','YY','XY')}
    need(census==dict(constant=22,X=64,Y=81,XX=27,YY=35,XY=72),'all301 physical coordinates')
    grams=[]
    for b in basis:
        row=[]
        for u in basis:
            g=sum(value*u['v'].get(i,0) for i,value in b['v'].items())
            need(b['sector']==u['sector'] or g==0,'every cross-sector Gram entry')
            if b['sector'] in ('constant','X','Y'):
                need(b['t']==u['t'] or g==0,'every different-orbit Gram entry')
                if b['t']==u['t'] and b['sector']==u['sector']:
                    if b['sector']=='constant':
                        expected=len(orbits[b['t']])
                    else:
                        _,it,jt=types[b['t']]
                        weight=choose(7,it-1)*choose(10,jt) if b['sector']=='X' else choose(9,it)*choose(8,jt-1)
                        expected=weight*(1+int(b['aux']==u['aux']))
                    need(g==expected,'every independently declared standard Gram entry')
            row.append(g)
        grams.append(row)
    return basis,orbits,census,digest(grams)


def ldl(matrix, metric, floor, damage=None):
    n=len(matrix)
    a=[[matrix[i][j]-floor*metric[i][j] for j in range(n)] for i in range(n)]
    if damage=='PSD-diagonal':a[0][0]=-1
    need(all(a[i][j]==a[j][i] for i in range(n) for j in range(n)),'symmetric actual weighted quadratic form')
    lower=[[F(int(i==j)) for j in range(n)] for i in range(n)]
    diagonal=[]
    for j in range(n):
        pivot=a[j][j]-sum(lower[j][k]**2*diagonal[k] for k in range(j))
        need(pivot>0,'fresh strictly positive exact LDL pivot')
        diagonal.append(pivot)
        for i in range(j+1,n):
            lower[i][j]=(a[i][j]-sum(lower[i][k]*lower[j][k]*diagonal[k] for k in range(j)))/pivot
    need(all(sum(lower[i][k]*diagonal[k]*lower[j][k] for k in range(n))==a[i][j]
             for i in range(n) for j in range(n)), 'every entire fresh LDL factor identity')
    record=dict(matrix=[[rat(x) for x in row] for row in a],lower=[[rat(x) for x in row] for row in lower],diagonal=list(map(rat,diagonal)))
    return dict(order=n,entries=n*n,pivots=n,minimum_pivot=rat(min(diagonal)),full_factor_sha256=digest(record))


def endpoint(data,basis,orbits,tau,damage=None):
    V,Q,proper=data['V'],data['Q'],data['proper'];types=data['types'];den=data['den']*tau.denominator
    actual=[[data['hM0'][i][j]*tau.denominator+data['hM1'][i][j]*tau.numerator for j in range(N)] for i in range(N)]
    floors=[]
    z=[N*int(bool(a&1))-S for a in V]
    for i,a in enumerate(V):
        need(sum(actual[i])==H*den,'every original stochastic row')
        need(sum(actual[i][j]*z[j] for j in range(N))==-S*den*z[i], 'every original centered-star eigen-equation')
        for j,b in enumerate(V):
            need(actual[i][j]==actual[j][i],'all original symmetry entries')
            if a&b:
                need(actual[i][j]==0,'all original support positions')
            else:
                need(actual[i][j]>=tau*den,'every allowed original floor including actual loop')
                floors.append((i,j,actual[i][j]-tau*den))
    need(len(floors)==72817 and min(value for i,j,value in floors)==0, 'complete ordered floor count and actual minimum')
    need(actual[0][0]==tau*den,'actual empty loop attains floor')
    proper_index={a:i for i,a in enumerate(proper)}
    T=[[F(data['c0'][proper_index[a]][proper_index[b]]*tau.denominator+data['c1'][proper_index[a]][proper_index[b]]*tau.numerator,den) for b in Q] for a in Q]
    Tnum=[[int(x*den) for x in row] for row in T]
    qindex={a:i for i,a in enumerate(Q)}
    star=[int(bool(a&1)) for a in Q]
    nonstar=[1-r for r in star]
    tr=[sum(row[j] for j in range(301) if star[j]) for row in Tnum]
    tb=[sum(row[j] for j in range(301) if nonstar[j]) for row in Tnum]
    rr=sum(tr[i] for i in range(301) if star[i])
    bb=sum(tb[i] for i in range(301) if nonstar[i])
    rb=sum(tb[i] for i in range(301) if star[i])
    inv_den=lcm(S,H)
    inv=[[inv_den*int(i==j)-inv_den//S*star[i]*star[j]-inv_den//H*nonstar[i]*nonstar[j] for j in range(301)] for i in range(301)]
    sr=[sum(inv[i][j] for i in range(301) if star[i]) for j in range(301)]
    sb=[sum(inv[i][j] for i in range(301) if nonstar[i]) for j in range(301)]
    rs=[sum(inv[i][j] for j in range(301) if star[j]) for i in range(301)]
    bs=[sum(inv[i][j] for j in range(301) if nonstar[j]) for i in range(301)]
    for i in range(301):
        for j in range(301):
            need(inv[i][j]+star[i]*sr[j]+nonstar[i]*sb[j]==inv_den*int(i==j), 'every original Gram inverse left product')
            need(inv[i][j]+rs[i]*star[j]+bs[i]*nonstar[j]==inv_den*int(i==j), 'every original Gram inverse right product')
    for i,a in enumerate(V):
        ar=star[qindex[a]] if a in qindex else -(S-1) if a==1 else 0
        ab=nonstar[qindex[a]] if a in qindex else -(H-1) if a==0 else 0
        for j,b in enumerate(V):
            br=star[qindex[b]] if b in qindex else -(S-1) if b==1 else 0
            bc=nonstar[qindex[b]] if b in qindex else -(H-1) if b==0 else 0
            if a in qindex and b in qindex:
                phiT=Tnum[qindex[a]][qindex[b]];K=int(a==b)
            elif a in qindex:
                phiT=-tr[qindex[a]] if b==1 else -tb[qindex[a]]
                K=-star[qindex[a]] if b==1 else -nonstar[qindex[a]]
            elif b in qindex:
                phiT=-tr[qindex[b]] if a==1 else -tb[qindex[b]]
                K=-star[qindex[b]] if a==1 else -nonstar[qindex[b]]
            else:
                phiT=rr if a==b==1 else bb if a==b==0 else rb
                K=S-1 if a==b==1 else H-1 if a==b==0 else 0
            lower=actual[i][j]+S*den*int(i==j)
            need(lower==den+phiT, 'every entire original lower lift position')
            projnum=K*N*S*H-ar*br*N*H-ab*bc*N*S
            need(projnum==N*S*H*int(i==j)-S*H-z[i]*z[j], 'every full centered-star projector position')
            need((N*den*int(i==j)-lower)*S*H==projnum*den-phiT*S*H+z[i]*z[j]*den, 'every entire original upper lift position')
    orbit_weights=list(map(len,orbits));coeff={}
    for t,oo in enumerate(orbits):
        for u,pp in enumerate(orbits):
            values={T[i][j] for i in oo for j in pp if not Q[i]&Q[j]}
            if values:
                need(len(values)==1,'actual witness defining type invariance')
                coeff[t,u]=next(iter(values))
    blocks={}
    for sector,slot in (('constant',None),('X',1),('Y',2)):
        selected=[t for t in range(22) if slot is None or types[t][slot]]
        actions=[]
        metric=[]
        for t in selected:
            mt,it,jt=types[t]
            w=orbit_weights[t] if slot is None else 2*choose(7,it-1)*choose(10,jt) if slot==1 else 2*choose(9,it)*choose(8,jt-1)
            metric.append(w)
            row=[]
            for u in selected:
                mu,iu,ju=types[u]
                a=coeff.get((t,u),F(0))
                if slot is None:
                    value=S*int(t==u)-orbit_weights[u]+(choose(9-it,iu)*choose(10-jt,ju)*(1+a) if not mt&mu else 0)
                elif slot==1:
                    value=S*int(t==u)-(choose(9-it-1,iu-1)*choose(10-jt,ju)*(1+a) if not mt&mu else 0)
                else:
                    value=S*int(t==u)-(choose(9-it,iu)*choose(10-jt-1,ju-1)*(1+a) if not mt&mu else 0)
                if damage=='action-sign' and sector=='X' and t!=u:value=-value
                row.append(value)
            actions.append(row)
        blocks[sector]=dict(selected=selected,action=actions,metric=metric)
    actions_checked=0
    basis_digest=hashlib.sha256()
    for v in basis:
        t=v['t'];sector=v['sector'];sv=sum(value for i,value in v['v'].items() if Q[i]&1);bv=sum(value for i,value in v['v'].items() if not Q[i]&1)
        vector_action=[sum(row[j]*value for j,value in v['v'].items()) for row in Tnum]
        for i,a in enumerate(Q):
            u=types.index(vtype(a))
            if sector=='constant':
                expected=blocks['constant']['action'][u][t]
            elif sector in ('X','Y'):
                pool=X if sector=='X' else Y
                f=int(bool(a&(1<<v['aux'])))-int(bool(a&(1<<pool[-1])))
                selected=blocks[sector]['selected']
                expected=blocks[sector]['action'][selected.index(u)][selected.index(t)]*f if u in selected else F(0)
            else:
                expected=(S+1+coeff[t,t])*v['v'].get(i,0)
            need(vector_action[i]==expected*den,'every actual original physical row action')
            gi=F(v['v'].get(i,0))-F(sv,S)*int(bool(a&1))-F(bv,H)*int(not a&1)
            upper_num=N*gi*den-vector_action[i]
            need(upper_num==den*(N*gi-expected),'every full inverse-Gram upper action')
            basis_digest.update(canonical([sector,t,i,vector_action[i],rat(upper_num)]));actions_checked+=2
    factors=[]
    for sector,block in blocks.items():
        selected,act,metric=block['selected'],block['action'],block['metric'];n=len(selected)
        gram=[[F(metric[i])*int(i==j) for j in range(n)] for i in range(n)]
        lower=[[F(metric[i])*act[i][j] for j in range(n)] for i in range(n)]
        if sector=='constant':
            inverse=[[F(int(i==j))-F(orbit_weights[u],S)*int(bool(types[t][0]&1))*int(bool(types[u][0]&1))-
                      F(orbit_weights[u],H)*int(not types[t][0]&1)*int(not types[u][0]&1) for j,u in enumerate(selected)] for i,t in enumerate(selected)]
        else:inverse=[[F(int(i==j)) for j in range(n)] for i in range(n)]
        if damage=='upper-metric' and sector=='constant':inverse=[[F(int(i==j)) for j in range(n)] for i in range(n)]
        upper=[[N*metric[i]*inverse[i][j]-lower[i][j] for j in range(n)] for i in range(n)]
        representatives=[next(v for v in basis if v['sector']==sector and v['t']==t) for t in selected]
        for i,v in enumerate(representatives):
            for j,u in enumerate(representatives):
                need(sum(T[a][b]*va*vb for a,va in v['v'].items() for b,vb in u['v'].items())==lower[i][j], 'every literal lower weighted quadratic position')
                gi=sum(va*vb for a,va in v['v'].items() for b,vb in u['v'].items() if a==b)-F(sum(va for a,va in v['v'].items() if Q[a]&1)*sum(vb for b,vb in u['v'].items() if Q[b]&1),S)-F(sum(va for a,va in v['v'].items() if not Q[a]&1)*sum(vb for b,vb in u['v'].items() if not Q[b]&1),H)
                need(N*gi-lower[i][j]==upper[i][j],'every literal full upper weighted quadratic position')
        for name,form in (('lower',lower),('upper',upper)):
            factor=ldl(form,gram,RESIDUAL_FLOOR,damage if sector=='constant' and name=='lower' else None)
            factors.append(dict(sector=sector,endpoint=name,**factor))
    for sector,typ in (('XX',(0,2,0)),('YY',(0,0,2)),('XY',(0,1,1))):
        t=types.index(typ);value=S+1+coeff[t,t]
        for name,scalar in (('lower',value),('upper',N-value)):
            need(scalar>RESIDUAL_FLOOR,'fresh harmonic scalar floor')
            factors.append(dict(sector=sector,endpoint=name,order=1,entries=1,pivots=1,minimum_pivot=rat(scalar-RESIDUAL_FLOOR),full_factor_sha256=digest(rat(scalar-RESIDUAL_FLOOR))))
    positive=F(0);negative=F(0);classes={'KK':0,'KG':0,'GG':0};changes={'KK':F(0),'KG':F(0),'GG':F(0)}
    for i,a in enumerate(proper):
        if a&1:continue
        for j in range(i+1,len(proper)):
            b=proper[j]
            if b&1 or a&b:continue
            value=F(data['c0'][i][j]*tau.denominator+data['c1'][i][j]*tau.numerator,den)-data['baseline'][i][j]
            label='KK' if a in data['bad'] and b in data['bad'] else 'KG' if (a in data['bad'])!=(b in data['bad']) else 'GG'
            classes[label]+=1;changes[label]+=value
            need(value<=0 if label=='KK' else value==0 if label=='KG' else value>=0,'each individual NN equality sign')
            positive+=max(value,0);negative+=max(-value,0)
    need(classes==dict(KK=1800,KG=10820,GG=11245) and positive==P0+38*tau,'all23865 individual positive repair costs')
    need(negative==F(16777855,65536)+F(75,2)*tau,'complete actual KK negative mass')
    need(all(actual[0][V.index(a)]==tau*den for a in data['bad']),'all75 bad empty floors attained')
    if damage=='objective':positive+=F(1,65536)
    need(positive==P0+38*tau,'independent exact sharp objective')
    return dict(tau=rat(tau),entry_denominator=den,original_hM_sha256=digest(actual),floor_positions=len(floors),floor_equalities=sum(value==0 for i,j,value in floors),
                original_lower_upper_lift_positions=2*N*N,original_projector_positions=N*N,inverse_product_positions=2*301**2,
                full_physical_actions=actions_checked,full_physical_action_sha256=basis_digest.hexdigest(),weighted_factors=factors,
                factor_identity_entries=sum(row['entries'] for row in factors),positive_pivots=sum(row['pivots'] for row in factors),positive_cost=rat(positive),negative_cost=rat(negative),NN_classes=classes)


def audit(damage=None):
    data=build(damage)
    basis,orbits,census,gram_digest=physical_basis(data,damage)
    upper_bounds=[];permanent=[]
    for i,a in enumerate(data['V']):
        for j,b in enumerate(data['V']):
            if a&b:continue
            intercept=F(data['hM0'][i][j],data['den']);gradient=F(data['hM1'][i][j],data['den'])-1
            if gradient<0:upper_bounds.append((intercept/-gradient,i,j))
            if intercept==0 and gradient==0:permanent.append((i,j))
    need(min(value for value,i,j in upper_bounds)==TAU_MAX,'exact recipe endpoint over all original affine surpluses')
    attaining=[(i,j) for value,i,j in upper_bounds if value==TAU_MAX]
    wanted={(0,data['V'].index(1<<x)) for x in X}|{(data['V'].index(1<<x),0) for x in X}
    need(set(attaining)==wanted and len(attaining)==18,'all18 exact endpoint obstructions')
    need(len(permanent)==211,'all211 recipe permanent floors, not imposed on all competitors')
    upper=TAU_MAX+F(1,3080192) if damage=='endpoint' else TAU_MAX
    endpoints=[endpoint(data,basis,orbits,tau,damage) for tau in (F(0),upper)]
    return dict(actual_agent='six-reviewer-5',role='independent mathematical reviewer',N=N,s=S,h=H,
                proved_residual_floor=rat(RESIDUAL_FLOOR),proved_original_two_gap=rat(RESIDUAL_FLOOR/H),
                physical_basis=census,full_Gram_entries=301**2,full_Gram_sha256=gram_digest,
                recipe_endpoint=rat(TAU_MAX),endpoint_obstruction_positions=18,permanent_recipe_floors=len(permanent),trade_census=data['counts'],endpoints=endpoints,
                trust='Literal finite certificate and ordinary real interpolation/kernel/congruence/mass proofs, UNFORMALIZED. No author executable/factor/EXPECTED or peer checker; attributed143integer fixture and reviewer-owned helper reuse explicit.')


if __name__=='__main__':
    allowed={None,'coefficient','duplicate-key','omit-aY','release-sign','empty-loop','basis','PSD-diagonal','action-sign','upper-metric','objective','endpoint'}
    damage=sys.argv[1] if len(sys.argv)==2 else None
    need(len(sys.argv)<=2 and damage in allowed,'declared exact checker mode')
    print(json.dumps(audit(damage),sort_keys=True,indent=2))
