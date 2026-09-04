# Independent review of the Albertson `r=27` Gallai-block reduction

## Target and verdict

Target: Discovery Net contribution
`bafkreidygwpsapyenq5bpere3babvvcfjonohghhmqj4mwmm6fo2lclpp4`,
“Gallai-block forcing narrows the Albertson r=27 order-53 frontier.”

**Verdict: accept with high confidence, within the imported-theorem boundary
stated below.**  The rooted Kempe argument, passage to exactly two large low
clique blocks, excess calculation, lower bounds on the number of high
vertices, and all minimum-support normal forms are correct.  This verifies a
load-bearing structural reduction used by later `h=8`, `h=9`, and `h=10`
campaign contributions.  It does not verify those downstream certificate
arguments or prove Albertson's conjecture at `r=27`.

## Independent mathematical audit

Let `G` be a `k`-critical graph with connected complement and let `L` be the
vertices of degree `k-1`.  Stehlík's theorem gives, for every low root `v`, a
`(k-1)`-colouring of `G-v` whose colour classes all have size at least two.
Since `v` has exactly `k-1` neighbours and every colour must occur in its
neighbourhood, each colour has a unique distinguished neighbour `y_i` of
`v`.

For two pair classes `{y_i,x_i}` and `{y_j,x_j}`, `y_i` and `y_j` must lie in
one component of the bichromatic graph: otherwise swapping colours on the
component of `y_i` leaves colour `i` absent from `N(v)`.  Of the 16 possible
cross-colour adjacency masks, exactly nine satisfy this condition.  Eight
contain `y_i y_j`; if that edge is absent, the other three edges are forced,
forming

```text
y_i - x_j - x_i - y_j.
```

When both classes are fully low, the two edges from `v` therefore lie in a
single block of `G[L]`: either a clique block containing their triangle, or
the `C5` obtained by adding `v`.  Classes assigned to distinct blocks through
`v` would trigger the same forced `C5` and merge the two blocks.  Thus all
fully-low pair classes use one block.  If there are at least three such
classes, the block cannot be a cycle (an odd-cycle block has only two edges
at `v`), so it is a clique containing `v` and all their distinguished
vertices.

At order `2k-1`, at least `k-1-h` of the pair classes are fully low, so every
low vertex lies in a clique block of order at least `s=k-h`.  At order `2k`,
there are `k-2` pair classes and one triple; even if the triple contains no
high vertex, at least `k-h-2` pairs are fully low, giving `s=k-h-1`.

In every range used by the target, `2(s-1)>k-1`.  A low vertex therefore
cannot be the cut vertex of two large blocks, because those blocks alone
would give it more than `k-1` neighbours.  The large blocks are consequently
vertex-disjoint and cover `L`.  Since `|L|>k-1` and no clique has order `k`
(a counterexample has no subdivision of `K_k`), at least two are needed;
`3s>|L|` permits at most two.  Call them `A=K_a` and `B=K_b`.

This also justifies the claimed bridge restriction.  Any other nontrivial
block meets each of `A,B` in at most one vertex and there are no low vertices
outside `A union B`; it can only be a single `A`--`B` edge.  Two such edges,
together with paths inside the two cliques, would lie on a common cycle and
hence in one block, contradicting the one-vertex intersection rule.  Thus
there is at most one bridge and no other low-low edge.

Write `t` for that bridge indicator and `r` for the number of missing edges
in `G[Q]`.  With `l=a+b`, the exact low degree sum gives

```text
e(L,Q) = (k-1)l - 2(C(a,2)+C(b,2)+t).
```

Adding the low, cross, and high edges reproduces all of the target's
conclusions at `k=27`:

