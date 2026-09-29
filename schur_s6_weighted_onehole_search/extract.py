"""Check a YalSAT witness on the weighted CNF and extract its one-hole word."""
import argparse
from pathlib import Path
from audit import defects


def main():
    p=argparse.ArgumentParser()
    p.add_argument('log',type=Path)
    p.add_argument('weighted_cnf',type=Path)
    p.add_argument('out',type=Path)
    a=p.parse_args()
    signed=[int(t) for line in a.log.read_text(encoding='ascii').splitlines()
            if line.startswith('v ') for t in line.split()[1:] if t!='0']
    assert len(signed)==3222 and {abs(t) for t in signed}==set(range(1,3223))
    true={t for t in signed if t>0}
    false={-t for t in signed if t<0}
    missing=[]
    with a.weighted_cnf.open(encoding='ascii') as f:
        assert f.readline().strip()=='p cnf 3222 441682'
        for number,line in enumerate(f,1):
            lits=[int(t) for t in line.split()]
            assert lits[-1]==0
            if not any(t in true if t>0 else -t in false for t in lits[:-1]):
                missing.append((number,lits[:-1]))
        assert number==441682
    word=[]
    for v in range(1,538):
        colours=[str(c) for c in range(1,7) if 6*(v-1)+c in true]
        assert len(colours)<=1
        word.append(colours[0] if colours else '?')
    word=''.join(word)
    assert [v for v,c in enumerate(word,1) if c=='?']==[35]
    assert defects(word)==[]
    assert len(missing)==2 and all(len(row)==6 for _,row in missing)
    a.out.write_text(word+'\n',encoding='ascii')
    print('PASS holes=35 weighted_unsatisfied=2 out='+str(a.out))


if __name__=='__main__':main()
