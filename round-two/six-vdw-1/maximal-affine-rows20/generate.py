"""Complete local one-coefficient extension catalogue of the chosen row cube."""
import argparse
from collections import Counter
import json
from pathlib import Path


def run():
    direction = sorted({(1023 if code & 1 else 0) ^ (62 if code & 2 else 0) ^
                        (124 if code & 4 else 0) ^ (60 if code & 8 else 0) for code in range(16)})
    rows = sorted(72 ^ h for h in direction)
    bad = {}
    good = set()
    for mask in range(1024):
        word = [((mask >> (s % 10)) & 1) ^ int(s >= 10) for s in range(20)]
        failure = None
        for start in range(20):
            for step in range(1, 20):
                points = [(start + j * step) % 20 for j in range(7)]
                if len({word[x] for x in points}) == 1:
                    failure = {'mask': mask, 'start': start, 'step': step,
                               'points': points, 'color': word[points[0]]}
                    break
            if failure is not None:
                break
        if failure is None:
            good.add(mask)
        else:
            bad[mask] = failure
    representatives = sorted({min(delta ^ h for h in direction) for delta in range(1024)})
    entries = []
    for delta in representatives:
        shifted = sorted(mask ^ delta for mask in rows)
        invalid = sorted(set(shifted) - good)
        entries.append({'representative': delta, 'shifted_coset_valid_rows': len(set(shifted) & good),
                        'locally_complete': not invalid,
                        'first_bad_row_AP': bad[invalid[0]] if invalid else None})
    proper = [e['representative'] for e in entries if e['representative'] != 0 and e['locally_complete']]
    return {'author': 'six-vdw-1', 'role': 'researcher', 'status': 'PROPOSED_COMPLETE_LOCAL_AFFINE_EXTENSIONS',
            'base_mask': 72, 'direction_space': direction, 'cube_rows': rows,
            'raw_differences_covered': 1024, 'cosets': len(entries), 'proper_extension_candidates': len(entries) - 1,
            'all_admissible_antiperiodic_rows': len(good), 'proper_locally_admissible_extensions': proper,
            'valid_rows_per_coset_histogram': dict(sorted(Counter(e['shifted_coset_valid_rows'] for e in entries).items())),
            'entries': entries,
            'scope': 'Every one-bit affine extension of this chosen16-row cube in the10-bit lower-row space; no field/interval existence or exclusion.'}


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('output', type=Path); a = p.parse_args(); value = run()
    a.output.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')
    print(json.dumps({k: v for k, v in value.items() if k != 'entries'}, sort_keys=True), flush=True)
