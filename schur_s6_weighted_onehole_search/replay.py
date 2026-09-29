"""Reproduce both deterministic whole-word local-search stages."""
import argparse
from pathlib import Path
import subprocess
import tempfile

from audit import defects

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'schur_s6_unrestricted_fullword_search'/'fullscore.cpp'


def run(binary, source, expected, seed, restarts):
    result=subprocess.run([str(binary),str(source),str(seed),str(restarts),
                           '100000','10','1','10','5'],check=True,
                          capture_output=True,text=True)
    word=next(line.split()[1] for line in result.stdout.splitlines()
              if line.startswith('BEST_COLOR '))
    assert word==expected.read_text(encoding='ascii').strip()
    print('PASS',expected.name,'seed',seed,'defects',len(defects(word)))


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--binary',type=Path)
    a=p.parse_args()
    def stages(binary):
        run(binary,HERE/'completed31.txt',HERE/'best3.txt',20261315,50)
        run(binary,HERE/'best3.txt',HERE/'best2.txt',20261316,100)
    if a.binary:stages(a.binary.resolve())
    else:
        with tempfile.TemporaryDirectory(prefix='schur-six-replay-') as temp:
            binary=Path(temp)/'fullscore'
            subprocess.run(['g++','-O3','-std=c++20',str(SOURCE),'-o',str(binary)],check=True)
            stages(binary)


if __name__=='__main__':main()
