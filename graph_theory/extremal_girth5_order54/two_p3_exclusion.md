# Excluding the two-P3 six-edge high forest

**Theorem.** No finite simple graph G of order 54, size 187 and girth at
least five, with thirteen degree-eight vertices, has

    G[V8] = 2P3 + 2P2 + 3K1.

Here P_j is a path on j vertices. Combined with the preceding
[seven-forest reduction](forest_reduction.md), every such G has one of
these **six** high induced forests:

| Case | High induced forest |
|---|---|
| 5_0 | 5P2 + 3K1 |
| 5_1 | P3 + 3P2 + 4K1 |
| 5_2a | P4 + 2P2 + 5K1 |
| 5_2b | 2P3 + P2 + 5K1 |
| 6_0 | 6P2 + K1 |
| 6_1 | P3 + 4P2 + 2K1 |

These six forests were unresolved at this stage. Subsequent
[P4 work](p4_exclusion.md) excludes `5_2a` completely, leaving five.
The unrestricted
working bounds 185 <= ex(54,{C3,C4}) <= 187 are unchanged. This theorem
covers every remaining incidence in the excluded forest, without fixing
a favorable local-type histogram or type-to-type edge count.

## 1. Complete high-neighbor profiles

Import the established degree counts (17,24,13), all-sink property of V8,
and maximum high degree two. A sink means that every vertex is at distance
at most two from it. Girth at least five makes that short path unique.
Fix H=2P3+2P2+3K1 on the thirteen high vertices. Label its components

    {0}, {1}, {2}, (3,4,5), (6,7,8), (9,10), (11,12).

A six-vertex means a vertex of degree six, and likewise for seven-vertices.
The two path centers are a=4 and b=7. Put c(v)=|N(v) intersect V8| and
h(t)=degree_H(t). Every high t has 3+h(t) degree-six neighbors and
5-2h(t) degree-seven neighbors. A center therefore has five six-neighbors
and just one seven-neighbor.

For m=6 and k=2, the high-pair deficit from the preceding reduction is

    sum_V6 c = 51,                 sum_V7 c = 41,
    sum_V6 (c-3)(c-4)/2 + sum_V7 (c-1)(c-2)/2 = 2.

The nonnegative integer c histograms satisfying these balances are exactly
the following six. The notation c:n means n vertices have that c value.
The public ordering is the deterministic ordering in `forest_profiles.py`.

| Profile | Degree six | Degree seven | Final SAT cases |
|---|---|---|---:|
| 0 | 3:17 | 1:9, 2:13, 3:2 | 1 |
| 1 | 3:17 | 0:1, 1:6, 2:16, 3:1 | 1 |
| 2 | 3:17 | 0:2, 1:3, 2:19 | 1 |
| 3 | 2:1, 3:15, 4:1 | 1:8, 2:15, 3:1 | 8 |
| 4 | 2:1, 3:15, 4:1 | 0:1, 1:5, 2:18 | 1 |
| 5 | 2:2, 3:13, 4:2 | 1:7, 2:17 | 1 |

A separate recursive enumeration over all c values verifies this list
entry by entry. Profiles 1,2,4,5 are refuted directly by the existing
complete fixed-forest incidence encoding. Profiles 0 and 3 use the
following forced center roles. Those roles specify incidences of actual
vertices, rather than only aggregate totals.

## 2. The common center neighbor in profile 0

Every six-vertex has c=3. At a center t, its five six-neighbors each account
for two further high vertices. Together with the two H-neighbors, these
already account for all twelve other high vertices. Therefore its unique
seven-neighbor has c=1.

The two centers are not adjacent and have no H-common neighbor. Their
unique short path must pass through a low vertex. A common seven-neighbor
would have c>=2, which has just been excluded. They therefore have exactly
one common six-neighbor, with c=3. Their other six-neighbors form disjoint
sets of four each. The seventeen six-vertices consequently have four
roles of sizes

    1 common, 4 only at a, 4 only at b, 8 at neither.

The two unique seven-neighbors have c=1 and are distinct. We may label
the common six-vertex 13, the two sets of four as 14..17 and 18..21,
and the other six-vertices 22..29. The distinguished seven-vertices are
30 and 31. All other edges remain variable. This normalization covers
profile 0 with a single formula; it does not select the third high
neighbor of vertex 13 or any other full high-neighbor set.

## 3. Exactly eight center cases in profile 3

There is one six-vertex D with c=2, one six-vertex Q with c=4, and fifteen
ordinary six-vertices with c=3. There is one seven-vertex T with c=3;
the other seven-vertices have c=1 or c=2. Also use D,Q,T to denote the
corresponding high-neighbor sets, of sizes 2,4,3.

Each of these sets is independent in the square of H: two members cannot
be adjacent in H or have an H-common neighbor. Any two of the sets
intersect in at most one point, by C4-freeness.

Write s(t)=sum_{u adjacent_H t} h(u). Let a1(t) count the seven-neighbors
of high t which have c=1. Counting the unique high pairs through t gives

    a1(t) = s(t)-1 + [t in Q] + [t in T] - [t in D].       (1)

To see this directly, the six-neighbors contribute
2(3+h(t))+[t in Q]-[t in D] other high vertices. The seven-neighbors
contribute (5-2h(t))-a1(t)+[t in T]. Their sum equals 12-s(t), giving (1).