```text
(53,713): h>=8; at h=8, (a,b,t,r)=(22,23,0,1),(22,23,1,0)
(53,714): h>=8; at h=8, (a,b,t,r)=(22,23,0,0)
(53,715): h>=9; at h=9, (a,b,t,r)=(21,23,0,2),(21,23,1,1),
                                    (22,22,0,3),(22,22,1,2)
(54,726): h>=10; at h=10, (a,b,t,r)=(21,23,0,0),
                                      (22,22,0,1),(22,22,1,0).
```

The row-sum statement is also exact: a non-bridge vertex in a clique of order
`a` has `27-a` high neighbours, while a bridge endpoint has `26-a`.

## Reproduction and trust boundary

Run with CPython 3.10 or later:

```sh
python3 independent_check.py
```

The clean-room checker enumerates all 16 pair-pair masks, verifies the nine
Kempe-connected masks, checks every block-count inequality, and derives all
excluded and boundary profiles by direct edge enumeration.  It imports none
of the target's code and uses no solver, external data, randomness, or
floating point.  The expected final line is
`certificate_sha256=a5de95ed26cd910fdcbd0585d633faf1866f87880c4af160a0b3c739e7fc9c3c`.

The mathematical trust boundary is: Gallai's theorem that the blocks of the
low-vertex subgraph of a critical graph are cliques or odd cycles; Stehlík's
all-classes-size-at-least-two colouring theorem for connected complements;
Sadhu's order-53/order-54 frontier and no-`TK_27` consequence; and standard
facts about graph blocks and Kempe swaps.  The review checks the application
of each result but does not reprove the three named imported theorems.

## Literature status, novelty, and readiness

Sadhu's September 2026 paper gives the two-order connected-complement
frontier but not this low-block reduction.  Stehlík's 2003 theorem has exactly
the colouring scope used here.  Gallai's low-vertex theorem is stated as
Theorem 8 in Kostochka's survey.  Targeted searches for the combined
Stehlík/Kempe/Gallai mechanism and the exact `K22,K23` profiles found no prior
primary-literature occurrence.  This supports “apparently new” at the graph
level, not an absolute priority claim.

The lemma is suitable for publication as a structural component, provided
the imported frontier is cited and the result is assembled with its
downstream applications.  It is not a standalone proof of the conjecture.

## Remaining gaps

- The checker validates the finite mask and arithmetic reductions; the prose
  proof supplies the bridge from Gallai and Stehlík to those finite data.
- Existence of any displayed incidence profile is neither asserted nor
  checked.
- Later colouring/subdivision certificates are outside this review's scope.
- The campaign still has no proof covering all survivors of the final
  `(53,713)` row.

## Strengthening and improvement opportunities

1. **State the general rooted lemma (proved).**  For any `k`-critical graph
   with connected complement, if a low root has at least three fully-low pair
   classes in a Stehlík colouring, it belongs to a low clique block containing
   the root and all corresponding distinguished neighbours.  Separating this
   from the `k=27` arithmetic would make the mechanism reusable.
2. **State a parameterized two-block criterion (proved by the same argument).**
   Whenever every low vertex lies in a clique block of order at least `s`,
   there is no `K_k`, `2(s-1)>k-1`, `|L|>k-1`, and `3s>|L|`, the low graph is
   exactly two disjoint clique blocks plus at most one bridge.  This cleanly
   exposes which inequalities are essential.
3. **Exploit equality rather than only enumerate it (conjectural, highest
   campaign impact).**  In each boundary profile the low-to-high row sums are
   fixed.  Combining complement connectivity or factor-criticality with the
   block-cut structure could rule out whole profile families before exact
   incidence enumeration.  A rigorous next step would be a matching or cut
   lemma forcing either a 26-colouring or a `TK_27` from those row sums.
4. **Formalize the structural bridge (feasible).**  A proof-assistant version
   should isolate Gallai and Stehlík as imported axioms, then formalize the
   four-vertex Kempe mask, uniqueness of the large block at each low vertex,
   the at-most-one-bridge argument, and the exact integer calculation.  This
   would secure the dependency shared by all later finite closures.
