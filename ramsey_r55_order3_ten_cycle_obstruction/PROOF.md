# Ten moving triangles must split four versus six in internal color

**Theorem.** Let a 43-vertex graph have neither a clique nor an independent
set of order five. If it has an automorphism of cycle type `1^13 3^10`,
then four moving triangles have one internal color and six have the other.
After complementation, only `r=4` red moving triangles remains possible.
The cases `r=0,1,2,3,5` are excluded by the checked formulas below.

This does **not** exclude the whole ten-cycle type. The current minimum
of ten moving 3-cycles is unchanged; types with eleven through fourteen
moving cycles also remain unresolved. There is no 43-vertex construction
or Ramsey lower-bound improvement here.

## Local arithmetic

Color edges red and nonedges blue. The established theorem `R(4,5)=25`
implies that every color-degree is between 18 and 24. A color neighborhood
has neither a same-color four-clique nor an opposite-color five-clique;
applying the upper bound to both colors gives the lower bound as well.

Write the moving vertices as `3i+s`, for `0<=i<10` and `s in Z/3Z`.
The permutation increments `s` and fixes vertices 30 through 42. Every
moving triple is a monochromatic triangle. For triangle `C_i`, let `c_i`
be its color, `a_i` its number of fixed neighbors in that color, `w_ij`
its number of neighbors per vertex in another triangle in that color,
and `m_i` the number of complete blocks `w_ij=3`.

The common color-`c_i` neighborhood of `C_i` contains no edge of that
color: an edge would extend the triangle to a five-clique. Five vertices
there would consequently form an opposite-color five-clique. Therefore,

```text
a_i + 3m_i <= 4,
2 + a_i + sum_(j != i) w_ij >= 18.                    (1)
```

For a permutation with `k` moving triangles, put

```text
delta(w) = 2-w+3*[w=3],       delta(0,1,2,3) = (2,1,0,2),
D_i = sum_(j != i) delta(w_ij).
```

The identity `sum w_ij = 2(k-1)+3m_i-D_i` and (1) give the useful
general inequality `D_i<=2k-14`. Thus the budget at ten cycles is SIX.
The exact local fixed-count interval in the current stratum is

```text
max(0,D_i-2-3m_i) <= a_i <= 4-3m_i.                  (2)
```

The own-color degree equals `20+a_i+3m_i-D_i`; (2) places it between
18 and 24. Since the available fixed count is 13, its external cap is
automatic in (2). An admissible fixed count exists exactly when `D_i<=6`
and `m_i<=1`. Neither condition may be dropped.

Exhausting all `4^9=262144` weight vectors and all 14 fixed counts gives
10,679 local arithmetic profiles. There are 5,459 with `m_i=0` and 5,220
with `m_i=1`. These are necessary profiles, not graph realizations.
The deficit budget alone falsely admits another 1,380 weight vectors:
1,296 with two complete blocks and 84 with three. For two blocks, choose
their positions in 36 ways; the remaining seven weights have deficit
at most two, in `1+7+7+21=36` ways. For three blocks their positions can
be chosen in 84 ways and all remaining weights must be two.

## Complete normalization

Global color reversal makes the number `r` of red moving triangles at
most five. Permuting moving triangles puts the red ones first, yielding
six cases `r=0,1,2,3,4,5`. The balanced case is included. For `i<j`, the
edge from `3i+s` to `3j+t` is represented by the red bit `b_ij,t-s`.

Independent choices of origin in triangles 1 through 9 rotate their
three-bit anchor words into `000,100,110,111`. Hence each anchor word
is componentwise nonincreasing. Every three-bit binary word admits such
a cyclic rotation; constant words cause no exception.

As an additional normalization, within each internal color permute the
nonanchor triangles by increasing
anchor-word weight. The four normalized words form the componentwise
chain `000 <= 100 <= 110 <= 111`. Thus for adjacent nonanchor triangles
`j,j+1` with the same internal color, we may require

```text
b_0j,s <= b_0(j+1),s     for s=0,1,2.                (3)
```

This only permutes whole triangles with equal internal color and fixes
the anchor. It preserves phase-normalized words and commutes with the
order-three permutation. The red-first convention is unchanged. No
uniqueness is claimed, and equal weights remain allowed.

