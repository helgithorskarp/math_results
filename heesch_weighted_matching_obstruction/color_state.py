"""Rotations-only color/state polyhex models and exact small-cover encodings.

No claim follows from SAT rooted covers alone.  Definition-level decoding
uses closed-form inverse rotations, independently of the forward generator.
"""
import itertools

import hex_domain as hexgrid
import marked_corona as signed


def validate_labels(tile, colors, states):
    n = len(hexgrid.boundary(tile))
    signed.check_witness({'grid': 'hex', 'tile': tile, 'signs': [0] * n,
                         'depth': 0, 'patch': [{'level': 0, 'reflect': False,
                                               'turns': 0, 'translation': [0, 0]}]})
    if len(colors) != n or any(type(c) is not int or c < 1 for c in colors):
        raise ValueError("one positive integer color per original boundary port")
    if len(states) != n or any(type(s) is not int or s not in (-1, 0, 1) for s in states):
        raise ValueError("one state in {-1,0,1} per original boundary port")


def color_constraints(circuit, colors, incidences):
    """An active boundary incidence fixes the shared edge's color bits."""
    width = max(1, (max(colors) - 1).bit_length())
    edge_bits = {}
    for active, edges in incidences:
        for index, (edge, _side) in enumerate(edges):
            bits = edge_bits.setdefault(edge, [])
            if not bits:
                bits.extend(circuit.new() for _ in range(width))
            value = colors[index] - 1
            for k, bit in enumerate(bits):
                circuit.clause([-active, bit if (value >> k) & 1 else -bit])
    return edge_bits


def build_corona(tile, depth, colors, states, Circuit):
    tile = tuple(map(tuple, tile))
    validate_labels(tile, colors, states)
    circuit, candidates, signs, stats = signed.build(
        tile, depth, None, None, Circuit, hexgrid.topology_constraint,
        fixed=states, domain=hexgrid, allow_reflections=False, require_charge=False)
    incidences = itertools.chain([(circuit.true, hexgrid.oriented(tile, False, 0)[1])],
                                ((c['z'][depth], c['ports']) for c in candidates))
    bits = color_constraints(circuit, colors, incidences)
    stats.update(variables=circuit.nv, clauses=len(circuit.clauses), color_edges=len(bits),
                 mode='complete_disc_coronas', matching='equal color, opposite state',
                 reflections=False)
    return circuit, candidates, stats


def variable_color_constraints(circuit, port_bits, incidences):
    edge_bits = {}
    for active, edges in incidences:
        for index, (edge, _side) in enumerate(edges):
            if edge not in edge_bits:
                edge_bits[edge] = tuple(circuit.new() for _ in port_bits[index])
            for source, target in zip(port_bits[index], edge_bits[edge]):
                circuit.clause([-active, -source, target])
                circuit.clause([-active, source, -target])
    return edge_bits


def exclude_periodic_pairs(circuit, port_bits, signs, pairs):
    """Exclude EVERY marking compatible with this validated periodic motif.

    Its matching conditions are equal colors and opposite states at every
    pair. Negating their conjunction is the disjunction encoded here.
    This is a construction-side certificate, not a presumed finite bound.
    """
    differences = []
    for i, j in pairs:
        differences.extend(circuit.xor(x, y) for x, y in zip(port_bits[i], port_bits[j]))
        differences.extend((circuit.xor(signs[i][0], signs[j][1]),
                            circuit.xor(signs[i][1], signs[j][0])))
    circuit.clause(differences)


def canonical_partition_constraints(circuit, port_bits):
    """Color value is the first port index in its equality class.

    Any partition has exactly one such naming. Port i chooses j<=i and,
    if j<i, requires that port j names itself. This preserves every matching
    table up to color renaming; states are unaffected.
    """
    equal = []
    for i, bits in enumerate(port_bits):
        row = [circuit.and_([bit if (j >> k) & 1 else -bit
                            for k, bit in enumerate(bits)]) for j in range(i + 1)]
        equal.append(row)
        circuit.clause(row)
        for j in range(i):
            circuit.clause([-row[j], equal[j][j]])


