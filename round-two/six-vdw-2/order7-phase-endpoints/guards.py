"""Concrete coverage, counter, source-before-import and proof corruption controls."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from common import BASE, HERE, pins, require


def main(work, output):
    began = time.monotonic()
    pins()
    require(not output.exists(), 'fresh corruption directory required')
    output.mkdir(parents=True)
    python = Path(sys.executable).absolute()
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1',
               MKL_NUM_THREADS='1', BLIS_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1')
    tests = []

    def rejected(name, argv, phrase=None, cwd=None):
        result = subprocess.run(list(map(str, argv)), capture_output=True, text=True,
                                timeout=55, env=env, cwd=cwd)
        require(result.returncode != 0 and (phrase is None or phrase in result.stderr),
                'corruption was accepted or failed unexpectedly: '+name)
        tests.append(name)

    for label, flags in [('normal', []), ('optimized', ['-O'])]:
        for missing in ('b-0-case-4', 'd-1-b-1'):
            case = output / (label+'-missing-'+missing)
            case.mkdir()
            data = json.loads((work / 'models.json').read_text())
            data['cases'] = [r for r in data['cases'] if r['stem'] != missing]
            (case / 'models.json').write_text(json.dumps(data))
            rejected(label+'-missing-'+missing,
                     [python, *flags, HERE / 'audit.py', '--work', case],
                     'incomplete or duplicated endpoint cover')
        case = output / (label+'-counter-unit')
        case.mkdir()
        shutil.copyfile(work / 'models.json', case / 'models.json')
        for path in work.glob('*.cnf'):
            (case / path.name).symlink_to(path.absolute())
        target = case / 'd-5-b-0.cnf'
        text = target.read_text()
        require('\n268 0\n' in text, 'expected exact-five unit absent')
        target.unlink()  # Never modify the verified target behind the symlink.
        target.write_text(text.replace('\n268 0\n', '\n-268 0\n', 1))
        rejected(label+'-wrong-exact-five-unit',
                 [python, *flags, HERE / 'audit.py', '--work', case], 'wrong exact-five units')

        isolated = output / (label+'-changed-helper')
        here = isolated / 'order7-phase-endpoints'
        base = isolated / 'order7-geometric-cut'
        phase = isolated / 'order7-antipodal-geography'
        for directory in (here, base, phase):
            directory.mkdir(parents=True)
        for name in ('common.py', 'SOURCE_PINS.json'):
            shutil.copyfile(HERE / name, here / name)
        for name in json.loads((HERE / 'SOURCE_PINS.json').read_text())['files']:
            shutil.copyfile(BASE / name, base / name)
        shutil.copyfile(HERE.parent / 'order7-antipodal-geography' / 'PROOF.md', phase / 'PROOF.md')
        with (base / 'encode.py').open('a') as stream:
            stream.write('\nraise RuntimeError("EXECUTED_CHANGED_HELPER")\n')
        rejected(label+'-changed-helper-before-import',
                 [python, *flags, '-c', 'import common; common.load_encoder()'],
                 'changed helper: encode.py', here)

        cnf = work / 'b-0-case-1.cnf'
        initial = int(cnf.read_text().splitlines()[0].split()[3])
        for name, tail in [('empty-without-hints', '0 0'),
                           ('missing-live-hint', '0 999999999 0')]:
            proof = output / (label+'-'+name+'.lrat')
            proof.write_text(str(initial+1)+' '+tail+'\n')
            rejected(label+'-'+name, [python, *flags, BASE / 'check_rup_lrat.py', cnf, proof])
    result = dict(status='ALL_CORRUPTION_CONTROLS_REJECTED', tests=tests,
                  rejected=len(tests), seconds=time.monotonic()-began)
    (output / 'result.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    main(args.work.absolute(), args.output.absolute())
