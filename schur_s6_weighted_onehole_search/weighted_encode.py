"""Add a second copy of each at-least-one clause to the complete 537 CNF.

The duplicated clauses change local-search penalties, not satisfiability.
"""
import argparse
import hashlib
from pathlib import Path
import tempfile
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'schur_s6_unrestricted_fullword_search'))
from encode import write

PLAIN_SHA='fd6503a79cfeb53c614fe436669f192e81416b6e7292069938cf607f41b070e2'


def build(target):
    with tempfile.TemporaryDirectory(prefix='schur-six-weight-') as temp:
        plain=Path(temp)/'plain.cnf'
        write(plain,'plain')
        assert hashlib.sha256(plain.read_bytes()).hexdigest()==PLAIN_SHA
        with plain.open(encoding='ascii') as src, target.open('w',encoding='ascii') as out:
            assert src.readline().strip()=='p cnf 3222 441145'
            out.write('p cnf 3222 441682\n')
            for line in src:out.write(line)
            for v in range(1,538):
                out.write(' '.join(str(6*(v-1)+c) for c in range(1,7))+' 0\n')
    digest=hashlib.sha256(target.read_bytes()).hexdigest()
    print('variables=3222 clauses=441682 sha256='+digest)
    return digest


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('target',type=Path)
    a=p.parse_args()
    build(a.target)
