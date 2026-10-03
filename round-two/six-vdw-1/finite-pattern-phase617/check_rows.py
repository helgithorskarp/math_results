"""Independent literal same-phase AP classification of all256 rows/phase."""
import hashlib
import json
from pathlib import Path
import struct


def need(ok, message):
    if not ok:
        raise ValueError(message)


def check(record):
    need(record['schema'] == 'LITERAL_SAME_PHASE6_THREE_CHARACTER_ROW_CERTIFICATE_V1'
         and record['q'] == 617 and record['N'] == 3704 and record['roots'] == [0, 1, 4]
         and record['phase_period'] == 6, 'chosen actual same-phase original family')
    signs = {r: sum((j*r) % 617 > 308 for j in range(1, 309)) % 2 for r in range(1, 617)}
    keys = []
    for n in range(3704):
        r = n % 617
        keys.append(None if r in (0, 1, 4) else
                    signs[r]*4+signs[(r-1) % 617]*2+signs[(r-4) % 617])
    survivors = sorted({sum(((k >> bit) & 1)*2**k for k in range(8)) ^ complement
                        for bit in range(3) for complement in (0, 255)})
    need(survivors == [15, 51, 85, 170, 204, 240], 'all three actual projection truth tables and complements')
    rows = record['all256_table_obstruction_APs_by_phase']
    need(len(rows) == 6 and all(len(row) == 256 for row in rows), 'entire six times256 original truth tables')
    witnesses = set()
    max_endpoint = max_step = checked = 0
    for phase, row in enumerate(rows):
        for table, AP in enumerate(row):
            if table in survivors:
                need(AP is None, 'actual surviving projection rows are positive controls')
                continue
            need(type(AP) is list and len(AP) == 2, 'every actual nonprojection table has a literal obstruction')
            a, d = AP
            need(type(a) is int and type(d) is int and a >= 0 and d > 0 and a+6*d < 3704,
                 'actual nonconstant row AP belongs to original finite interval')
            need(a % 6 == phase and d % 6 == 0, 'every actual row AP has its declared original phase')
            ns = [a+j*d for j in range(7)]
            actual_keys = [keys[n] for n in ns]
            need(None not in actual_keys, 'actual row obstruction avoids every original root occurrence')
            actual_colors = [(table >> key) & 1 for key in actual_keys]
            need(len(set(actual_colors)) == 1, 'actual seven-point obstruction is monochromatic for its whole truth table')
            witnesses.add((a, d))
            max_endpoint = max(max_endpoint, a+6*d)
            max_step = max(max_step, d)
            checked += 1
    need(checked == 1500 and record['surviving_truth_table_bytes_by_phase'] == [survivors]*6,
         'whole256 table coverage and both projection polarities')
    need(max_endpoint+1 == record['necessary_projection_only_prefix_length'] == 632,
         'literal quantified projection-only prefix bound')
    # Separately reconstruct the whole original same-phase domain using sets,
    # and check the retained projections at every literal root-free AP.
    by_phase = [{} for _ in range(6)]
    total = root_free = points = 0
    stream = hashlib.sha256()
    for d in range(1, 618):
        if d % 6:
            continue
        for a in range(3704-6*d):
            total += 1
            ns = [a+j*d for j in range(7)]
            actual_keys = [keys[n] for n in ns]
            if None in actual_keys:
                continue
            root_free += 1
            points += len(ns)
            support = frozenset(actual_keys)
            score = (ns[-1], a, d)
            old = by_phase[a % 6].get(support)
            if old is None or score < old:
                by_phase[a % 6][support] = score
            for bit in range(3):
                need(len({(key >> bit) & 1 for key in actual_keys}) == 2,
                     'every actual surviving projection is root-free progression-free')
            stream.update(struct.pack('<HHB7B', a, d, a % 6, *actual_keys))
    need(total == record['all_same_phase_positive_APs'] == 188700
         and root_free == record['all_root_free_same_phase_positive_APs'] == 182084,
         'entire original same-phase positive progression domain')
    for phase, row in enumerate(rows):
        for table in range(256):
            forbidden = [score for support, score in by_phase[phase].items()
                         if len({(table >> key) & 1 for key in support}) == 1]
            expected = None if not forbidden else list(min(forbidden)[1:])
            need(row[table] == expected, 'whole independently rebuilt original canonical row witnesses')
    return {'author': 'six-vdw-1', 'role': 'researcher',
            'status': 'EXACT_ORIGINAL_PHASE6_ROWS_REDUCE_TO_SINGLE_CHARACTER_PROJECTIONS_BY632',
            'q': 617, 'roots': [0, 1, 4], 'phase_period': 6,
            'necessary_projection_only_prefix_length': 632, 'all_truth_tables_per_phase': 256,
            'phases': 6, 'nonprojection_table_obstructions': checked,
            'surviving_truth_table_bytes_by_phase': [survivors]*6,
            'distinct_literal_root_free_obstruction_APs': len(witnesses),
            'maximum_obstruction_step': max_step, 'maximum_obstruction_endpoint': max_endpoint,
            'entire_original_same_phase_APs': total, 'entire_root_free_same_phase_APs': root_free,
            'entire_root_free_same_phase_AP_points': points,
            'whole_ordered_root_free_phase_AP_key_stream_sha256': stream.hexdigest(),
            'all_original_root_values_unrestricted': True,
            'surviving_rows_guarantee_mixed_phase_AP_avoidance': False,
            'unrestricted_W_bound_established': False, 'external_review_claimed': False}


if __name__ == '__main__':
    print(json.dumps(check(json.loads((Path(__file__).resolve().parent/'phase-rows-v2.json').read_bytes())),
                     sort_keys=True))
