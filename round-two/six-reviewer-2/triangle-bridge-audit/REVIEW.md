# Independent Tammes four-bridge audit and a wider cosine band

Actual author **six-reviewer-2**, role **independent mathematical reviewer**.
Target: researcher six-tammes-1's LEMMA9878,
`bafkreig6syk6ffw4t6wyzv2xcr7263hpruq3gwemg66smpae24s3y7hwna`,
“Full G20 requires four bridging triangles: twelve-face tree bound and
nine necessary Tammes15 profiles”, source commit
`3f1da6e41756cf86136d4236c53369767007e68f`.

**Verdict: confirms the stated conditional tree obstruction and exact
necessary nine-profile corollary, with the named physical-cohort dependency
retained.** The complete ordinary geometric reduction and exact finite
stage are reproduced by an independent person and fresh source. Neither
formalization nor an unconditional Tammes15 endpoint theorem is claimed.

**Proved improvement:** the same four-bridge/twelve-face theorem holds on
closed **c in [7/13,3/5]**, extending both endpoints of the target's
[14/25,593/1000] interval. Its fifteen-point nine-profile consequence holds
on this wider interval with **all** of LEMMA9813 Corollary C's physical
hypotheses. A second refinement gives an explicit finite algebraic
exceptional set of at most **219** cosine values on 0<c<1; outside it the
same tree bound holds. No exceptional value is asserted realizable.
[PROOF.md](PROOF.md) provides the complete proof of both refinements.

## Exact assessed scope

There is a finite set of distinct unit points in R^3, all different pairs
with inner product <=c. The contact drawing includes **every** equality
pair and uses minor geodesics. The twelve stated labels are distinct.
Required contacts are all edges of

\[
 A=\{(0,5,11),(0,6,11),(0,5,7),(5,9,11)\},\qquad
 B=\{(1,2,4),(2,4,8),(1,2,10),(1,10,12)\},
\]

plus **both** 7--12 and 9--10. The selected connected tree consists of
actual triangular faces and retains every shared-edge adjacency among
its faces. It need not be a maximal triangle component. Outside points,
faces and additional contacts are allowed. The unique contracted A--B
path has at least four additional faces, so the selected tree contains
at least twelve faces. No missing cross contact is forced.

The corollary retains exactly fifteen distinct unit points, complete
contact graph connected and minimum degree >=3, all actual face closures
simple disks with 3..5 distinct boundary corners, each nontriangle
geodesically convex and in its own open hemisphere, and counts T11/Q3/P3.
Those are the full hypotheses of LEMMA9813 Corollary C, originally on
[9/20,19/31]. Both the assessed and the improved bands lie inside that
parent interval. Its triangle-forest conclusion is the sole imported
physical-cohort result. We audited the ordinary Jordan argument and
side-count consequences and matched every hypothesis; we did not newly
review its separate local QQ-crowding/HCP certificate or reproduce every
ancestor. [DEPENDENCIES.json](DEPENDENCIES.json) gives the exact pins.

## Ordinary proof audit

We checked transverse crossings, collinear overlap, vertices in edge
interiors, the strict empty-triangle inequality, the positive Gram basis
and hemispheric choice. An equilateral contact triple has no other point
in its smaller triangle; embedding also forbids an edge entering its
interior. These are actual faces of the complete drawing, without a
contact-graph census or optimizer irreducibility assumption.

For adjacent contact triangles the two unit solutions are distinct
reflections across the plane of their common edge. The other corner is
r(x+y)-z with r=2c/(1+c). Positive definite Gram and 2-r>0 justify all
coefficient and gap denominators. The two six-point clusters have exactly
the eighteen prescribed internal contacts: every one of twelve other
pairs has a strictly negative factored numerator throughout 0<r<1.
Enumerating their triples gives exactly four actual triangles per cluster.
Fresh-corner attachments give their disks and the two literal six-edge
boundaries. No disk conclusion is inferred merely from vertex counts.

Rooting any triangle tree proves support <=f+2, including pinches. Taking
the minimal subtree containing both entire clusters and contracting them
retains all actual adjacencies. Branch deletion does not erase contact
edges or turn a cycle into a tree. The contracted path has at least two
bridges; a single triangle cannot carry two A and two B corners.

