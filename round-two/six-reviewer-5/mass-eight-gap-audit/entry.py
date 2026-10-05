"""Independent partial audit of 10300. No author executable/EXPECTED input.

Exact continuity, all 73 energy-entry cells, and closed tree/enclosures.
This program DOES NOT discharge the 139 origin/polar face contradictions.
"""
import copy
import hashlib
import json
import math
import pathlib
import re
from fractions import Fraction as F

HERE = pathlib.Path(__file__).resolve().parent
PIN = '70a773a61a3a7074719c124318ae8e9bf2e6b5d7719af45709dcefed2b8ed55a'
LOW, HIGH = F(2, 3), F(27, 40)
MINB, MAXB, MINAB, C = F(871, 1600), F(5, 9), F(23517, 64000), F(197, 360)
FLOOR, TMAX = F(40, 67), F(40824, 4489)
ROOT = tuple(map(F, ('2/3', '27/40', '0', '23/5', '51/80', '1', '0', '23/40')))
ROLES = {'scalar-product-origin', 'retained-mean-product-origin', 'standard-polar', 'joint-energy-polar'}

def require(ok, reason):
    if not ok:
        raise ValueError(reason)

def add(*terms):
    out = [F(0)] * max(map(len, terms))
    for term in terms:
        for i, x in enumerate(term):
            out[i] += x
    return out

def scale(values, factor):
    return [factor * x for x in values]

def multiply(left, right):
    out = [F(0)] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            out[i+j] += x * y
    return out

def power(values, exponent):
    out = [F(1)]
    for _ in range(exponent):
        out = multiply(out, values)
    return out

def integral(values, weight=0):
    return sum((x / (i + weight + 1) for i, x in enumerate(values)), F(0))

def beta_integral(i, j):
    return F(math.factorial(i) * math.factorial(j), math.factorial(i+j+1))

def binomial_linear(a, b, degree):
    return [math.comb(degree, i)*a**(degree-i)*b**i for i in range(degree+1)]

