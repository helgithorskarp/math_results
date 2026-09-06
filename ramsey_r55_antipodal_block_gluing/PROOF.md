# Conditional antipodal-block gluing for monochromatic K5 avoidance

This is a finite structural reduction and an exact interface, not an
existence or nonexistence result for Ramsey(5,5) graphs on 43 vertices.
The factorization principle is elementary; no priority claim is made.

## 1. General partial-coloring theorem

Let V be a finite labeled set. Suppose all pair colors are known except
the pairs in three complete bipartite blocks E_i=L_i x R_i, i=0,1,2.
The six vertex sets are pairwise disjoint. Prescribe row and column red
degrees within each block. The word "visible" means every pair outside
E_0 union E_1 union E_2, and its color is fixed in the following theorem.

For a five-set S and color c, discard its monochromatic-K5 prohibition
if a visible pair in S has color different from c. Otherwise the active
prohibition says that not every hidden pair of S has color c. Write
B(S)={i:S meets both L_i and R_i} for its block support.

**Support theorem.** Every active prohibition has one of these forms:

1. B(S) is empty: a visible monochromatic K5 already prevents every lift.
2. B(S)={i}: the hidden pairs are the complete rectangle P x Q with
   nonempty P=S intersect L_i and Q=S intersect R_i, and |P|+|Q|<=5.
   Its width is one of 1,2,3,4,6, never greater than six.
3. B(S)={i,j}: its hidden pairs are one edge in each block, or a
   two-edge wedge in one block and one edge in the other. Its width is
   two or three, and the wedge's edges share an endpoint.

Proof. Each used block needs at least two vertices of S. Three blocks
would need six distinct vertices, impossible. With one block, completeness
of its hidden bipartite pair set gives precisely P x Q, and pq<=6 for
positive integers p,q with p+q<=5. With two blocks the vertex counts are
2+2, 2+3 or 3+2 (possibly one unused outside vertex in the first case).
Two vertices give K1,1. Three vertices meeting both sides give K1,2 or
K2,1. These are all cases. No color, degree, symmetry, or Ramsey-number
theorem is needed for this argument.

Visible colors matter: a putative rectangle or wedge prohibition is
active only when every visible pair of that five-set has color c.
Dropping this guard would incorrectly strengthen the problem.

## 2. Exact gluing, not just pairwise nonemptiness

Assume there is no visible monochromatic K5. Let D_i be the full set of
binary matrices on E_i with the prescribed row/column margins satisfying
all active prohibitions whose block support is {i}. For i<j, define
R_ij subset D_i x D_j by retaining exactly those pairs of matrices that
satisfy all active prohibitions with support {i,j}.

**Gluing theorem.** A full lift with the prescribed margins and no red
or blue K5 exists if and only if there is (A_0,A_1,A_2) in D_0 x D_1 x D_2
with (A_i,A_j) in R_ij for every i<j. Equivalently, the tripartite graph
with vertex classes D_i and edge sets R_ij contains a triangle.

Proof. Restrict any valid full lift to the three disjoint blocks. Its
margins and one-block conditions give A_i in D_i, and its two-block
conditions give all three compatibility edges. Conversely, assemble a
compatible triple with the visible coloring. Any hypothetical monochromatic
K5 would have support zero, one or two by the support theorem. The
visible test, relevant domain, or relevant relation excludes it in each
case. All degrees inside the blocks follow from the prescribed margins.

The three graphs D_i may individually be nonempty and each R_ij may
contain an edge without there being such a triangle. Section 4 gives
an explicit physical counterexample. We do not claim this example defeats
arc consistency or every other stronger propagation procedure.

`glue.py` implements the theorem. Its domain enumeration chooses the red
positions in each successive row. It subtracts those choices from the
remaining column demands, rejecting a negative demand or one greater than
the number of remaining rows. These are necessary pruning conditions.
Every final matrix has been selected exactly once, and every prescribed
matrix follows its unique row choices. A fully assigned forbidden
rectangle is safely rejected when encountered. Thus a completed traversal
enumerates exactly D_i. The code tests every pair for R_ij and then tests
triples for a triangle, stopping at the first witness if any.

The work counter counts visited row-search nodes, tested matrix pairs,
and tested triples. It is not a CPU-time or memory bound, nor a bound on
the initial five-set scan. If exhausted, the result is INCOMPLETE. Only
an actual visible K5, a completely enumerated empty D_i, or a completed
join with no triangle yields a NO_LIFT status. The exponential size of
D_i is a remaining obstacle, not hidden by the factorization.

## 3. Exact H92 application and guarded interface

Use vertices0..42, H={0,..,19}, W={2,..,9}, D0={10,..,13},
D1={14,..,17}, D01={18,19}, X={20,..,28}, Y={29,..,37}, Z={39,..,42}.
Fix H92 and the red stars

    N_R(0)  = D0 union D01 union Y union Z union {38},
    N_R(1)  = D1 union D01 union X union Z union {38},
    N_R(38) = H.

Other root incidences are blue. These give276 fixed pairs and627 free
pairs. The three holes are Z x W, D0 x X, D1 x Y, respectively of sizes
4x8,4x9,4x9. Their104 pairs and38 vertices are disjoint across blocks.
The other523 free colors are visible variables, in lexicographic order.

