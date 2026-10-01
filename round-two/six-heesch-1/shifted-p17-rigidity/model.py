"""Exact finite mask/pose encoding and independent inverse-cell incidences.

The rectangular pool is a hypothesis. No solver, area constraint, connectedness
flow or geometric upper bound for other networks is used by this module.
"""
from collections import defaultdict
from itertools import product
import importlib.util
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent/'finite-contact-types'))
from contact import require
from rup import RupChecker


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def image(g, t, p):
    a,b,c,d = g
    return (a*p[0]+b*p[1]+min(a,b,0)+t[0],
            c*p[0]+d*p[1]+min(c,d,0)+t[1])


def inverse_incidence(g, t, width, height):
    """Transport doubled world-cell centers, independently of image()."""
    a,b,c,d = g
    vertices = [(a*x+b*y+t[0],c*x+d*y+t[1])
                for x,y in product((0,width),(0,height))]
    xmin,xmax = min(x for x,y in vertices),max(x for x,y in vertices)
    ymin,ymax = min(y for x,y in vertices),max(y for x,y in vertices)
    result = {}
    for u in range(xmin,xmax):
        for v in range(ymin,ymax):
            x,y = 2*u+1-2*t[0],2*v+1-2*t[1]
            rx,ry = a*x+c*y,b*x+d*y
            require(rx%2 == ry%2 == 1, 'center image is not an integer unit cell')
            p = ((rx-1)//2,(ry-1)//2)
            if 0 <= p[0] < width and 0 <= p[1] < height:
                require(p not in result,'nonbijective inverse incidence')
                result[p] = (u,v)
    require(len(result) == width*height,'inverse rectangle incidence incomplete')
    return result


def at_most_one(circuit, xs):
    if len(xs) < 2:
        return
    prior = xs[0]
    for x in xs[1:]:
        circuit.clause([-prior,-x])
        prior = circuit.or_([prior,x])


def scaled_cells(data):
    n = data['scale']
    return {(n*x+i,n*y+j) for x,y in data['cells']
            for i,j in product(range(n),repeat=2)}


def compile_formula(data, circuit_type, inverse=False, exclude_control=True):
    circuit = circuit_type()
    domain = list(product(range(data['width']),range(data['height'])))
    ids = {p:circuit.new() for p in domain}
    circuit.clause([ids[tuple(data['anchor'])]])
    owners = defaultdict(list)
    options, maps = [], []
    poses = [p for p in data['base_network'] if p[0] <= 2]
    for i,(level,g,t) in enumerate(poses):
        shifts = [(0,0)] if i == 0 else data['shifts']
        ys = []
        for dx,dy in shifts:
            y = circuit.true if i == 0 else circuit.new()
            ys.append(y)
            u = (data['scale']*t[0]+dx,data['scale']*t[1]+dy)
            o = len(options)
            options.append(dict(copy=i,level=level,matrix=tuple(g),translation=u,
                                shift=(dx,dy),selected=y))
            mapping = (inverse_incidence(g,u,data['width'],data['height']) if inverse
                       else {p:image(g,u,p) for p in domain})
            maps.append(mapping)
            for p,x in ids.items():
                z = circuit.and_([x,y])
                owners[mapping[p]].append((level,i,o,p,z))
        circuit.clause(ys)
        at_most_one(circuit,ys)
    for entries in owners.values():
        at_most_one(circuit,[z for level,i,o,p,z in entries])
    prefixes = []
    for level in range(3):
        occupancy = {q:circuit.or_(z for k,i,o,p,z in entries if k <= level)
                     for q,entries in sorted(owners.items())
                     if any(k <= level for k,i,o,p,z in entries)}
        prefixes.append(occupancy)
        vertices = {(x-dx,y-dy) for x,y in occupancy
                    for dx,dy in product((0,1),repeat=2)}
        for x,y in sorted(vertices):
            a,b,c,d = [occupancy.get(q,circuit.false)
                       for q in ((x,y),(x+1,y),(x,y+1),(x+1,y+1))]
            circuit.clause([-a,b,c,-d])
            circuit.clause([a,-b,-c,d])
    for level in range(2):
        for (x,y),u in sorted(prefixes[level].items()):
            for dx,dy in product((-1,0,1),repeat=2):
                if dx or dy:
                    circuit.clause([-u,prefixes[level+1].get((x+dx,y+dy),circuit.false)])
    for (x,y),v in ids.items():
        circuit.clause([-v]+[ids[q] for q in ((x+1,y),(x-1,y),(x,y+1),(x,y-1))
                            if q in ids])
    if exclude_control:
        control = scaled_cells(data)
        circuit.clause([-ids[p] if p in control else ids[p] for p in domain])
    require(circuit.nv <= 60000 and len(circuit.clauses) <= 200000,
            'formula guard; incomplete')
    return circuit,domain,ids,options,maps


def dimacs(circuit):
    return (f'p cnf {circuit.nv} {len(circuit.clauses)}\n'+
            ''.join(' '.join(map(str,row))+(' ' if row else '')+'0\n'
                    for row in circuit.clauses)).encode()
