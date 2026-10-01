"""Complete bounded enumeration of Y20 stars in the three rooted domains.

No absence follows from a guard. Generated star/graph corpora are private.
"""
from itertools import combinations
from pathlib import Path
import argparse
import json
import time
import model as M
import seeds


class Incomplete(RuntimeError):
    pass


def cliques(adjacency, target, cap=200000):
    M.require(type(cap) is int and 0 <= cap <= 200000 and
              type(target) is int and 0 <= target <= len(adjacency), 'invalid fixed clique guard/target')
    output, nodes = [], 0
    start = time.monotonic()

    def search(pool, chosen):
        nonlocal nodes
        nodes += 1
        if nodes > cap or time.monotonic() - start > 10:
            raise Incomplete('INCOMPLETE fixed Y-star guard')
        need = target - len(chosen)
        if need == 0:
            output.append(tuple(chosen))
            return
        while pool.bit_count() >= need:
            bit = pool & -pool
            v = bit.bit_length() - 1
            pool ^= bit
            search(pool & adjacency[v], chosen + (v,))

    search((1 << len(adjacency)) - 1, ())
    M.require(len(output) == len(set(output)), 'duplicate six-clique')
    return tuple(sorted(output)), nodes


def run(output):
    M.require(not output.exists(), 'use new output path')
    roots, table = seeds.root_cases()
    resources, rows = M.orbit_carrier()
    records, anchors = [], []
    for root in roots:
        domain = seeds.y_domains(root['anchor'], resources, rows)
        configs = domain['configurations']
        for j, config in enumerate(configs):
            sixes, nodes = cliques(config['adjacency'], 6)
            actual = []
            for six in sixes:
                words = tuple(sorted(root['anchor'] + config['fixed_words'] +
                                     tuple(w for i in six for w in config['rows'][i]['words'])))
                stats = M.check_code(words)
                M.require(len(words) == 36 and stats['fixed_words'] == 8 and
                          stats['replications'][16:] == (20, 20), 'actual complete XY20 anchor')
                actual.append(words)
                leftovers = M.residual(words, resources, rows)
                M.require(all(r['weight'] == 2 and r['replications'][16:] == (0, 0)
                              for r in leftovers), 'residual word avoids both saturated fixed points')
                record = dict(fixture=root['fixture'], matching=j, six=six, words=words,
                              residual_orbits=len(leftovers))
                anchors.append(record)
            record = dict(fixture=root['fixture'], matching=j, paired_candidates=len(config['rows']),
                          y20_completions=len(sixes), nodes=nodes,
                          anchor_sha256=__import__('hashlib').sha256(M.encoded(actual)).hexdigest())
            records.append(record)
            print(json.dumps(record, sort_keys=True), flush=True)
    M.require(len({tuple(r['words']) for r in anchors}) == len(anchors), 'duplicate XY anchor')
    result = dict(agent='six-code-2', role='researcher', status='COMPLETE exact Y-star census',
                  roots=roots, root_table=table, records=records, anchors=anchors)
    output.write_bytes(M.encoded(result))
    print('COMPLETE', len(anchors), 'XY20 anchors; residual ranges',
          min((r['residual_orbits'] for r in anchors), default=0),
          max((r['residual_orbits'] for r in anchors), default=0), flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    run(a.output)
