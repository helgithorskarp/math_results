"""NEW full ORIGINAL FIRST shifted-system reader for the asymptotic formulas.

six-downset-1 / researcher; same author, not independent review.
The exact geometry is credited to b7d26214d61e1aba86367ce2162ccf2a4e1aa749.
No old executable/factor/inverse/result is imported. Finite controls
validate the formulas; the rational leading-coefficient argument pays
the infinite limit. No q>=200h original matrix is constructed.
"""
import os
for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
             'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ[name] = '1'
import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path
import resource
import signal
import time
from upper_reader import require, barrier, vector, matrix, dot, full_positive_solve


def count_shift(q, h, counts, theta):
    r, s, m = len(counts), q + 3 * h, 3 * sum(counts)
    det = [2 * q * q + (6 * h - 3 * theta) * q + theta * theta
           - 3 * theta * (h + k) for k in counts[1:]]
    require(6 * h - theta > 0 and 2 * q - theta > 0 and q - theta > 0
            and all(value > 0 for value in det), 'all shifted count poles positive')
    w = m + 3 * h * theta / (q - theta) + sum(
        (3 * k * theta * (2 * q + 6 * k - theta) / d
         for k, d in zip(counts[1:], det)), F(0))
    z = -F(3 * h) / (q - theta) - sum(
        (3 * k * (2 * q + 6 * h - theta) / d
         for k, d in zip(counts[1:], det)), F(0))
    g = F(q - 1) / (6 * h - theta) + F(3 * h * (q - r), q) / (2 * q - theta) \
        + F(3 * h, q) / (q - theta) + sum(
            (3 * ((h + k) * q + 3 * h * (h + k) - h * theta) / (q * d)
             for k, d in zip(counts[1:], det)), F(0))
    return w, z, g, m - w + (1 - z) ** 2 / (1 + g), det


def read(data):
    barrier()
    n, counts = data.get('n'), data.get('counts')
    require(type(n) is int and 4 <= n <= 6, 'n preflight BEFORE arrays')
    require(type(counts) is list and 3 <= len(counts) <= n
            and all(type(k) is int for k in counts), 'literal count preflight')
    h, q, r = counts[0], 2 ** (n - 1), len(counts)
    require(3 <= h <= 10 and all(2 <= k < h for k in counts[1:]) and sum(counts) >= 9,
            'unique-heavy/count preflight')
    N = 2 * q + 6 * sum(counts)
    require(N <= 80 and data.get('N') == N and data.get('dimension') == N - 3,
            'unchanged N80 BEFORE original construction')
    d, oldsize = N - 3, 2 * q - 1
    whole_metric = matrix(data['metric'], d, d)
    whole_rows = matrix(data['rows'], N, d)
    blocks, offset = [], oldsize
    for group, count in enumerate(counts):
        width = count - 1 if group == 0 else count
        if group:
            blocks.append(range(offset, offset + width))
        offset += width
    basis = [[F(i == j) for i in range(d)] for j in range(oldsize)]
    basis += [[F(i in block) for i in range(d)] for block in blocks]
    width = len(basis)
    metric_images = [[dot(row, b) for row in whole_metric] for b in basis]
    Gm = [[dot(a, image) for image in metric_images] for a in basis]
    require(all(Gm[i][j] == Gm[j][i] for i in range(width) for j in range(width)),
            'entire original FIRST metric symmetry')
    rows = [row[:oldsize] + [sum((row[i] for i in block), F(0)) / len(block)
                            for block in blocks] for row in whole_rows]
    ell = 3 * sum(counts) + 1
    K = [sum((row[j] for row in rows[1:oldsize + 3 * sum(counts) + 1]), F(0))
         for j in range(width)]
    G = [F(i < oldsize) for i in range(width)]
    W = [k - g for k, g in zip(K, G)]
    require(rows[0] == [-value / ell for value in K], 'actual empty FIRST centroid')
    images = [[dot(row, b) for b in Gm] for row in rows]
    full_frame = [[sum((row[i] * row[j] for row in images), F(0))
                   for j in range(width)] for i in range(width)]
    gmG, gmK, gmW = [[dot(row, v) for row in Gm] for v in (G, K, W)]
    Afirst = [[full_frame[i][j] + gmG[i] * gmG[j] - gmK[i] * gmK[j] / ell
               for j in range(width)] for i in range(width)]
    results = []
    for theta in (F(1), F(2)):
        D = [[(2 * (q + 3 * h) - theta) * Gm[i][j] - Afirst[i][j]
              for j in range(width)] for i in range(width)]
        (diW, diG), dfactor = full_positive_solve(D, [gmW, gmG], original_centered=False)
        w, z, g = dot(gmW, diW), dot(gmG, diW), dot(gmG, diG)
        require(z == dot(gmW, diG), 'BOTH full FIRST shifted mixed products')
        expected_w, expected_z, expected_g, sigma, det = count_shift(q, h, counts, theta)
        require((w, z, g) == (expected_w, expected_z, expected_g),
                'three count shifts equal FULL original FIRST inverse products')
        B = [[D[i][j] + gmG[i] * gmG[j] for j in range(width)] for i in range(width)]
        (biK,), bfactor = full_positive_solve(B, [gmK], original_centered=False)
        require(ell - dot(gmK, biK) == sigma, 'whole original FIRST Schur-square identity')
        require(all(D[i][j] + gmG[i] * gmG[j] - gmK[i] * gmK[j] / ell ==
                    (2 * (q + 3 * h) - theta) * Gm[i][j] - full_frame[i][j]
                    for i in range(width) for j in range(width)),
                'EVERY whole original shifted-frame identity')
        results.append(dict(theta=str(theta), count_poles=[str(x) for x in det],
                            w=str(w), z=str(z), g=str(g), sigma=str(sigma),
                            original_shift_identity_positions=width * width,
                            D_positive_factor=dfactor, B_positive_factor=bfactor,
                            D_inverse_images=[[str(x) for x in y] for y in (diW, diG)],
                            B_inverse_image=[str(x) for x in biK]))
    return dict(agent='six-downset-1', role='researcher', n=n, counts=counts, N=N,
                original_FIRST_dimension=width, original_rows_retained=N,
                status='NEW ORIGINAL SHIFTED FIRST FORMULAS VALIDATED',
                shifts=results, independently_reviewed=False,
                infinite_limit='ORDINARY UNFORMALIZED leading-coefficient/sign proof, not finite sampling',
                new_source_commit=None, new_graph_ref=None)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    require(not args.out.exists(), 'unique output')
    require(args.input.stat().st_size <= 32 * 1024 * 1024, '32MiB BEFORE data read')
    def expire(_signal, _frame):
        raise TimeoutError('unchanged60s; incomplete is not mathematical absence')
    signal.signal(signal.SIGALRM, expire)
    signal.alarm(60)
    started = time.monotonic()
    data = args.input.read_bytes()
    result = read(json.loads(data))
    raw = json.dumps(result, sort_keys=True, separators=(',', ':')).encode() + b'\n'
    require(len(raw) <= 32 * 1024 * 1024, '32MiB whole record')
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(raw)
    signal.alarm(0)
    print(json.dumps(dict(status=result['status'], input_sha256=sha256(data).hexdigest(),
                         mathematical_bytes=len(raw), mathematical_sha256=sha256(raw).hexdigest(),
                         seconds=time.monotonic() - started,
                         peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)))


if __name__ == '__main__':
    main()
