"""Deterministic nonempty core cohorts for the complete q8 work queue."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import time

import task_queue


def partition(words, limit=4096):
    if type(limit) is not int or limit < 1:
        raise ValueError('Positive cohort capacity')
    n = len(words)
    columns = [bytearray((n+7)//8) for _ in range(55)]
    for c, word in enumerate(words):
        rest = word
        while rest:
            b = (rest & -rest).bit_length()-1
            columns[b][c//8] |= 1 << (c%8)
            rest &= rest-1
    columns = [int.from_bytes(x, 'little') for x in columns]
    nodes, leaves = [], []
    def visit(subset, mask, value):
        count = subset.bit_count()
        key = len(nodes)
        node = dict(id=key, mask=f'{mask:014x}', value=f'{value:014x}', count=count)
        nodes.append(node)
        if count <= limit:
            node['leaf'] = len(leaves)
            leaves.append(key)
            return key
        options = []
        for b in range(55):
            if not mask >> b & 1:
                yes = subset & columns[b]
                k = yes.bit_count()
                if 0 < k < count:
                    options.append((max(k, count-k), b, yes))
        if not options:
            raise ValueError('Distinct catalog words must admit a split')
        _, b, yes = min(options)
        node['bit'] = b
        node['zero'] = visit(subset ^ yes, mask | (1 << b), value)
        node['one'] = visit(yes, mask | (1 << b), value | (1 << b))
        return key
    visit((1 << n)-1, 0, 0)
    return dict(format='q8-core-cohorts-v1', limit=limit, cores=n, root=0, nodes=nodes, leaves=leaves)


def audit(words, tree):
    """Separate record traversal: verify every node's physical mask and count."""
    nodes = tree['nodes']
    counts = [0]*len(nodes)
    parents = [0]*len(nodes)
    leaf_numbers = []
    for i, node in enumerate(nodes):
        if node['id'] != i:
            raise ValueError('Node identity')
        mask, value = int(node['mask'], 16), int(node['value'], 16)
        if mask >= 1 << 55 or value & mask != value:
            raise ValueError('Node mask')
        if 'leaf' in node:
            leaf_numbers.append(node['leaf'])
            if not 1 <= node['count'] <= tree['limit']:
                raise ValueError('Leaf capacity')
        else:
            b = node['bit']
            if type(b) is not int or not 0 <= b < 55 or mask >> b & 1:
                raise ValueError('Split bit')
            for side in (0, 1):
                child = node['one' if side else 'zero']
                if type(child) is not int or not i < child < len(nodes):
                    raise ValueError('Acyclic child index')
                parents[child] += 1
                expected_mask, expected_value = mask | (1 << b), value | (side << b)
                if nodes[child]['mask'] != f'{expected_mask:014x}' or nodes[child]['value'] != f'{expected_value:014x}':
                    raise ValueError('Child physical assumptions')
    if parents != [0]+[1]*(len(nodes)-1) or sorted(leaf_numbers) != list(range(len(tree['leaves']))):
        raise ValueError('Not a complete rooted binary partition')
    if tree['root'] != 0 or nodes[0]['mask'] != '00000000000000' or nodes[0]['value'] != '00000000000000':
        raise ValueError('Unconditional root required')
    digests = [hashlib.sha256() for _ in tree['leaves']]
    for c, word in enumerate(words):
        i = 0
        while True:
            node = nodes[i]
            if word & int(node['mask'], 16) != int(node['value'], 16):
                raise ValueError('Record does not satisfy its node assumptions')
            counts[i] += 1
            if 'leaf' in node:
                digests[node['leaf']].update(struct.pack('<I', c))
                break
            i = node['one' if word >> node['bit'] & 1 else 'zero']
    if counts != [node['count'] for node in nodes] or tree['cores'] != len(words):
        raise ValueError('Entire-registry node membership mismatch')
    if [i for i, node in enumerate(nodes) if 'leaf' in node] != tree['leaves']:
        raise ValueError('Leaf registry mismatch')
    return dict(status='VERIFIED', original_task_ids=4*len(words), pending_cohort_jobs=4*len(tree['leaves']),
                core_leaves=len(tree['leaves']), nodes=len(nodes),
                smallest_cohort=min(nodes[i]['count'] for i in tree['leaves']),
                largest_cohort=max(nodes[i]['count'] for i in tree['leaves']),
                membership_digest=hashlib.sha256(''.join(x.hexdigest() for x in digests).encode()).hexdigest(),
                task_exclusions=0, all_original_task_statuses='UNKNOWN')


def job(tree, r, leaf):
    if type(r) is not int or r not in range(5, 9) or type(leaf) is not int or not 0 <= leaf < len(tree['leaves']):
        raise ValueError('Cohort worker scope')
    node = tree['nodes'][tree['leaves'][leaf]]
    mask, value = int(node['mask'], 16), int(node['value'], 16)
    a = [(802+b)*(1 if value >> b & 1 else -1) for b in range(55) if mask >> b & 1]
    return dict(r=r, cohort=leaf, original_tasks=node['count'], assumptions=a,
                status='PENDING_PHYSICAL43_COHORT', target_solver_calls=0)


def produce(directory):
    start = time.monotonic()
    d = Path(directory)
    words = task_queue.read_words(d/'cores.u64le')
    tree = partition(words)
    result = audit(words, tree)
    raw = (json.dumps(tree, separators=(',', ':'))+'\n').encode()
    with (d/'cohorts.json').open('xb') as f:
        f.write(raw)
    jobs = [job(tree, r, leaf) for r in range(5, 9) for leaf in range(len(tree['leaves']))]
    with (d/'cohort-jobs.jsonl').open('x') as f:
        for row in jobs:
            f.write(json.dumps(row, separators=(',', ':'))+'\n')
    if sum(row['original_tasks'] for row in jobs) != 4*len(words):
        raise ValueError('Dispatch lost a task')
    return dict(result, cohort_file_bytes=len(raw), cohort_sha256=hashlib.sha256(raw).hexdigest(),
                seconds=time.monotonic()-start, note='Grouped pending work units; no original task removed or decided')


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('directory'); p.add_argument('--r', type=int); p.add_argument('--leaf', type=int)
    a = p.parse_args()
    if a.r is None and a.leaf is None:
        result = produce(a.directory)
    else:
        expected = json.loads((task_queue.HERE/'EXPECTED.json').read_text())
        raw = (Path(a.directory)/'cohorts.json').read_bytes()
        if hashlib.sha256(raw).hexdigest() != expected['cohorts']['cohort_sha256']:
            raise ValueError('Audited cohort identity')
        row = job(json.loads(raw), a.r, a.leaf)
        result = dict(r=row['r'], core_assumptions=row['assumptions'], edge_cube=[])
    print(json.dumps(result, indent=2))
