# Shared-midpoint unit segments have four-colourable circle neighbourhoods

**Theorem.** Let two unit segments have the same midpoint. The unit-distance
graph on the entire union of the four unit circles centred at their endpoints
is four-colourable. When the four endpoints are distinct, **every prescription
of four pairwise distinct centre colours extends** to this entire support.

Equivalently, every Euclidean unit-distance graph with a dominating set
consisting of the four corners of a rectangle whose diagonals have length one
is four-colourable. Edges in this statement have length exactly one, and a
dominating set means that every other vertex has a neighbour in it.

For four distinct centres, the
[preceding paired-circle kernel](../hadwiger_nelson_paired_circle_kernel/README.md)
has at most **108 actual vertices** in this family, and this bound is sharp
for that kernel definition. At
\[
A=\{0,1\},\quad r=(3+4i)/5,\quad t=(1-r)/2=(1-2i)/5,\quad B=\{t,t+r\},
\]
the kernel has exactly **108 vertices and 294 unit edges**. The compact
certificate supplies 16 proper listed colourings, one for each antipodal
transversal used by the proof.

This closes the **whole common-midpoint family**, including every orientation,
not just the displayed rational example. Sharpness concerns kernel order;
no exact chromatic lower bound, minimal kernel, or five-chromatic graph is
claimed. In particular, there is no improvement to the 509-vertex target.

## 1. Normalization and ownership

Translate the common midpoint to the origin. The distinct endpoints lie on
the circle of radius \(1/2\) and form a rectangle. After a rotation and, if
necessary, a reflection, label them
\[
a_0=(a,b),\quad a_1=(-a,-b),\qquad
b_0=(a,-b),\quad b_1=(-a,b),
\]
where \(a,b>0\) and \(a^2+b^2=1/4\). The A and B pairs are the unit diagonals.
This covers every nondegenerate common-midpoint placement.

Say a centre owns a point when their distance is one. Every point has at most
two owners among the four centres. Indeed, for a fixed point \(z\), ownership
by a centre \(c\), where \(|c|=1/2\), is equivalent to
\[
2z\mathbin{\cdot}c=|z|^2-\tfrac34.
\]
For \(z\ne0\), this is a line intersecting the centre circle in at most two
points. For \(z=0\), it has no solution.

Let Z be the points with an owner in both groups. Each of the four cross
centre separations is either \(2a\) or \(2b\), strictly between zero and one.
Thus each pair of unit circles has two intersections. The owner bound makes
all eight points distinct, each with exactly one A owner and one B owner.
None is a centre. Central reflection \(z\mapsto-z\) pairs them and toggles
both owner indices.

## 2. Four distinct direction orbits

Let \(\omega=(1+i\sqrt3)/2\) and \(U=\{\omega^k:0\le k<6\}\).
We prove that, for either group, the eight owner-relative directions from Z
have exactly four U-orbits, each represented by **one antipodal pair of
points in Z**.

Put
\[
u=\sqrt{1-b^2},\qquad v=\sqrt{1-a^2}.
\]
The four points of Z owned by \(a_0=(a,b)\) are
\[
E=(a+u,0),\quad W=(a-u,0),\quad
N=(0,b+v),\quad S=(0,b-v).
\]
Their directions from \(a_0\) all have norm one. No two of these directions
lie in the same U-orbit, as the following strict distance bounds show.

Set \(A=au\), \(B=bv\). Since \(a,b<1/2\) and \(u,v<1\),
\(0<A,B<1/2\). Also
\[
u^2-4a^2=3b^2>0,\qquad v^2-4b^2=3a^2>0,
\]
so \(A+B>2(a^2+b^2)=1/2\). We therefore have
\[
\tfrac12<A+B<1,\qquad |A-B|<\tfrac12.
\]
The six squared pair distances are:

| Pair | Squared distance | Strict interval |
| --- | --- | --- |
| E,W | \(4u^2\) | \((3,4)\) |
| N,S | \(4v^2\) | \((3,4)\) |
| E,N | \(2+2(A+B)\) | \((3,4)\) |
| W,S | \(2-2(A+B)\) | \((0,1)\) |
| E,S | \(2+2(A-B)\) | \((1,3)\) |
| W,N | \(2-2(A-B)\) | \((1,3)\) |

Two unit directions in a common U-orbit have squared chord distance in
\(\{0,1,3,4\}\). Every displayed interval avoids that set.

Every other point of Z is the central reflection of one of these four,
owned by \(a_1\). Its direction is the negative of the original direction,
which belongs to the same U-orbit since \(-1=\omega^3\).
Hence these are exactly the four A direction orbits, with no additional
identifications. Reflection in a rectangle axis proves the same statement
for B. No angle enumeration or generic-position assumption is involved.

## 3. Two-circle orbit colouring

For a pair of unit-separated centres \(c_0,c_1\), remove the two centres
themselves from the union of their unit circles. Choose a representative w for
each U-orbit of unit directions and a phase \(\alpha_w\in\{0,1\}\).
For a point \(x=c_i+\omega^k w\), set
\[
f(x)=\alpha_w+i+k\pmod2.                                      \tag{1}
\]
This is well-defined and proper on that two-circle graph:

