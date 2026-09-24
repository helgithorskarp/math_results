"""Recover two actual complete links from the known 21-block cover."""
from pathlib import Path
import json

import audit_model
from catalogue import CAT
from point_maps import point_maps
from row_maps import embeddings, key, pointed_templates

ROOT = Path(__file__).resolve().parent


def main():
    fixture = json.loads((ROOT / 'UPPER21.json').read_text())['blocks']
    blocks = [sum(1 << (p - 1) for p in b) for b in fixture]
    low = [p for p in range(13) if sum(b >> p & 1 for b in blocks) == 9]
    links = []
    for p in low:
        star = [b & ~(1 << p) for b in blocks if b >> p & 1]
        points = tuple(x for x in range(13) if x != p)
        target_degrees = sorted(sum(b >> x & 1 for b in star) for x in points)
        for design in CAT:
            if sorted(map(int.bit_count, design['point_signatures'])) != target_degrees:
                continue
            action = next(point_maps(design['blocks'], tuple(range(12)), star, points), None)
            if action is not None:
                links.append((design['id'], p, action))
                break
        else:
            raise ValueError('known degree-nine link missing from catalogue')
    design, p, action = max(links, key=lambda x: x[0])
    r = max((x for x in low if x != p),
            key=lambda x: sum(b >> x & 1 and b >> p & 1 for b in blocks))
    inverse = {v: k for k, v in action.items()}
    inverse[p] = 12
    rr = inverse[r]
    fixed = tuple(sorted(sum(1 << inverse[x] for x in range(13) if b >> x & 1)
                         for b in blocks if b >> p & 1 or b >> r & 1))
    d = CAT[design]
    shared = tuple(b & ~(1 << rr) for b in d['blocks'] if b >> rr & 1)
    vertices = tuple(x for x in range(13) if x not in (12, rr))
    templates = pointed_templates()
    matches = 0
    for source in templates[(len(shared), key(shared, vertices))]:
        for mapping in embeddings(source, shared, vertices):
            first = {b | (1 << 12) for b in d['blocks']}
            second = {sum(1 << mapping[x] for x in range(12) if b >> x & 1)
                      | (1 << rr) for b in source['blocks']}
            if tuple(sorted(first | second)) == fixed:
                matches += 1
    if not matches:
        raise ValueError('primary gluing missed known complete links')
    _, audit_templates = audit_model.prepare()
    records, _ = audit_model.uncoloured(design, rr, audit_templates)
    choices = [x for x in records if x[0] == fixed]
    if len(choices) != 1 or choices[0][1] > design:
        raise ValueError('independent gluing or maximal-link normalization missed fixture')
    print(json.dumps(dict(status='KNOWN_TWO_LINK_GLUING_RECOVERED',
                          low_link_classes=[(p, d) for d, p, a in links],
                          first_design=design, second_design=choices[0][1],
                          shared_blocks=len(shared), fixed_blocks=len(fixed),
                          primary_identifications=matches,
                          independent_unique_union=True), indent=2))


if __name__ == '__main__':
    main()