The H92 source has SHA-256
926c18173764c02a45d6e6d46dc001eddff6a161570bdc3b1efcd8a24539f466.
The [physical projection](../ramsey_r55_antipodal_degree_projection) supplies
the pinned geometry and residual expressions. This proof does not need
its degree-margin census or its flow implementation for gluing.

The guarded interface enumerates every physical five-set in both colors,
simplifies only fixed pair colors and removes duplicate physical clauses.
A signed literal is positive to forbid all-blue, negative to forbid all-red.
Each JSONL record is `[guard, [[block, local_literals], ...]]`: the record
means the disjunction of its visible guard literals and all block literals.
Local edge numbers start at one in row-major L x R order. Guard numbers
start at one in visible lexicographic order. The prohibition activates
when every guard literal is false. Empty support means a visible-only
clause; empty guard would mean an unconditional residual prohibition.
All color guards are retained. The transformed record and physical clause
are mutually recoverable once the schema is fixed.

There are610,782 unique physical clauses. Their decomposition is:

| Hidden block support | Clauses |
| --- | ---: |
| None | 219,338 |
| One block | 332,908 |
| Two blocks | 58,536 |

The two-block part consists of32,346 two-edge and26,190 wedge-plus-edge
clauses. There are no three-block clauses. These are syntactic counts
before choosing visible colors, not counts of feasible graphs or active
clauses for any admissible assignment. In particular, this interface retains
all219,338 visible-only clauses; the older six-neighborhood clause stream
has only70,848 of them. This is a syntactic comparison, not a claim of
semantic irredundancy or separation of the feasible graph families.

For the fixed-family degree conditions, require red degrees20 at0,1,38
and21 elsewhere. Once the visible coloring x is assigned, set

    r(v) = target_degree(v) - known_visible_red_degree(v).

The known degree includes the fixed pairs and chosen523 colors. Require
r(v)=0 at0,1,18,19,38 and use the other r(v) as block margins. The two
marked blue neighborhoods of0 and1 must each have124 red edges. None
of their pairs is hidden, so these tests depend only on x.

`lift_h92.py` checks this complete pinned schema, the523 Boolean colors,
outside degrees, residual bounds, and both densities before calling the
generic oracle. A successful lift therefore satisfies the whole fixed
H92/stars/degrees/densities family with all global K5 conditions. Conversely
any graph in that family follows these steps and is represented by a
compatible triple. No symmetry or selected Q completion is imposed.

This is pointwise in a fully assigned x. No such admissible43-vertex
visible assignment is supplied here. No whole-H92, profile, M-stratum,
or unrestricted Ramsey43 family is decided. The previous full-K5 CNF
experiment remains UNKNOWN. This work does not rerun it.

## 4. Explicit obstruction to the weaker pairwise test

The compact input `negative.json` has12 vertices and holes

    {0,1} x {2,3}, {4,5} x {6,7}, {8,9} x {10,11}.

Every row and column margin equals one, so each2x2 block is either
matrix6 or matrix9, where the four bits in row-major order are used.
All unlisted visible pairs are blue. The input lists20 visible red pairs.
There is no visible monochromatic K5. Exact domains and relations are

    D0={6,9}, D1={6,9}, D2={6},
    R01={(6,9),(9,6),(9,9)},
    R02={(6,6)}, R12={(6,6)}.

Both relations involving block2 force the other state to6, but (6,6)
is missing from R01. Thus every domain and pair relation is nonempty,
yet no lift exists with these margins. The literal checker supplies
a blue K5 for each of the eight margin-correct triples; it also checks
all4,096 hole colorings without restricting the margins.

`positive.json` changes only the visible pair{0,4}, from blue to red.
It has five margin-correct K5-free lifts. One is(6,9,6). Both full
4,096-coloring truth sets, their conditional-clause truth sets, every
domain state, every compatibility edge, and every margin-correct joint
lift agree entrywise with a separate literal physical-graph oracle.
This is a12-vertex validation fixture, not the43-vertex target.

The negative fixture was found at sample508 (zero-based) of a bounded
50,000-sample exploration, Python Random seed553092. Search stopped at
the first witness, after509 visible assignments. The exact frozen input,
not the random sampler, is the mathematical counterexample.

## 5. Verification and trust boundaries

The H92 producer imports the pinned physical Model and scans all five-sets.
The separate verifier imports none of that code: it reconstructs fixed
colors, discovers opposite-signature hidden pairs and their connected
components, then uses fixed-color-compatible clique recursion. It unpacks
and compares every emitted clause entrywise, checks each rectangle/wedge,
and checks all462 abstract five-vertex occupancies among the six sides
and an outside cell. Six malformed records are rejected.

The generic oracle is checked by literal full-graph enumeration on8,192
fixture colorings. Seven malformed inputs, a visible-only K5, and a zero
work budget are tested. The H92 adapter is checked on the old G92 degree
fixture: it finds an already-known visible K5 without searching any block
states. That regression is not a new pruning result.

Normal and optimized Python produce identical interfaces and all compact
verification reports. These are internal algorithmically different checks,
not external peer review or proof-assistant formalization. Python integers,
interpreter/hardware, parsing, pinned source identities, and the displayed
unformalized argument remain explicit trusts. No SAT solver is used.

External review3287 independently accepted the earlier projected backend's
arithmetic equivalence. That resolved review gate is preserved, but the
backend arithmetic is not needed by this direct physical decomposition.
The review neither covers this new gluing code nor changes any UNKNOWN.
