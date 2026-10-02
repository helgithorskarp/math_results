"""Positive partial incidences, damaged inputs, and two geometric bridges."""
from pathlib import Path
import json

from check import evaluate, need
from patch import A, B, C, D, E, F, H, I, R, S, U, V, Bad, Patch
from audit import DartAudit, Reject, evaluate as audit_evaluate


def build_report():
    fixtures = [
        ('triangle', [(I, R, S)], [], True),
        ('triangle-from-three-bars', [], [(I, R), (I, S), (R, S)], True),
        ('two-T-path', [(I, R, S), (I, S, C)], [], True),
        ('repeated-face', [(I, R, R)], [], False),
        ('ordinary-opposite-five', [(F, I, R, S)], [], False),
        ('quad-contact-diagonal', [(I, R, 12, S)], [(I, 12)], False),
        ('short-closed-link', [(D, I, R), (D, R, S), (D, S, A), (D, A, E, I)], [], False),
        ('three-QQ-ends-at-oneT', [(A, I, E, U), (A, I, H, R)], [(A, V)], False),
        ('ordinary-three-contact', [], [(I, U)], False),
    ]
    checked = []
    for name, faces, bars, expected in fixtures:
        a = evaluate(Patch(faces, bars)) is not None
        b = audit_evaluate(DartAudit(faces, bars)) is not None
        need(a == b == expected, ('fixture', name, a, b))
        checked.append([name, a, b])
    # A has known link path I-U-V and still needs one T. I's two Ts
    # are full, while V has no T. Releasing this rule admits the patch.
    faces = [(I, R, S), (I, S, C), (A, I, C, U), (A, U, E, V)]
    releases = []
    for flag in (False, True):
        outcomes = []
        for cls, error, method in ((Patch, Bad, 'evaluate'), (DartAudit, Reject, 'inspect')):
            try:
                getattr(cls(faces, missing_capacity=flag), method)(False)
                good = True
            except error:
                good = False
            outcomes.append(good)
        need(outcomes == [not flag, not flag], 'missing-star capacity release')
        releases.append([flag, outcomes])
    # This accepted paired-fan patch is not asserted to be a packing.
    # Each listed missing Q sector has no possible actual original opposite.
    faces = [(F, I, D), (F, D, R), (F, R, S), (F, S, 12), (D, I, A),
             (F, I, B, 12), (D, A, E, V), (D, V, H, R),
             (I, A, U, B), (R, S, C, H)]
    bars = [(U, x) for x in (A, B, C)] + [(V, x) for x in (D, E, H)]
    p, q = Patch(faces, bars, fd_contact=True), DartAudit(faces, bars, fd_contact=True)
    need(evaluate(p) is not None and audit_evaluate(q) is not None, 'three-star positive prefix')
    sectors = []
    for v, a, b in ((U, A, C), (U, B, C), (V, E, H)):
        states = []
        for x in range(15):
            left = evaluate(p.plus((v, a, x, b))) is not None
            right = audit_evaluate(q.plus((v, a, x, b))) is not None
            need(left == right == False, ('original opposite control', v, a, b, x))
            states.append([x, left, right])
        sectors.append([v, a, b, states])
    return {'partial_incidence_controls': checked,
            'missing_star_T_capacity_release': releases,
            'three_star_positive_prefix': True, 'all_original_opposite_controls': sectors}


def main():
    report = build_report()
    expected = json.loads(Path(__file__).with_name('CONTROLS_EXPECTED.json').read_text())
    need(report == expected, 'complete control output mismatch')
    print(json.dumps(report, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
