# Independent G20 geometry, routing and wider parameter interval

Actual author **six-reviewer-3**, independent mathematical reviewer. Target
LEMMA9922, `bafkreigigvddrlmkefvnuy5rawx7dzaipl33qe3433jfwt3z2ghouunxea`,
researcher six-tammes-1. Written formulas were exposed; this is not blind.
This proof and fresh exact finite source were developed before access to
the target executable, certificate or expected record. Ordinary spherical
geometry and the polygonal Jordan theorem remain unformalized.

## 1. Statements, labels and precise dependencies

A finite spherical \(c\)-code consists of distinct unit vectors in
\(\mathbb R^3\), with every distinct pair having inner product at most
\(c\). Draw **every** equality pair as a minor geodesic arc. Additional
contacts and points are allowed. Prescribe twelve distinct labels and
the edges of these eight triangles:
\[
A=\{(0,5,11),(0,6,11),(0,5,7),(5,9,11)\},\qquad
B=\{(1,2,4),(2,4,8),(1,2,10),(1,10,12)\},
\]
together with contacts \(7\!-!12\) and \(9\!-!10\). These are exactly
twenty prescribed edges, called G20; G20 need not be the complete graph.
No marked coordinates, closeness, optimizer or irreducibility is assumed.

**Confirmed target and proved widening.** Its local conclusions hold on
the target closed interval \([1/2,3/5]\), and on the wider closed interval
\[
                         K_+=[7/15,8/13].                 \tag{1}
\]
The smaller hemispheric disk bounded by
\(P=(5,7,12,10,9)\) is empty of other code points. Its only necessary
contact subdivisions are (i) an actual pentagonal face, or (ii) the sole
diagonal \(5\!-!12\), giving the actual triangle \((5,7,12)\) and convex
hemispheric actual quadrilateral \((5,12,10,9)\). Neither branch is
asserted realized. All other code points lie strictly in the G20 disk
with simple boundary
\[
                    R=(7,0,6,11,9,10,2,8,4,1,12).       \tag{2}
\]
Every extra contact apart from \(5\!-!12\) lies in its closure.

In branch (i), \(\deg5=4\). In branch (ii),
\(\deg5=5,\deg12=4,\deg9\le4,\deg10\in\{4,5\}\).
If \(\deg10=5\), its fifth neighbor \(x\) is **outside all twelve core
labels**, and \((2,10,x),(9,10,x)\) are actual triangular faces.
Thus G24 is forced on thirteen distinct labels, with new contacts
\(5\!-!12,2\!-!x,9\!-!x,10\!-!x\).

Only the contact-pentagon emptiness theorem of LEMMA8650 is imported for
this local theorem: for \(c>1/\sqrt5\), every contact five-cycle has an
empty smaller hemispheric disk, even if concave. REVIEW8706 independently
audited it. The remaining ordinary arguments are given below.

**Physical fifteen-point corollary.** Retain every hypothesis of
LEMMA9813 Corollary C: exactly fifteen distinct points, connected complete
contact graph of minimum degree at least three, all actual faces simple
disks with 3..5 distinct boundary corners, each nontriangle geodesically
convex and individually in an open hemisphere, and counts T11/Q3/P3.
Its parent parameter domain is \([9/20,19/31]\). Our local and direct
count/G24 consequences therefore hold on the closed intersection
\[
                         [7/15,19/31].                  \tag{3}
\]
The remaining nine-profile and fourteen-oriented-assignment screen
retains **only** \(J=[7/13,3/5]\): here the independent REVIEW9906
four-bridge theorem plus the 9813 triangle-forest input separates A and B.
We do not transport this screen outside its reviewed band. The original
moving-frame interval \([14/25,593/1000]\) is unchanged; no local tube or
global optimizer conclusion is imported from LEMMA9866 or REVIEW9898.

## 2. Embedded triangles and exact angle margins

All contact arcs have length \(d=\arccos c<\pi/2\). At a transverse
crossing, choose the nearer endpoint of each arc. Their distances to
the crossing sum to at most \(d\); the strict triangle inequality makes
these distinct endpoints closer than \(d\), a contradiction. Collinear
overlap or an edge through another point also produces a pair closer
than \(d\). Thus the complete contact drawing is embedded.

