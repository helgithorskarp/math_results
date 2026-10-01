Actual agent **six-heesch-1**, role **researcher**. Exact computer-assisted
author proof; unformalized, independent review pending.

## Family and precise result

Let P be the second17-cell primary square-polyomino seed, zero-based index192
in [Kaplan's17-cell data](https://cs.uwaterloo.ca/~csk/heesch/omino/17omino_2up.txt):

```
(2,0),(3,0),(1,1),(2,1),(3,1),(4,1),
(0,2),(1,2),(2,2),(3,2),(4,2),
(2,3),(3,3),(4,3),(5,3),(3,4),(4,4).
```

For axis a in{0,1}, a band b between0 and the largest occupied coordinate
on that axis, and e in{1,2,3,4}, replace every cell in band b by e+1
consecutive cells along a, and shift every cell strictly beyond b by e.
Retain area greater than19, identify normalized D4-equivalent shapes,
and keep the first representative in lexicographic(a,b,e) loop order.
This gives precisely37 prototypes, indexed0 through36 by [check.py](check.py).

An **integer prefix** uses all normalized D4 orientations, reflections included,
and integer translations of the unit-cell prototype. Each new copy touches
the preceding union, every preceding boundary point is covered, and interiors
of whole copies are disjoint. For negative tests we impose no hole, pinch
or connectedness restriction on any prefix; this relaxes both standard
hole-free and outermost-hole corona conventions.

**Result.** Exactly three of these37 prototypes admit three complete integer
disc coronas: indices2,9,22. All three have explicit integer periodic plane
tilings. Every other prototype lacks even two such relaxed integer coronas,
except index5, which lacks three. In particular, these three are exactly the
integer-grid plane tilers in this finite family. No arbitrary-motion upper
bound for the other34 follows from this classification.

The exceptions and tiling certificates are:

| index |(axis,band,extra)|area|periods|fundamental poses|
|---|---|---:|---|---|
|2|(0,1,2)|21|(6,3),(-4,5)|(3,0,0),(1,0,-4)|
|9|(0,3,1)|22|(4,4),(-7,4)|(4,0,0),(1,-6,-1)|
|22|(1,1,1)|21|(6,-6),(7,7)|(6,0,0),(0,3,-3),(1,-2,-5),(2,-5,-2)|

Pose orientations index the lexicographically sorted normalized D4 images.
Their determinants are42,44,84. Each checked three-corona construction has
cumulative copy counts1,7,19,37. [input.json](input.json) records the literal
levels, periods and fundamental copies.

## Necessary contact exclusion

A contacting pair of integer copies has a relative orientation and translation
in a finite contact inventory: enumerate D4 images in the bounding rectangle
and retain precisely the disjoint full footprints meeting the one-cell
Chebyshev halo of the root. The `Geometry` class independently reconstructs
these inventories and exact affine transport/inverse maps for every prototype.
It checks that the prototypes are discs and have trivial stabilizers.

At an original fixed-copy vertex, an isolated empty90-degree sector must be
filled if all fixed copies are strictly inside a later covered prefix.
Any orthogonal copy filling this sector has a convex90-degree vertex at that
point, and its two incident edges align with the sector rays. Thus its D4
orientation and integer translation are among the reader's complete cell
alignments. A single whole-copy choice is forced; no choice is a contradiction.
Only vertices of the original fixed support are required interior. New vertices
of forced copies are not assumed covered. This is the previously published
[corner bridge](https://github.com/helgithorskarp/math_results/blob/main/heesch_polyomino_corner_obstruction/README.md),
applied to each literal pair, not a global phase-rigidity assumption.

The [compact certificate](certificate.json) supplies2240 pair contradictions.
The reader checks every forced step and terminal empty sector independently.
Reversing the pair and applying the inverse root isometry yields the reciprocal
exclusion of the same unordered geometric support. Let B be this reciprocal
set for the prototype. Every contacting pair of copies that are both strictly
covered must avoid B. Exclusions omitted by an incomplete exploratory atlas
weaken the necessary model; atlas completeness is unnecessary for a negative.

## Complete integer cover reconstruction

Fix a finite integer prefix X. Any next integer copy has a full footprint
disjoint from X and covers at least one halo cell of X. Transporting the entire
allowed relative-contact inventory from every fixed copy lists all such poses.
Reject full overlap with X and any forbidden contact with fixed copies.
Cell incidence gives full-copy overlap conflicts; halo incidence gives forbidden
contact conflicts between new copies. These are exactly the implemented
necessary constraints, including footprint portions outside the required halo.

The `Cover` reader branches on the first uncovered halo cell. Every complete
surround chooses a listed owner of that cell. Whole-copy conflicts remove only
impossible co-selections. After the halo is covered, no additional disjoint
copy can touch X, since every such copy would occupy a halo cell already covered.
Consequently this enumeration is complete. Memoization stores only fully
exhausted failed states. Guards raise an exception on incomplete work.

For33 non-exceptional prototypes, the root cover enumeration with B has no
solution. A hypothetical second corona would strictly cover both the root and
all first-corona copies, so every contact among them must avoid B. This rules
out that second corona, even under the relaxed topology convention.

For index5, the complete necessary first-surround inventory has exactly one
entry. Fix that entry and enumerate its necessary second surrounds with B;
there are none. A hypothetical third corona would strictly cover all copies
through the second, so these exclusions apply to that second-surround search.
This rules out three integer coronas. No selected-prefix failure or native
solver negative is substituted for either complete inventory.

An integer-grid plane tiling would supply each finite contact neighborhood and
cover it with the next contact neighborhood. These finite sets satisfy the
same relaxed halo/whole-copy/contact conditions, with no disc assumption.
They contradict the preceding depth2/3 exclusions. Thus the other34 prototypes
have no integer-grid plane tiling.

## Plane tiling and positive coronas

For periods u,v of positive determinant d, define the residue of q=(x,y) by

```
((v_y*x-v_x*y) mod d, (-u_y*x+u_x*y) mod d).
```

Two cells have the same residue exactly when their difference is in
Z u+Z v. The reader independently enumerates integer representatives in the
half-open fundamental parallelogram and checks its d residue classes.
The fundamental copies have exactly d distinct residues. Their lattice
translates therefore cover every integer cell exactly once and form a plane
tiling. Direct signed-permutation cell checks also verify every literal
corona: full overlap freedom, actual preceding-prefix contact, complete halo
coverage,4-connectivity, no alternating pinch and no bounded complementary
component. Every one of the37 positive copies lies in its claimed lattice orbit.

## Scope, prior work and trust

The primary seed and its grid Heesch value3 are prior art in
[Kaplan's paper](https://arxiv.org/abs/2105.09438) and
[author dataset](https://cs.uwaterloo.ca/~csk/heesch/). The separate
[P192 unrestricted exact-three proof](../p192-exact-three/proof.md) is credited
context and the source of the byte-pinned reusable integer reader; its motion
reduction and numeric atlas are not applied to the stretched prototypes.
This bounded deformation-family classification is useful for avoiding a
construction search whose only three-corona integer examples are tilers.
It makes no claim of historical priority, a new Heesch record, or an
unrestricted finite-five construction.

The trust boundary is written unformalized orthogonal-sector/completeness
arguments and CPython exact arithmetic. A solver selected small candidate
domains during discovery, but complete independent integer enumeration and
literal corner replay supply the final negatives. The source includes no
raw search dump, solver proof corpus or external data download. Same-author
algorithm independence does not establish independent peer review.
