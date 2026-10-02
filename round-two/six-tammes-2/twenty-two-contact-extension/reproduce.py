"""Regenerate and actually check a G22 cover from its empty dyadic root.

No incoming witness table is needed. A resumed chain is valid only when
the same operator actually executed its earlier successful checks.
"""
from pathlib import Path
from collections import Counter
import argparse
import hashlib
import json
import resource
import signal
import subprocess
import sys
import time
from binding import HERE, canonical, load, sha, write_json

GUARD_SECONDS = 160
CAMPAIGN_STATE = Path('/scratch/research-team-sol61-six-20260929/state')


def guard():
    if any((CAMPAIGN_STATE / name).exists()
           for name in ('PAUSED.json', 'HANDOVER.json')):
        raise RuntimeError('operational pause barrier')


def check(work, old_path, new_path, receipt_path, old_receipt_path=None):
    guard()
    delta, _, _ = load(work)
    new_bytes = Path(new_path).read_bytes()
    state = json.loads(new_bytes)
    started = time.monotonic()
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(
        TimeoutError('160-second literal replay guard; incomplete')))
    signal.alarm(GUARD_SECONDS)
    try:
        if old_path is None:
            result = delta.r.replay(state)
            result['literal_reader_sha256'] = delta.READER_HASH
        else:
            old_bytes = Path(old_path).read_bytes()
            previous_bytes = Path(old_receipt_path).read_bytes()
            previous = json.loads(previous_bytes)
            delta.r.require(previous['plan_sha256'] == sha(old_bytes), 'exact prior checked state')
            result = delta.verify_delta(json.loads(old_bytes), state, previous,
                                        require_complete=not state['stack'])
            result.update(input_plan_sha256=sha(old_bytes),
                          input_replay_receipt_sha256=sha(previous_bytes))
        result.update(plan_sha256=sha(new_bytes), seconds=round(time.monotonic()-started, 3),
                      guard_seconds=GUARD_SECONDS, canonical_state_sha256=sha(canonical(state)))
    finally:
        signal.alarm(0)
    write_json(receipt_path, result)
    print(json.dumps({key: result[key] for key in
                      ('status', 'witness_count', 'node_count', 'canonical_state_sha256', 'seconds')}))


def command(arguments):
    guard()
    started = time.monotonic()
    result = subprocess.run([sys.executable, *arguments], capture_output=True,
                            text=True, timeout=180)
    if result.returncode:
        sys.stderr.write(result.stderr)
        sys.stdout.write(result.stdout)
        raise RuntimeError('bounded generation/check job failed; preserve frontier and stop')
    return dict(command=arguments, seconds=round(time.monotonic()-started, 3),
                maximum_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)


def reproduce(work, steps=None, resume=False):
    guard()
    work = Path(work).resolve()
    _, _, _ = load(work)
    index_path = work / 'CHAIN.json'
    if resume:
        chain = json.loads(index_path.read_text())
        if chain['status'] not in ('CHECKED_PARTIAL_REGENERATION', 'CHECKED_COMPLETE_REGENERATION'):
            raise ValueError('unverified generated frontier; check it before resuming')
    else:
        if index_path.exists():
            raise ValueError('fresh reproduction requires a new work directory')
        node = dict(cell=[0,0,0,0], remaining=list(range(364)), proofs=[],
                    bounded_inherited=False, bounded=False)
        seed = dict(agent='six-tammes-2', role='researcher', status='EMPTY_ROOT_PARTIAL',
                    nodes=[node], stack=[0], stats={})
        seed_path = work / 'state-000.json'; receipt_path = work / 'receipt-000.json'
        write_json(seed_path, seed, compact=True)
        job = command([str(HERE/'reproduce.py'), 'check', '--work', str(work),
                       '--new', str(seed_path), '--receipt', str(receipt_path)])
        chain = dict(agent='six-tammes-2', role='researcher',
                     status='CHECKED_PARTIAL_REGENERATION', current=0,
                     transitions=[], seed_check=job,
                     validity_premise='actual successful seed and every transition check, not supplied receipts')
        write_json(index_path, chain)
    processed = 0
    while chain['status'] != 'CHECKED_COMPLETE_REGENERATION':
        if steps is not None and processed >= steps:
            break
        old_index = chain['current']; index = old_index + 1
        old_path = work/f'state-{old_index:03d}.json'
        old_receipt = work/f'receipt-{old_index:03d}.json'
        new_path = work/f'state-{index:03d}.json'
        new_receipt = work/f'receipt-{index:03d}.json'
        try:
            generation = command([str(HERE/'generate.py'), '--work', str(work),
                                  '--input', str(old_path), '--output', str(new_path)])
            checking = command([str(HERE/'reproduce.py'), 'check', '--work', str(work),
                                '--old', str(old_path), '--old-receipt', str(old_receipt),
                                '--new', str(new_path), '--receipt', str(new_receipt)])
        except Exception as error:
            chain.update(status='STOPPED_WITH_POSSIBLY_UNCHECKED_FRONTIER', error=str(error),
                         generated_candidate=str(new_path), candidate_receipt=str(new_receipt))
            write_json(index_path, chain)
            raise
        receipt = json.loads(new_receipt.read_text())
        chain['transitions'].append(dict(index=index, generation=generation, checking=checking,
                                         receipt_sha256=sha(new_receipt.read_bytes())))
        chain['current'] = index
        chain['status'] = 'CHECKED_COMPLETE_REGENERATION' if not receipt['pending_nodes'] else 'CHECKED_PARTIAL_REGENERATION'
        write_json(index_path, chain)
        processed += 1
        print(json.dumps(dict(transition=index, status=chain['status'],
                              checked_witnesses=receipt['witness_count'],
                              pending_nodes=len(receipt['pending_nodes']),
                              generation_seconds=generation['seconds'],
                              replay_seconds=checking['seconds'])), flush=True)
    final_receipt = json.loads((work/f"receipt-{chain['current']:03d}.json").read_text())
    summary = dict(status=chain['status'], actual_transition_checks=chain['current'],
                   final_receipt=final_receipt, chain_sha256=sha(index_path.read_bytes()),
                   interpreter=sys.version, independent_review=False)
    write_json(work/'SUMMARY.json', summary)
    return summary


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='action', required=True)
    check_parser = sub.add_parser('check')
    check_parser.add_argument('--work', required=True)
    check_parser.add_argument('--new', required=True)
    check_parser.add_argument('--receipt', required=True)
    check_parser.add_argument('--old')
    check_parser.add_argument('--old-receipt')
    run_parser = sub.add_parser('run')
    run_parser.add_argument('--work', required=True)
    run_parser.add_argument('--steps', type=int)
    run_parser.add_argument('--resume', action='store_true')
    args = parser.parse_args()
    if args.action == 'check':
        if bool(args.old) != bool(args.old_receipt):
            raise ValueError('old state and actual checked receipt are paired')
        check(args.work, args.old, args.new, args.receipt, args.old_receipt)
    else:
        if args.steps is not None and args.steps < 1:
            raise ValueError('positive transition count')
        result = reproduce(args.work, args.steps, args.resume)
        print(json.dumps(dict(status=result['status'], actual_transition_checks=result['actual_transition_checks'])))


if __name__ == '__main__':
    main()
