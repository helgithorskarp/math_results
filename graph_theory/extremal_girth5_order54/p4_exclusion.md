# Excluding the four-vertex-path high forest

**Theorem.** No finite simple graph G of order 54, size 187 and girth at
least five, with thirteen degree-eight vertices, has

    G[V8] = P4 + 2P2 + 5K1.

Here P_j is a path on j vertices. Together with the preceding
[forest reduction](forest_reduction.md) and
[two-P3 exclusion](two_p3_exclusion.md), this leaves exactly the following
**five possible high induced forests**:

| Case | High induced forest | Complete c histograms |
|---|---|---:|
| 5_0 | 5P2 + 3K1 | 49 |
| 5_1 | P3 + 3P2 + 4K1 | 29 |
| 5_2b | 2P3 + P2 + 5K1 | 15 |
| 6_0 | 6P2 + K1 | 24 |
| 6_1 | P3 + 4P2 + 2K1 | 13 |

Existence in these five forests remains unresolved. The table has 130
forest/histogram cases before any partial exploratory exclusions. This
theorem covers all incidences and all fifteen histograms in the excluded
forest. It does not exclude thirteen degree-eight vertices in general,
and the working bounds **185 <= ex(54,{C3,C4}) <= 187** are unchanged.

## 1. Adjacent centers force disjoint independent neighborhoods

Import the established degree counts (17,24,13), the all-sink property of
V8, and the necessary identities in `forest_reduction.md`. A sink has
every vertex within distance two. Girth at least five makes each such
short path unique. Write c(v)=|N(v) intersect V8| for low vertices and
h(t)=degree_H(t) for high vertices, where H=G[V8]. A low vertex here has
degree six or seven.

Label the components of H as

    {0}, {1}, {2}, {3}, {4}, (5,6,7,8), (9,10), (11,12).

Put x=5, a=6, b=7, y=8. The centers a,b are adjacent. Each high t has
3+h(t) degree-six neighbors and 5-2h(t) degree-seven neighbors. Thus the
low neighborhoods I_a and I_b of the centers each contain five six-vertices
and one seven-vertex. They are disjoint by triangle-freeness. Each is
independent by triangle-freeness, and an edge between them would complete
a quadrilateral through ab. Consequently I=I_a union I_b is an independent
set of size twelve. Neither endpoint x nor y can have a neighbor in I:
such an edge would make a triangle or quadrilateral along the P4.

The high-pair identity at a high t is

    sum_{low v adjacent t} (c(v)-1)
      = 12 - sum_{u adjacent_H t} h(u).                    (1)

At either center, the H-neighbors have high degrees 1 and 2. Equation (1)
therefore says that the six members of I_t have c values summing to 15.
Each has c>=1 because it is adjacent to t. This individual-neighborhood
condition drives the case reduction.

## 2. Complete histogram and center-role cover

There are m=5 high edges and k=2 high vertices of high degree two. The
necessary balances are

    sum_V6 c = 49,                  sum_V7 c = 45,
    sum_V6 (c-3)(c-4)/2 + sum_V7 (c-1)(c-2)/2 = 5.        (2)

The nonnegative integer histograms satisfying (2), the degree-class
orders, and 0<=c<=degree are exactly the following fifteen. The notation
c:n denotes n vertices with high-neighbor count c. Indices agree with
the deterministic enumeration in `forest_profiles.py`.

| Profile | Degree six | Degree seven | Center cases |
|---|---|---|---:|
| 0 | 2:2, 3:15 | 1:5, 2:18, 4:1 | 1 |
| 1 | 2:2, 3:15 | 1:6, 2:15, 3:3 | 1 |
| 2 | 2:2, 3:15 | 0:1, 1:3, 2:18, 3:2 | 1 |
| 3 | 2:2, 3:15 | 0:2, 2:21, 3:1 | 0 |
| 4 | 2:3, 3:13, 4:1 | 1:5, 2:17, 3:2 | 3 |
| 5 | 2:3, 3:13, 4:1 | 0:1, 1:2, 2:20, 3:1 | 3 |
| 6 | 2:4, 3:11, 4:2 | 1:4, 2:19, 3:1 | 9 |
| 7 | 2:4, 3:11, 4:2 | 0:1, 1:1, 2:22 | 4 |
| 8 | 2:4, 3:12, 5:1 | 1:3, 2:21 | 4 |
| 9 | 2:5, 3:9, 4:3 | 1:3, 2:21 | 12 |
| 10 | 1:1, 3:16 | 1:5, 2:17, 3:2 | 0 |
| 11 | 1:1, 3:16 | 0:1, 1:2, 2:20, 3:1 | 0 |
| 12 | 1:1, 2:1, 3:14, 4:1 | 1:4, 2:19, 3:1 | 2 |
| 13 | 1:1, 2:1, 3:14, 4:1 | 0:1, 1:1, 2:22 | 1 |
| 14 | 1:1, 2:2, 3:12, 4:2 | 1:3, 2:21 | 9 |

