#!/usr/bin/env python3
"""Direct OPB form of the published point613 residual; no new assumption."""
import argparse
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parent


def encode(old,with_degree=False):
    free=old['free'];var={v:i+1 for i,v in enumerate(free)}
    family=[set(row['D']) for row in old['family']]
    minimal=[i for i,D in enumerate(family) if not any(E<D for E in family)]
    rows=[' '.join(f'+1 x{var[v]}' for v in sorted(family[i]))+' >= 1 ;'
          for i in minimal if i not in [245,316]]
    rows += [f'-1 x{var[v]} >= 0 ;' for v in [13,24,129,518]]
    rows += [' '.join(f'-1 x{var[v]}' for v in free)+' >= -56 ;']
    if with_degree:rows.append(f'+1 x{var[14]} +1 x{var[126]} >= 1 ;')
    return (f'* #variable= {len(free)} #constraint= {len(rows)} #equal= 0 intsize= 8\n'+'\n'.join(rows)+'\n').encode()


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--with-degree',action='store_true');args=ap.parse_args()
    old=json.loads((REPO/'hadwiger_nelson_parts509_degree_pool_minimum/certificate_D7.json').read_text())
    args.out.write_bytes(encode(old,args.with_degree))
