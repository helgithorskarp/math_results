"""Render exact half-unit example placements as small explanatory SVG files.

The diagrams are displays; the two geometry checkers establish the witnesses.
"""
import argparse
from fractions import Fraction
import json
from pathlib import Path


def boundary(cells):
    edges = set()
    for x, y in cells:
        vertices = ((x, y), (x+1, y), (x+1, y+1), (x, y+1))
        for a, b in zip(vertices, vertices[1:]+vertices[:1]):
            if (b, a) in edges:
                edges.remove((b, a))
            else:
                edges.add((a, b))
    outgoing = dict(edges)
    if len(outgoing) != len(edges):
        raise ValueError('a displayed tile has a boundary pinch')
    start = min(outgoing)
    path = [start]
    at = outgoing.pop(start)
    while at != start:
        path.append(at)
        at = outgoing.pop(at)
    if outgoing:
        raise ValueError('a displayed tile has more than one boundary cycle')
    return path


def render(example):
    paths = []
    for placement in example['placements']:
        tx, ty = map(Fraction, placement['translation'])
        points = [(2*(Fraction(x)+tx), 2*(Fraction(y)+ty))
                  for x, y in boundary(placement['shape'])]
        if any(x.denominator != 1 or y.denominator != 1 for x, y in points):
            raise ValueError('display requires half-unit translations')
        paths.append([(int(x), int(y)) for x, y in points])
    xmin = min(x for p in paths for x, _ in p)-1
    xmax = max(x for p in paths for x, _ in p)+1
    ymin = min(y for p in paths for _, y in p)-1
    ymax = max(y for p in paths for _, y in p)+1
    width, height = xmax-xmin, ymax-ymin
    colors = ['#183b66', '#f0bb6b', '#99c8d5', '#b8d6ad', '#e6a6a6', '#c8b4dc', '#d8cf95', '#9bcbb8']
    lines = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height+5}">',
             f'<title>Family index {example["i"]}: unrestricted Hc=0, Hh=1</title>',
             '<desc>Dark blue root and seven half-unit translated neighbors. White gaps are holes. This image is a display, not a proof.</desc>',
             f'<rect width="{width}" height="{height+5}" fill="white"/>',
             f'<text x="1" y="2" font-family="sans-serif" font-size="1.4">Index {example["i"]}: Hc=0, Hh=1</text>',
             f'<g transform="translate({-xmin},{ymax+4}) scale(1,-1)" stroke="#334155" stroke-width="0.12" stroke-linejoin="round">']
    for i, points in enumerate(paths):
        command = 'M'+' L'.join(f'{x},{y}' for x, y in points)+' Z'
        lines.append(f'<path d="{command}" fill="{colors[i]}"/>')
    lines.extend(['</g>', '</svg>'])
    return '\n'.join(lines)+'\n'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--examples', type=Path, default=Path(__file__).parent/'fractional_examples.json')
    p.add_argument('--output-dir', type=Path, default=Path(__file__).parent)
    args = p.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for example in json.loads(args.examples.read_text())['cases']:
        target = args.output_dir/f'example_{example["i"]}.svg'
        target.write_text(render(example))
        print(str(target))


if __name__ == '__main__':
    main()
