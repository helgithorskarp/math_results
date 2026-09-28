"""Compare the public 536-digit baseline with the 2000 paper's printed list."""

import argparse
import re
from pathlib import Path

from pypdf import PdfReader

parser = argparse.ArgumentParser()
parser.add_argument('pdf', type=Path, help='Fredricksen--Sweet 2000 article PDF')
args = parser.parse_args()
BASELINE = Path(__file__).resolve().parent.parent / 'schur_s6_fredricksen_sweet_distance' / 'baseline.txt'

# The PDF's compact Type 1 font concatenates the first line of each set in
# text extraction. These six lines were transcribed from page 6 visually/textually.
first_lines = {
    1: '1 5 8 11 14 24 27 30 33 36 40 43 46 49',
    2: '2 12 19 25 26 34 41 57 58 63 72 79 85 86',
    3: '3 10 16 22 23 29 35 42 48 56 60 62 67 68',
    4: '4 13 20 28 31 38 50 61 64 73 83 91 98 108',
    5: '6 9 17 21 32 39 44 51 54 55 66 70 82 89',
    6: '7 15 18 37 45 47 53 59 76 78 97 105 116 122',
}

text = PdfReader(str(args.pdf)).pages[5].extract_text()
block = text.split('Partition of 536 into 6 symmetric sumfree sets:', 1)[1].split('(D(P) = 161)', 1)[0]
blocks = re.split(r'(?:S e t|Set )([1-6])\s*:', block)
assert len(blocks) == 13
source = {}
for k in range(1, len(blocks), 2):
    c = int(blocks[k])
    lines = blocks[k + 1].strip().splitlines()
    numbers = [int(v) for v in first_lines[c].split()]
    numbers += [int(v) for line in lines[1:] for v in line.split()]
    assert len(numbers) == len(set(numbers))
    for n in numbers:
        assert n not in source
        source[n] = c
assert set(source) == set(range(1, 269)) | {358}
assert source[179] == 4 and source[358] == 1
computed = {}
for n, c in source.items():
    computed[n] = c
    if n not in (179, 358):
        computed[537 - n] = c
assert set(computed) == set(range(1, 537))
actual = [int(v) for v in BASELINE.read_text().strip()]
assert all(computed[n] == actual[n - 1] for n in range(1, 537))
print('PASS paper_baseline_match source_entries=269 colors=536 exceptional_pair=179,358')
