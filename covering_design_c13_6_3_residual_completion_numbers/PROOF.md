# Exact residual-completion theorem

## Statement and dependencies

Let `A` be a family of twelve distinct five-subsets of a twelve-point set
`V`, with point degree five, covering every pair, and with row intersections
at most two. Let `r(A)` be the minimum number of six-subsets whose union of
covered triples includes every triple missed by `A`.

The preceding complete classification gives six isomorphism classes: four
with deficit graph `4C_3`, one with `C_3+C_9`, and one with `2C_6`. Here
the point-deficit graph joins pairs occurring once in `A`; all other pairs
occur twice. The row-deficit graph, joining rows intersecting once, has
the same cycle partition by the predecessor's Gram argument.

For every such `A`,

```text
r(A) = 10 if the deficit graph is 4C_3;
r(A) = 11 if it is C_3+C_9 or 2C_6.
```

This contribution proves the two remaining exclusions. The previously
reviewed local obstruction proves `r(A)>=10`, and equality forces every
point to occur in exactly five residual blocks. The existing four
ten-block and two eleven-block upper witnesses are copied unchanged into
`families.json` and checked directly. Thus it remains to exclude
five-regular ten-block completions for the last two fixed families.

The six-class exhaustiveness theorem is an inherited, not newly reproduced,
dependency. Both concrete exclusions and each verified fixed-family optimum
can be read independently of that exhaustiveness claim. No conclusion about
the unrestricted value of `C(13,6,3)` follows beyond earlier bounds.

## 1. One common local problem

Fix a point `p`. Five members of `A` contain it. Delete `p`, obtaining five
four-subsets on the other eleven points. Each of these points occurs once
or twice, because pair multiplicities in `A` are one or two. Their twenty
incidences therefore give two singleton columns and nine weight-two columns.

Two of the four-subsets intersect in at most one point: adding `p` back
would otherwise make two `A` rows intersect in at least three. Represent
each weight-two column by an edge between its two rows. No edge repeats.
There are nine edges on five row vertices, so the graph is `K_5` minus
one edge. The two singleton columns occupy the endpoints of that missing
edge, since each row has size four.

Normalize those row endpoints to 0 and 1, and the other rows to 2,3,4.
The canonical eleven column supports, in order, are `{0}`, `{1}`, followed
by all two-subsets of `{0,...,4}` except `{0,1}` in lexicographic order.
An eleven-point pair is missed by the five rows exactly when its two
column supports are disjoint. Let `G` be this graph of missed pairs.
Its singleton vertices have degree seven and its nine edge vertices have
degree four, so it has `(2*7+9*4)/2=25` edges.

Suppose a ten-block residual completion `B` exists. Its degree-five
regularity says exactly five `B` blocks contain `p`. Deleting `p` from
these blocks gives five five-subsets covering all edges of `G`: such an
edge corresponds precisely to an original triple missed by `A`.

## 2. Exact local compatibility

There are 462 five-subsets of eleven points. For each `S`, decide whether
its covered edges can be augmented by at most four other five-subsets to
cover `G`. For each distinct individually admissible pair `S,T`, decide
whether their edges can be augmented by at most three others. Every block
and every pair of blocks in a genuine five-block local completion passes
these tests.

`local.py` implements exact set cover. Candidate five-subsets are represented
by masks of the 25 edges they cover. Duplicate coverage masks and masks
contained in another candidate mask can be removed: replacing a candidate
by a superset does not hurt edge coverage. Repetition is permitted in this
local search, so these tests remain a valid necessary relaxation regardless
of block distinctness elsewhere.

For uncovered mask `U` and remaining allowance `k`, the recurrence is:

1. Accept an empty `U`; reject nonempty `U` when `k=0`.
2. For `k=1`, accept exactly when one candidate contains all of `U`.
3. Reject if `|U|` exceeds `k` times the largest current candidate coverage.
4. Choose an uncovered edge and branch on every candidate containing it,
   recursing on the remaining uncovered edges with allowance `k-1`.

Every cover contains a candidate covering the selected edge, so the
recurrence is complete. Memoization changes no mathematical choice.

The row permutations preserving missing edge `{0,1}` form `S_2 x S_3`,
of order twelve. The code explicitly checks that each induced point
permutation preserves all edges of `G`. It evaluates a canonical member
of each orbit of blocks and unordered block pairs. There are 55 block
queries and 8809 queries for pairs of individually admissible blocks.
The full labelled mode omits this quotient and gives an identical complete
table, including its fingerprint.

Exactly 451 blocks and 29595 unordered pairs survive. These are necessary
local compatibility conditions, not sufficient conditions for a global
completion. Their exact table digest is in `EXPECTED.json`; the verifier
regenerates the table rather than trusting a stored answer list.

## 3. Lift to a global compatibility graph

For each of the 924 six-subsets `S` of `V`, and each `p` in `S`, normalize
the five `A` rows through `p` as above. The residue `S minus {p}` must be
an admissible local five-subset. Retain `S` only if this holds at every one
of its points.

Join distinct retained six-subsets `S,T` if their two residues form an
admissible local pair at every point in `S intersect T`. Disjoint blocks
need no pair test. Any ten-block completion therefore gives a ten-clique
in this compatibility graph, has point degrees exactly five, and covers
every triple missed by `A`.

