#!/usr/bin/env python3
"""Check compact identities and the exact logical scope of the boundary."""
from pathlib import Path
import hashlib
import json


HERE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


result = json.loads((HERE / 'RESULT.json').read_text())
evidence = json.loads((HERE / 'EVIDENCE.json').read_text())
audit = json.loads((HERE / 'audit.json').read_text())
frozen = json.loads((HERE / 'frozen-run.json').read_text())
task = json.loads((HERE / 'branch-task.json').read_text())

assert result['status'] == 'AUDITED_GLOBAL_PACKING_R7_S4_T3_UNKNOWN_BOUNDARY'
assert result['branch'] == task['branch'] == frozen['branch'] == [7, 4, 3]
assert task['task_id'] == result['task_id'] == 'r7-s4-t3'
assert result['solver_status'] == 'UNKNOWN' and result['solver_exit_code'] == 0
assert not result['candidate_found'] and not result['target43_found']
assert not result['branch_excluded'] and result['unconditional_cover_branches_remaining'] == 60
assert result['partial_drat']['is_certificate'] is False
assert result['partial_drat']['checked'] is False
assert result['partial_drat']['published'] is False
assert result['witness']['bytes'] == len(b'c UNKNOWN\n')
assert result['witness']['sha256'] == hashlib.sha256(b'c UNKNOWN\n').hexdigest()
assert result['cnf']['sha256'] == audit['sha256'] == frozen['cnf']['sha256']
assert result['cnf']['variables'] == audit['variables'] == 847
assert result['cnf']['clauses'] == audit['clauses'] == task['cnf_clauses'] == 1425766
assert audit['five_sets_checked'] == 962598
assert audit['fixed_red_edges'] == 57 and audit['free_physical_edges'] == 846
assert evidence['result_sha256'] == digest(HERE / 'RESULT.json')
assert evidence['audit_record_sha256'] == digest(HERE / 'audit.json')
assert evidence['audit_source_sha256'] == digest(HERE / 'audit.py')
assert evidence['frozen_run_sha256'] == digest(HERE / 'frozen-run.json')

print(json.dumps({
    'status': 'VERIFIED_COMPACT_R7_S4_T3_UNKNOWN_BOUNDARY',
    'cnf_sha256': audit['sha256'],
    'solver_status': result['solver_status'],
    'target43_found': result['target43_found'],
    'branch_excluded': result['branch_excluded'],
}, sort_keys=True))
