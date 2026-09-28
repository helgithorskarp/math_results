"""Check the input identity used by EXTERNAL_TRADE_OVERLAP.md."""
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
FIXTURE_HASH = 'be1de027a09a08e6d78785a6af6ee126f7bc3f49bfa59f6061359566406d1a5a'
CERTIFICATE_HASH = '027b1c25df0ed2c21cbf25f653a8abb6e13bbc8dc2e0dfb868bc6da7a4812a81'
WORD_HASH = '58c26704225562a6cde8346f0febe1e09f5604c18f9ec0397e8bf16b3e3497b3'


def main():
    for name, digest in [('fixtures.json', FIXTURE_HASH),
                         ('class_splitting.json', CERTIFICATE_HASH)]:
        if hashlib.sha256((HERE / name).read_bytes()).hexdigest() != digest:
            raise ValueError('earlier input changed: ' + name)
    old = json.loads((HERE / 'fixtures.json').read_text())['near537']['colours']
    later = (HERE.parent / 'schur_s6_external_class_trade/seed537.txt').read_text().strip()
    if old != later or len(old) != 537 or set(old) - set('123456'):
        raise ValueError('inputs are not the same complete six-colour word')
    if hashlib.sha256((old + '\n').encode()).hexdigest() != WORD_HASH:
        raise ValueError('normalized word hash differs')
    word = [0] + list(map(int, old))
    defects = [(x, z-x, z, word[z]) for z in range(2, 538)
               for x in range(1, z//2+1) if word[x] == word[z-x] == word[z]]
    if defects != [(12, 12, 24, 4), (12, 24, 36, 4)]:
        raise ValueError('unexpected literal Schur defects')
    print('PASS identical_near537_word=yes length=537 defects=2 '
          'prior_fixture_and_certificate_hashes=yes')


if __name__ == '__main__':
    main()
