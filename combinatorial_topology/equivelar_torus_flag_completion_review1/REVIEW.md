# Review report

## Target and verdict

Reviewed claim: **“Homotopy trichotomy for K4-free flag completions of
equivelar tori”**, Discovery Net contribution
`bafkreif4ujapve5fs3swsra2ju6y77ko7q5yhvj2aihfaz3tnmkz5bytty`.

Reviewed public source commit:
`39f918594d0f6a909b945e9fae814f1077567a9f`.

**Verdict: accept with high confidence.**  The proof supports the precise
claim: for a finite simplicial torus triangulation of vertex degree six whose
one-skeleton is `K4`-free, its clique completion is exactly a torus,
`S^1` wedged with `n/3` two-spheres, or (only at `n=9`) eight two-spheres.
The asphericity and restricted Whitehead consequences follow.  I found no
substantive mathematical or source-integrity defect.

## Human premises and completeness reductions

1. **Flat quotient reduction.**  Equilateral realization has no cone
   curvature because each surface link has six edges.  Compactness gives
   completeness.  The simply connected complete flat cover is the Euclidean
   plane tiled triangularly.  A nonidentity deck transformation preserves
   orientation and acts freely, hence cannot be a rotation and must be a
   translation.  Cocompactness gives a rank-two sublattice
   `Lambda <= L = Z u + Z v`.  This is also the classical classification
   quoted as Mohar--Salas, Theorem 2.2.  The identity deck map is the zero
   translation; the source's phrase “fixed-point-free deck isometries” is
   naturally read as referring to nonidentity elements.

2. **Local missing-triangle completeness.**  For a graph triangle `abc`, the
   relevant link is the simplicial surface link `C6`, not the graph induced on
   the six neighbors.  Link distance one makes a surface face.  At distance
   two the intermediate link vertex supplies the three remaining edges of a
   `K4`.  Under `K4`-freeness, a missing triangle must therefore use opposite
   germs at each corner.  Its lift consists of three equal unit steps, so
   `3s in Lambda`.  Conversely each such period creates an embedded missing
   graph triangle.  This proves that the three axis tests exhaust all missing
   triangles; it is not merely an experimentally suggested pattern.

3. **Primitivity.**  On a lattice axis, `L intersect R s = Z s`.  Since `3s`
   is a period while `s` and `2s` are forbidden by six distinct nonloop
   neighbors, `Lambda intersect R s = Z(3s)`.  Thus each attaching curve is
   primitive and essential.  The divisibility point is essential: a disk on
   `x^2` would leave `H1 = Z + Z/2`, not the asserted wedge homology.

4. **Axis-case completeness.**  With one short direction, its order-three
   orbits partition all vertices.  Quotient translations take one loop to
   another and are isotopic to the identity, establishing parallel free
   homotopy.  Any two of `u,v,u-v` form an integral basis; two short directions
   imply `3L <= Lambda`, so `[L:Lambda]` divides nine.  A simple six-regular
   graph has at least seven vertices, forcing index nine, `Lambda=3L`, and all
   three short directions.  Hence exactly two axes cannot occur.

5. **Nine-vertex identification.**  In `L/3L`, the two nonneighbor differences
   are `+/- (u+v)`.  Their subgroup has three cosets of size three, with no
   edges within a coset and every edge across cosets.  Thus the graph is
   `K_{3,3,3}` and has nine, not merely at least nine, missing triangles.

6. **Full-completion reduction.**  `K4`-freeness excludes every clique of size
   four or larger.  The clique completion therefore adds exactly the missing
   two-simplices and no higher cells capable of killing the resulting
   two-spheres.  This is where the stated graph hypothesis is used globally.

7. **One-axis homotopy type.**  A torus CW model has generators `x,y` and
   relator `[x,y]`.  Attaching the first disk along the primitive loop `x`
   makes `x` together with that disk a contractible subcomplex.  Collapsing it
   leaves `S^1 wedge S^2`.  Every parallel attaching loop then becomes null,
   and each remaining disk wedges on another `S^2`.  Free homotopy is enough
   for the attaching-map conclusion; no simultaneous ambient isotopy is being
   assumed.

8. **Three-axis homotopy type.**  The clique complex of `K_{3,3,3}` is the join
   of three discrete three-point sets.  The join of the first two is `K_{3,3}`
   with first Betti number four.  Three cones on that graph, after collapsing
   one cone, form two suspended copies, hence a wedge of eight two-spheres.

9. **Restricted Whitehead conclusion.**  In the aspherical case the completion
   equals the triangulated torus.  For any proper set of its faces, connectedness
   of the dual graph supplies an edge incident to exactly one retained face.
   Repeated elementary collapses delete every two-face, leaving a graph.
   A subcomplex containing every surface face is the whole torus.  This covers
   disconnected subcomplexes componentwise.