def build_synthesis(tile, depth, Circuit, states=None):
    """All self-color partitions, and optionally all ternary directed states.

    n ports require at most n colors. A binary palette of 2^ceil(log2(n))
    therefore includes every marking up to color renaming. No count/charge
    condition is imposed. Port zero's color is fixed to zero by renaming.
    """
    tile = tuple(map(tuple, tile))
    n = len(hexgrid.boundary(tile))
    if states is not None:
        validate_labels(tile, [1] * n, states)
    else:
        validate_labels(tile, [1] * n, [0] * n)
    circuit, candidates, signs, stats = signed.build(
        tile, depth, None, None, Circuit, hexgrid.topology_constraint,
        fixed=states, domain=hexgrid, allow_reflections=False, require_charge=False)
    width = max(1, (n - 1).bit_length())
    port_bits = [tuple(circuit.new() for _ in range(width)) for _ in range(n)]
    for bit in port_bits[0]:
        circuit.clause([-bit])
    incidences = itertools.chain([(circuit.true, hexgrid.oriented(tile, False, 0)[1])],
                                ((c['z'][depth], c['ports']) for c in candidates))
    edges = variable_color_constraints(circuit, port_bits, incidences)
    stats.update(mode='color_state_synthesis', color_width=width, palette=2**width,
                 variables=circuit.nv, clauses=len(circuit.clauses), color_edges=len(edges),
                 state_mode='all ternary states' if states is None else 'fixed states')
    return circuit, candidates, port_bits, signs, stats


def region(tile, radius):
    if type(radius) is not int or radius < 0:
        raise ValueError('nonnegative integer radius')
    ball = [(x, y) for x in range(-radius, radius + 1)
            for y in range(-radius, radius + 1) if abs(x + y) <= radius]
    return {(x + dx, y + dy) for x, y in tile for dx, dy in ball}


def build_cover(tile, radius, colors, states, Circuit):
    """Rooted cover of P+B_radius, controlling overlap outside the target too.

    Every candidate meets the target.  Enumerating a target cell minus each
    oriented base cell gives ALL such translations. No topology or corona
    rank constraint is imposed: UNSAT is an upper bound; SAT is only a cover.
    """
    validate_labels(tile, colors, states)
    circuit, candidates, incidences, stats = cover_geometry(tile, radius, Circuit)
    signs = [(circuit.true if s == 1 else circuit.false,
              circuit.true if s == -1 else circuit.false) for s in states]
    signed.edge_state_constraints(circuit, signs, incidences)
    bits = color_constraints(circuit, colors, incidences)
    stats.update(mode='rooted_cover', variables=circuit.nv, clauses=len(circuit.clauses),
                 color_edges=len(bits))
    return circuit, candidates, stats


def cover_geometry(tile, radius, Circuit):
    """Unmarked geometric part; callers validate the base and add labels."""
    target, root = region(tile, radius), set(map(tuple, tile))
    circuit, candidates = Circuit(), []
    for turns in range(6):
        cells, ports = hexgrid.oriented(tile, False, turns)
        translations = {(x - a, y - b) for x, y in target for a, b in cells}
        for tx, ty in sorted(translations):
            moved = tuple((x + tx, y + ty) for x, y in cells)
            if root.intersection(moved):
                continue
            candidates.append({'cells': moved, 'turns': turns, 'reflect': False,
                               'translation': (tx, ty), 'active': circuit.new(),
                               'ports': [(tuple((x + tx, y + ty) for x, y in edge), side)
                                         for edge, side in ports]})
    covers = {}
    for c in candidates:
        for cell in c['cells']:
            covers.setdefault(cell, []).append(c['active'])
    for cell in sorted(target - root):
        circuit.clause(covers.get(cell, []))
    for cell in sorted(covers):
        signed.at_most_one(circuit, covers[cell])
    incidences = [(circuit.true, hexgrid.oriented(tile, False, 0)[1])]
    incidences.extend((c['active'], c['ports']) for c in candidates)
    return circuit, candidates, incidences, {'radius': radius,
        'target_cells': len(target), 'candidate_cells': len(covers) + len(root),
        'candidates': len(candidates), 'reflections': False}


