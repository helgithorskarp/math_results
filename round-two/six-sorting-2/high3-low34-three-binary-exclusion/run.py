"""Fresh portable serial replay, with full normal/optimized record comparison."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from collections import Counter

ROOT = Path(__file__).resolve().parent
ENV = dict(os.environ, **{k: '1' for k in (
    'OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS')})


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(x):
    return hashlib.sha256(json.dumps(x, separators=(',', ':')).encode()).hexdigest()


def main():
    started = time.monotonic()
    (ROOT / 'generated').mkdir(exist_ok=True)
    stages, records = [], {'normal': {}, 'optimized': {}}

    def stage(tool, mode, output, *args):
        command = [sys.executable] + (['-O'] if mode == 'optimized' else []) + [str(ROOT / tool)]
        if output is not None:
            command.extend(['--output', str(ROOT / 'generated' / output)])
        command.extend(args)
        label = tool.removesuffix('.py') + '-' + mode + ('-' + output if output else '')
        print('START ' + label, flush=True)
        start = time.monotonic()
        child = subprocess.run(command, capture_output=True, text=True, env=ENV, timeout=55)
        (ROOT / 'generated' / (label + '.log')).write_text(child.stdout + child.stderr)
        need(child.returncode == 0, 'child incomplete, not mathematical nonexistence: ' + label + '\n' + child.stdout + child.stderr)
        path = ROOT / 'generated' / output if output else ROOT / 'generated' / ('catalogue-damages-' + mode + '.json')
        result = json.loads(path.read_text())
        need(digest(result['mathematical']) == result['entire_mathematical_record_sha256'], 'entire child record seal differs')
        entry = {'stage': label, 'seconds': time.monotonic() - start,
                 'maximum_rss_kib': result['maximum_rss_kib'], 'whole_math_sha256': result['entire_mathematical_record_sha256']}
        stages.append(entry)
        print(json.dumps(entry), flush=True)
        return result['mathematical']

    for mode in records:
        records[mode]['packed_cover'] = stage('generate_cover.py', mode, 'cover-produced.json')
        records[mode]['scalar_cover'] = stage('check_cover.py', mode, 'cover-checked-' + mode + '.json')
    need(records['normal'] == records['optimized'], 'whole producer/scalar cover records differ under -O')
    for mode in records:
        records[mode]['catalogue_damages'] = stage('catalogue_damages.py', mode, None)
        records[mode]['positive45_original_controls'] = stage('positive.py', mode, 'positive45-' + mode + '.json')
        slices = []
        for start in range(0, 1042, 32):
            stop = min(start + 32, 1042)
            slices.append(stage('verify.py', mode, f'slice-{start}-{stop}-{mode}.json',
                                '--offset', str(start), '--cases', str(stop - start)))
        records[mode]['negative_slices'] = slices
    need(records['normal'] == records['optimized'], 'entire normal/optimized mathematical records differ')
    math = records['normal']
    ids, bindings, summary = [], [], Counter()
    damages = 0
    for part in math['negative_slices']:
        ids.extend(part['selected_state_ids'])
        bindings.extend(part['all_actual_negative_bindings'])
        summary.update(part['summary'])
        damages += len(part['damages_rejected'])
    need(ids == list(range(1042)) and len(bindings) == 4164 and summary['freed_heads'] == 3126 and
         summary['covered_free_tail_alternatives'] == 9378 and summary['live_heads_by_actual10034'] == 3126,
         'complete1042 actual partition missing, duplicated or insufficient')
    need(digest(bindings) == '84d1659baf71c24ec1eb313b453a6126537d776c333439443320b7e3d22b72b5',
         'entire fresh actual-original binding record differs from prior separate algorithms')
    math['complete_conditional_three_binary_exclusion'] = True
    math['unrestricted44_exclusion'] = False
    seal = digest(math)
    (ROOT / 'generated/entire-mathematical.json').write_text(json.dumps(math, separators=(',', ':')) + '\n')
    certificate = (ROOT / 'certificate.json').read_bytes()
    checks = {'agent': 'six-sorting-2', 'role': 'researcher', 'status': 'COMPLETE_PORTABLE_SOURCE_ONLY_THREE_BINARY_EXCLUSION',
        'python': sys.version.split()[0], 'mathematical_child_concurrency': 1, 'native_threads': 1,
        'per_child_guard_seconds': 55, 'entire_normal_optimized_records_equal': True,
        'entire_mathematical_sha256': seal, 'entire_actual_negative_binding_sha256': digest(bindings),
        'raw_binary_forests': 900, 'complete_three_input_functions': 11, 'raw_BG_words': 3597,
        'whole_Q_function_classes': 1042, 'actual_negative_bindings': len(bindings), 'summary': dict(summary),
        'catalogue_semantic_rejections_per_mode': len(math['catalogue_damages']['catalogue_damages_rejected']),
        'negative_semantic_rejections_per_mode': damages, 'positive_sorter_Boolean_inputs_per_mode': 8192,
        'positive_original_domains': len(math['positive45_original_controls']['all_used_actual_original_domain_controls']),
        'positive_numeric_assignments_per_mode': math['positive45_original_controls']['original_assignments_sorted'],
        'numeric_ground_assignments_per_mode': math['scalar_cover']['fresh_ground_assignments'],
        'certificate_bytes': len(certificate), 'certificate_sha256': hashlib.sha256(certificate).hexdigest(),
        'maximum_child_rss_kib': max(s['maximum_rss_kib'] for s in stages),
        'maximum_child_seconds': max(s['seconds'] for s in stages), 'stages': stages,
        'seconds': time.monotonic() - started, 'ordinary_bridges': 'written unformalized',
        'imported_live_head_lemma': '10034/0', 'independent_person_review': 'pending', 'global44_exclusion': False}
    expected = ROOT / 'checks.json'
    if expected.exists():
        previous = json.loads(expected.read_text())
        need(previous['entire_mathematical_sha256'] == seal and previous['certificate_sha256'] == checks['certificate_sha256'],
             'full source-only reproduction differs from the compact expected result')
    (ROOT / 'generated/checks.json').write_text(json.dumps(checks, indent=2) + '\n')
    print(json.dumps({k: v for k, v in checks.items() if k != 'stages'}), flush=True)


if __name__ == '__main__':
    main()
