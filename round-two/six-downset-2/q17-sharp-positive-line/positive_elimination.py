"""Positive-content Schur elimination on the complete original residual.

Each active integer form is a known positive multiple c of the original
Schur complement. A positive pivot p gives the numerator p*Krest-u*u^T.
Dividing by its positive integer content g replaces c by c*p/g. All exact
divisions are checked. This is a full-coordinate algorithm, not a quotient.
"""
import argparse
import hashlib
import json
from fractions import Fraction
from math import gcd
from pathlib import Path

def require(ok, message):
    if not ok:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def positive_content(matrix):
    g = 0
    for i, row in enumerate(matrix):
        for x in row[i:]:
            if g != 1:
                g = gcd(g, x)
    return g


def divide_content(matrix, content):
    require(type(content) is int and content > 0, 'strictly positive integer content')
    out = []
    for row in matrix:
        new = []
        for x in row:
            value, remainder = divmod(x, content)
            require(remainder == 0, 'every original-coordinate content division exact')
            new.append(value)
        out.append(new)
    return out


def eliminate(matrix, reference=None, state_path=None):
    n = len(matrix)
    require(n > 0 and all(len(row) == n for row in matrix), 'complete nonempty square residual')
    require(all(type(x) is int for row in matrix for x in row), 'exact integer domain')
    require(all(matrix[i][j] == matrix[j][i] for i in range(n) for j in range(n)),
            'every original residual symmetry position')
    if reference is not None:
        require(len(reference) == n and all(type(x) is int for x in reference),
                'complete reference leading-minor domain')
    g0 = positive_content(matrix)
    if g0 == 0:
        return {'status': 'nonpositive_pivot', 'order': 1, 'dimension': n,
                'original_leading_minors': ['0'], 'does_not_prove_candidate_nonexistence': True}
    active = divide_content(matrix, g0)
    c = Fraction(1, g0)
    determinant = Fraction(1)
    minors = []
    pivots = []
    contents = [str(g0)]
    updates = 0
    divisions = n * n
    whole_digest = hashlib.sha256(canonical(matrix)).hexdigest()
    for k in range(n):
        p = active[0][0]
        determinant *= Fraction(p) / c
        require(determinant.denominator == 1, 'every tracked original principal determinant integral')
        minors.append(str(determinant.numerator))
        pivots.append(str(p))
        if reference is not None:
            require(determinant.numerator == reference[k], 'every full original reference minor agrees')
        if p <= 0:
            return {'status': 'nonpositive_pivot', 'order': k + 1, 'dimension': n,
                    'original_leading_minors': minors, 'normalized_pivots': pivots,
                    'positive_contents': contents, 'does_not_prove_candidate_nonexistence': True}
        m = len(active) - 1
        if m == 0:
            break
        tail = [[0] * m for _ in range(m)]
        g = 0
        for i in range(m):
            u = active[i + 1][0]
            for j in range(i, m):
                value = p * active[i + 1][j + 1] - u * active[0][j + 1]
                tail[i][j] = tail[j][i] = value
                if g != 1:
                    g = gcd(g, value)
                updates += 1
        if g == 0:
            # A zero Schur complement supplies a zero next pivot, not PD.
            g = 1
        active = divide_content(tail, g)
        divisions += m * m
        c *= Fraction(p, g)
        contents.append(str(g))
        if state_path and (k + 1) % 32 == 0:
            state = {'original_matrix_sha256': whole_digest, 'completed_pivots': k + 1,
                     'dimension': n, 'scale': str(c), 'active_scaled_Schur_matrix': active,
                     'original_leading_minors': minors, 'normalized_pivots': pivots,
                     'positive_contents': contents, 'candidate_PD_not_yet_proved': True,
                     'research_state_only_not_an_independent_certificate': True}
            target = Path(state_path)
            temp = target.with_suffix(target.suffix + '.tmp')
            temp.write_bytes(canonical(state) + b'\n')
            temp.replace(target)
    return {'status': 'positive_definite', 'dimension': n,
            'original_leading_minors': minors, 'normalized_pivots': pivots,
            'positive_contents': contents, 'symmetric_numerator_updates': updates,
            'checked_content_divisions': divisions,
            'every_reference_minor_equal': reference is not None}
