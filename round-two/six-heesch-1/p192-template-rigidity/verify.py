"""Solver-free, direct cell-frame reader for a fixed corona-template rigidity."""
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OWN = HERE.parent
FOUR = ((1,0),(-1,0),(0,1),(0,-1))
NINE = tuple((x,y) for x in (-1,0,1) for y in (-1,0,1))


def require(ok,message):
    if not ok:
        raise ValueError(message)


def module(name,path):
    spec = importlib.util.spec_from_file_location(name,path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


deps = json.loads((HERE/'dependencies.json').read_text())
for row in deps:
    require(hashlib.sha256((OWN/row['path']).read_bytes()).hexdigest() == row['sha256'],
            'dependency byte pin differs: '+row['path'])
c = module('template_integer_geometry',OWN/'p192-exact-three/upper.py')
r = module('template_rup_reader',OWN/'finite-contact-types/rup.py')


def normalize(cells):
    cells = [tuple(p) for p in cells]
    require(cells and len(cells) == len(set(cells)),'empty or duplicate cells')
    require(all(len(p) == 2 and all(type(z) is int for z in p) for p in cells),
            'noninteger cell')
    lo = min(x for x,y in cells),min(y for x,y in cells)
    return tuple(sorted((x-lo[0],y-lo[1]) for x,y in cells))


def images(cells):
    return tuple(sorted({normalize([(sx*(y if swap else x),sy*(x if swap else y))
                                   for x,y in cells])
                         for swap in (False,True) for sx in (-1,1) for sy in (-1,1)}))


def positive_coronas(parent,levels):
    geometry = c.Geometry(parent)
    require(geometry.shapes == images(parent),'positive orientation frames differ')
    require(levels[0] == [geometry.root],'wrong unchanged root')
    occupied = set()
    stats = []
    for k,poses in enumerate(levels):
        previous = set(occupied)
        for pose in poses:
            fp = geometry.pixels(pose)
            require(occupied.isdisjoint(fp),'copy overlap')
            if k:
                require(bool(c.halo(fp)&previous),'copy misses preceding prefix')
            occupied.update(fp)
        if k:
            require(c.halo(previous) <= occupied,'incomplete corona')
        require(c.disc(occupied),'prefix is not a closed disc')
        stats.append(dict(prefix=k,copies=sum(map(len,levels[:k+1])),cells=len(occupied)))
    return stats


def compile_formula(data):
    require(data['scale'] == 2,'literal selected scale differs')
    depth = data['template_depth']
    require(depth == 1,'literal first-template depth differs')
    seed = normalize(data['seed_cells'])
    parent = tuple(sorted((2*x+i,2*y+j) for x,y in seed
                          for i in (0,1) for j in (0,1)))
    S = set(parent)
    boundary = {q for q in parent if any((q[0]+dx,q[1]+dy) not in S for dx,dy in FOUR)}
    exterior = {(x+dx,y+dy) for x,y in parent for dx,dy in FOUR}-S
    core = S-boundary
    universe = sorted(S | exterior)
    var = {q:i for i,q in enumerate(universe,1)}
    levels = [[(o,2*x,2*y) for o,x,y in ps] for ps in data['seed_levels'][:depth+1]]
    require([len(ls) for ls in levels] == [1,6],'literal first-template levels differ')
    lower = positive_coronas(parent,levels)
    shapes = images(parent)
    require(len(shapes) == 8,'reference frame is not unique')
    matrices = [(sx,0,0,sy) if not swap else (0,sx,sy,0)
                for swap in (False,True) for sx in (-1,1) for sy in (-1,1)]
    # Cell-index normalization directly; no discovery physical-square offsets.
    frames = []
    for shape in shapes:
        choices = []
        for a,b,cc,d in matrices:
            raw = [(a*x+b*y,cc*x+d*y) for x,y in parent]
            lo = min(x for x,y in raw),min(y for x,y in raw)
            normalized = tuple(sorted((x-lo[0],y-lo[1]) for x,y in raw))
            if normalized == shape:
                choices.append(((a,b,cc,d),lo))
        require(len(choices) == 1,'ambiguous direct frame')
        frames.append(choices[0])
    owners = [dict() for k in range(depth+1)]
    copy = 0
    for lev,ps in enumerate(levels):
        for o,tx,ty in ps:
            M,lo = frames[o]
            a,b,cc,d = M
            for q,i in var.items():
                x,y = a*q[0]+b*q[1]-lo[0]+tx,cc*q[0]+d*q[1]-lo[1]+ty
                for k in range(lev,depth+1):
                    owners[k].setdefault((x,y),[]).append((copy,i))
            copy += 1
    clauses = {(var[q],) for q in core}
    def add(zs):
        zs = set(zs)
        if not any(-z in zs for z in zs):
            clauses.add(tuple(sorted(zs)))
    for entries in owners[depth].values():
        for k,(copy,i) in enumerate(entries):
            for other,j in entries[k+1:]:
                if copy != other:
                    add([-i,-j])
    # Implications per global pixel, rather than discovery's per-pose cells.
    for k in range(depth):
        for (x,y),entries in owners[k].items():
            origins = {i for copy,i in entries}
            for dx,dy in NINE:
                suppliers = {j for copy,j in owners[k+1].get((x+dx,y+dy),[])}
                for i in origins:
                    add([-i]+list(suppliers))
    base = [list(zs) for zs in sorted(clauses)]
    selected = {var[q] for q in S}
    require(all(any(z in selected if z>0 else -z not in selected for z in zs)
                for zs in base),'unchanged template violates direct formula')
    dimacs = (f'p cnf {len(var)} {len(base)}\n'
              + ''.join(' '.join(map(str,zs))+' 0\n' for zs in base)).encode()
    expected_units = {var[q] if q in S else -var[q] for q in boundary | exterior}
    return dict(parent=parent,core=core,universe=universe,var=var,clauses=base,
                units=expected_units,lower=lower,
                formula_sha256=hashlib.sha256(dimacs).hexdigest())


def replay(data,trace):
    formula = compile_formula(data)
    checker = r.RupChecker(formula['clauses'],len(formula['var']))
    units = []
    for line in trace.splitlines():
        zs = list(map(int,line.split()))
        require(len(zs) == 2 and zs[1] == 0 and zs[0] != 0,'not a literal unit step')
        z = zs[0]
        require(z in formula['units'],'unit has the wrong membership sign')
        require(checker.rup([z])[0],'non-RUP template unit')
        checker.add([z])
        units.append(z)
    require(len(units) == len(set(units)) and set(units) == formula['units'],
            'proof does not fix every editable cell')
    return dict(parent_cells=len(formula['parent']),core_cells=len(formula['core']),
                template_depth=data['template_depth'],
                universe_cells=len(formula['universe']),editable_cells=len(formula['units']),
                variables=len(formula['var']),clauses=len(formula['clauses']),
                rup_units=len(units),formula_sha256=formula['formula_sha256'],
                trace_sha256=hashlib.sha256(trace.encode()).hexdigest(),
                unchanged_disc_coronas=formula['lower'],unique_prototype=True)


def damaged_controls(data,trace):
    lines = trace.splitlines(keepends=True)
    cases = [('omitted unit',data,''.join(lines[:-1]),'every editable cell')]
    flip = list(lines)
    z = int(flip[0].split()[0])
    flip[0] = f'{-z} 0\n'
    cases.append(('wrong membership sign',data,''.join(flip),'membership sign'))
    corrupt = deepcopy(data)
    corrupt['seed_levels'][1][0][1] += 1
    cases.append(('changed physical pose',corrupt,trace,None))
    results = []
    for label,fixture,proof,message in cases:
        try:
            replay(fixture,proof)
        except ValueError as exc:
            require(message is None or message in str(exc),'control failed for an unrelated reason')
            results.append(dict(control=label,rejected=True,reason=str(exc)))
        else:
            raise ValueError('damaged template certificate accepted: '+label)
    return results


def main():
    raw = (HERE/'input.json').read_bytes()
    data = json.loads(raw)
    trace = (HERE/'membership.rup').read_text()
    expected = json.loads((HERE/'expected.json').read_text())
    require(hashlib.sha256(raw).hexdigest() == expected['input_sha256'],'literal input digest differs')
    proof = replay(data,trace)
    require(proof == expected['proof'],'rebuilt template evidence differs')
    print(json.dumps(dict(agent='six-heesch-1',role='researcher',proof=proof,
                         damaged_controls=damaged_controls(data,trace)),sort_keys=True))


if __name__ == '__main__':
    main()
