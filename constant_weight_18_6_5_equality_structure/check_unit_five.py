"""Bounded pilot for the matched-low unit-core packing problem."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import argparse
import json
import sys
import time

import unit_five_carrier as carrier

HERE = Path(__file__).resolve().parent


class Incomplete(Exception):
    pass


def bits(value):
    while value:
        first = value & -value
        yield first.bit_length()-1
        value ^= first


def solve(eligible, columns, quota, mandatory, node_limit=200000, seconds=10):
    carrier.require(len(quota) == 15 and all(type(n) is int and n >= 0 for n in quota),
                    'invalid point quota')
    index = {e:i for i,e in enumerate(eligible)}
    masks, point_masks = [], [0]*15
    pair_masks = [0]*len(eligible)
    for i,q in enumerate(columns):
        carrier.require(len(q) == 4 and tuple(sorted(set(q))) == q, 'invalid candidate quadruple')
        edges = tuple(combinations(q,2))
        carrier.require(all(e in index for e in edges), 'candidate repeats an anchor pair')
        mask = sum(1 << index[e] for e in edges)
        masks.append(mask)
        for x in q:point_masks[x] |= 1 << i
        for e in edges:pair_masks[index[e]] |= 1 << i
    carrier.require(set(mandatory) <= set(eligible), 'invalid mandatory pair')
    required = sum(1 << index[e] for e in mandatory)
    conflicts = [0]*len(columns)
    for i,mask in enumerate(masks):
        for p in bits(mask):conflicts[i] |= pair_masks[p]
    active = (1 << len(columns))-1
    for x,n in enumerate(quota):
        if n == 0:active &= ~point_masks[x]
    nodes, started = 0, time.monotonic()

    def visit(left, need, available, selected):
        nonlocal nodes
        nodes += 1
        if nodes > node_limit or (nodes % 128 == 0 and time.monotonic()-started > seconds):
            raise Incomplete('INCOMPLETE quota-search guard')
        if not any(left) and not need:
            return selected, None
        for x,n in enumerate(left):
            if n and (available & point_masks[x]).bit_count() < n:
                return None, ['C',x,[]]
        if need:
            _,pivot = min(((available & pair_masks[p]).bit_count(),p) for p in bits(need))
            tag,choices = 'P',available & pair_masks[pivot]
        else:
            _,pivot = min(((available & point_masks[x]).bit_count(),x)
                          for x,n in enumerate(left) if n)
            tag,choices = 'V',available & point_masks[pivot]
        children = []
        for i in bits(choices):
            after,finished = list(left),0
            for x in columns[i]:
                after[x] -= 1
                carrier.require(after[x] >= 0, 'active candidate exceeds quota')
                if after[x] == 0:finished |= point_masks[x]
            witness,tree = visit(tuple(after),need & ~masks[i],
                                 available & ~conflicts[i] & ~finished,selected+(i,))
            if witness is not None:return witness,None
            children.append([i,tree])
        return None,[tag,pivot,children]

    witness,tree = visit(tuple(quota),required,active,())
    return witness,tree,nodes


def controls():
    _,_,eligible,columns = carrier.matrix('cycle10')
    q = columns[0]
    quota = tuple(int(x in q) for x in range(15))
    mandatory = tuple(combinations(q,2))
    witness,_,_ = solve(eligible,(q,),quota,mandatory)
    carrier.require(witness == (0,), 'known positive quota fixture rejected')
    missing = next(e for e in eligible if e not in mandatory)
    witness,tree,_ = solve(eligible,(q,),quota,mandatory+(missing,))
    carrier.require(witness is None and tree, 'known negative quota fixture accepted')
    try:
        solve(eligible,(q,),quota,mandatory,node_limit=0)
    except Incomplete:
        pass
    else:
        raise ValueError('zero quota-search cap yielded a mathematical verdict')
    return {'positive_fixture':True,'negative_fixture':True,'zero_cap_incomplete':True}


def check_witness(high,anchors,columns,witness):
    quads = anchors+tuple(columns[i] for i in witness)
    covered = Counter(e for q in quads for e in combinations(q,2))
    high = frozenset(high)
    carrier.require(len(quads) == len(set(quads)) == 20 and len(covered) == 120
                    and set(covered.values()) == {1}, 'invalid restored twenty-block witness')
    carrier.require([sum(x in q for q in quads) for x in range(17)]
                    == [4 if x in high else 5 for x in range(17)], 'invalid witness replications')
    leave = set(combinations(range(17),2))-set(covered)
    carrier.require(sum(set(e) <= high for e in leave) == 5
                    and {e for e in leave if not set(e)&high} == {(15,16)}, 'invalid five-edge witness')
    return quads


def build():
    report = {'agent':'six-code-1','role':'researcher',
              'status':'COMPLETE_PRIMARY_ALL_FIBERS_UNREPLAYED','cases':[],
              'controls':controls(),'matrix_census':carrier.matrix_census()}
    proofs = {}
    for name in ('cycle10','cycle6_cycle4'):
        cells,anchors,eligible,candidates = carrier.matrix(name)
        maps = carrier.group(name,cells,anchors)
        for high,weight,stabilizer in carrier.high_quotient(maps):
            instance = carrier.instance(high,eligible,candidates)
            if instance is None:continue
            quota,mandatory,columns,r,branches = instance
            witness,tree,nodes = solve(eligible,columns,quota,mandatory)
            if witness is not None:
                check_witness(high,anchors,columns,witness)
                raise ValueError('positive five-edge star found; exclusion is false')
            record = {'model':name,'high':high,'orbit_size':weight,'R':r,
                      'columns':len(columns),'mandatory_pairs':len(mandatory),
                      'input_sha256':carrier.digest([high,eligible,columns,quota,mandatory]),
                      'status':'EXACT_NO_WITNESS_UNREPLAYED','nodes':nodes}
            proofs[str(len(report['cases']))] = tree
            report['cases'].append(record)
    carrier.require(len(report['cases'])==267,'primary carrier is incomplete')
    return json.loads(carrier.encoded(report)),proofs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-certificate',action='store_true')
    args = parser.parse_args()
    report,proofs = build()
    expected_path = HERE/'unit_five_expected.json'
    expected = json.loads(expected_path.read_text())
    blob = carrier.encoded(proofs)
    if args.write_certificate:
        expected['primary'] = report
        expected_path.write_bytes(carrier.encoded(expected))
        (HERE/'unit_five_certificate.json').write_bytes(blob)
    else:
        carrier.require(report==expected['primary'],'primary expected report mismatch')
        carrier.require(blob==(HERE/'unit_five_certificate.json').read_bytes(),'certificate byte mismatch')
    print(json.dumps({'agent':'six-code-1','role':'researcher','status':report['status'],
                      'cases':len(report['cases']),'nodes':sum(c['nodes'] for c in report['cases']),
                      'certificate_bytes':len(blob),'certificate_sha256':carrier.digest(proofs)},indent=2))


if __name__=='__main__':main()
