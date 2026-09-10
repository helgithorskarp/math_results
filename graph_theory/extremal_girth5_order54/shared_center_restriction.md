# A shared degree-six neighbor in the five-edge two-P3 forest

**Theorem.** Let G be a finite simple graph on 54 vertices with 187 edges
and girth at least five. Suppose its thirteen degree-eight vertices induce

    H = 2P3 + P2 + 5K1.

The two P3 centers have a unique common neighbor r. This vertex has
**degree six and exactly two or three degree-eight neighbors**.
More precisely, G belongs to one of the 33 joint center-incidence states
listed below, across four possible high-neighbor-count histograms.

This is a necessary classification across the whole specified forest.
It does not prove that the forest is unrealizable, or that any remaining
state is realizable. The [five-forest classification](p4_exclusion.md)
and working interval **185 <= ex(54,{C3,C4}) <= 187** remain unchanged.

## 1. The complete joint-center cover

Import the preceding degree counts (17,24,13), all-sink property of the
degree-eight vertices, and identities in [forest_reduction.md](forest_reduction.md).
A sink has every vertex within distance two. Girth at least five makes
every such short path unique. Label the high components

    {0}, {1}, {2}, {3}, {4}, (5,6,7), (8,9,10), (11,12).

The centers are a=6 and b=9. They are nonadjacent and have no high common
neighbor. Their unique short path therefore passes through a low vertex r.
Here low means degree six or seven. Put c(v)=|N(v) intersect V8| and
h(t)=degree_H(t). Each center has five six-neighbors and one seven-neighbor.
Its six low neighbors have c sum sixteen, since

    sum_{low v adjacent t}(c(v)-1)
       = 12 - sum_{u adjacent_H t} h(u) = 10.             (1)

Write I_a and I_b for these low neighborhoods. Their intersection is
exactly {r}; each is independent. All their members have c>=1 and c(r)>=2.
We initially allow r to have either degree six or degree seven.

For m=5 and k=2, the complete c histograms satisfy

    sum_V6 c=49,                  sum_V7 c=45,
    sum_V6 (c-3)(c-4)/2 + sum_V7 (c-1)(c-2)/2=5.         (2)

There are fifteen such histograms, in the existing deterministic order
of `forest_profiles.py`; the full list is displayed in
[p4_exclusion.md](p4_exclusion.md). The histogram identities depend on
m,k and apply to the present forest as well.

A center signature S comprises the c histogram of its five six-neighbors
and the c value of its one seven-neighbor. Its six values sum to sixteen.
A joint state is (d(r),c(r),S,T), ordered with S<=T by exchanging the two
P3 components. If d(r)=6, the two six-neighborhoods share one vertex of
class c(r), and the seven-neighbors are distinct. If d(r)=7, the two
seven-neighbors are the same vertex and the six-neighborhoods are disjoint.
Every joint state must fit the global multiplicities in (2).

The complete joint-state counts for profiles 0 through 14 are

    5,7,7,4,23,22,48,23,13,40,2,2,14,7,34,

total **251**. `shared_center_cases.py` constructs all these states and
labels vertices within each degree/c class as common, only at a, only at b,
or at neither center. The shared vertex and distinguished seven-neighbors
are individually fixed. Every graph has such a labeling.

## 2. Partitioning the high vertices through the common neighbor

Only three joint states permitting d(r)=7 or c(r)>=4 survive the direct
incidence refutations used below. They all have profile 4:

    V6: 2:3, 3:13, 4:1;          V7: 1:5, 2:17, 3:2.

The notation c:n gives the number of vertices with that c value.
Writing D,N,Q for six-neighbors of c=2,3,4 respectively, the three states are

| Joint index | d(r),c(r) | First center | Second center | Star cases |
|---|---|---|---|---:|
| 6 | 6,4 | D+3N+Q; seven c=1 | D+3N+Q; seven c=1 | 8 |
| 9 | 6,4 | D+3N+Q; seven c=1 | 2D+2N+Q; seven c=2 | 5 |
| 14 | 7,2 | D+4N; seven c=2 | D+4N; same seven-vertex | 11 |

