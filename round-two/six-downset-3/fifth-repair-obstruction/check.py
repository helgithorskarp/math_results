"""Exact checker independent of the Newton search and rational recovery.

Original-pair census reconstructs all seven forms for all six finite points.
Independent binomial counts bind ten controls for the uniform scalar proof.
No numpy, numerical solver, original author producer or Schur decoder imported.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
from math import comb
import argparse
import hashlib
import importlib.util
import json
import sys

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))
import sourcecheck
SOURCE = sourcecheck.check_bundle(BASE)
LITERAL_PIN = '46218af58a0654279231ade1bc40106d9eb390b6c0b2ceee5f3c4c5b7bedbf39'


def require(value, message):
    if not value: raise ValueError(message)


def literal_input():
    path = BASE/'credited-original/literal.py'
    require(hashlib.sha256(path.read_bytes()).hexdigest() == LITERAL_PIN,
            'whole defining literal source pin before import')
    spec = importlib.util.spec_from_file_location('original_literal', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def keys():
    return sorted((c, z, w) for c in range(8) for z in range(3) for w in range(3)
                  if (1 <= c.bit_count()+z+w <= 2 or
                      c.bit_count()+z+w == 3 and c.bit_count() >= 2) and (c,z,w) != (6,1,0))


def params(q, k): return (q*q+13*q+16)//2-k, 3*q+4


def choose(n, r): return comb(n, r) if 0 <= r <= n else 0


def make_forms(q, k, K, mass, count, literal):
    N, s = params(q, k)
    table = literal.table(q)
    names = ('C0','Delta','Rb','Rc','B','T','U0')
    out = {n: [[F(0)]*23 for _ in K] for n in names}
    repairs = {'Rb':{(1,2):1,(2,5):-1}, 'Rc':{(1,4):1,(3,4):-1}, 'B':{(2,4):1}}
    for i, (c,z,w) in enumerate(K):
        for j, (cc,zz,ww) in enumerate(K):
            disjoint = count[i][j]
            a, d = table[tuple(sorted(((c.bit_count(),z+w),(cc.bit_count(),zz+ww))))] if disjoint else (0,0)
            out['C0'][i][j] = s*mass[i]*int(i==j)-mass[i]*mass[j]+disjoint*a
            out['Delta'][i][j] = disjoint*d
            out['U0'][i][j] = N*mass[i]*int(i==j)-mass[i]*mass[j]-out['C0'][i][j]
            for n, edge in repairs.items():
                if z+w+zz+ww == 0: out[n][i][j] = F(edge.get(tuple(sorted((c,cc))),0))
            if ((c == 0 and z+w == 1 and (cc,zz,ww) == (6,0,0)) or
                (cc == 0 and zz+ww == 1 and (c,z,w) == (6,0,0))):
                out['T'][i][j] = mass[i]*mass[j]
    require(all(M[i][j]==M[j][i] for M in out.values() for i in range(23) for j in range(23)),
            'all seven full original Gram forms symmetric')
    return out


def counted(q, k, literal):
    K = keys()
    mass = [choose(k,z)*choose(q-k,w) for c,z,w in K]
    count = [[0 if c&cc else mass[i]*choose(k-z,zz)*choose(q-k-w,ww)
              for cc,zz,ww in K] for i,(c,z,w) in enumerate(K)]
    require(len(K)==23 and sum(mass)==params(q,k)[0]-1, 'whole physical count')
    return K, mass, make_forms(q,k,K,mass,count,literal)


def original(q, k, literal):
    # Independent literal original carrier, includes the actual empty member.
    X = [0]+sorted(sum(1<<x for x in xs) for r in (1,2,3)
                   for xs in combinations(range(q+3),r)
                   if literal.member(q,k,sum(1<<x for x in xs)))
    N,s = params(q,k)
    require(len(X)==N and len(set(X))==N and X[0]==0, 'complete actual-empty original census')
    stars = [sum(bool(A & (1<<i)) for A in X) for i in range(q+3)]
    require(stars[0]==s and max(stars)==s, 'original maximum-star size')
    K=keys(); ix={key:i for i,key in enumerate(K)}
    def orbit(A): return A&7,((A>>3)&((1<<k)-1)).bit_count(),(A>>(3+k)).bit_count()
    mass=[0]*23
    for A in X[1:]: mass[ix[orbit(A)]]+=1
    pairs=[[0]*23 for _ in K]
    actual_T=[[0]*23 for _ in K]
    for A in X[1:]:
        i=ix[orbit(A)]
        for B in X[1:]:
            j=ix[orbit(B)]
            if not A&B: pairs[i][j]+=1
            v=int((A==6 and B&7==0 and B.bit_count()==1) or
                  (B==6 and A&7==0 and A.bit_count()==1))
            if v:
                require(not A&B and A!=B, 'original nonzero T pair proper and disjoint')
                actual_T[i][j]+=v
    G=make_forms(q,k,K,mass,pairs,literal)
    require(G['T']==actual_T, 'ALL literal original T entries aggregated independently')
    counted_K, counted_mass, counted_G=counted(q,k,literal)
    require(K==counted_K and mass==counted_mass and G==counted_G,
            'EVERY one of seven entire forms from actual pairs equals independent binomial count')
    astar=[int(bool(c&1)) for c,z,w in K]
    require(all(sum(G['T'][i][j]*astar[j] for j in range(23))==0 for i in range(23)),
            'entire T maximum-star action zero')
    return K,mass,G,{'q':q,'k':k,'actual_empty_present':True,'N':N,'s':s,
                    'ordered_original_nonempty_pairs':(N-1)**2,'whole_seven_form_positions':7*23*23}


def energy(M,x):
    return sum(M[i][i]*x[i]*x[i] for i in range(23))+2*sum(
        M[i][j]*x[i]*x[j] for i in range(23) for j in range(i+1,23))


def cross(M,x,y): return sum(x[i]*M[i][j]*y[j] for i in range(23) for j in range(23))


def constant_vectors(K):
    y=[];v=[];zeta=[]
    for c,z,w in K:
        r=z+w
        low=(F(0) if c in (0,6) or r==0 and c in (1,3,5) else
             F(1) if r==0 and c in (2,4) else F(1,2) if c in (1,7) else
             F(3,4) if c in (2,4) else F(-1,4))
        y.append(low)
        v.append(F(1) if r==0 and c in (2,4) else F(2))
        zeta.append(F(1) if c==0 else F(-1) if c==7 else F(0))
    return y,v,zeta


def uniform_component(q,k,literal):
    K,mass,G=counted(q,k,literal)
    y,v,zeta=constant_vectors(K)
    e=[F(int(key==(6,0,0))) for key in K]
    h=F(1,3*q+5)
    alpha=F(q*(q+1),2)+3*(q+1)*h
    d=2*q*(q+1)+4*(3*q+1-2*k)*h
    A=F(3*q*q-12*k*q+4*k*k-14*k)+F(69*q,2)+F(121,4)
    lower=[energy(G['C0'],y)]+[energy(G[n],y) for n in ('Delta','Rb','Rc','B','T')]
    upper=[energy(G['U0'],v)]+[-energy(G[n],v) for n in ('Delta','Rb','Rc','B','T')]
    require([a+b for a,b in zip(lower,upper)]==[A,-d,0,0,0,-8*q],
            'EVERY original combined affine scalar coefficient')
    require([energy(G[n],zeta) for n in ('C0','Delta','Rb','Rc','B','T')]==[0,alpha,0,0,0,0],
            'whole original orientation affine coefficients')
    require([cross(G[n],zeta,e) for n in ('C0','Delta','Rb','Rc','B','T')]==[0,h,0,0,0,q],
            'every original zeta/bc cross coefficient')
    s=params(q,k)[1]
    require([energy(G[n],e) for n in ('C0','Delta','Rb','Rc','B','T')]==[s-1,0,0,0,0,0],
            'every original bc affine diagonal coefficient')
    # The following direct scalar count is independent of the orbit forms.
    tab=literal.table(q); leaf=tab[((0,1),(2,0))]; pair=tab[((0,2),(2,0))]
    require(q*(leaf[0]-1)+comb(q,2)*(pair[0]-1)+1==0,
            'original C0 cross: outside singles, pairs, abc')
    require(q*leaf[1]+comb(q,2)*pair[1]==h,
            'original Delta cross: outside singles and pairs')
    return {'q':q,'k':k,'combined_affine_plane':list(map(str,[A,-d,0,0,0,-8*q])),
            'orientation':str(alpha),'zeta_bc_cross':str(h),'bc_diagonal':s-1}


def polynomial_obstruction():
    # Separate from the producer: Horner products and translation.
    def add(p,q):
        r=[F(0)]*max(len(p),len(q))
        for i in range(len(r)): r[i]=(p[i] if i<len(p) else 0)+(q[i] if i<len(q) else 0)
        while r and not r[-1]: r.pop()
        return r
    def times(p,q):
        r=[]
        for value in reversed(p): r=add([F(0)]+r,[value*x for x in q])
        return r
    def scale(p,c): return [c*x for x in p]
    K=[F(0),F(1)];q=scale(K,2);H=add(scale(q,3),[F(5)])
    qp1=add(q,[F(1)])
    an=add(scale(times(times(q,qp1),H),F(1,2)),scale(qp1,3))
    dn=add(scale(times(times(q,qp1),H),2),scale(add(add(scale(q,3),[F(1)]),scale(K,-2)),4))
    bn=scale(add(dn,[F(-8)]),F(1,4))
    ap=[F(121),F(220),F(-32)]
    signed=add(scale(times(an,add(scale(q,3),[F(3)])),16),times(ap,bn))
    require(signed==list(map(F,(23,1685,5772,6796,3280,-384))), 'ENTIRE eta numerator multiplication')
    def translated(p,a):
        r=[]
        for value in reversed(p): r=add(times(r,[F(a),F(1)]),[value])
        return r
    shift=translated(signed,11)
    require(shift==list(map(F,(-4058658,-8052383,-2499720,-313524,-17840,-384)))
            and all(x<0 for x in shift), 'all coefficients of strict k11 translation negative')
    betashift=translated(bn,8)
    require(all(x>0 for x in betashift), 'entire beta numerator positive at k8+x')
    ashift=translated(ap,8)
    require(all(x<0 for x in ashift), 'entire A numerator negative at k8+x')
    return {'whole_eta_numerator':list(map(str,signed)), 'whole_shift11':list(map(str,shift)),
            'whole_beta_numerator_shift8':list(map(str,betashift)),
            'whole_A_numerator_shift8':list(map(str,ashift)),
            'positive_clearing':'16(6k+5)',
            'ordinary_PSD_determinant_AMGM_bridge_unformalized':True}


def check_certificate(data,literal):
    require(data['coordinate_order']==[list(x) for x in keys()], 'ENTIRE original coordinate order')
    require([(r['q'],r['k']) for r in data['points']]==[(2*k,k) for k in range(5,11)],
            'exact canonical finite domain, no missing or duplicate point')
    rows=[];pairs=0
    for row in data['points']:
        require(row['positive_weights']==['1','1'], 'both original endpoint weights positive')
        low,cap=[list(map(F,row[name])) for name in ('lower','upper')]
        require(len(low)==len(cap)==23, 'complete original vectors')
        K,mass,G,receipt=original(row['q'],row['k'],literal)
        zeta=constant_vectors(K)[2]
        q=row['q'];alpha=F(q*(q+1),2)+F(3*(q+1),3*q+5)
        require(alpha>0 and [energy(G[n],zeta) for n in ('C0','Delta','Rb','Rc','B','T')]
                ==[0,alpha,0,0,0,0], 'ENTIRE original finite orientation forces kappa nonnegative')
        lo=[energy(G['C0'],low)]+[energy(G[n],low) for n in ('Delta','Rb','Rc','B','T')]
        up=[energy(G['U0'],cap)]+[-energy(G[n],cap) for n in ('Delta','Rb','Rc','B','T')]
        total=[a+b for a,b in zip(lo,up)]
        require([lo,up,total]==[list(map(F,row[n])) for n in ('lower_plane','upper_plane','combined_plane')],
                'EVERY original affine endpoint coefficient reproduced from original pairs')
        require(total[0]<0 and total[1]<0 and total[2:]==[F(0)]*4,
                'whole original dual negative and each real repair cancels independently')
        receipt['whole_combined_plane']=list(map(str,total));rows.append(receipt)
        pairs+=receipt['ordered_original_nonempty_pairs']
    return rows,pairs


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path)
    ap.add_argument('--certificate',type=Path,default=BASE/'CERTIFICATE.json')
    args=ap.parse_args()
    literal=literal_input()
    data=json.loads(args.certificate.read_text())
    rows,pairs=check_certificate(data,literal)
    uniform=[uniform_component(2*k,k,literal) for k in range(8,18)]
    poly=polynomial_obstruction()
    expected=json.loads((BASE/'EXPECTED.json').read_text())
    require(expected['finite_points']==[[r['q'],r['k']] for r in rows] and
            expected['whole_eta_numerator']==poly['whole_eta_numerator'] and
            expected['whole_shift11']==poly['whole_shift11'], 'complete compact expected mathematics')
    result={'actual_agent':'six-downset-3','role':'researcher','completed':True,
            'source':SOURCE,'finite_original_certificates':rows,
            'ordered_original_nonempty_pairs':pairs,'whole_seven_form_positions':6*7*23*23,
            'complete_uniform_scalar_controls':uniform,'uniform_exact_polynomial':poly,
            'scope':expected['total_scope'],'arbitrary_H_or_uncapped_H_not_decided':True,
            'ordinary_original_decoding_unformalized':True,'independent_person_review':False,
            'numerical_search_and_recovery_programs_not_imported':True}
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'completed':True,'finite_points':len(rows),'original_pairs':pairs,
                      'whole_seven_form_positions':6*7*23*23,'uniform_scalar_controls':len(uniform),
                      'whole_record_SHA256':hashlib.sha256(args.out.read_bytes()).hexdigest()}))


if __name__=='__main__':main()
