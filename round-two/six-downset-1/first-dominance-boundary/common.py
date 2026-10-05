"""Credited exact primitive helpers extracted from source6b upper_reader.

six-downset-1/researcher. Arithmetic helpers are verbatim after the
new attribution header; no old read/count/endpoint program is called
and no paid factor or expected record is imported. Not independent.
"""
import os
for _name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
              'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ[_name] = '1'
import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from math import lcm
from pathlib import Path
import resource
import signal
import time

LIMIT_BYTES = 32 * 1024 * 1024


def require(condition, message):
    if not condition:
        raise ValueError(message)


def barrier():
    root = os.environ.get('DISCOVERY_RESEARCH_TEAM_ROOT')
    if root:
        require(not any((Path(root) / name).exists() for name in
                ('PAUSED', 'PAUSED.json', 'HANDOVER', 'HANDOVER.json')),
                'operational barrier')


def rat(text):
    require(type(text) is str, 'canonical rational string')
    value = F(text)
    require(str(value) == text, 'canonical rational spelling')
    return value


def vector(raw, dimension):
    require(type(raw) is list and len(raw) == dimension, 'whole vector dimension')
    return [rat(value) for value in raw]


def matrix(raw, n, d):
    require(type(raw) is list and len(raw) == n, 'whole matrix row count')
    return [vector(row, d) for row in raw]


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def digest(value):
    return sha256(json.dumps(value, separators=(',', ':'), sort_keys=True).encode()).hexdigest()


def original_gram(rows, metric):
    """All original row pairs; sparsity only skips exact zero coefficients."""
    sparse = [[(j, v) for j, v in enumerate(row) if v] for row in rows]
    products = []
    for row in sparse:
        products.append([sum((v * metric[j][k] for j, v in row
                              if metric[j][k]), F(0))
                         for k in range(len(metric))])
    return [[sum((products[i][j] * value for j, value in row
                  if products[i][j]), F(0)) for row in sparse]
            for i in range(len(rows))]


def full_positive_solve(form, rhs, original_centered=True):
    """Full original Sylvester/Bareiss elimination and two exact RHS solves.

    Every symmetric trailing position and every RHS position is updated;
    every division is checked. No invariant-subspace inverse is used.
    """
    n = len(form)
    require(all(form[i][j] == form[j][i] for i in range(n) for j in range(n)),
            'full original upper form symmetry')
    denominator = 1
    for row in form + rhs:
        for value in row:
            denominator = lcm(denominator, value.denominator)
    integers = [[value.numerator * (denominator // value.denominator)
                 for value in form[i] + [column[i] for column in rhs]]
                for i in range(n)]
    previous, minors, divisions = 1, [], 0
    for k in range(n):
        pivot = integers[k][k]
        require(pivot > 0, 'full original V positive leading minor')
        minors.append(hex(pivot))
        for i in range(k + 1, n):
            factor = integers[i][k]
            for j in range(i, n):
                numerator = integers[i][j] * pivot - factor * integers[k][j]
                value, remainder = divmod(numerator, previous)
                require(remainder == 0, 'full original exact Bareiss division')
                integers[i][j] = integers[j][i] = value
                divisions += 1
            for j in range(n, n + len(rhs)):
                numerator = integers[i][j] * pivot - factor * integers[k][j]
                value, remainder = divmod(numerator, previous)
                require(remainder == 0, 'full original exact RHS division')
                integers[i][j] = value
                divisions += 1
            integers[i][k] = 0
        previous = pivot
    solutions = []
    for j in range(len(rhs)):
        x = [F(0)] * n
        for i in reversed(range(n)):
            x[i] = (F(integers[i][n + j]) -
                    sum((integers[i][k] * x[k] for k in range(i + 1, n)), F(0))) \
                   / integers[i][i]
        require([dot(row, x) for row in form] == rhs[j],
                'EVERY original inverse RHS product')
        if original_centered:
            require(sum(x, F(0)) == 0, 'original inverse image centered')
        solutions.append(x)
    return solutions, dict(dimension=n, denominator=str(denominator),
                           positive_leading_minors=n,
                           complete_positive_leading_minors_sha256=digest(minors),
                           exact_divisions=divisions, whole_rhs_products=n * len(rhs))


