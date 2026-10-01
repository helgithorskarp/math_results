# P17 interior contacts are integral

**six-heesch-1, researcher.** Author-proved finite reduction with exact
computer-assisted certificates; unformalized. This does not construct a
fourth or fifth corona and does not claim a new Heesch record.

P17 is the closed-disc union of the seventeen unit cells in [input.json](input.json),
normalized to [0,6] x [0,5]. It is entry 43, zero-based, in
[Kaplan's primary 17-cell file](https://cs.uwaterloo.ca/~csk/heesch/omino/17omino_2up.txt),
reported Hc=Hh=3. The older prose label "record seed" in our finite-contact
artifact was incorrect; the input geometry was unchanged. Its historical
JSON field record_seed_17 is retained for compatibility. Here the distinction
between the published integer-grid census and unrestricted-motion proofs
is explicit. The [prior all-motion frontier](../../../heesch_polyomino_four_corona_frontier/proof.md)
gives 3<=Hc<=Hh<=4 and leaves fourth-corona existence unresolved.

Use the strict convention X_(k-1) subset int(X_k), every new copy touching
the previous cumulative prefix, with disjoint tile interiors. All rigid
motions and reflections are initially allowed. Hc requires every prefix
to be a disc; Hh permits holes and pinches only in the last prefix.
The interior-integrality theorem below uses no prefix topology condition.

## The finite phase obstruction

The [finite contact-domain reduction](../finite-contact-types/proof.md),
source commit 4f67530506370b6a36dc916b0c117df990aeb816,
graph bafkreieojswuuzp65j7kw3clv7xbycjeizelt5xjbwwi2yiyypp5cfaahm,
establishes these elementary bridges, with its prior results attributed:

1. Filled 90/180/270-degree sector stars lock all copies contacting a strictly
   surrounded tile to its square axes, including vertex-only contacts.
2. Write copies as normalized D4 orientations O+t and define
   sigma(x)=x at integers, floor(x)+1/2 otherwise. Every physical contact
   has a half-grid type (O,sigma(tx),sigma(ty)). A product of increasing,
   unit-periodic coordinate homeomorphisms preserves every pair's type.
3. The first-root support F of a half-grid contact B is exactly tested by
   forcing B in a complete half-grid first-surround formula. Real witnesses
   can first normalize B to its representative homeomorphically, then use
   the unconstrained half-phase collapse, which fixes B and the root collar.
4. An unconstrained surround of a literal half-grid fixed pair is exactly
   decided on the quarter grid, even if their union has holes or pinches.
   This follows from scaling by two and preserving all integer-vertex stars
   under the earlier collapse theorem. It is not a later restricted-domain
   mesh assertion.

The D4 images are sorted lexicographically by normalized integer cell tuples.
The root has orientation index 3. Store type translations doubled as integers.
P17 has no nontrivial root stabilizer, which is checked by the reader.

**Certified census.** There are 704 contact types, 352 with a nonintegral relative
coordinate. Exactly eleven of those floating types occur in a first relaxed
surround of the root. Their complete list is:

    (0,-10,-3), (1,-3,-10), (2,7,-8), (3,7,-6), (4,-10,1),
    (4,-1,-12), (5,-1,-10), (6,-10,-1), (6,7,-12),
    (7,5,-10), (7,7,-10).

The remaining 341 types have entailed negative units in floating-support.rup;
every listed supported type occurs in a directly checked first-surround
witness. A contacting pair whose two copies are both surrounded must lie
in this support in both directions. Reciprocal transport leaves just

    B = (orientation 1, translation(-3/2,-5)),

which is self-reciprocal. All other floating types fail a directed support.

This exceptional pair has no surround. In the quarter-pixel scale, it is
enough to demand the three exterior halo pixels with lower corners

    (14,-4), (16,0), (18,-12).

Every strict quarter-grid pair surround must cover these pixels. Enumerate
all D4 copies on that mesh which cover at least one of the three and do not
overlap either fixed tile. There are 156 candidates. The complete formula has
156 variables and 10,396 clauses: every full-footprint overlapping pair is
forbidden, including overlap outside the three demanded pixels, and every
demanded pixel has an owner clause. exceptional-pair.rup has two checked
additions, -46 and the empty clause. Therefore even this necessary cover is
impossible. The quarter-grid bridge excludes every real-motion pair surround.
The smaller target is a sufficient obstruction, not an assumed search cutoff.

## Interior lattice rigidity

**Theorem.** In any finite packing of congruent P17 copies, if two contacting
copies A,B are both strictly inside the packing union, their relative rigid
motion has a D4 linear part and an integer translation in A's root frame.

*Proof.* The filled-star argument aligns the two copies and every copy touching
either of them. Delete copies touching neither. Because the original packing
is finite, these deleted compact copies have positive distance from A union B;
a sufficiently small covered collar therefore survives. Apply a rigid motion
to make A the root, and then an increasing periodic product homeomorphism to
normalize B to its half-grid type. Contact, nonoverlap and both collars survive.

Each fixed copy is surrounded, so both directed types belong to F. If the
relative translation is nonintegral, sigma has a half-integral coordinate.
The certified census leaves only the exceptional self-reciprocal type. Its
joint surround is prohibited by the quarter-grid three-pixel certificate.
Thus the translation is integral. D4 alignment already followed from the
filled sector stars. □

The assertion concerns the actual relative translation, not just an equivalent
integral placement: sigma(x) is integral if and only if x is integral.

**Corollary.** In every strict H-corona packing, after the root is fixed, all
copies in X_(H-1) lie on the integer square grid. In particular two complete
coronas already force the entire first prefix to be integral.

*Proof.* Every tile at level at most H-1 is strictly inside X_H. Any contact
between such tiles is integral by the theorem. Every new tile has a contact
chain down to the root, staying in these levels. Transport along that chain
composes only D4 matrices and integer translations. Therefore its absolute
root-frame orientation is D4 and its translation is integral. □

This strengthens the campaign's earlier
[three-corona integrality theorem](../../../heesch_polyomino_third_prefix_reduction/proof.md),
which placed only X_(H-2) on the root grid. That theorem is prior art, not a
premise of the present independent phase census. No equality of unrestricted
and integer-grid Heesch numbers follows merely from the new corollary: the
last corona can still have fractional translations.

Every plane tiling is similarly integral after root normalization. Bounded
tile diameter and positive area imply local finiteness. Any contacting pair
has a finite surround obtained by retaining the copies touching it; omitted
nearby copies have positive distance from that compact pair. The theorem makes
every contact integral, and a finite segment connects any two tiles through
a connected contact graph. Integral translations propagate from the root.
This is a conditional lattice-rigidity statement, not a plane-tiling witness.

## Uniform half-grid decision for relaxed coronas

**Corollary.** For every H>=1, an unrestricted Hh-admissible H-corona packing
of P17 exists if and only if there is one whose prefixes through H-1 are
integer and whose last-layer translations lie in (1/2)Z^2. Hence a single
mesh2 suffices for all corona depths under this relaxed final convention.

*Proof.* The preceding corollary fixes every earlier copy on the integer grid.
Apply the earlier half-phase collapse only to final-layer translations, which
is the same as applying it to every translation because the integral ones are
fixed. Separation inequalities and root contacts survive. At every integer
vertex of every constituent cell of X_(H-1), all four filled quadrant incidences
are preserved; the collapsed packing covers a half-unit collar of the whole
fixed prefix. Every final copy continues to touch that prefix, and strict
containment persists. Earlier prefixes and their disc topology are unchanged.
New holes or pinches in the final union are permitted by Hh. The reverse
direction is immediate because these mesh motions are real motions. □

The same collapse is not claimed to preserve an Hc final disc. It can add
contacts and change final topology, just as in the prior first-surround theorem.
The Hc interior-integrality corollary itself remains valid.

## Certificates, limits and attribution

check.py reconstructs the complete first half-grid formula and independently
audits its candidate pool by bounded exact unit-rectangle comparisons. It
checks every positive floating support by full rectangle geometry, pixel
halos and a separate variable-width face arrangement. The conditional negative
proofs have 592 additions; they prove all 341 negative support units against
the base formula, with previously proved clauses retained. Glucose deletion
records are discarded soundly, since retaining proved clauses strengthens unit
propagation. Every retained addition is checked; RAT-only steps are rejected.

The exceptional three-pixel pool has its own independent bounded-rectangle
audit. Pair collisions test the entire footprints. No arbitrary-motion
negative statement comes from solver status, a timeout, UNKNOWN or a truncated
search. Discovery's first full pair formula had 1,526,084 clauses and peaked
at 443,328KiB; the published proof uses only the compact necessary subset.
The optional generator keeps conflict, candidate and proof-size guards and
never treats a guard as exclusion. No resource settings were increased.

The input came from the primary source and is preserved literally. The
certificate/checker uses byte-pinned code from the preceding finite-contact
artifact. Shared isometry and CNF primitives, the written geometric bridges,
and the unformalized universal arguments remain trust boundaries. The audits
are not independent mathematical peer review. No historical priority claim
or record-height claim is made.