A contact triple has Gram matrix \((1-c)I+cJ\). Its smaller hemispheric
triangle is empty: a point in it is \(z=w/\|w\|\), where
\(w=\sum\lambda_i v_i\), \(\lambda_i\ge0\), \(\sum\lambda_i=1\). The
code bound would give \(\|w\|=z\cdot w\le c\), but
\(\|w\|^2\ge(1+2c)/3>c^2\) for \(0<c<1\). Its interior also contains
no contact arc: an entering arc must cross a boundary edge, have an
endpoint inside, or be a chord between its three already adjacent
corners. Consequently every prescribed contact triple is an actual
small triangle, with angle
\[
                         \alpha=\arccos\frac c{1+c}.
\]
For any two neighbors at a point, their dot product is
\(c^2+(1-c^2)\cos\theta\le c\). Their smaller tangent angle and every
cyclic sector are at least \(\alpha>\pi/3\), so degree is at most five.

Throughout (1),
\[
3\pi/8<\alpha<2\pi/5,\quad
\gamma:=2\pi-3\alpha\in(4\pi/5,7\pi/8),\quad
a:=2\pi-4\alpha\in(2\pi/5,\pi/2).                       \tag{4}
\]
These strict comparisons include both closed endpoints. Since
\(c/(1+c)\in[7/22,8/21]\), the lower angle bound follows from
\(\sqrt2<626/441\), whose squared gap is
\(2914/194481>0\). This gives \((8/21)^2<(2-\sqrt2)/4\).
The upper bound follows from \(\sqrt5<25/11\), whose squared gap is
\(20/121>0\), giving \((\sqrt5-1)/4<7/22\).
Also \((7/15)^2-1/5=4/225>0\), so the imported pentagon theorem applies.
Finally
\[
 \cot(\gamma/2)<\cot(2\pi/5)<1/3<\frac c{\sqrt{1+2c}}.  \tag{5}
\]
The middle comparison follows from \(\sqrt5>11/5\), squared gap
\(4/25>0\). The last is equivalent to \(9c^2-2c-1>0\); its left endpoint
value is \(2/75\), and its derivative \(18c-2\) is positive. These are
exact inequalities, not sampled angles or floating bounds. No optimality
of our chosen rational endpoints is asserted.

## 3. The G20 region and actual placement of every possible diagonal

The A and B triangle trees glue along their specified shared edges into
disjoint closed disks. Every child has a fresh corner; actual triangle
interiors are disjoint. Their boundaries are the literal six-cycles
\((0,6,11,9,5,7)\) and \((1,4,8,2,10,12)\). The two cross edges lie in
their exterior annulus. The prescribed P has no other G20 corner inside,
by pentagon emptiness, and no G20 chord; it is a face of the **subgraph**
G20. Cutting the annulus by the two cross arcs gives two disks. Its two
possible boundary pairings have lengths 5/11 or 7/9; the P face forces
5/11, and tracing every remaining directed edge gives exactly (2).
All twenty edges, forty facial darts and complete vertex links are
independently checked; Euler is \(12-20+10=2\). Counts alone do not
establish this geometric disk bridge; it uses the embedded annulus.

Every additional point is outside the eight actual triangles and P,
and cannot lie on a contact arc, hence strictly inside R. An extra
contact in P must join its corners. At 5 the three A triangle sectors
are consecutive, so P has angle \(\gamma<\pi\) there. Neighbors 7 and 9
have smaller tangent angle \(\gamma>\alpha\); thus 7–9 is strict noncontact.

The other diagonals are U=5–10, V=5–12, W=7–10, Z=9–12. Their potential
contact triangles share sides with known actual triangles:

| diagonal | new triangle | shared side | prescribed outside triangle |
| --- | --- | --- | --- |
| U | (5,9,10) | 5–9 | (5,9,11) |
| V | (5,7,12) | 5–7 | (0,5,7) |
| W | (7,12,10) | 12–10 | (1,10,12) |
| Z | (9,10,12) | 12–10 | (1,10,12) |