Finally permute the thirteen fixed vertices so that their ten-bit red
incidence signatures are lexicographically nondecreasing. This does not
affect the moving normalization. Equal signatures are allowed. Performing
these operations in the stated order proves coverage: every hypothetical
graph has a representative satisfying all normalizations. The explicit
audit tests all 1,024 internal-color profiles with invariant edge data,
checks the induced vertex permutation on all 903 pairs, and verifies
commutation with the order-three action.

The six solver formulas use the internal-color, phase and fixed-signature
normalizations. They do **not** impose the extra ordering (3). Its purpose
is to describe a smaller, reproducible frontier for the remaining case.
After (3), the red anchor in the surviving `r=4` case has three red and six
blue nonanchor triangles. A red-red block cannot have red weight three,
since the two triangles would contain a red five-clique. Thus its weights
are an increasing triple in `{0,1,2}` and an increasing sextuple in
`{0,1,2,3}`, with at most one weight three and deficit at most six.
Exactly **98** such vectors exist. Two enumerations agree entry by entry:
one uses combinations with replacement; the other canonicalizes all
labeled nine-weight vectors. These are necessary anchor profiles, not
98 graph realizations or 98 excluded cases. No cube search is claimed.
The same enumeration gives 25,56,82,98,105 vectors for `r=1,...,5`.

## Complete formula

The permutation has 353 unordered-pair orbits. Ten are constant internal
triangles; the other 343 supply primary red variables in this order:

1. 135 moving-cross bits, ordered by triangle pair and difference;
2. 78 fixed-fixed bits, ordered by vertex pair;
3. 130 fixed-moving bits, ordered by fixed vertex and moving triangle.

Every one of the `binom(43,5)=962598` five-subsets supplies the two clauses
forbidding it from being monochromatic. Constants are substituted;
duplicate literals and clauses are removed. No graph catalog or class of
fixed graphs is omitted.

For each triangle pair and each internal color appearing at an endpoint,
three auxiliary gates encode `u=[delta>=1]`, `v=[delta>=2]`, `z=[w=3]`.
For all eight input valuations, the three clauses consist of the input
literals falsified by that valuation followed by the correct gate literal.
They therefore force exactly those gate values. Same-color endpoints
share the gates; different-color endpoints use separate gates.

The eighteen `u,v` tokens at each moving triangle sum to its deficit.
All negative seven-token clauses impose deficit at most six. There are
`binom(18,7)=31824` such clauses per triangle before global deduplication.
Two counters at each moving triangle impose (1): at most four among its
13 fixed own-color bits and three copies of each of nine complete-block
gates; and at most 24 negations of its 13 fixed own-color bits and 27
moving-cross bits. Each has forty input occurrences. The latter counter
gives outside own-color degree at least sixteen; adding the two internal
neighbors gives degree at least eighteen.

The fixed vertices also receive explicit degree bounds. At a fixed vertex
`f`, list the twelve red bits to the other fixed vertices, followed by
three copies of each of its ten red moving-incidence bits. This lists
exactly its 42 incident edges, respecting orbit multiplicity. Counters
with bound 24 on this list and its negation impose the upper degree bound
in both colors, equivalently the full interval 18 through 24. These use
the same established Ramsey input as (1); they impose no new degree
profile, deficiency assumption or catalog restriction.

### Counter extension and soundness

For input occurrences `x_1,...,x_n` and bound `b`, allocate a variable
`S_ij` for `1<=j<=min(i,b+1)`. Include the implications

```text
x_i -> S_i1,
S_(i-1),j -> S_ij,
(x_i AND S_(i-1),(j-1)) -> S_ij,
NOT S_n,(b+1),
```

whenever the relevant cells exist (the third implication requires `j>1`).
Induction forces every reached prefix threshold. An overflow therefore
contradicts the last clause. Conversely, assigning true prefix thresholds
satisfies every clause when the bound holds. This proves the existence
of an auxiliary extension for every valid primary assignment. Occurrences
are counted, so the proof applies to signed and repeated literals.