A center signature consists of the c histogram of its five six-neighbors
and the c value of its one seven-neighbor. The sum of these six values
is 15. Two signatures are allowed only when they can use disjoint
vertices from the global histograms. Reversing the P4 allows the two
signatures to be ordered, with equality allowed. This gives **50** center
cases, as counted in the table.

The three zero-case profiles already contradict these necessary facts.
In profile 3 the seven-neighbor has c>=2, so a center needs at least two
of the c=2 six-vertices. Both centers cannot use the only two such vertices
disjointly. In profiles 10 and 11, five c=3 six-neighbors already sum to
15. Thus each center needs the sole c=1 six-vertex, again contradicting
disjointness.

For each of the other profiles, assign consecutive labels to the
six-vertices of each c class in the roles only-at-a, only-at-b, neither.
Within each seven-vertex c class, assign the distinguished center
neighbors first, then the other vertices. `p4_cases.py` constructs these
groups. Every graph admits this labeling by permutations within its
degree/c classes; no other high-neighbor sets are fixed.

`verify_p4.py` checks all fifteen histograms using a separate recursion
over all c values. It independently enumerates each center signature by
choosing concrete five-element subsets of the seventeen six-vertices,
then projects to histograms and checks disjoint capacities. It reproduces
all 50 cases and audits the sizes, c sums and allowed row permutations
of each assigned role group.

## 3. A complete endpoint refinement for profile 1

Of the 50 center cases, 49 have direct checked refutations. For profile 1,
replace its sole center case by the following three endpoint cases.

The five six-neighbors of a center have c=2 or 3. If q of them have c=2,
equation (1) forces its seven-neighbor to have c=q. Therefore q>=1.
The centers use disjoint six-neighbors and only two c=2 six-vertices
exist. Each center consequently uses one c=2 and four c=3 six-vertices,
and its seven-neighbor has c=1. Outside I remain exactly seven
six-vertices, all with c=3.

Each endpoint has four six-neighbors and three seven-neighbors, all
outside I. The two four-element subsets of the seven remaining
six-vertices intersect. They intersect in exactly one vertex, since
two common neighbors would make a quadrilateral. They use all seven
vertices, in roles

    1 common, 3 only at x, 3 only at y.

Their seven-neighborhoods are disjoint, since their unique common
neighbor is already a six-vertex. At an endpoint, the right side of
(1) is 12-h(center)=10. Its four six-neighbors each contribute two.
Thus its three seven-neighbors have c values summing to five.
Their possible sorted c triples are precisely

    A=(1,1,3),                 B=(1,2,2).

There are four remaining c=1 seven-vertices, fifteen with c=2 and three
with c=3. All three unordered pairs AA, AB, BB fit these capacities.
The center signatures are identical, so reversing the P4 permits this
ordering of endpoint types without losing a graph.

In the normalized center case, vertices 13,14 are the c=2 six-vertices;
15..18 and 19..22 are the centers' c=3 six-neighbors. Label the common
endpoint six-neighbor 23, the three x-only six-neighbors 24..26, and the
three y-only six-neighbors 27..29. The centers' c=1 seven-neighbors are
30,31. Within each remaining seven-vertex c class, label the x-neighbors
first, then the y-neighbors, then those at neither endpoint.

This yields three complete incidence cases. The verifier independently
enumerates the c triples and capacity-feasible pairs and checks the
assigned endpoint roles. All three cases have checked refutations.
The final cover thus consists of **49+3=52** SAT cases, together with
the three empty histograms from the center argument.

