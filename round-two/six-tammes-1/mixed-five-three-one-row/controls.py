"""Hand-checkable partial incidences and the decisive predicate release."""
from pathlib import Path
import json
from check import all_covers, digest, evaluate, need
from patch import A, F, I, R, S, U, V, Z, Bad, Patch
from audit import DartAudit, Reject, evaluate as audit_evaluate


def build_report():
    tests = [
        ('triangle', [(I, R, S)], [], True),
        ('triangle-from-three-bars', [], [(I, R), (I, S), (R, S)], True),
        ('two-T-path', [(I, R, S), (I, S, 11)], [], True),
        ('repeated-face', [(I, R, R)], [], False),
        ('ordinary-opposite-five', [(F, I, R, S)], [], False),
        ('quad-contact-diagonal', [(I, R, 11, S)], [(I, 11)], False),
        ('short-closed-link', [(I, R, 12, S), (I, S, 13, 11), (I, 11, 14, R)], [], False),
        ('three-QQ-ends-at-oneT', [], [(A, U), (A, V), (A, Z)], False),
    ]
    tested = []
    for name, faces, extra, expected in tests:
        a, b = evaluate(Patch(faces, extra)), audit_evaluate(DartAudit(faces, extra))
        need(a == b == expected, ('control', name, a, b, expected))
        tested.append([name, a, b])
    # A deliberately weaker necessary system. Its two survivors are not packings.
    x = all_covers(evaluate, missing_capacity=False)
    y = all_covers(audit_evaluate, patch_type=DartAudit, missing_capacity=False)
    need(x == y, 'released predicate complete-case comparison')
    need(x['admitted']['separated'] == 2, 'released missing-star capacity control')
    return {'partial_incidence_controls': tested, 'released_missing_star_T_capacity': x}


def main():
    x = build_report()
    expected = json.loads(Path(__file__).with_name('CONTROLS_EXPECTED.json').read_text())
    need(x == expected, 'control output mismatch')
    print(json.dumps(x, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