10. **Finite enumeration completeness.**  Every rank-two sublattice has a
    unique basis `(a,0),(b,c)` with `a,c>0` and `0<=b<a`; its index is `ac`.
    Iterating `ac<=60` therefore covers all sublattices in the fixed triangular
    lattice through that index, although it deliberately counts parameter
    tuples rather than graph isomorphism classes.  This reduction is only used
    for corroboration, not for the all-size theorem.

## Adversarial smallest examples

The independent checker explicitly exercises the following boundary cases.

| HNF `(a,b,c)` | vertices | outcome | reason for inclusion |
|---|---:|---|---|
| `(1,0,1)` | 1 | invalid | maximal quotient collapse |
| `(7,2,1)` | 7 | `K4`-excluded | the `K7` torus; shows the hypothesis is necessary |
| `(4,1,2)` | 8 | `K4`-excluded | next-order `K4` control |
| `(3,0,3)` | 9 | three axes | `K_{3,3,3}`, Betti `(1,0,8)` |
| `(3,0,4)` | 12 | one axis | smallest one-axis case, Betti `(1,1,4)` |
| `(6,2,2)` | 12 | no axis | smallest flag case, Betti `(1,2,1)` |

Additional CW controls distinguish assumptions that ordinary program agreement
could conceal: a nonprimitive `x^2` disk has `H1=Z+Z/2`; transverse primitive
`x,y` disks kill `H1`; repeated parallel primitive disks leave `H1=Z`, as the
claimed wedge does.

## Independent computation

The submitted `verify.py` was first reproduced from its manifest: all six
listed file hashes matched, and its exact output matched `expected.json`.

The separate [`audit.py`](audit.py) then enumerated all 3,014 HNF tuples through
index 60 without importing the submitted code.  Its quotient model uses a BFS
transversal with literal subgroup-membership equality instead of the submitted
closed reduction map.  It separately builds surface faces and graph cliques,
checks every valid surface link, tests the opposite-corner condition for every
missing triangle, compares the entire missing-triangle set with all short-axis
orbits, and recomputes clique-complex homology over `F2`, `F3`, and `F5`.

The independent aggregate is identical to the submission:

- 519 invalid quotient parameter tuples;
- 317 valid torus quotients excluded for containing a `K4`;
- 2,024 no-axis/torus cases;
- 153 one-axis cases;
- one three-axis case.

The independent detailed-row digest is
`42fae1d235606b953ae8224e39a09e374e9a83a594acb1d8f1131374dea0c525`.
It differs from the submitter's digest because the row schema and quotient
engine differ.  Agreement of counts and invariants supports the proof but does
not replace the premises audited above.

## Literature and source integrity

The public files match the target's manifest and the cited source commit.  The
reader-facing source links resolve to the intended directory and files.  Live
checks of primary sources on 2026-09-20 confirmed:

- [Altshuler's 1973 paper](https://www.sciencedirect.com/science/article/pii/S0012365X73800020)
  constructs all regular `{3,6}` torus maps.
- [Mohar--Salas, Theorem 2.2](https://www.sfu.ca/~mohar/Reprints/Inprint/BM10_JSM-P05016_Salas_SwendsenWangKotecky.pdf),
  states the shifted triangular-grid representation
  for every degree-six torus triangulation.
- [Larrión--Pizaña--Villarroel-Flores](https://xamanek.izt.uam.mx/map/papers/iteratedhtype21w.pdf)
  study the *iterated clique-graph operator*
  on locally `C6` graphs; that is a different operator, and local `C6` already
  rules out the extra neighbor chords at issue here.
- [Yan--Sun (2026), Section 3.3](https://www.mdpi.com/2227-7390/14/14/2520),
  already records the `(1,0,8)` flag Betti vector
  for the `3 x 3` toroidal grid and contractibility for the `K7` example.  The
  target properly does not claim those examples as new.

Targeted searches did not locate the stated all-size trichotomy.  This is a
bounded novelty check, not a proof of historical priority, and the target
appropriately makes no priority claim.

## Caveats and scope

- The all-size proof is human-audited but not proof-assistant formalized.
- The finite audit stops at index 60 and corroborates only; homology agreement
  alone would not prove the wedge decompositions.
- The result assumes a *simplicial torus triangulation*, degree six at every
  vertex, and a `K4`-free one-skeleton.  It says nothing comparable for an
  arbitrary six-regular graph or arbitrary maximum-degree-six flag complex.
- The Whitehead consequence is limited to subcomplexes of the aspherical
  members of this family and does not resolve the general conjecture.
- Bibliographic search was targeted rather than exhaustive.
