# Rooted Kempe-block states at the Albertson `r=27` frontier

This note gives a complete finite-state **over-encoding** of all four cases
left by the September 2026 Albertson reduction.  It also eliminates, by
explicit topological-clique certificates, every member of the classical
Kostochka--Stiebitz `E_27` family that has one of the three surviving
order-53 edge counts.  It does not settle Albertson's conjecture for
chromatic number 27.

## Rooted normal form

Let `G` be a `k`-critical graph, assume that its complement is connected,
and let `v` have degree `k-1`.  Stehlik's theorem supplies a `(k-1)`-coloring
of `G-v` in which every color class has at least two vertices.  Since `v`
must see every color and has only `k-1` neighbors, every color class has a
unique vertex `y_i` adjacent to `v`.

For any two colors `i,j`, the vertices `y_i,y_j` lie in the same component
of the bipartite graph induced by the two color classes.  Otherwise, swap
colors on the component containing `y_i`.  The unique neighbor of `v` with
color `i` changes color, while the unique neighbor with color `j` is outside
the component; color `i` is then absent from `N(v)` and can be assigned to
`v`, a contradiction.

### Two pair classes: nine masks

When both classes are pairs, write them as `{y_i,x_i}` and `{y_j,x_j}`.
If `y_i y_j` is an edge, the other three cross-class edges are arbitrary.
If it is not an edge, the only possible connecting path is

```text
y_i - x_j - x_i - y_j,
```

so all three displayed edges are forced.  Hence exactly

```text
2^3 + 1 = 9
```

of the 16 bipartite `2 x 2` adjacency masks are possible.

This contains the paired-shadow exclusion in the preceding conformal-
complement note: if `y_i y_j` is a complement edge, then `x_i x_j` cannot
also be a complement edge.  The Kempe form additionally fixes both cross
edges in that case.

### One triple and one pair: 39 masks

If the first class is `{y_0,a,b}` and the second is `{y_i,x_i}`, then a
missing edge `y_0 y_i` forces `y_0 x_i` and requires at least one of `a,b`
to be adjacent to both `x_i` and `y_i`.  There are 32 masks with the direct
edge present and

```text
4^2 - 3^2 = 7
```

with it absent, for a total of 39.  No longer connecting path is possible
in a bipartite graph with sides of sizes three and two.

## Complete map of the four frontier cases

At order 53, the degree excesses above 26 are respectively 48, 50, and 52
for `m=713,714,715`.  Thus there are at least 5, 3, and 1 degree-26 roots.
For any such root, Stehlik's 26 classes partition 52 vertices and therefore
are all pairs.  After ordering the classes, the graph is uniquely described
by one of the nine masks on each of the `binom(26,2)=325` class pairs,
together with the fixed 26 root edges.

At order 54 and `m=726`, the total degree excess is 48, so there are at
least six degree-26 roots.  For any such root, the 26 color classes on the
other 53 vertices consist of one triple and 25 pairs.  Put the triple first,
order its two nondistinguished vertices, and order the pair classes.  The
graph is then uniquely described by 300 nine-state pair-pair blocks and 25
39-state triple-pair blocks, again with 26 fixed root edges.

This is a map of every survivor, not a claim that every locally allowed
state is a survivor.  In particular, the counted family below deliberately
retains states that fail minimum degree at a nondistinguished vertex, have a
disconnected complement, are 26-colorable, or contain a topological
`K_27`.  Retaining them makes coverage transparent.

## Exact edge/excess filtered state counts

For a color-pair block `B`, let

```text
w(B) = number of edges in B - 1,
D(B) = (degree contributed to its two distinguished vertices) - 2.
```

Every allowed mask has `D(B)>=0`.  Across all class-pair blocks,

```text
sum_B D(B) = sum_i (d(y_i)-26).
```

The right side is at most the total degree excess of `G`.  This is a useful
global budget: only 48, 50, 52, or 48 distinguished-neighbor incidences can
occur above the one-per-other-color Kempe baseline.

In extra-edge/excess variables, direct enumeration gives

```text
P2(x,u) = (1+x)(1+xu)^2 + x^2

P3(x,u) = 1
          + (2+3u)x
          + (3+6u+3u^2)x^2
          + (2+5u+6u^2+u^3)x^3
          + (u+3u^2+2u^3)x^4
          + u^3 x^5.
```

Thus the exact labelled overfamily counts are

```text
n=53: [x^(m-351) u^<=E] P2(x,u)^325,
n=54: [x^375 u^<=48] P2(x,u)^300 P3(x,u)^25,
```

where `E=48,50,52` in the three order-53 rows.  The exact integers are in
`certificate.json`; their auditable sizes are:

| order, edges | decimal digits | bit length |
|---|---:|---:|
| 53, 713 | 219 | 726 |
| 53, 714 | 221 | 732 |
| 53, 715 | 223 | 738 |
| 54, 726 | 230 | 764 |