* A point owned by both circles is an equilateral intersection. Changing
  owners changes the direction by \(\omega\) or \(\omega^{-1}\), so both
  the owner index and exponent parity change.
* A unit chord on one circle changes the exponent by \(1\) or \(-1\).
* A unit edge between the two circles, with neither endpoint a removed centre,
  preserves the owner-relative direction and changes the owner index.

For the last fact, normalize the centres to \(c_0,c_1\) and take
\(x\in C(c_0,1)\), \(y\in C(c_1,1)\), \(|x-y|=1\).
The points \(c_0,y\) are the two distinct intersections of unit circles
centred at \(x,c_1\). Their sum is \(x+c_1\), hence
\(y-c_1=x-c_0\). The excluded-centre cases are exactly the degeneracies needed
for this assertion.

This is the elementary pair geometry from the earlier
[unit-path theorem](../hadwiger_nelson_dominating_unit_path/README.md) and
[incidence reduction](../hadwiger_nelson_paired_circle_incidence/README.md),
repeated here for a self-contained colouring proof. Representatives can be
chosen by arguments in the half-open interval \([0,\pi/3)\).

## 4. Split each antipodal pair between the palettes

Pin the centre colours to
\[
c(a_i)=2+i,\qquad c(b_j)=j.
\]
Choose **one point from each of the four antipodal pairs in Z** and call the
chosen set T. There are 16 such transversals.

For \(x\in T\), owned by \(a_i,b_j\), prescribe
\[
f_A(x)=1-j.
\]
For \(x\in Z\setminus T\), owned by \(a_i,b_j\), prescribe
\[
f_B(x)=1-i.
\]
Section 2 says each A orbit has exactly one prescribed point and each B
orbit also has exactly one prescribed point. Thus these prescriptions set
phases in (1) independently, with no conflict. Choose arbitrary phases,
for example zero, on unconstrained orbits.

Colour the complete circle support as follows:

* At a noncentre point owned only by A, use \(f_A(x)\in\{0,1\}\).
* At a noncentre point owned only by B, use \(2+f_B(x)\in\{2,3\}\).
* On T use \(f_A(x)=1-j\).
* On \(Z\setminus T\) use \(2+f_B(x)=3-i\).
* At the centres use the four pins above.

Any two noncentre vertices using the same palette belong to that group's
two-circle graph and obey (1); vertices using different palettes have
different colours. An A centre's noncentre neighbour either uses A's palette
or is a mixed point assigned \(3-i\), different from its centre colour
\(2+i\). A B centre's noncentre neighbour either uses B's palette or is a
mixed point assigned \(1-j\), different from its centre colour j.
All centre-centre edges have distinct pins.

This proves properness on **all points and all unit edges** of the infinite
support. A global palette permutation gives any prescribed four distinct
centre colours. Restriction gives the finite-graph and dominating-rectangle
corollaries.

If the two segments coincide, only two distinct centres remain. Colour their
noncentre circle union by (1) with colours 0,1 and their centres by 2,3.
Thus the degenerate orientations \(r=\pm1\) also have four-colourable supports.
The four-distinct-centre prescription and the kernel bound below apply only
to nondegenerate placements.

## 5. A sharp 108-point kernel bound

Use the earlier kernel definition: let \(S_A\) contain the A diagonal's
intrinsic U-orbit and every cross-intersection direction orbit relative to
its A owner; define \(S_B\) analogously. Put
\[
P_A=(a_0+S_A)\cup(a_1+S_A),\quad
P_B=(b_0+S_B)\cup(b_1+S_B),\quad P=P_A\cup P_B.
\]
The centres are already in P. By Section 2, each direction set has four
cross orbits and at most one additional intrinsic orbit, so
\(|S_A|,|S_B|\le30\).

Within either pair, the two translates overlap in exactly the two
equilateral intersections, both present through the intrinsic orbit.
Moreover, \(P_A\cap P_B\) is exactly Z, since every point common to the
patches is owned by both groups and all eight cross intersections are
included. Therefore
\[
|P|=(2|S_A|-2)+(2|S_B|-2)-8\le108.
\]
No assumption that intrinsic and cross orbits are disjoint is used.

The full-support colouring above restricts to the earlier kernel's lists:
A-only noncentres use \(\{0,1\}\), B-only noncentres use \(\{2,3\}\),
mixed noncentres may use all four colours, and the centres have their pins.
Thus the earlier sufficient list criterion succeeds throughout this family.

For \(r=(3+4i)/5\), \(t=(1-2i)/5\), both direction sets have 30 distinct
directions, each paired patch has 58 points, and their intersection has eight
points. The exact certificate verifies **108 distinct actual points**.
This attains the bound; it does not prove that 108 points are necessary for
some chromatic obstruction or that no smaller sufficient kernel exists.

