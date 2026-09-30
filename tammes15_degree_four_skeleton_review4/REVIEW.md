# Independent review: Tammes-15 degree-four exclusion and the full-range skeleton theorem

Reviewer: **six-reviewer-4**, role: **independent mathematical reviewer**.
Date: 2026-09-30. The shared signing identity does not establish distinct
authorship; this reviewer wrote and ran the independent methods below.

**Verdict: confirmed, with a proved strengthening.** The local theorem and
nine-quadrilateral corollary of six-tammes-1's
[degree-four exclusion](https://github.com/helgithorskarp/math_results/blob/main/tammes15_nine_quad_degree_four_exclusion/PROOF.md)
are correct under their stated geometric hypotheses. Target: lemma h7786,
`bafkreicb2v2lhtmsardhszso4mjifb3rizdabt5g6iar2cqgdsxoeolpl4`;
target source commit `dc8ebfb023d53b5c70e41e8aa886282ef557cf10`.
The audit checks the geometric reduction, every graph and sphere-map case,
the original-point/medial correspondence, and the exact angle obstruction.
It does not certify unrestricted Tammes-15 optimizer coverage or a new
numerical bound.

The target assumes a complete connected contact graph of fifteen distinct
unit points, all degrees four, a cellular sphere decomposition into simple
strictly convex geodesic triangles and quadrilaterals contained in open
hemispheres, and \(1/2<c<3/5\), where \(c=\cos d\). Different
quadrilaterals need not be congruent. Its combined earlier frontier
\(E\le30\) additionally depends on earlier dense, seven-Q and eight-Q
exclusions; those dependencies are not re-certified in this review.

## Proved broader statement

**Contact-skeleton theorem.** Let \(X\) consist of fifteen distinct unit
points, and let \(d>0\). Suppose every distinct pair in \(X\) has
geodesic distance at least \(d\). There is no simple connected graph on
these points that simultaneously has:

1. degree four at every vertex;
2. every selected edge realized by a shorter geodesic arc of length \(d\);
3. a cellular decomposition of the sphere whose faces are simple strictly
   convex geodesic triangles or quadrilaterals, each contained in an open
   hemisphere.

The graph may omit other pairs at distance \(d\). Neither an upper
cosine cutoff nor congruence between different quadrilaterals is required.
Because selected edges exist, \(d\) is the actual minimum separation.
The proof covers its entire possible parameter range
\(113/225\le c<1\). The geometric face and packing assumptions remain
essential to the argument given here.

## Geometric bridge and weak corner bounds

The fifteen disjoint open caps of radius \(d/2\) have total area at most
\(4\pi\). Thus
\[
15\bigl(1-\cos(d/2)\bigr)\le2,
\qquad c=2\cos^2(d/2)-1\ge113/225>1/2.
\]
Distinct points and the existence of edges give \(c<1\). Put
\[
\alpha=\arccos\frac{c}{1+c},\quad
H=1+2c,\quad h=\sqrt H,\quad A=2\pi-2\alpha.
\]
An equilateral triangular face has angle \(\alpha\). For an equilateral
convex hemispherical quadrilateral, opposite angles agree and adjacent
angles are related by the decreasing involution
\[
\rho(u)=2\arctan\frac{1}{c\tan(u/2)}.
\]
These spherical-rhombus identities are classical; they also follow by
splitting the rhombus along its two symmetry diagonals and applying the
spherical cosine law. Strict convexity selects angles in \((0,\pi)\).
For clarity, opposite vertices on either side of a diagonal are the two
unit vectors having equal inner product \(c\) with its endpoints;
reflection in their span interchanges these vectors. The shorter convex
arcs select opposite sides, giving the diagonal symmetries.

At a corner \(u\), the opposite diagonal has cosine
\(c^2+(1-c^2)\cos u\). Its endpoints have distance at least \(d\),
so this cosine is at most \(c\), giving \(u\ge\alpha\).
The adjacent corner also satisfies this bound; since
\(\rho(\alpha)=2\alpha\), the decreasing involution gives
\[
\alpha\le u\le2\alpha. \tag{1}
\]
This derivation uses the separation of all pairs, including unselected
diagonals. It does not use contact completeness. The target's strict
bounds follow when no diagonal is an omitted contact.

For \(1/2<c<1\),
\(\pi/3<\alpha<\arccos(1/3)<2\pi/5\).
The last inequality can be checked exactly from
\(\cos(2\pi/5)=(\sqrt5-1)/4<1/3\).
Consequently a degree-four star cannot contain three triangles:
its angle sum would be at most \(5\alpha<2\pi\).
Four triangles likewise cannot sum to \(2\pi\).
Thus every original vertex has at most two triangular corners, even
under the weak bounds (1).

Distinct convex cells meet properly: at most in a common complete edge
or a single vertex. Indeed, the shorter arc between two points of their
intersection belongs to both cells. A chord interior to either cell
would give overlapping interiors near an interior point of that chord.
The intersection must therefore lie on a boundary great-circle edge of
each cell; strict corners exclude a bend. No original point lies strictly
inside an edge of length \(d\), since it would be closer than \(d\)
to an endpoint. Overlapping edges must consequently be the same full
edge. An additional common vertex off it would again force an interior
chord. This argument holds for a selected skeleton as well.

For a degree-four graph, Euler's identity gives \(E=30,F=17\).
The edge-side equations imply \(T=8,Q=9\).
Every Eulerian graph on the sphere has a checkerboard face coloring:
crossing parity around a simple dual closed curve equals the sum of
primal degrees inside it modulo two, which vanishes. Each color has
thirty edge incidences. Solving \(3t+4q=30\), with \(0\le t\le8\)
and \(0\le q\le9\), gives colors \((t,q)=(2,6),(6,3)\).

Choose centers in the eight faces of the first color, and join the two
opposite chosen-color faces through each original degree-four vertex.
Inside a convex polygon these center-to-corner arcs can be drawn without
crossing. This creates an embedded graph \(G\) on eight vertices, with
fifteen edges and degrees \((3,3,4,4,4,4,4,4)\).
Simple face boundaries exclude loops. Two faces of the same color have
no common edge and, by proper intersections, share at most one original
point, excluding parallel edges. The other-color cells become the six
triangular and three quadrilateral faces of \(G\). Repeated selected
neighbors around such a cell would make two cells share two edges, so
these new face cycles are simple.

Connectivity also follows without a polyhedral uniqueness assumption:
the edges of \(G\) associated with consecutive original vertices of any
original edge share its chosen-color face center. Connectivity of the
original graph therefore connects all edges of \(G\), which has no
isolated vertices. The original map is exactly the medial map of this
embedded \(G\). Its fifteen points are the fifteen distinct edges of
\(G\); a graph edge mask never specifies their metric positions.

## Independent complete finite census

[maps.py](maps.py) imports no author modules. It uses a dynamic remaining
degree generator and **unoriented edge double covers with vertex links**,
rather than the target's rotation-prefix search or its directed-dart
partition audit.

The degree generator finishes the active vertex of greatest remaining
degree, with a deterministic tie break, and chooses all of its remaining
neighbors at once. Each final graph uniquely determines the choice at
every stage. Negative residuals, odd residual sum, or a requirement
greater than the number of available neighbors cannot extend to a
realization. The completed set contains **15,740 labelled masks**.
All \(2!6!=1,440\) permutations preserving the degree classes partition
it into **28 whole orbits**. Every orbit is checked as a subset of the
still-unassigned population, so orbit sizes alone do not establish coverage.

For each representative, enumerate all simple unoriented 3/4-cycles.
Choose six triangles and three quadrilaterals, with every undirected
edge in exactly two distinct faces. Each chosen corner joins the two
incident edge-neighbor labels in the link at its vertex. Reject a link
with degree above two, a duplicated link edge, or a closed component
that does not contain the entire local star. Such a component cannot
subsequently connect to the remaining neighbors. These conditions are
necessary for every valid embedding of a vertex of degree three or four.
They also explain why repeated copies of the same unoriented face are
unnecessary: they would repeat a local link edge.

The search chooses an unfinished edge with the fewest possible
completions and selects all its remaining incident faces together.
For any complete cover, the selected group is uniquely determined.
Edge capacity, remaining face quotas and the exact remaining side-count
equation give sound pruning. Upon completion, all local links are single
cycles and every edge has two face sides. Opposite edge orientations
are propagated over the connected face dual and explicitly checked.
Euler characteristic \(8-15+9=2\) then certifies a sphere, and both
global orientations reconstruct the normalized vertex rotations.

The complete computation has **149 edge-cover recursion states** over
the 28 graph representatives. It recovers **five unoriented sphere
covers, ten oriented maps**. Every entire oriented entry, and every
representative mask and orbit size, agrees with the target's output.
The labelled mask population has normalized SHA256
`e3ae898e0c57c8c06d42a4c47b31440d389225596a1f7b036cec4fbc891fd0b1`.
The reference output is used only for comparisons after independent
generation; it neither selects candidate graphs nor restricts face covers.

[angles.py](angles.py) independently rebuilds the original medial faces
with original points named by lexicographically sorted edges of \(G\).
Eight orientations have a vertex with three triangles and are excluded
by the weak corner bound above. The remaining two orientations have the
same full unoriented face complex, on representative mask 48691568:

\[
\begin{array}{ll}
T:&(0,1,2),(3,5,4),(0,14,1),(3,11,5),\\
  &(6,10,7),(7,12,8),(9,11,6),(13,14,12);\\[2pt]
Q_0:&(6,7,8,9),\quad Q_1:(3,10,6,11),\\
Q_2:&(7,10,13,12),\quad Q_3:(0,8,12,14),\\
Q_4:&(1,14,13,4),\quad Q_5:(2,5,11,9),\\
Q_6:&(1,4,5,2),\quad Q_7:(2,9,8,0),\\
Q_8:&(4,13,10,3).
\end{array}
\]
The comparison checks all cyclic triangle and quadrilateral boundaries,
allowing their reversal, rather than accepting a total or a graph mask.

## Independent projective angle obstruction

Give the even and odd corners of \(Q_i\) slots \(u_{2i}\) and
\(u_{2i+1}\). The nine quadrilaterals give nine \(\rho\)-links.
Each of the nine two-triangle original stars gives an \(S\)-link,
where \(S(u)=A-u\). The incidence-derived closed walk
\[
0,1,4,5,6,7,9,8,12,11,10,3,2,0
\]
has word
\(\rho,S,\rho,S,\rho,S,\rho,S,S,\rho,S,\rho,S\).
After cancellation of adjacent identical involutions it is
\(\rho S\rho\). Thus \(u_1=\rho(u_0)\) is an \(S\)-fixed angle,
so \(u_1=\pi-\alpha\).

The independent checker uses homogeneous pairs over \(\mathbb Q[c]\),
with \(z=\tan(u/2)/h=p/q\). Its two matrices are
\[
R=\begin{pmatrix}0&1\\cH&0\end{pmatrix},\qquad
B=\begin{pmatrix}c&1\\H&-c\end{pmatrix}.
\]
They satisfy \(R^2=cH I\), \(B^2=(1+c)^2 I\).
The full thirteen-step product equals
\(c^2(1+c)^6H^2 RBR\), coefficient by coefficient.
The \(B\)-fixed polynomial factors as
\[
Hz^2-2cz-1=(z-1)(Hz+1),
\]
whose only positive root is 1. This independently obtains \(z_1=1\).

**No unverified denominator argument extends the interval.**
For \(c>0\), both matrices are invertible. At every actual strict
convex corner the half-tangent is positive and finite. Start with the
positive pair \((1,1)\) at slot 1. Applying \(R\) preserves positivity.
For \(B\), the numerator \(cp+q\) is positive; the actual positive,
finite image angle forces the denominator \(Hp-cq\) to be positive.
Induction along each physical angle-link path therefore makes every
generated pair positive. A vanishing or negative denominator is already
an impossibility, rather than an exceptional parameter that can be dropped.

Breadth-first propagation reaches all eighteen slots and checks every
link by homogeneous cross multiplication. The original one-triangle star
at point 2 contains slots 10,13,14. Independent algebra gives
\[
z_{10}=\frac{c}{1-2c^2},\qquad
z_{13}=\frac{1-c-c^2}{c^2}
        =\frac{1-2c^2-c^3}{c^2(1+c)},\qquad z_{14}=1.
\tag{2}
\]
The checker records the actual homogeneous pairs and verifies that the
common factors canceled in these three formulas are nonzero polynomials
with nonnegative coefficients, hence positive for \(c>0\).
In particular, positivity of the slot-10 denominator forces
\(1-2c^2>0\) at any putative realization. No other separation range
is silently discarded.

Since \(u_{14}=\pi-\alpha\), the angle sum at point 2 requires
\(u_{10}+u_{13}=\pi\), equivalently \(Hz_{10}z_{13}=1\).
Exact identities give
\[
Hz_{10}z_{13}-1=\frac{1-3c^2}{c(1-2c^2)},\qquad
z_{10}-\frac1c=-\frac{1-3c^2}{c(1-2c^2)}.
\tag{3}
\]
Thus \(z_{10}=1/c\). As \(\tan\alpha=h/c\) and
\(0<\alpha<\pi/2\), injectivity of the half-tangent on \((0,\pi)\)
gives \(u_{10}=2\alpha\). The same star then gives
\[
u_{13}=\pi-2\alpha<\alpha,
\]
because \(\alpha>\pi/3\). This violates even the weak lower bound
(1), proving the full-range skeleton theorem. The target used the strict
upper bound on slot 10; the strict lower violation at slot 13 proves more.

For an additional exact check, (3) forces \(c^2=1/3\).
Reduction in \(\mathbb Q[c]/(3c^2-1)\) gives
\(z_{13}-1/H=5-9c<0\) at the positive root: \((9c)^2=27>25\).
The reduced fraction's denominator is coprime to \(3c^2-1\).
No floating root, approximate angle or sampled parameter is used.

## Corollaries and dependencies

If a selected T/Q skeleton on fifteen points has exactly nine
quadrilateral faces and degrees in \(\{3,4,5\}\), Euler's equations
give eight triangles and thirty edges, hence
\(n_5-n_3=2E-4\cdot15=0\). The theorem excludes the case
\(n_3=n_5=0\). Therefore \(n_3=n_5\ge1\) throughout the full possible
separation range, under the same geometric assumptions.

The target's combined \(E\le30\) statement below its polynomial cutoff
retains the earlier dependency chain: h7182
`bafkreiflxdrel4fv4opchhucsisp7ylw2lsfgtrv4q7tya3o5vjh4ld53a`,
h7192 `bafkreib7v7j2ex5iccpokhbiav53ufgjf6n5fm4x2dgb5fzgeobye7ykma`,
and h7729 `bafkreihybzsvuctxh6mdyej4d6fls26sd6e5xqajcnmwfsf3gyq73mvq5u`.
This review supplies the degree-four exclusion needed at equality, not
an independent verification of those earlier claims or arbitrary
optimizer coverage.

The newer [nine-Q odd-degree reduction](https://github.com/helgithorskarp/math_results/blob/main/tammes15_nine_quad_odd_degree_reduction/PROOF.md),
h7817 `bafkreic6shrttfdlf7vbae5wye7eytruyxeeb7j6422ubytjcwlaadlkfa`,
uses this exclusion for its lower endpoint \(n_3=n_5\ge1\).
The review supports that specific dependency. Its upper endpoint
\(n_3\le3\), its parameter cutoff and its 32 necessary profiles are
not audited here. In particular this review's full-range corollary does
not extend that separate upper endpoint or profile census.

## Reproduction and trust boundaries

Use CPython 3.11 or newer and SymPy 1.14.0. From this directory, run
`python3 -B audit.py --check` and `python3 -B -O audit.py --check` with
all native thread counts set to one, as specified in [README.md](README.md).
The unified entry point regenerates the entire census before the angle
audit; it never relies on a privately precomputed map population.
[provenance.json](provenance.json) pins the target's compact source inputs.
[EXPECTED.json](EXPECTED.json) contains the independently obtained
complete representative/map output, all homogeneous vectors and paths,
and exact obstruction identities. It is a bytewise comparison fixture,
not a proof input.

Positive controls include the tetrahedron, octahedron and triangular
prism, each giving one unoriented sphere cover and two orientations,
and global reflection of the original target faces. Seven negative
controls reject a wrong orbit size, a missing Q, a reused Q vertex,
a fake closed walk, a wrong original star, a wrong critical slot and
a changed full face complex. All checks use exceptions and remain
active under optimized Python. The original author's normal checker,
optimized checker and separate directed-cycle audit also reproduced
their respective expected outputs exactly; these author runs supplement
the independent methods.

The result is an exact computer-assisted proof with a written geometric
reduction. It is not formalized in a proof assistant. Trust includes
CPython's exact integers, SymPy's polynomial arithmetic, the inspected
independent algorithms and the geometric arguments above. No author
rational-arithmetic kernel is reused. Hash checks detect input changes,
but do not themselves establish a mathematical premise. The printed
integer-coefficient homogeneous vectors permit further independent
arithmetic checking.

## Literature and novelty assessment

The rhombus angle facts are classical; see Musin and Tarasov,
[The Tammes problem for N=14](https://arxiv.org/abs/1410.2536),
Proposition 3.2. That result concerns fourteen points. The related
classification by Yuan and Wang,
[Tilings of the sphere by congruent regular triangles and congruent rhombi](https://arxiv.org/abs/2311.01183),
explicitly requires congruent rhombi. The current theorem allows the
nine rhombi to vary and imposes the pairwise packing constraint.
Neither paper is asserted to establish or refute this specific theorem.

Candidate-specific primary-source and committed-graph searches found
no matching independent audit or previously cited full-range skeleton
exclusion. That is a bounded search, not proof of historical priority.
The confirming audit and the stronger hypothesis/parameter statement
are distinct from novelty of the classical geometric facts. The written
proof and compact reproducible evidence are ready for further referee
inspection; no journal acceptance or exhaustive priority claim is made.

## Strengthening and improvement opportunities

**Proved:** remove contact completeness and the arbitrary upper bound
\(c<3/5\), including the closed lower cap bound \(c=113/225\).
The essential new step is the forbidden *lower* angle at the sole
remaining medial face complex. The positive homogeneous propagation
closes the pole issue on the full possible parameter range. The
nine-Q lower degree-count corollary extends with it.

**Concrete next proof work:** for nine-Q graphs containing degree-three
and degree-five vertices, prove geometric feasibility or impossibility
of the necessary odd-degree profiles. Such graphs need not be Eulerian;
the eight-vertex checkerboard cover is not an exhaustive reduction for
that remaining branch. The newer h7817 count reduction supplies a
conditional finite starting point, not completed contact maps.

**Independent certification opportunity:** the census can be formalized
as an undirected surface-gluing checker with single-cycle vertex links,
and the homogeneous identities as coefficient lists over the integers.
This would reduce software trust. The separate geometric bridge, cap
bound and weak rhombus inequalities must also be formalized to obtain
a theorem about actual sphere points; certifying only matrix identities
would leave that bridge open. Removing strict convexity, open-hemisphere
faces or the all-pairs separation constraint is not proved here.
