#!/usr/bin/env python3
"""Independent pendant-completion audit: six-reviewer-1, mathematical reviewer.

Standard library, exact arithmetic, no target module imports. Literal member
indices, integer contrast vectors and fraction-free symmetric congruences.
The all-order norm and n=2 refinement proofs are in REVIEW.md.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from itertools import product, permutations
from math import ceil, lcm
from pathlib import Path
import argparse
import json


def need(ok, text):
    if not ok:
        raise ValueError(text)


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def mv(a, v):
    return [dot(row, v) for row in a]


def fingerprint(a):
    return sha256(json.dumps([[str(x) for x in row] for row in a],
                             separators=(',', ':')).encode()).hexdigest()


def determinant(a):
    result=0;N=len(a)
    for p in permutations(range(N)):
        sign=(-1)**sum(p[i]>p[j] for i in range(N) for j in range(i+1,N))
        term=sign
        for i in range(N):term*=a[i][p[i]]
        result+=term
    return result


def intersecting_census(D,s,c):
    visited=0;largest=0;maxima=[]
    def visit(chosen,remaining):
        nonlocal visited,largest,maxima
        visited+=1
        need(visited<=2000000,'bounded equality census incomplete')
        if len(chosen)>largest:largest=len(chosen);maxima=[chosen]
        elif len(chosen)==largest:maxima.append(chosen)
        for i,a in enumerate(remaining):
            visit(chosen+[a],[z for z in remaining[i+1:] if a&z])
    visit([],D[1:])
    need(largest==s and maxima==[[a for a in D if a&(1<<c)]],'whole equality census')
    return {'intersecting_subfamilies_of_nonempty_members_including_empty_family':visited,
            'largest_size':largest,'maximum_families':1}


def geometry(D, c):
    need(type(c) is int and c >= 0 and type(D) is list and D == sorted(set(D))
         and D and D[0] == 0 and all(type(x) is int and x >= 0 for x in D), 'family domain')
    members = set(D)
    need(all((a ^ (1 << p)) in members for a in D for p in range(a.bit_length())
             if a & (1 << p)), 'not a downset')
    ss = [i for i, a in enumerate(D[1:]) if a & (1 << c)]
    bb = [i for i, a in enumerate(D[1:]) if not a & (1 << c)]
    need(ss, 'inactive center')
    return ss, bb


def core_check(D, C, c):
    ss, bb = geometry(D, c)
    n = len(ss); m = len(D)-1
    need(len(C) == m and all(len(row) == m for row in C), 'core dimension')
    need(all(type(x) in (int, F) for row in C for x in row), 'exact core entries')
    need(all(C[i][j] == C[j][i] for i in range(m) for j in range(m)), 'core symmetry')
    need(all(C[i][i] == n-1 for i in range(m)), 'core diagonal')
    need(all(i == j or not D[i+1]&D[j+1] or C[i][j] == -1
             for i in range(m) for j in range(m)), 'core intersecting entries')
    need(all(sum(row) == 0 and sum(row[j] for j in ss) == 0 for row in C),
         'separate centering')
    need(n >= 2 and len(bb) >= max(2, n-1), 'nonvacuous regularization domain')
    return ss, bb


def seed(D, c):
    ss, bb = geometry(D, c); s = len(ss); b = len(bb); m = len(D)-1
    need(s >= 3 and b >= s-1, 'preliminary seed domain')
    nonempty = D[1:]; center = nonempty.index(1 << c)
    A = [[F(s-1 if i == j else -int(a & z != 0))
          for j, z in enumerate(nonempty)] for i, a in enumerate(nonempty)]
    for j in bb:
        A[center][j] = A[j][center] = F(sum(bool(nonempty[i]&nonempty[j]) for i in ss))
    outside_singletons = [i for i in bb if nonempty[i].bit_count() == 1]
    need(len(outside_singletons) >= 2, 'outside tuning pair')
    q, r = outside_singletons[:2]
    tune = (F(s-b)-sum(map(sum, A)))/2
    A[q][r] += tune; A[r][q] += tune
    rows = list(map(sum, A))
    point = 1 << max(D).bit_length(); E = sorted(D+[point, point | (1 << c)])
    singleton = point; spoke = point | (1 << c)
    lookup = {a: i for i, a in enumerate(nonempty)}
    def entry(a, z):
        if a == z:
            return F(s)
        if a == spoke or z == spoke:
            old = z if a == spoke else a
            return F(-1) if old == singleton or old & (1 << c) else F(1, b)
        if a == singleton or z == singleton:
            old = z if a == singleton else a; i = lookup[old]
            return -rows[i]+int(old == (1 << c)) if old & (1 << c) else -rows[i]-1
        i, j = lookup[a], lookup[z]
        return A[i][j]-F(int(a == (1 << c) and j in bb or z == (1 << c) and i in bb), b)
    C = [[entry(a, z) for z in E[1:]] for a in E[1:]]
    core_check(E, C, c)
    R = max(sum(abs(x) for x in row) for row in C)
    need(R <= 2*m*m+2, 'universal row bound')
    return E, C, {'original_N':len(D), 'original_s':s, 'tune':str(tune), 'R':str(R)}


def extend(D, C, c):
    ss, bb = core_check(D, C, c); n, b = len(ss), len(bb)
    old = D[1:]; pos = {a:i for i, a in enumerate(old)}
    point = 1 << max(D).bit_length(); spoke = point | (1 << c)
    E = sorted(D+[point, spoke])
    alpha, beta = 1-F(1, n*b), 1-F(1, b)
    def k(a, z):
        if a == z:
            return F(n+1)
        if a == spoke or z == spoke:
            other = z if a == spoke else a
            return F(0) if other == point or other & (1 << c) else 1+F(1,b)
        if a == point or z == point:
            other = z if a == point else a
            return 1+F(1,n) if other & (1 << c) else 1-F(n,b)
        if a & (1 << c) and z & (1 << c):
            return F(0)
        return (alpha if bool(a & (1 << c)) != bool(z & (1 << c)) else beta)*(C[pos[a]][pos[z]]+1)
    result = [[k(a,z)-1 for z in E[1:]] for a in E[1:]]
    core_check(E, result, c)
    return E, result, point, spoke


def profile(D, C, c):
    ss, bb = core_check(D,C,c); n,b=len(ss),len(bb)
    R=max(sum(abs(x) for x in row) for row in C)
    a=max(sum(abs(C[i][j]) for j in bb) for i in ss)
    d=max(sum(abs(C[i][j]) for i in ss) for j in bb)
    # Independent minimal integer ceiling via direct bounded integer enumeration.
    root=next(k for k in range(ceil(R)+1) if k*k >= a*d)
    P=min(R,F(root))
    T=min(R+n,max(sum(abs(C[i][j]-n*(int(i==j)-F(1,b))) for j in bb) for i in bb))
    A=B=F(1); limit=ceil(2*R+n)
    for u in range(1,limit+1):
        A*=1-F(1,(n+u-1)*(b+u-1)); B=F(b-1,b+u-1)
        if u>=2 and u>=B*T and u*(u-B*T)>=A*A*P*P:
            return u, {'n':n,'b':b,'R':str(R),'P':str(P),'T':str(T),
                       'A':str(A),'B':str(B),'margin':str(u-B*T),
                       'determinant':str(u*(u-B*T)-A*A*P*P),'row_count':limit}
    raise ValueError('decay did not terminate at guaranteed count')


def psd_rank(a):
    """Integer fraction-free symmetric elimination; every division exact.

    Positive pivots are congruences. A zero remaining diagonal forces its whole
    row zero for PSD; otherwise reject. Scaling by one positive grid is harmless.
    """
    N=len(a); need(N and all(len(row)==N for row in a), 'PSD shape')
    need(all(a[i][j]==a[j][i] for i in range(N) for j in range(N)), 'PSD symmetry')
    grid=lcm(*(F(x).denominator for row in a for x in row))
    z=[[int(grid*x) for x in row] for row in a]; prev=1; rank=0
    for k in range(N):
        need(all(z[i][i]>=0 for i in range(k,N)), 'negative PSD residual diagonal')
        p=next((i for i in range(k,N) if z[i][i]>0),None)
        if p is None:
            need(all(z[i][j]==0 for i in range(k,N) for j in range(k,N)), 'zero diagonal nonzero PSD row')
            break
        z[k],z[p]=z[p],z[k]
        for row in z:row[k],row[p]=row[p],row[k]
        pivot=z[k][k]
        for i in range(k+1,N):
            for j in range(i,N):
                numerator=pivot*z[i][j]-z[i][k]*z[k][j]
                need(numerator%prev==0,'nonexact symmetric elimination')
                z[i][j]=z[j][i]=numerator//prev
        for i in range(k+1,N):z[i][k]=z[k][i]=0
        prev=pivot;rank+=1
    return rank


def basis_check(initial, C0, final, C, c, history):
    ss0,bb0=geometry(initial,c); n,b=len(ss0),len(bb0); u=len(history)
    members=final[1:]; pos={a:i for i,a in enumerate(members)}; size=len(members)
    initial_basis=[]
    for group in (ss0,bb0):
        for i in group[:-1]:
            v=[0]*size;v[pos[initial[i+1]]]=1;v[pos[initial[group[-1]+1]]]=-1;initial_basis.append(v)
    planes=[]
    for j,(before,point,spoke) in enumerate(history):
        ss,bb=geometry(before,c);v=[0]*size;w=[0]*size
        for i in ss:v[pos[before[i+1]]]=-1
        for i in bb:w[pos[before[i+1]]]=-1
        v[pos[spoke]]=n+j;w[pos[point]]=b+j;planes.append((v,w))
    sf,bf=geometry(final,c)
    constants=[[int(i in group) for i in range(size)] for group in (sf,bf)]
    blocks=[initial_basis]+[list(vw) for vw in planes]+[[v] for v in constants]
    need(sum(map(len,blocks))==size,'complete invariant dimensions')
    for i,block in enumerate(blocks):
        for later in blocks[i+1:]:need(all(dot(v,w)==0 for v in block for w in later),'cross-block orthogonality')
    need(all(mv(C,v)==[0]*size for v in constants),'constant kernel')
    A=F(1);B=F(b-1,b+u-1)
    for j in range(u):A*=1-F(1,(n+j)*(b+j))
    # Compare full images of every original contrast using the initial entries.
    ss_set=set(ss0)
    for v in initial_basis:
        old_v=[v[pos[a]] for a in initial[1:]]; expected=[F(0)]*size
        for i,a in enumerate(initial[1:]):
            total=F(0)
            for k in range(len(old_v)):
                if (i in ss_set)==(k in ss_set):
                    coefficient=F(n+u)*int(i==k) if i in ss_set else F(n+u)*int(i==k)+B*(C0[i][k]-n*int(i==k))
                else:coefficient=A*C0[i][k]
                total+=coefficient*old_v[k]
            expected[pos[a]]=total
        need(mv(C,v)==expected,'complete initial-mode image')
    for j,(v,w) in enumerate(planes):
        at=F(1);bt=F(1)
        for k in range(j+1,u):at*=1-F(1,(n+k)*(b+k));bt*=1-F(1,b+k)
        av=n+u; bw=F(n+u)+bt*(F(n+j,b+j)-1)
        need(mv(C,v)==[av*x-at*F(n+j+1,b+j)*y for x,y in zip(v,w)],'star contrast image')
        need(mv(C,w)==[-at*F(b+j+1,n+j)*x+bw*y for x,y in zip(v,w)],'outside contrast image')
    return {'dimension':size,'initial_modes':len(initial_basis),'planes':u,'full_images':len(initial_basis)+2*u+2}


def finish(label,D,C,c,u=None,expected_hash=None):
    n=len(core_check(D,C,c)[0]); initial=D[:];C0=[row[:] for row in C]
    chosen,p=profile(D,C,c)
    if u is None:u=chosen
    need(u>=chosen and u<=70,'bounded fixture count')
    history=[]
    for _ in range(u):
        before=D[:];D,C,point,spoke=extend(D,C,c);history.append((before,point,spoke))
    modes=basis_check(initial,C0,D,C,c,history);ss,bb=geometry(D,c);N=len(D);s=len(ss)
    PZ=[[F(int(i==j))-F(int(i in ss and j in ss),s)-F(int(i in bb and j in bb),len(bb))
         for j in range(N-1)] for i in range(N-1)]
    need(psd_rank(C)==N-3,'whole raw rank')
    psd_rank([[C[i][j]-n*PZ[i][j] for j in range(N-1)] for i in range(N-1)])
    rawcap=[[F(N*int(i==j)-1)-C[i][j] for j in range(N-1)] for i in range(N-1)]
    need(psd_rank([[rawcap[i][j]-int(i==j) for j in range(N-1)] for i in range(N-1)])<=N-1,'raw unit cap')
    rawhash=fingerprint(C); epsilon=min(F(1,2),F(n,2*(len(bb)+2)))
    point=history[-1][1];other=next(a for a in initial[1:] if not a&(1<<c) and a.bit_count()==1)
    ai,di=D[1:].index(point),D[1:].index(other);C[ai][di]+=epsilon;C[di][ai]+=epsilon
    need(psd_rank(C)==N-2,'repaired core rank')
    cap=[[F(N*int(i==j)-1)-C[i][j] for j in range(N-1)] for i in range(N-1)]
    need(psd_rank([[cap[i][j]-F(int(i==j),2) for j in range(N-1)] for i in range(N-1)])==N-1,'repaired half cap')
    rows=list(map(sum,C));L=[[F(1)]*N for _ in range(N)]
    L[0][0]+=sum(rows)
    for i in range(N-1):
        L[0][i+1]=L[i+1][0]=1-rows[i]
        for j in range(N-1):L[i+1][j+1]=1+C[i][j]
    M=[[(L[i][j]-s*int(i==j))/(N-s) for j in range(N)] for i in range(N)]
    need(all(sum(row)==1 for row in M),'unit normalized rows')
    need(all(not a&z or M[i][j]==0 for i,a in enumerate(D) for j,z in enumerate(D)), 'H intersecting entries')
    need(psd_rank(L)==N-1 and psd_rank([[N*int(i==j)-L[i][j] for j in range(N)] for i in range(N)])==N-1,'whole two slack ranks')
    need(min(M[0][1:])>=F(1,2*(N-s)),'positive empty margin')
    h=fingerprint(M)
    if expected_hash:need(h==expected_hash,'complete independent matrix fingerprint')
    return {'case':label,'seed_N':len(initial),'n':n,'b':len(initial)-1-n,'u':u,'profile':p,
            'N':N,'s':s,'epsilon':str(epsilon),'lower_rank':N-1,'upper_rank':N-1,
            'raw_entries':(N-1)**2,'whole_definition_entries':N*N,'modes':modes,
            'raw_sha256':rawhash,'matrix_sha256':h,'complete_equality_census':intersecting_census(D,s,c)}


def all_four_point_seeds():
    count=centers=entries=0; digest=sha256();maximum=F(0)
    # Every family on 2^[4] is one of these 65,536 bit masks.
    for flags in range(1<<16):
        if not flags&1:continue
        D=[a for a in range(16) if flags&(1<<a)]
        if len(D)<2:continue
        if any(not flags&(1<<(a^(1<<p))) for a in D for p in range(4) if a&(1<<p)):continue
        count+=1
        stars=[sum(bool(a&(1<<p)) for a in D) for p in range(4)]
        for c in range(4):
            if stars[c]!=max(stars):continue
            original=D[:];s=stars[c]
            for _ in range(max(0,3-s)):
                point=1<<max(original).bit_length();original=sorted(original+[point,point|(1<<c)])
            E,C,record=seed(original,c);centers+=1;entries+=len(C)**2;maximum=max(maximum,F(record['R']))
            digest.update(json.dumps([D,c,E,fingerprint(C)],separators=(',',':')).encode()+b'\n')
    need(count==166,'complete four-point nontrivial downset count')
    return {'ground_points':4,'family_masks_examined':65536,'nontrivial_labelled_downsets':count,
            'maximum_center_choices':centers,'all_seed_entries':entries,'maximum_R':str(maximum),
            'complete_seed_digest':digest.hexdigest(),'scope':'affine seeds only; not full augmented certificates for every family'}


def minimum_seed():
    D=[0,1,2,3,4,5]; outside={(3,2):-1,(3,4):1,(5,2):1,(5,4):-1}
    def entry(a,z):
        if a==z:return F(2)
        if a&1 and z&1:return F(-1)
        if not a&1 and not z&1:return F(-2)
        x,y=(a,z) if a&1 else (z,a);return F(outside.get((x,y),0))
    return D,[[entry(a,z) for z in D[1:]] for a in D[1:]]


def two_star_indefinite_seed():
    D=[0,1,2,3,4,8];a=F(3)
    cross={2:F(1),4:a,8:-1-a}
    def entry(x,y):
        if x==y:return F(1)
        if x&1 and y&1:return F(-1)
        if not x&1 and not y&1:return F(-1,2)
        s,b=(x,y) if x&1 else (y,x);return cross[b] if s==1 else -cross[b]
    C=[[entry(x,y) for y in D[1:]] for x in D[1:]]
    v=[1,0,-1,-1,1]
    need(dot(v,mv(C,v))==-21,'indefinite n2 seed witness')
    return D,C


def polynomial_checks():
    # Tiny independently implemented polynomial arithmetic in n,b, with no CAS.
    def add(a,b):
        z=a.copy()
        for p,v in b.items():z[p]=z.get(p,0)+v
        return {p:v for p,v in z.items() if v}
    def scale(a,k):return {p:k*v for p,v in a.items() if k*v}
    def mul(a,b):
        z={}
        for (i,j),v in a.items():
            for (k,l),w in b.items():z[i+k,j+l]=z.get((i+k,j+l),0)+v*w
        return {p:v for p,v in z.items() if v}
    n={(1,0):1};b={(0,1):1};one={(0,0):1}
    np=add(n,one);bp=add(b,one);nb=mul(n,b)
    # nb[4+2(n/b-1)-(1+1/n)(1+1/b)]
    plus=add(add(scale(nb,2),scale(mul(n,n),2)),scale(mul(np,bp),-1))
    plus_fact=mul(add(n,scale(one,-1)),add(add(b,scale(n,2)),one))
    need(plus==plus_fact,'positive shift cleared identity')
    # nb[4-2(n/b-1)-(1+1/n)(1+1/b)]
    minus=add(add(scale(nb,6),scale(mul(n,n),-2)),scale(mul(np,bp),-1))
    minus_fact=add(mul(n,add(scale(n,3),scale(one,-7))),
                   mul(add(scale(n,5),scale(one,-1)),add(add(b,scale(n,-1)),one)))
    need(minus==minus_fact,'negative shift cleared identity')
    substitute_n2={}
    for (i,j),v in minus.items():substitute_n2[0,j]=substitute_n2.get((0,j),0)+v*2**i
    need(substitute_n2=={(0,1):9,(0,0):-11},'n2 shift boundary:9b-11=7+9(b-2)')
    return {'cleared_exact_polynomial_identities':3,
            'plus_numerator':'(n-1)(b+2n+1)',
            'minus_numerator':'n(3n-7)+(5n-1)(b-n+1)',
            'n2_minus_numerator':'7+9(b-2)',
            'proof_domain':'n>=2,b>=max(2,n-1); tail factors in[0,1]',
            'unformalized_sign_bridge':'For n>=3 both summands in minus are nonnegative with positive first; n2 uses last expression. Opposite sign uses4-kappa0^2>=7/4.'}


def controls():
    oracle_cases=accepted=0
    for values in product((-1,0,1),repeat=6):
        a=[[values[0],values[1],values[2]],[values[1],values[3],values[4]],[values[2],values[4],values[5]]]
        expected=all(determinant([[a[i][j] for j in inds] for i in inds])>=0
                     for k in range(1,4) for inds in combinations(range(3),k))
        try:psd_rank(a);actual=True
        except ValueError:actual=False
        need(actual==expected,'all-principal-minor PSD oracle')
        oracle_cases+=1;accepted+=actual
    D,C=minimum_seed();rejected=[]
    mutations=[('asymmetric_core',lambda z:z[0].__setitem__(1,z[0][1]+1)),
               ('wrong_diagonal',lambda z:z[0].__setitem__(0,3)),
               ('float_entry',lambda z:z[0].__setitem__(0,2.0)),
               ('wrong_intersection',lambda z:(z[0].__setitem__(2,0),z[2].__setitem__(0,0))),
               ('lost_centering',lambda z:(z[0].__setitem__(1,1),z[1].__setitem__(0,1)))]
    for name,mutate in mutations:
        bad=[row[:] for row in C];mutate(bad)
        try:core_check(D,bad,0)
        except ValueError:rejected.append(name)
        else:raise ValueError('damaged mathematical input accepted:'+name)
    for name,bad_D,c in [('non_downset',[0,1,3],0),('inactive_center',D,8)]:
        try:geometry(bad_D,c)
        except ValueError:rejected.append(name)
        else:raise ValueError('damaged family accepted:'+name)
    try:psd_rank([[0,1],[1,0]])
    except ValueError:rejected.append('zero_diagonal_nonzero_indefinite_row')
    else:raise ValueError('indefinite zero-diagonal matrix accepted')
    try:finish('below_recipe_threshold',D,C,0,u=1)
    except ValueError:rejected.append('below_sufficient_recipe_count')
    else:raise ValueError('below recipe threshold accepted')
    return {'symmetric_ternary_3x3_oracle_cases':oracle_cases,'PSD_cases':accepted,
            'damaged_inputs_rejected':rejected,'below_recipe_is_nonexistence_claim':False}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path);args=p.parse_args()
    census=all_four_point_seeds();records=[]
    D,C=minimum_seed();records.append(finish('minimum',D,C,0,expected_hash='2e293f1a4f010b7777d57c8f8b29ba8007f3d63a9fab3f9d19bbc92dd7af94f2'))
    for label,D,h in [('V',[0,1,2,3,4,5],'36e981261254ed628d8d7829e9ffa1223738d120b1c1cf46caa373ebbd9960b4'),('cube3',list(range(8)),'2c0d50ed7f217c514d9b46b58616558c4cc2c046ade418c6f51560c3d4226131')]:
        E,C,_=seed(D,0);records.append(finish(label,E,C,0,expected_hash=h))
    D,C=two_star_indefinite_seed();records.append(finish('new_n2_indefinite',D,C,0))
    result={'agent':'six-reviewer-1','role':'independent mathematical reviewer','target_height':8391,
            'target_ref':'bafkreibkyqrwxnrqjdwlt3hvkhe23xqcdqtcrrz4soob4o2cyvt3xaclmu',
            'proof_status':'Exact independent finite evidence; all-order real proof and n2 refinement unformalized in REVIEW.md',
            'method':'Literal member entries, integer contrast vectors, fraction-free symmetric congruences; no target imports',
            'four_point_seed_census':census,'records':records,
            'n2_refinement_sign_certificates':polynomial_checks(),'controls':controls()}
    text=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    else:print(text,end='')


if __name__=='__main__':main()
