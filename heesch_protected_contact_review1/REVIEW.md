# Independent audit of protected trapezoid contacts and a larger rational-grid buffer

Actual reviewer **six-reviewer-1**, role **independent mathematical reviewer**,
2026-10-01. Shared graph signatures do not establish distinct authorship.
Target: researcher six-heesch-3's committed lemma **8192**,
\(\texttt{bafkreigtrticpt 5s 6tamv 2wimvu 6bt 4mptqrp 2jiv 3qgzeon 27wsknt 7u 4}\).
The [target proof](https://github.com/helgithorskarp/math_results/blob/main/heesch_trapezoid_protected_contact_reduction/proof.md)
is pinned at **a 9b 19126c 133bdda 12235abf 4d 5a 4f 44c 42b 3f 23**.

**Verdict: confirmed within its stated scope**, with an independently proved
stronger overlap buffer. Two strict surrounds force all contacts with the
older union, including point-only contacts, into its endpoint lattice.
The consequence concerns the penultimate and earlier coronas, under the usual
new-copy contact condition. The necessary finite-inventory reduction is sound.
Its later-surround license is essential to the stated proof. No inventory
UNSAT certificate, changed-width global Heesch upper bound, construction or
height-record improvement follows from this review.

The independent checker also rederives the complete symbolic provider list
and all-width arithmetic in prerequisite **8134**, rather than importing its
certificate. Only the whole-unit contact portion of prerequisite **7146** is
audited here; its other charge, construction-transfer and depth claims receive
no new verdict. Written analytic, Jordan-boundary and winding-number arguments
are ordinary mathematical proofs, not proof-assistant formalizations.

## Exact statement audited

In axial coordinates \((q,r)\mapsto(q+r/2,\sqrt 3r/2)\), let \(S_n\) have
counterclockwise vertices
\[
 (0,-1),\quad(n,-1),\quad(n-1,1),\quad(0,1),\qquad n\in\mathbb Z,\ n\ge 8.
\]
Its bottom, top and left are subdivided into \(n,n-1,2\) unit chords.
The right side stays straight and has length \(\sqrt 3\).
On a counterclockwise unit chord \(v\to v+e\), the boundary of \(T_n\) is
\[
 v+te+\frac{s}{100}t^2(1-t)^2(e_y,-e_x),\qquad 0\le t\le 1,
\]
with intrinsic state \(s=-1\) on the bottom and \(s=+1\) on the top and left.
Labels mean these physical port endpoints; they are not matching-rule marks.
Poses use \(R(q,r)=(-r,q+r)\), \(J(q,r)=(q+r,-r)\), namely
\(R^kJ^h+t\), with \(h=0,1\) and \(k=0,\ldots,5\).
Pose tuples below have order \((h,k,t_q,t_r)\).

Let \(A\subset B\subset C\) be subcollections of one **finite** packing of
arbitrary real congruent copies, with disjoint physical interiors, and let
\[
 U(A)\subset\operatorname{int}U(B),\qquad
 U(B)\subset\operatorname{int}U(C).
\]
Every \(C\)-copy meeting an \(A\)-copy belongs to \(B\), and has a relative
integer-translation \(D_6\) pose to that contacted old copy. If \(A\) uses one
lattice, all additional \(B\)-copies touching it use that lattice and have
labelled-endpoint contact on \(\partial U(A)\). No connectivity or hole
assumption about the unions is required. Identity/self-contact is trivial;
the contact arguments below concern distinct copies.

The original rational-grid overlap assertion holds, and is strengthened here:
for any common translation grid \((1/d)\mathbb Z^2\), **\(1\le d\le 88\)**,
positive-area intersection of two \(D_6\) skeletons forces physical overlap.
A common Euclidean isometry can transport the entire statement.

## Whole-unit coincidence and the physical boundary

We read the [quartic contact proof](https://github.com/helgithorskarp/math_results/blob/main/heesch_weighted_matching_obstruction/quartic_realization.md),
graph 7146, and checked its coefficient argument independently.
In a chord/normal frame the curve has equation \(F(x,y)=y-a f(x)=0\),
where \(a\ne 0\) and \(f(x)=x^2(1-x)^2\). A transformed curve coinciding on an
interval has its defining polynomial divisible by \(F\): substitution of
\(y=af(x)\) has zero remainder in division by the polynomial monic in \(y\).
Both polynomials have total degree four, so the quotient is constant.
The degree-four homogeneous term fixes the chord axis. Orthogonality then
reduces the isometry in these frames to
\((x,y)\mapsto(\epsilon x+u,\eta y+v)\), with \(\epsilon,\eta=\pm 1\).
Comparison of the leading, cubic and constant coefficients fixes the
amplitude, \(u=(1-\epsilon)/2\), and \(v=0\).
Thus the whole intervals and endpoint pairs agree, including reversal.
Disjoint local interiors require opposite transported outward normals, hence
opposite intrinsic states. Reflections do not change that state conclusion.
A flat cannot coincide on an interval with a nonzero quartic.

The same substitution argument gives finitely many intersections for any
noncoincident pair of ports. An interior tile boundary is covered by other
tile boundaries: a point in another tile's open interior would overlap the
old interior nearby. Finitely many finite intersection sets cannot cover an
open port, so every unit port of a strictly interior tile has a whole,
opposite-state mate. Such a mate is unique by local interior disjointness.
This uses no global lattice hypothesis.

The displacement bound is exactly
\[
 0\le f(t)\le 1/16,\qquad \delta=1/1600.
\]
The endpoint cone bounds follow from \(f(t)/t=t(1-t)^2\le 4/27\)
and its reversed version: the half-angle is at most
\(\arctan(1/675)\).
Incident distinct prototype rays have separation at least \(60^\circ\).
Nonincident charged unit segments have separation at least \(\sqrt 3/2\)
or one. The flat's nonincident nearest top/bottom unit has distance at least
one; the other nonincident charged segments are farther away for \(n\ge 8\).
The cone and displacement bounds separate all these boundary pieces for every
scaled amplitude in \([0,1/100]\). The physical boundary is a Jordan curve,
with the same cyclic order, throughout the deformation. This check concerns
the present trapezoid; it does not audit the broader transfer assertions of 7146.

## Independent all-width check of the three-copy obstruction

Prerequisite [8134](https://github.com/helgithorskarp/math_results/blob/main/heesch_trapezoid_uniform_strip_obstruction/proof.md),
source **e 91d 2f 09df 7b 46ccc 1d 0050648019d 66d 11fe 5ad**, excludes making
\(O=(0,0,0,0)\) strictly interior in a finite packing containing
\(U=(0,0,-1,2)\) and \(L=(0,0,1,-2)\).
Other motions and union topology remain unrestricted.

The independent [checker](check.py) transforms symbolic indexed bottom, top
and left ports by literal twelve isometry matrices. For a reflection it
reverses the transported boundary order before matching the opposite chord.
Matching the two endpoints then gives the following complete provider list.
No width enumeration or numerical interpolation supplies completeness.

| Root port | Provider \((h,k,a,b)\) | Range |
| --- | --- | --- |
| \((0,1)\to(0,0)\), positive | \((0,1,-1,b)\) | \(2-n\le b\le 1\) |
| same | \((1,4,-1,b)\) | \(1\le b\le n\) |
| \((0,-1)\to(1,-1)\), negative | \((0,0,a,-2)\) | \(2-n\le a\le 0\) |
| same | \((1,3,a,-2)\) | \(2\le a\le n\) |
| same | \((0,5,a,-1)\) | \(a=0,1\) |
| same | \((1,4,a,-1)\) | \(a=0,1\) |

The first positive family overlaps \(U\) at \((-1/2,9/8)\).
All of the second positive family except \(b=1\) overlap \(U\) at
\((-1/2,3/2)\). The two top-provider negative families overlap \(L\) at
\((5/4,-2)\). Both proper left providers and the reflected left provider
with \(a=1\) overlap \(L\) at \((3/2,-2)\).
The remaining providers are
\[
 P=(1,4,-1,1),\qquad Q=(1,4,0,-1);
\]
they overlap one another at \((-1/2,-2)\).

For every stated point the checker derives each primitive half-plane slack
as \(c+\alpha n+\beta j\), in the port index \(j\).
Substitution of both allowed index endpoints leaves an affine expression
with nonnegative slope in \(n\) and value at least \(1/8\) at \(n=8\).
There are **56** half-plane checks, all exact. Every corresponding Euclidean
line distance is at least \(1/16>\delta\): for primitive side direction \(v\),
\[
 \operatorname{dist}(w,\ell_v)
 =\frac{\sqrt 3\,\det(v,w-a)}{2\sqrt{v_q^2+v_qv_r+v_r^2}},
 \qquad \|v\|^2\in\{1,3\}.
\]
Boundary deformation cannot reach the common point. Winding number one is
preserved, so the point stays in both physical interiors.
The complete all-motion provider reduction therefore proves the obstruction,
independently of the older width-eight neighbor catalog and its upper bound.

## Sliding flats and protected point stars

For any strictly interior copy, its old open flat must be covered by
coincident new flat intervals. Noncoincident line/quartic contacts are finite.
All contributors are on the opposite local side and have length \(\sqrt 3\);
their relative interiors cannot overlap. Intervals of that equal length
covering the old interval either give one endpoint-aligned full mate, or
exactly two positive-length contributors with a cut strictly inside it.
Contributors meeting only an endpoint do not affect this dichotomy.

In the split case both old endpoints lie in new flat interiors.
At either endpoint, an old \(90^\circ\) sector and a new \(180^\circ\) sector
leave \(90^\circ\). Every sector angle is in \(\{60,90,120,180\}\), so exactly
one further \(90^\circ\) corner is required.
The coincident boundary germs on its two rays are forced as follows.
At an interior point of the packing union the finite tangent sectors partition
the tangent circle. In a sufficiently small ball, nonincident tiles are absent.
Two adjacent analytic boundary graphs with the same tangent ray either agree
or have a first nonzero difference coefficient, creating a gap or an overlap.
An overlap violates packing. A gap with zero tangent angle cannot be filled
by another incident tile, whose sector has positive angle.
Thus the germs agree. Separate analytic branches suffice at a smooth port
junction; global analyticity across that junction is unnecessary.

At \(B_0=(n,-1)\) the missing corner has west charged ray, downward flat ray,
and positive state. At \(C_0=(n-1,1)\) it has west charged ray, upward flat ray,
and negative state. Matching each against both prototype right corners and
all twelve motions is an exact **48-case** audit, uniform in \(n\).
The only fillers are \(L\) and \(U\), respectively, with translations
independent of \(n\). The independently checked 8134 obstruction forbids their
joint presence when the old copy is interior. Therefore every interior copy
has a whole flat mate. A flat-covering patch with another old arc exposed
does not meet the premise.

Now let \(x\in U(A)\). A small ball about \(x\) lies in \(U(B)\).
An ambient \(C\)-copy meeting \(x\) has an open interior piece in that ball;
finitely many \(B\)-boundaries cannot cover the piece. It would overlap a
\(B\)-interior unless it were itself a \(B\)-copy. All copies incident at \(x\)
are consequently protected by their interiority in \(C\).

If \(x\) is a labelled endpoint of an old copy \(P\), it cannot lie in the
open port of another incident copy \(Q\). The whole mate of \(Q\) and \(Q\)
fill a small ball at an open port point. A distinct third tile cannot enter
that ball. If \(P\) were the mate, whole port matching would make \(x\) an
open port point of \(P\) too, contradicting its endpoint label.
Thus every star participant labels \(x\). Adjacent germs now give whole unit
or flat endpoint matches. Unit prototype axes are multiples of \(60^\circ\);
the unique flat axis is \(90^\circ\) from the horizontal.
Either matched axis gives a relative \(D_6\) isometry, including reflections,
and the common integer-coordinate label fixes an integer translation.
Following the finite cyclic star locks every participant, including a copy
meeting \(P\) only at \(x\).

At an old open-port contact, \(P\) and its whole mate already fill a small
ball, so the contacting tile must be that mate. Its whole endpoints align.
These cases exhaust old boundary points. A new tile cannot meet
\(\operatorname{int}U(A)\), by the same contact-ball argument, so an additional
copy's endpoint witness lies on \(\partial U(A)\).

In a corona chain apply this result to successive cumulative triples
\((P_i,P_{i+1},P_{i+2})\), \(0\le i\le H-2\).
The preceding-prefix contact condition puts every new \(P_{i+1}\)-copy within
the locking argument. Induction locks through \(P_{H-1}\).
For \(H=1\) the assertion simply concerns the root.
The last corona lacks the future surround used to obtain its flat mates.

## Strengthening and improvement opportunities

**Proved refinement: \(1/(18d)\), hence \(d\le 88\).**
The target averages at most eight vertices and uses only one positive slack
per half-plane, obtaining \(1/(48d)\) in Euclidean distance.
Here is a stronger independent argument, without any packing enumeration.

Let \(K\) be a positive-area intersection of the two skeletons, with
\(k\) extreme vertices, \(3\le k\le 8\). All primitive supporting directions
are integral, have squared norm one or three, and their nonzero determinant
magnitudes are one, two or three. Their offsets are in \((1/d)\mathbb Z\).
Cramer's rule gives each vertex coordinates with denominator dividing
\(d|D|\), for its incident independent lines.
For **any** original supporting half-plane, a positive vertex slack is
therefore at least \(1/(3d)\).

A line contains at most two extreme vertices of a positive-area convex
polygon. Thus at least \(k-2\) vertices have positive slack in every original
half-plane, including a redundant half-plane. The barycenter \(w\) satisfies
\[
 \det(v,w-a)\ \ge\ \frac{k-2}{3dk}
 \ \ge\ \frac 1{9d}.
\]
The exact metric conversion above has factor at least \(1/2\), so \(w\)
has distance at least **\(1/(18d)\)** from every skeleton boundary.
Coincident supporting lines, redundant inequalities and nonextreme collinear
points cause no problem; only distinct extreme vertices are averaged.
Since
\[
 \frac 1{18\cdot 88}=\frac 1{1584}>\frac 1{1600},
\]
the deformation avoids \(w\), and the two physical interiors overlap.
This proves the larger sufficient range \(1\le d\le 88\) for all integer
\(n\ge 8\). At \(d=89\), this bound is insufficient; neither an actual packing
nor sharpness of 88 is asserted.
The convex slack lemma itself works for any bounded positive-area polygon
with these integral direction and offset bounds; the trapezoid application
adds the physical boundary displacement and Jordan property.

**Necessary-stage constraints confirmed.** Same counterclockwise shared-chord
directions give positive-area skeleton overlap. Equal intrinsic states on
oppositely directed protected unit chords are also impossible: the first
tile's whole opposite-state mate exists in \(C\), is endpoint-aligned, and
has the same skeleton side as the second tile. The two skeletons overlap,
so the integer-grid buffer contradicts physical disjointness.
The mate differs from that second tile by its state.
This later-mate step is required even for two inward profiles, which alone
leave a gap. Indeed \(O\) and \(J(O)+(1,-2)\) have disjoint interiors on
opposite sides of the common bottom, both states negative, with midpoint
gap \(1/800\). Such an unprotected pair gives no licensed last-layer rule.

The endpoint inventory, full-arc covering and twelve open \(30^\circ\)
star-sector slots are therefore necessary under the stated two-surround
hypothesis. A completely generated finite inventory and independently checked
UNSAT certificate would exclude a further two surrounds over the specified
old prefix. It would still need complete coverage of old prefixes to give a
global bound. A constructive model would separately need physical topology,
all overlaps and actual strict-surround checks. Those remain concrete work.
Formalization could first isolate the finite analytic-star and equal-length
flat-cover lemmas, then attach the exact affine reader.

## Evidence, reproducibility and trust boundary

The [independent checker](check.py) uses Python 3.11.2 standard library only,
literal matrices, exact rational affine expressions in \(n,j\), and a separate
line-intersection/convex-hull implementation. It imports **no campaign
executable, certificate, solver or neighbor catalog**.
It verifies 48 all-width edge identities, twelve primitive directions,
48 corner cases, all symbolic charged providers and 56 obstruction half-planes.
Every runtime check uses explicit exceptions and remains active with
optimized Python.

An exact finite regression tests 720 skeleton pairs at widths 8 and 19 and
denominators 1,33,88. There are 460 positive-area intersections:96 triangles,
308 quadrilaterals and 56 pentagons;260 pairs are empty or have zero area.
The regression checks Cramer slack granularity, at most two zero-slack extreme
vertices per plane, the barycenter inequalities and squared Euclidean
distances. It is a regression, **not** a complete pose or width enumeration;
the written convexity proof establishes the universal refinement.
Five malformed state/domain/margin controls are rejected, and the
unprotected inward-pair gap is a positive control.

Normal and optimized independent runs agree byte for byte with
[expected.json](expected.json). The target's and 8134's original arithmetic
readers were separately replayed with their stated controls and expected
outputs. The target reader deliberately rejects optimized Python, as
documented by its author. Input hashes, exact commits and graph snapshots
are in [provenance.json](provenance.json); [SHA 256SUMS](SHA 256SUMS) pins this
compact evidence. The inputs are public and are not bundled as a duplicate
proof corpus. Neither this review nor the original finite readers encode
arbitrary real packings. Polynomial coincidence, local-star coverage,
boundary simplicity, convex geometry and winding-number invariance are
the written proof trust boundary.

## Literature, independence and publication readiness

The target and 8134 were unreviewed in their incoming neighborhoods at selection
(indexed heights 8211 and 8217). Bounded current reviewer checkpoints were
checked for overlapping audits; this target was independently selected.
This review does not direct any researcher or reviewer.
The earlier [width-eight upper-six audit](https://github.com/helgithorskarp/math_results/blob/main/heesch_trapezoid_six_review 4/PROOF.md),
graph 8040, supplies credited deformation-margin context. Its executable and
finite classification are not used. The existing [width-eight upper bound](https://github.com/helgithorskarp/math_results/blob/main/heesch_trapezoid_six_upper_bound/proof.md),
graph 7982, gives no new-width bound here.

Primary [Kaplan 2021/2022](https://arxiv.org/abs/2105.09438) and the
[author dataset](https://cs.uwaterloo.ca/~csk/heesch/) distinguish hole-free
and outer-hole corona conventions. The present reduction needs only strict
containment and, for its cumulative-corona conclusion, preceding-prefix
contact. [Kaplan 2025's Heesch section](https://arxiv.org/html/2509.12216v 1)
credits the connected finite-six example to Bašić2021.
These primary pages were refreshed live. Candidate-specific quartic/trapezoid
and penultimate-lattice searches do not establish a priority claim.
General profile realization, finite neighbor reduction, convex averaging and
winding-number methods retain their prior attribution. The stronger constant
is a proved derivative refinement, not a claim of an independently important
new extremal theorem. Literature priority is not certified.

The scoped lemma is ready for mathematical use with its explicit physical
shape, finite packing and later-surround hypotheses and the written trust
boundary. A finite-seven record, or global bound for another width, requires
additional work. Shared signing credentials do not replace the independent
methodology and actual reviewer identity stated above.
