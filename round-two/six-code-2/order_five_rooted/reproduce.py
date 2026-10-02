"""Serial, guarded cold reproduction of the scoped equality classification."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time


def need(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    expected = json.loads((source / 'EXPECTED.json').read_text())
    need(not args.work.exists(), 'cold reproduction requires a new work directory')
    args.work.mkdir(parents=True)
    for name, receipt in expected['source_files'].items():
        raw = (source / name).read_bytes()
        need(len(raw) == receipt['bytes'] and hashlib.sha256(raw).hexdigest() == receipt['sha256'], 'source changed: ' + name)
    model = args.work / 'model'; roots = args.work / 'roots'; cover = args.work / 'cover'
    equality = args.work / 'equality'; saturation = args.work / 'saturation'
    instance = source / 'INSTANCE.json'
    steps = [
        ('generate.py', ['--instance', instance, '--work', model]),
        ('roots.py', ['--model', model / 'ORBIT_MODEL.json', '--baseline', model / 'BASELINE68.json', '--work', roots]),
        ('root_audit.py', ['--model', model / 'ORBIT_MODEL.json', '--production', roots, '--work', args.work / 'root-audit']),
        ('cover.py', ['--model', model / 'ORBIT_MODEL.json', '--roots', roots / 'ROOTS.json', '--seed', '86', '--work', cover]),
        ('equality.py', ['--model', model / 'ORBIT_MODEL.json', '--roots', roots / 'ROOTS.json', '--seed', '86', '--work', equality]),
        ('equality_audit.py', ['--instance', instance, '--equality', equality, '--work', args.work / 'equality-audit']),
        ('construct.py', ['--instance', instance, '--completions', equality / 'COMPLETIONS68.json', '--work', args.work / 'construct']),
        ('saturation.py', ['--instance', instance, '--cover', cover / 'COVER.json', '--completions', equality / 'COMPLETIONS68.json', '--work', saturation]),
        ('saturation_audit.py', ['--instance', instance, '--roots', roots / 'ROOTS.json', '--cover', cover / 'COVER.json',
                                 '--completions', equality / 'COMPLETIONS68.json', '--saturation', saturation, '--work', args.work / 'saturation-audit'])]
    begin = time.monotonic()
    phases = []
    for script, arguments in steps:
        cmd = [sys.executable, '-B'] + (['-O'] if sys.flags.optimize else []) + [str(source / script)] + list(map(str, arguments))
        start = time.monotonic()
        try:
            result = subprocess.run(cmd, capture_output=True, check=True, timeout=60)
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as error:
            (args.work / 'INCOMPLETE.json').write_text(json.dumps({'status': 'INCOMPLETE_NO_CLASSIFICATION_CLAIM', 'phase': script}) + '\n')
            if isinstance(error, subprocess.CalledProcessError):
                sys.stderr.write(error.stderr.decode())
            raise
        (args.work / (script + '.stdout')).write_bytes(result.stdout)
        phases.append({'phase': script, 'seconds': time.monotonic() - start})
    for path, receipt in expected['evidence_files'].items():
        raw = (args.work / path).read_bytes()
        need(len(raw) == receipt['bytes'] and hashlib.sha256(raw).hexdigest() == receipt['sha256'], 'evidence differs: ' + path)
    for name, generated in [('COUNT_CERTIFICATE.json', equality / 'COUNT_CERTIFICATE.json'),
                            ('CLASSIFICATION.json', saturation / 'CLASSIFICATION.json'),
                            ('CONSTRUCTIONS.json', args.work / 'construct/CONSTRUCTIONS.json')]:
        need((source / name).read_bytes() == generated.read_bytes(), 'published compact evidence differs: ' + name)
    records = {name: json.loads((args.work / name / 'AUDIT.json').read_text())
               for name in ('root-audit', 'equality-audit', 'saturation-audit')}
    need(records['root-audit']['actual_rooted20_stars'] == 100 and records['equality-audit']['verified_exact68_completions'] == 32 and
         records['saturation-audit']['all_labelled_codes'] == 5850 and records['saturation-audit']['centralizer_classes'] == 8,
         'unexpected mathematical result')
    need([len(records[name]['semantic_damage_rejections']) for name in records] == [5, 10, 6], 'missing semantic controls')
    exact = {'agent': 'six-code-2', 'role': 'researcher', 'status': 'COMPLETE_EXACT_COLD_REPRODUCTION_AND_AUDIT',
             'all_rooted20_stars': 100, 'normalized68_completions': 32, 'root_zero_labelled_codes': 3200,
             'all_labelled_saturated_fixed_point_codes': 5850, 'centralizer_classes': 8,
             'centralizer_class_sizes': records['saturation-audit']['class_sizes'],
             'saturated_fixed_point_histogram': records['saturation-audit']['saturated_fixed_point_histogram'],
             'degree_profile_histogram': records['saturation-audit']['degree_profile_histogram'],
             'counting_certificate_nodes': 255, 'semantic_damage_counts': [5, 10, 6], 'solver_used_or_trusted': False,
             'scope': 'Exact68 codes invariant under the specified C5 action and with at least one fixed point of degree20. Centralizer classes only; no unsaturated-fixed-point or arbitrary point-isomorphism classification.'}
    exact_raw = (json.dumps(exact, sort_keys=True, separators=(',', ':')) + '\n').encode()
    (args.work / 'EXACT_RESULT.json').write_bytes(exact_raw)
    need(hashlib.sha256(exact_raw).hexdigest() == expected['exact_result_sha256'], 'cold exact result differs from frozen expectation')
    (args.work / 'EXECUTION.json').write_text(json.dumps({'seconds': time.monotonic() - begin, 'phases': phases,
                                                        'python': sys.version, 'optimized': bool(sys.flags.optimize)}, sort_keys=True, indent=2) + '\n')
    print(exact_raw.decode(), end='')


if __name__ == '__main__':
    main()
