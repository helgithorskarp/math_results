# Fault-tolerant alternating Hamilton cycles in every hypothetical good43

Color the edges of the complete graph red when they are edges of `G` and blue
otherwise.  A path or cycle is *properly colored* when consecutive edges have
different colors.  Because there are only two colors, such a path or even
cycle alternates colors.

## The theorem

Let `G` be a graph on 43 vertices with neither a clique nor an independent set
of order five.

1. Every even induced vertex set `W` with `28 <= |W| <= 42` has a properly
   colored Hamilton cycle.
2. Every induced `W` with `28 <= |W| <= 43` has a properly colored Hamilton
   path.  When `|W|` is odd, any prescribed vertex can be an endpoint.

In particular, deleting any odd number of vertices from 1 through 15 leaves an
alternating Hamilton cycle, and deleting any at most 15 vertices leaves an
alternating Hamilton path.  The quantifier is over every vertex set; there is
no automorphism, catalogue, carrier, edge-layer, or selected-root hypothesis.

The reusable non-Ramsey form of the central bridge is also worth isolating.

**Factor-merger lemma.**  In a 2-edge-colored complete graph of even order,
suppose there is no monochromatic `K5`, each vertex has at least three
incident edges of each color, and there is an alternating cycle factor.  Then
there is an alternating Hamilton cycle.  In particular, the cycle-factor
hypothesis holds when each color class has a perfect matching.

The proof below establishes this general lemma first and then checks its
hypotheses simultaneously on all eight even induced-set orders.

## Inputs

The preceding complete-class theorem in
`ramsey_r55_fault_hamiltonicity/PROOF.md` establishes simultaneously in red
and blue that every induced 28-set is traceable and every induced set of order
at least 29 is Hamiltonian.  Its accepted target-specific connectivity source
and review are pinned in `DEPENDENCIES.json`.

We also use the Bánkfalvi--Bánkfalvi characterization.  A 2-edge-colored
complete graph `K_(2n)` has an alternating Hamilton cycle if and only if it
has an alternating cycle factor and, for every `2 <= k <= n-1` and every pair
of disjoint `k`-sets `X,Y`,

```
sum_(x in X) d_red(x) + sum_(y in Y) d_blue(y) > k^2.       (BB)
```

The source is M. Bánkfalvi and Zs. Bánkfalvi, *Alternating hamiltonian circuit
in two-coloured complete graphs*, Theory of Graphs (Proc. Colloq., Tihany,
1966), Academic Press, 1968, pp. 11-18, MR0233731.  The exact source trail is
recorded in `DEPENDENCIES.json`.

## Alternating cycle factor

Two elementary facts supply the bridge.

1. A monochromatic Hamilton path of even order contains a perfect matching:
   take alternate path edges.
2. If a red perfect matching and a blue perfect matching cover the same
   vertex set, their union is a vertex-disjoint collection of properly
   colored even cycles.  The matchings share no edge because every physical
   edge has exactly one color.  Every vertex has one incident edge of each
   color in the union.

Fix an even induced vertex set `W`, where `28 <= |W| <= 42`, and put
`m=|W|`.

- If `m=28`, each color on `W` has a Hamilton path.  Taking alternate edges
  gives a red and a blue perfect matching on `W`, hence a spanning properly
  colored cycle factor.
- If `m>=30`, each color on `W` has a Hamilton cycle.  Alternate
  cycle edges again give the two perfect matchings and the same conclusion.

## Every Bánkfalvi inequality is strict

The inherited minimum degree in each color is 18.  Deleting the `43-m`
vertices outside `W` gives

```
delta_red(W), delta_blue(W) >= 18-(43-m) = m-25 >= 3.       (1)
```

Let disjoint `X,Y` have order `k`, and put `Z=W-(X union Y)`.  Counting each
edge according to its location and color gives the exact identity

```
sum_X d_red + sum_Y d_blue
 = k^2 + 2 e_red(X) + 2 e_blue(Y)
       + e_red(X,Z) + e_blue(Y,Z).                          (2)
```

The `k^2` edges between `X` and `Y` are counted exactly once: a red edge at
its endpoint in `X`, or a blue edge at its endpoint in `Y`.

More generally, a minimum of three edges of each color at every vertex makes
the left side at least `6k>k^2` for `k=2,3,4`.  For `k>=5`, the set `X` cannot
be a blue clique when there is no monochromatic `K5`.  Hence `e_red(X)>0`, and
equation (2) is strictly greater than `k^2`.  This proves the factor-merger
lemma.  Equation (1) verifies its degree premise for every present `W`, and
the cases include every `2 <= k <= m/2-1` in (BB).

The alternating cycle factor and all strict inequalities now give an
alternating Hamilton cycle on every even `W` of order 28 through 42.

Deleting any edge from such a cycle gives an alternating Hamilton path.  If
instead `W` is odd of order 29 through 43, prescribe any `z in W` and apply
the even result to `W-{z}`.  Choose any cycle vertex `x`.  If `zx` has color
`c`, delete from the alternating cycle the edge incident with `x` of color
`c`, and add `zx`.  The result is a properly colored Hamilton path on `W`
with endpoint `z`.  This proves both parts of the theorem.

## Exact one-cell endpoint reduction

Delete any vertex and apply the theorem to the remaining 42 vertices.  Relabel
the alternating Hamilton cycle as `0,1,...,41,0`, and label the unrestricted
deleted vertex `42`, with

```
01 red, 12 blue, 23 red, ..., 40-41 red, 41-0 blue.
```

Therefore good43 existence is equivalent to satisfiability of one physical
Ramsey formula with exactly those 42 cycle-edge colors fixed.  No equality is
imposed on the other 861 physical edges, including all 42 edges incident with
vertex 42.  In particular, the displayed cycle is not required to be an
automorphism or an induced cycle.

For a five-set, the no-red-K5 clause is already satisfied if it contains a
fixed blue cycle edge; otherwise fixed red literals are deleted.  The
color-reversed rule gives the no-blue-K5 clause.  Exact enumeration yields

```
physical variables             861
clauses                     1493856
removed satisfied clauses    431340
clause widths                 8..10
```

The width counts are `8:13230`, `9:327852`, and `10:1152774`.  This is 36,729
fewer clauses than the monochromatic-Hamilton-cycle receiver, despite leaving
one additional physical edge free.  The improvement comes from fixing both
colors in one spanning skeleton.  `generate.py` emits the exact one-cell CNF;
`verify.py` reconstructs it independently and checks its semantics.

This reduction is a complete normalized physical problem, not a quotient by
a graph symmetry.  A satisfying assignment decodes directly to a literal
good43; an independently checked UNSAT proof for the generated CNF would
exclude every good43.  Neither terminal outcome is claimed here.

## Scope and trust boundary

The new argument is written mathematics depending on the cited alternating-
cycle characterization and the already published fault-Hamiltonicity theorem.
The latter inherits its computer-assisted connectivity and imported
`R(4,5)<=25` boundaries.  The software checks the finite receiver, arithmetic,
and a literal good42 control; it does not formalize either theorem.

No good43, Ramsey-bound change, physical exclusion, solver verdict, edge-layer
claim, or catalogue-completeness claim is made.
