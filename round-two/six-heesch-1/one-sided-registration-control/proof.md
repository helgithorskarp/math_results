# A one-sided registration control with exact Heesch number one

Actual author **six-heesch-1**, role **researcher**. This is an unformalized
written argument with exact solver-free certificates. Independent review is
pending. It is a calibration/exclusion for a literal 21-cell prototype, not a
record improvement or historical-priority claim.

The prototype P is the closed union of the unit cells in [input.json](input.json).
It is an asymmetric topological disc. Search provenance is selected paired-edit
case 330, an independently normalized two-cell edit of the known plane parent 22
in the [single-band source](../single-band-filter/proof.md). The selected 1,200
window is truncated; this proof neither enumerates it nor classifies other
members. Only P's literal cells are mathematical input here.

Use strict nesting X_(k-1) subset int(X_k), disjoint whole-copy interiors, and
every new copy touching the preceding cumulative prefix. Hc requires all
prefixes to be discs. Hh allows holes/pinches in the last prefix, with earlier
prefixes discs. Plane tilers have infinite Heesch number. All Euclidean rigid
motions and reflections are initially permitted.

**Certified claim.** Every copy in every admissible corona patch of P has a D4
linear part and an integer translation after fixing the root. The literal tile
has unrestricted Hc=Hh=1 and does not tile the plane.

## 1. The one-sided registration implication

This implication is an elementary corollary of the already published
[finite-contact reduction](../finite-contact-types/proof.md) and the
[first-surround half-grid theorem](../../../heesch_polyomino_halfgrid/proof.md).
Their angular locking and phase-collapse arguments are attributed dependencies,
not a new general theorem here. The prior half-grid theorem also has an
[independent review](../../../heesch_polyomino_halfgrid_review1/README.md).
That review does not assess the new 21-cell certificate in this directory.

A covered copy A in a finite packing has a finite surround consisting of the
copies touching it: deleting the others preserves a sufficiently small collar,
since every deleted compact copy has positive distance from A. Normalize A to P.
The filled90/180/270-degree sector argument locks every retained neighbor to
P's axes, including vertex-only contacts and T junctions.

For a neighbor written O+(tx,ty), apply the prior nondecreasing, unit-periodic
coordinate collapse c(t)=t at integers and floor(t)+1/2 otherwise to the entire
surround. Whole-copy separation, contact with the root, and the root's strict
covered collar survive. Its half-grid representative is retained as a selected
copy in the complete half-grid root formula. No disc topology of the final
surround is needed. This is a one-sided test: the neighbor is not required to
be covered, and no restrictions are imposed between new neighbors beyond
whole-footprint packing.

It follows that, if no floating half-grid contact has root support, every
neighbor of every covered copy has an actual integer relative translation.
Indeed c(t) is integral if and only if t is integral. This is stronger than
merely eliminating reciprocal floating contacts between two covered copies:
one covered end is enough.

In any H-corona patch, each new copy touches a copy in the preceding prefix,
and that preceding copy is covered by the new cumulative prefix. Integer
relative translations and D4 orientations therefore propagate from the root
along these contacts through **every** layer, including the final one. The
argument uses strict nesting, rather than applying phase collapse to several
freely moving layers at once. For plane tilings the same implication applies
locally: bounded positive-area congruent tiles are locally finite, and the
touching neighbors of each tile retain a finite covered collar.

## 2. Exact absence of floating root support

Enlarge P by a factor two into 84 unit pixels. Its complete root contact pool
has 704 candidates, 352 of them with an odd coordinate in their pixel translation.
These are exactly the floating half-grid contacts of the original P. The
first-surround CNF has 704 selector variables and75,431 clauses. Each required
king-halo pixel has an owner clause; every pair of candidates whose **whole**
footprints overlap has a negative pair clause. Overlaps outside the demanded
halo are forbidden. Every candidate meets that halo and avoids the root.

The complete DIMACS SHA256 is

    4eb6163156d529b467311ea1722a26d4138cce2fd1521a0935774629898ce36c

[floating-support.rup](floating-support.rup) has 357 additions and 2,470 bytes.
Its SHA256 is

    dbf195237b526df8330ccc11646b7bfa09a8cbe429b6da2ff0a141ba4b3fb084

The reader accepts an added clause only when the base formula and preceding
proved clauses, together with the negations of its literals, unit-propagate
to a contradiction. Induction proves every retained addition. Negative units
for all 352 floating selectors are checked; there is no floating support.
Native solver UNSAT is not a proof premise. Section1 consequently registers
all copies in any corona patch, including its last layer, to the root grid.

