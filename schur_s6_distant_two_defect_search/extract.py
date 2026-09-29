"""Extract a fully audited two-hole word from a YalSAT DIMACS witness log."""
import argparse
from pathlib import Path
from audit import defects


def extract(path):
    signed = [int(token) for line in path.read_text(encoding='ascii').splitlines()
              if line.startswith('v ') for token in line.split()[1:] if token != '0']
    assert len(signed) == 3222
    assert {abs(lit) for lit in signed} == set(range(1,3223))
    true = {lit for lit in signed if lit > 0}
    colour = []
    for v in range(1,538):
        options = [str(c) for c in range(1,7) if 6*(v-1)+c in true]
        assert len(options) <= 1
        colour.append(options[0] if options else '?')
    word = ''.join(colour)
    assert word.count('?') == 2 and defects(word) == []
    return word


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('log', type=Path)
    p.add_argument('out', type=Path)
    a = p.parse_args()
    word = extract(a.log)
    a.out.write_text(word+'\n', encoding='ascii')
    print('holes', [i for i,c in enumerate(word,1) if c=='?'], 'out', a.out)
