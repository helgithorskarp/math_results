"""Cold portable generation/replay; serial children and full normal/O comparison.

No generated input is required. Optional campaign operations state is read
only through DISCOVERY_RESEARCH_TEAM_ROOT when explicitly configured.
"""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
ENV = dict(os.environ, **{k: '1' for k in (
    'OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS')})


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(x):
    return hashlib.sha256(json.dumps(x, separators=(',', ':')).encode()).hexdigest()


def operations_barriers():
    configured = os.environ.get('DISCOVERY_RESEARCH_TEAM_ROOT')
    if not configured:
        return
    state = Path(configured)
    need(not any((state / p).exists() for p in ('PAUSED', 'PAUSED.json', 'monitor/PAUSED', 'monitor/PAUSED.json')),
         'operations pause barrier; preserve incomplete mathematics')
    h = json.loads((state / 'monitor/health.json').read_text())
    age = (datetime.now(timezone.utc) - datetime.fromisoformat(h['checked_at'])).total_seconds()
    need(0 <= age < 180 and not h.get('reasons') and h['credit_budget']['status'] == 'authorized',
         'operations health/budget barrier; no mathematical negative')
    need(json.loads((state / 'monitor/HANDOVER.json').read_text())['phase'] == 'completed',
         'incomplete operations handover')


