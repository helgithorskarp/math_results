# Fault-Hamiltonicity of every hypothetical good43

Call a graph *good* if it contains neither a clique nor an independent set
of order five.  Vertex connectivity is denoted by `kappa`, minimum degree by
`delta`, and independence number by `alpha`.

## The theorem

**Theorem.**  Let `G` be a good graph on 43 vertices, and let `c` be either
red (edges of `G`) or blue (edges of its complement).  For every vertex set
`S`, in color `c`:

1. if `|S| <= 15`, the graph on `V(G)-S` has a Hamilton path;
2. if `|S| <= 14`, the graph on `V(G)-S` has a Hamilton cycle;
3. if `|S| <= 13`, the graph on `V(G)-S` is Hamilton-connected.

Thus every induced `k`-vertex subgraph in either color is traceable for
`28 <= k <= 43`, Hamiltonian for `29 <= k <= 43`, and Hamilton-connected
for `30 <= k <= 43`.  These statements quantify over every set `S`; they do
not select a structured family or assume an automorphism.

## Inputs

Two established results are used.

1. The accepted complete-class good43 theorem in
   `ramsey_r55_maximal_vertex_connectivity` says

       kappa(G)=delta(G),  kappa(complement(G))=delta(complement(G)).

   Together with `R(4,5) <= 25`, its proof gives minimum degree at least 18
   in both colors.  The source proof is pinned in `DEPENDENCIES.json`; its
   independent accepting review is pinned separately.  The target-specific
   connectivity theorem is computer-assisted and retains the trust boundary
   stated in those sources.

2. The Chvatal--Erdos theorem says that a graph `H` on at least three
   vertices is Hamiltonian if `kappa(H) >= alpha(H)`, and is
   Hamilton-connected if `kappa(H) > alpha(H)`.  The original citation is
   V. Chvatal and P. Erdos, *A note on Hamiltonian circuits*, Discrete
   Mathematics 2 (1972), 111--113,
   <https://doi.org/10.1016/0012-365X(72)90079-9>.

The Hamiltonian statement is Theorem 1 of the cited paper.  The standard
Hamilton-connected companion is cited with the same result in the modern
literature.  This package does not reprove that classical theorem.

Finally, goodness gives `alpha(G) <= 4` and
`alpha(complement(G)) <= 4`, and these bounds are inherited by induced
subgraphs.

## Proof

Work in either color and write the corresponding graph as `X`.  The accepted
input gives `kappa(X) >= 18` and `alpha(X) <= 4`.

If `S` has order `s < 18`, then

    kappa(X-S) >= 18-s.                                  (1)

Indeed, deleting fewer than `18-s` additional vertices from `X-S` deletes
fewer than 18 vertices from `X`, so the remaining graph is connected.  All
graphs below have at least 28 vertices, so no small-order convention is
involved.

For `s <= 14`, equation (1) gives `kappa(X-S) >= 4`, while
`alpha(X-S) <= 4`.  Chvatal--Erdos gives a Hamilton cycle.  For `s <= 13`,
equation (1) gives `kappa(X-S) >= 5 > alpha(X-S)`, so the companion theorem
gives Hamilton-connectedness.

It remains to prove traceability at `s=15`.  Put `H=X-S`.  Then `H` is
3-connected and `alpha(H)<=4`.  Add one universal vertex `z`.  The graph
`H+z` is 4-connected: after deleting at most three vertices it is connected
through `z` if `z` remains, and otherwise at most two vertices were deleted
from the 3-connected graph `H`.  Also `alpha(H+z)=alpha(H)<=4`.
Chvatal--Erdos supplies a Hamilton cycle in `H+z`; deleting `z` from this
cycle leaves a Hamilton path in `H`.  The smaller values of `s` were already
Hamiltonian.  Color complementation proves all three claims in both colors.

## Quantitative consequences

Distinct vertex sets support distinct cycles.  Consequently each color has
at least

    sum_{k=29}^{43} binom(43,k) = 138712176296

cycles whose lengths lie from 29 through 43.  For `k>=30`, each endpoint
pair in each `k`-set has a Hamilton path, so each color has at least

    sum_{k=30}^{43} binom(43,k) binom(k,2)
      = 27336541560552

such endpoint-distinguished paths.

There is also an edge-rooted consequence.  Fix a color edge `uv` and delete
any at most 13 vertices other than `u,v`.  A Hamilton `u`--`v` path in the
remaining graph cannot use `uv` when at least three vertices remain.  Adding
`uv` closes it to a Hamilton cycle.  Different deletion sets have different
vertex sets, so every color edge lies on at least

    sum_{s=0}^{13} binom(41,s) = 30273024984

color cycles of lengths 30 through 43.  In particular, every edge in either
color lies on a spanning cycle of that color.

These are lower bounds on literal subgraphs, not orbit counts.

## Complete construction normalization

Every good43 has a red Hamilton cycle.  Relabel its vertices cyclically as
`0,1,...,42`.  Therefore good43 existence is equivalent to satisfiability of
the physical no-monochromatic-five constraints after fixing

    01,12,...,41-42,42-0

red.  This fixes exactly 43 physical edges and leaves all 860 chords free.
It does not equate chord orbits: rotation of the displayed cycle need not be
an automorphism of a completion.

For each five-set, the red-K5 prohibition remains.  If the five-set spans
`j` fixed cycle edges, its clause has width `10-j`.  A blue-K5 prohibition is
already satisfied when `j>0`, and otherwise remains a width-ten clause.  The
exact five-set distribution is

| fixed cycle edges `j` | 0 | 1 | 2 | 3 | 4 |
|---:|---:|---:|---:|---:|---:|---:|
| five-sets | 567987 | 334110 | 57276 | 3182 | 43 |

Thus the normalized formula has 860 variables and 1,530,585 clauses, with
width histogram

    6:43, 7:3182, 8:57276, 9:334110, 10:1135974.

The unconstrained physical formulation has 903 variables and 1,925,196
ten-literal clauses.  The normalization removes 394,611 clauses already
satisfied by a fixed red cycle.  The degree window becomes a chord-degree
window `16 <= d_chord(v) <= 22` at every vertex.

This is an exact existence-preserving receiver, not a good43, an UNSAT
claim, a quotient by a graph automorphism, or evidence that the residual
formula is easy.  `generate.py` emits it without fixing any other edge.

## Scope and trust boundary

The new deduction is an ordinary mathematical corollary of the accepted
maximal-connectivity theorem and the classical Chvatal--Erdos theorem.
The finite target-specific input is not re-established here.  The Python
programs check the arithmetic, clause semantics, a physical good42 positive
normalization control, and source hashes; they do not formally verify the
classical or accepted theorems.

No good43, Ramsey-bound change, edge-layer exclusion, packing-task decision,
solver verdict, automorphism condition, or catalogue-completeness claim is
made.