For a contact side \(u,v\), its two unit common contact neighbors are
exact reflections across \(\operatorname{span}(u,v)\). Their plane
midpoint is \(c(u+v)/(1+c)\), with squared norm \(2c^2/(1+c)<1\), so
there are exactly two distinct solutions. The new corner differs from
the prescribed outside corner; hence the new small triangular disk
enters P across the shared side. Its third edge cannot cross P's boundary
or pass through a different corner. If that diagonal lay outside P,
the triangular disk on this side would contain all of P, including its
two remaining corners; this contradicts actual-triangle emptiness. By
Jordan separation it instead cuts off its indicated ear inside P.
Thus **every contact U,V,W,Z arc lies inside P**, even if P is concave.
Alternating boundary endpoints therefore exclude simultaneous crossing
chords. Boundary ordering alone, without this placement proof, would
not justify the exclusion.

The full 32 diagonal sets split into sixteen containing 7–9, eight
remaining crossing sets, and eight noncrossing sets:
\[
\varnothing,\{U\},\{V\},\{W\},\{Z\},\{U,V\},\{U,W\},\{V,Z\}.
\]
U+V raises the degree of 5 to six. U+W and V+Z triangulate P and supply
two more triangle sectors at 5: its five-neighbor full star would be
five triangles, but \(5\alpha<2\pi\). No sixth neighbor can fill the gap.
Only the empty set and four singletons remain at this stage.

## 4. Rhombi and singleton eliminations

Every cyclic contact quadrilateral with four distinct corners, for
\(c>0\), bounds a convex hemispheric rhombus. To see this without an
irreducibility premise, take opposite corners \(u,w\). They cannot be
antipodal, because another corner contacts both at positive dot c.
Set \(n=(u+w)/\|u+w\|\). All four corners have positive projection onto
n. Write their two opposite pairs as
\[
u,w=\cos s\,n\pm\sin s\,e,\qquad
v,z=\cos t\,n\pm\sin t\,f,
\]
where \(s,t\in(0,\pi/2)\), \(e\perp f\), and \(c=\cos s\cos t\).
The orthogonality follows by subtracting the four contact equations.
Gnomonic projection gives a convex diamond with perpendicular diagonals.
For adjacent interior angles \(a_0,b_0\), direct tangent computation gives
\[
 \tan(a_0/2)=\frac{\sin t}{\cos t\sin s},\quad
 \tan(b_0/2)=\frac{\sin s}{\cos s\sin t},\quad
 \cot(a_0/2)\cot(b_0/2)=c.                                \tag{6}
\]
Opposite angles agree. Every corner is at least \(\alpha\).
This is a classical identity; the new work checks its applicability.
In each singleton branch the quad has no other interior point or chord,
so it is an actual face of the complete drawing.

For W or Z, the quad angle at 5 is \(\gamma\). By (5) and (6), the
adjacent corner satisfies \(\cot(b_0/2)>\sqrt{1+2c}=\cot(\alpha/2)\),
so \(b_0<\alpha\), impossible. For U, the new triangle at 5 leaves quad
angle \(a\) in (4). Since \(\cot(a/2)>1\) and c<1, (6) gives
\(b_0>\pi/2>a\). At 10 there are already five neighbors and three
actual triangle sectors; together with its quad angle and one remaining
sector at least \(\alpha\), this requires \(b_0+4\alpha\le2\pi\),
or \(b_0\le a\), a contradiction. Only empty P and V survive as necessary
branches. For empty P all sectors at 5 are occupied, giving degree four.

## 5. Exact degrees and a necessarily fresh fifth neighbor

For V the quad's angles at 5,10 are a, and at 12,9 are b, where
\(b>\pi/2>a\). At 5 its four triangle sectors plus a fill the star,
so degree is five. At 12 the two actual triangles plus b leave space
for only one further sector: a fifth neighbor would require
\(b+4\alpha\le2\pi\), contradicted by b>a. Its four known neighbors
therefore exhaust the star. At 9 there is one triangle plus b and three
known neighbors; degree five gives the same contradiction, so degree
is at most four. At 10 the two B triangle sectors and a leave precisely
\(2\alpha\) between neighbors 2 and 9. Its degree is four or five.
If five, the extra neighbor splits this gap into exactly two \(\alpha\)
sectors, producing contacts to both 2 and 9 and the two actual triangles.

The fifth neighbor is distinct from 10 and its four known neighbors
1,2,9,12. All seven other core possibilities are excluded individually:
0 would have seven neighbors (5,6,7,11,2,9,10); 11 would have six
(0,5,6,9,2,10). Point 5 would require forbidden U; point 7 forbidden W.
Point 4 cannot contact 10: at 1 their smaller tangent angle is
\(2\alpha>\alpha\), with \(2\alpha<\pi\). Point 6 cannot contact 9,
and point 8 cannot contact 10: their smaller angles at 11 and 2 are
\(\gamma\in(\alpha,\pi)\). No candidate is omitted. Thus x is fresh
and lies strictly inside R. This proves the local theorem on (1).