def main():
    started = time.monotonic(); (ROOT / 'generated').mkdir(exist_ok=True)
    records, stages = {'normal': {}, 'optimized': {}}, []
    fixture = json.loads((ROOT / 'fixture.json').read_text())

    def stage(tool, mode, output, *args):
        operations_barriers()
        command = [sys.executable] + (['-O'] if mode == 'optimized' else []) + [str(ROOT / tool)]
        command += ['--output', str(ROOT / 'generated' / output)] + list(args)
        label = tool.removesuffix('.py') + '-' + mode + '-' + output
        print('START ' + label, flush=True); start = time.monotonic()
        child = subprocess.run(command, env=ENV, capture_output=True, text=True, timeout=55)
        (ROOT / 'generated' / (label + '.log')).write_text(child.stdout + child.stderr)
        need(child.returncode == 0, 'child incomplete, not nonexistence: ' + label + '\n' + child.stdout + child.stderr)
        result = json.loads((ROOT / 'generated' / output).read_text())
        field = 'whole_math_sha256' if 'whole_math_sha256' in result else 'entire_mathematical_record_sha256'
        need(digest(result['mathematical']) == result[field], 'entire child mathematical seal differs')
        item = {'stage': label, 'seconds': time.monotonic() - start,
                'maximum_rss_kib': result['maximum_rss_kib'], 'whole_math_sha256': result[field]}
        stages.append(item)
        (ROOT / 'generated/stages.json').write_text(json.dumps(stages, indent=2) + '\n')
        print(json.dumps(item), flush=True)
        return result['mathematical']

    for mode in records:
        records[mode]['packed_G_closure'] = stage('g4_catalogue.py', mode, 'g4-produced.json')
        records[mode]['scalar_G_closure'] = stage('check_g4.py', mode, 'g4-checked-' + mode + '.json',
                                                '--input', str(ROOT / 'generated/g4-produced.json'))
        records[mode]['packed_cover'] = stage('produce_cover.py', mode, 'cover-produced.json',
                                            '--library', str(ROOT / 'generated/g4-produced.json'))
        records[mode]['scalar_cover'] = stage('check_cover.py', mode, 'cover-checked-' + mode + '.json',
                                            '--input', str(ROOT / 'generated/cover-produced.json'))
    need(records['normal'] == records['optimized'], 'entire packed/scalar closure/cover records differ under -O')
    need(digest(records['normal']['packed_cover']) == fixture['expected_cover_math_sha256'] and
         digest(records['normal']['scalar_cover']) == fixture['expected_scalar_cover_math_sha256'],
         'cold complete candidate cover differs from sealed previous separate computations')
    for mode in records:
        records[mode]['positive45'] = stage('positive.py', mode, 'positive45-' + mode + '.json')
        records[mode]['root_rank_controls'] = stage('check_root_and_rank.py', mode, 'root-rank-' + mode + '.json')
        parts = []
        for start in range(0, 6400, 128):
            stop = min(start + 128, 6400)
            parts.append(stage('verify.py', mode, f'slice-{start}-{stop}-{mode}.json',
                               '--offset', str(start), '--cases', str(stop - start)))
        records[mode]['negative_slices'] = parts
    need(records['normal'] == records['optimized'], 'entire cold mathematical records differ under -O')
    math = records['normal']; ids, prep, heads, summary, originals = [], [], [], Counter(), set()
    damage_count = 0
    for p in math['negative_slices']:
        ids += p['selected_state_ids']; prep += p['actual_preparation_only_bindings']; heads += p['actual_head_tail_bindings']
        summary.update(p['summary']); originals.update(map(tuple, p['actual_original_domains']))
        damage_count += len(p['damages_rejected'])
    need(ids == list(range(6400)) and len(prep) == 6009 and len(heads) == 2864 and
         summary['preparation_only_classes'] == 6009 and summary['head_tail_classes'] == 391 and
         summary['actual_freed_heads'] == 1564 and summary['live_heads_by_actual10034'] == 782 and
         summary['covered_free_tail_alternatives'] == 76800, 'complete6400 actual coverage differs')
    kinds = {k: summary[k] for k in ('DIRECT_COST', 'TIGHT_FREE_CUT', 'TIGHT_MARKED_PORT_LOCK')}
    need(kinds == {'DIRECT_COST': 5857, 'TIGHT_FREE_CUT': 1981, 'TIGHT_MARKED_PORT_LOCK': 1035},
         'fresh sufficient binding counts differ')
    canonical = {'preparation': sorted(prep), 'head_tail': sorted(heads, key=lambda x:
                 (x['state_id'], x['head_partner'], -1 if x['tail_id'] is None else x['tail_id']))}
    c = json.loads((ROOT / 'certificate.json').read_text())
    need(digest(canonical) == c['expected_canonical_actual_bindings_sha256'],
         'every actual fresh original/word/cube/rank binding differs from sealed previous computations')
    controlled = {tuple(r[:2]) for r, sha in math['positive45']['all_used_actual_original_domain_controls']}
    need(originals <= controlled, 'actual negative original is absent from known45 positive controls')
    math['complete_conditional_four_binary_exclusion_relative_to_stated_imports'] = True
    math['unrestricted44_exclusion'] = False
    seal = digest(math)
    (ROOT / 'generated/entire-mathematical.json').write_text(json.dumps(math, separators=(',', ':')) + '\n')
    raw = (ROOT / 'certificate.json').read_bytes()
    checks = {'agent': 'six-sorting-2', 'role': 'researcher', 'status': 'COMPLETE_PORTABLE_SOURCE_ONLY_FOUR_BINARY_EXCLUSION',
              'python': sys.version.split()[0], 'mathematical_child_concurrency': 1, 'native_threads': 1,
              'per_child_guard_seconds': 55, 'entire_normal_optimized_records_equal': True,
              'entire_mathematical_sha256': seal, 'entire_canonical_actual_binding_sha256': digest(canonical),
              'raw_binary_forests': 2700, 'complete_four_input_functions': 261, 'complete_G_edges': 1566,
              'raw_BG_bindings': 111969, 'whole_Q_function_classes': 6400,
              'actual_negative_bindings': len(prep) + len(heads), 'summary': dict(summary),
              'original_negative_domains': len(originals), 'compact_witness_records': len(c['witnesses']),
              'numeric_ground_assignments_per_mode': math['scalar_cover']['fresh_ground_assignments'],
              'catalogue_semantic_rejections_per_mode': len(math['scalar_cover']['rejected_semantic_damages']),
              'G_closure_semantic_rejections_per_mode': len(math['scalar_G_closure']['rejected_semantic_damages']),
              'negative_and_coverage_semantic_rejections_per_mode': damage_count,
              'positive_Boolean_inputs_per_mode': 8192, 'positive_original_domains': len(controlled),
              'positive_numeric_assignments_per_mode': math['positive45']['original_assignments_sorted'],
              'root_head_tail_unit_checks_per_mode': math['root_rank_controls']['all76800_six_unit_head_tail_checks'],
              'certificate_bytes': len(raw), 'certificate_sha256': hashlib.sha256(raw).hexdigest(),
              'maximum_child_seconds': max(x['seconds'] for x in stages),
              'maximum_child_rss_kib': max(x['maximum_rss_kib'] for x in stages), 'stages': stages,
              'seconds': time.monotonic() - started, 'ordinary_bridges': 'written unformalized',
              'imported_live_head_lemma': '10034/0', 'independent_person_review': 'pending', 'global44_exclusion': False}
    expected = ROOT / 'checks.json'
    if expected.exists():
        old = json.loads(expected.read_text())
        need(old['entire_mathematical_sha256'] == seal and old['certificate_sha256'] == checks['certificate_sha256'],
             'whole cold source reproduction differs from compact expected result')
    (ROOT / 'generated/checks.json').write_text(json.dumps(checks, indent=2) + '\n')
    print(json.dumps({k: v for k, v in checks.items() if k != 'stages'}), flush=True)


if __name__ == '__main__':
    main()