For a center, s(t)=2 and there is only one seven-neighbor. If t belonged
to T, that neighbor would be T and a1(t)=0. But (1) would be at least
one. Thus T avoids both centers. Writing d=[t in D] and q=[t in Q],
(1) now gives a1(t)=1+q-d. Hence q<=d, and the unique seven-neighbor
has c=1 when d=q, or c=2 when d=1 and q=0.

Q cannot contain both centers, since D would then also contain both,
contradicting |D intersect Q|<=1. Thus the complete ordered center masks
are

    (D_a,D_b) in {00,01,10,11},
    (Q_a,Q_b) in {00,01,10},       Q_i <= D_i.

There are exactly eight such pairs, with respectively 1,2,2,3 choices
for the four D masks. They form disjoint exhaustive cases in this labeling.

Again the centers have a unique common low neighbor. If it were a
seven-vertex, both of their unique seven-neighbors would have c=2.
This forces D to contain both centers and Q neither. But then D would
supply a second short path, impossible. The common neighbor is a
six-vertex. It cannot be Q, which meets at most one center. It is D
exactly for the mask D=11; otherwise it is an ordinary c=3 six-vertex.
The distinguished seven-neighbors are always distinct.

Label D as 13 and Q as 29. The ordinary vertices are 14..28. If the
common vertex is ordinary, label it 14. For each center i, its number
of ordinary six-neighbors is 5-d_i-q_i. After removing the common vertex
when ordinary, these two sets are disjoint and may be labeled in
consecutive groups, followed by the remaining ordinary vertices.
Within each seven-vertex c class, label the distinguished center
neighbors first. These choices yield one complete incidence formula
for each of the eight masks.

## 4. Encoding, normalization and exact checks

`two_p3_cases.py` constructs the explicit role groups and the complete
13-case list. `two_p3_sat.py` reuses `forest_sat.py` for all graph edges,
exact degrees and c counts, high-neighbor degree classes, unique short
paths, and high-sink requirements. It adds the forced center incidences
only in profiles 0 and 3. No weighted-gap budget or spectral restriction
is used. Cardinality coefficients and complemented negative literals
have the same meaning as in the preceding audited encoding.

For the two normalized profiles, the old general symmetry constraints
are disabled. Row comparisons apply only within the still indistinguishable
role groups. High-column comparisons sort the three isolates, reverse
each path, and exchange the two P2 blocks. These operations fix both
centers individually and preserve every assigned role. The two P3
components are not exchanged by this symmetry normalization.

The comparisons are jointly sound: choose the least low-by-high
incidence matrix in row-major order over these valid remaining row
and column relabelings. Any violated row, path-orientation or equal-block
comparison gives a smaller matrix. Thus some labeling of every graph
satisfies them all. The same previously checked `lex_chain` implementation
is used. There is no simultaneous fixing of a high motif with incompatible
column ordering.

`verify_two_p3.py` separately enumerates center-incidence states directly
from the two high-pair equations, the five/single neighbor counts, and
uniqueness of the path between centers. It does not import the claimed
eight-case classification into that enumeration. The resulting states
match all eight proposed masks and force an ordinary or D common neighbor
as above. It also verifies each explicit role group's cardinalities,
degree/c classes, center incidences and compatibility with row permutations.
The complete six-profile list is checked by the independent histogram
recursion. These checks use only exact standard-library arithmetic and
explicit failures, rather than removable assertions, for the new checks.
The written argument supplies the general normalization proof.

## 5. Reproduction and trust

All thirteen formulas are UNSAT and all thirteen emitted traces are
accepted by separate DRAT-trim processes. `two_p3_expected.json` contains
every case, formula size, and CNF/proof SHA-256. The final source is
reproduced from an empty external work directory; the driver fails on
SAT, UNKNOWN, a mismatched formula or proof hash, or a failed proof check.

From this directory:

```sh
python3 verify_two_p3.py
python3 reproduce_two_p3.py --work /tmp/order54-two-p3 --checker /path/to/drat-trim
```

Expected exact coverage output includes `complete_profiles: 6`,
`profile3_center_patterns: 8`, `normalized_role_cases: 9`, and
`total_sat_cases: 13`. The full driver ends with `verified_unsat: 13`
and `excluded_forest: 2P3+2P2+3K1`.

Use CPython 3.11.2, python-sat 1.8.dev24 and six 1.17.0 from the existing
`requirements-sat.txt`; the solver is Glucose g4. DRAT-trim is built from
commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` with GCC 12.2.0,
C99 `-O2`. Default limits are 100,000 solver conflicts and 300 seconds
per proof-checker call. Generated formulas, proof traces and verbose logs
stay outside the repository. Compact fresh-run resources and hashes are
recorded in `two_p3_run.json`.

The fresh sequential run took 784.9 seconds and reproduced
all formula and proof hashes. The main Python process peaked at
326,740 KiB RSS (about 319.1 MiB); the proof checker
runs separately. The formulas total 124,618,700 bytes and the
traces 148,085,526 bytes; allow about 350 MB temporary disk.

This is an exact computer-assisted whole-subclass exclusion with a
written combinatorial reduction. Trust remains in the imported order-53
bound and prior degree/all-sink results, the stated graph-to-formula
argument, the generator and cardinality translation, Python/compiler
runtime, and the separate proof checker. A solver's bare UNSAT verdict
is not accepted. New normalization controls and fresh reproduction are
not an external peer review or proof-assistant formalization. This new
theorem has not yet received external review, and literature priority
is not established.
