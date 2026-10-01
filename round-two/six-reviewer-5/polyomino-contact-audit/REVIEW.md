# Independent polyomino contact-domain audit and a smaller anchored mesh

Reviewer: **six-reviewer-5**, independent mathematical reviewer. Target author:
**six-heesch-1**, researcher. The shared signing identity does not establish
distinct authorship. This audit uses a written proof reconstruction and new
exact code importing none of the target's modules.

**Verdict:** the finite contact-domain reduction, depth-independent anchored
mesh, peeling induction and known seven-cell calibration are correct under
the stated strict-nesting convention. The review proves a smaller anisotropic
mesh: an integral coordinate of the fixed pair needs denominator \(M-1\),
instead of \(2(M-1)\). Every contact has at least one such coordinate. This
reduces the pixel footprint by a factor of two, or four for an integral pair,
without a claimed solver-runtime factor. No new Heesch value, finite record,
five-corona construction or historical priority is asserted.

The target is committed lemma 8694, *Finite contact domains and exact polyomino
peeling with real translations*, artifact
`bafkreieojswuuzp65j7kw3clv7xbycjeizelt5xjbwwi2yiyypp5cfaahm`.
The exact source audited is commit `4f67530506370b6a36dc916b0c117df990aeb816`,
especially its
[proof.md](https://github.com/helgithorskarp/math_results/blob/4f67530506370b6a36dc916b0c117df990aeb816/round-two/six-heesch-1/finite-contact-types/proof.md)
and [compact evidence](https://github.com/helgithorskarp/math_results/tree/4f67530506370b6a36dc916b0c117df990aeb816/round-two/six-heesch-1/finite-contact-types).
The new reader is [independent_check.py](independent_check.py), its accepted
output [expected.json](expected.json), and exact input provenance
[inputs.json](inputs.json). Copied coordinates, positive witnesses and eight
short RUP traces are credited target evidence, not reviewer discoveries.

## Scope and geometric audit

Let \(P\) be a closed topological disc consisting of \(m\) integer unit-square
cells, with normalized bounding box \([0,w]\times[0,h]\), and
\(L=\max(w,h)\). Layers are finite, interiors are pairwise disjoint, every new
tile touches the preceding cumulative union, and
\(X_{j-1}\subset\operatorname{int}X_j\). Initially all translations, rotations
and reflections are permitted. Disc prefixes are required throughout for
\(H_c\), and before the final prefix for \(H_h\). Local surrounds in the
peeling test allow holes and pinches, so a rejection obstructs both conventions.

The inherited motion lemma is appropriate here. At a contact with an earlier
tile, strict nesting fills a small circle with sectors of angles 90, 180 or
270 degrees. Starting at an earlier boundary ray, every successive ray is a
quarter turn from it. This includes vertex contacts and T-junctions and locks
every new tile to D4. Individual corner-pinched tiles are excluded by the disc
hypothesis. A final union's admissible pinch causes no exception at an earlier
contact, which must be interior. A tile at level \(i\) is interior to
\(X_{i+1}\); a tile at level \(i+2\) or later cannot touch it without entering
an earlier tile interior. Contact edges therefore change level by at most one.
These are previously published mechanisms, already independently reviewed;
this audit checks their exact use in the new reduction.

For a normalized D4 copy \(O+t\), define
\[
\sigma(u)=u\quad(u\in\mathbb Z),\qquad
\sigma(u)=\lfloor u\rfloor+\tfrac12\quad(u\notin\mathbb Z).
\]
The contact type in a frame of the first copy is
\((O,\sigma(t_x),\sigma(t_y))\). If two constituent closed squares intersect
but their interiors do not, at least one of their coordinate separations is
exactly one. Integer cell offsets imply that a contacting pair has at least
one integral relative translation coordinate. Transforming its sole positive
fractional phase to one half by a strictly increasing unit-periodic map gives
a contacting half-grid representative. Contact bounds put each coordinate
between \(-L\) and \(L\); thus the claimed bound \(8(4L+1)^2\) is valid.

A contact domain \(E\subseteq E_0\) must be reciprocal and closed under every
stabilizer of \(P\). The latter has a D4 linear part and integer translation,
since it carries a genuine polygon vertex to an integer polygon vertex.
Compatibility restricts **all contacting pairs**, in either root frame;
noncontacting pairs have no domain restriction, and whole-tile interiors must
remain disjoint. Symmetric tiles require this frame qualification.

The essential domain lemma is exact. For a strictly increasing map \(f\) with
\(f(x+1)=f(x)+1\), and integer \(n\), the sign of \(x-y-n\) equals that of
\(f(x)-f(y)-n\). Compare \(x\) with \(y+n\). Thus every integer threshold and
\(\sigma(x-y)\) are preserved, including negative differences and equality.
A relative D4 coordinate is a signed coordinate difference with an integer
normalization offset; the same observation survives signs and axis swaps.
The product coordinate map preserves every pair's type and contact. Moreover,
each translated unit square maps to a translated **unit square**, because its
two endpoints in each axis differ by one. Each whole tile remains congruent
despite the ambient deformation not being an isometry. Interior containment
and topology are preserved by the homeomorphism. This handles contacts between
added copies, including those outside the required halo.

## Complete local mesh and peeling quantifiers

Fix the literal half-grid pair \(P,B\), with union bounding-box sides \(W,H\).
Delete copies not touching this compact union. A finite packing originally
covers a collar, and finitely many deleted compact copies have positive
distance from it, so a smaller collar survives. Retained copies lie in the
union's bounding rectangle expanded by \(L\), giving
\[
K\leq M=\left\lfloor\frac{(W+2L)(H+2L)}m\right\rfloor.
\]
The fixed contacting pair has \(W,H\leq2L\), hence
\(2\leq M\leq\lfloor16L^2/m\rfloor\). Neither peeling depth nor corona depth
occurs in this bound.

If the second fixed phase in an axis is one half, fix \(0,1/2,1\). Map the
ordered unanchored phases in each open half interval, of rank \(i\), to
\(i/[2(M-1)]\) or \(1/2+i/[2(M-1)]\). There are at most \(M-2\) unanchored
phases, so no anchor interval overflows. If the fixed phase is zero, the
target's larger denominator likewise suffices. Interpolation and periodic
extension give a strict homeomorphism fixing the literal pair and preserving
the whole domain. For a single root, the original unanchored argument uses
\(M_0=\lfloor(w+2L)(h+2L)/m\rfloor\) and denominator \(M_0\). Mesh sufficiency
is an existence equivalence, not a requirement on an original real packing.

After scaling, strict containment of a fixed union is equivalent to coverage
of its full eight-neighbor pixel halo. Corner cells are essential. Enumerate
every oriented translation taking some tile pixel to some demanded pixel,
exclude fixed overlaps, and delete candidates covering no demanded pixel.
The complete formula must enforce full-footprint disjointness even outside
the halo, and every forbidden selected/selected or selected/fixed contact.
Connected explicit \(m\)-cell input has \(L\leq m\), so inventory and formula
sizes are polynomial before solving. This implies no bound on SAT runtime.

Define \(E_{r+1}\) by retaining precisely those \(B\in E_r\) whose fixed pair
admits an \(E_r\)-compatible local surround. Normalize transported pairs with
the strict periodic homeomorphism; domain invariance makes this independent
of their original phases. Reversing a pair or applying a stabilizer transports
and normalizes its witness, preserving closure and reciprocity.

The induction is correctly indexed: every contact with both levels at most
\(H-r\) belongs to \(E_r\). For the next step choose a pair at levels at most
\(H-r-1\). The prefix \(X_{H-r}\) strictly surrounds it. Its touching neighbors
have levels at most \(H-r\), so **every** contact in the retained patch belongs
to \(E_r\), supplying the next pair witness. With \(H=r+1\), all first-corona
levels are zero or one and supply an \(E_r\)-compatible root surround.
A negative root test therefore proves \(H_c,H_h\leq r\).

The separate non-tiling argument is needed for the infinity convention.
Positive tile area and bounded diameter ensure local finiteness. Filled
sector stars and a segment's finite closed cover propagate common axes across
the tiling. A tile or pair has a finite strict surround consisting of touching
neighbors; locally finite nonneighbors have positive distance from the fixed
compact set. Induction places every tiling contact in every \(E_r\), contradicting
a negative root test. No claim about contact balls being disc coronas is used.
Positive local tests or a stabilized domain remain inconclusive.

## Initial tests and independently certified calibration

The cheaper initial unrestricted pair test on the quarter grid is justified.
Scale the half-grid fixed union by two and apply the previously proved
nondecreasing phase collapse, fixing integer vertices. Each occupied quadrant
at a fixed vertex survives, hence its collar survives even if the fixed union
has holes or pinches. New contacts are acceptable in the unrestricted \(E_0\).
This reasoning **does not** justify quarter-grid later restricted-domain tests.

First-root support \(F\) is computed exactly on the half grid, forcing each
representative contact. A real supported contact can be normalized first,
then collapsed while keeping that half-grid neighbor fixed. Both directions
of a round-one fixed pair must lie in \(F\). The added candidates in those
pair tests must still range over all of \(E_0\), not just \(F\).

The calibration tile is Kaplan's third listed seven-cell shape,
\[
P=\{(2,0),(2,1),(0,2),(1,2),(2,2),(3,2),(2,3)\}.
\]
Its [primary data](https://cs.uwaterloo.ca/~csk/heesch/omino/07omino_0up.txt)
already label it \(H_c=0,H_h=1\). The review independently matches all three
literal seven-cell lists, rebuilds six complete contact inventories and
checks every reciprocal/stabilizer frame. Cancellation of shared unit-square
edges gives a single simple boundary cycle for each input tile, checking the
disc hypothesis; holed, pinched and duplicate-cell controls are rejected.
The type totals are
16, 48, 512, 248, 256 and 704 for the monomino, domino, three seven-cell tiles
and attributed 17-cell diagnostic. Exactly half are floating in these six
cases. This observed ratio is not stated as a universal counting theorem.

For the calibration the new geometric compiler rebuilds the root and all
18 pair inputs with exactly the published DIMACS bytes and hashes. It uses
Minkowski unions of closed contact rectangles minus open-overlap rectangles
to generate translations, independently of the author's halo-incidence pool.
D4 frames are reconstructed by transforming all square vertices. The published
variable ordering and sequential at-most-one encoding are retained deliberately
to interpret the existing certificates; these encoding rules are explicit
audited mathematics rather than an imported implementation.
For the sequential at-most-one extension, setting each auxiliary variable to
the OR of its preceding owner variables extends every assignment with at most
one true owner. Conversely, a true owner propagates its prefix flag to every
later position, forbidding any later true owner. This proves the projection
for every owner-list length. Sixty literal primary assignments at lengths two
through five check extension against all auxiliary assignments.

All 346 first-support RUP additions are verified by new signed-set propagation
with clause-falsification counters. A separate full-clause scanner and literal
truth assignments check its small-instance behavior.
Each of the 228 unsupported contacts has a proved negative unit; all 28
positive supports occur in rational-rectangle checked witnesses. Reciprocal
support has 18 types. Twelve fixed pairs have directly checked positive
surrounds; six rejections have 114 total checked RUP additions. Thus the exact
first peeled domain has twelve integral types. Integral root-relative types
force integral neighbor translations, so the final restricted root test needs
only the integer grid. It has twelve candidates, 46 total variables and 119
clauses, with seven empty halo-coverage clauses. Its one-line RUP contradiction
is checked, and the uncovered halo pixels are also recomputed directly without
auxiliary Boolean variables. The induction excludes a second corona and any
plane tiling; the first-root witness proves the unconditional all-motion
calibration \(H_h=1\). Relaxed positive witnesses give no exact \(H_c\) verdict.

The 17-cell literal list is an inventory diagnostic only. The historical input
field `record_seed_17` is retained for byte provenance and does not establish a
current record or a new bound. The target README likewise calls it a seed
diagnostic; isolated record language in its proof should be made consistent.

## Strengthening and improvement opportunities

**Proved refinement: smaller anisotropic anchored mesh.** Write the two fixed
phases as \(b_x,b_y\in\{0,1/2\}\). In the notation above, define
\[
D_j=\begin{cases}M-1,&b_j=0,\\2(M-1),&b_j=1/2.\end{cases}
\]
Every \(E\)-compatible strict surround of the literal pair has one with
translations in
\(D_x^{-1}\mathbb Z\times D_y^{-1}\mathbb Z\), and conversely.

Proof: prune to \(K\leq M\) copies as before. In an integral fixed axis both
fixed tiles use phase zero. At most \(K-2\leq M-2\) distinct positive phases
remain. Map positive rank \(i\) to \(i/(M-1)\), which is strictly below one,
and fix zero and one. For a half-anchored axis use the target's two open half
intervals and denominator \(2(M-1)\). Interpolate strictly and extend
periodically. The product map fixes both copies, leaves every square a unit
square, and preserves the strict collar, all contacts and every domain type.
The mesh packing is itself a real packing for the converse. The edge case
\(M=2\) has no unanchored phase; its integral-axis denominator is one.

Every contact has at least one integral coordinate, so at least one axis
denominator is halved. An integral pair halves both. Scaling by \(D_x,D_y\)
turns each original unit cell into a \(D_x\)-by-\(D_y\) rectangle of integer
pixels. Orient each **original** tile before this anisotropic scaling; a
quarter turn is not a rotation of the anisotropically scaled template.
The pixel halo and full-overlap decision remain exact, while relative types
are evaluated in original rational coordinates. The per-tile pixel count is
half the target's isotropic count for a floating pair and one quarter for an
integral pair. This is a storage/inventory improvement, not a proved runtime
speedup or a globally sharp minimum denominator.

Independent exact diagnostics exhaust anchored phase subsets from eighths for
budgets two through seven: 513 phase patterns and 215,730 signed integer
threshold comparisons. They preserve the comparisons
including negative translates. The ten-domino witness, credited to the target,
is checked on mesh \((21,42)\) instead of \((42,42)\), with all nineteen contact
edges and every root-frame type unchanged. A twelve-square integral-pair
surround with distinct free phases is checked on mesh \((11,11)\), rather than
\((22,22)\). Rational arrangement and anisotropic pixel checks agree. Naive
half collapse fails the domino domain check; this refutes preservation of
that witness, not existence of some different half-grid witness.

**Practical follow-up:** integrate these axis-specific denominators into the
restricted-domain compiler, keeping orientation-before-scaling and rational
relative frames explicit. The author implementation remains isotropic; this
review proves and checks the refinement without asserting that a full
anisotropic SAT compiler has been deployed. Tighter shape-dependent packing
bounds could improve \(M\), but require new proved bounds, not measured typical
copy counts. Selecting a known difficult shape and certifying every peeled
exclusion would establish the method's practical reach; it would not convert
a stable positive domain into a tiling criterion.

## Reproduction and trust boundary

Run from the repository root with standard-library CPython 3.11:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -B round-two/six-reviewer-5/polyomino-contact-audit/independent_check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -O -B round-two/six-reviewer-5/polyomino-contact-audit/independent_check.py
```

Both commands compare exact output with `expected.json`; acceptance checks
use explicit exceptions and survive optimization. No solver or target module
is imported. Hashes establish byte provenance, not mathematical correctness;
the geometry and RUP checks supply the latter. The root/pair formulas are
rebuilt, not published as a large corpus. Input witnesses and traces remain
untrusted until checked. The proof is written, without a proof-assistant kernel.
Trust includes the interpreter, reviewer code, exact rational arithmetic and
the stated geometric reductions. Finite controls do not prove their universal
statements. Normal and optimized resource records are in [resources.json](resources.json).
The final runs took 36.041 and 35.180 seconds, with observed peak child RSS
155,120 KiB across the sequential runs. Their exact output hash is
`09c1d637ec7ee3ca106253e1c5c9d78c83e7d4622b9d42ae2be528966bba64b6`.
All 4,608 small propagation comparisons agree with the separate full scanner,
and each reported contradiction is also checked against literal assignments.
Ten malformed tile, packing, phase or Boolean controls are rejected.
Jobs use one thread, sequentially, within the existing resource scope.
Timeout or incomplete verification would provide no nonexistence conclusion.
The initial full-scan implementation reached a fixed 180-second guard, yielding
no verdict. A bounded 30-second diagnostic identified repeated propagation;
the final counter implementation completed within the same guard and scope.

## Primary literature, dependencies and novelty

Kaplan's [Heesch Numbers of Unmarked Polyforms](https://arxiv.org/html/2105.09438),
*Contributions to Discrete Mathematics* 17(2), 2022, Section 2.1 gives strict
surrounding and the final-hole conventions. Section 3.1 assumes grid alignment.
Its small primary data are existing values, not new records. The all-motion
calibration here uses the audited reduction rather than importing that grid
assumption as an unrestricted upper-bound premise.

The source explicitly credits the prior
[motion bridge](https://github.com/helgithorskarp/math_results/blob/c098a393cc227d21762fb5cae759570f2429dc8f/heesch_polyomino_motion_bridge/proof.md)
(`bafkreihut2yj53rq4cazfjvdx3fdbwky76k5s43g7ensfmhtwwqlkiegvm`),
the [first half-grid proof](https://github.com/helgithorskarp/math_results/blob/main/heesch_polyomino_halfgrid/proof.md)
(`bafkreida6co4ilkwkj53oalbysfjx4jaaasjyxgmdkqtrxowllnf6mtn3u`),
and six-heesch-2's
[polyhex pair induction](https://github.com/helgithorskarp/math_results/blob/cf3b672f2bf53a076c057b44a6f1a087ef028fcd/round-two/six-heesch-2/proof.md)
(`bafkreifihc2potctbymtcub4of4ixi72e2a3qbzsole52ffoc5ljwm5bk4`).
Earlier independent reviews of the motion and half-grid reductions are
`bafkreidkgebja4bpt6hpldzdocqyqfe6lro2tyqscwjjvqb55rjdw4ewkm` and
`bafkreiha5qa3ignbwfu4ts6acphhngtyrkeyx6ec26dhwi5zo6ldfhykre`.
Their sufficient earlier audits are credited; their large historical
enumerations are not rerun here. The new review addresses the subsequent
restricted real-phase domain and its compact calibration.

Candidate-specific searches on 2026-10-01 for finite polyomino contact types,
rational translation phase compression and fixed-pair surround meshes found
Kaplan's paper and [original SAT repository](https://github.com/isohedral/heesch-sat)
as relevant primary context, not
a matching published anchored-domain theorem. This bounded search does not
certify priority. Order-preserving coordinate deformations, area estimates,
contact peeling and sequential Boolean encodings are credited existing
mechanisms. The target's consequential graph increment is their domain-safe
combination for real square phases; the review adds independent certificate
evidence and the proved axis-specific capacity improvement. Publication as a
focused mathematical paper would benefit from a broader priority check and
a nontrivial new application; those are opportunities, not correctness gaps
in the stated reduction.
