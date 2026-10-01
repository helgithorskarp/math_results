#!/usr/bin/env python3
"""six-reviewer-3: independently rebuild the entire 97-edge boundary obstruction."""
import argparse
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, combinations_with_replacement, permutations, product
from math import isqrt
from pathlib import Path
import hashlib
import json


class Failure(Exception):
    pass


def need(ok, message):
    if not ok:
        raise Failure(message)


def encoded(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':')).encode()


def determinant(matrix):
    n = len(matrix)
    need(all(len(row) == n for row in matrix), 'determinant square shape')
    a = [[Q(x) for x in row] for row in matrix]
    value = Q(1)
    for k in range(n):
        p = next((i for i in range(k,n) if a[i][k]), None)
        if p is None:
            return 0
        if p != k:
            a[p],a[k] = a[k],a[p]
            value = -value
        pivot = a[k][k]
        value *= pivot
        for i in range(k+1,n):
            ratio = a[i][k]/pivot
            for j in range(k+1,n):
                a[i][j] -= ratio*a[k][j]
    need(value.denominator == 1, 'integral determinant')
    return int(value)


def rank(matrix):
    a = [[Q(x) for x in row] for row in matrix]
    if not a:
        return 0
    top = 0
    for k in range(len(a[0])):
        p = next((i for i in range(top,len(a)) if a[i][k]), None)
        if p is None:
            continue
        a[p],a[top] = a[top],a[p]
        t = a[top][k]
        a[top] = [x/t for x in a[top]]
        for i in range(top+1,len(a)):
            c = a[i][k]
            if c:
                a[i] = [x-c*y for x,y in zip(a[i],a[top])]
        top += 1
        if top == len(a):
            break
    return top


def shifted(H, eigenvalue):
    return [[x-eigenvalue*int(i==j) for j,x in enumerate(row)] for i,row in enumerate(H)]


def forced(degrees,F):
    need(len(degrees)==22 and len(F)==22 and all(len(row)==22 for row in F), 'forced shape')
    need(all(F[i][j]==F[j][i] for i in range(22) for j in range(22)), 'defect symmetry')
    need(all(F[i][i]==0 for i in range(22)), 'defect loops')
    # Low-rank degree correction, independently compared to the literal entries.
    H = [[25*int(i==j)+4*(degrees[i]+degrees[j]-14)
          +4*((10-degrees[i])**2-2*(10-degrees[i]))*int(i==j)-4*F[i][j]
          for j in range(22)] for i in range(22)]
    need(all(H[i][j] == ((2*degrees[i]-17)**2+4*degrees[i] if i==j
                        else 4*(degrees[i]+degrees[j]-14)-4*F[i][j])
             for i in range(22) for j in range(22)), 'two independent H entry formulas')
    return H


def reverse_classes(histogram):
    degrees = [d for d,count in zip((8,9,10),histogram) for _ in range(count)]
    need(len(degrees)==22, 'histogram order')
    pools = {d:[i for i,x in enumerate(degrees) if x==d][::-1] for d in (8,9,10)}
    permutation = [0]*22
    for d in pools:
        ordinary = pools[d][::-1]
        for i,j in zip(ordinary,pools[d]):
            permutation[i] = j
    return degrees,pools,permutation


def make_defect(histogram,profile,weights):
    degrees,pools,permutation = reverse_classes(histogram)
    centers = [pools[d].pop(0) for d,q in profile]
    demand = [q+d%2 for d,q in profile]
    F = [[0]*22 for _ in range(22)]
    for (i,j),w in zip(combinations(range(len(profile)),2),weights):
        F[centers[i]][centers[j]]=F[centers[j]][centers[i]]=w
        demand[i]-=w;demand[j]-=w
    need(min(demand,default=0)>=0 and sum(demand)<=len(pools[9]), 'normal-form leaf budgets')
    for c,l in zip(centers,demand):
        for _ in range(l):
            b=pools[9].pop(0);F[c][b]=F[b][c]=1
    need(len(pools[9])%2==0, 'normal-form odd remainder')
    for i,j in zip(pools[9][::2],pools[9][1::2]):
        F[i][j]=F[j][i]=1
    expected=[d%2 for d in degrees]
    for c,(d,q) in zip(centers,profile):
        expected[c]+=q
    need(list(map(sum,F))==expected, 'all defect row demands')
    H=forced(degrees,F)
    # The author uses increasing labels; this explicit degree-preserving
    # conjugation is for a subsequent optional comparison, not domain selection.
    canonical_F=[[F[i][j] for j in permutation] for i in permutation]
    canonical_H=[[H[i][j] for j in permutation] for i in permutation]
    return degrees,F,H,hashlib.sha256(encoded([canonical_F,canonical_H])).hexdigest()


