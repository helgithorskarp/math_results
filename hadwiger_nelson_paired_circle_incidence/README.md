# Paired unit circles: four-colourability outside explicit incidence curves

Fix a unit complex number \(r\). For four distinct centres
\[
A=\{0,1\},\qquad B=\{t,t+r\},
\]
let \(H_{r,t}\) be the unit-distance graph on the **entire union of their four
unit circles**. This includes all four centres, each lying on its partner's
circle. Segment interiors may intersect.

**Theorem.** An explicit product \(P_r(X,Y)\) of 22 factors, defined below,
has degree 108 and leading homogeneous part
\[
104976(X^2+Y^2)^{54}.
\]
If \(P_r(\Re t,\Im t)\ne0\), then \(H_{r,t}\) is four-colourable.
Consequently, for each fixed orientation, every non-four-colourable placement
lies on the specified algebraic exceptional set. Its complement is open,
dense and of full planar measure.

The factors need not be distinct or irreducible, and degree 108 is not claimed
minimal. The exceptional set is an **outer bound**: membership does not prove
failure of all four-colourings. The criterion comes from one particular
colouring construction. No five-chromatic graph with at most 508 vertices is
established.

For the nonparallel orientation \(r=(3+4i)/5\), the
[compact certificate](certificate.json) gives every factor over
\(\mathbb Q(\sqrt3)\). Conjugate factors pair, so their product belongs to
\(\mathbb Q[X,Y]\). A checker using a separate determinant derivation verifies
all 48 ordered signed-incidence identities, accounting for the complete
22-factor list. The proof below also applies to other unit orientations,
including the parallel ones; those symbolic parameters are handled by the
written argument, not inferred from the fixed-orientation computation.

## 1. Orbit colouring on one pair of circles

Write \(\omega=(1+i\sqrt3)/2\) and \(U=\{\omega^k:0\le k<6\}\).
Consider two unit-separated centres \(a_0,a_1\), with both centres themselves
removed from their circle union.

For each \(U\)-orbit of unit directions choose a representative \(v\) and a
phase \(\alpha_v\in\{0,1\}\). At a point \(x=a_i+\omega^k v\), set
\[
f(x)=\alpha_v+i+k\pmod2.                                      \tag{1}
\]
This is well-defined and is a proper two-colouring:

* A point owned by both circles is an equilateral intersection. Its two
  owner-relative directions differ by \(\omega\) or \(\omega^{-1}\);
  the change of owner index compensates for the odd exponent.
* A unit chord on one circle changes the exponent by \(1\) or \(-1\).
* If \(x\in C(a_0,1)\), \(y\in C(a_1,1)\), \(|x-y|=1\), and neither is a
  removed centre, then \(y=x+a_1-a_0\). Thus the directions agree and
  the owner indices differ.

For the last assertion, \(a_0,y\) are the intersections of the two unit
circles centred at \(x,a_1\). They are distinct because the centre was removed;
their sum is \(x+a_1\), by reflection in the midpoint of the two centres.
The case \(x=a_1\) was also removed. This includes tangencies: a tangent would
give only the excluded point.

These are the elementary unit-pair geometry and orbit parity used in the
[preceding paired-circle kernel](../hadwiger_nelson_paired_circle_kernel/README.md)
and the independently accepted
[unit-path theorem](../hadwiger_nelson_dominating_unit_path/README.md).
They are repeated here to make this reduction self-contained.

## 2. The exact signed conflict for one colouring procedure

Pin the four centre colours to
\[
c(0)=2,\quad c(1)=3,\quad c(t)=0,\quad c(t+r)=1.
\]
Let \(Z\) consist of all **noncentre** points belonging to an A circle and a
B circle. There are at most eight such points.

We try the following construction:

* Every noncentre point owned by A, including all of \(Z\), receives the
  A-palette colour \(f_A(x)\in\{0,1\}\) from (1).
