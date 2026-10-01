"""Independent referee audit of the n=10 signed cap dual; no author code import."""
from fractions import Fraction as F
from itertools import combinations
from functools import lru_cache
from math import comb
from pathlib import Path
from hashlib import sha256
import json,re
from exact import require,determinant,inverse,leading,canonical

LAYERS=list(range(2,9))
ALLOWED=[(2,2),(2,3),(2,8),(3,7),(4,6),(5,5)]

def rational(s):
    require(type(s)is str and re.fullmatch(r'-?\d+(?:/[1-9]\d*)?',s),'rational string required')
    return F(s)

def transpose(a):return list(map(list,zip(*a)))
def trace_pair(a,b):return sum(a[i][j]*b[j][i] for i in range(len(a)) for j in range(len(a)))

def decode(c):
    require(all(type(c[k])is int and c[k]==v for k,v in [('n',10),('N',1013),('s',502)]),'claimed family parameters')
    require(c['layers']==LAYERS and all(type(x)is int for x in c['layers']),'layer order')
    require(c['cancelled_unordered_layer_pairs']==list(map(list,ALLOWED)),'support list')
    d=c['common_denominator'];require(type(d)is int and d>0,'positive exact denominator')
    nums=[c[k] for k in ['lower_numerator','upper_numerator']]
    for a in nums:
        require(type(a)is list and len(a)==7 and all(type(r)is list and len(r)==7 for r in a),'matrix dimensions')
        require(all(type(v)is int for r in a for v in r),'integer coefficients')
        require(a==transpose(a),'matrix symmetry')
    gamma=[[F(nums[0][i][j]-nums[1][i][j],d) for j in range(7)] for i in range(7)]
    require(all(gamma[k-2][l-2]==0 for k,l in ALLOWED),'allowed coefficient cancellation')
    beta=rational(c['weighted_mass_lower_bound'])
    require(rational(c['simple_strict_lower_bound'])==F(11,2500) and beta>F(11,2500),'positive strict bound')
    return nums,d,gamma,beta

@lru_cache(maxsize=1)
def geometry():
    universe=tuple(range(10))
    members=[frozenset(a) for k in range(9) for a in combinations(universe,k)]
    middle=[a for a in members if len(a)>=2];m=len(middle)
    require(len(members)==1013 and m==1002,'literal sizes')
    require([sum(i in a for a in members) for i in universe]==[502]*10,'literal stars')
    columns=[[len(a)-1]+[-int(i in a) for i in universe]+[int(j==h) for j in range(m)] for h,a in enumerate(middle)]
    # Columns are only used here for complete constant/star annihilation checks.
    checks=0
    for a,col in zip(middle,columns):
        require(sum(col)==0,'S constant annihilation');checks+=1
        for i in universe:
            require(sum(v for b,v in zip(members,col) if i in b)==0,'S star annihilation');checks+=1
    b=[sum(len(a)==k for a in middle) for k in LAYERS]
    require(b==[comb(10,k) for k in LAYERS],'literal layer cardinalities')
    # Literal S-images of the seven layer indicators.
    image=[]
    for k in LAYERS:
        layer=[a for a in middle if len(a)==k]
        image.append([sum(len(a)-1 for a in layer)]+[-sum(i in a for a in layer) for i in universe]+[int(len(a)==k) for a in middle])
    g=[[sum(x*y for x,y in zip(row,col)) for col in image] for row in image]
    formula=[[F(b[i] if i==j else 0)+F(k*l*b[i]*b[j],10)+(k-1)*(l-1)*b[i]*b[j] for j,l in enumerate(LAYERS)] for i,k in enumerate(LAYERS)]
    require(g==formula,'literal complete Gram')
    for a,col in zip(middle,columns):
        for j,img in enumerate(image):
            require(sum(x*y for x,y in zip(col,img))==g[len(a)-2][j]/F(b[len(a)-2]),'G preserves layer constants')
    gi=inverse(g);w=[[b[i]*b[j]*gi[i][j] for j in range(7)] for i in range(7)]
    leading(g);leading(w)
    # Separate rank-two Woodbury reconstruction, with a 2x2 cofactor inverse.
    f=[[k,k-1] for k in LAYERS]
    h=[[F(10 if i==j==0 else int(i==j))+sum(b[t]*f[t][i]*f[t][j] for t in range(7)) for j in range(2)] for i in range(2)]
    hi=inverse(h)
    wood=[[F(b[i] if i==j else 0)-b[i]*b[j]*sum(f[i][u]*hi[u][v]*f[j][v] for u in range(2) for v in range(2)) for j in range(7)] for i in range(7)]
    require(w==wood,'cofactor/low-rank inverse agreement')
    return members,middle,b,g,w,h,checks

