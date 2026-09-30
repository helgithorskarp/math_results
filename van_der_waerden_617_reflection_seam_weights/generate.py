"""six-vdw-3, researcher: floating guidance for exact positive AP weights.

The certificate checker is separate. Neither LP optimality nor the discovery
enumeration's completeness is needed for the positive edit lower bound.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import time

P, N, C = 617, 3704, 1852


def edges(s):
    squares = {r*r % P for r in range(1, P)}
    t = (1 - s) % P
    colors = []
    for x in range(N):
        r = (x - C + (s if x < C else t)) % P
        colors.append(-1 if r == 0 else int(r not in squares) ^ int(x >= C))
    return [(a, d) for d in range(1, (N - 1)//6 + 1)
            for a in range(max(0, C - 6*d), min(C, N - 6*d))
            if colors[a] == 0 and all(colors[a + j*d] == 0 for j in range(1, 7))]


def discover(aps, seconds):
    import highspy as hs
    import numpy as np
    h = hs.Highs()
    options = {'threads': 1, 'parallel': 'off', 'output_flag': False,
               'solver': 'ipm', 'run_crossover': 'on', 'time_limit': seconds,
               'random_seed': 0, 'primal_feasibility_tolerance': 1e-9,
               'dual_feasibility_tolerance': 1e-9, 'ipm_optimality_tolerance': 1e-9}
    for name, value in options.items():
        if h.setOptionValue(name, value) != hs.HighsStatus.kOk:
            raise RuntimeError(f'Failed solver option: {name}')
    lp = hs.HighsLp()
    lp.num_col_, lp.num_row_ = len(aps), N
    lp.col_cost_, lp.col_lower_, lp.col_upper_ = (-np.ones(len(aps)), np.zeros(len(aps)), np.ones(len(aps)))
    lp.row_lower_, lp.row_upper_ = np.full(N, -hs.kHighsInf), np.ones(N)
    lp.a_matrix_.format_ = hs.MatrixFormat.kColwise
    lp.a_matrix_.start_ = np.arange(0, 7*len(aps) + 1, 7, dtype=np.int32)
    lp.a_matrix_.index_ = np.array([a+j*d for a, d in aps for j in range(7)], dtype=np.int32)
    lp.a_matrix_.value_ = np.ones(7*len(aps))
    if h.passModel(lp) != hs.HighsStatus.kOk:
        raise RuntimeError('Solver model load failed')
    h.run()
    solution = h.getSolution()
    if not solution.value_valid or not all(math.isfinite(v) for v in solution.col_value):
        raise RuntimeError('No finite guidance; this establishes no exclusion')
    info = h.getInfo()
    return solution.col_value, {'solver': h.version(), 'numpy': np.__version__,
                               'python': sys.version.split()[0], 'options': options,
                               'status': h.modelStatusToString(h.getModelStatus()),
                               'floating_objective': -h.getObjectiveValue(),
                               'ipm_iterations': info.ipm_iteration_count,
                               'crossover_iterations': info.crossover_iteration_count}


def rationalize(aps, values):
    q = 1000000
    numerators = [min(q, max(0, int(v*q))) for v in values]
    loads = [0]*N
    for (a, d), w in zip(aps, numerators):
        if w:
            for j in range(7):
                loads[a+j*d] += w
    denominator = max(q, max(loads))
    return denominator, sorted([a, d, w] for (a, d), w in zip(aps, numerators) if w)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('phase', type=int)
    p.add_argument('certificate', type=Path)
    p.add_argument('--seconds', type=float, default=15)
    p.add_argument('--guidance', type=Path)
    a = p.parse_args()
    if not (0 <= a.phase < P and 0 < a.seconds <= 60):
        raise ValueError('Phase or bounded guidance time')
    start = time.monotonic()
    aps = edges(a.phase)
    generated = time.monotonic() - start
    values, metadata = discover(aps, a.seconds)
    den, weighted = rationalize(aps, values)
    certificate = {'format': 'QR617_REFLECTION_WEIGHTS_1', 'P': P, 'N': N,
                   'terms': 7, 'seam': C, 's': a.phase, 't': (1-a.phase) % P,
                   'g': 1, 'denominator': den, 'color0_APs': weighted}
    raw = (json.dumps(certificate, sort_keys=True, separators=(',', ':'))+'\n').encode()
    partial = a.certificate.with_suffix(a.certificate.suffix+'.partial')
    partial.write_bytes(raw)
    os.replace(partial, a.certificate)
    metadata.update({'agent': 'six-vdw-3', 'role': 'researcher',
                     'color0_input_APs': len(aps), 'generation_seconds': generated,
                     'seconds': time.monotonic()-start,
                     'certificate_sha256': hashlib.sha256(raw).hexdigest(),
                     'certificate_bytes': len(raw), 'positive_weights': len(weighted),
                     'certificate_status': 'REQUIRES_INDEPENDENT_EXACT_CHECK'})
    if a.guidance:
        a.guidance.write_text(json.dumps(metadata, indent=2)+'\n')
    print(json.dumps(metadata), flush=True)


if __name__ == '__main__':
    main()
