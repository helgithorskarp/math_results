"""Literal incompatibility-class certificates for all residual domains."""
from itertools import combinations
from pathlib import Path
import hashlib
import json
import resource
import time

from coloring import proper_color

from paths import BASE, WORK
ROOT = WORK


def run():
    started = time.monotonic()
    joint = json.loads((ROOT/'joint_classes.json').read_text())
    if not joint['status'].startswith('COMPLETE'):
        raise RuntimeError('joint-star carrier is incomplete')
    records = []
    path = ROOT/'color_bounds.json'
    path.write_text(json.dumps(dict(status='INCOMPLETE', records=records))+'\n')
    for case in joint['cases']:
        case_started = time.monotonic()
        fixed = sorted(set(case['left']) | set(case['right']))
        if len(fixed) != 37:
            raise RuntimeError('wrong fixed code length')
        candidates = [sum(1 << u for u in q) for q in combinations(range(1, 17), 5)
                      if all((sum(1 << u for u in q) & w).bit_count() <= 2 for w in fixed)]
        # Build a separate literal set domain and check it entry by entry.
        literal_fixed = [frozenset(u for u in range(18) if w >> u & 1) for w in fixed]
        literal = [frozenset(q) for q in combinations(range(1, 17), 5)
                   if all(len(frozenset(q) & w) <= 2 for w in literal_fixed)]
        if candidates != [sum(1 << u for u in q) for q in literal]:
            raise RuntimeError('independent residual domains differ')
        adjacency = [sum(1 << j for j, v in enumerate(candidates)
                         if i != j and (u & v).bit_count() <= 2) for i, u in enumerate(candidates)]
        order, colors = proper_color((1 << len(candidates))-1, adjacency)
        primary = [[] for _ in range(max(colors, default=0))]
        for vertex, color in zip(order, colors):
            primary[color-1].append(vertex)
        conflict = [set(j for j, q in enumerate(literal) if i != j and len(p & q) >= 3)
                    for i, p in enumerate(literal)]
        remaining = set(range(len(literal)))
        separate = []
        while remaining:
            color = []
            possible = set(remaining)
            while possible:
                v = max(possible, key=lambda u: (len(conflict[u] & possible), -u))
                color.append(v)
                remaining.remove(v)
                possible.remove(v)
                possible.intersection_update(conflict[v])
            separate.append(color)
        for partition in (primary, separate):
            flattened = [u for color in partition for u in color]
            if (sorted(flattened) != list(range(len(candidates)))
                    or any(len(literal[a] & literal[b]) < 3 for color in partition
                           for a, b in combinations(color, 2))):
                raise RuntimeError('coloring certificate fails literal coverage/incompatibility')
        chosen = min((primary, separate), key=lambda q: (len(q), q))
        entry = dict(index=case['index'], first=case['first'], second=case['second'],
                     candidates=len(candidates), candidate_sha256=hashlib.sha256(
                         json.dumps(candidates, separators=(',', ':')).encode()).hexdigest(),
                     primary_colors=len(primary), separate_colors=len(separate),
                     certified_residual_upper=len(chosen), certified_code_upper=37+len(chosen),
                     partition=chosen)
        records.append(entry)
        if time.monotonic()-case_started > 10:
            raise RuntimeError('INCOMPLETE certificate case time guard')
        path.write_text(json.dumps(dict(status='INCOMPLETE', records=records), indent=2)+'\n')
    result = dict(agent='six-code-3', role='researcher', status='COMPLETE literal color certificates',
                  classes=len(records), maximum_code_upper=max(q['certified_code_upper'] for q in records),
                  maximum_primary_color_upper=max(q['primary_colors'] for q in records),
                  maximum_separate_color_upper=max(q['separate_colors'] for q in records),
                  unresolved72=[q['index'] for q in records if q['certified_code_upper'] >= 72],
                  records=records, seconds=round(time.monotonic()-started, 6),
                  maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    path.write_text(json.dumps(result, indent=2)+'\n')
    print({k:v for k,v in result.items() if k!='records'})
    return result


if __name__ == '__main__':
    run()
