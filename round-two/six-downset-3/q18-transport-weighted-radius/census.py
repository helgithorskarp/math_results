"""NEW exact original-entry floor census for the public q18 witness.

Actual six-downset-3 / researcher. Canonical mask/orbit/anchor formula is
openly reused from our public87c1 q18 reader. Only defining candidate DATA
are read; no published or private EXPECTED record, producer or PSD factor
is imported. This is an author census; real bridges are separate.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import hashlib
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def original():
    p = Path(__file__).resolve().parent.parent/'q18-schur-weight-radius'/'CANDIDATE.json'
    raw = p.read_bytes()
    require(hashlib.sha256(raw).hexdigest() ==
            'fae303f40a542478e22083289ea982cd1814b58323f4e13d237d7269583ab16e',
            'attributed whole candidate DATA')
    data = json.loads(raw); D = data['denominator']
    require(D == 2**32 and len(data['free_numerators']) == 143,
            'named exact defining coefficient domain')
    X = []
    for rank in (1, 2, 3):
        for points in combinations(range(21), rank):
            mask = sum(1 << point for point in points)
            if rank == 3 and ((mask & 7).bit_count() < 2 or
                              ((mask & 7) == 6 and mask & (511 << 3))):
                continue
            X.append(mask)
    X.sort()
    label = {mask: (mask & 7, ((mask >> 3) & 511).bit_count(),
                    (mask >> 12).bit_count()) for mask in X}
    S = [mask for mask in X if mask & 1]
    B = [mask for mask in X if label[mask] in {(0, 2, 0), (0, 0, 2), (6, 0, 1)}]
    require((len(X), len(S), len(B)) == (277, 58, 81), 'original dimensions')
    keys = sorted({tuple(sorted((label[m], label[n])))
                   for i, m in enumerate(X) for n in X[i+1:]
                   if m != 1 and n != 1 and not (m & n)})
    require(len(keys) == 143, 'original complete canonical coefficient order')
    table = dict(zip(keys, data['free_numerators']))

    def entry(m, n):
        if m == n:
            return 57*D
        if m & n:
            return -D
        if m == 1:
            return -sum(entry(s, n) for s in S if s != 1)
        if n == 1:
            return entry(n, m)
        return table[tuple(sorted((label[m], label[n])))]

    A = [[entry(s, b) for b in B] for s in S]
    require(all(sum(row[j] for row in A) == 0 for j in range(81)),
            'ALL81 whole original column kernels')
    v = [sum(row) for row in A]
    P = [i for i, value in enumerate(v) if value > 0]
    N = [i for i, value in enumerate(v) if value < 0]
    require(len(P) == 20 and len(N) == 38 and sum(v) == 0,
            'whole original signed partition')
    return S, B, label, A, v, P, N, D


def check():
    S, B, label, A, v, P, N, D = original()
    pure = [j for j, b in enumerate(B) if label[b] in {(0, 2, 0), (0, 0, 2)}]
    triples = [j for j, b in enumerate(B) if label[b] == (6, 0, 1)]
    positions = [(i, j) for i in P for j in pure if not (S[i] & B[j])]
    require(len(positions) == 1296 and len(triples) == 9, 'literal clipping domain')
    require(all(A[i][j] == -D for i in N for j in triples),
            'ALL342 fixed negative-group triple entries')
    require(all(sum(A[i][j] for i in P) == 38*D for j in triples),
            'ALL9 whole triple positive-group sums')
    margins = [F(A[i][j]+D, D) for i, j in positions]
    require(min(margins) >= F(1, 256), 'whole relevant original entry margins licence')
    levels = Counter(margins)
    by_type = defaultdict(Counter)
    for (i, j), margin in zip(positions, margins):
        by_type[(label[S[i]], label[B[j]])][margin] += 1
    V = F(sum(v[i] for i in P), D)
    require(V == F(2912214312567, 1073741824), 'same witness group sum')
    cap = F(4998177, 1024)  # Credited comparison theorem scalar, not a PSD factor.

    def mass(e, tau=F(0)):
        return V-sum(min(220*e, margin-tau) for margin in margins)

    samples = []
    for e in (F(1, 363), F(1, 362), F(1, 350), F(1, 320), F(1, 300), F(1, 280)):
        T = mass(e)
        samples.append({'e': str(e), 'floor_clipped_P_mass_lower_at_tau0': str(T),
                        'active_original_positions': sum(margin < 220*e for margin in margins),
                        'necessary_gap_if_mass_nonnegative': str(max(F(0), (T*T/760-cap)/2))
                        if T >= 0 else None})
    return {'actual_agent': 'six-downset-3', 'role': 'researcher',
            'status': 'PRIVATE exact author floor census; full-real/refined-radius bridge unpaid',
            'defining_witness_source_commit': '87c1eba73573ab49ed9131f6496c6703ce03fd1e',
            'complete_original_allowed_P_pure_pair_position_count': len(positions),
            'all_original_entry_coordinates': [{'star_mask': S[i], 'bad_mask': B[j],
                                               'C_dagger_numerator': A[i][j]}
                                              for i, j in positions],
            'denominator': D, 'positive_group_sum': str(V), 'credited_old_BB_cap': str(cap),
            'margin_levels': [{'margin_at_tau0': str(m), 'original_count': levels[m],
                               'first_radius_at_tau0': str(m/220)} for m in sorted(levels)],
            'literal_type_census': [{'star_type': list(st), 'bad_type': list(bt),
                                    'levels': [{'margin': str(m), 'count': count}
                                               for m, count in sorted(counts.items())]}
                                   for (st, bt), counts in sorted(by_type.items())],
            'exact_samples_not_an_entire_real_interval_proof': samples,
            'original_NS_matrix_or_best_distance_or_general_H_I_claimed': False,
            'independent_review_claimed': False}


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
