# Positive certificates for a hereditary four-colourability bound

## General lemma

Let H be a finite graph and F a set of distinct vertices such that H-v
has a proper k-colouring for every v in F. Then every subgraph J of H
with fewer than |F| vertices has a proper k-colouring.

Indeed, some v in F is absent from J. Consequently J is a subgraph of
H-v, and restricting its proper k-colouring colours J. Equivalently,
every non-k-colourable subgraph of H must contain all vertices of F.
This includes non-induced subgraphs: removing edges preserves a proper
colouring. The lemma does not assume H itself is non-k-colourable.

## Exact instance and certificate

L={0,...,373}; X is the previously committed, explicitly listed set of
200 pool vertices; and H is the strict unit-distance graph on L union X.
Its coordinates and input hashes are pinned in `manifest.json`. The
reviewed integer geometry reader reconstructs the 677-point universe
using a common denominator 288 in Q(sqrt(3),sqrt(5),sqrt(11)), checks
distinctness, and tests all squared distances exactly. Restriction gives
574 distinct vertices and 2707 edges. The sorted global-label edge stream
uses one `a,b` line per edge and has SHA-256:

```text
37d330b472e101c001e04aca6a1dc52ddf4f048d025adce0794f4e521682f575
```

The old certificate supplies a four-colouring of H-v for each v in X.
For each such row, the verifier concatenates its explicitly indexed
374-character L witness with its 200-character pool witness. The
new certificate supplies a full 574-character string for each v in
{0,...,308}, in the order L followed by sorted X. A dot appears exactly
at the deleted vertex, and all other entries lie in {0,1,2,3}.

For all 509 witnesses, the verifier checks that every edge whose
endpoints remain has differently coloured endpoints. It performs
1372888 retained-edge checks. Vertex labels 0,...,308 lie in L and are
disjoint from X, so

    F = {0,...,308} union X
    |F| = 309 + 200 = 509.

Applying the lemma with k=4 proves that **every subgraph of H with at
most 508 vertices is four-colourable**. No solver verdict or refutation
is needed. The previous non-four-colourability certificate for H gives
context, but is logically unnecessary for this exclusion theorem.

This is a finite family closure, not merely 309 isolated positive
observations: it covers all induced vertex subsets of order at most
508, and all their edge-deleted subgraphs. It does not assert that
H[F] is non-four-colourable, that H is vertex-critical, or that the
full 677-point universe has no smaller obstruction.

## Discovery CNF and symmetry

The discovery process retains all X and queries H-v for one L vertex
at a time. For each vertex w of H introduce four Boolean variables
C(w,c), c=0,...,3. For each w in L also introduce an activation A(w).
The formula consists of

    not A(w) OR C(w,0) OR C(w,1) OR C(w,2) OR C(w,3)   (w in L),
    C(w,0) OR C(w,1) OR C(w,2) OR C(w,3)              (w in X),
    not C(w,c) OR not C(z,c)                          (each edge wz, each c).

There are no at-most-one clauses. For a retained set Y subset L,
assume A(w) for every w in Y; unselected activations remain free.
The formula is satisfiable exactly when H[X union Y] is four-colourable.

To extend a proper colouring to a satisfying assignment, set the chosen
colour true at each retained vertex, set all colours false at absent
vertices, and set activations exactly on Y. Conversely, positive
assumptions require a true colour at each retained vertex. Choose any
true colour there. The edge clauses preclude equal chosen colours on
adjacent retained vertices. Extra activations or true colours on absent
vertices cannot invalidate restriction to X union Y. Hence leaving
unselected activations unassigned is sound in both directions.

The three pins C(384,0), C(386,1), C(388,2) use a verified triangle
entirely in X. All its vertices remain in every query. Any proper
four-colouring gives this triangle three distinct colours, and one
global permutation realizes the pins. The pinned and unpinned formulas
are equisatisfiable for every selected Y. This avoids using the old L
triangle when one of its vertices is deleted.

The resulting formula has 4*574+374=2670 variables and
574+4*2707+3=11405 clauses. Its SHA-256 is

```text
6b9dbf0c41fcb6757f2ebf608c18f8bf7c1542c24ade7b028ac1aae02e484036
```

The previously classified twenty interfaces concern the complete L.
They need not exhaust colourings after an L deletion and are not used
by this oracle. Their explicit positive witness strings remain valid
inputs to the final checker because the checker tests every edge.

## Finite run and trust boundary

The run attempted L vertices in ascending order with one incremental
CaDiCaL instance and saved a directly checked model after each SAT
answer. It stopped as planned when labels 0,...,308 supplied 309
witnesses. No graph update or subset-minimization step occurred.
All 309 answers were positive. The 65 remaining labels were not queried.

Finite controls compare all selected subsets in 48 abstract fixtures
with a direct backtracking definition of four-colourability: 1629
assignments, of which 1561 are SAT and 68 UNSAT. They include 99
assignments with required-triangle pins. A known actual-graph pool
deletion was also solved and directly checked. Separate checker controls
reject a monochromatic edge and five malformed witness cases.
These are implementation checks, not a proof of the general encoding.

The final theorem trusts the stated elementary restriction argument,
the pinned exact coordinate inputs and integer edge reconstruction,
and direct finite witness verification. It does not trust CaDiCaL's
negative answers, interface completeness, unverified numerical distances,
or the producing run's coverage claims. The checker explicitly requires
one witness for each of the 509 distinct specified vertices. These are
author checks, not external peer review or proof-assistant formalization.

## Consequence for continuation

Every further vertex deletion inside H remains in the closed family
once its order is at most 508. Deletion-only refinement of this seed is
therefore ruled out for a strict improvement of the 509-vertex record.
Any successful graph using the larger 677-point universe must contain
at least one of the 103 pool vertices outside X. The latter branches
remain open; they were not explored in this pass. For full-L subsets
of X, the earlier 200 deletion witnesses already gave the needed
closure. The new theorem removes the requirement to retain L.
