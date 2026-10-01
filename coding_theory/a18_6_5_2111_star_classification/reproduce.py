#!/usr/bin/env python3
"""Reproduce the complete eight-class certificate with two cover kernels."""
from contextlib import redirect_stdout
import io
import json
import os
import resource
import subprocess
import time

import carrier as c
import hub_carrier as h
import second_hub as s
import classify as k
from paths import BASE, WORK


def write(name, value):
    (WORK / name).write_text(json.dumps(value, indent=2) + '\n')


def matrix_text(required, rows):
    lines = [f'{len(required)} {len(rows)} 6']
    lines.extend(str(word) + ' ' + ' '.join(map(str, columns)) for word, columns in rows)
    lines += ['1', '0 0']
    return '\n'.join(lines) + '\n'


def full_fiber(index, prefix_index, record, orbit, expected):
    partition = tuple(map(tuple, orbit['representative']))
    prefix, required, rows = h.residual_matrix(record, partition)
    if len(rows) != expected['hub_candidates'] or c.digest([required, rows]) != expected['hub_matrix_sha256']:
        raise RuntimeError('hub matrix definition differs from compact certificate')
    inp = WORK / f'hub_{index}_{prefix_index}_fullcover.input'
    inp.write_text(matrix_text(required, rows))
    answers = []
    for kernel in ('fullcover', 'dlx'):
        out = WORK / f'hub_{index}_{prefix_index}_{kernel}.jsonl'
        result = subprocess.run([str(WORK / kernel), str(inp), str(out)],
                                capture_output=True, text=True, timeout=20)
        if result.returncode:
            raise RuntimeError('INCOMPLETE native fiber; no verdict: ' + result.stderr)
        summary = json.loads(result.stdout)
        answer = json.loads(out.read_text())
        if summary['status'] != 'COMPLETE' or summary['cases'] != 1 or answer['index'] != 0:
            raise RuntimeError('malformed native completion status')
        if len(answer['covers']) != expected['covers'] or c.digest(answer['covers']) != expected['covers_sha256']:
            raise RuntimeError('native covers differ from compact certificate')
        if answer['nodes'] != expected['primary_nodes' if kernel == 'fullcover' else 'sparse_nodes']:
            raise RuntimeError('native deterministic node count differs')
        if answers and answer['covers'] != answers[0]['covers']:
            raise RuntimeError('all covers differ entry by entry between native representations')
        answers.append(answer)
    for words in answers[0]['covers']:
        star = tuple(sorted(prefix + tuple(words)))
        c.validate_star(star, list(map(tuple, record['leave'])))
        if len(words) != 17 or h.shorten_hub(star) != partition:
            raise RuntimeError('literal returned star differs from fixed hub prefix')
    return dict(index=index, prefix_index=prefix_index, covers=len(answers[0]['covers']),
                primary_nodes=answers[0]['nodes'], sparse_nodes=answers[1]['nodes'],
                matrix_sha256=c.digest([required, rows]))


def main():
    started = time.monotonic()
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        os.environ[name] = '1'
    expected = json.loads((BASE / 'expected.json').read_text())
    progress = dict(agent='six-code-3', role='researcher', status='INCOMPLETE', fibers=[])
    write('proof_run.json', progress)
    try:
        leaves = c.build()
        write('leave_carrier.json', leaves)
        with redirect_stdout(io.StringIO()):
            h.main()
        hub = json.loads((WORK / 'hub_carrier.json').read_text())
        if c.digest(leaves) != expected['leave_carrier_sha256']:
            raise RuntimeError('complete leave carrier differs')
        if c.digest({key: value for key, value in hub.items() if key not in ('seconds', 'maxrss_kib')}) != expected['hub_carrier_sha256']:
            raise RuntimeError('complete independently checked hub carrier differs')
        for kernel, source in (('fullcover', 'bitset.cpp'), ('dlx', 'dlx.cpp')):
            subprocess.run(['g++'] + expected['compiler_flags'] + [str(BASE / source), '-o', str(WORK / kernel)], check=True)
        wanted = {(q['index'], q['prefix_index']): q for q in expected['fibers']}
        domain = [(q['index'], orbit['index']) for q in hub['cases'] for orbit in q['orbits']]
        if len(wanted) != 75 or len(expected['fibers']) != 75 or set(wanted) != set(domain):
            raise RuntimeError('expected fibers do not cover complete hub carrier exactly once')
        positives = []
        for index, prefix_index in domain:
            record = leaves['cases'][index]
            orbit = hub['cases'][index]['orbits'][prefix_index]
            spec = wanted[index, prefix_index]
            if (index, prefix_index) == (5, 0):
                partition = tuple(map(tuple, orbit['representative']))
                _, required, rows = h.residual_matrix(record, partition)
                if spec['mode'] != 'second-star-quotient' or c.digest([required, rows]) != spec['hub_matrix_sha256']:
                    raise RuntimeError('next-star exceptional fiber definition differs')
                with redirect_stdout(io.StringIO()):
                    s.main()
                actual = json.loads((WORK / 'twice_5_0.json').read_text())
                if actual['status'] != 'COMPLETE both exhaustive residual cover censuses agree entrywise':
                    raise RuntimeError('INCOMPLETE next-star quotient or cover census')
                for key in ('columns', 'candidates', 'matrix_sha256', 'covers', 'primary_nodes', 'sparse_nodes'):
                    if actual[key] != spec[key]:
                        raise RuntimeError('next-star fiber differs: ' + key)
                if actual['output_sha256'] != spec['covers_sha256']:
                    raise RuntimeError('next-star complete cover output differs')
                for key, value in expected['next_star_normalization'].items():
                    if actual[key] != value:
                        raise RuntimeError('entrywise next-star normalization differs: ' + key)
                result = dict(index=index, prefix_index=prefix_index, covers=actual['covers'],
                              primary_nodes=actual['primary_nodes'], sparse_nodes=actual['sparse_nodes'],
                              matrix_sha256=actual['matrix_sha256'])
                positives.append(dict(index=index, prefix_index=prefix_index))
            else:
                if spec['mode'] != 'hub-only':
                    raise RuntimeError('unexpected fiber mode')
                result = full_fiber(index, prefix_index, record, orbit, spec)
                if result['covers']:
                    positives.append(dict(index=index, prefix_index=prefix_index))
            progress['fibers'].append(result)
            write('proof_run.json', progress)
            if len(progress['fibers']) % 15 == 0:
                print(json.dumps(dict(complete_native_fibers=len(progress['fibers']), expected_fibers=75)), flush=True)
        if len(positives) != 6:
            raise RuntimeError('positive fiber carrier differs')
        write('hub_feasibility.json', dict(status='COMPLETE HUB-PREFIX FEASIBILITY CLASSIFICATION', positives=positives))
        k.main()
        progress.update(status='COMPLETE finite enumeration; compact certificate check pending',
                        seconds=round(time.monotonic() - started, 6),
                        parent_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                        child_maxrss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        write('proof_run.json', progress)
        import verify
        verify.check(False)
        progress['status'] = 'COMPLETE and compact certificate verified'
        write('proof_run.json', progress)
        print(json.dumps({key: value for key, value in progress.items() if key != 'fibers'}), flush=True)
    except Exception as error:
        progress.update(status='INCOMPLETE; no overall classification verdict', failure=str(error),
                        seconds=round(time.monotonic() - started, 6))
        write('proof_run.json', progress)
        raise


if __name__ == '__main__':
    main()
