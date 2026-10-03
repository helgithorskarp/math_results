"""Exact original rank-nine PSD dual, without a numerical input or solver.

Actual author six-downset-2, researcher. Independent literal counts and
star recovery are compared to the credited public model on its complete
affine basis. Ordinary real/counting/rank bridges remain unformalized.
"""
import argparse
import copy
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from math import comb
import os
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
REFERENCE = HERE.parent/'minimal_complement_classes_n24'
THREADS = ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
           'NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS')
DEPENDENCIES = {
    'CERTIFICATE.json': 'ddb58b2b00da4740126fba8784337e682e5d5cdb749eeb19e4659eabbecfbdf0',
    'model.py': '3a5e7f841699a27f674cf4c09560d80d86d52cb3443a6242485da503ca824974',
    'credited/matrices.py': '4541b4b7669ce706e0142339d614ebb36b46214f137abe2475a9d9ad99fd9588',
}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def schema(n, active):
    r, s, N = n-2, 2**(n-1)-n, 2**n-n-1
    middle = n//2
    endpoints = set(active)|{n-a for a in active}|{middle}
    proper = [(a,b) for a in range(2,r+1) for b in range(a,r+1)
              if a+b < n and a in endpoints and b in endpoints]
    return dict(n=n,r=r,s=s,N=N,h=N-s,active=active,middle=middle,proper=proper,
                names=['d'+str(a) for a in (*active,middle)]+
                      ['t'+str(a)+'_'+str(b) for a,b in proper])


def defining(spec, values):
    n,r,s,N = (spec[k] for k in ('n','r','s','N'))
    need(len(values) == len(spec['names']) and all(type(x) is Q for x in values),
         'Every exact original defining coefficient')
    B = [[Q(0) for _ in range(r+1)] for _ in range(r+1)]
    count = len(spec['active'])+1
    d = dict(zip((*spec['active'],spec['middle']),values[:count]))
    for a in range(2,spec['middle']+1):
        B[a][n-a] = B[n-a][a] = s-d.get(a,Q(0))
    for (a,b), t in zip(spec['proper'],values[count:]):
        B[a][b] = B[b][a] = t
    for a in range(2,r+1):
        B[a][1] = B[1][a] = s-sum(b*B[a][b]*choose(n-a,b)
                                  for b in range(2,r+1))/(n-a)
    B[1][1] = s-sum(b*B[1][b]*choose(n-1,b) for b in range(2,r+1))/(n-1)
    saturated = [a for a in range(2,spec['middle']) if a not in spec['active']]
    need(all(B[a][b] == B[b][a] for a in range(r+1) for b in range(r+1)), 'Original symmetry')
    for a in range(1,r+1):
        need(sum(b*B[a][b]*choose(n-a,b) for b in range(1,r+1)) == (n-a)*s,
             'Every original nonempty point-star identity')
        for b in range(1,r+1):
            if a+b > n or (a+b < n and
                    (a in saturated or n-a in saturated or b in saturated or n-b in saturated)):
                need(B[a][b] == 0, 'Every original unsupported or saturated-incident entry')
    rows = [N-s-sum(B[a][b]*choose(n-a,b) for b in range(1,r+1))
            for a in range(1,r+1)]
    loop = N-sum(comb(n,a)*rows[a-1] for a in range(1,r+1))
    for a in range(1,r+1):
        need(rows[a-1]+s+sum(B[a][b]*choose(n-a,b) for b in range(1,r+1)) == N,
             'All actual original nonempty rows')
        need(sum(B[a][b]*choose(n-a-1,b-1) for b in range(1,r+1)) == s,
             'Every original outside point-star row')
    need(sum(comb(n-1,b-1)*rows[b-1] for b in range(1,r+1)) == s,
         'Actual original empty-row star identity')
    need(loop+sum(comb(n,a)*rows[a-1] for a in range(1,r+1)) == N,
         'Actual original empty row, including its permitted loop')
    return B,dict(row=rows,loop=loop)


