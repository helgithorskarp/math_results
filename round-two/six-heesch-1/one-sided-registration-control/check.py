"""Solver-free registration/control proof for the literal 21-cell prototype.

The half-grid formula is rebuilt by halo anchoring and direct whole-footprint
intersections, independently of discovery's bounding boxes/lazy incidence.
The integer support queries and root catalogue use first-uncovered search.
The final candidate pool is additionally rebuilt by halo anchoring.
"""
from copy import deepcopy
import hashlib
import importlib.util
from itertools import product
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
DEADLINE = None


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


for name, digest in json.loads((HERE/'dependencies.json').read_text()).items():
    if hashlib.sha256((HERE/name).read_bytes()).hexdigest() != digest:
        raise ValueError('changed dependency '+name)
u = module('registration_integer_geometry', HERE/'../p192-exact-three/upper.py')
rup = module('registration_rup', HERE/'../finite-contact-types/rup.py')
require = u.require


def guard():
    require(time.monotonic() < DEADLINE, 'reader wall guard; incomplete')


def shapes_from_vertices(cells, scale):
    """Physical vertex images, instead of discovery's cell-index offset rule."""
    matrices = ((1, 0, 0, 1), (1, 0, 0, -1), (-1, 0, 0, 1),
                (-1, 0, 0, -1), (0, 1, 1, 0), (0, 1, -1, 0),
                (0, -1, 1, 0), (0, -1, -1, 0))
    orientations = set()
    for a, b, c, d in matrices:
        lower = []
        for x, y in cells:
            vertices = [(a*(x+i)+b*(y+j), c*(x+i)+d*(y+j))
                        for i, j in product((0, 1), repeat=2)]
            lower.append((min(p[0] for p in vertices), min(p[1] for p in vertices)))
        xmin, ymin = min(x for x, y in lower), min(y for x, y in lower)
        pixels = {(scale*(x-xmin)+i, scale*(y-ymin)+j)
                  for x, y in lower for i, j in product(range(scale), repeat=2)}
        orientations.add(tuple(sorted(pixels)))
    return tuple(sorted(orientations))


def anchored_pool(shapes, occupied):
    target = sorted(u.halo(occupied))
    candidates = []
    for o, shape in enumerate(shapes):
        offsets = {(x-a, y-b) for x, y in target for a, b in shape}
        for tx, ty in sorted(offsets):
            fp = frozenset((a+tx, b+ty) for a, b in shape)
            if fp.isdisjoint(occupied):
                candidates.append(((o, tx, ty), fp))
    candidates.sort()
    require(len(candidates) <= 2000, 'candidate guard; incomplete')
    return target, candidates


def half_formula(cells):
    shapes = shapes_from_vertices(cells, 2)
    require(len(shapes) == 8, 'unexpected prototype stabilizer')
    root = {(2*x+i, 2*y+j) for x, y in cells for i, j in product((0, 1), repeat=2)}
    target, pool = anchored_pool(shapes, root)
    n = len(pool)
    clauses = [[i+1 for i, (pose, fp) in enumerate(pool) if q in fp] for q in target]
    for i, (pose, fp) in enumerate(pool):
        guard()
        clauses.extend([-i-1, -j-1] for j in range(i+1, n)
                       if not fp.isdisjoint(pool[j][1]))
    require(len(clauses) <= 450000, 'formula guard; incomplete')
    dimacs = (f'p cnf {n} {len(clauses)}\n'
              + ''.join(' '.join(map(str, c))+' 0\n' for c in clauses)).encode()
    return pool, clauses, hashlib.sha256(dimacs).hexdigest()


def phase_units(clauses, n, trace):
    require(len(trace.encode()) <= 100000, 'trace guard; incomplete')
    checker = rup.RupChecker(clauses, n)
    additions = 0
    for line in trace.splitlines():
        guard()
        words = list(map(int, line.split()))
        require(words and words[-1] == 0 and 0 not in words[:-1], 'bad proof terminator')
        clause = words[:-1]
        require(checker.rup(clause)[0], 'non-RUP floating support step')
        checker.add(clause)
        additions += 1
    return {c[0] for c in checker.clauses if len(c) == 1}, additions


