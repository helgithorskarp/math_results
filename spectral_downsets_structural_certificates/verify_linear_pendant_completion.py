#!/usr/bin/env python3
"""Literal four-block replay, exhaustive Schur decomposition and exact full LDL.

Finite evidence validates implementation; the all-order proof is separate.
"""
import argparse
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
import json

import linear_pendant_completion as build
from affine_pendant_completion import geometry, add_pendants
from verify import check, psd_ldl, require

def construct(D, c, r=None):
    s, S, B = geometry(D, c)
    E = [0] + B
    t = len(E)
    r = t + 1 if r is None else r
    require(isinstance(r, int) and not isinstance(r, bool) and r >= t + 1,
            'Insufficient fresh count for this universal recipe')
    k, b, N = s + r, t + r, len(D) + 2 * r
    delta = t - s
    p = [1 << (max(D).bit_length() + j) for j in range(r)]
    z = [a | (1 << c) for a in p]
    family = add_pendants(D, c, r)
    ix = {a: i for i, a in enumerate(family)}
    u, v = F(1, r), F(k, b * r)
    w = F(r * r - s * t, b * r * (r - 1))
    y = F(r - t, r * (r - 1))
    mu = F(delta, b)
    eta = min(u, v, w)
    gap = F(2) * eta / ((N - 1) ** 2)
    Rbound = 2 * s + 4 * (b - 2)
    eps = min(F(1, 15 * b * Rbound), gap / (2 * Rbound), v / (2 * s), u / 2)
    if delta:
        eps = min(eps, mu / (2 * r), mu * y / 2)
    M = [[F(0)] * N for _ in family]
    def put(a, d, value):
        M[ix[a]][ix[d]] = M[ix[d]][ix[a]] = value
    for a in S:
        for q in p:
            put(a, q, u)
    for q in z:
        for a in E:
            put(q, a, v)
    for i in range(r):
        for j in range(r):
            if i != j:
                put(z[i], p[j], w)
    for a in E:
        for q in p:
            put(a, q, mu / r)
    for i in range(r):
        for j in range(i + 1, r):
            put(p[i], p[j], mu * y)
    raw = [row[:] for row in M]
    R = [[F(0)] * N for _ in family]
    def trade(a, d, amount):
        R[ix[a]][ix[d]] += amount
        if a != d:
            R[ix[d]][ix[a]] += amount
    # Square cross trade: all old stars get positive empty entries.
    for a in S:
        for x, d, amount in ((0, a, 1), (z[0], p[1], 1),
                             (a, p[1], -1), (z[0], 0, -1)):
            trade(x, d, amount)
    # Triangular outside trade: every outside empty edge gets a positive gain.
    for a in E[1:] + p[1:]:
        for x, d, amount in ((0, a, 1), (0, p[0], 1),
                             (p[0], a, -1), (0, 0, -2)):
            trade(x, d, amount)
    for i in range(N):
        for j in range(N):
            M[i][j] += eps * R[i][j]
    return family, raw, R, M, dict(original_N=len(D), original_s=s, t=t, r=r,
        k=k, b=b, N=N, delta=delta, u=u, v=v, w=w, y=y, mu=mu,
        eta=eta, upper_gap=gap, Rbound=Rbound, epsilon=eps)


