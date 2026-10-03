"""Guarded finite37 child; completed cases are flushed before next case."""
import argparse
from itertools import permutations
import json
from pathlib import Path
import resource
import sys
import time
from model import Budget, Guard, digest, encode, literal37, load, need, validate
import producer
import oracle


def put(path, obj):
    path.write_bytes(encode(obj) + b'\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['prepare', 'cases'])
    parser.add_argument('--indices', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--input', type=Path, required=True)
    args = parser.parse_args()
    out = args.out
    out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    active = None
    records = []
    certs = []
    progress = {'actual_agent': 'six-code-1', 'role': 'researcher', 'status': 'INCOMPLETE_NOT_ABSENCE',
                'completed_case_indices': [], 'complete': False}
    put(out / 'progress.json', progress)
    try:
        data, input_sha = load(args.input)
        Q, targetF = data['whole_original_Q4_quadruples'], data['target_free_triples']
        active = Budget('whole literal source validation')
        owners = validate(data, active)
        source_states = active.states
        need(time.monotonic() - start < 60, 'original60s child limit')
        if args.action == 'prepare':
            hashes = []
            all_free_maps = []
            for oi, (u, v) in enumerate(data['source_root_orientations']):
                active = Budget('whole1296 free maps orientation ' + str(oi))
                this = []
                for rank in range(1296):
                    A, ah = producer.free_map(Q, u, v, targetF, rank)
                    B, bh = oracle.free_map(Q, u, v, targetF, rank)
                    active.tick()
                    need(A == B and ah == bh, 'whole free9-point bindings match independent factoradic formula')
                    need(A[u] == 16 and A[v] == 17 and
                         sorted(A[a] for a in A if a not in [u, v]) == sorted(set().union(*(set(c) for c in targetF))),
                         'entire free binding image')
                    this.append(sorted(A.items()))
                need(len({encode(m) for m in this}) == 1296, 'all distinct free bindings')
                hashes.append(digest(this))
                all_free_maps.append(this)
            mathematical = {'action': 'prepare', 'input_sha256': input_sha, 'free_binding_sha256': hashes,
                            'two1296_free_map_lists_independently_identical': True,
                            'literal_owner_groups': data['literal_owner_groups'],
                            'literal_distinct_owner_stars': {k: [list(w) for w in v] for k, v in owners.items()},
                            'representative_whole_cases': data['representative_whole_case_count'],
                            'all_original_owner_whole_cases': data['all_original_owner_whole_case_count'],
                            'raw_representative17_point_bijections': data['representative_whole_case_count'] * 720,
                            'raw_all_original_owner17_point_bijections': data['all_original_owner_whole_case_count'] * 720,
                            'full37_outcomes_uncomputed_by_this_action': True}
            put(out / 'whole-free-bindings.json', all_free_maps)
        else:
            need(args.indices is not None, 'sealed predetermined indices required')
            indices = json.loads(args.indices.read_text())
            need(indices and len(indices) == len(set(indices)) and all(isinstance(i, int) and 0 <= i < data['representative_whole_case_count'] for i in indices),
                 'distinct actual whole-case indices')
            put(out / 'requested-indices.json', indices)
            with (out / 'complete-decisions.jsonl').open('wb') as stream, (out / 'actual37-certificates.jsonl').open('wb') as cert_stream:
                for index in indices:
                    if time.monotonic() - start > 60:
                        raise Guard('original60s focused child')
                    owner_rank, rem = divmod(index, 2592)
                    orientation, free_rank = divmod(rem, 1296)
                    owner_index = sorted(owners)[owner_rank]
                    owner = owners[owner_index]
                    u, v = data['source_root_orientations'][orientation]
                    active = Budget('whole six-hole case ' + str(index))
                    progress['active_case'] = index
                    put(out / 'progress.json', progress)
                    A, A_counts = producer.search(Q, owner, u, v, targetF, free_rank, active)
                    B, B_counts = oracle.search(Q, owner, u, v, targetF, free_rank, active)
                    need(A == B and len(A) == len(set(A)), 'entire original17-point solution lists agree')
                    for image in A:
                        cert = literal37(Q, owner, image, u, v, active)
                        cert.update(case_index=index, original_owner_row_index=owner_index,
                                    source_root_orientation=[u, v], free_rank=free_rank)
                        certs.append(cert)
                        cert_stream.write(encode(cert) + b'\n')
                        cert_stream.flush()
                    row = {'case_index': index, 'original_owner_row_index': owner_index,
                           'source_roots': [u, v], 'free_rank': free_rank,
                           'whole_solution_maps': [list(p) for p in A],
                           'producer_search_counts': A_counts, 'oracle_search_counts': B_counts,
                           'decision': 'POSITIVE_ACTUAL37' if A else 'NEGATIVE_COMPLETE_SIX_HOLE_DOMAIN',
                           'whole_case_states': active.states}
                    records.append(row)
                    stream.write(encode(row) + b'\n')
                    stream.flush()
                    progress['completed_case_indices'].append(index)
                    progress['actual37_positive_count'] = len(certs)
                    progress.pop('active_case', None)
                    put(out / 'progress.json', progress)
                    active = None
            mathematical = {'action': 'cases', 'input_sha256': input_sha, 'requested_indices': indices,
                            'complete_requested_domain': True, 'all_whole_solution_map_lists_agree': True,
                            'complete_records_sha256': digest(records), 'actual37_certificates_sha256': digest(certs),
                            'actual37_certificate_count': len(certs),
                            'all_complete_solution_maps_checked_all666_pairs': True,
                            'max_whole_case_states': max(r['whole_case_states'] for r in records),
                            'complete_full_domain': set(indices) == set(range(data['representative_whole_case_count'])),
                            'global_endpoint_change': False}
        progress.update(complete=True, status='COMPLETE_DECLARED_DOMAIN', mathematical_sha256=digest(mathematical))
        put(out / 'progress.json', progress)
        summary = {'actual_agent': 'six-code-1', 'role': 'researcher', 'mathematical_record': mathematical,
                   'mathematical_sha256': digest(mathematical), 'elapsed_seconds': time.monotonic() - start,
                   'source_validation_states': source_states, 'peak_rss_KiB': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                   'optimized': bool(sys.flags.optimize), 'interpreter': sys.version}
        put(out / 'mathematical-record.json', mathematical)
        put(out / 'summary.json', summary)
        print(json.dumps(summary))
    except BaseException as exc:
        progress.update(complete=False, status='INCOMPLETE_GUARD_OR_DISCREPANCY_NOT_ABSENCE',
                        error_type=type(exc).__name__)
        # The active case can never silently turn into a completed negative.
        progress['error'] = str(exc)
        progress['active_case_receipt'] = active.receipt() if active else None
        put(out / 'progress.json', progress)
        raise


if __name__ == '__main__':
    main()