def covers(cover, forced=None, first_only=False):
    """Complete first-uncovered search; negative memo entries only."""
    failed = set()
    answers = set()
    nodes = 0

    def visit(remaining, available, selected):
        nonlocal nodes
        nodes += 1
        guard()
        require(nodes <= 100000, 'node guard; incomplete')
        if not remaining:
            answers.add(tuple(sorted(cover.pool[i][0] for i in selected)))
            require(len(answers) <= 10000, 'catalogue guard; incomplete')
            return True
        key = remaining, available
        if key in failed:
            return False
        k = (remaining & -remaining).bit_length()-1
        possible = cover.owners[k] & available
        found = False
        while possible:
            bit = possible & -possible
            possible -= bit
            i = bit.bit_length()-1
            yes = visit(remaining & ~cover.covers[i],
                        available & ~cover.conflicts(i), selected+(i,))
            found = found or yes
            if yes and first_only:
                return True
        if not found:
            failed.add(key)
        return found

    remaining, available = (1 << len(cover.owners))-1, (1 << len(cover.pool))-1
    selected = ()
    if forced is not None:
        remaining &= ~cover.covers[forced]
        available &= ~cover.conflicts(forced)
        selected = (forced,)
    visit(remaining, available, selected)
    return answers, nodes


def integer_support(data, geometry):
    original = u.Cover(geometry, [geometry.root], set())
    bypose = {p: i for i, (p, fp) in enumerate(original.pool)}
    excluded = [tuple(p) for p in data['excluded_integer_types']]
    require(len(excluded) == len(set(excluded)) and set(excluded) <= set(bypose),
            'invalid/repeated integer exclusion')
    nodes = 0
    for typ in excluded:
        answers, cost = covers(original, bypose[typ], first_only=True)
        require(not answers, 'false integer support exclusion')
        nodes += cost
        require(nodes <= 100000, 'aggregate support node guard; incomplete')
    positive = set()
    for witness in data['integer_support_witnesses']:
        poses = [tuple(p) for p in witness]
        original.accepts(poses)
        positive.update(poses)
    allowed = set(bypose)-set(excluded)
    require(positive == allowed, 'incomplete/inconsistent integer support witnesses')
    return allowed, nodes


def first_catalogue(data, geometry, allowed):
    bad = geometry.integer_contacts-allowed
    bad |= {geometry.relative(p, geometry.root) for p in bad}
    cover = u.Cover(geometry, [geometry.root], bad)
    answers, nodes = covers(cover)
    supplied = {tuple(sorted(tuple(p) for p in star)) for star in data['first_catalogue']}
    require(len(supplied) == len(data['first_catalogue']) and answers == supplied,
            'first catalogue omitted/added/repeated a surround')
    require(len(answers) == 1, 'unexpected first catalogue cardinality')
    return sorted(answers)[0], nodes, len(bad)


def final_second(data, geometry, star, allowed):
    fixed = [geometry.root]+list(star)
    occupied = geometry.union(fixed)
    fp_fixed = [geometry.pixels(p) for p in fixed]
    halos = [u.halo(fp) for fp in fp_fixed]
    for i, a in enumerate(fixed):
        for j, b in enumerate(fixed):
            require(i == j or fp_fixed[j].isdisjoint(halos[i])
                    or geometry.relative(a, b) in allowed, 'fixed directed contact unsupported')
    # Independently inventory all placements by halo anchoring, not transport.
    shapes = shapes_from_vertices(geometry.cells, 1)
    require(shapes == geometry.shapes, 'integer orientation audit differs')
    target, unconstrained = anchored_pool(shapes, occupied)
    pool = [(p, fp) for p, fp in unconstrained
            if all(fp.isdisjoint(hh) or geometry.relative(a, p) in allowed
                   for a, hh in zip(fixed, halos))]
    # Second complete inventory, using transported directed support.
    raw = {geometry.transport(a, t) for a in fixed for t in allowed}
    transported = []
    for p in sorted(raw):
        fp = geometry.pixels(p)
        if fp & occupied or not fp & set(target):
            continue
        if all(fp.isdisjoint(hh) or geometry.relative(a, p) in allowed
               for a, hh in zip(fixed, halos)):
            transported.append((p, fp))
    require(pool == transported, 'final pool inventories differ')
    blocked = tuple(data['blocked_second_cell'])
    require(blocked in target, 'blocked pixel is not a required halo cell')
    require(all(blocked not in fp for p, fp in pool), 'blocked pixel has an admissible owner')
    return len(unconstrained), len(pool), blocked