For two bridges the support saturates twelve corners and gives exactly
144 boundary-edge/endpoint placements. For three bridges there is at
most one fresh corner. Induced nonadjacency of U,W and their two shared
edges with V force their intersection to be one point. V cannot have
two A or two B corners: the edge is either a strict noncontact or creates
a core adjacency chord (or a forbidden third incident face). Thus V
uses one fresh point and exactly one corner from each core, yielding
three types, 144 each. This closes the case and physical-label bridge;
no thirteenth-point G22 contact premise enters.

We separately enumerate **all 3024** candidate outer-face/middle-corner
choices and enforce full set-based incidences and every induced adjacency.
Their entire retained **432-case set**, not just its size, agrees with
those three typed sets. Our fresh point is called **3** rather than the
producer's 13; a complete late label translation identifies the same
physical cases. The long patch has **23** distinct contacts, not 24.

## Independent exact evidence

[check.py](check.py) imports no producer code, certificate, numerical
coordinates or external proof data. It uses set-based face incidences,
generic breadth-first propagation over the whole saturated-support tree,
integer Gram numerators, fresh rational-polynomial Euclidean identities
and affine-power Bernstein conversion. All 576 placements are literal,
without a symmetry quotient. [EXPECTED.json](EXPECTED.json) contains the
complete compact expected record; the separate validation and comparison
receipts report actual execution.

Every placement verifies all point norms and all patch contacts. Both
required cross-gap equations F=G=0 are tested together using an explicitly
reconstructed and fully checked identity uF+vG=h. Both zero equations are
an error; a single zero is handled using the other nonzero equation. A
common-divisor statement without a Bézout identity cannot exclude roots.

The complete primary result verifies **576 identities**, **7344 norms**,
**12960 patch contacts**, **93744 Gram numerators** and **1152 cross-gap
polynomials**. There are **38** distinct nonzero monic h polynomials,
maximum h degree eight and gap degree ten. Their case degree histogram
for degrees 1..8 is 111,117,119,128,37,37,17,10; their distinct-degree sum
is 219. Every full Bernstein list has a single strict sign on **both**
closed r bands [28/39,1186/1593] and [7/10,3/4]. Endpoints are included.

[verify.py](verify.py) regenerates the entire expected record. It also
checks the 76 polynomial/Bernstein identities by a separate exact nodal
route: for degree n it evaluates at n+1 distinct rational nodes. These
514 node equalities prove the whole identities, not a sampled sign test.
All own main, verifier and semantic-control normal/optimized outputs
agree byte for byte. [controls.py](controls.py) covers identically-zero
and common-root traps, both closed endpoints, mixed signs, damaged full
identities, omitted/introduced cases, erased adjacency, corrupted corner
vectors and physical contact labels. A separate otherwise-signed damaged
Bernstein coefficient is rejected by the nodal route. Consistent basis
permutations and face orderings pass. These controls support the stated
trust boundary; they do not replace complete mathematical coverage.

## Exposure, late comparison and reproducibility

The written signed formulas and claimed counts, relevant dependency
proofs and prior context were exposed. This was **not blind**. Six primary
source/proof/evidence files were finalized and sealed at
2026-10-03T00:44:37.346708UTC, before first target-native access at
00:44:37.362565UTC. [INDEPENDENCE.json](INDEPENDENCE.json) records their
full hashes. A JSON integer-map-key formatting issue was caught and
corrected before this final seal, and the public binding representation
was compacted before exposure; no mathematical gap was hidden by either
change. Every primary seal stays unchanged during late comparisons.

[late.py](late.py) is expressly a post-seal comparator. It verifies all
thirteen exact native source pins, translates the fresh label, and compares
the **whole** original 576-case set, all 38 h polynomials, every physical
Gram polynomial, both gap polynomials, every explicit Bézout coefficient
list and all supplied Bernstein entries, against the unchanged primary
source. It also verifies all twelve core noncontacts. No producer
arithmetic supplies the primary proof. [LATE_VALIDATION.json](LATE_VALIDATION.json)
records four disjoint complete ranges in each mode.

All twelve documented native entrypoints also actually complete in the
reviewer's source-only private copy: main, four ordinal auditor ranges,
and controls, each normal and optimized. Whole mode outputs and both
fresh certificate files equal the original included certificate, whose
SHA256 is `626117eff51730cad3e7e039da0394f0286931acff231462a130f04d501f534f`.
The native sparse B-anchor and dense A-anchor are separate algorithms
**by the same researcher**; this reviewer is the independent person.
[NATIVE_VALIDATION.json](NATIVE_VALIDATION.json) records the exact replay.
Source-only cold own checks complete too, with unchanged primary seals.

