# Proof of the five-module eight-terminal obstruction

All physical graphs below are strict unit-distance graphs: every pair of
distinct represented points at Euclidean distance one is an edge.

## 1. Assembly hypotheses

Let `V_1,...,V_5` be finite sets of distinct plane points and let
`T_i subset V_i` contain at least two points. Assume:

1. every two distinct points of `T_i` have distance strictly greater than two;
2. every assignment of four colours to `T_i` that is not monochromatic
   extends to a proper four-colouring of the strict graph on `V_i`;
3. for distinct `i,j`, `V_i intersect V_j` is contained in
   `T_i intersect T_j`; and
4. every unit edge of the strict graph on `V=union V_i` which is not internal
   to one module has both endpoints in `T=union T_i`.

There are no additional connector points. Suppose `|T|<=8`.

## 2. An arbitrary pair selection has maximum degree five

Choose any pair of distinct points in each `T_i`. Let `L` be the set of the
chosen pairs after duplicate pairs are identified, let `U` be the strict unit
graph on `T`, and put `H=(T,U union L)`. Edges in `L` express colour
inequality; they are not asserted to be physical unit edges.

Fix a terminal `x` and let `r` be the number of terminal sets containing it,
with repeated terminal sets counted by module. No unit neighbour of `x` lies
in one of those `r` sets. A terminal set not containing `x` contains at most
one unit neighbour of `x`: two such neighbours would be at mutual distance at
most two by the triangle inequality, contradicting their within-set distance
greater than two. Distinct unit neighbours therefore occupy distinct terminal
sets not containing `x`, so

```text
d_U(x) <= 5-r.
```

Only a chosen pair from a set containing `x` can add an `L`-edge incident with
`x`, and each set adds at most one. Hence `d_L(x)<=r` and

```text
Delta(H) <= 5.
```

This argument respects coincidences and repeated sets; either can only
identify neighbours or selected edges.

## 3. Five long edges cannot make a geometric K5

Suppose five distinct plane points form a clique in `H`. Every one of their
ten pairs then has length either one (an edge of `U`) or greater than two (an
edge of `L`). A triangle cannot have exactly two unit pairs: the remaining
distance is at most two and therefore cannot be an `L`-edge. Thus the unit
relation, after equality is adjoined, partitions the five points into unit
cliques.

A plane unit clique has at most three vertices. Normalize two of its points
to `(0,0),(1,0)`. A third common unit neighbour is one of the two equilateral
apices, and those two apices are not a unit pair. Therefore the partition
blocks have size at most three. The maximum possible number of unit pairs is

```text
binom(3,2)+binom(2,2)=4.
```

At least six of the ten clique edges would have to lie in `L`, but `L` has at
most five distinct edges in all. Hence `H` contains no `K5`.

## 4. Small graph lemma

**Lemma.** Every `K5`-free simple graph `X` on at most eight vertices with
maximum degree at most five is four-colourable.

Let `C` be the complement of `X`. A proper colouring of `X` is a partition of
`V(C)` into cliques. Add `8-|V(C)|` new universal vertices to `C`, mutually
adjacent as well, obtaining an eight-vertex graph `C'`. For every old vertex,

```text
d_C'(v)=7-d_X(v)>=2,
```

and a new vertex has degree seven. Moreover `alpha(C')<=4`, because an
independent five-set among the old vertices would be a `K5` in `X`, while a
new universal vertex cannot join another vertex in an independent set. It is
enough to partition `C'` into at most four cliques and then delete the added
vertices from those cliques.

If `C'` has a perfect matching, its four matching edges are the required
clique partition. Otherwise Tutte's one-factor theorem supplies a set `S`
such that the number `o(C'-S)` of odd components is greater than `|S|`.
Parity and the eight-vertex order leave the following cases.

* `|S|=0`: minimum degree two forces every component to have at least three
  vertices. The only possible odd-component orders are `3+5`. The
  three-vertex component is a triangle. Every five-vertex graph of minimum
  degree two has a matching of size two: otherwise all its edges are pairwise
  intersecting, hence form a star or a triangle, neither of which has minimum
  degree two on five vertices. The triangle, two matching edges, and the one
  unmatched vertex partition `C'` into four cliques.
* `|S|=1`: an isolated component of `C'-S` would have total degree at most one,
  while three nontrivial odd components need at least nine vertices. This case
  is impossible.
* `|S|=2`: the component-order possibilities outside `S` are
  `3+1+1+1`, `2+1+1+1+1`, and `1+1+1+1+1+1`. The latter two contain five
  vertices in different components, contradicting `alpha(C')<=4`. In the
  first, the three singleton components plus any nonadjacent pair in the
  three-vertex component would again be an independent five-set. That
  component is therefore a triangle. Each singleton is adjacent to both
  vertices of `S`, by minimum degree two. Use the triangle as one clique,
  pair two singletons with the two vertices of `S`, and leave the third
  singleton as the fourth clique.
* `|S|=3`: all five vertices outside `S` must be singleton odd components,
  contradicting `alpha(C')<=4`.
* `|S|>=4`: `o(C'-S)<=8-|S|<=|S|`, a contradiction.

Thus `C'`, and hence `C`, has a clique partition into at most four parts.
Those parts are independent sets in `X`, proving the lemma.

The cited classical source is W. T. Tutte, *The Factorization of Linear
Graphs*, Journal of the London Mathematical Society s1-22 (1947), 107-111,
[doi:10.1112/jlms/s1-22.2.107](https://doi.org/10.1112/jlms/s1-22.2.107).

There is also a computation-independent-of-Tutte validation route in this
package. A vertex-minimal non-four-colourable subgraph of `X` has minimum
degree at least four, since a vertex of degree at most three can be reinserted
into a four-colouring. Its degrees therefore lie in `{4,5}`. Exact enumeration
of every such labelled graph through order eight finds that each `K5`-free
one is explicitly four-colourable. This alternative is described in
`VALIDATION.md`.

## 5. Lift the terminal colouring through the modules

Sections 2 and 3 put `H` under the small graph lemma, so `H` has a proper
four-colouring. The selected pair in every `T_i` has different colours; hence
no `T_i` is monochromatic. Hypothesis 2 extends the fixed terminal word
through each module. The extensions agree at shared terminals by hypothesis
3. Internal edges are proper in their module extension, and all remaining
unit edges are terminal edges already proper in `U` by hypothesis 4.
Therefore the complete physical assembly is four-colourable.

The selected pair in each terminal set was arbitrary. The stronger universal
pair-selection statement, and in particular the requested existential
statement for five equilateral side-`sqrt(7)` terminal triangles, follows.

## 6. Exact target-budget consequences

Any non-four-colourable five-module assembly satisfying the hypotheses must
have at least nine distinct terminals. Private vertices of different modules
are disjoint under hypothesis 3, so an assembly of order at most 508 has at
most `508-9=499` private vertices in total. Some module then has at most
`floor(499/5)=99` private vertices. Five modules with at least 100 private
vertices each would instead have at least `5*100+9=509` physical points.

For the h4051 full A159/B214 modules, the private orders are 156 and 212.
With `b=0,...,5` B214 copies, the respective non-four-colourable order lower
bounds become

```text
5*156 + 56*b + 9 = 789, 845, 901, 957, 1013, 1069.
```

These bounds are conditional on the four assembly hypotheses. They are not
lower bounds for arbitrary unit-distance graphs and do not show that any
reduced module retains a negative forcing property.
