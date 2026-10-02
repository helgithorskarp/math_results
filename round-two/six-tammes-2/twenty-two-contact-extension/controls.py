"""Entry-level chunking regression and genuine rejection controls.

The positive fixtures cover the whole rectangle structurally but prove
only a partial list of obligations. They are never called a theorem.
These checks share the frozen arithmetic kernel and are not independent
mathematical review.
"""
from pathlib import Path
import argparse
import copy
import json
import signal
import time
from binding import canonical, load, sha, write_json
from generate import advance


def seed():
    return dict(nodes=[dict(cell=[0,0,0,0], remaining=list(range(364)), proofs=[],
                            bounded_inherited=False, bounded=False)], stack=[0], stats={})


def checked_receipt(reader, reader_hash, state):
    result = reader.replay(state)
    result['literal_reader_sha256'] = reader_hash
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', required=True)
    parser.add_argument('--report', required=True)
    args = parser.parse_args()
    started = time.monotonic()
    delta, runtime, _ = load(args.work)
    reader = delta.r
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(
        TimeoutError('160-second controls guard; incomplete')))
    signal.alarm(160)
    rejects = []

    def reject(name, action):
        try:
            action()
        except (ValueError, ArithmeticError) as error:
            rejects.append(dict(name=name, reason=str(error)))
        else:
            raise ValueError('damaged control accepted: ' + name)

    try:
        start = seed()
        initial_receipt = checked_receipt(reader, delta.READER_HASH, start)
        one = advance(copy.deepcopy(start), reader, 32)
        full_receipt = checked_receipt(reader, delta.READER_HASH, one)
        part = copy.deepcopy(start); previous_receipt = initial_receipt
        transition_counts = []
        for _ in range(4):
            old = part
            part = advance(copy.deepcopy(old), reader, 8)
            previous_receipt = delta.verify_delta(old, part, previous_receipt)
            transition_counts.append(previous_receipt['checked_new_witnesses'])
        reader.require(canonical(part) == canonical(one),
                       'one32 and four8 generation chunks agree at every structural/literal entry')
        reader.require(sum(transition_counts) == 32 == full_receipt['witness_count'],
                       'all32 generated literal entries actually checked')
        # The first32 records need no split. Add a valid closed dyadic
        # partition explicitly; its children carry the exact outstanding
        # obligations and no new arithmetic claim.
        split_fixture = copy.deepcopy(one)
        reader.require(len(split_fixture['nodes']) == 1, 'small unsplit root fixture')
        root = split_fixture['nodes'][0]
        root.update(split='t', children=[1,2])
        inherited = root['bounded_inherited'] or root['bounded']
        for cell in ([1,0,0,0], [1,1,0,0]):
            split_fixture['nodes'].append(dict(cell=cell, remaining=list(root['remaining']),
                                              proofs=[], bounded_inherited=inherited, bounded=False))
        split_fixture['stack'] = [2,1]
        checked_receipt(reader, delta.READER_HASH, split_fixture)
        write_json(Path(args.work)/'fixture32.json', one, compact=True)
        write_json(Path(args.work)/'split-fixture32.json', split_fixture, compact=True)
        reject('partial_fixture_is_not_complete', lambda: reader.shape(one, True))
        broken = copy.deepcopy(split_fixture)
        split_index = next(i for i,n in enumerate(broken['nodes']) if 'split' in n)
        broken['nodes'][split_index]['children'] = broken['nodes'][split_index]['children'][:1]
        reject('missing_closed_split_child', lambda: reader.shape(broken))
        broken = copy.deepcopy(one)
        first_proof = next(i for i,n in enumerate(broken['nodes']) if n['proofs'])
        broken['nodes'][first_proof]['proofs'].append(broken['nodes'][first_proof]['proofs'][0])
        reject('duplicate_active_triple_obligation', lambda: reader.shape(broken))
        broken = copy.deepcopy(one)
        row = next(row for n in broken['nodes'] for row in n['proofs'] if row[0] != reader.c.CRITICAL)
        row[1:] = ['K']
        reject('critical_import_on_another_triple', lambda: reader.replay(broken))
        r_proof = next((i,j) for i,n in enumerate(one['nodes'])
                       for j,row in enumerate(n['proofs']) if row[1] == 'R')
        broken = copy.deepcopy(one)
        i,j = r_proof
        broken['nodes'][i]['proofs'][j][1:] = ['T']
        reject('false_valid_core_norm_predicate', lambda: reader.replay(broken))
        broken = copy.deepcopy(one)
        multi_node = next(i for i,n in enumerate(broken['nodes']) if len(n['proofs']) > 1)
        old_node = broken['nodes'][multi_node]
        old_node['proofs'] = list(reversed(old_node['proofs']))
        reject('changed_order_of_previously_checked_records',
               lambda: delta.structure(one, broken))
        forged = copy.deepcopy(previous_receipt); forged['witness_count'] += 1
        reject('forged_checked_input_record_count',
               lambda: delta.verify_delta(part, copy.deepcopy(part), forged))
        target = runtime/'scratch/g22-cap-model-v2.py'
        payload = target.read_bytes()
        try:
            target.write_bytes(payload+b'\n')
            reject('changed_runtime_arithmetic_source', lambda: load(args.work))
        finally:
            target.write_bytes(payload)
        result = dict(status='PASSED_AUTHOR_CHUNKING_AND_REJECTION_CONTROLS',
                      agent='six-tammes-2', role='researcher',
                      actual_positive_full_reader_checks=3,
                      actual_positive_delta_checks=4,
                      checked_literal_count=32, per_transition_additions=transition_counts,
                      complete_exclusion_claimed=False,
                      canonical_partial_fixture_sha256=sha(canonical(one)),
                      canonical_split_fixture_sha256=sha(canonical(split_fixture)),
                      negative_controls=rejects, independent_review=False,
                      seconds=round(time.monotonic()-started, 3))
        write_json(args.report, result)
        print(json.dumps(result, indent=2))
    finally:
        signal.alarm(0)


if __name__ == '__main__':
    main()
