"""Audit YalSAT's near assignment against every plain CNF clause."""
import argparse
import hashlib
from pathlib import Path


def main():
    p=argparse.ArgumentParser()
    p.add_argument('log',type=Path)
    p.add_argument('cnf',type=Path)
    p.add_argument('--out',type=Path,default=Path('/tmp/schur-six-partial537.txt'))
    a=p.parse_args()
    signed=[int(t) for line in a.log.read_text(encoding='ascii').splitlines()
            if line.startswith('v ') for t in line.split()[1:] if t!='0']
    assert len(signed)==3222 and {abs(t) for t in signed}==set(range(1,3223))
    true={t for t in signed if t>0}
    false={-t for t in signed if t<0}
    unsatisfied=[]
    with a.cnf.open(encoding='ascii') as f:
        assert f.readline().split()==['p','cnf','3222','441145']
        for number,line in enumerate(f,1):
            lits=list(map(int,line.split()))
            assert lits[-1]==0
            if not any(lit in true if lit>0 else -lit in false for lit in lits[:-1]):
                unsatisfied.append((number,lits[:-1]))
    assert len(unsatisfied)==2 and all(len(row)==6 for _,row in unsatisfied)
    partial=[]
    for v in range(1,538):
        colours=[str(c) for c in range(1,7) if 6*(v-1)+c in true]
        assert len(colours)<=1
        partial.append(colours[0] if colours else '?')
    word=''.join(partial)
    assert [v for v,c in enumerate(word,1) if c=='?']==[2,4]
    digest=hashlib.sha256((word+'\n').encode()).hexdigest()
    a.out.write_text(word+'\n',encoding='ascii')
    print(f'PASS variables=3222 unsatisfied_clauses=2 holes=2,4 '
          f'partial_sha256={digest} out={a.out}')


if __name__=='__main__':main()