The moving common and degree counters allocate 190 and 700 cells. Each
fixed degree counter allocates 750 cells. Including the truth-table gates,
the total variable count is `28878+3r(10-r)`. All identifiers are below
the constant sentinel 100000; integer arithmetic is far below C++ limits.

### Fixed-signature sorting

For adjacent signatures `A,B`, each coordinate and each possible common
binary prefix gives a clause excluding that prefix together with a first
disagreement `A_q=1,B_q=0`. The matching-prefix clause enforces order at
the first unequal coordinate; other clauses are satisfied. Equal
signatures satisfy all clauses. This is precisely lexicographic order.

## Verification boundary

The Python generator uses modular differences. The separate C++ checker
builds all 903 actual pairs, joins them under the permutation by DSU, and
recovers the 353 pair orbits. It reconstructs every primary and auxiliary
clause, including all counter inputs from actual incident edges. It
compares the complete canonical DIMACS stream, not only counts or a core.

The 30-vertex fixture has 219 red edges, with five red and five blue
rotating triangles. A literal audit checks all 142,506 five-subsets,
rotation invariance, the deficit bound and the complete-block cap. It
shows that the moving-vertex conditions have a valid partial graph.
It is not a 43-vertex target witness.

Any final UNSAT assertion requires replay of the corresponding general
DRAT trace, which may contain RAT steps and deletions. A solver verdict,
timeout, or stored hash alone is not a proof. The mathematical reduction,
normalizations and counter argument remain unformalized; exact execution
trusts the checking implementations, runtime, compiler and external DRAT
checker. Internal checking is not independent peer review.

## Certified exclusions and the surviving case

The complete formula counts are:

| red triangles | variables | clauses | status |
|---:|---:|---:|:---|
| 0 | 28,878 | 922,248 | DRAT verified |
| 1 | 28,905 | 924,030 | DRAT verified |
| 2 | 28,926 | 925,416 | DRAT verified |
| 3 | 28,941 | 926,406 | DRAT verified |
| 4 | 28,950 | 927,000 | unresolved |
| 5 | 28,953 | 927,198 | DRAT verified |

The complete C++ reconstruction passes all six formulas. For each of the
five excluded cases, Kissat supplies a trace and the external `drat-trim`
checker verifies it against that exact audited formula. The published
reproduction generates all six formulas, verifies their canonical hashes
and clauses, and regenerates and checks the five certified traces. It
explicitly skips a proof claim for `r=4`. These facts rule out every
normalized internal-color count except four, proving the theorem.

The general DRAT traces can contain RAT steps and deletions. They cannot
be treated as addition-only RUP proofs. Large formulas, traces and logs
remain outside Git; source, exact recipe, pinned tool versions, sizes and
hashes are published. Verification requires regeneration and successful
replay, not merely comparison with a stored hash. Different valid proof
hashes require successful replay against the identical audited formula.

The new fixed-degree counters were useful experimentally: the earlier
encoding without them reached a 60-second limit for `r=1,2,3,4`. The
strengthened encoding closed `r=1,2,3`. The `r=4` case reached its
180-second limit both with the basic normalizations and with additional
anchor ordering (3). These timings are observations, not impossibility
proofs or intrinsic complexity estimates. No incomplete trace is used
as a certificate.

Optimized and sanitized complete-clause checks, clause mutations, exact
local arithmetic, signed/repeated counters, graph relabelings, anchor
profiles and the positive fixture supplement the certificate replay.
The fixed-vertex counter is reconstructed from all 42 actual incident
edges, so orbit multiplicities are checked without using the generator's
weighted list.

The only graph-theoretic external input to this direct theorem is
[McKay--Radziszowski, R(4,5)=25](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf).
The inherited minimum-ten statement additionally uses the previous
[nine-cycle exclusion](../ramsey_r55_order3_nine_cycle_obstruction), whose
complete dependency chain has an
[accepted independent review](../ramsey_r55_order3_nine_cycle_review1).
The new theorem is independent of the global order-five exclusion,
external graph catalogs, and the teammate's asymmetric hard-branch work.
It has internal reconstruction and certificate checking, but no new
independent peer review is claimed.
