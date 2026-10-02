"""Damage controls for fixed G20 coverage and dyadic boundary semantics.

No interval leaf replay occurs here. Controls never modify the actual inputs.
Same-author controls are not an independent researcher review.
"""
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
import ast
import importlib.util
import json
import signal
import tempfile

BASE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('g20_replay_controls', BASE/'replay.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)


def require(ok, why):
    if not ok:
        raise ValueError(why)


def main():
    originals = {n: (BASE/n).read_bytes()
                 for n in ('PLAN.json','LITERALS.json','model.py','replay.py')}
    plan, table = json.loads(originals['PLAN.json']), json.loads(originals['LITERALS.json'])
    _, structure = r.describe()
    expected = [(t['leaf_range'],t['nodes'],t['maximum_depth']) for t in structure['trees']]
    rejected, accepted = [], []

    def trial(name, mutate, should_pass=False):
        a, b = deepcopy(plan), deepcopy(table)
        mutate(a, b)
        with tempfile.TemporaryDirectory(prefix='g20-damage-') as d:
            target = Path(d)
            for n, raw in originals.items():
                (target/n).write_bytes(raw)
            (target/'PLAN.json').write_text(json.dumps(a))
            (target/'LITERALS.json').write_text(json.dumps(b))
            r.BASE = target
            try:
                _, value = r.describe()
            except ValueError as e:
                require(not should_pass, name+' incorrectly rejected')
                rejected.append({'case':name,'reason':str(e)})
            else:
                require(should_pass, name+' incorrectly accepted')
                require([(t['leaf_range'],t['nodes'],t['maximum_depth'])
                         for t in value['trees']] == expected, 'full structure semantics')
                accepted.append(name)
            finally:
                r.BASE = BASE

    def field(key, value):
        return lambda a, b: a.__setitem__(key, value)

    trial('wrong format', field('format',2))
    trial('wrong outward precision', field('lattice_bits',79))
    trial('weaken rectangle endpoint', field('box',['14/25','592/1000','-5/2','5/2']))
    trial('reintroduce point13', lambda a,b: a['labels'].append(13))
    trial('drop actual contact', lambda a,b: a['contacts'].pop())
    trial('reintroduce contact2-13', lambda a,b: a['contacts'].append([2,13]))
    trial('omit orientation', lambda a,b: a['trees'].pop())
    trial('duplicate orientation', lambda a,b: a['trees'].__setitem__(1,deepcopy(a['trees'][0])))
    trial('change g-half target mode', lambda a,b: a['trees'][3].__setitem__('mode','bad'))
    trial('truncate prefix', lambda a,b: a['trees'][0].__setitem__('tree',a['trees'][0]['tree'][:-1]))
    trial('unused prefix token', lambda a,b: a['trees'][0].__setitem__('tree',a['trees'][0]['tree']+'0'))
    trial('unknown literal', lambda a,b: a['trees'][0].__setitem__('tree','?'))
    trial('g-half witness in bad tree', lambda a,b: a['trees'][0].__setitem__('tree','3'))
    trial('depth budget exceeded', lambda a,b: a['trees'][0].__setitem__('tree','T'*23+'0'*24))
    full = '0'
    for _ in range(14):
        full = 'T'+full+full
    trial('node budget exceeded', lambda a,b: a['trees'][0].__setitem__('tree',full))
    trial('fixed compact-size budget exceeded', lambda a,b: a['trees'][0].__setitem__('tree','0'*50001))
    trial('remove typed literal', lambda a,b: b['literals'].pop())
    trial('restore removed-point predicate', lambda a,b: b['literals'].__setitem__(9,['pair',6,13]))
    trial('unknown W comparison', lambda a,b: b['literals'].__setitem__(4,['W-pair',7,13]))
    trial('change literal code binding', lambda a,b: b.__setitem__('codes',b['codes'][::-1]))
    def reverse_fields(a, b):
        for value in (a, b):
            items = list(value.items())
            value.clear()
            value.update(reversed(items))
    trial('JSON field order', reverse_fields, should_pass=True)
    trial('unused descriptive metadata', lambda a,b: a.__setitem__('description','same fixed certificate'), should_pass=True)

    m = r.m
    arithmetic = []
    for i, q in enumerate((Fraction(-1,3), Fraction(0), Fraction(1,7), Fraction(1,2))):
        v = m.I(q)
        require(Fraction(v.l,m.S) <= q <= Fraction(v.h,m.S), 'point containment')
        arithmetic.append('point '+str(i))
    zero = m.I(0).sqrt()
    require(zero.l == zero.h == 0, 'tangent root retained')
    arithmetic.append('square-root zero retained')
    sq = m.I(Fraction(-1,3),Fraction(1,7))**2
    require(sq.l == 0 and Fraction(sq.h,m.S) >= Fraction(1,9), 'zero-spanning square')
    arithmetic.append('zero-spanning square')
    for name, fn in [('zero denominator', lambda: m.I(1)/m.I(-1,1)),
                     ('negative root', lambda: m.I(-1,0).sqrt()),
                     ('empty intersection', lambda: m.clip(m.I(-1,0),m.I(1,2)))]:
        try:
            fn()
        except (ValueError,ArithmeticError):
            arithmetic.append(name+' rejected')
        else:
            raise ValueError(name+' incorrectly accepted')
    for source in ('model.py','replay.py','identities.py','controls.py'):
        tree = ast.parse((BASE/source).read_text())
        require(not any(isinstance(n,ast.Assert) for n in ast.walk(tree)),
                'checks must survive python -O')
    require(all((BASE/n).read_bytes() == raw for n,raw in originals.items()),
            'fixed runtime changed during controls')
    print(json.dumps({'actual_agent':'six-tammes-2','role':'researcher',
                      'damages_rejected':len(rejected),'damage_reasons':rejected,
                      'valid_controls_accepted':accepted,'arithmetic_boundary_controls':arithmetic,
                      'assert_free_guards_checked':4,'runtime_inputs_unchanged':True,
                      'new_interval_predicate_evaluations':False,
                      'independent_researcher_review':'pending'},indent=2))


if __name__ == '__main__':
    signal.signal(signal.SIGALRM,lambda *_: (_ for _ in ()).throw(
        TimeoutError('55-second control guard')))
    signal.alarm(55)
    main()