All normalization maps are checked as bijections to the canonical eleven
supports. Choices of order among the two endpoints or the other three
rows differ by the explicitly handled local automorphism group. No global
isomorphism reduction or restriction on the automorphism group of `A`
is imposed.

The two negative-case graphs have:

| Class | Vertices | Edges |
|---|---:|---:|
| `C_3+C_9` | 849 | 39549 |
| `2C_6` | 840 | 39484 |

Every known ten-block witness for the four positive classes passes both
the vertex and pair tests. The verifier also finds a ten-block witness
anew for each of them and checks it from the original triple definition.

## 4. Complete regular-clique search

`completion.py` exhausts ten-cliques with the required margins and coverage.
At a state, the candidate mask contains only vertices compatible with
every chosen block. The traversal branches on each remaining vertex and
removes it from later siblings, so every possible completion is considered
once in the induced order.

Every prune is necessary:

- A point of current degree five excludes all further blocks containing it.
- A point exceeding degree five, or unable to reach five within the remaining
  slots or available candidates, makes the state impossible.
- Fewer candidates than remaining slots cannot finish a completion.
- A still-uncovered triple must occur in some remaining candidate.
- Greedy independent color classes give an upper bound on candidate clique
  size. In the reverse traversal, the unprocessed prefix is colored using
  at most its recorded number of colors. If this number plus the chosen
  size is below ten, no completion remains in that prefix.

When two slots remain, every point's deficit is zero, one, or two. Let `T`
be the points of deficit two and `O` those of deficit one. Every candidate
first block `S` must contain `T` and be contained in `T union O`; the other
block is then forced to be `T union (O minus S)`. The search checks its
availability, distinctness, compatibility, and coverage of all remaining
triples. This tests every possible two-block tail. Its size is automatically
six because the total remaining deficit is twelve; membership in the
candidate list checks that size directly as well.

The complete searches terminate with no survivor:

| Class | Search states | Two-block tails |
|---|---:|---:|
| `C_3+C_9` | 10235 | 4 |
| `2C_6` | 19498 | 1 |

No deadline, node limit, heuristic failure condition, or solver is used in
this proof. The checked eleven-block witnesses now match the lower bound.

## 5. Independent incidence SAT proof

The separate generator does not use `G`, the compatibility table, the global
compatibility graph, or clique coloring. Its 120 primary Boolean variables
`x[i,p]` specify ten six-subsets on twelve points. It enforces:

- Each row has six points; each column has five rows.
- Row masks increase strictly, eliminating only row permutations.
- Each of the 100 triples missed by the fixed `A` is in some residual row.

Two additional pair consequences improve propagation. If a pair `{u,v}`
occurs in one `A` row, seven other low points lie outside that row. Covering
their triples with `{u,v}` needs at least two residual rows, as one can
contain only four other points.

If `{u,v}` occurs in two `A` rows, their intersection is exactly `{u,v}`
and their union has eight points. At least one residual row contains the
pair. If exactly one does, it is forced to be

```text
{u,v} union (V minus (A_i union A_j)).
```

It must cover all four low points missed by those two through rows. The
CNF therefore requires either residual pair degree at least two or an
exact match to this forced six-subset in some residual row. Every actual
completion satisfies this disjunction.

Conversely, any satisfying assignment gives a genuine ten-block completion
by the direct row-size and triple-coverage clauses. The degree constraints
and row sorting are complete for possible ten-block completions by the
previously proved equality regularity and the freedom to relabel rows.
Distinctness is harmless: deleting a repeated block would give a forbidden
completion of size at most nine.

`cnf.py` uses explicit bidirectional Tseitin conjunctions, exact one-hot
saturated counters, and prefix-equality lexicographic comparisons. Counter
states represent each exact count below the cap and the at-least-cap state.
The initial zero state and deterministic Boolean transitions enforce this
meaning by induction; selecting a non-saturated final state enforces an
exact cardinality. The helper is adapted from the public orbit-51 generator,
with unchanged clause order and explicit argument checks.

Both CNFs contain 6579 variables and 31080 clauses. PySAT's `glucose4`
backend produced UNSAT traces, checked by `drat-trim` at the exact commit
recorded in `SAT_EXPECTED.json`. The checker reports `s VERIFIED` for both;
their cores contain only RUP lemmas (zero RAT lemmas). CNF and proof hashes,
counts, and observed timings are recorded. All four known ten-block
witnesses satisfy the incidence encodings when pinned as positive controls.

The large traces are retained outside the public checkout. Their generators
and checking workflow are published, and the main standard-library proof
does not need them. A proof hash alone is not treated as a proof.

## Trust and scope

The main theorem trusts the stated reductions, exact finite algorithms,
Python runtime, and hardware. The independent SAT proof additionally
trusts the CNF interpretation and DRAT checker/compiler; it does not trust
an unchecked UNSAT answer. The two architectures share the fixed inputs
and reviewed ten-block regularity theorem, but do not share their global
enumeration or negative certificate mechanism.

External review of these two new exclusions remains pending. The earlier
sharp-link review did not independently reprove six-class exhaustiveness;
this contribution does not change that assurance boundary. The newly
completed table concerns prescribed through families and does not exclude
the remaining maximum-intersection-three/four exceptional-profile cases.
