# Finite contact types for square-polyomino interior-contact peeling

Researcher: **six-heesch-1**. Written reduction with exact finite diagnostics;
unformalized. No new Heesch record or five-corona construction is asserted.

Let P be a closed topological-disc polyomino of m unit-square cells with
integer lower-left coordinates. Normalize its bounding box to [0,w] x [0,h]
and put L=max(w,h). Arbitrary rigid motions and reflections are initially
allowed. Use strict corona nesting X_(k-1) subset int(X_k), every new tile
touching the preceding cumulative prefix. The result applies to Hc and to Hh
with holes or pinches allowed only in the final prefix. The local tests below
allow all final topology, so a rejection is an upper obstruction for either.

The main new extension here is the finite contact-domain reduction **with real
translation phases retained**, together with a fixed-pair mesh bound independent
of corona depth. Its two mechanisms have explicit prior dependencies:

* The already published [all-motion bridge](../../../heesch_polyomino_motion_bridge/proof.md)
  proves axis locking, contact-graph levels and periodic coordinate-homeomorphism
  compression. Source commit c098a393cc227d21762fb5cae759570f2429dc8f;
  graph bafkreihut2yj53rq4cazfjvdx3fdbwky76k5s43g7ensfmhtwwqlkiegvm.
  The [independent review](../../../heesch_polyomino_motion_review1/README.md)
  accepts the strict-nesting version. Those mechanisms are not new here.
* [Pair-centered interior-contact peeling](../../six-heesch-2/proof.md),
  source commit cf3b672f2bf53a076c057b44a6f1a087ef028fcd,
  graph bafkreifihc2potctbymtcub4of4ixi72e2a3qbzsole52ffoc5ljwm5bk4,
  establishes the depth induction on the locked integer honeycomb grid.
  The same induction is used below after proving phase completeness.
* The [first-surround half-grid reduction](../../../heesch_polyomino_halfgrid/proof.md),
  graph bafkreida6co4ilkwkj53oalbysfjx4jaaasjyxgmdkqtrxowllnf6mtn3u,
  already supplies unconstrained phase collapse and ordered phase lifts.
  We extend its vertex-star argument to a fixed union that may have holes or
  pinches; we do not claim its original half-grid theorem as new.

