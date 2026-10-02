#!/usr/bin/env python3
"""Sequential, guarded reconstruction. Cache is generated data, never source."""
import argparse,json,hashlib,signal,sys
from pathlib import Path

BASE=Path(__file__).resolve().parent
PHASES=('algebra','signs','frames','controls','arithmetic')


def canonical(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()

def require(ok,message):
    if not ok:raise ValueError(message)


def algebra_record(data):
    require(set(data)=={'functions','budget'},'exact cache fields')
    require(set(data['functions'])=={'zeta_heavy','zeta_light','heavy_within_slack','light_within_slack',*['invariant_minor_'+str(i) for i in range(1,5)]},'all8 exact functions')
    require(len(data['budget'])==4 and all(len(row)==4 for row in data['budget']),'all16 budget entries')
    def record(z):
        require(set(z)=={'numerator','denominator','denominator_factors'},'exact rational fields')
        return {'numerator_terms':len(z['numerator']),'denominator_terms':len(z['denominator']),
                'whole_rational_sha256':hashlib.sha256(canonical(z)).hexdigest()}
    return {'whole_generated_cache_sha256':hashlib.sha256(canonical(data)).hexdigest(),
            'functions':{label:record(z) for label,z in data['functions'].items()},
            'budget':[[record(z) for z in row] for row in data['budget']]}


def compare(actual,expected,label):
    require(canonical(actual)==canonical(expected),'WHOLE exact expected record: '+label)


def compute(phase,data=None):
    if phase=='algebra':
        import sympy
        require(sympy.__version__=='1.14.0','pinned SymPy1.14.0')
        import derive
        data=derive.run()
        return algebra_record(data),data
    if phase=='signs':
        import signs
        return signs.run(data['functions']),None
    if phase=='frames':
        import frame
        return frame.run(),None
    if phase=='controls':
        import controls
        return controls.run(data),None
    if phase=='arithmetic':
        import arithmetic
        return arithmetic.run(),None
    raise ValueError('unknown phase')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase',required=True,choices=PHASES)
    parser.add_argument('--expected',type=Path,default=BASE/'EXPECTED.json')
    parser.add_argument('--cache',type=Path,default=Path('scratch/two-load-audit/generated.json'))
    args=parser.parse_args()
    expected=json.loads(args.expected.read_text())
    require(set(expected)=={'schema',*PHASES} and expected['schema']==1,'exact expected schema')
    signal.alarm(90)
    data=None
    if args.phase in ('signs','controls'):
        data=json.loads(args.cache.read_text())
        compare(algebra_record(data),expected['algebra'],'generated cache identity; regenerate with algebra phase')
    record,generated=compute(args.phase,data)
    compare(record,expected[args.phase],args.phase)
    if generated is not None:
        args.cache.parent.mkdir(parents=True,exist_ok=True)
        args.cache.write_bytes(canonical(generated))
    signal.alarm(0)
    sys.stdout.buffer.write(canonical({'phase':args.phase,'record':record}))


if __name__=='__main__':main()
