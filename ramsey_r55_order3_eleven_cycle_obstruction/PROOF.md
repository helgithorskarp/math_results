# The eleven-cycle local reduction and complete formula cover

Let G be a two-coloring of the pairs of 43 vertices with no monochromatic
five-set. Suppose an order-three automorphism has eleven moving cycles,
so its type is `1^10 3^11`. The formulas in this package give an exact
six-case decision problem for this type. Individual computational conclusions
and remaining open cases are recorded separately in README.md and result.json.

## Local arithmetic

The only external graph-theoretic input to the direct reduction is
[McKay and Radziszowski, R(4,5)=25](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf).
Every color neighborhood is a graph with no same-color four-clique and
no opposite-color five-clique, so it has at most 24 vertices. Since the
two color degrees sum to 42, both degrees lie in [18,24].

Label the moving cycles `C_i = {3i,3i+1,3i+2}`, for `0<=i<11`;
vertices 33 through 42 are fixed. Each moving cycle is a monochromatic
triangle. Write its color as c_i. Let a_i count the fixed vertices joined
to C_i in color c_i, let w_ij be the number of c_i-colored neighbors per
vertex in C_j, and let m_i count those blocks with w_ij=3. The degree in
the triangle's own color is

```
d_i = 2 + a_i + sum_(j != i) w_ij.
```

The common c_i-neighborhood of the triangle has a_i+3m_i vertices.
It contains no c_i-edge, since that edge and the triangle would give a
monochromatic five-set. Consequently it has at most four vertices, or
five of them would form an opposite-colored five-set. Thus

```
a_i + 3m_i <= 4,       18 <= d_i <= 24.               (1)
```

Define `delta(w)=2-w+3*[w=3]`, with values `(2,1,0,2)` for `w=0,1,2,3`,
and let D_i be its sum over the ten other moving cycles. Then

```
sum w_ij = 20 + 3m_i - D_i,
d_i = 22 + a_i + 3m_i - D_i.
```

For a prescribed ten-weight vector, (1) is precisely the fixed-count interval

```
max(0, D_i-4-3m_i) <= a_i <= min(10, 4-3m_i, D_i+2-3m_i).      (2)
```

An integer in this interval exists exactly when `D_i<=8` and `m_i<=1`.
For necessity, combine the degree lower bound with the common-neighbor cap;
m_i>=2 immediately makes a_i+3m_i>4. For sufficiency, if m_i=0 the interval
is nonempty for every D_i in [0,8]. If m_i=1, necessarily D_i>=2, and the
interval is nonempty for every D_i in [2,8]. The fixed count cap ten is
harmless here but retained explicitly.

The upper degree bound is a new active restriction at eleven moving cycles.
At ten cycles the analogous formula starts with 20, and the common-neighbor
cap already bounds the degree above by 24. At eleven cycles it starts with 22.
Dropping `D_i+2-3m_i` from the upper endpoint admits exactly twelve spurious
arithmetic profiles: all ten weights equal two with a_i=3 or 4, and one
weight equal one with the other nine equal two and a_i=4, in ten positions.
These have own-color degree 25 or 26. All production formulas include the
upper degree bound; no earlier ten-cycle theorem is changed or challenged.

Two exact counts agree entry by entry. One enumerates all `4^10=1048576`
ordered weight vectors and all eleven possible fixed counts. The other
counts occupancy vectors `(n_0,n_1,n_2,n_3)` with multinomial multiplicities.
There are 80,726 admissible local arithmetic profiles, split into 35,046
with m_i=0 and 45,680 with m_i=1. These are necessary local arithmetic data,
not graph realizations or a classification of complete graphs.

The deficit bound alone admits 23,565 additional weight vectors with too
many complete blocks. For m=2 choose the positions in 45 ways; the other
eight weights have total deficit at most four, in
`1+8+36+112+266=423` ways. For m=3 there are `120*(1+7+28)=4320` vectors;
for m=4 there are 210. The total is `45*423+4320+210=23565`.

## Complete centralizer normalization

Complement the entire graph if necessary so that the number r of red moving
triangles is at most five. There are six cases r=0,1,2,3,4,5 because eleven
is odd. Permute the moving cycles so that the first r have red internal
edges. Every independent cyclic rotation of a moving triangle commutes with
the given automorphism. Fix the origin of C_0; independently rotate each
other triangle so that its three-bit red adjacency word from vertex 0 is
one of `000,100,110,111`, the unique cyclic representative with weakly
decreasing bits. This is possible even for constant words.

Now permute the nonanchor triangles within each internal color by increasing
anchor-word weight. The four canonical words form the componentwise chain
`000 <= 100 <= 110 <= 111`. Thus adjacent nonanchor triangles j,j+1 of
one internal color can be required to satisfy

```
b_(0j,t) <= b_(0(j+1),t),        t=0,1,2.             (3)
```

Carry coordinates identically when permuting whole cycles. The normalized
phases and internal colors are preserved. Finally, permute the ten fixed
vertices by lexicographically increasing eleven-bit red signatures on the
moving cycles. This does not change any moving edge. Equal weights and
equal fixed signatures are allowed. The order of these operations proves
coverage for every invariant graph. No extra graph automorphism is imposed;
these operations relabel the same order-three action.

The literal control enumerates all 2,048 internal-color profiles with
deterministically sampled remaining invariant edges. It constructs the
relabeling, checks commutation with the vertex permutation, all 903 literal
pairs, and all four normalizations. This is an implementation check in
support of the preceding general argument, not a sampling proof of coverage.

