"""Author controls for the written analytic theorem in ELEVEN.md.
Actual author six-books-2, researcher; no computation is a theorem premise.
Independent degree/core generation, literal local costs, complete small
necessary census, written case checks and sampled literal22 lifts. Stdlib.
"""
from pathlib import Path
from itertools import combinations, permutations, product
from collections import defaultdict
from functools import lru_cache
import json

P = Path(__file__).resolve().parent
Q = 11
PAIRS = tuple(combinations(range(Q), 2))
POINTS = frozenset((0, 1))
R, B, M = 0, 1, 2


def guard(ok, message):
    if not ok:
        raise RuntimeError(message)


def partitions(total, ceiling, remaining):
    if total == 0:
        yield ()
    elif remaining:
        for d in range(min(total, ceiling), 0, -1):
            for rest in partitions(total-d, d, remaining-1):
                yield (d,) + rest


def neighbors(edges, n=Q):
    out = [set() for _ in range(n)]
    for i, j in edges:
        out[i].add(j)
        out[j].add(i)
    return out


def canonical_blue(edges):
    adjacency = neighbors(edges)
    unseen = set(range(Q))
    components = []
    while unseen:
        stack = [min(unseen)]
        vertices = []
        while stack:
            v = stack.pop()
            if v not in unseen:
                continue
            unseen.remove(v)
            vertices.append(v)
            stack.extend(adjacency[v] & unseen)
        classes = defaultdict(list)
        for v in vertices:
            classes[len(adjacency[v])].append(v)
        blocks = [sorted(classes[d]) for d in sorted(classes, reverse=True)]
        best = None
        for choices in product(*(permutations(block) for block in blocks)):
            order = tuple(v for block in choices for v in block)
            code = sum(1 << k for k, (i, j) in enumerate(combinations(range(len(order)), 2))
                       if order[j] in adjacency[order[i]])
            candidate = (code, order)
            if best is None or candidate < best:
                best = candidate
        components.append((len(vertices), best[0], best[1]))
    components.sort(key=lambda t: (-t[0], t[1], t[2]))
    order = tuple(v for size, code, component in components for v in component)
    inverse = {v: i for i, v in enumerate(order)}
    normalized = sorted(tuple(sorted((inverse[i], inverse[j]))) for i, j in edges)
    key = tuple((size, code) for size, code, component in components)
    return key, order, normalized