* A noncentre point owned only by B receives \(2+f_B(x)\), where \(f_B\)
  is any orbit colouring (1) on the B pair.

A point \(x\in Z\) owned by \(a_i=i\) and \(b_j=t+jr\) must have
\[
f_A(x)=1-j                                                     \tag{2}
\]
to avoid the colour of \(b_j\). These are the only additional conditions.
All other noncentre A/B edges join disjoint palettes. An A centre's B-owned
noncentre neighbour would be in Z, hence already uses the A palette.
Same-group edges follow (1), and all centre-centre edges have distinct pins.

For each orbit, equations (2) merely prescribe the same binary phase.
They are consistent exactly when there is no pair of incidences
\[
\begin{split}
x&\in C(i,1)\cap C(t+jr,1),\\
y&\in C(h,1)\cap C(t+lr,1),\\
y-h&=\omega^k(x-i),\qquad i+h+j+l+k\equiv1\pmod2,              \tag{3}
\end{split}
\]
with \(x,y\) noncentres. The points may coincide and may have multiple owners;
all owner incidences are included. Indeed their required orbit phases differ
by \(i+h+j+l+k\). If there is no conflict, assign the prescribed phase on each
constrained orbit and choose zero on the others. Representatives may be chosen
by argument in the half-open interval \([0,\pi/3)\).

Thus (3) is an exact obstruction to this stated orbit-phase procedure. It is
not an obstruction to arbitrary graph colourings, to all two-palette
procedures, or even to every colouring allowed by the earlier finite kernel.
In particular, this procedure requires all mixed-owner points to use A's two
colours, which the earlier kernel did not require.

## 3. Eliminating the intersection direction

A slot is \(a=(i,j)\in\{0,1\}^2\). Order slots as
\(00,01,10,11\). For slots \(a=(i,j)\), \(b=(h,l)\), put
\[
d=t+jr-i,\qquad e=t+lr-h,\qquad
v=R_{-k\pi/3}e,
\]
viewing complex numbers as real vectors. Define
\[
q=|d|^2,\quad w=|e|^2,\quad H=d\mathbin{\cdot}v,\quad
F_{a,b,k}=qw(q+w-2H-4)+4H^2.                                  \tag{4}
\]
Every collision (3) implies \(F_{a,b,k}=0\).

To see this without dividing by a possibly zero determinant, put \(u=x-i\).
Then \(|u|=1\), and the two circle conditions are
\[
2d\mathbin{\cdot}u=q,\qquad2v\mathbin{\cdot}u=w.
\]
Writing \(\Delta=\det(d,v)\), define
\[
N_x=qv_y-wd_y,\qquad N_y=wd_x-qv_x.
\]
These equations imply \(N=2\Delta u\), even when \(\Delta=0\).
Consequently
\[
|N|^2-4\Delta^2=0.
\]
Expanding gives (4), since \(|v|^2=w\) and \(\Delta^2=qw-H^2\).
No division, squaring of an untracked sign, or nonsingularity assumption is
used for the necessary condition.

There is also an exact reconstruction on a nonsingular locus: if \(F=0\)
and \(\Delta\ne0\), then \(u=N/(2\Delta)\) has norm one and satisfies both
dot equations. The points \(x=i+u\), \(y=h+\omega^ku\) realize the incidence.
They give a conflict when neither is a centre and the displayed parity is odd.
At \(\Delta=0\), or when a reconstructed point is a centre, polynomial
vanishing alone is not used as a converse.

For a repeated slot \(a=b\), odd \(k\) is necessary. If \(k=1,5\), equation
(4) is \(q^2(q-3)\). If \(k=3\), it is \(4q^3\).
Since the four centres are distinct, \(d\ne0\), so the latter case is
impossible. Equivalently, the two distinct circle intersections have
directions summing to \(d\), and an odd 60-degree separation forces \(q=3\).
A repeated point cannot have a nonzero rotation exponent.

## 4. The complete 22-factor outer set

