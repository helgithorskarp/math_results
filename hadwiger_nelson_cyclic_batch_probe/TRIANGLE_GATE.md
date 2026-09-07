# Complete fresh-triangle insertion gate

Let `S` be the published 509-point nine-move seed, `V` the original Parts
point set, and `C(V)` the set of all planar points having at least two unit
neighbours in `V`, including points of `V` when applicable. Consider a unit
equilateral triangle `A` disjoint from `S`, with every vertex having at least
two unit neighbours in `S` and at least one vertex outside `C(V)`.

**Claim.** For every four-element subset `D` of `S`, the strict unit-distance
graph on `(S minus D) union A` is four-colourable. In particular none of these
508-point mutations meets the target.

All original and seed coordinates lie in
`K^2`, where `K=Q(sqrt(3),sqrt(5),sqrt(11))` in the positive real embedding.
A point with three distinct `K`-valued unit neighbours is their circumcentre
and belongs to `K^2`: subtracting the three circle equations gives an
invertible linear system over `K`. The three centres cannot be collinear,
since a circle meets a line in at most two points. Consequently an enumerated
point outside `K^2` has exactly its two generating `K`-valued unit neighbours
and occurs under only one signed centre-pair label. A mixed `K`/non-`K`
triangle is impossible under the two-seed-neighbour hypothesis: its non-`K`
vertex would have a third distinct `K`-valued neighbour.

For distinct seed centres `a,b` at squared distance `s`, their common unit
neighbours are

```text
(a+b)/2 +/- sqrt(1/s - 1/4) perpendicular(b-a).
```

There are no intersections for `s>4`, one midpoint for `s=4`, and two for
`0<s<4`. All pairs are enumerated. Since `b-a` is nonzero and `K`-valued, an
intersection lies in `K^2` exactly when `1/s-1/4` is a square in `K`.

The recursive square-root algorithm is complete. In a tower step
`L(sqrt(p))/L`, write the argument as `a+b sqrt(p)` and a possible root as
`u+v sqrt(p)`. If `b=0`, either `u=0` or `v=0`, giving the two tested
subcases. Otherwise `u,v` are nonzero and
`u^2=(a +/- sqrt(a^2-p b^2))/2`, with `v=b/(2u)`. Recursively testing both
signs and confirming a candidate by exact squaring covers all roots. The
base case is rational numerator/denominator integer-square testing. The
primes `3,5,11` give genuine quadratic steps.

The original pair census produces 4372 `K`-valued points. The seed census
produces 4377, including all 509 seed points, so there are 3868 external
points. Exactly 104 lie outside the original census. Exact unit-pair tests
on the external points give 126 unit triangles involving one of these 104.
The unit-pair routine uses a modular homomorphism only to reject impossible
pairs; every surviving equality is checked in the eight-dimensional rational
basis. All denominators are invertible in the modular image, or the run
fails. No floating-point equality enters this enumeration.

In the non-`K` case, a point lies outside `C(V)` exactly when one of its two
generating seed centres is among the nine moved points. Otherwise both
centres belong to `V`, so it lies in `C(V)`. Conversely, a moved generating
centre together with two unit neighbours in `V` would give three distinct
`K`-valued neighbours, which is impossible. The complete seed pair census
gives 135630 signed non-`K` points, of which 4574 are fresh in this sense.

Every physical coordinate is enclosed by outward integer interval arithmetic
with denominator `T=2^100`. Basis radicals use integer square roots of
`d T^2`; interval addition, subtraction, multiplication, division by a
positive interval and square root are rounded outwards. The squared centre
distance is separated from both zero and four; exact tangencies are handled
separately. An unseparated case fails the run. The same circle formula then
encloses both physical intersections. The maximum enclosure width is
`2545/T`. A midpoint representative is rounded to denominator `B=2^32`, and
the program directly checks against both interval endpoints that each
coordinate differs from the physical point by at most `2/B`.

For a true unit pair, each displacement coordinate therefore changes by at
most `4/B`. Its squared integer-grid distance differs from `B^2` by at most
`16B+32`, strictly less than `M=2^40`. Thus the annulus
`[B^2-M,B^2+M]` conservatively contains every true unit pair. Cells have
integer width `H=2^28`; their minimum/maximum squared-distance bounds give
260 possible offsets. Offsets outside `[-18,18]^2` have minimum distance
exceeding the annulus. For each fresh point, enumerate its annulus neighbours
and test every pair of those neighbours against the same annulus. Every
true fresh triangle is included among the resulting 1468 candidates. False
candidates are allowed: requiring all three abstract edges makes extending
a four-colouring harder and is safe for this negative result.

For each seed deletion `u`, directly checked colourings of `S-u` determine
the available-colour lists at the three new vertices. The three vertices
can be coloured as a clique precisely when their lists have distinct
representatives. The public verifier checks this by enumerating distinct
first and second colours and looking for a remaining third colour. This
is independent of the Hall-condition formula used to find the certificate.
Both were compared with direct colour enumeration on all list triples.

For a triangle `A`, define `Uhat(A)` to be the seed vertices for which no
stored colouring extends to `(S-u) union A`. If `(S-D) union A` were not
four-colourable, then `D` would be a subset of `Uhat(A)`: any extending
witness for `u` in `D` restricts after the other seed deletions. It therefore
suffices to prove `|Uhat(A)|<=3` for every triangle.

The compact public certificate consists of 300 additional seed-deletion
colourings, supplementing the sibling certificate's 509 rows. Every row is
checked on all retained seed edges. The regenerated geometry has 843
canonical triples of seed-neighbour lists. Replaying the rows gives the
following declaration counts:

| `|Uhat(A)|` | Exact `K` triangles | Conservative non-`K` candidates |
|---:|---:|---:|
| 0 | 108 | 1468 |
| 1 | 3 | 0 |
| 2 | 8 | 0 |
| 3 | 7 | 0 |

This proves the claim without any solver verdict or imported completion
census as a premise. The public command regenerates both full pair censuses,
the triangle screen and the colouring checks:

```sh
python3 hadwiger_nelson_cyclic_batch_probe/gate.py --output /tmp/hn-triangle-gate
```

Trust is in the stated unformalized reduction, the exact Python algorithms,
the imported field arithmetic, and the sibling coordinate/colouring inputs
which are reconstructed and checked. Runs with and without Python
optimization agree. No external review or formalization is claimed.

The hypotheses matter: triangles wholly contained in `C(V)`, triangles with
a vertex having fewer than two seed neighbours, other joint batches, and
arbitrary subgraphs of the 769-point joint host are not classified here. The
separate 543-point construction has its own exact geometry, DRAT and deletion
certificates, described in the README; it does not provide a lower bound for
every subgraph of that host.
