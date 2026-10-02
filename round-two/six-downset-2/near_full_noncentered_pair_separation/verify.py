"""Portable exact replay, six-downset-2, researcher; no solver/proposal input.

The finite certificate is checked on the full star-only affine face. Universal
real/PSD/averaging bridges are the ordinary proof in PROOF.md, not a finite
rational enumeration. Same-author independent algorithms are not peer review.
"""
import argparse
import copy
from fractions import Fraction as Q
import hashlib
from itertools import product
import json
from math import comb, isqrt
from pathlib import Path
import re
from affine import direct, rref, supported_pairs
from exact import both
from model import (choose, complete, defect, physical, reduced_physical,
                   root_reduction, direct_schur, lower_energy_budget,
                   parameters, require)

HERE = Path(__file__).resolve().parent


def encode(x):
    if type(x) is Q:
        return str(x)
    if isinstance(x, dict):
        return {str(k): encode(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [encode(v) for v in x]
    return x


def canonical(x):
    return json.dumps(encode(x), sort_keys=True, separators=(',', ':')).encode()+b'\n'


def digest(x):
    return hashlib.sha256(canonical(x)).hexdigest()


def rational(x):
    require(type(x) is str and re.fullmatch(r'-?\d+(?:/[1-9]\d*)?', x) is not None,
            'Rational string input only')
    return Q(x)


def decode(data):
    require(data['agent'] == 'six-downset-2' and data['role'] == 'researcher', 'Author metadata')
    require(type(data['n']) is int and data['n'] == 16 and data['scale_s'] == 32752,
            'Fixed original n16 scale')
    require(data['normalization'] == 'A_ik=F_ik/(s*r_i*r_k), r_i=isqrt(g_i)>0',
            'Exact physical congruence convention')
    modes = [(j, upper) for upper in (False, True) for j in range(3)]
    require(len(data['forms']) == len(modes), 'Six physical duals')
    blocks = []
    for f, (j, upper) in zip(data['forms'], modes):
        aa = list(range(1 if upper and j <= 1 else 2, 15))
        require(type(f['degree']) is int and f['degree'] == j and
                type(f['upper']) is bool and f['upper'] == upper and f['layers'] == aa,
                'Original layer and mode labels')
        triangle = f['triangle']; d = len(aa)
        require(len(triangle) == d and all(len(row) == d-i for i, row in enumerate(triangle)),
                'Exact upper triangle dimensions')
        Y = [[Q(0) for _ in aa] for _ in aa]
        for i, row in enumerate(triangle):
            for k, value in enumerate(row, i):
                Y[i][k] = Y[k][i] = rational(value)
        blocks.append((j, upper, aa, Y))
    lam = rational(data['degree_three_multiplier'])
    require(lam > 0, 'Positive degree-three rank-one weight')
    require(data['ranks'] == [13, 13, 13, 14, 14, 13], 'Claimed exact dual ranks')
    require(data['original_unordered_count'] == 18942222, 'Original unordered pair count')
    require(rational(data['eta_lower']) == Q(1, 2**21) and
            rational(data['original_weight_upper']) == Q(1, 2**15), 'Strict rational thresholds')
    rational(data['negative_constant'])
    return blocks, lam


def functional(B, blocks, lam):
    n = 16; s = parameters(n)[1]; value = Q(0)
    for j, upper, expected_aa, Y in blocks:
        aa, g, F = reduced_physical(n, B, j, upper)
        require(aa == expected_aa, 'Displayed physical layer agreement')
        rr = [isqrt(g[a]) for a in aa]
        require(all(r > 0 for r in rr), 'Positive rational congruence')
        value += sum(Y[i][k]*F[k][i]/(s*rr[i]*rr[k])
                     for i in range(len(aa)) for k in range(len(aa)))
    aa, g, F = physical(n, B, 3)
    ids = [aa.index(3), aa.index(13)]
    require(g[3] == g[13] == 1, 'Degree-three endpoint physical metric')
    value += lam*sum(F[i][k] for i in ids for k in ids)/2
    return value


def finite_certificate(data):
    blocks, lam = decode(data)
    ranks = [both(Y, len(aa)) for j, upper, aa, Y in blocks]
    pairs, recover = rref(16)
    base = [Q(32751) if a+b == 16 else Q(0) for a, b in pairs]
    B = direct(16, base)
    require(B == recover(base), 'Independent base completion')
    require(all(B[1][a] == 1 for a in range(2, 15)) and B[1][1] == 16370,
            'Explicit star-only base')
    constant = functional(B, blocks, lam)
    require(constant == rational(data['negative_constant']), 'Exact claimed constant')
    eta = -constant
    require(eta > Q(1, 2**21), 'Strict eta margin')
    omitted = []; canceled = []
    for i, (a, b) in enumerate(pairs):
        values = base.copy(); values[i] += 1
        direction = direct(16, values)
        require(direction == recover(values), 'Independent full affine direction')
        d = functional(direction, blocks, lam)-constant
        if a+b == 16 or a == 2:
            require(d == 0, 'Every S2 free coordinate canceled')
            canceled.append([a, b])
        else:
            require(a >= 3 and a+b < 16 and d > 0, 'Positive omitted coefficient')
            ordered = comb(16, a)*comb(16-a, b)
            k = ordered//(2 if a == b else 1)
            require(k*(2 if a == b else 1) == ordered, 'Unordered diagonal factor')
            alpha = Q(32767)*d/k
            require(0 < alpha < Q(1, 2**15), 'Strict original mass weight')
            omitted.append({'sizes': [a, b], 'coefficient_beta': d,
                            'original_unordered_pairs': k, 'weight_M': alpha})
    require(len(pairs) == 49 and len(canceled) == 19 and len(omitted) == 30,
            'Entire full star-only face partition')
    count = sum(x['original_unordered_pairs'] for x in omitted)
    ordered_ie = (3**16-2**16-2*sum(comb(16,a)*(2**(16-a)-1) for a in range(3))
                  +sum(comb(16,a)*comb(16-a,b) for a in range(3) for b in range(3)))
    require(ordered_ie == 2*count and count == data['original_unordered_count'] and count < 2**25,
            'Independent ternary assignment count')
    require(eta/Q(1,2**15) > Q(1,64) and Q(1,64)/count > Q(1,2**31),
            'Original positive mass and individual entry consequences')
    return {'n': 16, 'N': 65519, 's': 32752, 'h': 32767,
            'supported_coordinates': len(supported_pairs(16)), 'star_equation_rank': 14,
            'free_coordinates': len(pairs), 'dual_ranks_both_algorithms': ranks,
            'degree_three_multiplier': lam, 'negative_constant': constant, 'eta': eta,
            'canceled_S2_coordinates': canceled, 'omitted_positive_coefficients': omitted,
            'original_unordered_count': count, 'independent_ordered_count': ordered_ie,
            'strict_positive_mass_lower': Q(1,64), 'strict_individual_entry_lower': Q(1,2**31)}


# Tiny coefficient ring in six formal variables x,y,s,c,X,Y over Q.
# The all-order proof uses the identity, not evaluations at bounded orders.
def p_add(*polys):
    out = {}
    for poly in polys:
        for m, c in poly.items():
            out[m] = out.get(m, Q(0))+c
    return {m:c for m,c in out.items() if c}


def p_mul(*polys):
    out = {(0,)*6: Q(1)}
    for poly in polys:
        nxt = {}
        for m, c in out.items():
            for k, d in poly.items():
                key = tuple(a+b for a,b in zip(m,k))
                nxt[key] = nxt.get(key, Q(0))+c*d
        out = {m:c for m,c in nxt.items() if c}
    return out


def p_scale(c, p):
    return {m:Q(c)*v for m,v in p.items() if c*v}


def polynomial_identity(damage=False):
    vs = [{tuple(int(k == i) for k in range(6)):Q(1)} for i in range(6)]
    x,y,s,c,X,Y = vs
    sp = p_add(s,c); sm = p_add(s,p_scale(-1,c))
    XmY = p_add(X,p_scale(-1,Y)); XpY = p_add(X,Y)
    xXp = p_add(p_mul(x,X),p_mul(y,Y))
    xXm = p_add(p_mul(x,X),p_scale(-1,p_mul(y,Y)))
    lhs = p_add(p_mul(x,y,p_add(p_mul(sp,XmY,XmY),p_mul(sm,XpY,XpY))),
                p_mul(sp,xXp,xXp),p_mul(sm,xXm,xXm))
    rhs = p_scale(2,p_mul(s,p_add(x,y),p_add(p_mul(x,X,X),p_mul(y,Y,Y))))
    if damage:
        lhs = p_add(lhs,p_mul(c,x,y,X,Y))
    require(lhs == rhs, 'Universal cleared quadratic coefficient identity')
    return {'formal_variables': ['x','y','s','c','X','Y'], 'coefficient_count': len(lhs),
            'exact_coefficients': [{'exponents': list(m), 'value': v} for m,v in sorted(lhs.items())]}


def table_check(n,z,b,positive=False):
    B = complete(n,z,b)
    values = [B[a][c] for a,c in supported_pairs(n) if a >= 2]
    require(B == direct(n,values), 'S2 completion vs separate singleton solve')
    forms = []
    for upper in (False,True):
        for j in range(3):
            red = root_reduction(n,B,j,upper)
            require(red['schur'] == direct_schur(n,B,j,upper), 'Dense vs pair Schur')
            if positive:
                both(red['schur'],len(red['roots']))
                aa,g,F = reduced_physical(n,B,j,upper); both(F,len(aa))
            forms.append({'degree':j, 'upper':upper, 'root_order':len(red['roots']),
                          'schur':red['schur'], 'mean_gamma':red['mean_gamma']})
    budget = lower_energy_budget(n,B); s=parameters(n)[1]; c=B[2][n-2]
    L1 = root_reduction(n,B,1)['schur']; L2 = root_reduction(n,B,2)['schur']
    require(L1[0][0]/(n-2)-c*c/s == budget['A']-(n-3)*b[2]-budget['E1_normalized'],
            'Degree-one root budget')
    require(L2[0][0]-c*c/s == budget['A']+b[2]-budget['E2'], 'Degree-two root budget')
    if positive:
        require(budget['combined_cost'] < budget['combined_budget'], 'Strict seed budget')
        for j in range(3,n//2+1):
            for upper in (False,True):
                aa,g,F = physical(n,B,j,upper); both(F,len(aa))
    return {'n':n, 'forms':forms, 'budget':budget, 'original_defect':defect(n,B)}


def s2_controls():
    records=[]; directions=[]
    for n in (6,7,10,16,20):
        z={a:Q(1) for a in range(2,n//2+1)}; b={a:Q(0) for a in range(2,n-2)}
        records.append(table_check(n,z,b))
        for label,keys in [('z',list(z)),('b',list(b))]:
            for key in keys:
                zz=z.copy(); bb=b.copy(); (zz if label=='z' else bb)[key]+=1
                rec=table_check(n,zz,bb)
                directions.append({'n':n,'coordinate':[label,key],'exact_record_sha256':digest(rec)})
    require(len(directions) == 63, 'All bounded S2 free directions')
    six=table_check(6,{2:Q(4),3:Q(2)},{2:Q(4,3),3:Q(0)})
    require(six['original_defect'][1] == 0, 'Credited centered six-point seed')
    ten=table_check(10,{2:Q(519,25),3:Q(107,50),4:Q(111,50),5:Q(11,5)},
                    {2:Q(47,50),3:Q(11,25),4:Q(6,25),5:Q(0),6:Q(0),7:Q(0)},True)
    require(ten['original_defect'][1] > 0, 'Credited noncentered ten-point cap')
    boundary=[]
    for n in (6,7,8):
        for sign in (1,-1):
            s=parameters(n)[1]
            z={a:Q((1-sign)*s) for a in range(2,n//2+1)}
            b={a:Q(0) for a in range(2,n-2)}
            B=complete(n,z,b)
            # Mean degree zero can fail for c=-s; ordinary necessary budget uses1/2.
            red=[root_reduction(n,B,j)['schur'] for j in (1,2)]
            budget=lower_energy_budget(n,B)
            require(budget['diagonal_cost'] == budget['diagonal_budget'] == 0,
                    'Both singular complement signs force zero two-set budget')
            boundary.append({'n':n,'sign':sign,'schur':red,'budget':budget})
    return {'base_controls':records, 'direction_count':len(directions),
            'direction_record_hashes':directions, 'credited_six':six,
            'credited_ten':ten, 'singular_complement_boundaries':boundary}


def determinant3(A):
    return (A[0][0]*(A[1][1]*A[2][2]-A[1][2]**2)
            -A[0][1]*(A[0][1]*A[2][2]-A[1][2]*A[0][2])
            +A[0][2]*(A[0][1]*A[1][2]-A[1][1]*A[0][2]))


def psd_backend_controls():
    positive=0; hashes=[]
    for entries in product((-1,0,1),repeat=6):
        a,b,c,d,e,f=entries
        A=[[a,b,c],[b,d,e],[c,e,f]]
        oracle=(a >= 0 and d >= 0 and f >= 0 and a*d-b*b >= 0 and
                a*f-c*c >= 0 and d*f-e*e >= 0 and determinant3(A) >= 0)
        try:
            rank=both(A)
        except ValueError:
            require(not oracle,'PSD engine incorrectly rejects principal-minor oracle')
            hashes.append([list(entries),False])
        else:
            require(oracle,'PSD engine accepts false principal-minor oracle')
            positive+=1; hashes.append([list(entries),rank])
    require(positive == 24, 'Complete ternary PSD control count')
    return {'symmetric_ternary_matrices':729, 'PSD_count':positive,'full_census_sha256':digest(hashes)}


def original_data(n):
    N,s,h=parameters(n)
    require(N <= 247,'Literal original-coordinate guard N<=247')
    masks=[a for a in range(1,2**n) if a.bit_count() <= n-2]
    require(len(masks) == N-1,'Original nonempty census')
    B=complete(n,{a:Q(1) for a in range(2,n//2+1)},
               {a:Q(0) for a in range(2,n-2)})
    C=[[Q(s*int(A==D)-1)+(B[A.bit_count()][D.bit_count()] if A&D == 0 else 0)
        for D in masks] for A in masks]
    require(all(v.denominator == 1 for row in C for v in row),'Integral affine fixture')
    C=[[int(v) for v in row] for row in C]
    v=[sum(row) for row in C]; sigma=sum(v)
    L=[[1+sigma]+[1-x for x in v]]
    L.extend([[1-v[i]]+[1+x for x in row] for i,row in enumerate(C)])
    return masks,B,C,L


def original_checks(n,masks,C,L):
    N,s,h=parameters(n); all_masks=[0]+masks
    require(len(L)==N and all(len(row)==N for row in L),'Actual whole lift shape')
    v=[sum(row) for row in C];sigma=sum(v)
    require(L[0][0]==1+sigma and L[0][1:]==[1-x for x in v], 'Actual empty loop and row')
    require(all(sum(row)==N for row in L),'All original regular rows')
    for i,A in enumerate(all_masks):
        for k,D in enumerate(all_masks):
            require(L[i][k]==L[k][i],'Original symmetry')
            if A&D:
                require(L[i][k] == s*int(i==k),'Original H intersection support')
    for point in range(n):
        inds=[i for i,A in enumerate(all_masks) if (A>>point)&1]
        require(len(inds)==s,'Actual star cardinality')
        require(all(sum(row[k] for k in inds)==s for row in L),'Every full forced star')
        core_inds=[k-1 for k in inds]
        require(all(sum(row[k] for k in core_inds)==0 for row in C),'Every nonempty forced star')
    return {'n':n,'N':N,'whole_ordered_entries':N*N,'stars':n,
            'sigma':sigma,'row_defect_norm2':sum(x*x for x in v),
            'actual_empty_loop':L[0][0],'whole_affine_sha256':digest(L)}


def phi(mask,j):
    value=1
    for i in range(j):
        value*=int(bool(mask&(1<<(2*i))))-int(bool(mask&(1<<(2*i+1))))
    return value


def physical_original_checks(n,masks,B,C):
    N,s,h=parameters(n); action_count=0; records=[]
    for j in range(4):
        aa,g,F=physical(n,B,j)
        au,gu,U=physical(n,B,j,True)
        require(au==aa and gu==g,'Both physical layer labels')
        for bi,b in enumerate(aa):
            vector=[phi(A,j) if A.bit_count()==b else 0 for A in masks]
            require(sum(x*x for x in vector)==2**j*g[b],'Actual original Gram norm')
            nz=[(k,x) for k,x in enumerate(vector) if x]
            total=sum(vector)
            require(total==(comb(n,b) if j==0 else 0),'Actual constant projection')
            for i,A in enumerate(masks):
                a=A.bit_count(); p=phi(A,j)
                disjoint=sum(x for k,x in nz if A&masks[k]==0)
                target=(-1)**j*choose(n-a-j,b-j)*p
                require(disjoint==target,'Every original disjoint action')
                acted=sum(C[i][k]*x for k,x in nz)
                expected=s*vector[i]-total+B[a][b]*target
                require(acted==expected,'Literal original lower action')
                upper=N*vector[i]-total-acted
                require(upper==h*vector[i]-B[a][b]*target,'Literal original upper action')
                if a in aa:
                    ai=aa.index(a)
                    require(acted==F[ai][bi]*p/g[a] and upper==U[ai][bi]*p/g[a],
                            'Displayed physical forms in actual point metric')
                action_count+=1
            records.append({'j':j,'layer':b,'norm2':2**j*g[b],
                            'vector_sha256':digest(vector)})
    return {'n':n,'original_coordinate_actions':action_count,
            'physical_vectors':records}


def orbit_table(n,masks,C):
    sums={};counts={};s=parameters(n)[1]
    for i,A in enumerate(masks):
        for k,D in enumerate(masks):
            if A&D==0:
                key=tuple(sorted((A.bit_count(),D.bit_count())))
                sums[key]=sums.get(key,0)+C[i][k]+1
                counts[key]=counts.get(key,0)+1
    return {key:Q(v,counts[key]) for key,v in sums.items()}


def original_controls():
    fixtures=[];actions=[];trade_record=None
    for n in (6,8):
        masks,B,C,L=original_data(n)
        fixtures.append(original_checks(n,masks,C,L))
        actions.append(physical_original_checks(n,masks,B,C))
        if n==8:
            before=orbit_table(n,masks,C)
            loc={A:i for i,A in enumerate(masks)}
            left=[(1<<0)|(1<<2),(1<<0)|(1<<3),(1<<1)|(1<<2),(1<<1)|(1<<3)]
            right=[(1<<4)|(1<<6),(1<<4)|(1<<7),(1<<5)|(1<<6),(1<<5)|(1<<7)]
            signs=[1,-1,-1,1]; changed=0
            for A,x in zip(left,signs):
                for D,y in zip(right,signs):
                    require(A&D==0,'Original rectangle supported')
                    i,k=loc[A],loc[D]
                    C[i][k]+=x*y;C[k][i]+=x*y
                    L[i+1][k+1]+=x*y;L[k+1][i+1]+=x*y
                    changed+=2
            after=orbit_table(n,masks,C)
            require(before==after,'Original signed orbit averages preserved')
            require(C[loc[left[0]]][loc[right[0]]] != C[loc[left[0]]][loc[right[1]]],
                    'Trade truly breaks invariance')
            require(C[loc[left[0]]][loc[right[0]]]+1==1 and
                    C[loc[left[0]]][loc[right[1]]]+1==-1,'Both original entry signs')
            require(all(after[(a,b)]==B[a][b] for a,b in after),'Actual orbit means equal model')
            trade_record={'changed_ordered_positions':changed,
                          'signed_orbit_average_sha256':digest([[a,b,v] for (a,b),v in sorted(after.items())]),
                          'noninvariant_whole_checks':original_checks(n,masks,C,L)}
    return {'affine_fixtures':fixtures,'original_physical_actions':actions,
            'signed_noninvariant_rectangle':trade_record,
            'scope':'Affine/support/metric controls; no capped feasibility asserted for these fixtures'}


def rejects(action,name):
    try:
        action()
    except (ValueError,KeyError,TypeError,ZeroDivisionError):
        return name
    raise ValueError('Damaged input accepted: '+name)


def damage_controls(data):
    outcomes=[]
    for name,change in [
        ('floating_dual_entry',lambda d:d['forms'][0]['triangle'][0].__setitem__(0,1.0)),
        ('triangle_width',lambda d:d['forms'][0]['triangle'][0].pop()),
        ('original_layer_label',lambda d:d['forms'][0]['layers'].__setitem__(0,1)),
        ('lower_upper_mode',lambda d:d['forms'][0].__setitem__('upper',True)),
        ('negative_degree_three_multiplier',lambda d:d.__setitem__('degree_three_multiplier','-1')),
        ('unordered_pair_factor',lambda d:d.__setitem__('original_unordered_count',37884444)),
    ]:
        d=copy.deepcopy(data);change(d)
        outcomes.append(rejects(lambda d=d:decode(d),name))
    blocks,lam=decode(data)
    bad=copy.deepcopy(blocks[0][3]);bad[0][0]=-Q(1)
    outcomes.append(rejects(lambda:both(bad),'negative_dual_PSD'))
    # A positive diagonal perturbation preserves PSD but destroys b22 cancellation.
    bad_blocks=copy.deepcopy(blocks);bad_blocks[2][3][0][0]+=1
    pairs=[(a,b) for a,b in supported_pairs(16) if a>=2]
    vals=[Q(32751) if a+b==16 else Q(0) for a,b in pairs]
    base=direct(16,vals);changed=vals.copy();changed[pairs.index((2,2))]+=1
    other=direct(16,changed)
    outcomes.append(rejects(lambda:require(functional(other,bad_blocks,lam)==
                                           functional(base,bad_blocks,lam), 'S2 cancellation'),
                            'PSD_preserving_false_affine_cancellation'))
    outcomes.append(rejects(lambda:require(functional(base,blocks,lam)==0,'Claimed constant'),
                            'false_affine_constant'))
    outcomes.append(rejects(lambda:polynomial_identity(True),'universal_mixed_coefficient'))
    outcomes.append(rejects(lambda:complete(6,{2:Q(1),3:1.0},{2:Q(0),3:Q(0)}),'floating_S2_coordinate'))
    outcomes.append(rejects(lambda:root_reduction(6,complete(6,{2:Q(1),3:Q(0)},
                                {2:Q(0),3:Q(1)}),1),'singular_complement_range'))
    outcomes.append(rejects(lambda:root_reduction(6,complete(6,{2:Q(1),3:Q(52)},
                                {2:Q(0),3:Q(0)}),0),'singular_negative_mean_bulk'))
    outcomes.append(rejects(lambda:original_data(16),'original_matrix_allocation_guard'))
    masks,B,C,L=original_data(6);L[0][0]+=1
    outcomes.append(rejects(lambda:original_checks(6,masks,C,L),'actual_empty_loop'))
    masks,B,C,L=original_data(6);L[0][1:]=[1]*(len(L)-1)
    outcomes.append(rejects(lambda:original_checks(6,masks,C,L),'false_centered_empty_row'))
    outcomes.append(rejects(lambda:require(sum(phi(A,2)**2 for A in masks if A.bit_count()==3)==
                            comb(2,1),'Physical metric missing factor2^j'), 'wrong_original_harmonic_norm'))
    return outcomes


def replay():
    data=json.loads((HERE/'dual.json').read_text())
    return {'agent':'six-downset-2','role':'researcher',
            'claim_status':'Exact finite certificate plus ordinary all-order lemma; real/PSD/averaging bridges unformalized; independently unreviewed',
            'dual_file_sha256':hashlib.sha256((HERE/'dual.json').read_bytes()).hexdigest(),
            'finite_certificate':finite_certificate(data),
            'universal_polynomial_identity':polynomial_identity(),
            'S2_reduction_controls':s2_controls(),
            'PSD_backend_controls':psd_backend_controls(),
            'original_definition_controls':original_controls(),
            'rejected_damages':damage_controls(data)}


def main():
    parser=argparse.ArgumentParser()
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write-expected',type=Path)
    mode.add_argument('--check',type=Path)
    args=parser.parse_args()
    result=replay();payload=canonical(result)
    if args.write_expected is not None:
        args.write_expected.write_bytes(payload)
    else:
        require(args.check.read_bytes()==payload,'Complete regenerated frozen record mismatch')
    print(json.dumps({'ok':True,'finite_n':16,'free_directions':49,'S2_cancellations':19,
                      'positive_omitted_orbits':30,'original_unordered_pairs':18942222,
                      'S2_validation_directions':63,'damage_controls':len(result['rejected_damages']),
                      'record_sha256':hashlib.sha256(payload).hexdigest()},sort_keys=True))


if __name__=='__main__':
    main()