For each of the four slots include
\[
Q_{ij}=|t+jr-i|^2-3.
\]
For each of the six **unordered distinct** slot pairs \(a<b\), include (4)
for each of the three \(k\in\{0,\ldots,5\}\) with
\(i+h+j+l+k\) odd. Define
\[
P_r=\prod_{i,j\in\{0,1\}} Q_{ij}\;
    \prod_{\substack{a<b\\i+h+j+l+k\ {\rm odd}}}F_{a,b,k}.       \tag{5}
\]

There are 48 ordered odd slots among the \(4\cdot4\cdot6=96\) total slots.
The 12 self slots reduce to four Q factors and four impossible \(k=3\)
slots. The remaining 36 slots pair under
\((a,b,k)\leftrightarrow(b,a,-k)\); their polynomials are identical by (4).
They give 18 factors. This proves completeness of (5), with no search over
placements or truncated root enumeration.

Each Q has degree two and leading part \(X^2+Y^2\).
There are four distinct-slot \(k=0\) factors. In each, exactly one binary
index changes, so \(e=d+c\) with \(|c|=1\). Their Cramer expression has degree
four and leading part \((X^2+Y^2)^2\): its leading vector is
\(|t|^2c-2(t\mathbin{\cdot}c)t\), of squared norm \(|t|^4|c|^2\).
The determinant correction has degree at most two.

For \(k\ne0\), (4) has degree six and leading part
\[
2(1-\cos(k\pi/3))(X^2+Y^2)^3.
\]
There are eight factors with \(k=2,4\), four with \(k=1,5\), and two with
\(k=3\). Therefore no factor is identically zero, for **any unit r**, and
\[
\deg P_r=4\cdot2+4\cdot4+14\cdot6=108,\qquad
{\rm lead}(P_r)=3^8\,4^2(X^2+Y^2)^{54}.
\]
If \(P_r(t)\ne0\), no signed conflict is possible, so Section 2 constructs a
four-colouring of the entire support. Restricting it colours every finite
unit-distance graph on that support, regardless of size.

A nonzero real polynomial's zero set is closed, has empty interior and has
planar measure zero. For example, regarding it as a polynomial in Y, all
nonexceptional vertical fibres have finitely many zeros; the exceptional X
values are contained in the finite zero set of a nonzero coefficient.
This proves the stated generic consequence. The theorem still assumes the
four centres distinct; the four forbidden translations \(0,1,-r,1-r\) are
not silently included.

## 5. Exact nonparallel specialization and controls

Fix \(r=(3+4i)/5\). The certificate lists all 22 factors without expanding
their product: four quadratic, four quartic and fourteen sextic factors,
with **570 nonzero rational coefficient terms** in \(X,Y,\sqrt3\).
Its term format is
\([X\text{-exponent},Y\text{-exponent},\sqrt3\text{-exponent},n,d]\),
representing \(nX^aY^b(\sqrt3)^s/d\), with reduced rational \(n/d\).
Conjugation exchanges \(k\) with \(-k\); the Q, \(k=0\) and \(k=3\) factors
are rational individually. Hence (5) is rational.

At \(t=(1+2i)/5\), **all 22 factors are nonzero**. The four cross squared
centre distances, in slot order, are
\[
1/5,\quad52/25,\quad4/5,\quad37/25.
\]
Each lies strictly between zero and four, so all four cross-circle pairs
have two intersection incidences. This witness is inside the interacting
region, not a case of circles from opposite groups being too far apart.
The theorem colours its full support without a graph solver.

The common-midpoint placement \(t=(1-r)/2=(1-2i)/5\) is an explicit boundary
control. Let
\[
x=\frac{1+2\sqrt{19}}{10}
  +i\frac{-2+\sqrt{19}}{10},\qquad y=1-x.
\]
Then \(x\) is unit from centres \(0,t\), and \(y\) is unit from \(1,t+r\).
Neither is a centre, and \(y-1=-x=\omega^3x\).
The slots \(00,11,k=3\) have odd parity. Equation (1) gives equal A-palette
colours to x and y, while their B-centre neighbours demand 1 and 0.
Thus the specific procedure fails here. Also \(v=d\), so this is a genuine
singular incidence, not evidence that singular cases can be discarded.
Four exact unit distances and the parity conflict are checked using
\(\mathbb Q(\sqrt{19})\).

