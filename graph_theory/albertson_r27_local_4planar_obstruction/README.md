# A 24-vertex local obstruction at the Albertson `r=27` frontier

This note turns the surviving order-54 case of Albertson's conjecture into a
small equality problem for 4-planar drawings. It does **not** yet prove the
conjecture for chromatic number 27.

## Main reduction

The following single local statement would eliminate the order-54 survivor:

> **Local target.** Every simple graph with 24 vertices and 132 edges has
> crossing number at least 165.

Indeed, Büngener--Kaufmann give, for a graph with 24 vertices and `e` edges,

```text
cr >= ceil(37e/9 - 3410/9),
cr >= ceil(5e - 4466/9) = 5e-496.
```

For `e <= 131`, the first inequality (including its integer rounding) is at
least `5e-495`. At `e=132`, the local target gives the same inequality. For
`e>132`, repeatedly delete an edge with at least five crossings until 132
edges remain; such an edge exists by the sharp `6(n-2)` density bound for
simple 4-planar graphs. Consequently the local target implies, uniformly for
every 24-vertex graph,

```text
cr >= 5e-495.                                      (1)
```

Now let `G` be the sole order-54 survivor from the September 2026 frontier,
so `|E(G)|=726`. Sum (1) over all induced 24-vertex subgraphs in a fixed good
drawing. Every edge is counted `binom(52,22)` times and every crossing is
counted `binom(50,20)` times. Thus

```text
cr(G) >=
  (5*726*binom(52,22) - 495*binom(54,24)) / binom(50,20)
  = 1965795/322
  = 6104.953... .
```

Hence `cr(G) >= 6105 > Z(27)=6084 >= cr(K_27)`, a contradiction. Notice that
this is not a request for a generic improvement of the crossing lemma: it is
one exact finite value, `cr(24,132) >= 165`. The value 165 is also exactly the
endpoint predicted at `m=6(n-2)` by the sparse-crossing line conjectured by
Pach--Radoicic--Tardos--Toth.

## What a counterexample to the local target must look like

Assume a 24-vertex, 132-edge simple graph has a good drawing `D` with at most
164 crossings. Apply the deletion process in the proof of Theorem 6(a) of
Büngener--Kaufmann. Put `s=24-2=22`, and write:

- `a` for edges deleted with at least five crossings;
- `b` for edges deleted with four crossings;
- `c` for the first edge deleted from each full 3-planar hexagon while reducing
  to `5s=110` edges;
- `d` for the subsequent three-crossing edges deleted after the other two
  edges paired with each of those `c` configurations are removed.

Thus `a+b+c=22`. The resulting 2-planar drawing `D2` has
`e2=110-2c-d` edges. Let:

- `Delta` be the number of empty triangular faces of its crossing-free
  subgraph;
- `p,h` be the numbers of full 2-planar pentagons and hexagons in `D2`;
- `m0` be Büngener--Kaufmann's number of missing configuration-boundary
  edges; and
- `t` be the number of triangles of their auxiliary triangulation outside
  all forbidden configurations.

The strengthened sparse bound of Pach--Radoicic--Tardos--Toth and
Propositions 21 and 23 of Büngener--Kaufmann give the following entirely
integral system:

```text
e2 = 110-2c-d
x2 >= ceil((7e2-550+2Delta)/3)
164 >= 5a+4b+9c+3d+x2
t = 44-4c-3p-4h
3(p+h) >= 44-4c-3d+3m0
b <= c+h+4m0+2t,
```

with all variables nonnegative integers. Exhausting this small system leaves
exactly two profiles:

| | `a` | `b` | `c` | `d` | `Delta` | `m0` | `p` | `h` | `t` | `e2` | `x2` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 0 | 20 | 2 | 3 | 0 | 0 | 9 | 0 | 9 | 103 | 57 |
| B | 0 | 22 | 0 | 4 | 0 | 0 | 11 | 0 | 11 | 106 | 64 |

Every displayed lower bound is an equality. In particular, `D` is 4-planar,
the deleted four-crossing edges are pairwise noncrossing, and `D2` is an
equality drawing for Lemma 3.2 of Pach--Radoicic--Tardos--Toth.

## Equality structure of the 2-planar remainder