def root_grid(x, grid, upward):
    require(x >= 0 and type(grid) is int and grid > 0, 'root domain')
    floor = math.isqrt(x.numerator * grid**2 // x.denominator)
    result = floor + int(upward and F(floor, grid)**2 < x)
    if upward:
        require(F(result, grid)**2 >= x and (result == 0 or F(result-1, grid)**2 < x), 'minimal upper root')
    else:
        require(F(result, grid)**2 <= x and F(result+1, grid)**2 > x, 'maximal lower root')
    return F(result, grid)

def canonical_rational(value):
    require(type(value) is str and re.fullmatch(r'-?(0|[1-9][0-9]*)(/[1-9][0-9]*)?', value) is not None, 'rational text type/syntax')
    number = F(value)
    require(str(number) == value, 'canonical rational text')
    return number

def decode_cover(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate JSON key')
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=pairs)

def cover_cells(cover):
    require(type(cover) is dict and set(cover) == {'root', 'splits', 'leaves'}, 'cover schema')
    require(type(cover['root']) is list and len(cover['root']) == 8, 'root schema')
    root = tuple(map(canonical_rational, cover['root']))
    require(root == ROOT, 'entire closed root')
    splits, leaves = cover['splits'], cover['leaves']
    require(type(splits) is dict and type(leaves) is dict, 'tree maps')
    require(not set(splits).intersection(leaves), 'internal/leaf disjointness')
    for path in list(splits) + list(leaves):
        require(type(path) is str and re.fullmatch('[01]*', path) is not None, 'binary path schema')
    for path, role in leaves.items():
        require(type(role) is str and role in ROLES, 'defining role')
    for path, split in splits.items():
        require(type(split) is dict and set(split) == {'axis', 'cut'}, 'split schema')
        require(type(split['axis']) is int and 0 <= split['axis'] < 4, 'axis integer/type/range')
        canonical_rational(split['cut'])
    seen, output = set(), []
    def visit(path, box):
        require(path not in seen, 'unique reachability')
        seen.add(path)
        if path in leaves:
            output.append(dict(path=path, role=leaves[path], raw_box=box))
            return
        require(path in splits, 'complete child coverage')
        split = splits[path]
        position, cut = 2*split['axis'], canonical_rational(split['cut'])
        require(box[position] < cut < box[position+1], 'strict interior cut')
        left, right = list(box), list(box)
        left[position+1], right[position] = cut, cut
        # Both children are CLOSED and have their entire common cut face.
        require(tuple(left[:position]+left[position+2:]) == tuple(right[:position]+right[position+2:]), 'unchanged coordinates')
        require(left[position] == box[position] and right[position+1] == box[position+1] and left[position+1] == right[position], 'no cut gap')
        visit(path+'0', tuple(left))
        visit(path+'1', tuple(right))
    visit('', root)
    require(seen == set(splits).union(leaves), 'no unreachable tree entries')
    return output, dict(internal_nodes=len(splits), leaves=len(leaves), reachable_nodes=len(seen), maximum_depth=max(map(len, seen)))

def tighten_mass_eight(raw):
    a, b, el, eh, ul, uh, wl, wh = raw
    rounds = []
    for _ in range(4):
        old = (a, b, el, eh, ul, uh, wl, wh)
        uh = min(uh, F(1))
        ul = max(ul, 1-eh/16)
        el = max(el, 2*max(0, 8-8*uh), 8*((1-uh)**2+wl))
        wh = min(wh, 1-ul**2, eh/8-(1-uh)**2)
        new = (a, b, el, eh, ul, uh, wl, wh)
        require(all(new[i] >= old[i] and new[i+1] <= old[i+1] for i in (0, 2, 4, 6)), 'enclosing endpoint monotonicity')
        require(all(new[i] <= new[i+1] for i in (0, 2, 4, 6)), 'nonempty necessary enclosure')
        rounds.append(new)
    m = 1/(1+b)
    require(F(8) > 7*m+1, 'radius-budget monotonicity premise')
    tl = max(0, el-16+16*ul)
    tu = min(eh-2*max(0, 8-8*uh), (7-7*m)**2+7*(m-1)**2)
    require(0 <= tl <= tu <= TMAX, 'whole necessary T interval')
    return rounds, (tl, tu)

def product_cap(box, t_interval):
    a, b, el, eh, ul, uh, wl, wh = box
    tl, tu = t_interval
    square_root = root_grid(F(7, 8)*tu, 4096, True)
    radius = max(F(1), min(8-7/(1+b), 1+square_root))
    z = tl/(2*radius)
    terms = [z**i / math.factorial(i) for i in range(5)]
    horner = 1+z*(1+z*(F(1, 2)+z*(F(1, 6)+z/F(24))))
    require(sum(terms) == horner and radius >= 1 and z >= 0, 'entire product exponential budget')
    return dict(upper_radius=radius, root_ceiling=square_root, exponent=z, all_five_terms=terms, product_upper_bound=1/sum(terms))

def polar_entry(lower, upper):
    # Only mass eight, E >= 23/5. No face/mean/energy-derived derivative input.
    delta = root_grid(lower/56, 1024, False)
    radius_excess = min(root_grid(F(7, 8)*upper, 256, True), 7-7/(1+HIGH))
    p = max(F(0), (F(23, 5)-upper)/2)
    mb = HIGH+C
    mc = HIGH+MAXB*(1+radius_excess)
    nu, alpha = MAXB*(1+radius_excess)/mc, C/mb
    require(radius_excess >= 0 and C-MINB*delta > 0 and 0 <= nu < 1 and 0 <= alpha < 1, 'polar signs/ratios')
    radial = multiply([HIGH, C+7*MINB*delta], power([HIGH, C-MINB*delta], 7))
    g2 = add(*[scale(binomial_linear(1, -1, n), F(n+1)*nu**n/mc**2) for n in range(5)])
    g1 = add(*[scale(binomial_linear(1, -1, n), alpha**n/mb) for n in range(5)])
    kernel = scale([F(0)]+g2, MINAB*p)
    paid = multiply(radial, add([F(1)], scale(kernel, -1), scale(multiply(kernel, kernel), F(1, 2))))
    require(len(paid) == 19, 'complete nineteen polar coefficients')

    # Separate radial expansion, then direct choices in t^i (1-t)^n.
    radial_other = [F(0)]*9
    for i in range(9):
        phi = ((-1)**i * math.comb(7, i) if i <= 7 else 0) + (7*(-1)**(i-1)*math.comb(7, i-1) if i >= 1 else 0)
        part = binomial_linear(HIGH, C, 8-i)
        for j, value in enumerate(part):
            radial_other[i+j] += phi*(MINB*delta)**i*value
    require(radial == radial_other, 'whole independent radial vector')
    other = [F(0)]*19
    beta_payment = F(0)
    k_terms = [(1, n, MINAB*p*(n+1)*nu**n/mc**2) for n in range(5)]
    # The full first-power-deficit kernel has zero coefficient at F=8;
    # g1 is still constructed and checked separately, never discarded silently.
    require(g1 == add(*[scale(power([F(1), F(-1)], n), alpha**n/mb) for n in range(5)]), 'complete reciprocal-one kernel')
    terms = [(0, 0, F(1))] + [(i, n, -x) for i, n, x in k_terms]
    terms += [(i+j, n+m, x*y/2) for i, n, x in k_terms for j, m, y in k_terms]
    for i, r in enumerate(radial_other):
        for shift, n, amount in terms:
            beta_payment += r*amount*beta_integral(i+shift, n)
            for j in range(n+1):
                other[i+shift+j] += r*amount*(-1)**j*math.comb(n, j)
    require(paid == other and integral(paid) == beta_payment, 'whole polar vector and independent beta integral')
    require(beta_payment < F(49, 50), 'strict energy-shell exclusion')
    return dict(interval=[lower, upper], radial=radial, delta_floor=delta, radius_excess_cap=radius_excess, phase_floor=p, g1=g1, g2=g2, complete_coefficients=paid, integral=beta_payment, strict_margin=F(49, 50)-beta_payment)

def continuity(epsilon):
    m, s0 = FLOOR, 8+epsilon
    sigma, radius = (s0-m)/7, s0-7*m
    j_coefficients = binomial_linear(HIGH, MAXB*sigma, 7)
    j = MAXB*integral(j_coefficients, 1)
    c, d = HIGH, MAXB*sigma
    # Substitute y=c+dt in integral t(c+dt)^7, separate endpoint primitive.
    j_other = MAXB/d**2*((c+d)**9/F(9)-c*(c+d)**8/F(8)-c**9/F(9)+c*c**8/F(8))
    require(j == j_other and j < F(7, 12), 'entire energy-independent J derivative')
    ul, eh = F(57, 80)-epsilon/8, F(23, 5)+2*(radius+1)*epsilon
    coupled_energy = eh+16*ul-8
    require(coupled_energy == 8+2*radius*epsilon, 'entire coupled mean-energy identity')
    b = [F(8, 7), -F(16, 7)*LOW*ul, HIGH**2*coupled_energy/7]
    require(b[2] > 0 and b[1]+2*b[2] < 0 and sum(b) > 0, 'B positive/decreasing on entire interval')
    majorant = F(107, 100)
    require(majorant**2 > b[0], 'square-root constant valid')
    cubic = power(b, 3)
    other = [F(0)]*7
    for constant_count in range(4):
        for linear_count in range(4-constant_count):
            quadratic_count = 3-constant_count-linear_count
            other[linear_count+2*quadratic_count] += F(math.factorial(3), math.factorial(constant_count)*math.factorial(linear_count)*math.factorial(quadratic_count))*b[0]**constant_count*b[1]**linear_count*b[2]**quadratic_count
    require(cubic == other, 'entire signed cubic')
    o = 9*HIGH*majorant*integral(cubic, 1)
    require(o < F(6, 5), 'origin derivative upper bound')
    ratio_coefficients = binomial_linear(1, epsilon/(8*m), 8)
    require(ratio_coefficients == power([F(1), epsilon/(8*m)], 8), 'entire eight-factor ratio')
    ratio = sum(ratio_coefficients)
    loss = ratio-1+F(6, 5)*epsilon
    require(loss < F(1, 100), 'strict complete origin loss')
    require(j*epsilon < F(1, 600) and 1-j*epsilon > F(49, 50), 'strict clipped J entry and polar loss')
    return dict(epsilon=epsilon, floor=m, radius_cap=radius, seven_radius_mean=sigma, j_coefficients=j_coefficients, j_derivative=j, j_loss=j*epsilon, real_mean_lower=ul, energy_upper=eh, B_coefficients=b, B_at_one=sum(b), B_derivative_at_one=b[1]+2*b[2], full_cubic=cubic, origin_derivative=o, product_ratio_coefficients=ratio_coefficients, complete_product_ratio=ratio, origin_loss_using_six_fifths=loss, origin_strict_margin=F(1, 100)-loss)

def ordinary_budgets():
    require(C == LOW+1-LOW**2-HIGH and MINB == 1-HIGH**2 and MAXB == 1-LOW**2 and MINAB == min(LOW*(1-LOW**2), HIGH*(1-HIGH**2)), 'all marked endpoint budgets')
    require(FLOOR == 1/(1+HIGH) and TMAX == 56*(1-FLOOR)**2 and F(72, 8) < TMAX < F(73, 8), 'whole radial budget/last shell')
    floor_coefficients = binomial_linear(HIGH, C*F(37, 40), 8)
    floor_integral = integral(floor_coefficients)
    require(floor_integral == ((HIGH+C*F(37, 40))**9-HIGH**9)/(9*C*F(37, 40)) and floor_integral < F(49, 50), 'complete scalar mass-floor polynomial')
    # Independently verify both exact polynomial identities used in the path.
    # In real/imaginary slot coordinates, removed-slot inequality discards
    # exactly -(1-x Re(q))^2-x^2 Im(q)^2, a nonpositive square sum.
    return dict(marked_interval=[LOW, HIGH], scalar_mass_floor_coefficients=floor_coefficients, scalar_mass_floor_integral=floor_integral, radius_budget=TMAX)

def rejected(operation, reason):
    try:
        operation()
    except ValueError as error:
        require(reason in str(error), 'semantic control rejected for intended reason')
        return reason
    raise ValueError('semantic control incorrectly accepted: '+reason)

def controls(cover):
    cases = []
    for label, change, message in (
        ('axis_bool', lambda c: c['splits'][''].update(axis=True), 'axis integer'),
        ('cut_endpoint', lambda c: c['splits'][''].update(cut=c['root'][4]), 'strict interior cut'),
        ('noncanonical_cut', lambda c: c['splits'][''].update(cut='262/320'), 'canonical rational'),
        ('missing_leaf', lambda c: c['leaves'].pop(next(iter(c['leaves']))), 'complete child coverage'),
        ('extra_leaf', lambda c: c['leaves'].update({'00000':'scalar-product-origin'}), 'no unreachable'),
        ('unknown_role', lambda c: c['leaves'].update({'0000':'wrong-origin'}), 'defining role'),
        ('wrong_root', lambda c: c['root'].__setitem__(1, '11/16'), 'entire closed root'),
    ):
        mutated = copy.deepcopy(cover)
        change(mutated)
        cases.append(dict(case=label, rejection=rejected(lambda: cover_cells(mutated), message)))
    cases.append(dict(case='duplicate_json', rejection=rejected(lambda: decode_cover('{"root":[],"root":[]}'), 'duplicate JSON key')))
    cases.append(dict(case='too_large_gap', rejection=rejected(lambda: continuity(F(1, 349)), 'polar loss')))
    return cases

def serializable(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {key: serializable(x) for key, x in value.items()}
    if isinstance(value, (tuple, list)):
        return [serializable(x) for x in value]
    return value

def main():
    raw = (HERE/'COVER.json').read_bytes()
    require(len(raw) == 15266 and hashlib.sha256(raw).hexdigest() == PIN, 'defining cover bytes before parse')
    cover = decode_cover(raw)
    cells, coverage = cover_cells(cover)
    for cell in cells:
        rounds, interval = tighten_mass_eight(cell['raw_box'])
        cell.update(tightening_rounds=rounds, t_interval=interval, product_payment=product_cap(rounds[-1], interval))
    entries = [polar_entry(F(k, 8), min(F(k+1, 8), TMAX)) for k in range(73)]
    require(entries[0]['interval'][0] == 0 and entries[-1]['interval'][1] == TMAX and all(left['interval'][1] == right['interval'][0] for left, right in zip(entries, entries[1:])), 'all seventy-three consecutive CLOSED shell cells')
    record = dict(agent='six-reviewer-5', role='independent reviewer', scope='PARTIAL only: 73 energy-entry cells, scalar floor, coupled continuity, closed tree and necessary leaf enclosures/product caps. NO leaf origin/polar contradiction audit or complete theorem verdict.', cover_sha256=PIN, budgets=ordinary_budgets(), entry_shells=entries, maximum_entry_integral=max(e['integral'] for e in entries), continuity_original=continuity(F(1, 350)), conditional_improvement=continuity(F(2, 699)), coverage=coverage, roles={role:sum(c['role']==role for c in cells) for role in sorted(ROLES)}, leaf_enclosures=cells, semantic_controls=controls(cover))
    require((HERE/'COVER.json').read_bytes() == raw, 'defining input unchanged')
    print(json.dumps(serializable(record), sort_keys=True, separators=(',', ':')))

if __name__ == '__main__':
    main()