def positive_first(geometry, star):
    root = geometry.pixels(geometry.root)
    occupied = geometry.union([geometry.root]+list(star))
    require(u.halo(root) <= occupied, 'first collar incomplete')
    require(u.disc(occupied), 'first prefix is not a disc')
    require(all(geometry.pixels(p) & u.halo(root) for p in star),
            'new first copy misses preceding prefix')
    return len(occupied)


def reject(call, name):
    try:
        call()
    except ValueError as exc:
        require('guard' not in str(exc), 'negative control only hit a guard')
        return name
    raise ValueError('negative control accepted: '+name)


def check():
    global DEADLINE
    DEADLINE = time.monotonic()+35
    data = json.loads((HERE/'input.json').read_text())
    geometry = u.Geometry(data['cells'])
    require(len(geometry.cells) == 21, 'wrong prototype area')
    pool, cnf, digest = half_formula(geometry.cells)
    require(digest == data['half_formula_sha256'], 'changed half-grid formula')
    trace = (HERE/'floating-support.rup').read_text()
    require(hashlib.sha256(trace.encode()).hexdigest() == data['floating_trace_sha256'],
            'changed floating trace')
    units, additions = phase_units(cnf, len(pool), trace)
    floating = {i for i, (p, fp) in enumerate(pool, 1) if p[1] % 2 or p[2] % 2}
    require(all(-i in units for i in floating), 'unproved floating contact remains')
    allowed, support_nodes = integer_support(data, geometry)
    star, first_nodes, reciprocal_bad = first_catalogue(data, geometry, allowed)
    first_cells = positive_first(geometry, star)
    unconstrained, final_pool, blocked = final_second(data, geometry, star, allowed)
    controls = []
    short = '\n'.join(trace.splitlines()[:-1])+'\n'
    def complete_trace(text):
        uu, steps = phase_units(cnf, len(pool), text)
        require(all(-i in uu for i in floating), 'truncated trace misses an exclusion')
    controls.append(reject(lambda: complete_trace(short), 'truncated floating trace'))
    lookup = {p: i for i, (p, fp) in enumerate(pool, 1)}
    positive = lookup[(star[0][0], 2*star[0][1], 2*star[0][2])]
    controls.append(reject(lambda: phase_units(cnf, len(pool), f'{-positive} 0\n'),
                           'false exclusion of a checked first neighbor'))
    damaged = deepcopy(data)
    damaged['first_catalogue'] = []
    controls.append(reject(lambda: first_catalogue(damaged, geometry, allowed),
                           'omitted unique first surround'))
    damaged = deepcopy(data)
    damaged['blocked_second_cell'] = list(geometry.cells[0])
    controls.append(reject(lambda: final_second(damaged, geometry, star, allowed),
                           'non-halo obstruction pixel'))
    return dict(agent='six-heesch-1', role='researcher', cells=21,
                half_contact_types=len(pool), half_floating_types=len(floating),
                half_formula_variables=len(pool), half_formula_clauses=len(cnf),
                half_formula_sha256=digest, floating_RUP_additions=additions,
                floating_trace_sha256=data['floating_trace_sha256'],
                supported_floating=0, integer_contact_types=len(geometry.integer_contacts),
                integer_supported=len(allowed), integer_excluded=len(data['excluded_integer_types']),
                integer_support_search_nodes=support_nodes,
                reciprocal_integer_exclusions=reciprocal_bad,
                necessary_first_surrounds_for_second_corona=1, first_catalogue_nodes=first_nodes,
                first_disc_copies=7, first_disc_cells=first_cells,
                final_unconstrained_candidates=unconstrained,
                final_directed_candidates=final_pool, blocked_second_cell=list(blocked),
                rejected_controls=controls,
                claim='All corona copies are integral after root normalization; this literal tile has all-motion Hc=Hh=1.',
                scope='A registration/control certificate; no record or historical priority claim. Written phase bridge remains outside a formal kernel.')


if __name__ == '__main__':
    result = check()
    expected = HERE/'expected.json'
    if expected.exists():
        require(result == json.loads(expected.read_text()), 'expected output differs')
    print(json.dumps(result, indent=2, sort_keys=True))
