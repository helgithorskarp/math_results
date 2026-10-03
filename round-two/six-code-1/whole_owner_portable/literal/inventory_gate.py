"""All literal surviving right interfaces versus all697 original D2 keys."""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import time
from model import Budget, Guard, digest, encode, need
from partitions import key, point_bijections


def prototype(k, budget):
    deficit, colors, rows = k
    need(deficit == 2 and len(colors) == 4 and len(rows) == 5, 'entire D2 colored matrix')
    M = []
    columns = [set() for _ in range(4)]
    nxt = 5
    for hubmask, cells in rows:
        budget.tick()
        need(len(cells) == 4, 'all four incidence cells')
        row = set()
        for j, (mask, count) in enumerate(cells):
            cell = {h for h in range(5) if (mask >> h) & 1} | set(range(nxt, nxt + count))
            nxt += count
            row |= cell
            columns[j] |= cell
        need(sum(1 << h for h in row if h < 5) == hubmask and len(row) == 3, 'whole Hub-colored triple')
        M.append(sorted(row))
    need(nxt == 15 and set().union(*(set(m) for m in M)) == set(range(15)) and
         sum(map(len, M)) == 15, 'whole five-cell ground')
    need(all(len(c) == 3 for c in columns[:3]) and len(columns[3]) == 6,
         'whole three-free/six-hole partition')
    need([sum(1 << h for h in c if h < 5) for c in columns] == colors, 'all free/hole Hub colors')
    F = [sorted(c) for c in columns[:3]]
    need(key(M, F, budget) == k, 'literal prototype reproduces whole original key')
    return M, F


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--spec', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    spec = json.loads(args.spec.read_text())
    for pin in spec['input_pins']:
        b = Path(pin['path']).read_bytes()
        need(len(b) == pin['bytes'] and hashlib.sha256(b).hexdigest() == pin['sha256'], 'whole pinned input')
    types = spec['all_original697_D2_types']
    need(len(types) == len({t['original_type_id'] for t in types}) == 697 and
         len({encode(t['canonical_key']) for t in types}) == 697, 'entire original697 disjoint type dictionary')
    actual = spec['all_literal_surviving_right_F']
    need(len(actual) == len({encode(f) for f in actual}) == spec['literal_right_interface_count'], 'all literal right interfaces')
    M = spec['actual_common_mate_partition']
    targets = []
    max_states = 0
    for t in types:
        budget = Budget('whole original prototype ' + str(t['original_type_id']))
        targets.append(prototype(t['canonical_key'], budget))
        max_states = max(max_states, budget.states)
    rows = []
    positive_controls = []
    active = None
    progress = {'complete': False, 'completed_pair_cases': 0, 'status': 'INCOMPLETE_NOT_ABSENCE'}
    (args.out / 'progress.json').write_bytes(encode(progress) + b'\n')
    try:
        with (args.out / 'complete-pair-decisions.jsonl').open('wb') as stream:
            for fi, F in enumerate(actual):
                active = Budget('self-interface synthetic positive control ' + str(fi))
                k = key(M, F, active)
                PM, PF = prototype(k, active)
                maps = point_bijections(M, F, PM, PF, active)
                need(maps, 'actual complete point maps to own prototype accepted')
                positive_controls.append({'literal_F_index': fi, 'whole_actual_key': k,
                                          'all_actual_self_prototype_maps': [list(p) for p in maps]})
                max_states = max(max_states, active.states)
                for ti, t in enumerate(types):
                    if time.monotonic() - start > 60:
                        raise Guard('original60s inventory gate child')
                    active = Budget('whole right-interface pair ' + str(fi) + '/' + str(t['original_type_id']))
                    TM, TF = targets[ti]
                    maps = point_bijections(M, F, TM, TF, active)
                    need(bool(maps) == (k == t['canonical_key']), 'literal point-bijection versus entire colored matrix')
                    row = {'literal_F_index': fi, 'original_D2_type_id': t['original_type_id'],
                           'entire_point_maps': [list(p) for p in maps], 'realized': bool(maps),
                           'whole_case_states': active.states}
                    rows.append(row)
                    stream.write(encode(row) + b'\n')
                    stream.flush()
                    max_states = max(max_states, active.states)
                    progress['completed_pair_cases'] = len(rows)
                (args.out / 'progress.json').write_bytes(encode(progress) + b'\n')
                active = None
        mathematical = {'actual_agent': 'six-code-1', 'role': 'researcher', 'complete': True,
                        'all_actual37_right_interfaces': len(actual), 'original_D2_type_count': 697,
                        'complete_pair_cases': len(rows), 'entire_pair_record_sha256': digest(rows),
                        'realized_D2_pairs': sum(r['realized'] for r in rows),
                        'all_self_prototype_positive_controls': positive_controls,
                        'max_whole_case_states': max_states,
                        'scope': spec['literal_scope'],
                        'inventory_completeness': 'literal source-only selected-domain generation; application/normalization bridges ordinary unformalized',
                        'global_endpoint_change': False, 'independent_person_review': 'pending'}
        (args.out / 'mathematical-record.json').write_bytes(encode(mathematical) + b'\n')
        progress.update(complete=True, status='COMPLETE_LITERAL_SELECTED_INVENTORY', mathematical_sha256=digest(mathematical))
        (args.out / 'progress.json').write_bytes(encode(progress) + b'\n')
        summary = {'mathematical_record': mathematical, 'mathematical_sha256': digest(mathematical),
                   'elapsed_seconds': time.monotonic() - start,
                   'peak_rss_KiB': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
        (args.out / 'summary.json').write_bytes(encode(summary) + b'\n')
        print(json.dumps({'complete': True, 'whole_pairs': len(rows), 'realized_D2_pairs': mathematical['realized_D2_pairs'],
                          'max_states': max_states, 'seconds': summary['elapsed_seconds'], 'mathematical_sha256': digest(mathematical)}))
    except BaseException as exc:
        progress.update(error_type=type(exc).__name__, error=str(exc),
                        active_case=active.receipt() if active else None)
        (args.out / 'progress.json').write_bytes(encode(progress) + b'\n')
        raise


if __name__ == '__main__':
    main()
