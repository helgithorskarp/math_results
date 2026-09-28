"""Optional untrusted discovery of kernels for fixed-class exclusions."""
import argparse
import json
from pathlib import Path

from discover import discover


def interior(colours,palette):
    free = {v for v in range(1,len(colours)) if colours[v] in palette}
    if len(colours) == 537:
        free.add(537)
    for d in set(range(1,7))-set(palette):
        A = {v for v in range(1,len(colours)) if colours[v] == d}
        if any(x+y in A for x in A for y in A):
            raise ValueError('an unchanged old class already has a violation')
        blocked = {x+y for x in A for y in A}
        blocked.update(abs(x-y) for x in A for y in A)
        blocked.update(x//2 for x in A if x%2 == 0)
        free.intersection_update(blocked)
    return sorted(free)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    parser.add_argument('palette',nargs=3,type=int)
    parser.add_argument('--seed',type=int,default=1)
    parser.add_argument('--budget',type=int,default=3000)
    parser.add_argument('--output',required=True)
    args = parser.parse_args()
    palette = sorted(args.palette)
    if len(set(palette)) != 3 or not set(palette) <= set(range(1,7)):
        raise ValueError('three distinct labels from 1,...,6 are required')
    directory = Path(__file__).resolve().parent
    fixture = json.loads((directory/'fixtures.json').read_text())[args.input]
    old = [0]+list(map(int,fixture['colours']))
    vertices = discover(interior(old,palette),args.seed,args.budget)
    row = {'input':args.input,'palette':palette,'vertices':vertices,'root':vertices[-1]}
    Path(args.output).write_text(json.dumps(row,indent=2)+'\n')
    print('UNVERIFIED kernel candidate: {} vertices'.format(len(vertices)))


if __name__ == '__main__':
    main()
