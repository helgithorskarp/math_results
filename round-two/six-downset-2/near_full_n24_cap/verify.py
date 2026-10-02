"""Exact n24 S7 cap certificate. Actual six-downset-2, researcher.

RREF, independent completion, projection metric, literal n6 baseline and
both PSD algorithms retain the published9017 source credits. No solver
or floating input is in this checker. Whole-space bridges are ordinary.
"""
import argparse,copy,hashlib,itertools,json
from fractions import Fraction as Q
from math import comb
from pathlib import Path
from exact import bareiss_rank,both,schur_rank
from model import affine,blocks,choose,original,parameters,require
ROOT=Path(__file__).resolve().parent

def rational_strings(values):
    require(all(type(v) is str for v in values), "Rational strings required")
    return [Q(v) for v in values]


def digest(matrix):
    raw = json.dumps([[str(v) for v in row] for row in matrix],
                     separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def closed_complete(n, meta, values):
    """Independent direct two-row completion, without using RREF."""
    r, N, s = parameters(n)
    beta = [[Q(0)]*(r+1) for _ in range(r+1)]
    require(len(values) == len(meta["free_pairs"]), "Closed free-value count")
    for (a, b), value in zip(meta["free_pairs"], values):
        require(a >= 3 and b >= 3, "Closed decoder free face")
        beta[a][b] = beta[b][a] = value
    for a in range(3, r+1):
        b = n-a
        total = sum(beta[a][k]*choose(b, k) for k in range(3, r+1))
        star = sum(beta[a][k]*choose(b-1, k-1) for k in range(3, r+1))
        v = Q(b*(s-star)-(N-1-s-total), comb(b, 2))
        u = s-star-(b-1)*v
        beta[2][a] = beta[a][2] = v
        beta[1][a] = beta[a][1] = u
    total = sum(beta[2][a]*choose(n-2, a) for a in range(3, r+1))
    star = sum(beta[2][a]*choose(n-3, a-1) for a in range(3, r+1))
    beta[2][2] = Q((n-2)*(s-star)-(N-1-s-total), comb(n-2, 2))
    beta[1][2] = beta[2][1] = s-star-(n-3)*beta[2][2]
    beta[1][1] = s-sum(beta[1][a]*choose(n-2, a-1) for a in range(2, r+1))
    for a in range(1, r+1):
        require(sum(beta[a][b]*choose(n-a, b) for b in range(1, r+1)) == N-1-s,
                "Closed center residual")
        require(sum(beta[a][b]*choose(n-a-1, b-1) for b in range(1, r+1)) == s,
                "Direct excluding-point star residual")
    return beta


def decoded(n, meta, recover, values):
    beta = recover(values)
    require(beta == closed_complete(n, meta, values), "Independent completion agreement")
    return beta


def projection_gram(g, aa, j):
    d = len(g)
    if j >= 2:
        return [[Q(g[i]*int(i == k)) for k in range(d)] for i in range(d)]
    if j == 1:
        return [[Q(g[i]*int(i == k))-Q(g[i]*g[k], sum(g))
                 for k in range(d)] for i in range(d)]
    M = [[sum(g[a]*aa[a]**(i+k) for a in range(d)) for k in range(2)] for i in range(2)]
    det = M[0][0]*M[1][1]-M[0][1]**2
    require(det > 0, "Positive constant/cardinality moment determinant")
    Mi = [[Q(M[1][1], det), Q(-M[0][1], det)],
          [Q(-M[0][1], det), Q(M[0][0], det)]]
    return [[Q(g[i]*int(i == k))-g[i]*g[k]*sum(
        aa[i]**a*Mi[a][b]*aa[k]**b for a in range(2) for b in range(2))
        for k in range(d)] for i in range(d)]


def check_original(n, C, L, F):
    r, N, s = parameters(n)
    require(len(L) == N and all(sum(row) == N for row in L), "Original rows/empty loop")
    for i, A in enumerate([0]+F):
        for k, B in enumerate([0]+F):
            require(L[i][k] == L[k][i], "Original symmetry")
            if A & B:
                require(L[i][k] == s*int(i == k), "Original intersecting support")
    for point in range(n):
        x = [int(bool(A & (1 << point))) for A in F]
        require(sum(x) == s and all(sum(v*x[k] for k, v in enumerate(row)) == 0 for row in C),
                "Original exact star kernel")


def literal_baseline():
    n = 6
    meta, recover = affine(n)
    beta = decoded(n, meta, recover, [Q(24)])
    require([list(p) for p in meta["free_pairs"]] == [[3, 3]], "Published rank-four baseline coordinate")
    records = []
    for t in (Q(0), Q(1, 528)):
        F, C, L = original(n, beta, t)
        check_original(n, C, L, F)
        N = meta["N"]
        lower_rank = N-n-(not t)
        both(L, lower_rank)
        upper = [[Q(N*int(i == k))-v-Q(1, 8)*(int(i == k)-Q(1, N))
                  for k, v in enumerate(row)] for i, row in enumerate(L)]
        both(upper, N-1)
        columns = 0
        for j, aa, g, K, U in blocks(n, beta, t)[:2]:
            for bindex, b in enumerate(aa):
                vector = [Q(int(A.bit_count() == b))*(
                    1 if j == 0 else int(bool(A & 1))-int(bool(A & 2))) for A in F]
                image = [sum(v*vector[k] for k, v in enumerate(row)) for row in C]
                predicted = [K[aa.index(A.bit_count())][bindex]*(
                    1 if j == 0 else int(bool(A & 1))-int(bool(A & 2))) for A in F]
                require(image == predicted, "Definition-level constant/point action")
                columns += 1
        records.append({"t": str(t), "N": N, "lower_rank": int(lower_rank),
                        "upper_gap_rank": N-1, "action_columns": columns,
                        "full_L_sha256": digest(L)})
    return records


def determinant_small(A):
    d = len(A)
    total = 0
    for permutation in itertools.permutations(range(d)):
        sign = (-1)**sum(permutation[i] > permutation[k] for i in range(d) for k in range(i+1, d))
        value = sign
        for i in range(d):
            value *= A[i][permutation[i]]
        total += value
    return total


def rejected(operation):
    try:
        operation()
    except ValueError:
        return True
    return False


def arithmetic_audit():
    positive = 0
    for values in itertools.product((-1, 0, 1), repeat=6):
        A = [[0]*3 for _ in range(3)]
        for (i, k), v in zip(((0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)), values):
            A[i][k] = A[k][i] = v
        criterion = all(determinant_small([[A[i][k] for k in subset] for i in subset]) >= 0
                        for size in (1, 2, 3) for subset in itertools.combinations(range(3), size))
        outcomes = [not rejected(lambda method=method: method(A))
                    for method in (bareiss_rank, schur_rank)]
        require(outcomes == [criterion, criterion], "Separate all-principal-minor PSD audits")
        positive += criterion
    require(positive == 24, "Ternary audit count")
    return {"all_symmetric_ternary_3x3": 729, "PSD": positive}


def seed_fixture(doc):
    require((doc['n'],doc['r'],doc['N'],doc['s'])==(24,22,16777191,8388584),
            'Fixed n24 domain')
    require(doc['common_denominator']==10**9,'Declared common denominator')
    require(doc['repair_endpoint']=='1/86856','Exact endpoint')
    require(doc['proper_support_cutoff']==7,'Stated support cutoff')
    meta,recover=affine(24)
    require(doc['free_pairs']==[list(p) for p in meta['free_pairs']], 'Complete free-pair census')
    values=rational_strings(doc['free_values'])
    require(len(values)==100 and all(10**9%v.denominator==0 for v in values),
            'One hundred common-denominator coordinates')
    beta=decoded(24,meta,recover,values)
    require(all(beta[a][b]==0 for a in range(8,23) for b in range(8,23) if a+b<24),
            'All proper bulk couplings above7 vanish')
    return meta,beta


def seed_checks(doc):
    meta,beta=seed_fixture(doc)
    n,N,s=24,16777191,8388584
    endpoint=Q(doc['repair_endpoint'])
    records=[]
    for t in (Q(0),endpoint):
        total,rank_total,details=0,0,[]
        for j,aa,g,K,U in blocks(n,beta,t):
            d=len(aa)
            require(all(v>0 for v in g),'Positive sector metric')
            require(j or all(sum(K[i][k]*aa[k] for k in range(d))==0 for i in range(d)),
                    'Degree-zero cardinality kernel')
            if j==1 or j==0 and not t:
                require(all(sum(row)==0 for row in K),'Constant/point kernel')
            expected=d-(2 if j==0 and not t else 1 if j in (0,1) else 0)
            lower=[[g[i]*v for v in row] for i,row in enumerate(K)]
            both(lower,expected)
            if not t:
                P=projection_gram(g,aa,j)
                both([[lower[i][k]-P[i][k] for k in range(d)] for i in range(d)],expected)
            floor=Q(1,4) if not t else Q(1,8)
            upper=[[g[i]*(v-floor*int(i==k)) for k,v in enumerate(row)] for i,row in enumerate(U)]
            both(upper,d)
            mult=comb(n,j)-(comb(n,j-1) if j else 0)
            total+=mult*d
            rank_total+=mult*expected
            details.append([j,d,mult,expected,digest(lower),digest(upper)])
        require(total==N-1 and rank_total==N-n-(2 if not t else 1),'Whole original dimensions/ranks')
        records.append({'t':str(t),'full_lower_rank':rank_total+1,
                        'full_upper_rank':N-1,'upper_floor':str(floor),'blocks':details})
    h=N-s
    classes=[]
    positive_mass=Q(0)
    for a in range(6,19):
        for b in range(a,19):
            if a+b>=n or beta[a][b]<=0:
                continue
            count=comb(n,a)*comb(n-a,b)//(2 if a==b else 1)
            mass=Q(count,h)*beta[a][b]
            positive_mass+=mass
            classes.append([a,b,str(beta[a][b]),count,str(mass)])
    B=sum(a*a*comb(n,a) for a in range(3,6))
    R=s-12*n*n
    require(6*B<=R and positive_mass>Q(1,2*n*n),'9471 sufficient-tail baseline and realized positive mass')
    require(any(a==7 for a,b,value,count,mass in classes),'Seed uses actual layer7 bulk entries')
    return {'n':n,'N':N,'s':s,'affine_rank':meta['affine_rank'],'free_coordinates':100,
            'zero_free_coordinates':sum(v=='0' for v in doc['free_values']),
            'proper_support_cutoff':7,'seed_projected_lower_floor':'1',
            'parameters':records,'positive_bulk_mass_k5':str(positive_mass),
            'positive_bulk_classes':classes,'credited9471_tail_control':{'B':B,'R':R,'holds':True},
            'minimum_support_cutoff_bracket':[6,7]}


def rectangular_rank(rows):
    A=[[Q(v) for v in row] for row in rows]
    if not A:
        return 0
    rank=0
    for col in range(len(A[0])):
        hit=next((i for i in range(rank,len(A)) if A[i][col]),None)
        if hit is None:
            continue
        A[rank],A[hit]=A[hit],A[rank]
        pivot=A[rank][col]
        A[rank]=[v/pivot for v in A[rank]]
        for i in range(rank+1,len(A)):
            factor=A[i][col]
            if factor:
                A[i]=[v-factor*w for v,w in zip(A[i],A[rank])]
        rank+=1
        if rank==len(A):
            break
    return rank


def matchings(points):
    if not points:
        yield []
        return
    first=points[0]
    for k in range(1,len(points)):
        other=points[k]
        remainder=points[1:k]+points[k+1:]
        for tail in matchings(remainder):
            yield [(first,other)]+tail


def harmonic_literal_control():
    """Entire n6 spaces/actions from literal pairs, not a second block call."""
    n=6
    layers={a:[A for A in range(1<<n) if A.bit_count()==a] for a in range(n+1)}
    F=[A for A in range(1,1<<n) if A.bit_count()<=4]
    meta,recover=affine(n)
    beta=decoded(n,meta,recover,[Q(24)])
    data=[]
    spans=[]
    for j in range(4):
        selected=[]
        for chosen in itertools.combinations(range(n),2*j):
            for pairing in matchings(list(chosen)):
                vector=[]
                for A in layers[j]:
                    value=1
                    for u,v in pairing:
                        value*=int(bool(A&(1<<u)))-int(bool(A&(1<<v)))
                    vector.append(value)
                if rectangular_rank(selected+[vector])>len(selected):
                    selected.append(vector)
        required=comb(n,j)-(comb(n,j-1) if j else 0)
        require(len(selected)==required,'Whole literal harmonic dimension')
        for h in selected:
            if j:
                require(all(sum(h[k] for k,S in enumerate(layers[j]) if S&T==T)==0
                            for T in layers[j-1]),'Literal harmonic lowering')
            for a in range(max(1,j),min(4,n-j)+1):
                lift=[sum(h[k] for k,S in enumerate(layers[j]) if S&A==S)
                      if A.bit_count()==a else 0 for A in F]
                require(sum(v*v for v in lift)==comb(n-2*j,a-j)*sum(v*v for v in h),
                        'Literal higher-degree lift norm')
                spans.append(lift)
                data.append((j,a,lift))
    require(len(spans)==56 and rectangular_rank(spans)==56,'Entire nonempty literal span')
    actions=0
    for t in (Q(0),Q(1,528)):
        _,C,_=original(n,beta,t)
        sector={j:(aa,K) for j,aa,g,K,U in blocks(n,beta,t)}
        for j,b,vector in data:
            aa,K=sector[j]
            source_index=aa.index(b)
            for i,A in enumerate(F):
                a=A.bit_count()
                if a not in aa:
                    predicted=Q(0)
                else:
                    # Recover the selected literal h from this lift using the
                    # defining subset sum; at j this is the harmonic itself.
                    current=data.index((j,b,vector))
                    base_index=current-(b-max(1,j))
                    base=data[base_index][2]
                    if j==0:
                        lifted=1
                    elif j==1:
                        lifted=sum(base[k] for k,S in enumerate(F) if S.bit_count()==1 and S&A==S)
                    else:
                        lifted=sum(base[k] for k,S in enumerate(F) if S.bit_count()==j and S&A==S)
                    predicted=K[aa.index(a)][source_index]*lifted
                image=sum(C[i][k]*vector[k] for k in range(len(F)))
                require(image==predicted,'Entire literal harmonic action')
            actions+=1
    return {'original_nonempty_span':56,'harmonic_dimensions':[1,5,9,5],
            'full_action_columns':actions,'whole_action_positions':actions*56}


def controls(seed):
    cases=[]
    for name,alter in [
        ('missing coordinate',lambda d:d['free_values'].pop()),
        ('floating coordinate',lambda d:d['free_values'].__setitem__(0,0.5)),
        ('wrong common denominator',lambda d:d.__setitem__('common_denominator',1000)),
        ('wrong support cutoff',lambda d:d.__setitem__('proper_support_cutoff',6)),
        ('changed proper bulk support',lambda d:d['free_values'].__setitem__(75,'1/1000000000'))]:
        wrong=copy.deepcopy(seed);alter(wrong)
        require(rejected(lambda:seed_fixture(wrong)),'Reject '+name)
        cases.append(name)
    wrong=copy.deepcopy(seed);wrong['free_values'][0]='1000000000'
    require(rejected(lambda:seed_checks(wrong)),'Damaged seed positivity')
    cases.append('damaged lower seed')
    meta,recover=affine(6);beta=recover([Q(24)])
    F,C,L=original(6,beta);L[0][0]+=1
    require(rejected(lambda:check_original(6,C,L,F)),'Damaged actual empty loop')
    cases.append('actual empty loop')
    require(rejected(lambda:original(24,seed_fixture(seed)[1])),'Forbid n24 literal allocation')
    cases.append('n24 original allocation')
    require(rejected(lambda:both([[Q(1),Q(2)],[Q(2),Q(1)]])),'Indefinite PSD input')
    cases.append('indefinite PSD input')
    return cases


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',type=Path)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    seed=json.loads((ROOT/'seed.json').read_text())
    result={'agent':'six-downset-2','role':'researcher',
            'status':'Exact n24 certificate; ordinary bridges unformalized; independent review unclaimed',
            'seed':seed_checks(seed),'literal_published_n6_baseline':literal_baseline(),
            'whole_literal_harmonic_control':harmonic_literal_control(),
            'arithmetic_audit':arithmetic_audit(),'rejected_controls':controls(seed),
            'seed_sha256':hashlib.sha256((ROOT/'seed.json').read_bytes()).hexdigest(),
            'arithmetic':'integers and fractions.Fraction','no_literal_n24_matrix':True}
    body=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.check:
        require(body==args.check.read_text(),'Whole frozen record mismatch')
    if args.output:
        args.output.write_text(body)
    print(json.dumps({'ok':True,'record_sha256':hashlib.sha256(body.encode()).hexdigest(),
                      'full_n24_sectors':26,'literal_action_columns':112,
                      'controls':len(result['rejected_controls'])}))


if __name__=='__main__':
    main()
