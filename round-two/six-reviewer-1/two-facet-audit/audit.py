#!/usr/bin/env python3
"""Independent rational Gram reconstruction and integer congruence audit."""
import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
import json
from math import lcm
from pathlib import Path


def need(ok, message):
    if not ok:
        raise ValueError(message)


def psd(a):
    """Clear denominators, then fraction-free symmetric elimination.

    Every positive pivot is a congruence Schur step. A zero diagonal
    in a PSD residual must have a zero row. Division is exact Bareiss
    division; skipped zero rows leave the previous divisor unchanged.
    """
    n = len(a)
    need(n and all(len(r) == n for r in a), 'square')
    a = [[F(x) for x in r] for r in a]
    need(all(a[i][j] == a[j][i] for i in range(n) for j in range(n)), 'symmetric')
    d = lcm(*(x.denominator for r in a for x in r))
    a = [[int(x*d) for x in r] for r in a]
    rank, previous = 0, 1
    for k in range(n):
        pivot = a[k][k]
        need(pivot >= 0, 'negative pivot')
        if not pivot:
            need(all(a[k][j] == 0 for j in range(k+1, n)), 'zero pivot row')
            continue
        rank += 1
        for i in range(k+1, n):
            for j in range(i, n):
                value = pivot*a[i][j] - a[i][k]*a[k][j]
                need(value % previous == 0, 'nonexact division')
                a[i][j] = a[j][i] = value//previous
        previous = pivot
    return rank


def row_rank(rows):
    if not rows:
        return 0
    a = [[F(x) for x in r] for r in rows]
    n = len(a[0]); k = 0
    for j in range(n):
        p = next((i for i in range(k, len(a)) if a[i][j]), None)
        if p is None:
            continue
        a[k], a[p] = a[p], a[k]
        for i in range(k+1, len(a)):
            if a[i][j]:
                ratio = a[i][j]/a[k][j]
                a[i] = [x-ratio*y for x, y in zip(a[i], a[k])]
        k += 1
        if k == len(a):
            break
    return k


def core_to_matrix(c, s):
    # Use all rows of E explicitly, rather than special-case empty sums.
    m = len(c); n = m+1
    e = [[-1]*m]+[[int(i == j) for j in range(m)] for i in range(m)]
    ec = [[sum(F(x)*c[k][j] for k, x in enumerate(r) if x)
           for j in range(m)] for r in e]
    q = [[sum(ec[i][k]*x for k, x in enumerate(r) if x) for r in e]
         for i in range(n)]
    return [[(1+q[i][j]-s*int(i == j))/(n-s) for j in range(n)] for i in range(n)]


def fingerprint(a):
    return sha256(json.dumps([[str(x) for x in r] for r in a],
                            separators=(',', ':')).encode()).hexdigest()


def stars(f):
    need(f and f[0] == 0 and len(set(f)) == len(f), 'indexing')
    for a in f:
        need(isinstance(a, int) and a >= 0, 'mask')
        sub = a
        while True:
            need(sub in f, 'downset')
            if sub == 0:
                break
            sub = (sub-1)&a
    return max(sum(bool(a&(1 << i)) for a in f) for i in range(max(f).bit_length()))


def check(f, a, s, gap=F(0)):
    n = len(f)
    need(stars(f) == s and len(a) == n and all(len(r) == n for r in a), 'star/dimension')
    a = [[F(x) for x in r] for r in a]
    for i in range(n):
        need(sum(a[i]) == 1, 'row')
        for j in range(n):
            need(a[i][j] == a[j][i], 'symmetry')
            need(not (f[i]&f[j]) or a[i][j] == 0, 'support')
    lower = [[(n-s)*a[i][j]+s*int(i == j) for j in range(n)] for i in range(n)]
    upper = [[int(i == j)-a[i][j] for j in range(n)] for i in range(n)]
    ranks = [psd(lower), psd(upper)]
    if gap:
        need(gap > 0, 'gap positive')
        psd([[(n-s)*upper[i][j]-gap*(int(i == j)-F(1,n))
              for j in range(n)] for i in range(n)])
    return dict(N=n, s=s, lower_rank=ranks[0], upper_rank=ranks[1],
                matrix_sha256=fingerprint(a))