def nonuniform_fixture(members,middle,b,gamma,x,y,w,beta):
    m=len(middle);q=[[-1]*m for _ in range(m)];aggregate=[[0]*7 for _ in range(7)]
    histogram={};cancelled=0;mass=F(0)
    for i,a in enumerate(middle):
        q[i][i]=501
        for j in range(i+1,m):
            other=middle[j]
            if a.isdisjoint(other):
                sa=sum(v+1 for v in a);sb=sum(v+1 for v in other)
                value=((sa+sb)*5+sa*sb+len(a)*len(other))%23-11
                q[i][j]+=value;q[j][i]+=value
                k,l=len(a),len(other);pair=(k,l)
                histogram[pair]=histogram.get(pair,0)+1
                aggregate[k-2][l-2]+=value;aggregate[l-2][k-2]+=value
                mass+=2*gamma[k-2][l-2]*value
                if pair in ALLOWED:
                    require(gamma[k-2][l-2]==0,'individual edge cancellation');cancelled+=1
    expected={(k,l):comb(10,k)*comb(10-k,l)//(2 if k==l else 1) for k in LAYERS for l in LAYERS if k<=l and k+l<=10}
    require(histogram==expected,'all literal orbit counts')
    c=[[F(502*b[i] if i==j else 0)-b[i]*b[j]+aggregate[i][j] for j in range(7)] for i in range(7)]
    u=[[1013*w[i][j]-c[i][j] for j in range(7)] for i in range(7)]
    require(trace_pair(x,c)+trace_pair(y,u)+beta==mass,'unsymmetrized ordered trace identity')
    require(mass!=0 and trace_pair(x,c)+trace_pair(y,u)+beta!=mass/2,'ordered factor two')
    # Complete affine forced-face lift, all entries regenerated as integers.
    small_middle=[]
    small_middle.append([sum((len(middle[h])-1)*q[h][j] for h in range(m)) for j in range(m)])
    for point in range(10):
        small_middle.append([-sum(q[h][j] for h,a in enumerate(middle) if point in a) for j in range(m)])
    small=[[0]*11 for _ in range(11)]
    weights=[[len(a)-1 for a in middle]]+[[-int(i in a) for a in middle] for i in range(10)]
    for i in range(11):
        for j in range(11):small[i][j]=sum(small_middle[i][h]*weights[j][h] for h in range(m))
    matrix_hash=sha256();entry_checks=0;row_checks=0;star_checks=0;min_entry=None;max_entry=None
    for i,a in enumerate(members):
        if i<11:row=[1+v for v in small[i]]+[1+v for v in small_middle[i]]
        else:row=[1+small_middle[j][i-11] for j in range(11)]+[1+v for v in q[i-11]]
        require(sum(row)==1013,'complete affine row');row_checks+=1
        for point in range(10):
            require(sum(v for other,v in zip(members,row) if point in other)==502,'complete affine star equation');star_checks+=1
        for j,(other,v) in enumerate(zip(members,row)):
            require(type(v)is int,'integer lifted entry')
            if a and i==j:require(v==502,'nonempty diagonal')
            elif not a.isdisjoint(other):require(v==0,'intersection support')
            reflected=1+(small[j][i] if i<11 and j<11 else small_middle[i][j-11] if i<11 else small_middle[j][i-11] if j<11 else q[j-11][i-11])
            require(v==reflected,'complete affine symmetry')
            entry_checks+=1
        matrix_hash.update(canonical(row));lo,hi=min(row),max(row)
        min_entry=lo if min_entry is None else min(min_entry,lo);max_entry=hi if max_entry is None else max(max_entry,hi)
    require(entry_checks==1013**2 and star_checks==10130,'complete coverage')
    return {'unordered_disjoint_middle_pairs':sum(histogram.values()),'allowed_individual_pairs_cancelled':cancelled,'orbits':[{'sizes':list(k),'unordered_pairs':v} for k,v in sorted(histogram.items())],'synthetic_signed_mass':str(mass),'synthetic_is_only_affine_not_PSD':True,'affine_entry_checks':entry_checks,'affine_row_checks':row_checks,'affine_star_checks':star_checks,'affine_matrix_sha256':matrix_hash.hexdigest(),'affine_min_max':[min_entry,max_entry]}

def audit(c,literal=True):
    nums,d,gamma,beta=decode(c);minors=[];all_counts=[]
    for a in nums:
        minors.append([int(v) for v in leading(a)]);count=0
        for k in range(1,8):
            for ix in combinations(range(7),k):
                require(determinant([[a[i][j] for j in ix] for i in ix])>0,'positive principal minor');count+=1
        all_counts.append(count)
    members,middle,b,g,w,h,annihilations=geometry()
    x,y=[[[F(v,d) for v in row] for row in a] for a in nums]
    constant=1013*trace_pair(y,w)+502*sum(gamma[i][i]*b[i] for i in range(7))-sum(gamma[i][j]*b[i]*b[j] for i in range(7) for j in range(7))
    require(constant==-beta,'dual scalar')
    tau=trace_pair(y,w);require(tau>0,'relaxed-cap trace coefficient')
    cap_gap=beta/(511*tau)
    require(cap_gap==F(673166951899,35033660507720) and F(19,1000)<cap_gap<F(1,50),'quantitative ordinary-H cap gap')
    g24=gamma[0][2];require(g24>0,'added2/4 sign')
    mean=beta/(6300*g24);require(mean==F(51782073223,946576514520),'sole2/4 necessary bound')
    candidates=[(abs(gamma[k-2][l-2]),(k,l)) for k in LAYERS for l in LAYERS if k<=l and k+l<=10 and (k,l) not in ALLOWED]
    gmax,pair=max(candidates)
    extra_l1=beta/(2*511*gmax)
    result={'agent':'six-reviewer-5','role':'independent mathematical reviewer','n':10,'N':1013,'s':502,'certificate_canonical_sha256':sha256(canonical(c)).hexdigest(),'dual_ranks':[7,7],'leading_minors':minors,'all_principal_minors_checked':all_counts,'constant':str(constant),'weighted_mass_lower_bound':str(beta),'tau_trace_YW':str(tau),'ordinary_H_top_eigenvalue_strict_floor':str(1+cap_gap),'ordinary_H_cap_gap_strict_floor':str(cap_gap),'ordinary_H_L_upper_surplus_strict_floor':str(beta/tau),'sole_two_four_mean_strict_floor':str(mean),'max_extra_coefficient':str(gmax),'max_extra_coefficient_sizes':list(pair),'extra_unordered_abs_M_mass_strict_floor':str(extra_l1),'literal_geometry':{'members':len(members),'middle':len(middle),'layer_counts':b,'Gram_entries':49,'S_annihilations':annihilations,'G_layer_invariance_coordinates':len(middle)*7,'Woodbury_2x2':[[int(v) for v in row] for row in h]},'extra_coefficients':[{'sizes':[k,l],'coefficient':str(gamma[k-2][l-2])} for k in LAYERS for l in LAYERS if k<=l and k+l<=10 and (k,l) not in ALLOWED]}
    if literal:result['literal_fixture']=nonuniform_fixture(members,middle,b,gamma,x,y,w,beta)
    return result

def compare_author(result,original):
    require(result['leading_minors']==[original['lower_leading_principal_minors'],original['upper_leading_principal_minors']],'author leading minor comparison')
    require(result['constant']==original['constant'] and result['weighted_mass_lower_bound']==original['weighted_mass_lower_bound'],'author bound comparison')
    require(result['all_principal_minors_checked']==original['all_principal_minors_checked'],'author principal minor coverage')
    require(result['extra_coefficients']==original['additional_disjoint_layer_pairs'],'all extra coefficients')
    require(result['literal_geometry']['Woodbury_2x2']==original['Woodbury_2x2'],'author rank-two geometry')
    require(result['literal_fixture']['orbits']==original['literal_controls']['disjoint_orbits'],'all author orbit counts')
    require(result['literal_fixture']['allowed_individual_pairs_cancelled']==original['literal_controls']['individual_allowed_pairs_cancelled'],'all author cancellation counts')
    return {'leading_minors':14,'extra_coefficients':10,'orbit_counts':16,'bound_and_geometry_match':True,'author_code_imported':False}