**The full graph at that boundary placement was not tested.** No
non-four-colourability, lower chromatic bound, kernel-list failure, or finite
candidate claim is inferred from this control.

## 6. Reproduce and evidence boundary

Python 3.11.2 and the standard library suffice. From this directory, with
fresh output directories:

~~~sh
sha256sum -c SHA256SUMS
python3 build.py --out work/build
python3 verify.py --out work/check
python3 -O verify.py --out work/check-optimized
~~~

The producer multiplies sparse polynomials over
\(\mathbb Q[S]/(S^2-3)\) and expands (4).
The [independent checker](verify.py) imports no producer or parent code.
It evaluates the Cramer determinant expression directly using pairs of exact
rational field elements and recursively generated rotations. It checks each
of the 48 ordered signed slots against the certified polynomial on a 7-by-7
integer grid. Both expressions have degree at most six in each variable.
Successive univariate root bounds therefore turn these **2,352 exact
evaluations into complete polynomial identities**, not sampled geometric
evidence. This includes the self-factor reductions and reverse-slot symmetry.

The checker also validates the coefficient domain, all leading homogeneous
forms, degrees, exact conjugate-factor matches, all 22 witness values, the
eight intersection incidences, and the singular midpoint control. Seven
malformed certificates are rejected: missing factor, wrong slot parity,
altered coefficient, false witness value, wrong degree, false record flag
and damaged midpoint coordinate. Normal and optimized reports agree exactly.

The final [certificate](certificate.json) is **11,040 bytes**, SHA-256
~~~text
ee51e8cf1517bd2885d3c74d7b5ccaa74418593e5e9910bf948bcab56021febb
~~~
[expected.json](expected.json) gives the exact audit report;
[validation.json](validation.json) records execution and source context.
No native solver, CAS, floating-point test, external mathematical data,
omitted large certificate or background computation is a premise.
The general geometric argument and polynomial degree proof remain written
mathematics. The executable fixed-orientation audit trusts CPython exact
integer/Fraction arithmetic, field-basis independence and the interpolation
degree bound. Author-run algorithmic independence is not external review;
independent review of this new result is pending.

## 7. Campaign boundary

This closes the generic translation family for paired unit circles and
replaces an undirected two-dimensional placement search with a necessary
explicit incidence condition. It does not classify colourability on the
exceptional curves, assert that every paired-circle support is four-colourable,
or certify that the degree-108 outer set is smallest.

The [preceding kernel](../hadwiger_nelson_paired_circle_kernel/README.md)
remains available for actual exceptional placements and permits mixed-owner
vertices all four colours. Its 204-point bound and sufficient extension
criterion are compatible with this stronger restriction on a particular
colouring procedure. No new translation grid, larger denominator, second
orientation, full exceptional curve search, or midpoint graph query was run.

The teammate's [503-point endpoint colouring](../hadwiger_nelson_heule503_endpoint/README.md)
and [accepted one-pair Kempe classification](../hadwiger_nelson_heule560_kempe_review1/README.md)
were inspected as coordination context, not mathematical dependencies.
That lane's support family was not duplicated.

The record baseline is [Parts's 509-vertex construction](https://arxiv.org/abs/2010.12665),
also identified as the current record in the introduction of
[Haugland's August 2026 manuscript](https://arxiv.org/html/2608.04542v4);
both were checked live on 6 September 2026. No priority claim is made.
The next unstarted task is to select and analyse one actual exceptional
nonparallel placement or incidence stratum, with unrestricted graph colouring
kept separate from this procedure's failure. This pass ends at the complete
incidence-reduction checkpoint.