def generate_domain():
    degree_lists = [d for d in partitions(14, 14, Q)
                    if len(d) + sum(x >= 3 for x in d) >= Q]
    prototypes = {}
    core_attempts = 0
    for ds in degree_lists:
        core_degrees = [d for d in ds if d >= 2]
        nleaves = sum(d == 1 for d in ds)
        core_pairs = list(combinations(range(len(core_degrees)), 2))
        for bits in range(1 << len(core_pairs)):
            core_attempts += 1
            edges = [edge for k, edge in enumerate(core_pairs) if bits >> k & 1]
            degrees = [len(row) for row in neighbors(edges, len(core_degrees))]
            attachments = [d-a for d, a in zip(core_degrees, degrees)]
            if any(a not in (0, 1) for a in attachments):
                continue
            remaining = nleaves - sum(attachments)
            if remaining < 0 or remaining % 2:
                continue
            cursor = len(core_degrees)
            for i, a in enumerate(attachments):
                if a:
                    edges.append((i, cursor))
                    cursor += 1
            for _ in range(remaining // 2):
                edges.append((cursor, cursor+1))
                cursor += 2
            guard(cursor == len(ds) and len(edges) == 7, 'domain construction mismatch')
            guard(sorted((len(x) for x in neighbors(edges) if x), reverse=True) == list(ds),
                  'generated degrees differ')
            key, order, normalized = canonical_blue(edges)
            prototypes.setdefault(key, normalized)
    return degree_lists, core_attempts, sorted(prototypes.items())


def red_set(kind, label, sign=0):
    return POINTS if kind == R else frozenset() if kind == B else frozenset((label ^ sign,))


@lru_cache(None)
def matching_costs(left_kind, right_kind):
    costs = set()
    for left_sign, right_sign in product((0, 1), repeat=2):
        ir = red_set(left_kind, 0, left_sign)
        jr = red_set(right_kind, 0, right_sign)
        jb = POINTS - red_set(right_kind, 1, right_sign)
        costs.add((len(ir & jr), len((POINTS - ir) & jb)))
    return tuple(sorted(costs))


@lru_cache(None)
def matching_relaxation(cost_lists):
    sums = {(0, 0)}
    for costs in cost_lists:
        sums = {(r+a, b+c) for r, b in sums for a, c in costs
                if r+a <= 3 and b+c <= 6}
        if not sums:
            return False
    return bool(sums)


@lru_cache(None)
def uniform_cost(left_kind, right_kind, color):
    totals = set()
    for left_sign, right_sign in product((0, 1), repeat=2):
        ir = red_set(left_kind, 0, left_sign)
        if color == B:
            ir = POINTS-ir
        value = 0
        for label in (0, 1):
            jr = red_set(right_kind, label, right_sign)
            if color == B:
                jr = POINTS-jr
            value += len(ir & jr)
        totals.add(value)
    guard(len(totals) == 1, 'summed uniform costs depend on matching orientations')
    return totals.pop()


def literal_inside_cost(kind, color):
    a = red_set(kind, 0)
    b = red_set(kind, 1)
    if color == B:
        a, b = POINTS-a, POINTS-b
    return len(a & b)


def relation_matrix(red, blue):
    matrix = [[M] * Q for _ in range(Q)]
    for color, edges in ((R, red), (B, blue)):
        for i, j in edges:
            matrix[i][j] = matrix[j][i] = color
    return matrix


def inspect_literal(red, blue):
    matrix = relation_matrix(red, blue)
    for i, j in PAIRS:
        if matrix[i][j] != M:
            continue
        cost_lists = tuple(sorted(matching_costs(matrix[i][k], matrix[j][k])
                                  for k in range(Q) if k not in (i, j)))
        if not matching_relaxation(cost_lists):
            return None
    inside_options = []
    for i in range(Q):
        costs = {color: sum(literal_inside_cost(matrix[i][k], color)
                            for k in range(Q) if k != i) for color in (R, B)}
        inside_options.append([flag for flag in (0, 1)
                               if costs[R if flag else B] <= (3 if flag else 6)])
    if any(not opts for opts in inside_options):
        return []
    restrictions = [[] for _ in range(Q)]
    for i, j in PAIRS:
        color = matrix[i][j]
        if color == M:
            continue
        outside = sum(uniform_cost(matrix[i][k], matrix[j][k], color)
                      for k in range(Q) if k not in (i, j))
        allowed = set()
        for left, right in product((0, 1), repeat=2):
            mate_pages = sum(int(flag == (1 if color == R else 0))
                             for flag in (left, right) for _ in (0, 1))
            if outside + mate_pages <= (6 if color == R else 12):
                allowed.add((left, right))
        if not allowed:
            return []
        restrictions[j].append((i, allowed))
    flags = []
    assignment = []
    def extend(i, word):
        if i == Q:
            flags.append(word)
            return
        for flag in inside_options[i]:
            if all((assignment[j], flag) in allowed for j, allowed in restrictions[i]):
                assignment.append(flag)
                extend(i+1, word | (flag << i))
                assignment.pop()
    extend(0, 0)
    return sorted(flags)


def canonical_record(record):
    key, order, normalized = canonical_blue(record['blue_pairs'])
    inverse = {v: i for i, v in enumerate(order)}
    red = sorted(tuple(sorted((inverse[i], inverse[j]))) for i, j in record['red_pairs'])
    flags = sorted(sum((word >> vertex & 1) << index for index, vertex in enumerate(order))
                   for word in record['flags'])
    return (key, tuple(red), tuple(flags))


# Written labels for checking the proof's formulas, not inputs to generate_domain.
WRITTEN_FORMS = [
    ('triangle_4edges', [(0,1),(0,2),(1,2),(3,4),(5,6),(7,8),(9,10)]),
    ('path5_3edges', [(0,1),(1,2),(2,3),(3,4),(5,6),(7,8),(9,10)]),
    ('triangle_1leaf_3edges', [(0,1),(0,2),(1,2),(0,3),(4,5),(6,7),(8,9)]),
    ('star_arms122_2edges', [(0,1),(0,2),(2,3),(0,4),(4,5),(6,7),(8,9)]),
    ('triangle_2leaves_2edges', [(0,1),(0,2),(1,2),(0,3),(1,4),(5,6),(7,8)]),
    ('triangle_3leaves_edge', [(0,1),(0,2),(1,2),(0,3),(1,4),(2,5),(6,7)]),
]


def red_candidates(blue):
    candidates = []
    for i, j in PAIRS:
        if (i, j) in blue:
            continue
        minimum = sum(uniform_cost(B if tuple(sorted((i,k))) in blue else M,
                                   B if tuple(sorted((j,k))) in blue else M, R)
                      for k in range(Q) if k not in (i,j))
        if minimum <= 6:
            candidates.append((i,j))
    return candidates


def w_matrix(red, blue):
    w = [[0]*Q for _ in range(Q)]
    for color, edges in ((1,red),(-1,blue)):
        for i,j in edges:
            w[i][j] = w[j][i] = color
    return w


def w_square(w, i, j):
    return sum(w[i][k]*w[k][j] for k in range(Q))


def outside_sum(matrix, i, j, color):
    return sum(uniform_cost(matrix[i][k],matrix[j][k],color)
               for k in range(Q) if k not in (i,j))


def written_case_controls():
    counts = {'triangle_red_triples':0, 'triangle_red_spine_fail':0,
              'triangle_blue_spine_fail':0, 'triangle_red_sum_identities':0,
              'path_red_triples':0, 'path_matching_square_identities':0,
              'path_missing_forced_red_pair':0, 'path_red_spine_fail':0,
              'path_middle_inside_blue_conflict':0, 'path_known_core':0,
              'one_leaf_fixed_square_cases':0, 'arms_fixed_square_cases':0,
              'two_leaf_square_identities':0, 'two_leaf_support_cases':0,
              'three_leaf_support_cases':0}
    for name, blue_list in WRITTEN_FORMS:
        blue = set(blue_list)
        for rt in combinations(red_candidates(blue),3):
            red = set(rt)
            matrix = relation_matrix(red,blue)
            w = w_matrix(red,blue)
            support = {v for edge in red|blue for v in edge}
            if name == 'triangle_4edges':
                counts['triangle_red_triples'] += 1
                nr = neighbors(red)
                for a,x in red:
                    guard(a < 3 <= x, 'triangle R pair outside A-H')
                    y = next(iter(neighbors(blue)[x]))
                    expected = 5+len(nr[a])-int(y in nr[a])
                    guard(outside_sum(matrix,a,x,R) == expected, 'triangle red sum identity')
                    counts['triangle_red_sum_identities'] += 1
                if any(outside_sum(matrix,a,x,R)>6 for a,x in red):
                    counts['triangle_red_spine_fail'] += 1
                else:
                    incident = [a for a in range(3) if nr[a]]
                    guard(len(incident)>=2 and all(len(nr[a])<=2 for a in incident),
                          'triangle red degree conclusion')
                    guard(all(outside_sum(matrix,a,x,R)==6 for a,x in red),
                          'triangle inside colors not forced blue')
                    a,b = incident[:2]
                    guard(outside_sum(matrix,a,b,B)+4>=13, 'triangle blue contradiction')
                    counts['triangle_blue_spine_fail'] += 1
            elif name == 'path5_3edges':
                counts['path_red_triples'] += 1
                guard(w_square(w,0,2)==1-int((0,3) in red), 'path02 square')
                guard(w_square(w,2,4)==1-int((1,4) in red), 'path24 square')
                counts['path_matching_square_identities'] += 2
                if not {(0,3),(1,4)}<=red:
                    counts['path_missing_forced_red_pair'] += 1
                    continue
                third = (red-{(0,3),(1,4)}).pop()
                if third == (1,3):
                    guard(all(outside_sum(matrix,i,j,R)==6 for i,j in red), 'path red saturation')
                    guard(outside_sum(matrix,0,1,B)==8, 'path blue saturation')
                    counts['path_known_core'] += 1
                elif third[0] in (1,3) and third[1]>=5:
                    spine = (1,4) if third[0]==1 else (0,3)
                    guard(outside_sum(matrix,*spine,R)==7, 'path external red contradiction')
                    counts['path_red_spine_fail'] += 1
                else:
                    guard(third[0]==2 and third[1]>=5, 'unexpected path third R pair')
                    guard(outside_sum(matrix,*third,R)==6, 'path middle R inside constraint')
                    guard(outside_sum(matrix,1,4,R)==6, 'path endpoint inside constraint')
                    guard(outside_sum(matrix,1,2,B)+4==13, 'path middle blue contradiction')
                    counts['path_middle_inside_blue_conflict'] += 1
            elif name == 'triangle_1leaf_3edges':
                guard(not neighbors(red)[3] and matrix[3][1]==M and w_square(w,3,1)==1,
                      'one-leaf fixed square')
                counts['one_leaf_fixed_square_cases'] += 1
            elif name == 'star_arms122_2edges':
                guard(not neighbors(red)[1] and matrix[1][2]==M and w_square(w,1,2)==1,
                      'arms fixed square')
                counts['arms_fixed_square_cases'] += 1
            elif name == 'triangle_2leaves_2edges':
                guard(matrix[3][2]==M and w_square(w,3,2)==1-int((1,3) in red),
                      'two-leaf32 square')
                guard(matrix[4][2]==M and w_square(w,4,2)==1-int((0,4) in red),
                      'two-leaf42 square')
                counts['two_leaf_square_identities'] += 2
                if len(support)==Q:
                    guard(not {(1,3),(0,4)}<=red, 'two leaves fit R budget with full support')
                    counts['two_leaf_support_cases'] += 1
            else:
                if len(support)==Q:
                    guard(all(i>=8 or j>=8 for i,j in red), 'three-isolate budget')
                    guard(not neighbors(red)[3] and matrix[3][1]==M and w_square(w,3,1)==1,
                          'three-leaf fixed square')
                    counts['three_leaf_support_cases'] += 1
    balanced = [word for word in range(1<<6) if word.bit_count()==3]
    dots = {6-2*(a^b).bit_count() for a,b in product(balanced,repeat=2)}
    guard(dots=={-6,-2,2,6}, 'known path balanced-row contradiction')
    counts['known_path_balanced_row_pairs'] = len(balanced)**2
    counts['known_path_mutual_dot_values'] = sorted(dots)
    return counts


def lifted_controls():
    all_points = (1<<(2*Q))-1
    counts = {'lifts':0, 'full_literal_spines':0, 'matching_combined_page_identities':0,
              'uniform_summed_page_identities':0, 'inside_page_identities':0}
    for form_index,(name,blue_list) in enumerate(WRITTEN_FORMS):
        blue = set(blue_list)
        candidates = red_candidates(blue)
        for seed in range(8):
            red = {candidates[(seed+offset)%len(candidates)] for offset in (0,5,11)}
            guard(len(red)==3, 'sample marking duplicate')
            matrix = relation_matrix(red,blue)
            w = w_matrix(red,blue)
            word = (0x5a5 ^ (73*seed+127*form_index)) & ((1<<Q)-1)
            adjacency = [0]*(2*Q)
            signs = {}
            def edge(a,b):
                adjacency[a] |= 1<<b
                adjacency[b] |= 1<<a
            for i in range(Q):
                if word>>i&1:
                    edge(2*i,2*i+1)
            for i,j in PAIRS:
                kind = matrix[i][j]
                if kind==R:
                    for a,b in product((0,1),repeat=2):
                        edge(2*i+a,2*j+b)
                elif kind==M:
                    orientation = (i*19+j*37+seed*11+form_index*7+i*j)&1
                    signs[i,j] = orientation
                    for a in (0,1):
                        edge(2*i+a,2*j+(a^orientation))
            complement = [all_points & ~row & ~(1<<i) for i,row in enumerate(adjacency)]
            red_pages,blue_pages = {},{}
            for a,b in combinations(range(2*Q),2):
                red_pages[a,b] = (adjacency[a]&adjacency[b]).bit_count()
                blue_pages[a,b] = (complement[a]&complement[b]).bit_count()
                counts['full_literal_spines'] += 1
            for i,j in PAIRS:
                kind = matrix[i][j]
                if kind==M:
                    label = signs[i,j]
                    rp = red_pages[2*i,2*j+label]
                    bp = blue_pages[2*i,2*j+(1^label)]
                    guard(rp+bp==9+w_square(w,i,j), 'literal matching combined pages')
                    counts['matching_combined_page_identities'] += 1
                else:
                    pages = red_pages if kind==R else blue_pages
                    actual = pages[2*i,2*j]+pages[2*i,2*j+1]
                    inside = 2*sum(int((word>>k&1)==(1 if kind==R else 0)) for k in (i,j))
                    guard(actual==outside_sum(matrix,i,j,kind)+inside, 'literal uniform summed pages')
                    counts['uniform_summed_page_identities'] += 1
            for i in range(Q):
                color = R if word>>i&1 else B
                expected = sum(literal_inside_cost(matrix[i][k],color) for k in range(Q) if k!=i)
                actual = (red_pages if color==R else blue_pages)[2*i,2*i+1]
                guard(actual==expected, 'literal inside pages')
                counts['inside_page_identities'] += 1
            counts['lifts'] += 1
    return counts


def main():
    degree_lists,attempts,domain = generate_domain()
    guard(len(degree_lists)==10 and len(domain)==6, 'degree/core domain')
    names = {canonical_blue(edges)[0]:name for name,edges in WRITTEN_FORMS}
    guard(set(names)=={key for key,edges in domain}, 'written/generated blue forms differ')
    cases,records = [],[]
    for key,blue_list in domain:
        blue = set(blue_list)
        candidates = red_candidates(blue)
        case = {'name':names[key], 'red_candidate_count':len(candidates),
                'red_triples':0, 'support11_pass':0, 'matching_budget_pass':0,
                'necessary_survivors':0, 'inside_flag_survivors':0}
        cases.append(case)
        for rt in combinations(candidates,3):
            case['red_triples'] += 1
            red = set(rt)
            if len({v for edge in red|blue for v in edge})!=Q:
                continue
            case['support11_pass'] += 1
            flags = inspect_literal(red,blue)
            if flags is None:
                continue
            case['matching_budget_pass'] += 1
            if flags:
                case['necessary_survivors'] += 1
                case['inside_flag_survivors'] += len(flags)
                records.append({'blue_pairs':blue_list,'red_pairs':sorted(red),'flags':flags})
    fields = ('red_triples','support11_pass','matching_budget_pass','necessary_survivors','inside_flag_survivors')
    totals = {field:sum(c[field] for c in cases) for field in fields}
    # A direct description of the known record is checked only after generation.
    expected_flags = [word for word in range(1<<Q)
                      if all(not(word>>i&1) for i in (0,1,3,4))
                      and all((word>>i&1)+(word>>j&1)>=1 for i,j in ((5,6),(7,8),(9,10)))]
    known = {'blue_pairs':dict(WRITTEN_FORMS)['path5_3edges'],
             'red_pairs':[(0,3),(1,3),(1,4)], 'flags':expected_flags}
    computed = {canonical_record(record) for record in records}
    guard(len(records)==1 and len(expected_flags)==54 and computed=={canonical_record(known)},
          'entire surviving record or inside words differ from the known core')
    altered = json.loads(json.dumps(records))
    altered[0]['flags'][0] ^= 1
    guard({canonical_record(record) for record in altered}!=computed, 'altered flag not rejected')
    guard({canonical_record(record) for record in records[1:]}!=computed, 'missing record not rejected')
    canonical_key,canonical_red,canonical_flags = next(iter(computed))
    _,_,canonical_blue_edges = canonical_blue(known['blue_pairs'])
    summary = {
        'agent':'six-books-2', 'role':'researcher', 'complete':True,
        'written_analytic_proof':'ELEVEN.md', 'controls_not_theorem_premise':True,
        'positive_degree_lists':degree_lists, 'nonleaf_core_attempts':attempts,
        'blue_forms_independently_generated':len(domain),
        'cases':sorted(cases,key=lambda c:c['name']), 'totals':totals,
        'survivor':{'canonical_blue_pairs':canonical_blue_edges,
                    'canonical_red_pairs':canonical_red,'canonical_inside_words':canonical_flags,
                    'known_arbitrary_complement_path_core':True,'core_complement_matching_blocks':30},
        'all_survivors_and_inside_words_checked':True,
        'altered_flag_rejected':True, 'missing_record_rejected':True,
        'written_case_controls':written_case_controls(),
        'literal_lift_controls':lifted_controls(),
        'full_matching_sign_enumeration':False,
        'normalization_and_completeness_are_written_not_sampled_inferences':True,
        'author_controls_are_not_independent_peer_review':True,
    }
    print(json.dumps(summary,indent=2))


if __name__ == '__main__':
    main()