def original_energy(spec,B,u):
    n,r,s = (spec[k] for k in ('n','r','s'))
    need(len(u) == r and all(type(x) is int for x in u), 'All original integer layer coefficients')
    diagonal = 2*s*sum(comb(n-2,a-1)*u[a-1]**2 for a in range(1,r+1))
    disjoint = -2*sum(B[a][b]*comb(n-2,a-1)*choose(n-a-1,b-1)*u[a-1]*u[b-1]
                      for a in range(1,r+1) for b in range(1,r+1))
    return diagonal+disjoint


def determinant(A):
    M = [[Q(x) for x in row] for row in A]
    ans = Q(1)
    for k in range(len(M)):
        p = next((i for i in range(k,len(M)) if M[i][k]),None)
        if p is None:
            return Q(0)
        if p != k:
            M[p],M[k] = M[k],M[p]
            ans = -ans
        pivot = M[k][k]
        ans *= pivot
        for i in range(k+1,len(M)):
            multiplier = M[i][k]/pivot
            for j in range(k,len(M)):
                M[i][j] -= multiplier*M[k][j]
    return ans


def load(name,path):
    item = importlib.util.spec_from_file_location(name,path)
    mod = importlib.util.module_from_spec(item)
    item.loader.exec_module(mod)
    return mod


def vector_value(A,u):
    return 0 if not A else u[len(A)-1]*(int(1 in A)-int(2 in A))


