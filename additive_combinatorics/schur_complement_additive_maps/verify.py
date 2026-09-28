"""Independent standard-library checks of the additive working lemmas.

No SAT encoder, solver, generator, or numerical linear algebra is imported.
These finite checks accompany the general proofs, rather than replacing them.
"""
from fractions import Fraction
from itertools import product
import json
from pathlib import Path


def equations(n):
    return [(a, b, a+b) for a in range(1, n+1)
            for b in range(a, n-a+1)]


def sum_free(T):
    return all(a+b not in T for a in T for b in T)


def decomposition(n, T):
    M = set(range(1, n+1))-T
    if not M:
        return [], {}, []
    if 1 in M:
        a = 1
        t = min(T) if T else n+1
        candidates = [v for v in M if v > t]
    else:
        a = 2
        candidates = [v for v in M if v % 2]
    b = min(candidates) if candidates else None
    generators = [a] if b is None else [a,b]
    coefficients, recurrences = {}, []
    for v in sorted(M):
        if v == a:
            coefficients[v] = (1,0)
        elif v == b:
            coefficients[v] = (0,1)
        else:
            if v-a in M:
                u, generator = v-a, a
            elif b is not None and v-b in M:
                u, generator = v-b, b
            else:
                raise AssertionError(('no recursive determination', n,T,v))
            old = coefficients[u]
            coefficients[v] = (old[0]+(generator==a), old[1]+(generator==b))
            recurrences.append((u, generator, v))
        r,s = coefficients[v]
        assert r >= 0 and s >= 0 and r*a+s*(b or 0) == v
    for u,g,v in recurrences:
        assert u in M and g in M and v in M and u+g == v
    return generators, coefficients, recurrences


def rational_rank(rows, width):
    basis = {}
    for raw in rows:
        row = list(map(Fraction, raw))
        for p in sorted(basis):
            multiplier = row[p]
            if multiplier:
                row = [a-multiplier*b for a,b in zip(row,basis[p])]
        pivot = next((i for i,v in enumerate(row) if v), None)
        if pivot is not None:
            divisor = row[pivot]
            basis[pivot] = [v/divisor for v in row]
    return len(basis)


def audit(max_n=14):
    checked, matrix_checks, max_dimension = 0, 0, 0
    for n in range(1, max_n+1):
        sums = equations(n)
        for mask in range(1<<n):
            T = {v for v in range(1,n+1) if mask>>(v-1)&1}
            if not sum_free(T):
                continue
            generators, coefficients, paths = decomposition(n,T)
            M = sorted(set(range(1,n+1))-T)
            assert len(generators) <= 2 and set(coefficients) == set(M)
            checked += 1
            # Independent direct rational nullspace dimension for smaller
            # instances includes doubled coefficients when a=b.
            if n <= 9:
                index = {v:i for i,v in enumerate(M)}
                rows = []
                for a,b,c in sums:
                    if a in index and b in index and c in index:
                        row = [0]*len(M)
                        row[index[a]] += 1
                        row[index[b]] += 1
                        row[index[c]] -= 1
                        rows.append(row)
                dim = len(M)-rational_rank(rows,len(M))
                assert dim <= len(generators)
                max_dimension = max(max_dimension,dim)
                matrix_checks += 1
    # The three-residue upper construction must preserve each actual sum.
    heights, rejected = 0, 0
    for d in range(4,13):
        for q in range(1,11):
            n=d*q+1
            M={v for v in range(1,n+1) if v%d in (0,1,d-1)}
            def labels(A,B):
                return {v:((v//d)*A if v%d==0 else
                           (v//d)*A+B if v%d==1 else
                           ((v+1)//d)*A-B) for v in M}
            f=labels(2,1)
            assert 0 not in f.values() and max(map(abs,f.values())) == 2*q+1
            assert all(f[a]+f[b]==f[c] for a,b,c in equations(n)
                       if a in M and b in M and c in M)
            heights += 1
            # Any height<=2q map has nonzero A,B in that range. Exhaust
            # both signs independently; this checks the proof's split.
            for A,B in product(range(-2*q,2*q+1),repeat=2):
                if not A or not B:
                    continue
                f=labels(A,B)
                assert 0 in f.values() or max(map(abs,f.values())) > 2*q
                rejected += 1
    # Absolute-value pullback: verify the elementary signed-equation step.
    signed = 0
    for a,b in product(range(-12,13),repeat=2):
        c=a+b
        if not a or not b or not c:
            continue
        x,y,z=sorted((abs(a),abs(b),abs(c)))
        assert x+y==z
        signed += 1
    return {'sum_free_deletions_checked':checked,
            'rational_matrix_checks':matrix_checks,
            'maximum_observed_dimension':max_dimension,
            'three_residue_height_controls':heights,
            'smaller_height_parameter_pairs_rejected':rejected,
            'signed_equations_checked':signed}


def audit_parameterization():
    from parameterize import parameterize
    cyclic_assignments = 0
    for n in range(1, 10):
        for mask in range(1 << n):
            T = {v for v in range(1,n+1) if mask >> (v-1) & 1}
            if not sum_free(T):
                continue
            generators, coeff, rows = parameterize(n,T)
            M = set(range(1,n+1))-T
            # Check nonnegative construction coefficients and index identity.
            assert set(coeff)==M and len(generators)<=2
            for v,(r,s) in coeff.items():
                assert r>=0 and s>=0
                assert r*generators[0]+s*(generators[1] if len(generators)>1 else 0)==v
            for modulus in (2,3,4):
                for values in product(range(modulus),repeat=len(generators)):
                    A=values[0] if values else 0
                    B=values[1] if len(values)>1 else 0
                    f={v:(r*A+s*B)%modulus for v,(r,s) in coeff.items()}
                    direct=all((f[x]+f[y]-f[z])%modulus==0 for x,y,z in equations(n)
                               if x in M and y in M and z in M)
                    reduced=all((r*A+s*B)%modulus==0 for r,s in rows)
                    assert direct==reduced
                    cyclic_assignments += 1
    # Independent numeric check at q=107 for the exact claimed optimum.
    q=107
    target_pairs=0
    for A in (-2,-1,1,2):
        for B in range(-214,215):
            if not B: continue
            values=[j*A for j in range(1,q+1)]
            values += [j*A+B for j in range(q+1)]
            values += [j*A-B for j in range(1,q+1)]
            assert 0 in values or max(map(abs,values))>214
            target_pairs += 1
    # Height<=214 forces |A|<=2 by the value at535, covering every case.
    T={v for v in range(1,538) if v%5 in (2,3)}
    assert sum_free(T)
    generators,coeff,rows=parameterize(537,T)
    assert generators==[1,4] and not rows and len(coeff)==322
    f={v:r+s for v,(r,s) in coeff.items()}  # f(1)=f(4)=1, hence f(5)=2
    assert min(f.values())==1 and max(f.values())==215
    assert all(f[x]+f[y]==f[z] for x,y,z in equations(537)
               if x in f and y in f and z in f)
    return {'cyclic_group_assignments_checked':cyclic_assignments,
            'target_height_214_pairs_rejected':target_pairs,
            'target_minimum_height':215}


if __name__ == '__main__':
    result=audit()
    result.update(audit_parameterization())
    expected=json.loads(Path(__file__).with_name('expected.json').read_text())
    assert result==expected, (result,expected)
    print('PASS '+json.dumps(result,sort_keys=True))
