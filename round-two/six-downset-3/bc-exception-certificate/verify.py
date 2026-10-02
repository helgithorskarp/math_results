"""Original q18,k5 BC-edge certificate and balanced-repair obstruction.

Only the Python standard library and two whole byte-pinned parent files
are used. No SDP solver, SymPy, heuristic status, or floating matrix is
an input. All arithmetic is exact. Ordinary whole-space bridges are in
PROOF.md; two algorithms by one author do not constitute peer review.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
from math import comb
import argparse
import json
import sys
import time

import source_pins
source_pins.check()
SOURCE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SOURCE/'small-deletion-boundary'))
from literal import table, typ, require
sys.path.insert(0, str(SOURCE/'triangle-majority'))
from exact import digest, lift, schur_psd, polynomial_psd

Q, K, N, S = 18, 5, 282, 58
KAPPA, TB, TC, SIGMA = F(1,4096), F(4), F(4), F(-1)
LOWER_FLOOR, CAP_FLOOR = F(1,65536), F(1,4096)
RB = {(1,2): 1, (2,5): -1}
RC = {(1,4): 1, (3,4): -1}
BC = {(2,4): 1}
# Ordered exactly as the independently counted 23 keys below.
DUAL = [F(x) for x in ('125/128','125/128','125/128','125/128','63/64',
        '269/288','119/128','121/128','1','1','1','269/288','1','1',
        '1','1','1','269/288','1','1','63/64','63/64','127/128')]


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {key: encode(v) for key,v in value.items()}
    if isinstance(value, (list,tuple)):
        return [encode(v) for v in value]
    return value


def action(matrix, vector):
    return [sum(x*y for x,y in zip(row,vector)) for row in matrix]


def quadratic(matrix, vector):
    return sum(x*y for x,y in zip(vector,action(matrix,vector)))


def orbit(A):
    return A&7, ((A>>3)&((1<<K)-1)).bit_count(), (A>>(3+K)).bit_count()


def member(A):
    return (A.bit_count() <= 2 or A.bit_count()==3 and (A&7).bit_count()>=2) and not (
            A&7==6 and (A>>3).bit_count()==1 and (A>>3).bit_length()<=K)


def domain():
    out = [0]+sorted(sum(1<<i for i in points)
                    for size in (1,2,3) for points in combinations(range(Q+3),size)
                    if member(sum(1<<i for i in points)))
    require(len(out)==N and out[0]==0 and len(set(out))==N,
            'entire original family census including actual empty')
    require(all(member(A & ~(1<<i)) for A in out for i in range(Q+3) if A&(1<<i)),
            'every immediate downset deletion survives')
    return out


def base_entry(A,B,tab):
    if A==B:
        return F(S-1), F(0)
    if A&B:
        return F(-1), F(0)
    x,y = tab[tuple(sorted((typ(A),typ(B))))]
    return x-1,y


def edge_entry(edges,A,B):
    return F(edges.get(tuple(sorted((A,B))),0))


def choose(n,r):
    return comb(n,r) if 0<=r<=n else 0


def counted(keys,sizes,tab):
    forms = {name: [] for name in ('C0','Delta','Rb','Rc','B','U0')}
    for i,(c,z,w) in enumerate(keys):
        rows = {name: [] for name in forms}
        for j,(cc,zz,ww) in enumerate(keys):
            cnt = 0 if c&cc else choose(K-z,zz)*choose(Q-K-w,ww)
            back = 0 if c&cc else choose(K-zz,z)*choose(Q-K-ww,w)
            require(sizes[i]*cnt==sizes[j]*back,'entire disjoint reciprocity')
            a,b = tab[tuple(sorted(((c.bit_count(),z+w),(cc.bit_count(),zz+ww))))] if cnt else (F(0),F(0))
            base = F(S*sizes[i]*int(i==j)-sizes[i]*sizes[j])+sizes[i]*cnt*a
            rows['C0'].append(base)
            rows['Delta'].append(sizes[i]*cnt*b)
            for name,edges in (('Rb',RB),('Rc',RC),('B',BC)):
                rows[name].append(edge_entry(edges,c,cc) if z+w+zz+ww==0 else F(0))
            rows['U0'].append(F(N*sizes[i]*int(i==j)-sizes[i]*sizes[j])-base)
        for name in forms:
            forms[name].append(rows[name])
    return forms


def psd_record(matrix, rank):
    got = schur_psd(matrix)
    other, characteristic, denominator = polynomial_psd(matrix)
    require(got==other==rank,'both full exact PSD algorithms and ranks')
    return {'rank':got,'characteristic_sha256':characteristic,
            'integer_scaling_denominator':denominator,'entire_matrix_sha256':digest(encode(matrix))}


def closed_empty(A,tab):
    h = F(1,3*Q+5)
    alpha = F(Q*(Q+1),2)+3*(Q+1)*h
    if A==0:
        return 1+K*(S-K)+KAPPA*(alpha-2*K*h)+2*SIGMA
    core = (A&7).bit_count()
    r = F(1) if core==0 else h if core<3 else -3*(Q+1)*h
    m = K if A&6 else ((A>>3)&((1<<K)-1)).bit_count()
    if m==K:
        deleted = F(-K)
    else:
        a,b = tab[tuple(sorted((typ(A),(2,1))))]
        deleted = -m+(K-m)*(a+KAPPA*b-1)
    rb = sum(edge_entry(RB,A,V) for V in (1,2,3,4,5,6,7))
    rc = sum(edge_entry(RC,A,V) for V in (1,2,3,4,5,6,7))
    bc = int(A in (2,4))
    return 1-(KAPPA*r-deleted+TB*rb+TC*rc+SIGMA*bc)


def check_original(C,L,M,X,tab):
    n = len(C)
    require(n==N-1 and len(L)==len(M)==N,'actual empty vertex retained')
    require(all(L[i][j]==L[j][i] and M[i][j]==M[j][i]
                for i in range(N) for j in range(N)),'every original symmetry position')
    require(all(sum(row)==N for row in L) and all(sum(row)==1 for row in M),
            'every original row-balance equation')
    require(all(M[i][j]==0 for i,A in enumerate(X) for j,B in enumerate(X) if A&B),
            'every original intersecting position zero')
    require(all(L[0][i]==closed_empty(A,tab) for i,A in enumerate(X)),
            'every separate closed actual-empty entry')
    star = [F(bool(A&1)) for A in X[1:]]
    centered = [F(bool(A&1))-F(S,N) for A in X]
    require(not any(action(C,star)) and not any(action(L,centered)),
            'every original maximum-star and whole centered-star kernel row')
    require(sum(centered)==0,'centered star has zero mean')


def reject(call,message):
    try:
        call()
    except (ValueError,KeyError):
        return message
    raise ValueError('Semantic damage was accepted: '+message)


def run():
    X=domain();nonempty=X[1:];n=len(nonempty);tab=table(Q)
    groups={}
    for A in nonempty:
        groups.setdefault(orbit(A),[]).append(A)
    keys=sorted(groups);sizes=[len(groups[key]) for key in keys]
    independent_keys=sorted((c,z,w) for c in range(8) for z in range(3) for w in range(3)
                           if (1<=c.bit_count()+z+w<=2 or c.bit_count()+z+w==3 and c.bit_count()>=2)
                           and (c,z,w)!=(6,1,0))
    require(keys==independent_keys and len(keys)==23 and
            sizes==[choose(K,z)*choose(Q-K,w) for c,z,w in keys] and sum(sizes)==n,
            'entire two independently generated original orbit censuses')
    index={key:i for i,key in enumerate(keys)}
    gram={name:[[F(0)]*23 for _ in range(23)] for name in ('C0','Delta','Rb','Rc','B','U0')}
    C0=[];Delta=[];C=[];U=[]
    for i,A in enumerate(nonempty):
        base_row=[];der_row=[];lower_row=[];upper_row=[]
        oi=index[orbit(A)]
        for j,B in enumerate(nonempty):
            base,der=base_entry(A,B,tab)
            rb,rc,bc=(edge_entry(edges,A,B) for edges in (RB,RC,BC))
            lower=base+KAPPA*der+TB*rb+TC*rc+SIGMA*bc
            upper=F(N*int(i==j)-1)-lower
            base_row.append(base);der_row.append(der);lower_row.append(lower);upper_row.append(upper)
            oj=index[orbit(B)]
            for name,val in (('C0',base),('Delta',der),('Rb',rb),('Rc',rc),('B',bc),
                             ('U0',F(N*int(i==j)-1)-base)):
                gram[name][oi][oj]+=val
        C0.append(base_row);Delta.append(der_row);C.append(lower_row);U.append(upper_row)
    compressed=counted(keys,sizes,tab)
    require(compressed==gram,'ALL 6 times 529 weighted forms equal full original pair sums')
    G=[[gram['C0'][i][j]+KAPPA*gram['Delta'][i][j]+TB*gram['Rb'][i][j]+
        TC*gram['Rc'][i][j]+SIGMA*gram['B'][i][j] for j in range(23)] for i in range(23)]
    H=[[F(N*sizes[i]*int(i==j)-sizes[i]*sizes[j])-G[i][j] for j in range(23)] for i in range(23)]
    astar=[F(bool(c&1)) for c,z,w in keys];weighted=[sizes[i]*astar[i] for i in range(23)]
    W=[[F(sizes[i]*int(i==j)) for j in range(23)] for i in range(23)]
    P=[[W[i][j]-F(weighted[i]*weighted[j],S) for j in range(23)] for i in range(23)]
    require(sum(weighted)==S and not any(action(G,astar)),'exact full physical star frame')
    checks={name:psd_record(A,rank) for name,A,rank in (
        ('lower',G,22),('cap',H,23),
        ('lower_floor',[[G[i][j]-LOWER_FLOOR*P[i][j] for j in range(23)] for i in range(23)],22),
        ('cap_floor',[[H[i][j]-CAP_FLOOR*W[i][j] for j in range(23)] for i in range(23)],23),
        ('credited_C0',gram['C0'],19))}
    L=lift(C)
    M=[[(L[i][j]-S*int(i==j))/F(N-S) for j in range(N)] for i in range(N)]
    check_original(C,L,M,X,tab)
    stars=[sum(bool(A&(1<<i)) for A in X) for i in range(Q+3)]
    require(stars==[58,53,53]+[23]*5+[24]*13,'entire original star census')
    rows=[sum(row) for row in U]
    lifted_U=[[sum(rows)]+[-v for v in rows]]+[
              [-rows[i]]+list(U[i]) for i in range(n)]
    require(all(F(N*int(i==j))-L[i][j]==lifted_U[i][j]
                for i in range(N) for j in range(N)),'ALL original physical cap-lift positions')
    # Original baseline scalar, derived from original weighted moments.
    one=[F(1)]*23;y=[F(c==1 and z+w==1) for c,z,w in keys]
    v=[F(bool(c&6) and (c,z,w) not in ((3,0,0),(5,0,0))) for c,z,w in keys]
    moment=[[sum(x*yy for x,yy in zip(a,action(gram['U0'],b))) for b in (one,y,v)]
            for a in (one,y,v)]
    e,A,B0=moment[0];T,B,V=moment[1][1],moment[1][2],moment[2][2]
    determinant=T*V-B*B
    aa=(V*A-B*B0)/determinant;bb=(T*B0-B*A)/determinant
    scalar=e-aa*A-bb*B0
    require(scalar==F(-784601496,1274780111),'original negative exceptional scalar baseline')
    z=[F(1-int(bool(c&2))-int(bool(c&4))+int(c.bit_count()>=2)) for c,a,b in keys]
    require(not any(action(gram['C0'],z)),'whole fixed lower orientation kernel')
    require(all(not any(action(gram[name],z)) for name in ('Rb','Rc','B')),
            'each core repair annihilates the original orientation vector')
    alpha=quadratic(gram['Delta'],z)
    require(alpha==F(10146,59)>0,'original lower orientation forces kappa>=0')
    p=[F(key==(1,0,0))-F(int(key[0]==1 and key[1]+key[2]==1),Q) for key in keys]
    wp=sum(sizes[i]*DUAL[i]*p[i] for i in range(23))
    zp=sum(sizes[i]*z[i]*p[i] for i in range(23))
    require(wp==zp==0 and all(z[index[key]]==0 for key in ((2,0,0),(4,0,0),(6,0,0))),
            'whole balanced-repair cap isotropy and orientation annihilation')
    pairing={name:quadratic(gram[name],DUAL) for name in ('U0','Delta','Rb','Rc','B')}
    require(pairing=={'U0':F(-4744087,15040512),'Delta':F(145525378055,887390208),
                     'Rb':F(0),'Rc':F(0),'B':F(2)},'every new compact original dual pairing')
    original_dual=[DUAL[index[orbit(A)]] for A in nonempty]
    require(quadratic(C0,original_dual)==quadratic(gram['C0'],DUAL) and
            quadratic(Delta,original_dual)==pairing['Delta'] and
            quadratic(U,original_dual)==pairing['U0']-KAPPA*pairing['Delta']-2*SIGMA,
            'independent entire original-domain dual decoding')
    core=[1,2,3,4,5,6,7]
    disjoint=[(a,b) for a,b in combinations(core,2) if not a&b]
    require(disjoint==[(1,2),(1,4),(1,6),(2,4),(2,5),(3,4)],
            'complete plain-core disjoint edge census for the three-dimensional affine classification')
    damage=[]
    without_bc=[[H[i][j]-gram['B'][i][j] for j in range(23)] for i in range(23)]
    damage.append(reject(lambda:schur_psd(without_bc),'missing BC edge fails the original cap'))
    too_negative=[[G[i][j]-7*gram['B'][i][j] for j in range(23)] for i in range(23)]
    damage.append(reject(lambda:schur_psd(too_negative),'BC weight -8 fails lower PSD'))
    badL=[row[:] for row in L];badL[0][0]+=1
    damage.append(reject(lambda:check_original(C,badL,M,X,tab),'altered actual-empty diagonal rejected'))
    badL=[row[:] for row in L];badL[0][1]+=1
    damage.append(reject(lambda:check_original(C,badL,M,X,tab),'altered actual-empty off-diagonal rejected'))
    badstar=astar[:];badstar[index[(1,0,0)]]=0
    damage.append(reject(lambda:require(not any(action(G,badstar)),'bad star'),'wrong forced star rejected'))
    badp=DUAL[:];badp[index[(1,0,0)]]+=F(1,128)
    damage.append(reject(lambda:require(sum(sizes[i]*badp[i]*p[i] for i in range(23))==0,
                                    'bad dual p pairing'),'broken balanced-repair annihilation rejected'))
    wrong_weights=sizes[:];wrong_weights[0]+=1
    damage.append(reject(lambda:require(counted(keys,wrong_weights,tab)==gram,'bad physical metric'),
                         'changed original orbit weight rejected'))
    damage.append(reject(lambda:require(-alpha>=0,'negative kappa orientation'),
                         'negative kappa rejected by original lower direction'))
    damage.append(reject(lambda:schur_psd([[G[i][j]-LOWER_FLOOR*W[i][j] for j in range(23)]
                                           for i in range(23)]),
                         'lower floor on full identity violates the forced star kernel'))
    result={'agent':'six-downset-3','role':'researcher',
            'status':'exact certificate with ordinary unformalized whole-space bridges; independently unreviewed',
            'q':Q,'k':K,'N':N,'s':S,'parameters':{'kappa':KAPPA,'t_b':TB,'t_c':TC,'sigma':SIGMA},
            'keys':keys,'sizes':sizes,'original_nonempty_positions':n*n,
            'whole_ordered_positions':N*N,'original_downset_and_all_star_census':stars,
            'entire_forms_sha256':digest(encode(gram)),'fixed_checks':checks,
            'nonfixed_dimension':n-23,'credited_nonfixed_lower_floor':KAPPA/2,
            'credited_nonfixed_cap_floor':N-2*S,'nonempty_lower_floor':LOWER_FLOOR,
            'nonempty_cap_floor':CAP_FLOOR,'whole_projected_M_unit_gap':CAP_FLOOR/(N-S),
            'whole_lower_rank':N-1,'whole_cap_rank':N-1,'whole_M_sha256':digest(encode(M)),
            'actual_empty_M_diagonal':M[0][0],'all_separate_empty_entries_and_physical_cap_lift_match':True,
            'reproduced_original_exceptional_Q':scalar,'lower_orientation_energy':alpha,
            'balanced_repair_cap_dual':DUAL,'dual_pairings':pairing,'dual_p_pairing':wp,
            'plain_core_disjoint_edges':disjoint,'core_star_preserving_space_dimension':3,
            'semantic_damages_rejected':damage,
            'trust_boundary':'byte-pinned literal table and two exact PSD algorithms; complete ordinary symmetry/complement/lift/rank arguments in PROOF.md; no formalization or independent-review claim'}
    return encode(result)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--freeze',type=Path)
    parser.add_argument('--record',type=Path)
    args=parser.parse_args();start=time.perf_counter();result=run()
    full=digest(result)
    if args.freeze:
        require(not args.freeze.exists(),'refusing to overwrite a frozen record')
        args.freeze.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    else:
        expected=json.loads(Path(__file__).with_name('RESULTS.json').read_text())
        require(result==expected,'ENTIRE substantive frozen record differs')
    if args.record:
        args.record.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'record_sha256':full,'q':Q,'k':K,'whole_gap':result['whole_projected_M_unit_gap'],
                      'whole_ranks':[result['whole_lower_rank'],result['whole_cap_rank']],
                      'seconds':time.perf_counter()-start,'semantic_damages':len(result['semantic_damages_rejected'])}))


if __name__=='__main__':
    main()