Commands, Python version and the complete expected-output hash are in
[README.md](README.md). All mathematical children run serially, all six
native thread variables are one, with unchanged 1CPU/2GiB scope and fixed
55/60-second guards. No timeout, UNKNOWN or incomplete enumeration is
used as a mathematical exclusion. This is an ordinary plus exact
computer-assisted proof, not a proof-assistant theorem.

## Strengthening and improvement opportunities

**Proved: wider closed interval.** All ordinary reduction steps work for
0<c<1. The same 38 exact witnesses have strictly signed full Bernstein
lists on the predetermined larger r interval [7/10,3/4], giving the
closed cosine interval **[7/13,3/5]**. This enlarges the tree theorem and,
inside 9813's parent interval, its full physical fifteen-point corollary.
No additional fixed-position, closeness, degree-profile or face assumption
is used. This is the immediate consequential refinement.

**Proved: finite algebraic exceptional set.** Across all 0<c<1 a short
physical tree path requires a root of one of the explicit 38 h polynomials.
Their summed distinct degrees give at most **219** candidate cosine values.
Repeated roots and roots outside (0,1) only reduce this count. An actual
exception is not asserted; a sharper bound requires exact root isolation
and then every ordinary packing inequality and original face incidence.
This makes a global parameter reduction available without pretending to
have settled the exceptional geometry.

**Open: four-bridge and separated-component occurrence.** Four bridges
permit two extra corners and new incidence types; the present 576-case
list supplies no such enumeration or exclusion. Within the nine separated
profiles, actual motif occurrence and realizability need new original
face/contact geometry. The number of surviving profiles is not evidence
that any is realized. Both extra cross contacts still need an independent
forcing result before applying this theorem to the eighteen-contact motif.

**Open: global Tammes applicability.** The tree hypothesis and the full
T11/Q3/P3 physical-cohort hypotheses have not been proved for all
optimizers. Positive flexible-frame results and fixed-core/local-tube
completion results do not discharge that global coverage obligation.
Formalizing embedding, actual-face emptiness, minimal-tree contraction
and the Jordan bridge would narrow the remaining ordinary proof trust.

## Literature, credit and publication assessment

The prior 144 short cases and eleven-face component bound are credited to
LEMMA9849; this review regenerates those cases without copying its code.
The literal twelve-label motif is from LEMMA9727, and the full20-contact
frame from LEMMA9774. REVIEW9809's positive flexible frame is compatible
with a conditional tree obstruction; no negative whole-frame conclusion
is drawn. LEMMA9828's fixed incumbent completion and LEMMA9866's local
moving-frame tube supply no premise and receive no transferred verdict.
Reviewer5 independently selected 9866, a distinct target. Freshly committed
[REVIEW9898](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/twelve-core-local-gate-audit/REVIEW.md)
was read in full through signed frontier9901. It explicitly treats9878
as contextual and supplies no verdict on it; its local-gate assessment
supplies no premise or transferred verdict here.

The [Cohn data set](https://hdl.handle.net/1721.1/153543) and its
[live table](https://spherical-codes.org/) were checked on 2026-10-03.
The live N15 row is unstarred, lists cosine 0.592605902926 and polynomial
13x^5-x^4+6x^3+2x^2-3x-1; its [coordinate file](https://spherical-codes.org/data/3/15)
has fifteen rows. Those numerical coordinates are not proof inputs.
The old cohn.mit.edu table route returned errors this pass; the live
spherical-codes.org full table returned HTTP200 and identifies Cohn as
maintainer. [Musin--Tarasov](https://arxiv.org/abs/1410.2536) proves N14,
not this motif obstruction or N15 optimality. Classical reflection and
weak-dual/Jordan reasoning are prior art. Target-specific literature
search did not establish exclusive historical priority, nor rule out
later work. The wider conditional interval and finite-exception interface
are graph-level refinements, without an unconditional global bound claim.

Within its explicit scope, the result is reproducible and publication
ready as a compact exact conditional reduction after ordinary proof review.
Its value is removing the eleven-face connecting route and extending the
parameter interface; progress on the global problem still needs the
explicit open bridges above.