## 6. Exact certificate and independent audit

The pilot on the fixed rational orientation produced a listed colouring with
a deterministic backtracker in 109 search nodes. That positive result was
then replaced for publication by the explicit orbit construction: the
[producer](build.py) computes all 16 transversal colourings without a solver.

The [certificate](certificate.json) stores the eight exact cross-circle
intersections, kernel counts and hashes, centre labels, four antipodal pairs,
owner-group masks, and the 16 colour strings. It is **3,162 bytes**, SHA-256

~~~text
523ad8d9922a5e3ac6d2ff1a648cff37b4705a69b3d870f4579f9d722c6486b0
~~~

Coordinates belong to \(\mathbb Q(\sqrt3,\sqrt{19})^2\).
The producer uses sparse squarefree radicals with exact rational
coefficients and the two-circle midpoint/root formula.
The [independent checker](verify.py) imports no producer or parent executable.
It uses fixed integer coefficient arrays in the basis
\((1,\sqrt3,\sqrt{19},\sqrt{57})\), with coordinate denominator 20.
Squared unit distance is exactly \((400,0,0,0)\).

The checker does **not** repeat the producer's intersection formula.
It verifies the four rational squared centre separations
\((1/5,4/5,4/5,1/5)\), proves from their range that each pair has exactly two
intersections, and checks that two distinct supplied points lie on both
circles. It then reconstructs all directions, actual points and every unit
edge. The canonical streams have SHA-256:

~~~text
points: 87a52869f7242473c654cd6e968470e5908acace12d79305f3f6fb02d7056daa
edges:  f294b04715440a6fd8c583000699ce035ba54bf970fd557135da8220735fac02
~~~

Exact checks include:

| Check | Count |
| --- | ---: |
| Actual point-pair norms | 5,778 |
| Unit edges in the kernel | 294 |
| Positive edge inequalities across all colourings | 4,704 |
| Antipodal transversals | 16 |
| Mixed-point colour prescriptions | 128 |
| Owner-direction checks | 116 |
| Orbit-phase consistency checks | 1,728 |

The checker additionally confirms that each group's four cross-direction
orbits consist of precisely the four antipodal pairs. Phase consistency is
checked with a different ordering of orbit representatives from the producer.
All eight malformed controls are rejected: missing intersection, missing
transversal, invalid coordinate, monochromatic colouring, false point hash,
wrong orientation, damaged antipodal pair and false size bound.

## 7. Reproduction and trust boundary

Python 3.11.2 and its standard library suffice. From this directory, choose
fresh output directories:

~~~sh
sha256sum -c SHA256SUMS
python3 build.py --out work/build
python3 verify.py --out work/check
python3 -O verify.py --out work/check-optimized
~~~

Normal and optimized checks produce identical
[expected.json](expected.json) reports. Timings and source context are in
[validation.json](validation.json). The certificate and producer regenerate
byte for byte. No native solver, CAS, floating-point calculation, external
coordinate input, omitted large trace or background computation is needed.

The universal theorem is the written orbit-separation and colouring argument,
not an inference from the single rational orientation. The executable audit
checks that example, all its 16 transversals, and attainment of the kernel
bound. Trust remains in the written Euclidean argument, exact Python
integer/Fraction arithmetic, squarefree-basis independence, canonical
encoding and direct colour checks. Algorithmic independence in an author-run
audit is not independent peer review or proof-assistant formalization.
External review of this result is pending.

## 8. Campaign consequence and stopping boundary

The previous
[degree-108 incidence reduction](../hadwiger_nelson_paired_circle_incidence/README.md)
gave a common-midpoint example that defeated a **one-sided** orbit procedure.
That failure remains correct: putting all mixed points in one palette creates
opposite demands within each antipodal orbit. Splitting each antipodal pair
between the palettes resolves it and proves the actual full support
four-colourable for every orientation.

This result closes the shared-midpoint construction family and all its
subgraphs for the five-chromatic target. It does not close arbitrary paired
unit-segment placements, classify the rest of the incidence locus, or apply
to larger circle sets merely because a subset of their centres forms a
rectangle. No other exceptional translation or orientation was searched.

The teammate's
[complete 72-state H560 separator interface](../hadwiger_nelson_heule560_separator/README.md)
was read as durable coordination context. Its remaining selector relations
stay in that separate support-certification lane and are not mathematical
dependencies here.

The baseline remains
[Parts's 509-vertex construction](https://arxiv.org/abs/2010.12665), also
identified as the current record in the introduction of
[Haugland's August 2026 manuscript](https://arxiv.org/html/2608.04542v4).
Both were checked live on 6 September 2026. A targeted literature search did
not supply a matching earlier result; no priority claim is made.

This pass ends at the completed whole-family proof and certificate.
Do not enumerate more common-midpoint orientations or their subgraphs.
The next unstarted geometric question concerns a different part of the
exceptional incidence set, such as a cross-centre separation of \(\sqrt3\),
with actual graph colouring kept distinct from restricted-procedure failure.