def cube(n):
    f = list(range(1 << n)); full = f[-1]
    return f, [[F(int((a^b) == full)) for b in f] for a in f], 1 << (n-1), 'cube'+str(n)


def proper(n):
    f = list(range((1 << n)-1)); s=(len(f)-1)//2; full=len(f)
    a = [[F(0) for _ in f] for _ in f]
    for i,x in enumerate(f):
        for j,y in enumerate(f):
            if i == j == 0:
                a[i][j]=F(1-s,s+1)
            elif i == 0 or j == 0:
                a[i][j]=F(1,s+1)
            elif x^y == full:
                a[i][j]=F(s,s+1)
    return f,a,s,'proper_cube'+str(n)


def colored(f, colors, s, name):
    # Rational regular-simplex coordinates, metric s*I.
    k=s
    need(set(colors) <= set(range(k)), 'colors')
    vectors = [[F(int(c == j))-F(1,k) for j in range(k)] for c in colors]
    c = [[s*sum(x*y for x,y in zip(v,w)) for w in vectors] for v in vectors]
    return f,core_to_matrix(c,s),s,name


def baseline():
    parts = [cube(n) for n in range(1,5)] + [proper(2),proper(3)]
    parts += [colored([0,1,2,3,4,5],[2,1,0,0,1],3,'path3'),
              colored([0,1,2,3,4,8,12],[1,1,0,0,0,1],2,'matching2')]
    f=sorted([0]+[1 << i for i in range(4)]+[(1 << i)|(1 << j) for i,j in combinations(range(4),2)])
    c=[[F(3) if a==b else F(-1) if a&b or a.bit_count()==b.bit_count()==1
        else F(1) for b in f[1:]] for a in f[1:]]
    parts += [(f,core_to_matrix(c,4),4,'uniform_rank2_4')]
    return parts


def union(parts):
    s=parts[0][2]; need(all(p[2] == s for p in parts) and len(parts)>=2, 'equal stars')
    f=[0]; vertex=[None]; offset=0
    for p,(fj,_,_,_) in enumerate(parts):
        f += [x << offset for x in fj[1:]]
        vertex += [(p,i) for i in range(1,len(fj))]
        offset += max(fj).bit_length()
    n=len(f); a=[]
    for i,x in enumerate(vertex):
        row=[]
        for j,y in enumerate(vertex):
            if x is None and y is None:
                value=(sum((len(p[0])-s)*p[1][0][0] for p in parts)+(len(parts)-1)*(s-1))/(n-s)
            elif x is None or y is None:
                k,l=x or y; value=F(len(parts[k][0])-s,n-s)*parts[k][1][0][l]
            elif x[0]==y[0]:
                k=x[0]; value=F(len(parts[k][0])-s,n-s)*parts[k][1][x[1]][y[1]]
            else:
                value=F(1,n-s)
            row.append(value)
        a.append(row)
    return f,a,s,'union('+','.join(p[3] for p in parts)+')'


def union_gamma(parts):
    m=sum(len(p[0])-1 for p in parts); delta=m-max(len(p[0])-1 for p in parts)
    h=max(len(p[0]) for p in parts);s=parts[0][2]
    return F(delta,delta+h)*sum(F(s,len(p[0])-s) for p in parts)/m


