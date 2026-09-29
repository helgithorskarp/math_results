"""Regenerate semantic rational certificates; no proof checker imports SciPy."""
import argparse
import json
import math
import tempfile
from fractions import Fraction
from pathlib import Path
from model import run
from round import run as round_bound
from audit import verify


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',default='certificate.json');p.add_argument('--output',required=True)
    p.add_argument('--multipliers',nargs='+',type=int)
    args=p.parse_args();source=json.loads(Path(args.source).read_text());n=len(source['seed_word'])+1
    units=[u for u in range(1,n//2+1) if math.gcd(u,n)==1]
    selected=units if args.multipliers is None else args.multipliers
    assert len(selected)==len(set(selected)) and set(selected)<=set(units)
    family=dict(seed_word=source['seed_word'],seed_axis_factor=source['seed_axis_factor'],
                definition='independent run lengths in seed-selected interval-separation chambers',chambers=[])
    with tempfile.TemporaryDirectory(prefix='schur-interval-regeneration-') as folder:
        for u in selected:
            m,record=run(args.source,str(Path(folder)/('unit%d.json'%u)),u)
            c=record['exact_certificate']
            entry=dict(multiplier=u,run_counts=m['run_counts'],dimension=m['dimension'],
                       inequalities=len(m['rows']),upper_bound_axis_factor=c['upper_bound_axis_factor'],
                       equality_weights=c['equality_weights'],
                       terms=[dict(weight=z['weight'],reason=m['reasons'][z['row']]) for z in c['inequalities']])
            if Fraction(c['upper_bound_axis_factor'])>=71:
                refinement=round_bound(args.source,u,str(Path(folder)/('rounded%d.json'%u)))
                entry.update(refinement)
            family['chambers'].append(entry)
            Path(args.output).write_text(json.dumps(family,separators=(',',':'))+'\n')
    print(json.dumps(verify(args.output,selected==units),indent=2))


if __name__=='__main__':main()
