# Pointwise conjugation of the native T721 spindle needs at least 593 points

The fixed 1,441-point native T721 spindle meets **593 distinct orbits** under
the eight automorphisms of `K = Q(sqrt(2),sqrt(3),sqrt(5))`. Consequently every
map that independently applies one of these automorphisms to both coordinates
of each source point has at least 593 distinct images. In particular, no
edge-preserving map in this class meets the 508-point target.

This is a small exact construction preflight, not a smaller five-chromatic
graph or a global vertex bound. The calculation rejects the cap before any
edge-compatibility census or chromatic query. The previously reviewed
[fixed-host deletion bound through 573](../hadwiger_nelson_t721_weighted_cover/README.md)
is separate: conjugate images may lie outside that host.

## Fixed point set and map class

Let `T` be the 721 exact coordinate rows of
[Heule's native T721.vtx](https://github.com/marijnheule/CNP-SAT/blob/master/vtx/T721.vtx).
The upstream revision is `bb414955a6ef5f49f7df2b245b1e778aa67c068a`;
the input has 40,529 bytes and SHA-256
`a63fa371d7cf42faa8a3b26d56df81b0c25c1f149d6791dd25c7c356abe1b7c6`.
In complex notation define

```
r = (7+i sqrt(15))/8,
P = T union {-1+r(z+1): z in T}.
```

Use the displayed Cartesian coordinates, with no preliminary coordinate
change. They lie in `K`, and exact collision merging gives 1,441 points.
For each `p=(x,y)` independently choose `sigma_p in Gal(K/Q)` and put

```
f(p) = (sigma_p(x), sigma_p(y)).
```

The same automorphism acts on both coordinates of a point. Choices may differ
between points. Every source point is retained. A common Euclidean isometry
after the map leaves the image count unchanged. Source deletions, preliminary
coordinate changes, arbitrary translations, new points not obtained by this
rule, and other deformations are outside the result. The retained unit edges
need not be tested: the cardinality bound holds even without that constraint.

## Orbit proof

The squareclasses 2, 3 and 5 are independent over the rationals. Thus `K` has
degree eight, with basis

```
1, sqrt(2), sqrt(3), sqrt(6), sqrt(5), sqrt(10), sqrt(15), sqrt(30).
```

Its automorphisms are the independent sign choices on `sqrt(2),sqrt(3),sqrt(5)`.
Their signs on products, including `sqrt(6)` and `sqrt(30)`, are determined.
Use denominator 96 and represent a point by eight integer x coefficients
followed by eight integer y coefficients. Basis independence makes equality
of these integer tuples exactly equality of physical points.

Form the invariant finite set

```
C = {sigma(p) : p in P, sigma in Gal(K/Q)}.
```

Exact enumeration gives 3,223 distinct points in C. Under the sign choices in
the order produced by `product((1,-1), repeat=3)`, the numbers of fixed points
are

```
3223, 1075, 47, 139, 163, 55, 11, 31.
```

Burnside's formula gives `(3223+1075+47+139+163+55+11+31)/8 = 593` orbits.
Every orbit of C meets P by construction. Images of source points in different
orbits cannot coincide. Therefore `|f(P)| >= 593`. Without the unit-edge
requirement this is attained by choosing one representative per orbit.
Attainment by an edge-preserving map is **not** claimed.

The other computation partitions P directly by the least of its eight
conjugates. The source occupies one point in 165 orbits, two points in 218
orbits, and four points in 210 orbits. These give both
`165+218+210=593` and `165+2*218+4*210=1441`.

## Reproduction and trust

Use CPython 3.11 or newer and a complete repository checkout. The only external
input is the hash-pinned coordinate file; the fetcher is in the earlier source
package. From the repository root:

```sh
python3 -B hadwiger_nelson_t721_weighted_cover/fetch_input.py /tmp/T721.vtx
python3 -B hadwiger_nelson_t721_galois_orbit_gate/verify.py --input /tmp/T721.vtx
python3 -O -B hadwiger_nelson_t721_galois_orbit_gate/verify.py --input /tmp/T721.vtx
python3 -B hadwiger_nelson_t721_galois_orbit_gate/produce.py \
  --input /tmp/T721.vtx --output /tmp/t721-orbit-expected.json
```

The final verifier reports `verified: true`, `orbit_count: 593`,
`closure_points: 3223`, and `cap_excluded: true`. The producer regenerates
[expected.json](expected.json). Coordinate and closure hashes use compact
JSON with separators `(',', ':')`, with lexicographically sorted point lists
and no trailing newline in the hash input.

The producer reuses the pinned dense-coordinate AST parser and conjugate
inversion from `native.py` in the earlier package. The checker reuses that
package's separate recursive-descent parser and sparse-radical arithmetic
from `exact.py`. Their complete ordered source-point streams have identical canonical
hashes, as do the complete generated conjugate sets. The new producer
uses direct orbit partitioning; the checker uses the invariant-set fixed-point
count. Neither runs the inherited edge enumeration or colouring check.

Five small fixtures independently compare the orbit bound with exhaustive
pointwise assignments. They include a genuine conjugate collision, rational
points that cannot merge, inconsistent coordinate signs, and the product-sign
constraint on `sqrt(6)`. Three false counts are rejected. Normal and optimized
Python results agree. The verifier took approximately two seconds in the
recorded environment; this is an observation, not a runtime guarantee.

The trust boundary is the pinned coordinate file and two reused exact parsers,
the explicit field and orbit argument, integer/rational arithmetic, these
short programs, and ordinary execution integrity. This is author validation,
not an independent-author review or a formal proof. Source non-four-colourability
is motivation only and is neither assumed nor re-certified by this bound.
The source geometry is imported; no new all-pairs unit-distance census or
proper-five-colouring check is claimed.

## Construction boundary

The source-acquisition lead resolved to a known exact native file with an
already closed deletion space. This distinct conjugate-compression gate also
fails. No compatibility SAT instance, larger support, different origin,
partial-source variant or new host was generated. The mechanism is retired at
the 508-point cap. Other operations remain unclassified.

The unrestricted published benchmark remains the
[Parts 509-point construction](https://arxiv.org/abs/2010.12665).
This package adds a source-specific rejection test and makes no record claim.