def unequal(a,b,improved=False):
    need(a>b>=1, 'unequal orders')
    t=1 << (a-1);u=1 << (b-1); big=(1 << a)-1; small=(1 << b)-1
    vertices=[(0,x,big) for x in range(1,big+1)]+[(1,x,small) for x in range(1,small+1)]
    f=[0]+[x if j==0 else x << a for j,x,_ in vertices]
    # h coefficient plus a centered pair-space residual. This is a Gram
    # construction, not the author's explicit casewise rational core.
    c=[]
    shifted=[]
    for j,x,full in vertices:
        alpha=F(1) if x==full else -F(1,t-1)
        row=[];sr=[]
        for k,y,other in vertices:
            alpha2=F(1) if y==other else -F(1,t-1)
            value=(t-1)*alpha*alpha2
            if j==k and x!=full and y!=other:
                v=(full+1)//2
                z=t-2 if x==y else 2*v-t-2 if x^y==full else -1
                value+=F(t,t-1)*z
            row.append(value)
            v=(full+1)//2
            sr.append(F(v*int(min(x,full^x)==min(y,other^y))-1+(t-v)*int(x==y)) if j==k else F(0))
        c.append(row);shifted.append(sr)
    n=len(f);beta=F((2*u-1)*(t-2*u+1),t-1)
    q=(n-1)*(t-1)+t+u-2+(t-u)*(2*u-1)
    penalty=2*u*(t-u)-1
    epsilon=beta/(2*(beta+(penalty if improved else q)))
    mixed=[[(1-epsilon)*x+epsilon*y for x,y in zip(r,sr)] for r,sr in zip(c,shifted)]
    matrix=core_to_matrix(mixed,t)
    return (f,matrix,t,'unequal_cubes(%d,%d)'%(a,b)),dict(beta=beta,q=q,penalty=penalty,epsilon=epsilon,c=c,shifted=shifted)


