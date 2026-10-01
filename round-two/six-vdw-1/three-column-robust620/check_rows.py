"""Helper-free literal check of the full row partition and affine orbit cover."""
import argparse
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def audit(path):
    data = json.loads(path.read_text())
    require(data['author'] == 'six-vdw-1' and data['role'] == 'researcher', 'author/role')
    seen = set()
    rejected = data['rejection_records']
    for record in rejected:
        require(len(record) == 4, 'row rejection record schema')
        mask, start, step, color = record
        require(all(type(x) is int for x in record), 'integer row record')
        require(0 <= mask < 1024 and mask not in seen, 'duplicate/outside row record')
        require(0 <= start < 20 and 0 < step < 20 and color in [0, 1], 'literal row AP bounds')
        full = mask | ((mask ^ 1023) << 10)
        require(all(((full >> ((start + j*step) % 20)) & 1) == color for j in range(7)), 'invalid row witness')
        seen.add(mask)
    units = [a for a in range(20) if any(a*b % 20 == 1 for b in range(20))]
    representatives = []
    cases = []
    for orbit in data['orbits']:
        rep = orbit['representative']
        members = orbit['members']
        require(members == sorted(set(members)) and members and rep == members[0], 'canonical row orbit')
        full = rep | ((rep ^ 1023) << 10)
        images = set()
        # Push each actual point forward, unlike the producer's pullback.
        for multiplier in units:
            for translation in range(20):
                image = 0
                for point in range(20):
                    if (full >> point) & 1:
                        image |= 1 << ((multiplier*point + translation) % 20)
                low = image & 1023
                require(image >> 10 == (low ^ 1023), 'affine image lost opposite halves')
                images.add(low)
        require(images == set(members), 'incorrect affine orbit cover')
        for mask in members:
            require(type(mask) is int and 0 <= mask < 1024 and mask not in seen, 'overlapping/outside orbit')
            actual = mask | ((mask ^ 1023) << 10)
            codes = set()
            for first in range(20):
                for second in range(20):
                    points = [(first + j*(second-first)) % 20 for j in range(7)]
                    code = sum(((actual >> x) & 1) << j for j, x in enumerate(points))
                    codes.add(code)
                    if first != second:
                        require(code not in [0, 127], 'surviving row contains a monochromatic AP')
            require(sorted(codes) == orbit['patterns'], 'incorrect row progression signature')
            require(sorted(set(range(128)) - codes) == orbit['missing_patterns'], 'incorrect allowed signature')
            require({p ^ 127 for p in codes} == codes, 'missing complementary pattern')
            seen.add(mask)
        representatives.append(rep)
        cases.append([rep, len(members), len(orbit['patterns'])])
    require(seen == set(range(1024)), 'incomplete row partition')
    require(representatives == [8, 10, 12, 16, 20, 34, 72], 'case list differs from both native tools')
    require(data['opposite_half_rows'] == 1024 and data['rejected_rows'] == len(rejected) == 444
            and data['surviving_rows'] == 580 and data['affine_group_order'] == len(units)*20 == 160
            and data['affine_orbits'] == len(cases) == 7, 'incorrect quantified metadata')
    # Exhaust every arbitrary 20-bit row; a violated opposite-half pair
    # directly gives a step310 product AP, independently of the field bits.
    nonanti = 0
    for actual in range(1 << 20):
        low = actual & 1023
        if (actual >> 10) == (low ^ 1023):
            continue
        equal_pairs = (~(low ^ (actual >> 10))) & 1023
        require(equal_pairs != 0, 'missing equal opposite pair')
        point = (equal_pairs & -equal_pairs).bit_length() - 1
        color = (actual >> point) & 1
        require(all(((actual >> ((point + j*310) % 20)) & 1) == color for j in range(7)), 'nonanti step310 witness')
        require(point + 6*310 < 2480, 'nonanti literal lift bounds')
        nonanti += 1
    require(nonanti == (1 << 20) - 1024, 'arbitrary row domain count')
    return {'status': 'COMPLETE_LITERAL_ROW_PARTITION_AND_AFFINE_COVER',
            'all_rows': 1 << 20, 'nonanti_rows': nonanti,
            'rejected_anti_rows': len(rejected), 'surviving_anti_rows': 580,
            'cases': cases}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('rows', type=Path)
    print(json.dumps(audit(parser.parse_args().rows), sort_keys=True), flush=True)
