"""Exact 36-position arc models and the 22 six-exception gap profiles."""
from pathlib import Path
import importlib.util
import itertools

HERE = Path(__file__).resolve().parent
BASE = HERE.parent/'order7-geometric-cut'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def records():
    result = [{'stem':f'arc-b{b}', 'kind':'arc', 'background':b,
               'width':36, 'variables':79} for b in (0, 1)]
    rotate = lambda t,j:t[j:]+t[:j]
    rooted = [t for t in itertools.product(range(5), repeat=6) if sum(t) == 4]
    canonical = sorted({min(rotate(t,j) for j in range(6)) for t in rooted})
    require(len(rooted) == 126 and len(canonical) == 22, 'incomplete gap cover')
    for b in (0, 1):
        for case,t in enumerate(canonical, 1):
            positions = [0]
            for value in t[:-1]:
                positions.append(positions[-1]+8-value)
            require(positions[-1]+8-t[-1] == 44, 'wrong cyclic gap sum')
            result.append({'stem':f'boundary-b{b}-{case:02d}', 'kind':'boundary',
                           'background':b, 'variables':44, 'case':case,
                           'deficit':list(t), 'exception_positions':positions})
    return result


def clauses(rec, edges):
    b = rec['background']
    if rec['kind'] == 'arc':
        mapping = list(range(1, 45))+[-1 if b == 0 else 1]
        mapping += [44+i for i in range(1, 36)]
        mapping += [(i+1)*(-1 if b else 1) for i in range(36, 44)]
    else:
        phase = [b^int(i in rec['exception_positions']) for i in range(44)]
        mapping = list(range(1, 45))
        mapping += [(i+1)*(-1 if phase[i] else 1) for i in range(44)]
    require(len(mapping) == 88, 'incomplete quotient mapping')
    result = set()
    for edge in edges:
        signed = {mapping[i] for i in edge}
        if any(-v in signed for v in signed):
            continue
        result.add(tuple(sorted(signed)))
        result.add(tuple(sorted(-v for v in signed)))
    return sorted(result, key=lambda c:(len(c), c))+[(-1,)]


def prepare(work):
    spec = importlib.util.spec_from_file_location('committed_h7_log_generator', BASE/'encode.py')
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    edges = helper.field_edges()
    result = records()
    for rec in result:
        cs = clauses(rec, edges)
        text = f'p cnf {rec["variables"]} {len(cs)}\n'
        text += ''.join(' '.join(map(str,c))+' 0\n' for c in cs)
        path = work/(rec['stem']+'.cnf')
        require(not path.exists() or path.read_text() == text, 'changed existing exact model')
        path.write_text(text)
        rec['clauses'] = len(cs)
    return result
