"""Check the compact identities and exact UNKNOWN scope without solving."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    value = hashlib.sha256()
    with Path(path).open('rb') as stream:
        while chunk := stream.read(1024 * 1024):
            value.update(chunk)
    return value.hexdigest()


def manifest():
    count = 0
    for line in (HERE / 'SHA256SUMS').read_text().splitlines():
        wanted, name = line.split('  ', 1)
        require(digest(HERE / name) == wanted, 'source identity: ' + name)
        count += 1
    return count


def run():
    result = json.loads((HERE / 'RESULT.json').read_text())
    gate = json.loads((HERE / 'GATE.json').read_text())
    frozen = json.loads((HERE / 'FROZEN.json').read_text())
    audit = json.loads((HERE / 'FORMULA_AUDIT.json').read_text())
    controls = json.loads((HERE / 'MODEL_CONTROLS.json').read_text())
    evidence = json.loads((HERE / 'EVIDENCE.json').read_text())
    require(result['status'] == 'AUDITED_ORDERED_TRIANGLE_Q7R7_UNKNOWN_BOUNDARY', 'result status')
    require(result['task'] == frozen['task'] == audit['task'] == 'bo1-q7-r7-c000000', 'task identity')
    require(result['solver_status'] == 'UNKNOWN' and result['solver']['exit_code'] == 0, 'solver outcome')
    require(result['solver_calls'] == gate['solver_calls_max'] == 1, 'one-call gate')
    require(result['solver']['seconds_limit'] == frozen['seconds_limit'] == gate['solver_wall_seconds_max'] == 1800,
            'time gate')
    require(not result['candidate_found'] and not result['target43_found'], 'no target')
    require(not result['branch_excluded'] and result['tasks_decided'] == 0, 'no exclusion')
    require(result['tasks_remaining'] == 2189178, 'complete carrier remains')
    require(result['partial_drat']['is_certificate'] is False, 'partial proof scope')
    require(result['partial_drat']['checked'] is False and result['partial_drat']['published'] is False,
            'partial proof handling')
    require(result['witness']['bytes'] == len(b'c UNKNOWN\n'), 'witness size')
    require(result['witness']['sha256'] == hashlib.sha256(b'c UNKNOWN\n').hexdigest(), 'witness identity')
    for key in ('bytes', 'clauses', 'sha256', 'variables'):
        require(result['cnf'][key] == frozen['cnf'][key] == audit[key] == gate['formula'][key],
                'formula ' + key)
    require(result['cnf']['physical_variables'] == audit['physical_variables'] == 756, 'physical variables')
    require(result['cnf']['max_width'] == audit['max_width'] == 8, 'formula width')
    require(controls == {'encoding_variants': 2, 'models_rejected': 4,
                         'status': 'COMPLETE_NON_TARGET_MODELS_REJECTED',
                         'valid_ordering_clauses_checked': 910}, 'model controls')
    require(evidence['formula_audit_sha256'] == digest(HERE / 'FORMULA_AUDIT.json'), 'audit hash')
    require(evidence['gate_sha256'] == digest(HERE / 'GATE.json') == frozen['gate_sha256'], 'gate hash')
    require(evidence['model_controls_sha256'] == digest(HERE / 'MODEL_CONTROLS.json'), 'controls hash')
    require(evidence['runner_sha256'] == digest(HERE / 'run_decision.py') == frozen['runner_sha256'], 'runner hash')
    require(frozen['solver']['sha256'] == result['solver']['sha256'] == gate['solver']['sha256'], 'solver identity')
    return {
        'status': evidence['status'],
        'manifest_entries': manifest(),
        'solver_status': result['solver_status'],
        'solver_calls_replayed': 0,
        'target43_found': False,
        'task_excluded': False,
    }


if __name__ == '__main__':
    print(json.dumps(run(), sort_keys=True))
