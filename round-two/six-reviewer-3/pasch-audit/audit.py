"""Independent Pasch perturbation audit; six-reviewer-3, reviewer.
Standard library only. No campaign/author imports. Exact finite controls
supplement the ordinary all-order argument in REVIEW.md.
"""
import argparse
from fractions import Fraction as F
from itertools import combinations, product
import hashlib
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def transpose(a):
    return [list(c) for c in zip(*a)]


def multiply(a, b):
    return [[sum(x*y for x,y in zip(r,c)) for c in zip(*b)] for r in a]


def subtract(a, b):
    return [[x-y for x,y in zip(r,s)] for r,s in zip(a,b)]


def determinant(a):
    if not a:
        return F(1)
    m=[list(map(F,r)) for r in a]
    out=F(1)
    for k in range(len(m)):
        piv=next((i for i in range(k,len(m)) if m[i][k]),None)
        if piv is None:
            return F(0)
        if piv!=k:
            m[k],m[piv]=m[piv],m[k]
            out=-out
        q=m[k][k]
        out*=q
        for i in range(k+1,len(m)):
            t=m[i][k]/q
            for j in range(k+1,len(m)):
                m[i][j]-=t*m[k][j]
    return out


def psd_rank(a):
    require(a==transpose(a),'nonsymmetric matrix')
    m=[list(map(F,r)) for r in a]
    rank=0
    while m:
        require(all(m[i][i]>=0 for i in range(len(m))),'negative diagonal')
        piv=next((i for i in range(len(m)) if m[i][i]>0),None)
        if piv is None:
            require(not any(x for r in m for x in r),'nonzero zero-diagonal remainder')
            break
        indices=[i for i in range(len(m)) if i!=piv]
        m=[[m[i][j]-m[i][piv]*m[piv][j]/m[piv][piv] for j in indices] for i in indices]
        rank+=1
    return rank


def completion(v, blocks):
    return [[int(tuple(sorted((*p,x))) in blocks) if x not in p else 0
             for p in combinations(range(v),2)] for x in range(v)]


def gram_from_links(v, blocks):
    links=[{tuple(y for y in t if y!=x) for t in blocks if x in t} for x in range(v)]
    return [[len(a&b) for b in links] for a in links]


def parity_sides(groups):
    sides=[set(),set()]
    for bits in product(range(2),repeat=3):
        sides[sum(bits)%2].add(tuple(sorted(groups[i][bits[i]] for i in range(3))))
    return sides