def tensor(parts):
    tuples=list(product(*(range(len(p[0])) for p in parts)))
    offsets=[];off=0
    for f,_,_,_ in parts:
        offsets.append(off);off+=max(f).bit_length()
    f=[sum(parts[k][0][i] << offsets[k] for k,i in enumerate(x)) for x in tuples]
    a=[]
    for x in tuples:
        row=[]
        for y in tuples:
            z=F(1)
            for k,p in enumerate(parts):z*=p[1][x[k]][y[k]]
            row.append(z)
        a.append(row)
    s=max(p[2]*(len(f)//len(p[0])) for p in parts)
    return f,a,s,'tensor('+','.join(p[3] for p in parts)+')'


def selectors(n):
    full=(1 << n)-1
    pairs=[(x,full^x) for x in range(1,full) if x<(full^x)]
    result=[]
    for choices in product((0,1),repeat=len(pairs)):
        fam=(full,)+tuple(p[c] for p,c in zip(pairs,choices))
        if all(a&b for a,b in combinations(fam,2)):
            result.append(frozenset(fam))
    need(row_rank([[int(x in fam) for x in range(1,full+1)] for fam in result])==1 << (n-1),'selector span')
    return result


def weighted_switches(n):
    # Independent weighted threshold: force A winning, all proper
    # subsets losing, and break every complementary tie by binary weights.
    full=(1 << n)-1;out=[]
    for a in range(1,full):
        k=a.bit_count();scale=1 << (n+1)
        weights=[scale*(n*(n-k)+1 if a&(1 << i) else n*k)+(1 << i) for i in range(n)]
        total=sum(weights)
        fam=frozenset(x for x in range(1,full+1) if 2*sum(weights[i] for i in range(n) if x&(1 << i))>total)
        need(a in fam and all(not (x in fam) for x in range(1,a) if x&a==x),'threshold minimum')
        alt=(fam-{a})|{full^a}
        need(len(fam)==len(alt)==1 << (n-1),'switch sizes')
        need(all(x&y for x,y in combinations(alt,2)),'switch intersection')
        out.append([sorted(fam),sorted(alt)])
    return dict(n=n,switches=len(out),sha256=sha256(json.dumps(out,separators=(',',':')).encode()).hexdigest())


def maximum_families(f):
    # All cliques of the literal nonempty intersection graph, ordered
    # recursion without symmetry quotient or pruning; at most 12 vertices.
    best=0;result=[]
    def visit(chosen,pending):
        nonlocal best,result
        if len(chosen)>best:best=len(chosen);result=[frozenset(chosen)]
        elif len(chosen)==best:result.append(frozenset(chosen))
        for i,a in enumerate(pending):
            visit(chosen+[a],[b for b in pending[i+1:] if a&b])
    visit([],f[1:])
    return best,set(result)


def two_facets(c,a,b,improved=True):
    if a<b:a,b=b,a
    if a==b:
        p=union([cube(a),cube(b)])
    else:p=unequal(a,b,improved)[0]
    return tensor([cube(c),p]) if c else p


def run():
    records=[];matrices={};spectra=[]
    def add(p,gap=F(0)):
        f,a,s,label=p;r=check(f,a,s,gap);r['label']=label
        records.append(r);matrices[label]=p;return r
    bs=baseline()
    for p in bs:add(p)
    for n,r in [(2,2),(2,3),(2,4),(3,2),(3,3),(4,2),(4,3)]:
        parts=[cube(n)]*r;p=union(parts);v=add(p,union_gamma(parts));N=v['N'];s=v['s'];B=N-s
        need(v['lower_rank']==N-r*s and v['upper_rank']==N-1,'union ranks')
        eigen={F(1):1,F(-s,B):r*s,F(s,B):r*(s-2),F(1,B):r-1,F(r*(s-1)+1,B):1}
        for x,mult in eigen.items():
            need(N-row_rank([[p[1][i][j]-x*int(i==j) for j in range(N)] for i in range(N)])==mult,'complete spectrum')
        spectra.append(dict(n=n,r=r,spectrum={str(x):m for x,m in eigen.items()}))
    for parts in [[cube(3),bs[-1]],[proper(3),bs[6]],[cube(2),bs[7],cube(2)]]:
        expected=sum(len(p[0])-check(*p[:3])['lower_rank'] for p in parts)
        p=union(parts);v=add(p,union_gamma(parts))
        need(v['N']-v['lower_rank']==expected and v['upper_rank']==v['N']-1,'mixed union ranks')
    u2=union([cube(2)]*2);u3=union([cube(2)]*3)
    products=[[u2,u2],[u2,u3]]+[[cube(c),u2] for c in (1,2,3)]
    for parts in products:
        p=tensor(parts);v=add(p);density=max(F(p[2],len(p[0])) for p in parts)
        forced=sum(len(p[0])-check(*p[:3])['lower_rank'] for p in parts if F(p[2],len(p[0]))==density)
        need(v['N']-v['lower_rank']==forced,'tensor rank')
    improved=[]
    for a,b in [(2,1),(3,1),(3,2),(4,1),(4,2),(4,3),(5,2),(5,4),(6,1)]:
        p,d=unequal(a,b);v=add(p,d['beta']/2)
        need(v['N']-v['lower_rank']==p[2] and v['upper_rank']==v['N']-1,'unequal ranks')
        new,e=unequal(a,b,True);w=check(*new[:3],e['beta']/2)
        need(w['lower_rank']==v['lower_rank'] and w['upper_rank']==v['upper_rank'],'improved ranks')
        need(e['epsilon']>=d['epsilon'],'improvement')
        N=w['N'];t=p[2];R=sum(sum(r) for r in d['shifted'])
        u=1 << (b-1);S=[[int(x) for x in r] for r in d['shifted']]
        psd([[sum(S[i][k]*S[k][j] for k in range(N-1))-(t-u)*S[i][j]
              for j in range(N-1)] for i in range(N-1)])
        seed=core_to_matrix(d['c'],t)
        check(p[0],seed,t,d['beta'])
        shifted_lower_rank=psd(d['shifted'])+1
        need(shifted_lower_rank==N-t,'shifted lower rank')
        shift=core_to_matrix(d['shifted'],t)
        Q=[[(N-t)*shift[i][j]+t*int(i==j)-1 for j in range(N)] for i in range(N)]
        psd([[(2*t+R)*(int(i==j)-F(1,N))-Q[i][j] for j in range(N)] for i in range(N)])
        improved.append(dict(a=a,b=b,old_epsilon=str(d['epsilon']),new_epsilon=str(e['epsilon']),
                             lower_slack_positive_gap=str(e['epsilon']*(t-u)),
                             enlargement=str(e['epsilon']/d['epsilon']),**w))
    for c,a,b in [(1,3,1),(2,3,2)]:
        p=tensor([cube(c),unequal(a,b)[0]]);v=add(p)
        need(v['lower_rank']==v['upper_rank']==v['N']-(1 << (c-1)),'overlap ranks')
    family_checks=[]
    # Every unordered incomparable nonempty facet pair in a four-point cube.
    for Fmask,Gmask in combinations(range(1,16),2):
        if Fmask&Gmask in (Fmask,Gmask):continue
        c=(Fmask&Gmask).bit_count();a=(Fmask&~Gmask).bit_count();b=(Gmask&~Fmask).bit_count()
        p=two_facets(c,a,b);f,m,s,_=p;v=check(f,m,s)
        original=[x for x in range(16) if x&Fmask==x or x&Gmask==x]
        best,maxima=maximum_families(original)
        need(best==s and len(original)==len(f),'facet size/maximum')
        Cmask=Fmask&Gmask
        if c:
            core_bits=[1 << i for i in range(4) if Cmask&(1 << i)]
            bases=selectors(c)
            expected={frozenset(x for x in original if sum(int(bool(x&z)) << k for k,z in enumerate(core_bits)) in base) for base in bases}
            forced=1 << (c-1)
        else:
            eligible=[h for h in (Fmask,Gmask) if h.bit_count()==max(a,b)]
            expected=set()
            for h in eligible:
                bits=[1 << i for i in range(4) if h&(1 << i)]
                for base in selectors(len(bits)):
                    expected.add(frozenset(sum(bits[k] for k in range(len(bits)) if x&(1 << k)) for x in base))
            forced=(1 << (max(a,b)-1))*len(eligible)
        need(maxima==expected,'literal complete family equality')
        centered=[[F(int(x in fam))-F(s,len(original)) for x in original] for fam in maxima]
        need(row_rank(centered)==forced and v['N']-v['lower_rank']==forced,'forced maximal rank')
        family_checks.append([Fmask,Gmask,c,a,b,len(original),len(maxima),forced])
    counts=[dict(n=n,count=len(selectors(n)),forced_dimension=1 << (n-1)) for n in range(1,6)]
    switches=[weighted_switches(n) for n in range(2,6)]
    example,d=unequal(3,1);f,_,s,_=example
    shift=core_to_matrix(d['shifted'],s);w=[0]+[5]*6+[1,6]
    bad_form=sum(w[i]*(len(f)-s)*(int(i==j)-shift[i][j])*w[j]
                 for i in range(len(f)) for j in range(len(f)))
    need(bad_form==-37,'unequal shifted cap counterexample')
    controls=[lambda:psd([[-1]]),lambda:psd([[0,1],[1,0]]),lambda:psd([[1,2],[0,1]]),
              lambda:stars([0,3]),lambda:union([cube(2),cube(3)]),lambda:unequal(2,2),
              lambda:check(cube(2)[0],cube(2)[1],1),lambda:check(f,shift,s)]
    for control in controls:
        try:control()
        except ValueError:pass
        else:raise ValueError('accepted damaged control')
    return dict(agent='six-reviewer-1',role='independent reviewer',records=records,
                full_spectra=spectra,improved_repairs=improved,selector_censuses=counts,
                threshold_switches=switches,all_four_point_facet_pairs=family_checks,
                shifted_cap_counterexample=str(bad_form),
                controls=len(controls),coverage=dict(original_matrices=len(records),
                original_matrix_entries=sum(r['N']**2 for r in records),
                independent_facet_pairs=len(family_checks),complete_selector_orders=[1,2,3,4,5],
                largest_matrix=max(r['N'] for r in records)))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path);parser.add_argument('--check',type=Path)
    args=parser.parse_args();result=run();content=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.check:need(args.check.read_text()==content,'receipt bytes')
    if args.output:args.output.write_text(content)
    print(json.dumps(dict(ok=True,coverage=result['coverage'],controls=result['controls'],
                         expected_sha256=sha256(content.encode()).hexdigest()),sort_keys=True))


if __name__=='__main__':main()