def build_cover_synthesis(tile, radius, Circuit, states=None, canonical_colors=False):
    """Every self-color partition and, optionally, every ternary state table."""
    n = len(hexgrid.boundary(tile))
    validate_labels(tile, [1] * n, states if states is not None else [0] * n)
    circuit, candidates, incidences, stats = cover_geometry(tile, radius, Circuit)
    if states is None:
        signs = [(circuit.new(), circuit.new()) for _ in range(n)]
        for a, b in signs:
            circuit.clause([-a, -b])
    else:
        signs = [(circuit.true if s == 1 else circuit.false,
                  circuit.true if s == -1 else circuit.false) for s in states]
    signed.edge_state_constraints(circuit, signs, incidences)
    width = max(1, (n - 1).bit_length())
    port_bits = [tuple(circuit.new() for _ in range(width)) for _ in range(n)]
    for bit in port_bits[0]:
        circuit.clause([-bit])
    if canonical_colors:
        canonical_partition_constraints(circuit, port_bits)
    edges = variable_color_constraints(circuit, port_bits, incidences)
    stats.update(mode='cover_synthesis', color_width=width, palette=2**width,
                 variables=circuit.nv, clauses=len(circuit.clauses), color_edges=len(edges),
                 state_mode='all ternary states' if states is None else 'fixed states',
                 canonical_colors=canonical_colors)
    return circuit, candidates, port_bits, signs, stats


def rotate(p, turns):
    """Closed forms for the six rotations, used only in direct decoders."""
    x, y = p
    return ((x, y), (-y, x + y), (-x - y, x), (-x, -y),
            (y, -x - y), (x + y, -x))[turns]


def placement(tile, record):
    turns = record['turns']
    if record.get('reflect', False) is not False or type(turns) is not int or not 0 <= turns < 6:
        raise ValueError('rotations-only model')
    tx, ty = record['translation']
    if type(tx) is not int or type(ty) is not int:
        raise ValueError('integer translation required')
    raw = [rotate(p, turns) for p in tile]
    ox, oy = min(x for x, y in raw), min(y for x, y in raw)
    cells = {(x - ox + tx, y - oy + ty) for x, y in raw}

    def inverse(p):
        return rotate((p[0] + ox - tx, p[1] + oy - ty), (-turns) % 6)
    return cells, inverse


def check_patch(tile, colors, states, records, target=None):
    """Independent ownership and original-port decoding of a finite patch."""
    validate_labels(tile, colors, states)
    original = {port: i for i, port in enumerate(hexgrid.boundary(tile))}
    owners, inverses = {}, []
    roots = 0
    for k, record in enumerate(records):
        cells, inverse = placement(tile, record)
        if cells & owners.keys():
            raise ValueError('cell overlap')
        if record.get('level') == 0:
            roots += 1
            if record['turns'] or tuple(record['translation']) != (0, 0) or cells != set(map(tuple, tile)):
                raise ValueError('wrong rooted copy')
        for cell in cells:
            owners[cell] = k
        inverses.append(inverse)
    if roots != 1:
        raise ValueError('expected exactly one root')
    if target is not None and not set(target) <= owners.keys():
        raise ValueError('target not covered')
    checks, pairs = 0, set()
    for cell, owner in sorted(owners.items()):
        inverse = inverses[owner]
        for dx, dy in hexgrid.NEIGHBORS:
            other_cell = cell[0] + dx, cell[1] + dy
            other = owners.get(other_cell)
            if other is None or other == owner:
                continue
            other_inverse = inverses[other]
            a = original[inverse(cell), inverse(other_cell)]
            b = original[other_inverse(other_cell), other_inverse(cell)]
            if colors[a] != colors[b] or states[a] != -states[b]:
                raise ValueError('incompatible actual boundary incidence')
            pairs.add(tuple(sorted((a, b))))
            checks += 1
    return {'copies': len(records), 'cells': len(owners),
            'matched_boundary_incidences': checks, 'original_port_inverse_decoding': True,
            'matching_port_pairs': [list(p) for p in sorted(pairs)]}


def check_corona(witness):
    # The signed checker independently verifies full halo completion and
    # hole-free connected topology of every prefix. Then decode all colors.
    stats = signed.check_witness(witness)
    stats['color_checks'] = check_patch(witness['tile'], witness['colors'],
                                       witness['signs'], witness['patch'])
    return stats


def check_cover(witness):
    if witness.get('mode') != 'rooted_cover' or witness.get('grid') != 'hex':
        raise ValueError('wrong cover mode or grid')
    return check_patch(witness['tile'], witness['colors'], witness['signs'], witness['patch'],
                       region(witness['tile'], witness['radius']))


def periodic_representative(cell, a, b, c):
    q, y = divmod(cell[1], c)
    return (cell[0] - q * b) % a, y


