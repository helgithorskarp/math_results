"""Replay the two deterministic whole-word continuations."""
import argparse
from pathlib import Path
import subprocess
import tempfile

from audit import defects

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent/'schur_s6_unrestricted_fullword_search'/'fullscore.cpp'


def run(binary, source, expected, seed, restarts, kick, global_noise, local_noise, tabu):
    result = subprocess.run([str(binary), str(source), str(seed), str(restarts),
                             '100000', str(kick), str(global_noise),
                             str(local_noise), str(tabu)], check=True,
                            capture_output=True, text=True)
    lines = result.stdout.splitlines()
    word = next(line.split()[1] for line in lines if line.startswith('BEST_COLOR '))
    saved = expected.read_text(encoding='ascii').strip()
    assert word == saved
    assert len(defects(word)) == int(lines[-2].split('defects=')[1].split()[0])
    print('PASS', expected.name, 'seed', seed, 'defects', len(defects(word)))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--binary', type=Path,
                   help='already compiled fullscore.cpp; compile from sibling source if omitted')
    a = p.parse_args()
    if a.binary:
        binary = a.binary.resolve()
        run(binary, HERE/'completed29.txt', HERE/'best3.txt', 20261102,
            50, 20, 3, 15, 7)
        run(binary, HERE/'best3.txt', HERE/'best2.txt', 20261203,
            100, 10, 1, 10, 5)
    else:
        with tempfile.TemporaryDirectory(prefix='schur-six-replay-') as temp:
            binary = Path(temp)/'fullscore'
            subprocess.run(['g++', '-O3', '-std=c++20', str(SOURCE),
                            '-o', str(binary)], check=True)
            run(binary, HERE/'completed29.txt', HERE/'best3.txt', 20261102,
                50, 20, 3, 15, 7)
            run(binary, HERE/'best3.txt', HERE/'best2.txt', 20261203,
                100, 10, 1, 10, 5)


if __name__ == '__main__':
    main()