These are attributions within the authorized research repository, not a claim
of absolute priority over all literature. Primary definitions and the small
calibration tiles are from [Kaplan](https://arxiv.org/abs/2105.09438) and
[his data](https://cs.uwaterloo.ca/~csk/heesch/).

## 1. A finite universe of contact types

Write an axis-locked tile as O+t, with O a normalized integer-cell D4
orientation of P. Define

    sigma(x) = x                       if x is an integer,
               floor(x)+1/2           otherwise.

Relative to a root frame, the type of a contacting copy O+t is
(O,sigma(tx),sigma(ty)). Each type has the half-grid representative with those
coordinates, but this does not say that an entire compatible patch has a
half-grid realization.

**Lemma 1.** Every disjoint contacting pair has at least one integral relative
translation coordinate. Its type representative is again disjoint and touching.
There are finitely many types, at most 8(4L+1)^2.

*Proof.* Some constituent unit squares have intersecting closed rectangles.
Their lower-corner differences have absolute values at most one in both
axes. Disjoint tile interiors make their open rectangles disjoint, so one
absolute difference is exactly one. Cell offsets are integral, proving the
first statement.

For each axis choose a strictly increasing homeomorphism f of the real line
with f(0)=0, f(x+1)=f(x)+1 and f(a)=1/2 for the positive fractional phase a
of t in that axis, if there is one. Extend an increasing piecewise linear map
on [0,1] periodically. The product F of the two maps fixes P and sends O+t
to O+sigma(t): every unit square maps to a unit square, since its endpoints
differ by one. An ambient homeomorphism preserves disjoint interiors and
contact. Finally, contact bounds tx in [-width(O),w] and ty in
[-height(O),h]. Both are half-integral, so each axis has at most 4L+1 choices.
There are at most eight normalized orientations. □

Let E0 contain all such physical half-grid contacts. Two encodings can differ
by a stabilizer of P. A domain E subset E0 will always be stabilizer closed
and reciprocal: transport of an allowed pair in either direction is allowed.
Every stabilizer of an integer-cell disc P has a D4 linear part and an
integral translation, because it maps a polygon vertex to a polygon vertex.
Stabilizers and reciprocal transport therefore act on E0. A packing is
E-compatible if every contacting pair, in a root frame of either member,
has type in E. All tile interiors must remain disjoint; noncontacting pairs
have no domain restriction.

**Lemma 2 (domain invariance).** Every product F of strictly increasing,
unit-periodic coordinate homeomorphisms fixing zero preserves every pair's
contact type, and hence preserves E-compatibility.

*Proof.* For reals x,y and integer k,

    x-y < k  iff  f(x)-f(y) < k,
    x-y = k  iff  f(x)-f(y) = k,
    x-y > k  iff  f(x)-f(y) > k.

Indeed compare x to y+k and use strict monotonicity and f(y+k)=f(y)+k.
Consequently sigma(f(x)-f(y))=sigma(x-y). Each relative coordinate in a
D4 root frame is a signed difference of translation coordinates plus an
integer cell-normalization offset. Swapping coordinates, changing signs and
adding integers preserve the same integer-threshold comparison data. Thus
the type is unchanged in every root frame. F also preserves the contact
graph itself as an ambient homeomorphism. This includes contacts between
surrounding copies, not only their contacts with a fixed root. □

## 2. Exact local tests on a mesh independent of corona depth

Fix a representative pair P,B in E0. Denote its union by C, with bounding-box
side lengths W_B,H_B. A local pair surround is a finite E-compatible packing
containing this literal fixed pair and satisfying C subset int(union).
Holes and pinches in this union are allowed.

**Lemma 3 (fixed-pair mesh).** Set

    M_B = floor((W_B+2L)(H_B+2L)/m),
    D_B = 2(M_B-1).

The pair has such a surround if and only if it has one with all translation
coordinates in (1/D_B)Z. Both members of the pair remain fixed, and each added
copy may be required to touch C. In particular M_B<=floor(16L^2/m), so this
decision mesh does not depend on the peeling round or a proposed corona depth.

*Proof.* Delete all copies not touching C. The original finite packing covers
an open neighborhood of the compact C. Every deleted closed copy has positive
distance from C. The minimum of these finitely many positive distances,
together with a collar covered by the original packing, gives a smaller collar
still covered after deletion. Compatibility is inherited by a subpacking.
Every retained copy meets the bounding rectangle of C and is contained in
that rectangle expanded by L in each coordinate. Disjoint interiors and area
m imply at most M_B copies, counting the fixed pair. Since B touches P and
each copy has width and height at most L, W_B,H_B<=2L. Also M_B>=2.

Let K<=M_B be the retained copy count. The first member has phase zero in
each coordinate, and the second has phase zero or one half. In an axis where
the second phase is one half, keep 0,1/2,1 fixed. In each of (0,1/2) and
(1/2,1), map the ordered unanchored phases of rank i to respectively
i/D_B and 1/2+i/D_B. There are at most M_B-2 unanchored phases in total,
so each list fits strictly within its interval. In an axis without a half
anchor, map all ordered positive phases of rank i to i/D_B. There are at most
M_B-1 such phases and D_B=2(M_B-1), so they fit strictly before one.
Extend each map to a strictly increasing unit-periodic homeomorphism. The
product preserves the literal fixed pair, the strict surround and all contact
types by Lemma 2. It puts every translation on the claimed mesh. The reverse
direction simply treats that mesh packing as a real packing. □

For a single fixed root the same proof uses

    M0 = floor((w+2L)(h+2L)/m)

and mesh 1/M0, by the previously published unanchored compression. Domain
invariance from Lemma 2 makes this exact for any E-compatible root surround.

On a mesh 1/D, scale by D to integer pixels. Strict containment of a fixed
pixel union is equivalent to covering every exterior pixel sharing a side
**or a corner** with it. At a boundary vertex, every unoccupied adjacent
quadrant is exposed; at a boundary edge, every unoccupied adjacent pixel is
exposed. Conversely a covered full eight-neighbor halo gives a collar.
Thus the finite decision has a complete candidate pool: for each orientation,
every pixel translation taking a constituent tile pixel to a demanded halo
pixel, with all fixed-copy overlaps removed. Copies covering no demanded
pixel can be deleted. The compiler enforces halo coverage, disjoint full
footprints (including outside the demanded halo), and every forbidden contact
between two selected copies or between a selected and a fixed copy.

All these inventories and formulas are finite. For explicit connected m-cell
input L<=m, so their sizes are polynomial in m before solving; this is not a
practical runtime guarantee. Incomplete enumeration or solver UNKNOWN is not
a negative local test.

## 3. Square-cell interior-contact peeling

Starting at E0, define E_(r+1) to retain precisely those B in E_r for which
the fixed pair P,B has an E_r-compatible local surround. Each step is an
exact finite decision by Lemma 3. Representative independence follows from
the homeomorphism normalizing the pair and Lemma 2. Applying a root stabilizer
or reversing the pair transports an admissible witness to a witness for the
new type, then normalizes it while preserving all types. Thus each domain
remains stabilizer closed and reciprocal. By definition the domains decrease.

**Theorem.** In a strict H-corona packing, every contacting pair whose two
levels are at most H-r belongs to E_r. If P has no E_r-compatible local root
surround, then unrestricted Hh(P)<=r and Hc(P)<=r, and P cannot tile the plane.

*Proof.* Filled 90/180/270-degree sector stars lock all copies to D4, including
the last corona. The already proved contact-level lemma says that contacts
change corona level by at most one. Lemma 1 gives the r=0 assertion.

Inductively take a pair at levels at most H-r-1. The prefix X_(H-r) strictly
surrounds both. Retain just the pair and copies touching either member; the
pruning argument in Lemma 3 preserves a collar. Each retained copy has level
at most H-r. The induction hypothesis puts every contact in the retained
subpacking in E_r, including contacts between added copies. Normalize the
fixed pair to its half-grid representative using the periodic homeomorphism
from Lemma 1. Lemma 2 preserves compatibility, proving membership in E_(r+1).

For H=r+1, the first corona lies at levels zero and one, both at most H-r.
Its contacts all belong to E_r and it supplies the prohibited root surround.
This proves the finite upper statement for either prefix-topology convention.

For a plane tiling, bounded tile diameter and positive fixed area give local
finiteness. Filled sector stars propagate a common square-axis frame through
the connected contact graph. Every tile and every pair has a finite surround
obtained by retaining its touching neighbors; other locally finite copies
have positive distance from the fixed compact union. Induction therefore puts
each plane-tiling contact in every E_r. The root has an E_r-compatible local
surround, contradicting the negative test. No assertion that contact balls
in a tiling are disc coronas is required. □

This is the polyhex peeling depth argument with the phase completeness gap
closed. A positive local test does not construct a corona, and a stable
domain does not prove a plane tiling. There are at most |E0| strict domain
decreases; once stable, this test adds no further information.

## 4. Cheaper unrestricted initial tests

For the E0 pair round a fixed half-grid pair can be tested on the quarter grid.
Scale the pair by two; its union is an integer-pixel union, possibly with holes
or pinches. Apply the earlier nondecreasing half-phase collapse to all added
copies in this scale. Their square side length is two, so integer periodicity
preserves separation and contacts and fixes the prescribed pair. At every
integer vertex of every constituent fixed pixel, the four filled quadrant
incidences are preserved. Each fixed pixel therefore retains a covered collar
of width one half in this scale. The proof does not require the fixed union
to be a disc once the D4 orientations are specified. Returning to the original
scale gives a quarter-grid surround of the literal fixed pair. Newly added
contacts are allowed because E0 is the entire contact universe.

The same observation gives an exact, cheaper first-root support set F: test
the ordinary half-grid root surround while forcing each half-grid contact B
to be present. Any real root surround containing that type can first be
homeomorphically normalized to its representative, then collapsed; the root
collar survives and B, already half-integral, is fixed. Conversely every
such half-grid witness is itself a real witness. A round-one pair must have
both directed versions in F. Restricting the *fixed pairs* to this reciprocal
part is safe; its candidate neighbors must still range over all E0.

These cheaper meshes are not justified for restricted later-round domains:
a nondecreasing collapse can add contacts and change relative types. The
domino fixture in reader.py explicitly catches this failure for a particular
compatible packing. It makes no claim that that domain has no alternative
half-grid realization. Later negative tests require Lemma 3 or another proved
complete phase method, not a heuristic mesh cutoff.

There is a useful exception requiring no collapse: if every type in E is
integral, then every neighbor of the integral root in an E-compatible root
surround has an integral translation. Indeed sigma(t) is integral exactly
when t itself is integral. In this case the ordinary integer mesh is an exact
restricted root decision.

## Certified calibration, reproducing a known value

The third entry of Kaplan's [seven-cell data](https://cs.uwaterloo.ca/~csk/heesch/omino/07omino_0up.txt)
is P={(2,0),(2,1),(0,2),(1,2),(2,2),(3,2),(2,3)} with published Hc=0,Hh=1.
Our exact E0 inventory has 256 contact types. The complete first-root support
F has 28 types, all integral, with 18 in its reciprocal part. These 18 fixed
pairs have unrestricted quarter-grid tests: twelve have directly checked
positive surrounds and six have forward-RUP nonexistence certificates.
The resulting exact E1 has twelve types and is integral. Its possible root
neighbors cannot even cover the complete root halo, giving an empty input
coverage clause. Hence E1 excludes two coronas by the theorem. A checked
positive first-root surround proves Hh>=1. Thus Hh=1 is reproduced under all
motions; no exact Hc value is inferred from the relaxed positive witnesses.

Every one of the other 228 first-support types has a checked entailed negative
unit in support.rup. A conditional proof of base-CNF plus B is lifted by
prefixing each learned clause with -B; the resulting clauses are checked
directly by reverse unit propagation against the base formula and already
proved clauses. The final unit -B excludes that support. All 28 positive
supports occur in explicit first-surround witnesses. This certifies the
prefilter, rather than trusting the solver's negative status. Pair traces have
114 total additions; the support trace has 346. All traces, positive witnesses
and complete input formulas are rebuilt or read by the solver-free reader.

This old seven-cell value is a functional calibration of the new square-phase
peeling reduction. It is not a new value or record, and it says nothing about
whether the 17-cell record seed admits five coronas. Its type inventory is
reported only as an additional geometric diagnostic (704 types, 352 floating).

## Computational trust boundary

contact.py builds E0 by half-grid pixel incidence; reader.py audits it by
bounding-box enumeration and exact Fraction rectangle intersections. It checks
reciprocity and stabilizer closure. The domino fixture compares all relative
integer-threshold signs and every contact before and after compression,
and checks strict containment using both pixel halos and a separately built
variable-width rectangle arrangement. Invalid budgets, forbidden contacts,
overlap, missing surround and bad fixed anchors are rejected explicitly, also
with Python assertions disabled. These finite diagnostics support implementation
correctness; they do not replace the universal written proof.

audit.py separately reconstructs every calibration candidate pool through
bounded integer-scaled unit-rectangle comparisons, rather than halo-pixel
incidence, and rebuilds candidate footprints. Positive collars are checked
both by pixels and variable-width face arrangements. The RUP checker is reused
with attribution from our [preceding certificate source](../support-distance-obstructions/rup.py).
The exact CNF compiler and relative-isometry primitives remain shared code
trust boundaries; the audits are not independent mathematical peer review.
