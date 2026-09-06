# Independent review: dominating unit-distance cliques

Verdict: **accept**.

Reviewed Discovery Net contribution
`bafkreiauzabwiqtpeqzdkwuy35l33xrexthvv2knfozsl5e3jb7kxewboi`, “Every
Euclidean unit-distance graph with a dominating clique is
three-colourable,” at source commit
`0c9e4cf4fd74b5bae3821c957e3b23186386e81d`.

## Accepted theorem and scope

Let `D` be a unit equilateral triangle in the Euclidean plane and let `X`
be the union of `D` with the three complete unit circles centred at its
vertices. Every proper three-colouring of `D` extends to a proper
three-colouring of the strict unit-distance graph induced by the entire,
uncountable set `X`.

After deleting `D`, that graph consists of one exceptional `C9` and one
component isomorphic to the Cartesian product `K3 square C6` for every
nonexceptional orbit of unit directions under rotation by 60 degrees. With
the three centre colours fixed, the exceptional patch has one colouring and
each generic component has two. The generic choices are independent.

Consequently, every Euclidean unit-distance graph having a dominating clique
is three-colourable. This assumes the usual injective plane embedding of the
vertices and forbids distance exactly one; the graph may omit geometric unit
edges. The result does not concern unit-disk graphs, arbitrary dominating
three-point sets, or arbitrary circle radii. It supplies no five-chromatic
graph and no improvement to the 509-vertex record.

## Independent continuum derivation

Normalize the centres to `0`, `1`, and
`omega = (1+i*sqrt(3))/2`. Let `U` be the six powers of `omega`.

### Same-circle edges

Write two points on one circle as `d+u` and `d+v`, where `|u|=|v|=1`.
Their squared chord length is `2-2 cos(alpha)`, where `alpha` is the angle
between the directions. It equals one exactly when `alpha` is plus or minus
60 degrees. Thus the unit edges on a circle stay within a six-rotation orbit,
and each nonexceptional orbit induces a `C6` on that circle.

### Cross-circle edges

Let `|a-b|=1`, `x=a+u`, and `y=b+v`, with `|u|=|v|=1`. Suppose also that
`|x-y|=1` and neither endpoint is the other centre. The two unit circles
centred at `x` and `b` have the known common point `a`; their other possible
common point is `x+b-a`. Hence `y=x+b-a`, so `v=u`. If these two intersection
points coincide, then `x=2a-b`; the circles are tangent at `a`, leaving no
allowed `y`. Conversely, equal directions always give
`|x-y|=|a-b|=1`.

Therefore every non-centre edge between distinct owner circles preserves the
actual unit direction. This proves both completeness and soundness of the
claimed cross-circle edge list for every direction, rather than for a sampled
finite set.

### Exceptional and generic pieces

A point on two owner circles is one of the two equilateral completions of the
corresponding centre edge. Its directions lie in `U`. Thus all multiple-owner
points are contained in

```text
P = union {d+U : d in D},
```

which has exactly 12 distinct triangular-lattice points, including `D`.
Every point outside `P` has a unique owner circle. Its direction belongs to a
unique six-rotation orbit having a representative angle strictly between 0
and 60 degrees.

For one such representative `u`, label the 18 points by
`(i,j) = d_i + omega^j u`. The same-circle argument gives exactly the edges
`(i,j)--(i,j+1)`, while the cross-circle argument gives exactly
`(i,j)--(k,j)`. Different direction orbits have no edges between them. Hence
the generic component is precisely `K3 square C6`. The only centre neighbour
of `(i,j)` is its owner `d_i`.

The exact lattice calculation on `P` gives 24 edges; deleting the three
centres leaves a connected 2-regular nine-vertex graph, hence `C9`. The
lattice colour

```text
colour(a+b*omega) = a+2b mod 3
```

is proper on all six unit steps and pins the three centres to distinct
colours.

On a generic component with centre `d_i` coloured `i`, use

```text
colour(i,j) = i + (-1)^j mod 3.
```

Every centre spoke, cycle edge, and fixed-column `K3` edge is then proper.
For classification, a fixed column must be a derangement of `(0,1,2)` because
it is a triangle and each owner colour is forbidden. There are exactly two
such derangements. Consecutive columns must choose different derangements, so
the choices alternate around the even six-cycle. This yields exactly the two
claimed colourings. Selecting the displayed sign uniformly supplies an
explicit colouring of all continuum components and requires no arbitrary
choice principle.

### Dominating-clique corollary

A planar unit-distance clique has at most three vertices: relative to a fixed
unit edge, the only two common unit neighbours are the equilateral
completions, and they are `sqrt(3)` apart. A dominating three-clique is a unit
equilateral triangle and the graph embeds in its `X`. For a dominating edge,
adjoin either equilateral completion; the graph lies in the two original
owner circles and hence in the enlarged `X`. For a dominating vertex, adjoin
two points forming a unit triangle with it; every original non-centre vertex
lies on its owner circle. Restricting the universal colouring proves all
three cases. The empty graph is immediate.

## Independent computational audit

[`independent_check.py`](independent_check.py) imports no submitted executable
and uses only Python integer and `Fraction` arithmetic in
`Q(sqrt(3)) x Q(sqrt(3))`.

- It pins all eight reviewed source files, reconstructs the exceptional patch
  from the three centres and six unit directions, and recomputes all 66 patch
  distances. It obtains 24 edges and the residual `C9`. Exhausting all
  `3^9 = 19,683` pinned rim assignments gives exactly the lattice colouring.

- It constructs three exact nonexceptional unit directions using half-angle
  parameters `1/7`, `1/3`, and `1/2`; only the last is the submitted
  `(3/5,4/5)` representative. For each, all 435 pairs in the combined
  30-point realization are tested. Each has exactly 78 edges: the same 24
  patch edges, 36 generic internal edges, and 18 centre spokes, with no other
  patch/generic edges.

- Independently exhausting all `2^18 = 262,144` assignments allowed by the
  centre spokes gives exactly the two generic colourings above. Applying all
  six centre-colour permutations passes 936 representative edge checks.
  Definition-level parity controls find two colourings for the analogous
  `K3 square C4` component and none for `K3 square C5`.

- The reconstructed `(3/5,4/5)` realization matches every coordinate, edge,
  label, chord value, and colouring in the 1,493-byte submitted certificate.
  Five mutations affecting distinct certificate fields are rejected. The
  submitted producer and checker were also replayed successfully.

Finite direction checks are only controls. The continuum quantifier is
discharged by the same-circle chord, cross-circle rhombus, and unique-orbit
arguments above. The machine-readable audit is [`result.json`](result.json).
Normal and optimized Python executions produce byte-identical output.

## Reproduction

From the repository root:

```sh
python3 -B hadwiger_nelson_dominating_triangle_review1/independent_check.py \
  --repository . \
  --report hadwiger_nelson_dominating_triangle_review1/result.json
```

The review is deterministic, solver-free, single-process, and took under one
second in the review environment.

## Trust boundary

The universal step retains trust in elementary Euclidean facts about unit
chords and the at-most-two intersections of distinct circles. Exact finite
checks additionally rely on the irrationality of `sqrt(3)`, CPython
integer/`Fraction` semantics, exhaustive-loop execution, faithful JSON
decoding, and SHA-256 collision resistance. There are no external
mathematical data, numerical tolerances, native solvers, or completeness
claims inferred from finite sampling.