def validate(data):
    spec = schema(26,(8,9,10,11,12))
    need(data['n'] == 26 and data['active'] == list(spec['active']) and data['names'] == spec['names'],
         'Declared carrier and all36 original affine labels')
    u, g = data['integer_layer_direction'], data['old_integer_layer_direction']
    mu,w = data['old_direction_weight'],data['empty_direction_weight']
    lam = data['deficit_difference_weights']
    need(type(mu) is int and mu > 0 and type(w) is int and w > 0 and
         len(lam) == 6 and all(type(x) is int and x > 0 for x in lam),
         'All eight nontrivial original outer-product weights positive')
    need(len(u) == len(g) == 24 and all(type(x) is int for x in u+g), 'Whole original profiles')
    need(len(data['fixed_transported_proper_values']) == len(spec['proper']) == 30,
         'Every fixed proper input present')
    for name,digest in DEPENDENCIES.items():
        need(hashlib.sha256((REFERENCE/name).read_bytes()).hexdigest() == digest,
             'Pinned credited public dependency: '+name)
    seed = json.loads((REFERENCE/'CERTIFICATE.json').read_bytes())
    old = schema(24,(7,8,9,10,11))
    need(seed['n'] == 24 and seed['names'] == old['names'] and
         spec['proper'] == [(a+1,b+1) for a,b in old['proper']], 'Complete proper-label transport')
    def scales(S):
        n = S['n']
        return [Q(n)]*(len(S['active'])+1)+[Q(n,max(choose(n-a-1,b-1),choose(n-b-1,a-1)))
                                        for a,b in S['proper']]
    transported = [Q(x)/a*b for x,a,b in zip(seed['values'],scales(old),scales(spec))]
    fixed = [Q(x) for x in data['fixed_transported_proper_values']]
    need(fixed == transported[6:], 'All30 exact proper values reproduced from public10080 seed')
    # Independence of all9 original directions, using actual original vertices.
    universe = set(range(1,27))
    complements = [(set(range(1,i+1)),universe-set(range(1,i+1))) for i in range(8,14)]
    rows = [set(),{1},{1,*range(3,10)}]+[a for a,b in complements]
    minor = [[vector_value(A,u),vector_value(A,g),int(not A)]+
             [int(A == a)-int(A == b) for a,b in complements] for A in rows]
    minor_det = determinant(minor)
    need(minor_det != 0 and len(rows) == 9 and all(len(A) <= 24 for A in rows),
         'Nine original columns independent on actual original vertices')
    # Two literal signed profiles, six sparse complement differences, actual empty.
    def pairing(values):
        B,e = defining(spec,values)
        return original_energy(spec,B,u)+mu*original_energy(spec,B,g)+w*e['loop']+2*sum(
            coefficient*deficit for coefficient,deficit in zip(lam,values[:6]))
    zero = [Q(0)]*36
    probes = [zero]+[[Q(int(i == j)) for i in range(36)] for j in range(36)]
    model = load('credited_full_face_model',REFERENCE/'model.py')
    refspec = model.specification(26,(8,9,10,11,12))
    intercept = None
    coefficients = []
    for k,values in enumerate(probes):
        B,e = defining(spec,values)
        need(B == model.table(refspec,values), 'Whole table at every original affine-basis probe')
        other = model.empty_entries(refspec,B)
        need(e['row'] == other['row'] and e['loop'] == other['loop'],
             'All actual empty entries at every original affine-basis probe')
        result = pairing(values)
        if k == 0:
            intercept = result
        else:
            coefficients.append(result-intercept)
    need(coefficients[:6] == [Q(0)]*6, 'ALL six independent real deficit coefficients cancel')
    need(intercept == Q(data['full36_affine_cut_intercept']) and
         coefficients == [Q(x) for x in data['full36_affine_cut_coefficients']],
         'Entire claimed proper-only affine cut regenerated exactly')
    base = [Q(0)]*6+fixed
    value = pairing(base)
    need(value == intercept+sum(c*t for c,t in zip(coefficients[6:],fixed)) ==
         Q(data['strict_negative_fixed_slice_pairing']) < 0,
         'Exact strictly negative constant for every real choice of six deficits')
    # Direct ORIGINAL small matrix: independent of harmonic formulas/mean normalization.
    small = schema(8,(2,3))
    values = [Q(6),Q(179,100),Q(449,200)]+[Q(0)]*len(small['proper'])
    values[3+small['proper'].index((2,2))] = Q(37,25)
    B8,e8 = defining(small,values)
    literal = load('credited_original_n8_control',REFERENCE/'credited/matrices.py')
    members,L = literal.construct(8,{2:Q(6),3:Q(179,100),4:Q(449,200)},Q(37,25))
    bitsets = [set(i+1 for i in range(8) if A >> i & 1) for A in members]
    for i,A in enumerate(bitsets):
        for j,T in enumerate(bitsets):
            expected = e8['loop'] if not A and not T else (
                e8['row'][len(T)-1] if not A else (
                e8['row'][len(A)-1] if not T else (
                Q(small['s']) if i == j else (Q(0) if A & T else B8[len(A)][len(T)]))))
            need(L[i][j] == expected, 'Every actual original n8 entry, including empty and loop')
    controls = ([2,-3,5,-7,11,-13],[3,0,7,7,7,0])
    literal_energies = []
    for profile in controls:
        f = [vector_value(A,profile) for A in bitsets]
        support = [i for i,x in enumerate(f) if x]
        direct = sum(Q(f[i])*L[i][j]*f[j] for i in support for j in support)
        need(direct == original_energy(small,B8,profile), 'Literal original signed-profile energy')
        literal_energies.append(direct)
    differences = []
    for a,d in zip((2,3,4),values[:3]):
        A = set(range(1,a+1));T = set(range(1,9))-A
        i,j = bitsets.index(A),bitsets.index(T)
        direct = L[i][i]+L[j][j]-2*L[i][j]
        need(direct == 2*d, 'Literal actual complement-difference energy is2d')
        differences.append(direct)
    need(L[bitsets.index(set())][bitsets.index(set())] == e8['loop'], 'Actual empty-indicator energy')
    return dict(agent='six-downset-2',role='researcher',status='exact original rank-nine PSD dual verified',
                n=26,N=spec['N'],s=spec['s'],h=spec['h'],
                original_profiles=[u,g],original_positive_weights=[1,mu,w,*lam],
                original_dual_rank=9,rank_minor_vertices=[sorted(A) for A in rows],
                rank_minor=minor,rank_minor_determinant=minor_det,
                complete_affine_basis_probes=len(probes),whole_table_entries_compared=len(probes)*25**2,
                all_original_row_star_support_and_empty_equations=True,
                full36_affine_cut_intercept=intercept,full36_affine_cut_coefficients=coefficients,
                fixed_transported_proper_values=fixed,strict_negative_fixed_slice_pairing=value,
                all_real_six_deficit_fixed30_family_excluded=True,
                original_lower_PSD_only=True,upper_cap_not_used=True,full36_real_face_infeasible=False,
                literal_baseline=dict(credited_claim='8319/0',vertices=len(members),entries_compared=len(members)**2,
                                      signed_profile_energies=literal_energies,difference_energies=differences,
                                      actual_empty_loop=e8['loop'],new_research=False),
                public_dependency_sha256=DEPENDENCIES,solver_or_numeric_input_used=False,
                harmonic_completeness_needed=False,ordinary_proof_unformalized=True,
                independent_new_result_review='pending')