These numbers are a negative feasibility result: local-mask enumeration,
even after the exact edge count and distinguished-excess budget, is not a
credible flat search.  A complete computation must additionally impose the
nondistinguished degree constraints, the conformal matching conditions,
and isomorph rejection during generation.  The natural symmetry groups are
`S_26` at order 53 and `S_25 x S_2` at order 54.

For an independent closed count at order 53, choose `q` of `N=325` blocks
to use the forced indirect mask.  On the remaining `N-q` direct blocks,
choose `z` optional nondistinguished--nondistinguished edges and `d`
optional distinguished incidences.  The coefficient is

```text
sum_q binom(N,q) binom(N-q, W-2q-d) binom(2(N-q),d),
```

summed over `0<=d<=E`.  `verify.py` uses this formula.  The unrelated
implementation `independent_check.py` obtains the same four integers by
literal bivariate polynomial multiplication.

## A completed certificate stratum: every `E_k` graph contains `TK_k`

Kostochka and Stiebitz define `E_k` as follows.  Its vertices are four
nonempty sets `A1,A2,B1,B2`, with

```text
|A1|+|A2| = |B1|+|B2| = k-1,
|A2|+|B2| <= k-1,
```

and one vertex `c`.  The sets `A=A1 union A2` and `B=B1 union B2` are
cliques; the only `A`--`B` edges are all edges between `A2` and `B2`; and
`N(c)=A1 union B1`.

Every graph in `E_k` contains a subdivision of `K_k`.  Put
`a=|A2|`, `b=|B2|`.  If `a<=b`, use `A union {c}` as the `k` branch
vertices.  The only missing branch edges are `c x` for `x in A2`.
Because

```text
a <= b  and  a+b <= k-1,
```

there are `a` distinct vertices in each of `B1` and `B2`.  Pair them with
the vertices of `A2` and route the missing edges as

```text
c - B1_i - B2_i - A2_i.
```

The paths have disjoint internal vertices.  If `b<=a`, use the symmetric
construction with branch set `B union {c}`.  This proves the claim for all
parameters, not only `k=27`.

For `k=27`, an `E_27` graph has

```text
m = 701 + (|A2|-1)(|B2|-1).
```

The three surviving edge counts therefore give products 12, 13, and 14.
Up to swapping `A` with `B`, there are exactly six unordered parameter
types:

```text
m=713: (2,13), (3,7), (4,5)
m=714: (2,14)
m=715: (2,15), (3,8).
```

`certificate.json` records these six types.  The verifier constructs every
graph and checks every branch edge, routed edge, internal-vertex exclusion,
and path-disjointness condition.  Swapping the two sides accounts for all
12 ordered parameter pairs.  Hence no order-53 Albertson counterexample in
the three surviving edge rows belongs to `E_27`.

## Certificate endpoint for the remaining computation

The normal form suggests a proof-certificate format that avoids asking a
checker to trust chromatic-number or topological-minor decisions.  An
isomorph-free generator should enumerate the degree- and conformal-filtered
root states and attach to each canonical state either:

1. a 26-coloring, proving it is not a survivor; or
2. a `TK_27` certificate consisting of 27 branch vertices and one
   internally vertex-disjoint path for every missing branch edge.

Both alternatives are checkable in polynomial time.  A manifest of
canonical state hashes plus an independently reproduced canonical-augmentation
count would certify coverage.  The six `E_27` types above are the first
completed structural stratum under exactly these certificate semantics.

## Reproduction

Python 3.9 or later is sufficient; there are no third-party dependencies.

```sh
python3 verify.py
python3 independent_check.py
```

On the recorded host the closed-form verifier takes about five seconds.  The
independent dynamic program is intentionally simpler and slower.  All
assertions use exact integers; there is no solver, randomness, floating
point, external data, or imported project code.

## Sources, relation to prior work, and trust boundary

- A. Sadhu, [*Albertson's Conjecture Holds for r at Most
  26*](https://arxiv.org/abs/2609.01682v1), for the four-case frontier.
- M. Stehlik, [*Critical graphs with connected
  complements*](https://doi.org/10.1016/S0095-8956(03)00069-8), JCTB 89
  (2003), 189--194, for the all-classes-size-at-least-two coloring.
- A. V. Kostochka and M. Stiebitz, *Excess in Colour-Critical Graphs*,
  Bolyai Soc. Math. Stud. 7 (1999), 87--99, for the definition and
  criticality of the `E_k` family.
- The adjacent
  [conformal-complement reduction](../albertson_r27_conformal_complement_constraints/README.md),
  for the matching and paired-shadow constraints that the next generator
  should impose.

The Kempe swap, local mask classification, coefficient formulas, and
topological-clique construction are proved above.  The imported mathematical
boundary is Sadhu's frontier and Stehlik's theorem; membership of the named
`E_k` family as critical graphs is not needed for the subdivision proof, but
is the reason that family is relevant.  Targeted searches of the current
Albertson literature, the cited critical-graph sources, and the committed
Discovery Net found no prior statement of these exact rooted mask counts or
the general `E_k` subdivision certificate.  This is a search-relative
novelty assessment, not a claim of historical priority.
