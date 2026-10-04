"""Whole original 23-orbit coefficient identities for a constant two-plane dual.

Input is the explicit original disjointness table, not a Schur residual,
stationary vector, saved generated polynomial, or prior spectral theorem.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse
import hashlib
import json
import sys

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))
import sourcecheck
SOURCE = sourcecheck.check_bundle(BASE)
import polynomial as p


def require(value, message):
    if not value:
        raise ValueError(message)


def cleared_table(q):
    c, a, m, t = p.constant, p.add, p.mul, p.scale
    s = a(t(q, 3), c(4))
    qm1, qm2, qm3, hp = a(q, c(-1)), a(q, c(-2)), a(q, c(-3)), a(t(q, 3), c(5))
    P = t(m(q, qm1, qm2, qm3, hp), 4)
    out = {}

    def put(x, y, bn, bd=p.ONE, dn=(), dd=p.ONE):
        out[tuple(sorted((x, y)))] = (p.divide(m(P, bn), bd), p.divide(m(P, dn), dd))

    o, oo, co, cx, cc, ccx, ccc = (0, 1), (0, 2), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0)
    put(o, o, a(c(6), t(m(q, q), -1), t(q, -4)), m(q, qm1), p.ONE, qm1)
    put(o, oo, m(q, qm3), m(qm1, qm2))
    pp = a(t(qm1, 12), t(m(q, q), 4), t(m(s, q, qm1), -2), m(q, q, qm1, qm1))
    put(oo, oo, pp, m(q, qm1, qm2, qm3),
        t(a(m(q, qm1, hp), t(a(q, c(1)), -6)), 2), m(q, qm1, qm2, qm3, hp))
    for leaf in (o, oo):
        if leaf == o:
            alpha = (qm1, q, (), p.ONE)
            beta = (a(q, c(1)), q, (), p.ONE)
            gamma = (a(q, c(6)), q, (), p.ONE)
        else:
            alpha = (p.ONE, p.ONE, c(2), m(hp, q, qm1))
            beta = (a(m(q, qm2), t(qm1, 2)), m(q, qm2), c(2), m(hp, qm1, qm2))
            gamma = (a(q, c(6)), q, t(a(q, c(1)), -6), m(hp, q, qm1))
        for core, values in ((co, alpha), (cc, alpha), (cx, beta), (ccx, beta), (ccc, gamma)):
            put(leaf, core, *values)
    rr = a(t(q, 3), c(2))
    ww = a(t(m(q, q), 3), q, c(-2))
    for x, y, num, den in ((co, co, (), p.ONE), (co, cx, (), p.ONE),
                          (cx, cx, (), p.ONE), (co, cc, c(2), p.ONE),
                          (co, ccx, rr, q), (cx, cc, rr, q), (cx, ccx, ww, m(q, qm1))):
        put(x, y, num, den)
    require(all(len(poly) <= 6 for pair in out.values() for poly in pair),
            'EVERY cleared original table coefficient has degree at most five')
    return P, out


def values(key):
    core, z, w = key
    outside = z+w
    low = (F(0) if core in (0, 6) or outside == 0 and core in (1, 3, 5) else
           F(1) if outside == 0 and core in (2, 4) else
           F(1, 2) if core in (1, 7) else F(3, 4) if core in (2, 4) else F(-1, 4))
    cap = F(1) if outside == 0 and core in (2, 4) else F(2)
    orientation = F(1) if core == 0 else F(-1) if core == 7 else F(0)
    return low, cap, orientation


def generated():
    c, a, m, t = p.constant, p.add, p.mul, p.scale
    k, q = p.K, t(p.K, 2)
    N, s = a(t(m(k, k), 2), t(k, 12), c(8)), a(t(k, 6), c(4))
    P, tab = cleared_table(q)
    keys = sorted((core, z, w) for core in range(8) for z in range(3) for w in range(3)
                  if (1 <= core.bit_count()+z+w <= 2 or
                      core.bit_count()+z+w == 3 and core.bit_count() >= 2)
                  and (core, z, w) != (6, 1, 0))
    masses = [m(p.choose(k, z), p.choose(k, w)) for core, z, w in keys]
    require(len(keys) == 23 and a(*masses) == a(N, c(-1)), 'ENTIRE physical orbit census')
    names = ('C0', 'Delta', 'Rb', 'Rc', 'B', 'U0')
    forms = {name: [[() for _ in keys] for _ in keys] for name in names}
    repairs = {'Rb': {(1, 2): 1, (2, 5): -1}, 'Rc': {(1, 4): 1, (3, 4): -1}, 'B': {(2, 4): 1}}
    for i, (co, z, w) in enumerate(keys):
        for j, (cc, zz, ww) in enumerate(keys):
            count = () if co & cc else m(p.choose(a(k, c(-z)), zz), p.choose(a(k, c(-w)), ww))
            reverse = () if co & cc else m(p.choose(a(k, c(-zz)), z), p.choose(a(k, c(-ww)), w))
            require(m(masses[i], count) == m(masses[j], reverse), 'EVERY physical disjoint-pair reciprocity identity')
            bn, dn = tab[tuple(sorted(((co.bit_count(), z+w), (cc.bit_count(), zz+ww))))] if count else ((), ())
            C0 = a(t(m(P, s, masses[i]), int(i == j)), t(m(P, masses[i], masses[j]), -1), m(masses[i], count, bn))
            forms['C0'][i][j] = C0
            forms['Delta'][i][j] = m(masses[i], count, dn)
            forms['U0'][i][j] = a(t(m(P, N, masses[i]), int(i == j)), t(m(P, masses[i], masses[j]), -1), t(C0, -1))
            for name, edges in repairs.items():
                forms[name][i][j] = t(P, edges.get(tuple(sorted((co, cc))), 0)) if z+w+zz+ww == 0 else ()
    require(all(G[i][j] == G[j][i] for G in forms.values() for i in range(23) for j in range(23)),
            'ALL six complete original forms symmetric coefficient by coefficient')
    require(all(len(poly) <= 10 for G in forms.values() for row in G for poly in row),
            'ALL cleared original Gram entries degree at most nine')
    low, cap, zz = (list(x) for x in zip(*(values(key) for key in keys)))

    def energy(name, x):
        return a(*(t(forms[name][i][j], x[i]*x[j]) for i in range(23) for j in range(23)))

    planes = [energy('C0', low)] + [energy(name, low) for name in names[1:5]], [energy('U0', cap)] + [t(energy(name, cap), -1) for name in names[1:5]]
    total = [a(planes[0][i], planes[1][i]) for i in range(5)]
    A = (F(121, 4), F(55), F(-8))
    Bn = tuple(map(F, (4, 36, 64, 48)))
    h = a(t(k, 6), c(5))
    alpha_num = a(m(a(t(m(k, k), 2), k), h), t(a(t(k, 2), c(1)), 3))
    require(total[0] == m(P, A), 'EVERY coefficient of the complete constant-energy identity')
    require(m(total[1], h) == t(m(P, Bn), -1), 'EVERY coefficient of the complete kappa-energy identity')
    require(total[2:] == [(), (), ()], 'both independent trades and sigma cancel individually')
    require(planes[0][1:4] == [(), (), ()] and planes[1][2:4] == [(), ()],
            'lower slope and every endpoint trade vanish separately')
    require(planes[0][4] == t(P, 2) and planes[1][4] == t(P, -2), 'original sigma energies exactly 2 and minus 2')
    require(all(not energy(name, zz) for name in ('C0', 'Rb', 'Rc', 'B')),
            'ALL original constant/repair orientation energies zero')
    require(m(energy('Delta', zz), h) == m(P, alpha_num), 'ENTIRE original positive orientation identity')
    require(p.shift(A, 8) == tuple(map(F, (F(-167, 4), -73, -8))), 'whole strict negative shift k8')
    require(all(value > 0 for value in Bn) and all(value > 0 for value in alpha_num), 'entire positive slope/orientation coefficient lists')
    receipt = {'actual_agent': 'six-downset-3', 'role': 'researcher',
               'domain': 'ALL integers k>=8, q=2k, EVERY deletion set Z of size k',
               'coefficient_field': 'QQ[k], dense coefficients ascending in k',
               'keys': keys, 'masses': [p.record(x) for x in masses], 'clearing': p.record(P),
               'complete_cleared_original_forms': {name: [[p.record(x) for x in row] for row in G] for name, G in forms.items()},
               'physical_vectors': {'lower': list(map(str, low)), 'cap': list(map(str, cap)), 'orientation': list(map(str, zz))},
               'complete_cleared_affine_planes': [[p.record(x) for x in plane] for plane in planes],
               'complete_cleared_combined_plane': [p.record(x) for x in total],
               'A': p.record(A), 'A_shift8': p.record(p.shift(A, 8)), 'negative_kappa_numerator': p.record(Bn),
               'slope_and_orientation_denominator': p.record(h), 'orientation_numerator': p.record(alpha_num),
               'whole_form_positions': 6*23*23, 'all_original_coefficient_identities_checked': True,
               'ordinary_original_decoding_and_empty_lift_unformalized': True, 'independent_person_review': False,
               'old_q_ge_3k_criterion_not_used': True, 'CAS_or_solver_imported': False}
    return receipt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True, type=Path)
    args = ap.parse_args()
    result = generated()
    args.out.write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    print(json.dumps({'completed': True, 'whole_form_positions': result['whole_form_positions'],
                      'A': result['A'], 'A_shift8': result['A_shift8'],
                      'negative_kappa_numerator': result['negative_kappa_numerator'],
                      'whole_record_SHA256': hashlib.sha256(args.out.read_bytes()).hexdigest()}))


if __name__ == '__main__':
    main()
