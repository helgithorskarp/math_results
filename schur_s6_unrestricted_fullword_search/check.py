"""Definition-level check of a complete classical six-colouring through 537."""
import argparse
from pathlib import Path


def defects(word):
    assert len(word) == 537 and set(word) <= set('123456')
    return [(x, z-x, z)
            for z in range(2, 538)
            for x in range(1, z//2+1)
            if word[x-1] == word[z-x-1] == word[z-1]]


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('word', type=Path)
    a = p.parse_args()
    word = a.word.read_text(encoding='ascii').strip()
    bad = defects(word)
    print(f'positions={len(word)} triples=72092 defects={len(bad)} '
          f'doubling_defects={sum(x == y for x,y,z in bad)}')
    if bad:print('first_defects', bad[:20])
    else:print('VERIFIED S(6)>=537')
