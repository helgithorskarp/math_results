"""Independent collision-set equivalence and malformed-certificate controls."""
from itertools import combinations
import json
import contacts_audit as V
import audit as A

H, M = V.factors()
differences = []
for points in (H, M):
    values = set()
    for i, j in V.unit_edges(points, 42):
        x = A.sub(points[i], points[j])
        values.add(x); values.add(A.scale(x, -1))
    differences.append(values)
U, W = differences
roots = (A.sub(A.OMEGA, A.O), A.scale(A.OMEGA, -1))
for eta in roots:
    assert A.norm(eta) == A.O
    assert A.norm(A.add(A.O, eta)) == A.O
    assert {A.mul(eta, a) for a in U} == U
collision = set()
contact = set()
event_checks = 0
for a in U:
    for b in W:
        quotient = V.canonical(A.mul(a, A.conjugate(b)), 42**2)
        collision.add(quotient)
        for eta in roots:
            r = V.multiply((eta, 1), quotient)
            contact.add(r)
            rn, rd = r
            combined = A.add(A.scale(a, rd), A.mul(rn, b))
            assert A.norm(combined) == A.scale(A.O, (42*rd)**2)
            event_checks += 1
assert collision == contact and len(contact) == 252
assert A.norm(A.add(A.O, A.O)) == A.scale(A.O, 4)
rejected = 0
for row, d in [(A.O[:-1], 1), (A.O, 0), (A.O, -1), ((0.5,)+A.O[1:], 1)]:
    try:
        V.canonical(row, d)
    except AssertionError:
        rejected += 1
assert rejected == 4
for a in (A.O, A.S, A.zp(3), A.add(A.OMEGA, A.W)):
    assert V.canonical(A.scale(a, 42), 126) == V.canonical(a, 3)
assert V.canonical(A.Z, 42) == (A.Z, 1)
print(json.dumps({'status': 'UNIT-CONTACT AND COLLISION-SET CONTROLS PASSED',
    'independent_unit_H_differences': len(U), 'independent_unit_M_differences': len(W),
    'mu3_actions_checked': 2, 'contact_events_checked_by_norm': event_checks,
    'unit_difference_collision_rotations': len(collision),
    'contact_and_unit_collision_sets_equal': True,
    'invalid_rational_rows_rejected': rejected, 'rational_normalization_controls': 5,
    'wrong_contact_angle_rejected': True}, indent=2))