For any joint state, let d=d(r) and c=c(r). Besides a,b, the high neighbors
of r avoid all four P3 leaves, since an edge to such a leaf creates a
triangle. The only other possibilities are the five isolates and the
two P2 endpoints. At most one P2 endpoint can be a neighbor of r.
Let e in {0,1} record whether it has one; then r has

    q=c-2-e

isolated high neighbors. Permute the isolates and, if needed, reverse P2
to label these neighbors 0..q-1 and endpoint 11.

Let L=N(r) minus V8, so |L|=d-c. Every vertex in L lies outside I_a union I_b:
an edge from r to another member of either center neighborhood makes a
triangle. Also, the high-neighbor sets of vertices of L partition exactly
the high vertices not already reached from r directly or through one of
its high neighbors. They cannot overlap, and cannot contain an already
reached high vertex, by uniqueness of short paths from a high vertex to r.
Every still-unreached high vertex must occur in one of these sets, by the
all-sink property. Thus they partition

    R = {q,...,4} union {11,12},     if e=0,
    R = {q,...,4},                  if e=1.               (3)

In particular their c values sum to 9-c-e. A block cannot contain both
11 and 12, since those vertices are adjacent. Empty blocks are allowed
when a chosen low neighbor has c=0.

This gives a small complete star normalization. Choose the degree/c types
of the d-c vertices in L, subject to the available counts outside the
center neighborhoods and the sum 9-c-e. When e=0, mark two distinct
positive-size blocks as containing 11 and 12. Their degree/c types may be
ordered by reversing P2. Order the unmarked blocks by degree/c type.
Assign consecutive unused isolate labels to each block, in numbers equal
to its c value minus its marker. When e=1 there are no marked blocks.
Within each degree/c class, choose the first available low labels for
these blocks. This normalization covers every partition (3), including
repeated types and empty blocks.

`shared_star_cases.py` constructs these stars and their explicit incidences.
For the three required joint states it gives 8+5+11=**24** cases. All have
checked refutations. This closes every state with an impermissible
common-neighbor type in the theorem.

## 3. The resulting 33-state classification

Nine entire histograms are refuted directly: 0,3,5,7,8,11,12,13,14.
For the six other histograms, 91 joint-center formulas are refuted directly.
The 24 star formulas replace three further joint states. The total is

    9 whole-profile + 91 joint-center + 24 star = 124 refutations.

All remaining joint states have d(r)=6 and c(r) in {2,3}. They are exactly
the following states not excluded by this public reduction. Indices refer
to `cases(profile)` in `shared_center_cases.py`; these are complete
incidence specifications, not full graph realizations.

| Profile | Degree-six c histogram | Degree-seven c histogram | Remaining joint indices |
|---|---|---|---|
| 1 | 2:2, 3:15 | 1:6, 2:15, 3:3 | 0,1,2,3,4,6 |
| 2 | 2:2, 3:15 | 0:1, 1:3, 2:18, 3:2 | 0,1,3,4 |
| 4 | 2:3, 3:13, 4:1 | 1:5, 2:17, 3:2 | 0,1,2,3,4,7,8,10,11,12,13,15,16,18,19,20,21 |
| 6 | 2:4, 3:11, 4:2 | 1:4, 2:19, 3:1 | 10,13,14,27,28,39 |

The row counts are 6,4,17,6, totaling 33. In particular every six-vertex
has between two and four high neighbors; every seven-vertex has at most
three. The stronger statement about r distinguishes an individual vertex.
No assertion of realizability or minimality of this residual cover is made.
Partial exploratory refutations outside the 124-case proof are not premises.

## 4. Incidence encoding and sound symmetry

The base formulas use `forest_sat.py`: every possible edge with a low
endpoint remains available; exact degrees, c counts, high-neighbor degree
classes, unique short paths and high-sink conditions are imposed. The
joint formulas in `shared_center_sat.py` disable general base symmetry
and fix only the chosen center incidences and independent neighborhoods.
Rows are compared only within the remaining degree/c/center-role groups.
Columns may permute the isolates, interchange the two leaves of either
P3, and reverse P2. The centers are fixed individually after their
signature ordering has selected the case.