For completeness, the equality induction in that lemma sharpens the two
rows further. Form the *edge-crossing graph* of `D2`: its vertices are the
crossed edges of `D2`, adjacent when the corresponding edges cross.
It has maximum degree two.

The preliminary reductions in the cited proof cause no gap here. Adding a
missing crossing-free edge raises `e` without decreasing `Delta`, and hence
would make its inequality strict. A separation of order at most one is also
strict because of the `v-2` term. An equality separation therefore has order
two, and `e`, crossings, `Delta`, and `v-2` split additively; the argument may
be applied to its 3-connected blocks.

Within a block, equality excludes a path component on at least three vertices
(Case 3 of the induction) and a triangular component (Case 4.2). For a cycle
of length at least four, Case 4.1 followed by Case 3 removes two edges and four
crossings and creates an empty triangular face. Write

```text
delta(D) = 3x(D)-7e(D)+25s-2Delta(D).
```

The cited lemma says `delta >= 0`. If `D'` is the drawing after this two-edge
step and `r=Delta(D')-Delta(D)`, then
`delta(D)=delta(D')-2+2r`. Equality thus forces `r=1` and
`delta(D')=0`. A cycle of length at least six leaves a path on at least three
vertices and is therefore strict. A 4-cycle makes both of the two formerly
crossed neighbours crossing-free; applying the Case 3 triangle argument at
both crossings gives `r>=2`, also strict. Therefore only 5-cycles and single
crossing pairs remain.

Reduce every 5-cycle by the same two-edge step. If there are `q5` such
cycles, the terminal drawing is in the equality case of the 1-planar bound,
so

```text
e2-2q5 = 4s-q5/2,
q5 = (2e2-8s)/3.
```

It follows that the two rows have respectively

```text
A: 10 C5 components, 7 K2 components, 39 crossing-free edges;
B: 12 C5 components, 4 K2 components, 38 crossing-free edges.
```

A full 2-planar pentagon contributes one of these `C5` components. Comparing
with `p=9` and `p=11`, respectively, shows that **exactly one** `C5` component
is non-full in either profile. This is the remaining finite topological
obstruction: exclude the extension of one non-full crossing 5-cycle through
either row's rigid deletion history. Proving that exclusion proves the local
target and therefore removes the complete order-54 Albertson branch.

The only delicate point in the 4-cycle exclusion is distinctness of the two
new triangles. In the Case 3 notation, their third vertices are the two
different endpoints of the deleted edge: the two crossings are encountered
at opposite ends of that edge. Neither endpoint can be an endpoint of either
crossing edge in a good drawing. The two triangular vertex sets therefore
cannot coincide.

## Reproduction

Python 3.9 or later is sufficient; there are no third-party dependencies.

```sh
python3 verify.py
```

The verifier exhausts every nonnegative integer assignment allowed by the
displayed system, checks that exactly rows A and B survive, derives the
crossing-component counts, and checks the conditional sampling fraction using
integer arithmetic.

## Sources and trust boundary

- A. Sadhu, [*Albertson's Conjecture Holds for r at Most
  26*](https://arxiv.org/abs/2609.01682v1), for the reduction to
  `(n,m)=(54,726)` and `Z(27)=6084`.
- A. Büngener and M. Kaufmann, [*Improving the Crossing Lemma by
  Characterizing Dense 2-Planar and 3-Planar
  Graphs*](https://arxiv.org/abs/2409.01733v2), especially Theorem 6 and
  Propositions 21 and 23.
- J. Pach, R. Radoicic, G. Tardos, and G. Toth, [*Improving the Crossing
  Lemma by Finding More Crossings in Sparse
  Graphs*](https://doi.org/10.1007/s00454-006-1264-9), especially Lemma 3.2.
- E. Ackerman, [*On topological graphs with at most four crossings per
  edge*](https://doi.org/10.1016/j.comgeo.2019.101574), for the simple
  4-planar density bound.

The imported trust boundary is the cited crossing and density results and
their stated structural propositions. The profile enumeration and sampling
arithmetic are checked by `verify.py`; the equality-induction refinement is a
deductive argument recorded above, not a computer assertion. No claim is
made here that the final non-full-`C5` obstruction has been excluded.