def check_design(v, lam, blocks):
    require(len(blocks)==lam*v*(v-1)//6,'wrong block count')
    require(all(len(t)==3 and tuple(sorted(set(t)))==t for t in blocks),'bad triple')
    degrees=[sum(set(p)<=set(t) for t in blocks) for p in combinations(range(v),2)]
    reps=[sum(x in t for t in blocks) for x in range(v)]
    require(set(degrees)=={lam},'pair degrees')
    require(set(reps)=={lam*(v-1)//2},'point replications')
    return degrees,reps


def literal_witness():
    # Public six-downset-2 data, reconstructed independently as tuple triples.
    masks=(1482252,1681832,2001546,991329,418224,120368)
    outside_triples=((0,1,2),(0,1,3),(0,1,4),(0,2,3),(0,2,5),
                     (1,2,4),(1,2,6),(0,3,5),(1,5,6),(2,4,6))
    groups=((0,1),(2,3),(4,5))
    blocks=set(parity_sides(groups)[0])
    for group in range(3):
        for other in range(3):
            if group!=other:
                blocks.add(tuple(sorted((*groups[group],groups[other][0]))))
    for i,j in combinations(range(3),2):
        for a,b in product(range(2),repeat=2):
            ends=groups[i][a],groups[j][b]
            outs=[6,7] if a!=b else [8]
            if a==b==1:
                outs.extend([9,10])
            for x in outs:
                blocks.add(tuple(sorted((*ends,x))))
    for pair in groups:
        for x in (11,12):
            blocks.add(tuple(sorted((*pair,x))))
    for x in range(6):
        mask=masks[x//2 + 3*(x%2)]
        for k,p in enumerate(combinations(range(6,13),2)):
            if (mask>>k)&1:
                blocks.add((x,*p))
    blocks.update(tuple(6+x for x in t) for t in outside_triples)
    return blocks,groups


def characteristic(a):
    # Faddeev--LeVerrier over integers, checking every division.
    n=len(a)
    b=[[int(i==j) for j in range(n)] for i in range(n)]
    cs=[1]
    for k in range(1,n+1):
        b=multiply(a,b)
        tr=sum(b[i][i] for i in range(n))
        require(tr%k==0,'characteristic division')
        ck=-tr//k
        cs.append(ck)
        for i in range(n):
            b[i][i]+=ck
    require(not any(x for r in b for x in r),'Cayley-Hamilton remainder')
    return cs


def verify_witness():
    v,lam=13,4
    before,groups=literal_witness()
    degrees,reps=check_design(v,lam,before)
    even,odd=parity_sides(groups)
    require(even<=before and not (odd&before),'illegal witness switch')
    after=(before-even)|odd
    check_design(v,lam,after)
    c,c1=completion(v,before),completion(v,after)
    g,g1=multiply(c,transpose(c)),multiply(c1,transpose(c1))
    require(g==gram_from_links(v,before) and g1==gram_from_links(v,after),'link/completion mismatch')
    delta=subtract(g1,g)
    require(all(sum(r)==0 for r in delta),'constant not killed')
    vec=[7,-7,7,-7,7,-7,6,6,-6,-3,-3,0,0]
    require(sum(vec)==0 and sum(x*x for x in vec)==420,'eigenvector normalization')
    require([sum(a*b for a,b in zip(r,vec)) for r in delta]==[14*x for x in vec],'eigenvalue 14')
    char=characteristic(delta)
    # t^9 (t+4)^2 (t+6) (t-14)
    expected=[1,0,-132,-800,-1344]+[0]*9
    require(char==expected,'full characteristic polynomial')
    ranks=[]
    for sign in (-1,1):
        form=[[14*(int(i==j)-F(1,v))+sign*delta[i][j] for j in range(v)] for i in range(v)]
        ranks.append(psd_rank(form))
    require(ranks==[11,12],'signed endpoint ranks')
    comp=set(combinations(range(v),3))-before
    comp_after=set(combinations(range(v),3))-after
    check_design(v,7,comp)
    require(subtract(gram_from_links(v,comp_after),gram_from_links(v,comp))==delta,'complement difference')
    # At least one genuinely indefinite control must be rejected.
    try:
        psd_rank([[13*(int(i==j)-F(1,v))-delta[i][j] for j in range(v)] for i in range(v)])
    except ValueError:
        rejected=True
    else:
        rejected=False
    require(rejected,'smaller-budget control accepted')
    digest=lambda x: hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
    return {'blocks':len(before),'pair_count':len(degrees),'pair_multiplicity':4,
            'replications':reps,'delta_sha256':digest(delta),
            'blocks_sha256':digest(sorted(before)), 'characteristic_coefficients':char,
            'signed_14K_ranks':ranks,'eigenvector_squared_norm':420,
            'complement_multiplicity':7,'smaller_budget_rejected':rejected}


def verify_local_update():
    groups=((0,1),(2,3),(4,5))
    even,odd=parity_sides(groups)
    free=sorted(set(combinations(range(6),3))-even-odd)
    pairs=list(combinations(range(6),2))
    a=[[int(x==2*j)-int(x==2*j+1) for j in range(3)] for x in range(6)]
    w=[]
    for pair in pairs:
        row=[]
        for k in range(3):
            others=[j for j in range(3) if j!=k]
            if {x//2 for x in pair}==set(others):
                row.append(1 if sum(x%2 for x in pair)%2 else -1)
            else:
                row.append(0)
        w.append(row)
    update=multiply(a,transpose(w))
    transcript=hashlib.sha256()
    for bits in product(range(2),repeat=12):
        before=even|{t for t,b in zip(free,bits) if b}
        after=(before-even)|odd
        c,c1=completion(6,before),completion(6,after)
        require(subtract(c1,c)==update,'entrywise switch identity')
        y=[[z+2*t for z,t in zip(r,s)] for r,s in zip(multiply(c,w),a)]
        require(all(y[2*i+1][j]==-y[2*i][j] for i,j in product(range(3),repeat=2)),'pair-sum mode')
        t=[y[2*i] for i in range(3)]
        require(all(t[i][i]==0 for i in range(3)),'T diagonal')
        require(all(abs(z)<=1 for r in t for z in r),'T range')
        direct=subtract(gram_from_links(6,after),gram_from_links(6,before))
        ya=multiply(y,transpose(a))
        lowrank=[[ya[i][j]+ya[j][i] for j in range(6)] for i in range(6)]
        require(direct==lowrank,'rank-six identity')
        # Every reverse starts from after with -W, giving -Y and -Delta.
        reverse_y=[[z+2*s for z,s in zip(r,q)] for r,q in zip(multiply(c1,[[-z for z in r] for r in w]),a)]
        require(reverse_y==[[-z for z in r] for r in y],'reverse orientation')
        transcript.update(json.dumps(t,separators=(',',':')).encode())
    return {'fills':4096,'oriented_checks':8192,'T_transcript_sha256':transcript.hexdigest()}


def verify_inside_bounds():
    alpha=(0,2,4,5,6,7,8)
    counts=[0]*7
    off=[(i,j) for i,j in product(range(3),repeat=2) if i!=j]
    for xs in product((-1,0,1),repeat=6):
        t=[[0]*3 for _ in range(3)]
        for (i,j),x in zip(off,xs):
            t[i][j]=x
        e=sum(x!=0 for x in xs)
        d=[[2*(t[i][j]+t[j][i]) for j in range(3)] for i in range(3)]
        for sign in (-1,1):
            m=[[alpha[e]*int(i==j)+sign*d[i][j] for j in range(3)] for i in range(3)]
            for size in (1,2,3):
                for inds in combinations(range(3),size):
                    require(determinant([[m[i][j] for j in inds] for i in inds])>=0,'inside minor')
        counts[e]+=1
    # The universal comparison after using p >= ceil(e/2).
    offsets=[(8-alpha[e])*10+8*e+4*((e+1)//2)-60 for e in range(7)]
    require(min(offsets)>=0,'mu>=3 comparison')
    # k=2+2sqrt(7): exact margins a+b sqrt(7) against 2(24-6e).
    margins=[(-16,8),(-8,4),(0,0),(10,-2)]
    def nonnegative(a,b):
        if a>=0 and b>=0:return True
        if a<0 and b<0:return False
        return 7*b*b>=a*a if b>=0 else a*a>=7*b*b
    require(all(nonnegative(a,b) for a,b in margins),'refined mu2 margin')
    # k>5 follows sqrt(7)>3/2; and k<22/3 follows sqrt(7)<8/3.
    require(7>F(9,4) and 7<F(64,9),'mu2 budget comparison')
    return {'directed_matrices':sum(counts),'by_e':counts,'signed_minor_checks':729*2*7,
            'mu_ge3_offsets_at_10':offsets,'mu2_budget':'2+2sqrt(7)',
            'mu2_margins_a_plus_b_sqrt7':[list(x) for x in margins]}


def verify_column_identity():
    for u0,u1,z0,z1 in product(range(2),repeat=4):
        n=u0+u1+z0+z1
        c=abs(u0-u1)+abs(z0-z1)
        lhs=max(u1+z0,u0+z1)+max(u0+z0,u1+z1)
        require(lhs==n+int(c>0),'square-budget identity')
        require(c<=n<=4-c,'inside bit capacity')
        h=[1-u-z for u,z in product((u0,u1),(z0,z1))]
        if min(h)>=0:
            require(c<=1,'mu2 column quota')
    return {'Boolean_patterns':16}


def verify_mu_one_boundary():
    fano={t for t in combinations(range(7),3) if (t[0]+1)^(t[1]+1)^(t[2]+1)==0}
    check_design(7,1,fano)
    def matchings(xs):
        if not xs:
            yield ()
        else:
            for j in range(1,len(xs)):
                for rest in matchings(xs[1:j]+xs[j+1:]):
                    yield ((xs[0],xs[j]),)+rest
    choice=None
    for support in combinations(range(7),6):
        for groups in matchings(support):
            even,odd=parity_sides(groups)
            if even<=fano and not (odd&fano):
                choice=(even,odd)
                break
        if choice:
            break
    require(choice is not None,'no boundary legal move')
    even,odd=choice
    after=(fano-even)|odd
    check_design(7,1,after)
    require(gram_from_links(7,fano)==gram_from_links(7,after),'lambda-one defect changes')
    universe=set(combinations(range(7),3))
    comp,comp_after=universe-fano,universe-after
    check_design(7,4,comp)
    check_design(7,4,comp_after)
    require(gram_from_links(7,comp)==gram_from_links(7,comp_after),'q-one defect changes')
    return {'v':7,'checked_multiplicities':[1,4],'legal_moves':2,'defect_changes_zero':True}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',type=Path)
    args=parser.parse_args()
    result={'reviewer':'six-reviewer-3','role':'reviewer','status':'COMPLETE',
            'local_update':verify_local_update(),'inside':verify_inside_bounds(),
            'column_identity':verify_column_identity(),'sharp_witness':verify_witness(),
            'mu_one_boundary':verify_mu_one_boundary()}
    output=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.check:
        require(output==args.check.read_text(),'expected output mismatch')
    print(output,end='')


if __name__=='__main__':
    main()