def audit(D, c, r=None):
    family, M0, R, M, meta = construct(D, c, r)
    N, k, b = meta['N'], meta['k'], meta['b']
    producer = build.completion(D, c, r)
    require(producer['family'] == family, 'Closed/literal geometry differs')
    require(build.dense_entries(producer, 'raw') == M0
            and build.dense_entries(producer, 'repair') == R
            and build.dense_entries(producer) == M,
            'Complete raw/repair/final oracle replay differs')
    star = [i for i, a in enumerate(family) if a >> c & 1]
    outside = [i for i in range(N) if i not in star]
    one = [1] * N
    q = [b if i in star else -k for i in range(N)]
    def mv(A, v):
        return [sum(x * z for x, z in zip(row, v)) for row in A]
    require(sum(q) == 0, 'Wrong forced-star constant')
    for A in (M0, M):
        require(mv(A, one) == one and mv(A, q) == [-F(k, b) * x for x in q],
                'Base/final endpoints failed')
    require(mv(R, one) == mv(R, q) == [0] * N, 'Repair changes endpoint lines')
    require(max(sum(abs(x) for x in row) for row in R) <= meta['Rbound'], 'Repair norm bound failed')
    PZ = [[F(i == j) - (F(1, k) if i in star and j in star else 0)
           - (F(1, b) if i in outside and j in outside else 0)
           for j in range(N)] for i in range(N)]
    X = [[M0[i][j] for j in outside] for i in star]
    old_E = [j for j, index in enumerate(outside) if family[index] in D]
    new_P = [j for j in range(b) if j not in old_E]
    require(len(old_E) == meta['t'] and len(new_P) == meta['r'],
            'Outside split dimensions differ')
    Y = [[F(0)] * b for _ in range(b)]
    for i in old_E:
        for j in new_P:
            Y[i][j] = Y[j][i] = F(1, meta['r'])
    for i in new_P:
        for j in new_P:
            if i != j:
                Y[i][j] = meta['y']
    require(all(sum(row) == 1 for row in Y), 'Outside stochasticity failed')
    require(all(M0[outside[i]][outside[j]] == meta['mu'] * Y[i][j]
                for i in range(b) for j in range(b)), 'Outside base block differs')
    Q = [[F(k*(i==j)) + meta['delta']*Y[i][j]
          - F(b*b,k)*sum(X[z][i]*X[z][j] for z in range(k))
          for j in range(b)] for i in range(b)]
    PE = [[F(i==j and i in old_E) - F(int(i in old_E and j in old_E), meta['t'])
           for j in range(b)] for i in range(b)]
    PP = [[F(i==j and i in new_P) - F(int(i in new_P and j in new_P), meta['r'])
           for j in range(b)] for i in range(b)]
    z = [F(1,meta['t']) if i in old_E else -F(1,meta['r']) for i in range(b)]
    psi = k - meta['delta']*meta['y'] - (b*meta['w'])**2/k
    coefficient = F(k*meta['t']*(meta['r']-meta['t']),meta['r'])
    literal_image = [[k*PE[i][j]+psi*PP[i][j]+coefficient*z[i]*z[j]
                      for j in range(b)] for i in range(b)]
    require(Q == literal_image, 'Complete Schur image decomposition differs')
    require(psi >= F(2,3) and coefficient*sum(x*x for x in z) >= 1,
            'Schur contrast quantitative bounds failed')
    require(psd_ldl(Q) == b-1, 'Complete Schur rank differs')
    psd_ldl([[Q[i][j]-F(2,3)*(F(i==j)-F(1,b))
              for j in range(b)] for i in range(b)])
    for matrix, lower_gap, upper_gap in ((M0, F(2,15), meta['upper_gap']),
                                        (M, F(1,15), meta['upper_gap']/2)):
        require(check(family, matrix, k, upper=True) == N - 1, 'Whole lower rank differs')
        require(psd_ldl([[F(i == j)-matrix[i][j] for j in range(N)] for i in range(N)])
                == N - 1, 'Whole upper rank differs')
        psd_ldl([[b*matrix[i][j]+F(k*(i==j))-lower_gap*PZ[i][j]
                  for j in range(N)] for i in range(N)])
        psd_ldl([[F(i==j)-matrix[i][j]-upper_gap*PZ[i][j]
                  for j in range(N)] for i in range(N)])
    require(min(M[0][1:]) >= meta['epsilon'], 'Empty margin failed')
    if meta['delta']:
        require(all(M[i][j] >= 0 for i in range(1,N) for j in range(i+1,N)),
                'Strict-surplus nonempty sign failed')
    record={key:(str(value) if isinstance(value,F) else value) for key,value in meta.items()}
    record.update(center=c, original_family=D, lower_rank=N-1, upper_rank=N-1,
        empty_margin=str(min(M[0][1:])),
        negative_nonempty_edges=sum(M[i][j]<0 for i in range(1,N) for j in range(i+1,N)),
        complete_raw_repair_final_entry_replays=3*N*N, complete_Schur_entries=b*b,
        full_Schur_image_and_buffer=True, full_raw_repaired_buffered_LDL=True,
        matrix_sha256=sha256(json.dumps([[str(x) for x in row] for row in M],
                                      separators=(',',':')).encode()).hexdigest())
    return record


def labeled_three_point_downsets():
    families=[]
    for mask in range(1<<8):
        D=[a for a in range(8) if mask>>a&1]
        if len(D)<2 or 0 not in D: continue
        present=set(D)
        if all(b in present for a in D for b in range(8) if b&a==b):
            families.append(D)
    require(len(families)==18, 'Complete labeled input count differs')
    return families


def rejection_controls():
    functions=[lambda:build.completion([0,1],0,1),
               lambda:build.completion(list(range(8)),0,4),
               lambda:build.completion([0,1],0,True),
               lambda:build.completion([0,1],0,2.0),
               lambda:build.completion([0,1,2],1,-1),
               lambda:build.completion([0,1,3,4],0),
               lambda:build.completion(list(range(4)),2),
               lambda:build.completion([0,1,2],True)]
    good=build.completion([0,1],0)
    functions.extend([lambda:good['entry'](0,32),lambda:good['entry'](0,True),
                      lambda:build.dense_entries(good,'unknown'),
                      lambda:build.dense_entries(good,limit=2)])
    for f in functions:
        try:f()
        except ValueError:pass
        else:raise ValueError('Invalid linear-recipe input accepted')
    return len(functions)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true')
    args=parser.parse_args();records=[]
    for D in labeled_three_point_downsets():
        s=max(sum(bool(a>>c&1) for a in D) for c in range(3))
        for c in range(3):
            if sum(bool(a>>c&1) for a in D)==s:
                records.append(audit(D,c))
    require(len(records)==33,'Complete maximum-center choice count differs')
    extra=[]
    for E0,E1 in [([0,1,2,4,5],[0,2,4]),
                  ([a for a in range(16) if a.bit_count()<=2],[0,1,2,4,8])]:
        D=sorted([a<<1 for a in E0]+[(a<<1)|1 for a in E1])
        extra.append(audit(D,0))
    # Counts above the threshold and a center relabeling with inactive holes.
    extra.append(audit([0,1,2,3,4,5],0,5))
    extra.append(audit([0,1,8,16,17,24],4,6))
    result=dict(agent='six-downset-1',role='researcher',
        theorem_scope='exact finite implementation checks for separate ordinary all-order proof',
        complete_labeled_three_point_D=18,maximum_center_choices=33,
        rejected_controls=rejection_controls(),records=records,extra=extra)
    result['canonical_sha256']=sha256(json.dumps(result,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    if args.check:
        expected=json.loads(Path(__file__).with_name('linear_pendant_expected.json').read_text())
        require(result==expected,'Whole linear-count output differs from frozen fixture')
    print(json.dumps(result,sort_keys=True,indent=2))


if __name__=='__main__':main()
