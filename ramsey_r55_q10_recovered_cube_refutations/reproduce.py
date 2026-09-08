"""Replay three proof cores, the complete physical cover, and integration."""
from pathlib import Path
import argparse
import json
import resource
import subprocess
import sys
import time
import controls
import interface
import verify

ROOT = Path(__file__).resolve().parent


def command(args):
    result = subprocess.run(list(map(str, args)), capture_output=True, text=True)
    if result.returncode:
        raise ValueError('command failed: ' + result.stderr[-2000:])
    return json.loads(result.stdout)


def replay(branches, scratch):
    start = time.monotonic()
    scratch = Path(scratch).resolve()
    scratch.mkdir(parents=True, exist_ok=True)
    verify.need(not any(scratch.iterdir()), 'scratch must be empty')
    branches = Path(branches).resolve()
    support = verify.support(branches)
    structure = verify.structure()
    tasks = verify.tasks()
    verify.need(json.loads((ROOT/'TASKS.json').read_text()) == tasks, 'task entry agreement')
    binaries = {}
    for name, source in [('check-rup', 'check_rup.cpp'), ('propagate', 'propagate.cpp'),
                         ('check-fixedpoint', 'check_fixedpoint.cpp')]:
        binary = scratch/name
        result = subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra',
            '-Wconversion', '-pedantic', str(ROOT/source), '-o', str(binary)],
            capture_output=True, text=True)
        verify.need(result.returncode == 0 and not result.stderr, 'clean C++ build')
        binaries[name] = binary
    cpp_controls = command([binaries['check-rup'], '--controls'])
    proofs = {}
    for row in support:
        name = row['id']
        proofs[name] = command([binaries['check-rup'], ROOT/(name+'-core.cnf'),
                               ROOT/(name+'-core.drat')])
        verify.need(proofs[name]['additions'] == proofs[name]['rup_additions'],
                    'every addition RUP')
    control_result = controls.run(binaries['propagate'], binaries['check-rup'], scratch,
                                  binaries['check-fixedpoint'])
    integration = []
    fixedpoints = []
    for branch in ('d20-22', 'd22-20'):
        selected = [r for r in tasks if r['branch'] == branch]
        query = scratch/(branch+'-children.txt')
        query.write_text(''.join(' '.join(str(-x) for x in r['cube'])+' 0\n'
                                 for r in selected))
        source = branches/(branch+'.cnf')
        baseline = command([binaries['propagate'], source, query, '--all'])
        partials = scratch/(branch+'-fixedpoints.txt')
        partials.write_text(''.join(' '.join(map(str, r['assigned_literals']))+' 0\n'
                                   for r in baseline['tests']))
        fixedpoints.append(command([binaries['check-fixedpoint'], source, query, partials]))
        patched = scratch/(branch+'-patched.cnf')
        interface.write_cnf(source, patched, interface.patch_clauses(branch))
        after = command([binaries['propagate'], patched, query, '--physical'])
        verify.need(len(baseline['tests']) == len(after['tests']) == 130,
                    'complete physical partition tested')
        verify.need(baseline['rup'] == 0, 'baseline child was already RUP')
        for task, before, changed in zip(selected, baseline['tests'], after['tests']):
            closed = task['status'] == 'CERTIFIED_UNSAT'
            verify.need(changed['rup'] == closed, 'patched propagation status')
            extra = sorted(set(changed['physical_values']) - set(before['physical_values']))
            forced = task['forced_residual_literal']
            if forced is not None:
                verify.need(forced not in before['physical_values'] and
                            forced in changed['physical_values'], 'new physical edge implication')
            integration.append({'task': task['id'], 'baseline_conflict': before['rup'],
                'patched_conflict': changed['rup'],
                'new_physical_literals_on_unknown': extra if not closed else None})
    # Exercise receiving emission, including a remaining p=0 task and the
    # closed-task guard. Verify every suffix and the unchanged physical body.
    emissions = []
    for branch in ('d20-22', 'd22-20'):
        row = next(r for r in tasks if r['branch'] == branch and
                   r['status'] == 'UNKNOWN' and r['id'].endswith('p0'))
        output = scratch/(row['id']+'.cnf')
        receipt = interface.emit(row['id'], branches, output)
        suffix = interface.patch_clauses(branch) + [[x] for x in row['cube']]
        if row['forced_residual_literal'] is not None:
            suffix.append([row['forced_residual_literal']])
        with output.open('rb') as stream, (branches/(branch+'.cnf')).open('rb') as source:
            verify.need(stream.readline() ==
                f'p cnf 40351 {1931146+len(suffix)}\n'.encode(), 'emitted header')
            source.readline()
            while data := source.read(1024*1024):
                verify.need(stream.read(len(data)) == data, 'emitted source body')
            expected = ''.join(' '.join(map(str,c))+' 0\n' for c in suffix).encode()
            verify.need(stream.read() == expected, 'emitted suffix')
        emissions.append(receipt)
    closed = next(r for r in tasks if r['status'] == 'CERTIFIED_UNSAT')
    output = scratch/'closed-must-not-exist.cnf'
    result = interface.emit(closed['id'], branches, output)
    verify.need(not result['file_written'] and not output.exists(), 'closed-task guard')
    stable = {'status': 'REPRODUCED_99_Q10_PHYSICAL_SUBTASK_REFUTATIONS',
              'structure': structure, 'support': support, 'proofs': proofs,
              'cpp_controls': cpp_controls, 'controls': control_result,
              'baseline_fixedpoint_audits': fixedpoints,
              'tasks': verify.task_summary(tasks), 'integration': integration,
              'emissions': emissions, 'solver_calls': 0,
              'whole_parent_formulas': 'BOTH_UNKNOWN', 'good43_found': False}
    expected = json.loads((ROOT/'EXPECTED.json').read_text())
    verify.need(stable == expected, 'expected entry-level replay')
    return {'status': stable['status'], 'tasks': stable['tasks'],
            'residual_physical_units': 29, 'solver_calls': 0,
            'elapsed_seconds': time.monotonic()-start,
            'maxrss_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
            'whole_parent_formulas': 'BOTH_UNKNOWN', 'good43_found': False}


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--branches', type=Path)
    group.add_argument('--rebuild', type=Path)
    parser.add_argument('--scratch', type=Path, required=True)
    args = parser.parse_args()
    branches = args.branches
    if args.rebuild is not None:
        command([sys.executable, '-B', ROOT.parent/'ramsey_r55_q10_regular_cnf_reduction'/'rebuild.py',
                 '--output', args.rebuild])
        branches = args.rebuild
    print(json.dumps(replay(branches, args.scratch), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