def forms(histogram, surplus):
    colors=[d for d,c in zip((8,9,10),histogram) if c]
    types=[(d,q) for d in colors for q in range(2,surplus+1,2)]
    records=[]
    profile_counts=Counter()
    labeled_counts=Counter()
    for k in range(1,surplus//2+1):
        for profile in combinations_with_replacement(types,k):
            if sum(q for d,q in profile)!=surplus:
                continue
            if any(sum(d==color for d,q in profile)>histogram[color-8] for color in colors):
                continue
            pairs=list(combinations(range(k),2));edge_index={pair:i for i,pair in enumerate(pairs)}
            demand=[q+d%2 for d,q in profile]
            allowed_permutations=[p for p in permutations(range(k)) if tuple(profile[i] for i in p)==profile]
            seen=set()
            # Flat Cartesian products, followed by global row-demand filtering,
            # rather than the author's row-budget recursion.
            for weights in product(*(range(min(demand[i],demand[j])+1) for i,j in pairs)):
                loads=[0]*k
                for (i,j),w in zip(pairs,weights):
                    loads[i]+=w;loads[j]+=w
                leaves=[d-l for d,l in zip(demand,loads)]
                available=histogram[1]-sum(d==9 for d,q in profile)
                if min(leaves,default=0)<0 or sum(leaves)>available or (available-sum(leaves))%2:
                    continue
                labeled_counts[k]+=1
                orbit={tuple(weights[edge_index[tuple(sorted((p[i],p[j])))]] for i,j in pairs)
                       for p in allowed_permutations}
                canonical=min(orbit)
                if canonical in seen:
                    continue
                seen.add(canonical)
                degrees,F,H,digest=make_defect(histogram,profile,canonical)
                value=determinant(H)
                need(value>0, 'positive forced determinant')
                root=isqrt(value)
                records.append({'profile':profile,'weights':canonical,'orbit_size':len(orbit),
                                'det':value,'root':root,'canonical_F_H_sha256':digest})
            if seen:
                profile_counts[k]+=1
    return records,profile_counts,labeled_counts


def simple_four():
    cases=[]
    degrees=[8]*4+[9]*18
    # An independently labeled cycle and descending degree-nine vertices.
    b=list(range(21,3,-1));centers=b[:2];normal=b[2:]
    for w in range(4):
        l,p=3-w,5+w
        F=[[0]*22 for _ in range(22)]
        for i,j in ((0,1),(1,2),(2,3),(3,0)):
            F[i][j]=F[j][i]=1
        c,d=centers;F[c][d]=F[d][c]=w
        left,right=normal[:l],normal[l:2*l]
        for center,leaves in ((c,left),(d,right)):
            for leaf in leaves:F[center][leaf]=F[leaf][center]=1
        remaining=normal[2*l:]
        for i,j in zip(remaining[::2],remaining[1::2]):F[i][j]=F[j][i]=1
        H=forced(degrees,F)
        need(sorted(map(sum,F))==[1]*16+[2]*4+[3]*2,'four-case full row demands')
        cells=[list(range(4)),centers]+([left+right] if l else [])+[remaining]
        quotient=[[sum(H[i][j] for j in cell) for cell in cells] for i in [cell[0] for cell in cells]]
        need(all([sum(H[i][j] for j in cell) for cell in cells]==quotient[k]
                 for k,C in enumerate(cells) for i in C),'every literal equitable quotient row')
        expected=([[49,24,24*l,24*p],[48,53-4*w,28*l,32*p],
                   [48,28,21+32*l,32*p],[48,32,32*l,17+32*p]]
                  if l else [[49,24,24*p],[48,53-4*w,32*p],[48,32,17+32*p]])
        need(quotient==expected,'explicit small quotient')
        eigenvalue=33 if l else 17
        nullity=22-rank(shifted(H,eigenvalue))
        need(nullity==(1 if l else 7),'independent full rank verifies odd eigenspace')
        basis=[]
        if l:
            basis=[[1,-1,1,-1]+[0]*18]
        else:
            pairs=list(zip(remaining[::2],remaining[1::2]))
            for pair in pairs[:-1]:
                v=[0]*22
                for i in pair:v[i]=1
                for i in pairs[-1]:v[i]=-1
                basis.append(v)
        need(rank(basis)==nullity,'complete explicit rational eigenspace basis')
        need(all(all(sum(x*y for x,y in zip(row,v))==eigenvalue*v[i] for i,row in enumerate(H))
                 for v in basis),'literal eigenvector actions')
        value=determinant(H);qd=determinant(quotient)
        factored=(33*25**(p+2)*17**(p-1)*21**(2*l-2)*(393+100*w)*qd
                  if l else 33**2*25**(p+2)*17**(p-1)*qd)
        need(value==factored and isqrt(value)**2!=value,'small quotient/full determinant crosscheck')
        qshift=determinant(shifted(quotient,eigenvalue))
        need(qshift==(-577536-364544*w if l else 8192),'small collision exclusions')
        if l:
            need(determinant([[21+4*w-33,-4*l],[-4,21-33]])==32*l,'odd center/leaf block collision')
        modulus=13 if w==0 else 23
        need(value%modulus not in {i*i%modulus for i in range(modulus)},'original modular obstruction')
        # Map our cycle to the author's cycle; B labels are reversed.
        permutation=[0,2,1,3]+b
        canonF=[[F[i][j] for j in permutation] for i in permutation]
        canonH=[[H[i][j] for j in permutation] for i in permutation]
        cases.append({'w':w,'l':l,'p':p,'eigenvalue':eigenvalue,'odd_multiplicity':nullity,
                      'quotient':quotient,'quotient_det':qd,'quotient_shift_det':qshift,
                      'det':value,'canonical_F':canonF,'canonical_H':canonH})
    return cases


def exceptional(record):
    degrees,F,H,digest=make_defect((5,16,1),record['profile'],record['weights'])
    pairs=[(i,j) for i,j in combinations(range(5),2) if F[i][j]==2]
    need(len(pairs)==2 and len(set(sum(([i,j] for i,j in pairs),[])))==4,'exceptional disjoint doubled edges')
    basis=[]
    for i,j in pairs:
        v=[0]*22;v[i]=1;v[j]=-1;basis.append(v)
    need(rank(basis)==2 and 22-rank(shifted(H,33))==2,'entire exceptional33 plane')
    need(all(all(sum(x*y for x,y in zip(row,v))==33*v[i] for i,row in enumerate(H)) for v in basis),
         'literal exceptional eigenspace action')
    need([[sum(x*y for x,y in zip(u,v)) for v in basis] for u in basis]==[[2,0],[0,2]],'equal plane Gram')
    need(not [(a,b,c) for a,b,c in product(range(9),repeat=3)
              if (a*a+b*b-33*c*c)%9==0 and any(x%3 for x in (a,b,c))],'norm primitive mod9 rejection')
    return {'eigenvalue':33,'multiplicity':2,'Gram':[[2,0],[0,2]],'primitive_mod9_solutions':0,
            'adjacency_restriction_possible_traces':[-6,-4,-2]}


def zero_surplus():
    degrees,F,H,digest=make_defect((7,12,3),(),())
    Q3=[[81,144,48],[84,209,60],[112,240,97]]
    groups=[list(range(7)),list(range(7,19)),list(range(19,22))]
    need(all([sum(H[i][j] for j in group) for group in groups]==Q3[k]
             for k,C in enumerate(groups) for i in C),'zero-surplus constant quotient')
    need(determinant(shifted(Q3,17))==-3072,'zero-surplus quotient excludes17')
    need(22-rank(shifted(H,17))==5,'zero-surplus odd17 multiplicity')
    return {'histogram':[7,12,3],'eigenvalue':17,'odd_multiplicity':5,'quotient':Q3,
            'quotient_shift_det':-3072}


def local_checks():
    pairs=list(combinations(range(4),2));graphs=Counter()
    for bits in product((0,1),repeat=6):
        degrees=[sum(bits[k] for k,pair in enumerate(pairs) if i in pair) for i in range(4)]
        if min(degrees)>=2:graphs[sum(bits)]+=1
    need(dict(graphs)=={4:3,5:6,6:1},'all four-vertex cases')
    sets=[set(i for i in range(4) if mask>>i&1) for mask in range(1,16)]
    c4=[s for s in sets if not ({0,2}<=s or {1,3}<=s)]
    kh=[s for s in sets if not {0,1}<=s]
    need(len(c4)==8 and max(map(len,c4))==2,'cycle neighbor sets')
    need(len(kh)==11 and all(len(s&{0,1})*len(s&{2,3})<=len(s)-1 for s in kh),'K4-e mixed-pair bound')
    families=[(s,) for s in sets if len(s)==3]
    families+=list(combinations_with_replacement([s for s in sets if len(s)==2],2))
    survivors=[]
    for family in families:
        F=[[0 if i==j else 1-sum(i in s and j in s for s in family) for j in range(4)] for i in range(4)]
        if min(x for row in F for x in row)>=0 and max(map(sum,F))<=2:
            survivors.append(family);need(len(family)==2 and not family[0]&family[1],'disjoint-pair survivor')
    need(len(families)==25 and len(survivors)==3,'all local exceptional patterns')
    # Elementary minimum-degree capacity values; no spectral classification.
    blue_bounds=[]
    for d in range(15,22):
        q=21-d;r,s=6,3
        score=max((3*d+r-s-4-q)*h-3*h*h for h in range(r+1))
        bound=d*score+(s-d+2)*d*(d-1)+q*r*(r+1)
        need(bound<0,'blue high-degree capacity rejection');blue_bounds.append(bound)
    score14=[34*h-3*h*h for h in range(7)]
    need(score14==[0,31,56,75,88,95,96] and 14*max(score14)==1344,'degree-seven tight scores')
    histograms=[]
    for a,b,c in product(range(23),repeat=3):
        if a+b+c==22 and 8*a+9*b+10*c==194 and 3*(4*a+b)+b<=132:
            histograms.append([a,b,c])
    need(histograms==[[4,18,0],[5,16,1],[6,14,2],[7,12,3]],'all97 endpoint histograms')
    return {'four_vertex_graph_counts':dict(graphs),'C4_subsets':len(c4),'K4_minus_edge_subsets':len(kh),
            'exceptional_patterns':len(families),'disjoint_survivors':len(survivors),
            'blue_capacity_bounds_d15_to21':blue_bounds,'degree7_scores':score14,'all97_histograms':histograms}


def algebra_controls():
    # Literal pages for fixed unrelated graph families, allowing signed F.
    count=0
    for family in range(12):
        red=[[int(i!=j and ((i*j+3*i+3*j+family)%11 < family%10)) for j in range(22)] for i in range(22)]
        degrees=list(map(sum,red));blue=[[int(i!=j)-red[i][j] for j in range(22)] for i in range(22)]
        F=[[0 if i==j else (3-sum(red[i][k]*red[j][k] for k in range(22)) if red[i][j]
                           else 6-sum(blue[i][k]*blue[j][k] for k in range(22))) for j in range(22)] for i in range(22)]
        H=forced(degrees,F)
        K=[[2*red[i][j]+(2*degrees[i]-17)*int(i==j) for j in range(22)] for i in range(22)]
        need([[sum(K[i][k]*K[k][j] for k in range(22)) for j in range(22)] for i in range(22)]==H,'literal signed square controls')
        edges=sum(degrees)//2
        need(sum(map(sum,F))==132-3*sum((d-10)**2 for d in degrees),'signed defect sum')
        need(all(sum(F[i])==2*edges-294+38*d-d*d-2*sum(degrees[j] for j in range(22) if red[i][j])
                 and (sum(F[i])-d)%2==0 for i,d in enumerate(degrees)),'literal incident/parity controls')
        count+=1
    return count


def reject(call):
    try:call()
    except Failure:return
    raise Failure('negative control was accepted')


def audit_original(folder,records,four):
    data=json.loads((folder/'slack8_expected.json').read_text())
    expected={}
    for pi,weights,orbit,d,r,digest in data['records']:
        profile=tuple(tuple(x) for x in data['profiles'][pi]['types'])
        expected[(profile,tuple(weights))]=(orbit,d,r,digest)
    own={(tuple(x['profile']),tuple(x['weights'])):(x['orbit_size'],x['det'],x['root'],x['canonical_F_H_sha256'])
         for x in records}
    need(own==expected,'all original559 records/domain/full matrix hashes independently match')
    source=json.loads((folder/'degree97_expected.json').read_text())
    for own,original in zip(four,source['cases']):
        need(own['w']==original['center_weight'] and own['det']==original['det_H']
             and own['canonical_F']==original['F'] and own['canonical_H']==original['H'],
             'all four original matrices match after explicit independent relabeling')
    return {'original559_records_exact':True,'four_original_F_H_entry_comparisons':4*2*484}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',type=Path);parser.add_argument('--check',type=Path)
    parser.add_argument('--audit-original',type=Path)
    args=parser.parse_args()
    six,pc6,lc6=forms((6,14,2),4);five,pc5,lc5=forms((5,16,1),8)
    need(len(six)==22 and all(x['root']**2!=x['det'] for x in six),'all slack-four22 nonsquares')
    need(len(five)==559,'entire slack-eight559 domain')
    squares=[x for x in five if x['root']**2==x['det']]
    need(len(squares)==1 and sum(x['root']**2!=x['det'] for x in five)==558,'sole square survivor')
    four=simple_four();exception=exceptional(squares[0])
    controls=[('singular determinant',lambda:need(determinant([[1,2],[2,4]])!=0,'false nonsingularity')),
              ('wrong square shape',lambda:determinant([[1,2]])),
              ('missing559 case',lambda:need(len(five[:-1])==559,'incomplete case list')),
              ('false odd multiplicity',lambda:need(four[3]['odd_multiplicity']==6,'wrong spectral multiplicity')),
              ('false norm solution',lambda:need((1+4*4)==33,'bad norm equation'))]
    for name,call in controls:reject(call)
    result={'agent':'six-reviewer-3','role':'independent mathematical reviewer','arithmetic':'stdlib int/Fraction',
            'scope':'Complete97 boundary; original global degree8..10/upper110 reused separately.',
            'local':local_checks(),'signed_graph_controls':algebra_controls(),
            'slack_four':{'histogram':[6,14,2],'forms':len(six),'all_nonsquare':True,
                          'profiles_by_center_count':dict(pc6),'labeled_cores_by_center_count':dict(lc6),
                          'record_stream_sha256':hashlib.sha256(encoded(six)).hexdigest()},
            'slack_eight':{'histogram':[5,16,1],'forms':len(five),'nonsquares':558,'squares':1,
                           'profiles_by_center_count':dict(pc5),'labeled_cores_by_center_count':dict(lc5),
                           'record_stream_sha256':hashlib.sha256(encoded(five)).hexdigest(),
                           'square_survivor':squares[0],'exceptional_plane':exception},
            'zero_surplus':zero_surplus(),
            'four_cases':[{k:v for k,v in x.items() if k not in ('canonical_F','canonical_H')} for x in four],
            'negative_controls_rejected':[name for name,call in controls]}
    if args.audit_original:
        print(json.dumps(audit_original(args.audit_original,five,four),sort_keys=True))
    output=json.dumps(result,sort_keys=True,indent=2)+'\n'
    if args.write:args.write.write_text(output)
    if args.check:need(json.loads(args.check.read_text())==json.loads(output),'expected summary mismatch')
    print(json.dumps({'verified':True,'agent':'six-reviewer-3','forms':[len(six),len(five),len(four)],
                      'result_sha256':hashlib.sha256(output.encode()).hexdigest()},sort_keys=True))


if __name__=='__main__':
    main()
