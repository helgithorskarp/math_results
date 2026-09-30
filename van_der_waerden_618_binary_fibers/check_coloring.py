"""Independent definition-level checker; no SAT/NAE generator is imported."""
import argparse
import hashlib
import json
from pathlib import Path


def interval_report(colors):
    n=len(colors)
    checked=0
    monochromatic=0
    first=None
    for d in range(1,(n-1)//6+1):
        for a in range(n-6*d):
            checked+=1
            if all(colors[a+j*d]==colors[a] for j in range(1,7)):
                monochromatic+=1
                if first is None: first={'a':a,'d':d,'positions':[a+j*d for j in range(7)]}
    return {'n':n,'interval_progressions_checked':checked,'monochromatic_interval_progressions':monochromatic,
            'first_obstruction':first,'verified':monochromatic==0}


def cyclic_report(colors):
    n=len(colors)
    checked=0
    monochromatic=0
    first=None
    for d in range(1,n):
        for a in range(n):
            checked+=1
            if all(colors[(a+j*d)%n]==colors[a] for j in range(1,7)):
                monochromatic+=1
                if first is None: first={'a':a,'d':d,'residues':[(a+j*d)%n for j in range(7)]}
    return {'period':n,'cyclic_progression_pairs_checked':checked,'monochromatic_cyclic_pairs':monochromatic,
            'first_cyclic_obstruction':first}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('word',type=Path)
    parser.add_argument('--anti-period-half',action='store_true')
    parser.add_argument('--length',type=int)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    word=args.word.read_text().strip()
    assert word and all(c in '01' for c in word)
    colors=list(map(int,word))
    extras={}
    if args.anti_period_half:
        period=colors+[1-c for c in colors]
        assert args.length is not None and args.length>0
        extras=cyclic_report(period)
        colors=[period[i%len(period)] for i in range(args.length)]
    else:
        assert args.length is None or len(colors)==args.length
    result={**interval_report(colors),**extras,'bits_sha256':hashlib.sha256(''.join(map(str,colors)).encode()).hexdigest()}
    if args.output: args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))
    return 0 if result['verified'] else 2


if __name__=='__main__':
    raise SystemExit(main())