## Primary variables and full five-set clauses

The actual pair permutation has 331 orbits. Eleven internal triangle orbits
are constants, with the first r red. The remaining 320 Boolean variables are

1. 165 moving-cross bits in cycle-pair/difference order;
2. 45 fixed-fixed bits in vertex-pair order;
3. 110 fixed-moving bits in fixed-vertex/cycle order.

For i<j, the edge `(3i+s,3j+t)` has bit `b_(ij,t-s mod3)`. A fixed-moving
bit has three literal edge occurrences. For each of the 962,598 five-subsets,
substitute constants into both clauses forbidding all-blue and all-red.
Remove satisfied clauses, duplicate literals, tautologies and duplicate
clauses. Nothing is omitted by graph catalog, degree profile, or fixed-core
choice. In particular the ten fixed vertices retain arbitrary edges subject
to the complete Ramsey constraints.

## Gates and counters

For each pair of moving triangles and each internal color occurring at an
endpoint, create three exact gates

```
u=[delta(w)>=1],    v=[delta(w)>=2],    z=[w=3].
```

For each of the eight primary three-bit assignments, negate that assignment
and append the correct signed gate literal. These truth-table clauses force
each gate exactly. Same-color endpoints share gates; opposite-color endpoints
have their own gates. The gate count is `3*(55+r*(11-r))`.

The following occurrence-counted at-most constraints are added:

- At each moving triangle, the twenty u,v tokens sum to D_i and have bound 8.
- Its ten fixed own-color bits plus three copies of each complete-block gate
  count the common own-color neighborhood and have bound 4. This is a list
  of forty occurrences.
- Its forty actual outside-triangle own-color incidences have bound 22.
  With the two internal neighbors, this imposes total degree at most 24.
- The negations of that same forty-occurrence list have bound 24, imposing
  outside own-color degree at least 16 and total degree at least 18.
- At each fixed vertex, its nine fixed-edge bits and three copies of each
  of its eleven moving-incidence bits list all 42 edges. Bound 24 on the
  list and on its negation enforces both color-degree upper bounds.

The moving degree lower bound and common cap imply D_i<=8, but its explicit
counter is useful redundancy. The former full subset encoding would have
`C(20,9)=167960` clauses per moving triangle. The prefix counters used here
have 144 cells per deficit row and preserve all valid primary assignments.
This avoids adding 1,847,560 nine-token clauses; no performance comparison
between solvers or encodings is claimed.

For a signed input list x_1,..,x_n and bound b, allocate S_ij for
`1<=j<=min(i,b+1)`. Add

```
x_i -> S_i1,
S_(i-1),j -> S_ij,
(x_i AND S_(i-1),(j-1)) -> S_ij,
NOT S_n,(b+1),
```

whenever the referenced cells exist. Induction forces every reached prefix
threshold, so an input count greater than b forces the forbidden overflow.
Conversely, the true prefix-threshold assignment satisfies all implications
when the input count is at most b. This proves extension completeness and
soundness for repeated or signed literals. Each counter receives fresh cells.

A moving triangle uses 144 deficit, 190 common-neighbor, 667 upper-degree
and 700 lower-degree cells. Each fixed vertex uses two 750-cell counters.
Together with primary bits and gates, the variable count is
`34196+3r(11-r)`, at most 34,286. The constant sentinel 100,000 is disjoint
from every variable. All C++ loop indices, shifts and arithmetic are bounded
well inside the signed-integer range.

## Lexicographic clause layer

The phase and anchor order conditions have their displayed binary implication
clauses. For adjacent fixed signatures A,B, each coordinate q and each common
binary prefix of length q has a clause excluding exactly that equal prefix
followed by `A_q=1,B_q=0`. A first unequal coordinate therefore enforces
lexicographic order; equal signatures satisfy every clause. Each comparison
uses `2^11-1=2047` clauses before global deduplication.

All clauses are canonicalized by length and then signed integer tuple.
There are no separate unproved symmetry-breaking assumptions.

## Verification boundary

The Python generator uses modular differences. The C++ verifier independently
builds the 903 literal pairs and joins them under the actual vertex
permutation, recovering all 331 pair orbits. It independently reconstructs
every constant-substituted five-set clause, truth-table gate, prefix-counter
clause and normalization. It compares every canonical DIMACS line. The
counter reconstruction first allocates an entire cell array and then derives
its implications; the generator allocates row by row.

The counter control checks 1,734 assignments with positive, signed and repeated
inputs, giving explicit prefix extensions for feasible assignments and forced
unit conflicts for overflows. The seven-vertex two-triangle test checks all
32 assignments for each of three internal-color counts: 28,30,28 are Ramsey.
Both normal and optimized Python give the same complete control report.
Representative full formulas also pass address and undefined-behavior
sanitizers. Malformed full formulas must fail exact reconstruction.

Any claimed exclusion additionally requires a full DRAT trace replayed
against that exact audited formula. General DRAT may include RAT and
deletions. Neither a solver verdict, time limit, nor stored hash is a proof.
The source and compact manifests regenerate omitted large traces outside Git.
The direct theorem depends on R(4,5)=25 and the displayed unformalized
reduction, source correctness, compiler/runtime/hardware and drat-trim.
Internal independent reconstruction does not constitute external peer review.

This work does not depend on the C3-square or order-five exclusions, nor on
the teammate's non-symmetric hard-branch filters. Combining a future complete
exclusion of this type with the minimum-eleven theorem would raise the motion
minimum; any proper subset of the six certified counts does not do so.