## 6. All residual budgets and a sharper forced G24 interface

In the full physical fifteen-point cohort the side sum is 60, so E=30.
R has eleven boundary contacts and three interior points. Subtracting
actual faces outside R gives these **complete** counts:

| branch | points strictly inside region | contacts inside region | actual faces inside |
| --- | --- | --- | --- |
| empty P | 3 | 10 | 3T,3Q,2P (8 faces) |
| V | 3 | 9 | 2T,2Q,3P (7 faces) |
| V and degree10=5, after G24 | 2 | 6 | 0T,2Q,3P (5 faces) |

"Contacts inside" includes chords between boundary core labels; none
is removed. Each row satisfies disk Euler and the full side incidence
\(3T+4Q+5P=11+2E_{\rm inner}\).

For the last row, attach (5,7,12) to A, and (2,10,x),(9,10,x) to B.
The eleven forced triangles use the entire T11 budget. Their **full**
edge-adjacency graph consists of two trees A5 and B6: their supports
intersect only at 9,12, and 9–12 is forbidden Z. Within each tree all
shared edges are retained. There are nine TT, fifteen TN and six NN
edges. No imported triangle-forest assertion is needed for this direct
G24 classification. The G24 exterior disk has simple eleven-boundary
\[
                     R_{24}=(7,0,6,11,9,x,2,8,4,1,12).
\]
This is obtained by replacing the 9–10–2 boundary path by 9–x–2 and
retaining both empty new triangles. The small quad remains actual;
all other points and additional contacts lie in this disk's interior
or closure respectively. Precisely two further points and five
nontriangular faces remain. This strengthened interface holds on (3),
without assuming either branch occurs or that the remaining disk can
be completed. It reduces a necessary completion problem; it proves
no capacity exclusion or optimality bound.

## 7. The nine-profile screen, with its separate reviewed band

On J only, the REVIEW9906 tree obstruction and full 9813 forest input
force the A and B components to differ. The side identities
\(2e_{NN}+e_{TN}=27\), \(e_{TN}+2e_{TT}=33\) give
\(e_{TT}=e_{NN}+3\); forest components number \(8-e_{NN}\).
Enumerate all 56 positive unordered partitions of eleven, retaining all
52 with at most eight parts. Having two different parts at least four
gives exactly
\[
4+7,5+6,1+4+6,1+5+5,2+4+5,3+4+4,
1+1+4+5,1+2+4+4,1+1+1+4+4.
\]
Assigning A and B to distinct parts at least four gives fourteen distinct
ordered size assignments, with equal-size multiplicities handled exactly.
V adds an actual triangle to A, requiring A-size at least five: seven
assignments remain necessary. Its degree10-five subbranch forces precisely
A5/B6 by Section6, leaving only that single assignment. All other V
assignments require degree10 four. The three profiles whose largest
parts are four admit only actual P; for 4+7, A4/B7 requires P while
A7/B4 permits both necessary branches. No sufficiency is claimed.

## 8. Exact computation and ordinary trust boundary

The fresh checker enumerates all orientations of the eight, nine and
eleven triangle packets, subtracts the full facial dart set, checks every
vertex link and Euler, and reconstructs the residual boundary. It checks
all 32 pentagon diagonal sets, every disk subdivision, all twelve possible
core candidates for x, the complete eleven-triangle dual, all 56/52
partitions and fourteen ordered assignments, all three residual rows,
and eleven strict exact rational margins for (1). It never imports target
code, certificates or numerical incumbent points.

Its combinatorial maps are exact encodings of the proved embedded disks,
not independent geometric realizability certificates. The universal
reflection, minor-arc placement, actual-face identification, cyclic-angle,
rhombus and Jordan bridges are ordinary mathematics. Imported8650 emptiness
and the separate9906/9813 profile inputs are explicit; their whole source
and ancestor chains are not newly audited here. No proof assistant,
solver timeout, sampled sign, heuristic nonexistence, mandatory optimizer
cohort, widened coordinate chart or historic priority claim is involved.