Discovery built its pool by bounded translations and its pair clauses by
lazy cell incidence. The reader independently maps physical square vertices,
anchors oriented pixels to demanded halo pixels, and tests candidate pairs
by direct full-footprint intersections. It reconstructs precisely the formula
whose fingerprint is above. The exact isometry and RUP primitives are shared,
byte-pinned dependencies. This is same-author implementation independence,
not independent mathematical review.

## 3. One necessary first prefix under a second-corona assumption

On the integer grid there are 352 contacts. Exactly 34 have a packing-only
root surround: thirteen literal root witnesses establish all 34 positives,
and complete first-uncovered forced-root searches reject the other 318.
Neither a neighbor's own halo nor reciprocal support is imposed in those
one-sided tests. The reader reconstructs each full-footprint problem and
completes every negative search; no solver is used.

Suppose a second corona existed. Section1 registers every copy, and both root
and first-layer copies are covered. Every touching pair among them must belong
to the 34 supported types in **both** directed relative frames. Reciprocal
closure of the 318 exclusions forbids 327 of the 352 physical contacts. A complete
root halo-cover enumeration in the remaining necessary domain has exactly one
selection, with six neighbors. Every contacting integer neighbor occupies at
least one required halo cell, so none can be omitted as an optional extra
copy once the halo is covered.

This is the sole first prefix compatible with these necessary constraints
**under the second-corona assumption**. It is not a claim that P has only one
unrestricted first corona. The literal selection is also independently a valid
first disc corona: its seven full copies are pairwise disjoint, each new copy
touches the root, all root halo cells are covered, and their 147-cell union is
a disc. Therefore Hc>=1 and Hh>=1.

## 4. The final second layer cannot cover a required cell

Fix that necessary seven-copy first prefix. Every fixed copy would be covered
by the hypothetical second prefix. Inventory every new integer placement that
avoids the fixed copies, meets their exterior halo, and has a supported
directed contact from **each** fixed copy it touches. There are 688 placements
before this support filter and 50 afterwards. No reciprocal support or other
interior-pair restriction is imposed between new second-layer copies. This
fixed-center directed-support use is credited to the complementary
[T5 proof](../../six-heesch-2/strip-t5/proof.md) and peer2's demand-driven hint;
its hexagonal motion-registration argument is not imported.

The required exterior unit cell with lower-left corner **(0,11)** belongs to
none of those 50 candidate footprints. Therefore a second layer cannot cover
the first prefix's whole halo. This is already a one-cell necessary obstruction;
there is no inference from a failed search for a chosen witness or from a
truncated candidate pool. The reader builds the final pool twice, by full halo
anchoring and by transport of the 34 directed support types, and requires exact
agreement. It checks that (0,11) is outside the fixed union and in its demanded
king halo, and that every admissible whole candidate misses it.

All real second-corona copies would be integer by Section1. Thus the complete
necessary obstruction excludes second coronas under arbitrary motions, even
without a final disc requirement. It gives Hc,Hh<=1. The first disc witness
in Section3 proves equality.

A hypothetical plane tiling would have the same root-grid registration and
supported contacts. Its root's touching neighbors would yield the necessary
first prefix, and the finitely many tiles touching that union would provide
a final halo cover of the kind just excluded. Hence P cannot tile the plane.
This separately addresses the infinity convention for tilers.

## 5. Reproduction and limits

Run [check.py](check.py) using CPython 3.11+ from the repository root:

    python3 round-two/six-heesch-1/one-sided-registration-control/check.py
    python3 -O round-two/six-heesch-1/one-sided-registration-control/check.py

Both outputs must equal [expected.json](expected.json). The reader requires
only the standard library and two exact source dependencies listed in
[dependencies.json](dependencies.json); it rejects changed dependency bytes.
Four damaged controls reject a truncated floating proof, a false negative
unit for a checked first neighbor, an omitted necessary first prefix, and an
obstruction cell outside the demanded halo. Node, candidate, trace and wall
guards raise incomplete-check errors and supply no mathematical exclusion.

The universal phase/sector arguments, ordinary exact-code reasoning, shared
byte-pinned primitives and CPython remain explicit trust boundaries. There is
no formal-kernel theorem and no independent-review verdict for this artifact.
The empty one-sided floating support is a reusable sufficient registration
criterion, with this low-Heesch tile as a certificate control. It does not
prove that all unmarked polyominoes have integral coronas. The square-cell
finite-five construction frontier remains unresolved.
