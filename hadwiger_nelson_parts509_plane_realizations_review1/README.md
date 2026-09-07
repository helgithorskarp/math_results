# Independent review of the reduced Parts-509 realization theorem

## Verdict and exact scope

**Verified, high confidence.**  The reviewed contribution is Discovery Net
artifact
`bafkreigqjxw3lhtcfx6q4v3rnm6p5mtqp4h4ksitcshbeixxoifcohlesu`, *Four
normalized drawings exhaust all near-injective planar realizations of reduced
Parts-509*.

Let `S` be the labelled 509-vertex graph with the 2,259 edges pinned by this
directory's checker.  Every map of its vertices to the Euclidean plane that
makes every listed edge have length one and has at least 508 distinct vertex
images is injective.  After translation, rotation, and (when needed)
reflection, its coefficient parameters are exactly

```text
A = 1,       B = +/-sqrt(5),
C = +/-sqrt(33), D = B*C,
E = t*A,     F = t*B,
G = t*C/3,   H = t*D/3,       t^2 = -3.
```

These four choices are precisely the independent sign conjugates of the
supplied Parts drawing in `sqrt(5)` and `sqrt(11)`.  Thus there are exactly four
normalized labelled drawings up to Euclidean isometry, and there is no
realization with exactly 508 images.

This is an intermediate exclusion theorem, not a sub-509 graph and not a new
Hadwiger--Nelson record.  It does not classify realizations with at most 507
images, a graph obtained by changing the source edges, or arbitrary smaller
unit-distance graphs.

If one identifies a nonadjacent pair of vertices in `S`, the quotient would
remain non-four-colourable and have 508 vertices.  The theorem proves that none
of these one-pair quotients has an injective unit-distance realization in the
plane.  The non-four-colourability assertion is an imported, separately
reviewed DRAT-based fact; it is not needed for the geometric classification.

## Independent reconstruction

`independent_check.py` imports none of the claimed verifier or generator.  It
binds the exact input bytes by SHA-256 and then performs the following checks.

1. It enumerates all 2,726 source rhombi from adjacency, confirms that no
   vertex pair has more than two common neighbours, and checks the eight
   rational coordinate columns against every rhombus identity.
2. Using the independent prime 998,244,353 and left-pivot sparse elimination,
   it gives rank 500 to each of the six 500-row rhombus bases and rank 9 to the
   constant column together with the eight coordinate columns.  Hence every
   intact basis has exactly the claimed nine-dimensional scalar kernel.
3. It recomputes, rather than trusts, every obstruction associated with the
   five rows common to all six bases.  Of their ten opposite pairs, four are
   source edges and cannot collapse; each of the other six quotient graphs
   contains a directly reconstructed `K_2,3`.  An injective planar unit-distance
   drawing of `K_2,3` is impossible because two distinct unit circles have at
   most two common points.
4. It reconstructs all 36 coefficient directions of graph edges and verifies
   that the twelve certified linear triads are disjoint and cover them.
5. Crucially, it ignores the claimed 34-prefix orientation cover.  It enumerates
   all 4,096 complete orientation words, performs fresh exact Gauss--Jordan
   reduction over `Q(t)`, and independently checks two forced vertex
   coincidences for every one of 4,094 rejected words.  The two remaining words
   have rank four and give exactly the two reflected frames
   `E=tA, F=tB, G=tC/3, H=tD/3`.
6. It independently expands the 36 unit-direction equations over
   `Q(sqrt(33))[b,y,d,z]`.  The 21 sparse certificate weights give the exact
   consequences

   ```text
   b^2 + 3*y^2 - 5 = 0,  y = 0,  z = 0,  d - sqrt(33)*b = 0.
   ```

7. Finally, direct multiquadratic arithmetic checks injectivity and all
   `4 * 2259 = 9036` unit edges of the four claimed coordinate conjugates.

The geometric bridge in step 2 is elementary but load-bearing.  With at least
508 images there is at most one colliding label pair.  A nondegenerate unit
rhombus has equal diagonal midpoints; the sole collision can invalidate at most
one rhombus equation because of the common-neighbour bound.  Unless that row is
common to all six bases, one full-rank basis remains intact.  The ten common-row
cases are disposed of in step 3.  The 500 independent equations leave a
nine-dimensional scalar kernel, and the independent constant-plus-coordinate
rank shows that every coordinate function is a linear combination of the
constant and eight pinned coefficient columns.

For step 5, a direction triad has
`U_i + s*U_j = r*U_k`, where all three complex values have norm one.  Therefore

```text
U_j/U_i = (-s + epsilon*t)/2,  epsilon in {-1,+1}.
```

This explains why the twelve disjoint triads exhaust exactly 4,096 orientation
words.  Two distinct forced equality pairs reduce the number of images by at
least two, even when the pairs share a vertex.

For the two surviving frames, reflection chooses the positive frame and
rotation makes `A=1`.  The unit directions `(C+t)/6` and `(C-t)/6` make `C`
real and give `C^2=33`.  Writing `B=b+t*y` and `D=d+t*z`, with real variables,
the four exact polynomial consequences above leave only the four stated sign
choices.  Direct checking shows all four exist.

## Reproduction

CPython 3.11 or newer is sufficient; no solver or third-party package is used.

```bash
cd hadwiger_nelson_parts509_plane_realizations_review1
sha256sum -c SHA256SUMS
python3 -B independent_check.py
```

The expected deterministic report is in `verification.json`.  A fresh run on
2026-09-07 returned `all_checks_passed: true`, rejected 4,094 orientation words,
and recovered the two asserted survivors.

The reviewed producer also regenerated its 17,179-byte certificate byte for
byte (SHA-256
`675a5c65e67f9080cdf82649c1ce2f1ca9371e83536c536b0394b04f1c6cef74`).
Its ordinary and `python -O` verifier reports agreed, and all 15 negative
certificate mutations were rejected in both modes.

## Trust boundary and literature status

The independent audit trusts CPython's `Fraction`, JSON, and SHA-256
implementations; the pinned input bytes; and ordinary modular/exact arithmetic
in this small checker.  It reuses the contribution's six basis index sets,
direction witnesses, twelve triads, and 21 polynomial weights as proof
witnesses, but validates their mathematical content independently.  It does
not independently derive the algebraic coordinates from Parts's paper.

For the candidate consequence, non-four-colourability of the 2,259-edge graph
is imported from the separately reviewed artifact
`bafkreicfirhiei7pjthu24jj75oct4kqt4x6f5vap3n5yf2rpphhkb5ige`.  That result
trusts an audited CNF, external DRAT proof bytes, and `drat-trim`; those bytes
were not replayed again in this review.

Parts's primary paper records a 509-vertex, 2,442-edge five-chromatic
unit-distance graph: <https://arxiv.org/abs/2010.12665>.  De Grey and Parts give
the later order-bound comparison: <https://arxiv.org/abs/2303.14714>.  A
targeted arXiv search found no prior classification of the near-injective
labelled realizations of this graph.  This supports novelty but does not prove
priority.