## 4. Full-incidence encoding and compatible symmetry

`p4_sat.py` starts with `forest_sat.py` and disables its general symmetry
constraints. All edges with a low endpoint are variable. The formula
enforces the fixed high forest, degrees, c counts, high-neighbor degree
classes, at most one edge or two-path for every vertex pair, and existence
of a short path for every pair containing a high vertex. These are exactly
the required girth and sink conditions. The redundant individual
high-pair equations use the preceding cardinality encoding, with negative
coefficients represented by complemented literals and the corresponding
constant shift.

The new clauses force the selected center incidences, the independence
of I, and, in profile 1 only, the selected endpoint incidences. No
weighted-gap budget, characteristic-polynomial constraint or prescribed
bipartite grid is used in the final 52 refutations.

Rows of the low-by-high incidence matrix are compared only within equal
degree/c/assigned-role groups. In profile 1 the endpoint roles replace
the coarser center-only row groups. High-column symmetries permute the
five isolates, reverse either P2, and exchange the two P2 components.
All four P4 vertices are fixed individually by these remaining column
operations. The reversal used to order case signatures is not imposed
again as a column comparison.

These comparisons are compatible. Choose a least low-by-high incidence
matrix in row-major order over the valid remaining row and column
permutations. Any violated row, isolated-column, P2-orientation or
P2-block comparison would give a smaller matrix under its corresponding
valid permutation. Hence every realization has at least one labeling
satisfying all comparisons. The existing checked `lex_chain` routine
implements them.

As a positive control of the adjacent-center mechanism, `verify_p4.py`
checks every one of the 12,600 oriented induced P4s in the
Hoffman-Singleton graph. Each has disjoint independent center neighborhoods
outside its four path vertices, and its endpoints avoid that union.
For every vertex v outside the path and these neighborhoods, it also
checks the individual partition equations

    |N(v) intersect I_a| + [v adjacent x] = 1,
    |N(v) intersect I_b| + [v adjacent y] = 1.

All 907,200 such equalities pass. This control concerns the general
girth-five, diameter-two neighborhood argument; the 50-vertex control
does not satisfy the target 54-vertex degree profile. It supplements
the written proof and does not replace the graph-to-formula argument.

## 5. Reproduction and trust boundary

From this directory, run

```sh
python3 verify_p4.py
python3 reproduce_p4.py --work /tmp/order54-p4 --checker /path/to/drat-trim
```

The first command uses only the standard library. Its output includes
`complete_histograms: 15`, center case counts
`[1,1,1,0,3,3,9,4,4,12,0,0,2,1,9]`, `endpoint_role_cases: 3`, and
`sat_cases: 52`. The full driver ends with `verified_unsat: 52` and
`excluded_forest: P4+2P2+5K1`.

The recorded environment is CPython 3.11.2, python-sat 1.8.dev24 and
six 1.17.0 from `requirements-sat.txt`, with Glucose g4. Build DRAT-trim
from commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` using GCC 12.2.0,
C99 `-O2`. Default limits are 100,000 solver conflicts and 300 seconds
per checker call. Every UNSAT trace must pass a separate DRAT-trim
process. `p4_expected.json` records all case identifiers, formula sizes,
and CNF/proof SHA-256 hashes. The driver fails on SAT, UNKNOWN, hash
mismatch, or a failed check.

The fresh sequential reproduction took 611.9 seconds and
matched every formula and proof hash. Its main Python process peaked at
339,924 KiB RSS; the proof checker runs separately. Formulas total
496,384,935 bytes and traces 207,253,189 bytes.
Fresh-run resources are recorded in `p4_run.json`. Generated formulas,
proof traces and verbose logs remain in an external work directory;
allow 1 GB temporary disk. The compact source and manifest regenerate
the omitted certificates.

Trust remains in the imported order-53 bound and earlier degree/all-sink
results, the written histogram and graph-to-case arguments, the generator
and cardinality translation, Python/compiler runtime, and the separate
proof checker. The solver's bare UNSAT verdict is insufficient. The
fresh reproduction and controls were performed within this research
campaign; this new theorem has not yet received external review or
proof-assistant formalization. Literature priority is not established.
