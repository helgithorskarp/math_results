"""Independently check a SAT solver's complete 537-colouring witness."""
import argparse
import hashlib
from pathlib import Path


def check(log, out):
    lines = log.read_text(encoding='ascii').splitlines()
    assert any(line.strip() == 's SATISFIABLE' for line in lines)
    positive = {int(token) for line in lines if line.startswith('v ')
                for token in line.split()[1:] if int(token) > 0}
    digits = []
    for v in range(1, 538):
        choices = [c for c in range(1, 7) if 6 * (v - 1) + c in positive]
        assert len(choices) == 1, (v, choices)
        digits.append(str(choices[0]))
    word = ''.join(digits)
    count = 0
    for x in range(1, 538):
        for y in range(x, 538 - x):
            z = x + y
            count += 1
            assert not (word[x-1] == word[y-1] == word[z-1]), (x, y, z)
    assert count == 72092
    out.write_text(word + '\n', encoding='ascii')
    print('VERIFIED537', 'sha256', hashlib.sha256((word+'\n').encode()).hexdigest(),
          'out', out)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('log', type=Path)
    p.add_argument('out', type=Path)
    a = p.parse_args()
    check(a.log, a.out)