The star formulas in `shared_star_sat.py` additionally fix all neighbors
of r and all high-neighbor sets of the vertices in L. These selected low
vertices are removed from the residual row groups. Isolate columns may
be permuted only within the q neighbors of r or within one block of (3).
The P3 leaf interchanges remain valid; no P2 reversal is imposed after
fixing its marked blocks.

These comparisons are jointly sound. Take the least low-by-high incidence
matrix in row-major order over precisely the remaining valid row and column
permutations. A violated comparison would produce a smaller matrix under
its permitted permutation. Thus at least one labeling of every realization
satisfies all comparisons. The previously checked `lex_chain` routine is
reused. No full unrelated motif or incompatible column order is imposed.

The final 124 refutations use neither the optional defect-budget cuts,
spectral conditions, an extra isolated-high normalization, nor a separate
unit-propagation preprocessing experiment. Those exploratory routes are
not inputs to the theorem.

## 5. Independent controls, reproduction and trust

`verify_shared_center.py` checks the full fifteen-histogram list by a
separate recursion. It constructs joint signatures by choosing concrete
five-element subsets for the first center, then concrete disjoint or
one-point-overlapping subsets for the second. Its entry-level output
matches all 251 states. It audits every assigned center role.

For the three refined states, a separate labeled-set-partition recursion
constructs all possible partitions of R, assigns degrees to blocks, allows
empty blocks, and tests capacities directly. This does not import the
production enumeration of block-type multiplicities. Its normalized
results match all 24 stars, and the explicit star labels and remaining
row/column classes are checked. The proof-plan checker verifies that every
joint state is refuted by the indicated complete case or belongs to the
stated 33-state residual cover, and checks the theorem for each residual state.

As a positive control of the common-star mechanism, the verifier examines
all 1,050 nonadjacent center pairs in the Hoffman-Singleton graph. For each,
it chooses a deterministic thirteen-vertex high subset containing the
centers and excluding their common neighbor. The general partition identity
passes in every case, with 6,155 high-partition entries checked. These
subsets need not induce the target forest, and the graph has order 50;
the control tests the general short-path argument, not target realizability.

From this directory:

```sh
python3 verify_shared_center.py
python3 reproduce_shared_center.py --work /tmp/order54-shared-center --checker /path/to/drat-trim --jobs 4
```

The first command requires only Python's standard library. Expected fields
include `histograms: 15`, `total_cases: 251`, `total_stars: 24`,
`total_refutations: 124`, and `residual_center_states: 33`. The full driver
ends with `verified_unsat: 124` and `residual_center_states: 33`.

Use CPython 3.11.2, python-sat 1.8.dev24 and six 1.17.0 from
`requirements-sat.txt`, Glucose g4, and DRAT-trim commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985` built with GCC 12.2.0,
C99 `-O2`. Default limits are 100,000 conflicts per solver and 300 seconds
per proof check. The driver fails on SAT, UNKNOWN, mismatched CNF/proof
hashes or failed checking. `shared_center_expected.json` identifies every
case and its sizes and SHA-256 hashes. `shared_center_run.json` records the
fresh four-worker reproduction. Generated formulas, traces and logs remain
outside Git; allow 3 GB temporary disk.

The fresh four-worker run took 439.272 seconds. The largest
Python worker reached 280,088 KiB peak RSS; this is not
aggregate concurrent memory and excludes the separate checker processes.
It regenerated 1,180,172,555 formula bytes and 538,460,010
proof bytes, matching all initial hashes.

This is an exact computer-assisted necessary classification. Trust remains
in the imported order-53 bound and preceding degree/all-sink results, the
written graph-to-case and symmetry arguments, generator/cardinality library,
runtime/compiler and separate DRAT checker. Bare solver verdicts are not
accepted. The controls and fresh reproduction are author-run checks, not
external peer review or proof-assistant formalization. Literature priority
is not established.
