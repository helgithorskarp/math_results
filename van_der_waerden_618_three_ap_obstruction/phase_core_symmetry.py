"""Exact support stabilizer, phase-domain orbit, and CRT color identity checks."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import resource
import time


def analyze(allowed):
    began = time.monotonic()
    allowed = {int(r): tuple(p) for r, p in allowed.items()}
    support = set(allowed)
    assert support and all(0 <= r < 103 for r in support)
    assert all(p and len(set(p)) == len(p) and all(0 <= x < 6 for x in p) for p in allowed.values())
    supports = set()
    stabilizer = []
    for a in range(1, 103):
        for b in range(103):
            image = tuple(sorted((a * r + b) % 103 for r in support))
            supports.add(image)
            if set(image) == support:
                stabilizer.append([a, b])
    # For this explicit support, no nontrivial affine map fixes it.
    assert stabilizer == [[1, 0]] and len(supports) == 10506
    # Independently bound the candidate maps by the images of two anchors.
    # Any stabilizer sends this ordered pair into S x S with distinct images.
    anchors = sorted(support)[:2]
    inverse_difference = pow(anchors[1] - anchors[0], -1, 103)
    anchor_candidates = set()
    for u in support:
        for v in support - {u}:
            a = (v - u) * inverse_difference % 103
            b = (u - a * anchors[0]) % 103
            if {(a * r + b) % 103 for r in support} == support:
                anchor_candidates.add((a, b))
    assert anchor_candidates == {tuple(pair) for pair in stabilizer}
    phase_variants = set()
    phase_stabilizer = []
    original = tuple((r, tuple(sorted(p))) for r, p in sorted(allowed.items()))
    for eps in [1, -1]:
        for k in range(6):
            image = tuple((r, tuple(sorted((eps * p + k) % 6 for p in permitted)))
                          for r, permitted in sorted(allowed.items()))
            phase_variants.add(image)
            if image == original:
                phase_stabilizer.append([eps, k])
    identity_cases = 0
    for eps in [1, -1]:
        for e in range(6):
            for p in range(6):
                transformed = (p - e) % 6 if eps == 1 else (e - p - 2) % 6
                for y in range(6):
                    assert int((eps * y + e - p) % 6 >= 3) == int((y - transformed) % 6 >= 3)
                    identity_cases += 1
    # CRT gives exactly the units of Z618, with residues (a,eps) in F103 x Z6.
    multipliers = set()
    for a in range(1, 103):
        for eps in [1, -1]:
            m = next(t for t in range(a, 618, 103) if t % 6 == eps % 6)
            assert pow(m, -1, 618) * m % 618 == 1
            multipliers.add(m)
    assert len(multipliers) == 204
    assert all((617 + 6 * min(d, 618 - d) + 1) <= 2472 for d in range(1, 618))
    family_size = 6 ** (103 - len(support))
    for permitted in allowed.values():
        family_size *= len(permitted)
    digest = hashlib.sha256()
    generated = 0
    for a in range(1, 103):
        for b in range(103):
            for phase_pattern in sorted(phase_variants):
                image = sorted(((a * r + b) % 103, permitted) for r, permitted in phase_pattern)
                digest.update((json.dumps(image, separators=(',', ':')) + '\n').encode())
                generated += 1
    assert generated == len(supports) * len(phase_variants) <= 200000
    result = {'status': 'EXACT_AFFINE_SUPPORT_AND_PHASE_DOMAIN_ORBIT_VERIFIED',
        'support_size': len(support), 'affine_parameters': 10506, 'affine_support_stabilizer': stabilizer,
        'distinct_affine_supports': len(supports), 'phase_domain_stabilizer': phase_stabilizer,
        'independent_anchor_stabilizer_candidates': len(support) * (len(support) - 1),
        'independent_anchor_stabilizer': sorted(anchor_candidates),
        'distinct_phase_domain_variants': len(phase_variants), 'distinct_transformed_domains': generated,
        'canonical_orbit_stream_sha256': digest.hexdigest(), 'six_state_color_identity_cases': identity_cases,
        'CRT_unit_multipliers_checked': len(multipliers), 'transformed_AP_prefix_bound': 2472,
        'each_excluded_phase_family_size': family_size, 'union_size_not_claimed': True,
        'seconds': time.monotonic() - began, 'maxrss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    assert result['seconds'] < 30
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('checked_certificate', type=Path)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    assert not args.output.exists()
    data = json.loads(args.checked_certificate.read_text())
    assert data['status'] == 'INTEGER_AP_PREMISES_AND_COMPACT_RUP_INDEPENDENTLY_VERIFIED'
    result = analyze(data['allowed_phase_sets'])
    result.update(agent='six-vdw-1', role='researcher', checked_at=datetime.now(timezone.utc).isoformat(),
                  checked_certificate_sha256=hashlib.sha256(args.checked_certificate.read_bytes()).hexdigest(),
                  no_new_W_bound=True, source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
