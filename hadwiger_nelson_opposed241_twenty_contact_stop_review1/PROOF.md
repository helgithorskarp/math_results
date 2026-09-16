# Independent proof audit

## Faithful exact field

Put `a=sqrt(3)`, `b=sqrt(11)`, `c=ab=sqrt(33)`, and

```text
K = Q(c),                  T = (2+2c)/3,
t^2 = T,                   t > 0.
```

The reviewer represents every physical coordinate in the flat ordered basis

```text
1, a, b, c, t, at, bt, ct.
```

This is a basis, not a formal quotient with undetected zero divisors. First,
`a` is not in `K`: the distinct quadratic fields `Q(sqrt(3))` and
`Q(sqrt(33))` cannot coincide. Next, suppose `T` were a square in `K(a)`.
Writing the square root as `u+va`, with `u,v in K`, the `a` coefficient of
its square gives `uv=0`. If `v=0`, then `T` is a square in `K`, impossible
because

```text
Norm_K/Q(T) = -128/9.
```

If `u=0`, then `T/3` is a square in `K`, also impossible because

```text
Norm_K/Q(T/3) = -128/81.
```

Thus adjoining `a` and then `t` has degrees two and two over `K`; the eight
displayed coefficients compare faithfully. The checker implements the
relations `a^2=3`, `b^2=11`, and `t^2=T` directly. Its controls verify all
512 triples of basis monomials for associativity.

The standard real embedding has `c=sqrt(33)>0` and `T>0`, so the stated
positive real root exists. The sign merely fixes which conjugate placement
is under review.

## Source reconstruction and rotation

The hash-pinned 214-point fixture uses only its `1`, `sqrt(33)`, `sqrt(3)`,
and `sqrt(11)` coordinate slots. The reviewer forms its translations by
`-1/2` and its reflected translations by `+1/2`, merges them with the ten
Golomb points, and retains the 241 labels in the hash-pinned source
certificate. Complete exact pair testing gives 991 edges. The source point
and edge streams reproduce the earlier independent review's hashes

```text
70c14dfaec7875038c0f3cc1b9f84f5469143f5227fbd49377340bb46e27d908
02e1fbb4c9f94cc5aca57945657706088e25560d3ca0c00217d0d17d647f55ab
```

The second copy is rotated by the displayed target coefficients. In physical
coordinates the reviewer first multiplies `sin(theta)/sqrt(3)` by `a`, then
checks `cos(theta)^2+sin(theta)^2=1` in the flat field. It also checks that
source point 45 and rotated source point 65 are exactly unit-separated.
Therefore the transformation is a genuine Euclidean rotation realizing the
frozen defining contact; no floating approximation is used.

## Complete strict physical graph

Coefficientwise merging of the two 241-point streams identifies exactly one
point, their common origin, leaving 481 points. The reviewer tests every one
of the `481 choose 2 = 115,440` distances. Exactly 2,002 are one:

```text
991 first-copy edges + 991 second-copy edges + 20 private cross edges.
```

The independently translated target-format point stream and canonical edge
stream have the published hashes

```text
9ac902c4f179dbe1c1a3a2c76dab6225f77c7969041e9feef18d5455082adff6
57296047b72d08a553b2a84b22db353ad5a6af29369314e3bf74fa01ac4a287f
```

This establishes that the reviewed graph is an actual strict plane
unit-distance graph, not merely an abstract 2,002-edge graph.

## Chromatic number

The submitted 481-symbol word is proper on every complete physical edge. A
deterministic direct DSATUR search then starts only from triangle `(0,1,2)`
with colours `(0,1,2)` and finds another proper word. It visits 7,054 nodes,
backtracks 6,279 times, and differs from the submitted word at 304 vertices.
Either witness proves `chi <= 4`.

The first ten source points induce exactly the 18-edge Golomb graph. Any
proper three-colouring assigns three different colours to its first
triangle. Relabel those colours as `0,1,2`; the checker exhausts the remaining
`3^7` assignments and finds none proper. Hence `chi >= 4`, and the complete
481-point graph has chromatic number exactly four.

## Cross-contact strengthening

Traversing only the twenty private cross edges gives thirteen connected
components: seven have `(3 vertices, 2 edges)` and six have `(2 vertices,
1 edge)`. Every component is a path, so the contact graph is a linear forest.
It uses 17 first-copy and 16 second-copy vertices, has maximum degree two,
and an independently computed bipartite maximum matching of size thirteen.

This is descriptive structure of the failed fixed coupling, not an
exclusion theorem for other placements.

