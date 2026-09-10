"""Prepare the complete, canonically ordered reflection-orbit catalog."""
import argparse, hashlib, json
from itertools import combinations_with_replacement
from pathlib import Path

def sidon(row):
    sums=[a+b for a,b in combinations_with_replacement(row,2)]
    return len(sums)==len(set(sums))

def orbit_catalog(rows,weights):
    n=len(weights)
    if weights!=weights[::-1]:raise ValueError('weights must be reflection invariant')
    size=len(rows[0]); masks={}
    for row in rows:
        if len(row)!=size or len(set(row))!=size or not all(0<=x<n for x in row) or not sidon(row):raise ValueError('invalid set')
        mask=sum(1<<x for x in row)
        if mask in masks:raise ValueError('duplicate set')
        masks[mask]=sorted(row)
    orbits=[]
    for mask,row in masks.items():
        other=sum(1<<(n-1-x) for x in row)
        if other not in masks:raise ValueError('catalog not reflection closed')
        if other==mask:raise ValueError('self-reflecting set not supported by this paired format')
        if mask<other:orbits.append((sum(weights[x] for x in row),mask,other))
    orbits.sort(key=lambda t:(-t[0],t[1]))
    return [masks[m] for _,a,b in orbits for m in (a,b)]

def prepare(catalog,weights,outdir):
    rows=[list(map(int,l.split())) for l in catalog.read_text().splitlines()]
    w=list(map(int,weights.read_text().split()))
    if len(w)!=84 or len(rows)!=30510 or any(len(r)!=11 for r in rows):raise ValueError('P84 catalog dimensions')
    ordered=orbit_catalog(rows,w);outdir.mkdir(parents=True,exist_ok=True)
    output=outdir/'orbit_catalog.txt'
    output.write_text(''.join(' '.join(map(str,r))+'\n' for r in ordered))
    threshold=sum(w)-4*2000000
    eligible=[j for j in range(len(ordered)//2) if 4*sum(w[x] for x in ordered[2*j])>=threshold]
    record={'catalog_sets':len(rows),'reflection_orbits':len(rows)//2,'weight_sum':sum(w),'ten_cap':2000000,'four_eleven_threshold':threshold,'eligible_orbits':len(eligible),'raw_catalog_sha256':hashlib.sha256(catalog.read_bytes()).hexdigest(),'orbit_catalog_sha256':hashlib.sha256(output.read_bytes()).hexdigest()}
    (outdir/'orbits.json').write_text(json.dumps(record,indent=2)+'\n');return record

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('catalog',type=Path);p.add_argument('weights',type=Path);p.add_argument('output_dir',type=Path);a=p.parse_args();print(json.dumps(prepare(a.catalog,a.weights,a.output_dir)))
