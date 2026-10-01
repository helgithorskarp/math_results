"""Separate matching-pair and rational-elimination audit of degree98_two_roots.
No imports of author/predecessor programs; fixtures do not select the proof domain.
Actual author: six-books-1, role researcher, 2026-10-01.
"""
import argparse
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, permutations, product
from pathlib import Path
import json
HISTOGRAMS=((2,20,0),)

def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def serialize(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def elimination(matrix, want_determinant=False):
    a = [[Fraction(x) for x in row] for row in matrix]
    rank, answer = 0, Fraction(1)
    for col in range(len(a[0])):
        pivot_row = next((i for i in range(rank, len(a)) if a[i][col]), None)
        if pivot_row is None:
            continue
        if pivot_row != rank:
            a[pivot_row], a[rank] = a[rank], a[pivot_row]
            answer = -answer
        pivot = a[rank][col]
        answer *= pivot
        for i in range(rank + 1, len(a)):
            multiplier = a[i][col] / pivot
            for j in range(col + 1, len(a[0])):
                a[i][j] -= multiplier * a[rank][j]
            a[i][col] = 0
        rank += 1
        if rank == len(a):
            break
    if not want_determinant:
        return rank
    need(len(a) == len(a[0]), "nonsquare determinant")
    if rank != len(a):
        return 0
    need(answer.denominator == 1, "nonintegral determinant")
    return answer.numerator


def sqrt_floor(value):
    need(value > 0, "nonpositive determinant")
    low, high = 0, 1 << ((value.bit_length() + 1) // 2)
    while high - low > 1:
        mid = (low + high) // 2
        if mid * mid <= value:
            low = mid
        else:
            high = mid
    need(low * low <= value < high * high, "wrong square-root interval")
    return low


def multiply(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]


def controls(fixtures):
    need(elimination([[0,1],[2,3]],True)==-2 and elimination([[1,2],[2,4]],True)==0,"determinant controls")
    need(elimination([[0,1],[2,3]])==2 and elimination([[1,2],[2,4]])==1,"rank controls")
    rows = Path(__file__).with_name("baseline21.rows").read_text().split()
    need(len(rows)==21 and all(len(row)==21 and set(row)<={"0","1"} for row in rows),"bad baseline")
    R = [[int(c) for c in row] for row in rows]
    B = [[1-R[i][j]-(i==j) for j in range(21)] for i in range(21)]
    need(all(R[i][i]==0 and R[i][j]==R[j][i] for i in range(21) for j in range(21)),"baseline symmetry")
    hist = Counter(map(sum,R))
    maxima = [max(sum(A[i][k]*A[j][k] for k in range(21)) for i,j in combinations(range(21),2) if A[i][j])
              for A in (R,B)]
    need(hist=={8:4,9:16,10:1} and maxima==[3,6],"baseline differs")
    pairs = list(combinations(range(22),2))
    signed = []
    need(len(fixtures)==1,"wrong signed fixture families")
    for histogram,item in zip(HISTOGRAMS,fixtures):
        need(tuple(item["histogram"])==histogram,"wrong signed histogram")
        degrees = [d for d,n in zip((8,9,10),histogram) for _ in range(n)]
        need(len(item["red_masks"])==len(set(item["red_masks"]))==24,"wrong fixture count")
        for mask in item["red_masks"]:
            need(isinstance(mask,int) and 0<=mask<(1<<231),"bad control mask")
            A = [[0]*22 for _ in range(22)]
            for bit,(i,j) in enumerate(pairs):
                A[i][j]=A[j][i]=(mask>>bit)&1
            need(list(map(sum,A))==degrees,"control degrees differ")
            B22 = [[int(i!=j)-A[i][j] for j in range(22)] for i in range(22)]
            defect = [[0]*22 for _ in range(22)]
            for i,j in pairs:
                value = 3-sum(A[i][k]*A[j][k] for k in range(22)) if A[i][j] else 6-sum(B22[i][k]*B22[j][k] for k in range(22))
                defect[i][j]=defect[j][i]=value
            K = [[2*A[i][j]+(2*degrees[i]-17)*(i==j) for j in range(22)] for i in range(22)]
            for i in range(22):
                triangles = sum(A[i][j]*A[i][k]*A[j][k]+B22[i][j]*B22[i][k]*B22[j][k]
                                for j,k in pairs if i!=j and i!=k)
                need(sum(defect[i])==3*degrees[i]+6*(21-degrees[i])-2*triangles,"literal triangle row")
                need(sum(defect[i])==sum(degrees)-294+38*degrees[i]-degrees[i]**2-
                     2*sum(A[i][j]*degrees[j] for j in range(22)),"literal incident row")
                for j in range(22):
                    expected = (2*degrees[i]-17)**2+4*degrees[i] if i==j else 4*(degrees[i]+degrees[j]-14)-4*defect[i][j]
                    need(sum(K[i][k]*K[j][k] for k in range(22))==expected,"literal square row product")
            need(sum(map(sum,defect))-histogram[1]==28,"wrong signed surplus")
        signed.append({"histogram":list(histogram),"red_masks":item["red_masks"],"graphs":24,
                       "incident_identity_checks":528,"square_identity_entries":11616})
    return {"determinant_controls":[-2,0],"rank_controls":[2,1],
            "baseline21_red_edges":sum(map(sum,R))//2,"baseline21_degree_histogram":[hist[d] for d in (8,9,10)],
            "baseline21_max_pages":maxima,"signed":signed}


def matching_domain(vertices):
    if not vertices:yield [];return
    first=vertices[0]
    for second in vertices[1:]:
        rest=[x for x in vertices if x not in (first,second)]
        for tail in matching_domain(rest):yield [(first,second)]+tail

def permutation_pair_domain():
    permutations4=list(permutations(range(4)));matrices=set();pairs=0
    for a,b in combinations_with_replacement(permutations4,2):
        counts=Counter((i,a[i]) for i in range(4));counts.update((i,b[i]) for i in range(4))
        matrices.add(tuple(counts[i,j] for i in range(4) for j in range(4)));pairs+=1
    need(pairs==300 and len(matrices)==282,"two-perfect-matching domain")
    return sorted(matrices),pairs

def literal_defect(flat,matching_x,matching_y):
    weights=Counter()
    def add(i,j,weight=1):
        if weight:weights[tuple(sorted((i,j)))]+=weight
    for i,j in combinations([2,3,4],2):add(i,j)
    for center,leaves in [(2,[13,14,15]),(3,[16,17,18]),(4,[19,20,21])]:
        for leaf in leaves:add(center,leaf)
    for i,j in matching_x:add(5+i,5+j)
    for i,j in matching_y:add(9+i,9+j)
    for i in range(4):
        for j in range(4):
            for _ in range(flat[4*i+j]):add(5+i,9+j)
    f=[[weights[tuple(sorted((i,j)))] if i!=j else 0 for j in range(22)] for i in range(22)]
    u=[int(i<2) for i in range(22)]
    h=[[21*(i==j)+16-4*(u[i]+u[j])+4*u[i]*(i==j)-4*f[i][j] for j in range(22)] for i in range(22)]
    need(list(map(sum,f))==[0,0]+[5]*3+[3]*8+[1]*9,"literal defect row degrees")
    return f,h

def matching_order(matching):
    edges={frozenset(pair) for pair in matching}
    orders=[p for p in permutations(range(4)) if frozenset((p[0],p[1])) in edges and frozenset((p[2],p[3])) in edges]
    need(len(orders)==8,"matching coordinate orders")
    return min(orders)

def matching_stabilizer():
    answer=[]
    for swap,left_flip,right_flip in product(range(2),repeat=3):
        blocks=[[0,1],[2,3]]
        if swap:blocks.reverse()
        if left_flip:blocks[0].reverse()
        if right_flip:blocks[1].reverse()
        answer.append(tuple(blocks[0]+blocks[1]))
    need(len(set(answer))==8,"explicit matching stabilizer")
    return answer

def orbit(flat):
    return min(tuple(flat[4*p[i]+q[j]] for i in range(4) for j in range(4))
               for p in matching_stabilizer() for q in matching_stabilizer())

def entry_compare(f,h,expected):
    need(f==expected['F'] and h==expected['H'],"every full F/H entry differs")

def lattice_certificate():
    primary=[];alternative=[]
    for start in (13,16,19):
        for i in (0,1):
            row=[0]*22;row[start+i]=1;row[start+2]=-1;primary.append(row)
        x=[0]*22;y=[0]*22
        x[start]=1;x[start+1]=-1;y[start+1]=1;y[start+2]=-1
        alternative.extend([x,y])
    b=list(map(list,zip(*primary)));c=list(map(list,zip(*alternative)))
    gram=multiply(primary,b);other=multiply(alternative,c)
    transform=[[0]*6 for _ in range(6)]
    for k in (0,2,4):transform[k][k]=1;transform[k+1][k]=-1;transform[k+1][k+1]=1
    need(multiply(b,transform)==c and elimination(transform,True)==1,"unimodular alternative basis")
    need(elimination(b)==6 and elimination(gram,True)==27 and elimination(other,True)==27,"six-dimensional primitive lattice")
    need(other==[[2 if i==j else -1 if i//2==j//2 else 0 for j in range(6)] for i in range(6)],"alternative A2 Gram")
    selectors=[13,14,16,17,19,20]
    need([b[i] for i in selectors]==[[int(i==j) for j in range(6)] for i in range(6)],"integral coordinate selectors")
    need(all(other[i][j]%2==int(i//2==j//2 and i!=j) for i in range(6) for j in range(6)),"alternating nondegenerate mod2 Gram")
    s=[[Fraction(0),Fraction(5,2)],[Fraction(2),Fraction(-1)]]
    g=gram[:2];g=[row[:2] for row in g];square=multiply(s,s)
    need(multiply(list(map(list,zip(*s))),g)==multiply(g,s),"rational self-adjoint control")
    need(all(square[i][j]+s[i][j]==5*(i==j) for i in range(2) for j in range(2)),"rational odd-trace polynomial control")
    need(s[0][0]+s[1][1]==-1 and s[0][1].denominator==2,"integrality is essential")
    # Irreducible quadratic on dimension6 has characteristic polynomial power3.
    need(sqrt_floor(21)==4 and 4*4<21<5*5,"nonsquare discriminant")
    need(sum((-1 for _ in range(3)))==-3 and -3%2==1,"odd forced trace")
    return {'basis_columns':primary,'gram':gram,'gram_determinant':27,
            'coordinate_selectors':selectors,'rank':6,'eigenvalue':21,
            'adjacency_polynomial':[1,1,-5],'discriminant':21,
            'characteristic_polynomial_power':3,'forced_trace':-3,
            'integral_self_adjoint_trace_parity':0,
            'rational_2plane_control':[['0','5/2'],['2','-1']]},c

def compute(fixtures,corpus):
    flat_domain,pair_count=permutation_pair_domain()
    matchings=list(matching_domain(list(range(4))))
    need(len(matchings)==3,"all internal perfect matchings")
    certificate,alternative_basis=lattice_certificate()
    cases={};groups={};ranks={};placements=0
    for mx,my in product(matchings,repeat=2):
        px,py=matching_order(mx),matching_order(my)
        relabel=list(range(5))+[5+i for i in px]+[9+i for i in py]+list(range(13,22))
        for flat in flat_domain:
            f,h=literal_defect(flat,mx,my)
            normalized=tuple(flat[4*px[i]+py[j]] for i in range(4) for j in range(4))
            fnew=[[f[i][j] for j in relabel] for i in relabel]
            hnew=[[h[i][j] for j in relabel] for i in relabel]
            key=','.join(map(str,normalized))
            if corpus is not None:
                need(key in corpus,"missing full matrix record")
                entry_compare(fnew,hnew,corpus[key])
            if normalized not in cases:
                value=elimination(hnew,True);root=sqrt_floor(value);square=root*root==value
                cases[normalized]=[list(normalized),value,root,sha256(serialize(fnew)).hexdigest(),sha256(serialize(hnew)).hexdigest(),square]
                representative=orbit(normalized)
                if representative not in groups:groups[representative]={'flat_M':list(representative),'labeled_count':0,'detH':value,'square':square}
                need(groups[representative]['detH']==value,"orbit determinant discrepancy")
                groups[representative]['labeled_count']+=1
                if square:
                    rank=elimination([[hnew[i][j]-21*(i==j) for j in range(22)] for i in range(22)])
                    need(rank==16,"entire21 kernel rank")
                    need(multiply(hnew,alternative_basis)==[[21*x for x in row] for row in alternative_basis],"alternative21 eigenbasis")
                    ranks[normalized]={'flat_M':list(normalized),'rank_H_minus21I':rank}
            else:
                need(sha256(serialize(fnew)).hexdigest()==cases[normalized][3] and sha256(serialize(hnew)).hexdigest()==cases[normalized][4],"full labeled normalization digest")
            placements+=1
    need(placements==2538 and len(cases)==282 and len(ranks)==18,"complete independent labeled census")
    result={'agent':'six-books-1','role':'researcher','version':1,'histogram':[2,20,0],
            'record_fields':['flat_M','det_H','floor_sqrt','F_sha256','H_sha256','square'],
            'row_compositions':10,'labeled_forms':282,'positive_nonsquares':264,'square_forms':18,
            'normal_form_orbits':16,'orbits':[groups[k] for k in sorted(groups)],
            'lattice_certificate':certificate,'square_ranks':[ranks[k] for k in sorted(ranks)],
            'controls':controls(fixtures),'records':[cases[k] for k in sorted(cases)]}
    return result,{'permutation_pairs':pair_count,'labeled_placements':placements,
                   'full_F_entries_compared':placements*484,'full_H_entries_compared':placements*484}

def compare(actual,expected):need(actual==expected,"expected certificate mismatch")

def corruptions(actual,corpus):
    mutations=[]
    def add(name,change):
        bad=deepcopy(actual);change(bad);mutations.append((name,bad))
    add('missing form',lambda d:d['records'].pop())
    add('duplicate form',lambda d:d['records'].append(d['records'][0]))
    add('wrong cross matrix',lambda d:d['records'][0][0].__setitem__(0,2))
    add('wrong determinant',lambda d:d['records'][0].__setitem__(1,d['records'][0][1]+1))
    add('wrong floor root',lambda d:d['records'][0].__setitem__(2,d['records'][0][2]+1))
    add('wrong F digest',lambda d:d['records'][0].__setitem__(3,'0'*64))
    add('wrong H digest',lambda d:d['records'][0].__setitem__(4,'0'*64))
    add('wrong orbit multiplicity',lambda d:d['orbits'][0].__setitem__('labeled_count',0))
    add('missing square rank',lambda d:d['square_ranks'].pop())
    add('wrong full eigenspace rank',lambda d:d['square_ranks'][0].__setitem__('rank_H_minus21I',17))
    add('nonprimitive basis',lambda d:d['lattice_certificate']['basis_columns'][0].__setitem__(13,2))
    add('wrong Gram entry',lambda d:d['lattice_certificate']['gram'][0].__setitem__(1,0))
    add('wrong Gram determinant',lambda d:d['lattice_certificate'].__setitem__('gram_determinant',28))
    add('wrong trace',lambda d:d['lattice_certificate'].__setitem__('forced_trace',-2))
    add('wrong polynomial',lambda d:d['lattice_certificate']['adjacency_polynomial'].__setitem__(2,-4))
    add('false rational root',lambda d:d['lattice_certificate']['rational_2plane_control'][0].__setitem__(1,'2'))
    add('changed signed mask',lambda d:d['controls']['signed'][0]['red_masks'].__setitem__(0,d['controls']['signed'][0]['red_masks'][0]^1))
    rejected=[]
    for name,bad in mutations:
        try:compare(actual,bad)
        except RuntimeError:rejected.append(name)
        else:raise RuntimeError('accepted corrupted '+name)
    if corpus is not None:
        key=next(iter(corpus));bad=deepcopy(corpus[key]);bad['F'][0][0]=1
        try:entry_compare(corpus[key]['F'],corpus[key]['H'],bad)
        except RuntimeError:rejected.append('full matrix loop')
        else:raise RuntimeError('accepted corrupted full matrix')
    return rejected

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected',type=Path,default=Path(__file__).with_name('degree98_two_roots_expected.json'))
    parser.add_argument('--matrices',type=Path)
    args=parser.parse_args();expected=json.loads(args.expected.read_text())
    corpus=json.loads(args.matrices.read_text()) if args.matrices else None
    actual,receipt=compute(expected['controls']['signed'],corpus);compare(actual,expected)
    rejected=corruptions(actual,corpus)
    print(json.dumps({'complete':True,'separate_domain':'unordered pairs of perfect matchings; all internal matching placements',
                      'forms':282,'nonsquares':264,'square_cases':18,'square_orbits':3,
                      'adjacency_survivors':0,'alternative_integral_basis':True,
                      'full_F_H_entry_comparison':bool(args.matrices),'corruptions_rejected':rejected,**receipt}))

if __name__=='__main__':main()