def audit(data):
    damages = []
    for label,key,index in [('negative_empty_weight','empty_direction_weight',None),
                            ('negative_profile_weight','old_direction_weight',None),
                            ('negative_difference_weight','deficit_difference_weights',0),
                            ('missing_empty_energy','empty_direction_weight',None),
                            ('wrong_independent_deficit_weight','deficit_difference_weights',4),
                            ('wrong_actual_profile','integer_layer_direction',7),
                            ('wrong_proper_only_cut','full36_affine_cut_coefficients',10),
                            ('wrong_exact_transport','fixed_transported_proper_values',29)]:
        altered = copy.deepcopy(data)
        if index is None:
            altered[key] = 0 if label == 'missing_empty_energy' else -abs(altered[key])
        elif type(altered[key][index]) is int:
            altered[key][index] = -abs(altered[key][index]) if label == 'negative_difference_weight' else altered[key][index]+1
        else:
            altered[key][index] = str(Q(altered[key][index])+1)
        try:
            validate(altered)
        except ValueError as error:
            damages.append(dict(label=label,rejected=True,reason=str(error)))
        else:
            raise ValueError('Semantic damaged certificate accepted: '+label)
    return damages


def encode(x):
    if type(x) is Q:
        return str(x)
    raise TypeError(type(x).__name__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',required=True)
    parser.add_argument('--check')
    parser.add_argument('--audit',action='store_true')
    args = parser.parse_args()
    need(all(os.environ.get(k) == '1' for k in THREADS), 'Native threads all one')
    data = json.loads((HERE/'CERTIFICATE.json').read_bytes())
    record = validate(data)
    if args.audit:
        record['semantic_rejections'] = audit(data)
    raw = (json.dumps(record,indent=2,default=encode)+'\n').encode()
    digest = hashlib.sha256(raw).hexdigest()
    if args.check:
        expected = json.loads(Path(args.check).read_text())
        need(expected == dict(record_bytes=len(raw),record_sha256=digest,semantic_audit=args.audit),
             'Entire regenerated mathematical record matches compact expected result')
    Path(args.output).write_bytes(raw)
    print(json.dumps(dict(status=record['status'],record_bytes=len(raw),record_sha256=digest,
                         original_dual_rank=9,strict_negative_fixed_slice_pairing=str(record['strict_negative_fixed_slice_pairing']),
                         affine_basis_probes=record['complete_affine_basis_probes'],
                         semantic_rejections=len(record.get('semantic_rejections',[])),
                         full36_real_face_infeasible=False,
                         flags=dict(isolated=sys.flags.isolated,optimize=sys.flags.optimize),
                         native_threads={k:os.environ[k] for k in THREADS})))


if __name__ == '__main__':
    main()