def build_periodic(tile, colors, states, a, b, c, Circuit):
    """Exact periodic-screen CNF for periods (a,0),(b,c), with boundary labels."""
    if any(type(v) is not int for v in (a, b, c)) or a < 1 or c < 1 or not 0 <= b < a:
        raise ValueError('positive HNF periods required')
    validate_labels(tile, colors, states)
    rep = lambda p: periodic_representative(p, a, b, c)
    circuit, candidates, covers, incidences = Circuit(), [], {}, []
    positive = hexgrid.NEIGHBORS[:3]
    for turns in range(6):
        cells, ports = hexgrid.oriented(tile, False, turns)
        for tx, ty in itertools.product(range(a), range(c)):
            moved = tuple((x + tx, y + ty) for x, y in cells)
            classes = [rep(p) for p in moved]
            if len(set(classes)) != len(classes):
                continue
            active = circuit.new()
            edges = []
            for edge, side in ports:
                owner, neighbor = edge[side], edge[1 - side]
                owner = owner[0] + tx, owner[1] + ty
                neighbor = neighbor[0] + tx, neighbor[1] + ty
                difference = neighbor[0] - owner[0], neighbor[1] - owner[1]
                if difference in positive:
                    key, incidence_side = (rep(owner), difference), 0
                else:
                    key, incidence_side = (rep(neighbor), (-difference[0], -difference[1])), 1
                edges.append((key, incidence_side))
            candidate = {'turns': turns, 'reflect': False, 'translation': (tx, ty),
                         'cells': moved, 'active': active}
            candidates.append(candidate)
            incidences.append((active, edges))
            for cell in classes:
                covers.setdefault(cell, []).append(active)
    for cell in itertools.product(range(a), range(c)):
        xs = covers.get(cell, [])
        circuit.clause(xs)
        signed.at_most_one(circuit, xs)
    signs = [(circuit.true if s == 1 else circuit.false,
              circuit.true if s == -1 else circuit.false) for s in states]
    signed.edge_state_constraints(circuit, signs, incidences)
    color_constraints(circuit, colors, incidences)
    return circuit, candidates


def check_periodic(tile, colors, states, records, a, b, c):
    """Check an infinite periodic tiling through inverse cell owners.

    An entry for each cell class determines its owner in every translate.
    All boundary contacts from one fundamental set are decoded, including
    contacts crossing either period and contacts to translates of one motif.
    """
    validate_labels(tile, colors, states)
    if a < 1 or c < 1 or not 0 <= b < a:
        raise ValueError('invalid HNF periods')
    rep = lambda p: periodic_representative(p, a, b, c)
    original = {port: i for i, port in enumerate(hexgrid.boundary(tile))}
    owners, data = {}, []
    for k, record in enumerate(records):
        cells, inverse = placement(tile, record)
        for cell in cells:
            key = rep(cell)
            if key in owners:
                raise ValueError('periodic cell overlap')
            owners[key] = k, cell
        data.append((cells, inverse))
    if set(owners) != set(itertools.product(range(a), range(c))):
        raise ValueError('periodic uncovered cell')

    def owner(cell):
        k, base = owners[rep(cell)]
        displacement = cell[0] - base[0], cell[1] - base[1]
        if displacement[1] % c or (displacement[0] - (displacement[1] // c) * b) % a:
            raise ValueError('not a lattice displacement')
        return (k, displacement), data[k][1]

    checks, pairs = 0, set()
    for _key, (_k, cell) in sorted(owners.items()):
        placement1, inverse1 = owner(cell)
        for dx, dy in hexgrid.NEIGHBORS:
            other_cell = cell[0] + dx, cell[1] + dy
            placement2, inverse2 = owner(other_cell)
            if placement1 == placement2:
                continue
            d1, d2 = placement1[1], placement2[1]
            local = lambda p, d: (p[0] - d[0], p[1] - d[1])
            i = original[inverse1(local(cell, d1)), inverse1(local(other_cell, d1))]
            j = original[inverse2(local(other_cell, d2)), inverse2(local(cell, d2))]
            if colors[i] != colors[j] or states[i] != -states[j]:
                raise ValueError('periodic boundary mismatch')
            pairs.add(tuple(sorted((i, j))))
            checks += 1
    return {'periods': [[a, 0], [b, c]], 'determinant': a * c,
            'motif_copies': len(records), 'cell_classes': len(owners),
            'boundary_incidences': checks, 'original_port_inverse_decoding': True,
            'matching_port_pairs': [list(p) for p in sorted(pairs)]}
