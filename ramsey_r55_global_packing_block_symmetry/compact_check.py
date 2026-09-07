#!/usr/bin/env python3
"""Check compact identities and prevent scope inflation."""
from pathlib import Path
import hashlib
import json


HERE = Path(__file__).resolve().parent
def digest(name): return hashlib.sha256((HERE / name).read_bytes()).hexdigest()

result = json.loads((HERE / 'RESULT.json').read_text())
evidence = json.loads((HERE / 'EVIDENCE.json').read_text())
audit = json.loads((HERE / 'audit.json').read_text())
metadata = json.loads((HERE / 'metadata.json').read_text())
interface = json.loads((HERE / 'interface-audit.json').read_text())
frozen = json.loads((HERE / 'frozen-run.json').read_text())

assert result['status'] == 'VERIFIED_BLOCK_NORMALIZED_R7_S4_T3_UNKNOWN_BOUNDARY'
assert result['solver_status'] == 'UNKNOWN' and result['solver_exit_code'] == 0
assert not result['candidate_found'] and not result['target43_found'] and not result['branch_excluded']
assert result['h3835_branches_decided'] == 0 and result['h3835_branches_remaining'] == 60
assert result['partial_drat']['is_certificate'] is False
assert result['partial_drat']['checked'] is False and result['partial_drat']['published'] is False
assert result['witness']['sha256'] == hashlib.sha256(b'c UNKNOWN\n').hexdigest()
assert result['cnf']['sha256'] == audit['sha256'] == metadata['sha256'] == frozen['cnf']['sha256']
assert result['cnf']['variables'] == 966 and result['cnf']['clauses'] == 1426489
assert audit['symmetry_clauses'] == result['normalization']['symmetry_clauses'] == 723
assert audit['auxiliary_prefix_variables'] == result['normalization']['auxiliary_prefix_variables'] == 119
assert interface['status'] == 'VERIFIED_ALL_60_IDENTICAL_BLOCK_NORMALIZATIONS'
assert interface['branches'] == 60 and interface['r7_s4_t3']['block_action_order'] == 86400
for key, name in [('result_sha256','RESULT.json'),('gate_sha256','GATE.md'),
                  ('frozen_run_sha256','frozen-run.json'),('generator_sha256','block_symmetry.py'),
                  ('controls_source_sha256','controls.py'),('controls_record_sha256','controls.json'),
                  ('audit_source_sha256','audit.py'),('audit_record_sha256','audit.json'),
                  ('interface_audit_source_sha256','interface_audit.py'),
                  ('interface_audit_record_sha256','interface-audit.json')]:
    assert evidence[key] == digest(name)

print(json.dumps({'status':'VERIFIED_COMPACT_GLOBAL_PACKING_BLOCK_SYMMETRY_BOUNDARY',
                  'branches_normalized':60,'cnf_sha256':audit['sha256'],
                  'solver_status':'UNKNOWN','target43_found':False,
                  'branch_excluded':False},sort_keys=True))
