# Proof: unit-edge dominating triples are four-colourable

## 1. Statement and normalization

A plane unit-distance graph has distinct points as vertices and edges only
between points at Euclidean distance exactly one; it may omit some such edges.
A set dominates when every vertex outside it has a neighbour in the set.

Let

\[
a_0=0,\qquad a_1=1,\qquad c=z,
\]

and write (C_d=\{x:|x-d|=1\}). We prove four-colourability of the
strict graph on

\[
X=\{a_0,a_1,c\}\cup C_{a_0}\cup C_{a_1}\cup C_c. \tag{1}
\]

The new case has three distinct centres and
(|c-a_0|,|c-a_1|\ne1). Coincident centres reduce to two circles. If a
second centre edge is present, the three-centre graph is connected and the
accepted connected-dominating-triple theorem applies. These boundary cases
are combined in Section 7.

Pin the centre colours to

\[
\operatorname{col}(a_0)=2,\qquad
\operatorname{col}(a_1)=3,\qquad
\operatorname{col}(c)=0. \tag{2}
\]

Put (omega=(1+i\sqrt3)/2) and
(U=\{1,\omega,\ldots,\omega^5\}).

## 2. The two binary orbit colourings

On one unit circle, two points are unit-separated exactly when their
owner-relative directions differ by (omega) or (omega^{-1}). Thus
each (U)-orbit is a six-cycle and admits either binary phase.

For the two circles centred at (a_0,a_1), choose a bit
(alpha_O) on every (U)-orbit (O) of directions. If
(p=a_i+\omega^k u), define

\[
f_A(p)=\alpha_{[u]}+i+k\pmod2. \tag{3}
\]

This is well-defined away from the two centres and is proper on the full
unit-distance graph induced by the two circles. Same-circle edges change
(k) by one. For a noncentre cross-circle edge, the unit-rhombus lemma gives

\[
p-a_0=q-a_1,
\]

so the owner index changes by one. At either common circle point the two
owner descriptions in (3) agree for the same reason.

Independently, choose a phase (eta_O) for each direction orbit on (C_c)
and put

\[
f_C(c+\omega^k v)=\beta_{[v]}+k\pmod2. \tag{4}
\]

This properly two-colours every six-cycle on the third circle.

A finite set of prescribed values for (3), or for (4), is feasible unless
two prescriptions in the same direction orbit demand different phases. Its
**conflict graph** partitions the prescribed points by direction orbit and,
inside each orbit, joins the phase-0 demands to the phase-1 demands. Hence a
conflict graph is exactly a disjoint union of complete bipartite graphs.

## 3. Allocate the mixed intersections

Let

\[
Z=C_c\cap(C_{a_0}\cup C_{a_1})
\]

be the set of mixed-owner points. There are at most four: each of the two
circle pairs has at most two intersections.

First suppose no point of (Z) lies on both (A)-circles. Then
(Z=Z_0\mathbin\dot\cup Z_1), where a point of (Z_i) is owned by
(a_i,c) and (|Z_i|\le2). Allocate every mixed point either to palette
(A=\{0,1\}) or to palette (C=\{2,3\}).

* If (p\in Z_i) is allocated to (A), require (f_A(p)=1), avoiding
  the colour 0 of centre (c).
* If (p\in Z_i) is allocated to (C), require
  (f_C(p)=1-i), so its actual colour (2+f_C(p)=3-i) avoids the
  colour (2+i) of centre (a_i).

Let (E_A) join pairs that cannot both receive the first allocation, and
let (E_C) join pairs that cannot both receive the second. By Section 2,
both are disjoint unions of complete bipartite graphs. If (Z_i) has two
points, its pair is in (E_A) exactly when it is in (E_C): the two
owner-relative direction changes have opposite signs but the same parity.

The following finite lemma is therefore applicable, padding a part with
isolated dummy vertices if necessary.

**Parity-allocation lemma.** Partition four labelled vertices into two
specified pairs. Let (E_A,E_C) each be a disjoint union of complete
bipartite graphs, and suppose the two graphs agree on the two within-pair
edges. A labelling of each vertex by (A) or (C), containing no
(E_A)-edge inside (A) and no (E_C)-edge inside (C), exists except
for two graph pairs. In either exception both within-pair edges occur, and
the cross edges of (E_A,E_C) are the two complementary perfect matchings.

The producer represents every such graph by a set partition and one binary
label on each vertex. It obtains 29 distinct conflict graphs and 251 ordered
graph pairs satisfying the within-pair agreement. Directly testing all 16
allocations leaves only masks

\[
(E_A,E_C)=(45,51),(51,45), \tag{5}
\]

in lexicographic pair order
((01,02,03,12,13,23)). The independent checker instead examines all
(2^6) graph masks and recognizes the complete-bipartite-component property
by graph traversal. It reproduces all counts, allocation histograms, and
(5). This 251-case finite lemma is the computer-assisted step.

## 4. Geometry removes the two abstract exceptions

Let the two points of (Z_i) be (p,q), and put
(d_i=|c-a_i|>0). Their common chord satisfies

\[
|p-q|^2=4-d_i^2. \tag{6}
\]

The within-pair edge lies in the conflict graphs precisely when the two unit
directions differ by an odd power of (omega). For distinct centres and
distinct intersection points, (6) then has chord square one; the antipodal
odd power would force (d_i=0). Consequently

\[
\{p,q\}\in E_A\quad\Longleftrightarrow\quad
\{p,q\}\in E_C\quad\Longleftrightarrow\quad d_i^2=3. \tag{7}
\]

Both abstract exceptions in (5) require (7) for (i=0,1). Writing
(c=x+iy), subtraction of

\[
x^2+y^2=3,\qquad (x-1)^2+y^2=3
\]

gives

\[
c=(1\mathbin\pm i\sqrt{11})/2. \tag{8}
\]

At (8), let (d_0=c), (d_1=c-1), and let (delta) be their smaller
oriented angle. The cosine law gives

\[
\cos\delta=\frac{3+3-1}{2\cdot3}=\frac56,
\qquad 0<\delta<\frac{\pi}{3}. \tag{9}
\]

An intersection direction based at (a_i) differs from (d_i) by
(\pm\pi/6). A direction based at (c) differs by
(\pm5\pi/6). Therefore every cross-(i) relative angle, in either
palette, belongs modulo (2\pi) to

\[
\delta-\frac{\pi}{3},\quad\delta,\quad
\delta+\frac{\pi}{3}. \tag{10}
\]

For points with different (A)-owners, a conflict needs an **even** power
of (omega), hence an angle (0) or (\pm2\pi/3). The three open
intervals in (10), using (9), contain none of those values. Thus (8) has no
cross conflicts at all. Its actual conflict masks are both 33, and it has
four palette allocations. Neither abstract exception (5) is geometrically
realizable.

The checker also evaluates the three cosines in (10) exactly as

\[
\frac56,\qquad\frac{5+\sqrt{33}}{12},\qquad
\frac{5-\sqrt{33}}{12},
\]

and confirms directly on a 35-vertex orbit patch that every strict unit edge
is properly coloured.

## 5. Triple-owned intersections

Now suppose (t\in Z) lies on all three circles. Because the centres
(a_0,a_1,c) have colours (2,3,0), the point (t) is forced to palette
(A) with colour 1. There are at most two other mixed points, one for each
circle pair.

For one forced vertex and two remaining vertices, the direct allocation
table has 16 systems. It is unsatisfiable only if the forced point
(A)-conflicts with **both** other points and those other points
(C)-conflict; an optional additional (A)-conflict between them changes
nothing. These are masks ((3,4)) and ((7,4)) in pair order
((01,02,12)).

The two conflicts incident with (t) again imply, by (7), that
(|c|=|c-1|=\sqrt3), so (c) must be (8). But the only common points of
(C_0,C_1) are

\[
t=(1\mathbin\pm i\sqrt3)/2,
\]

and their squared distances from the two points (8) are

\[
\frac{7\mathbin\pm\sqrt{33}}2,
\]

never one. Hence the one-triple abstract exceptions are also physically
impossible. With fewer other mixed points an allocation is immediate.

If both common points of (C_0,C_1) were also on (C_c), then (c) would
be an intersection of their two unit circles. Those intersections are
exactly (0,1), contrary to the three-distinct-centre hypothesis. Thus no
additional triple case exists. The checker reconstructs the exact example
(c=\omega+i), whose mixed set is
(\{\omega,i,1+i\}), and checks its complete 32-vertex orbit patch.

## 6. Colour every point and every edge

Choose a valid allocation of (Z). For each (A)-direction orbit meeting
an (A)-allocated point, choose the unique phase required in Section 3.
Do the same for every (C)-direction orbit meeting a (C)-allocated point.
The definition of the two conflict graphs guarantees consistency. Choose
phase zero on every other orbit.

Colour the noncentre points of (1) as follows:

* an (A)-only point uses colour (f_A\in\{0,1\});
* a (C)-only point uses colour (2+f_C\in\{2,3\});
* a mixed point uses its allocated rule.

This is well-defined. Two noncentre points using palette (A) both lie in
the two-circle graph coloured by (3), so any unit edge between them is
proper. Two using palette (C) both lie on (C_c), so (4) handles their
unit edge. Points using different palettes have different colours.

Every noncentre neighbour of (a_i) that uses palette (A) has colour
0 or 1. A mixed neighbour allocated to (C) has colour (3-i\ne2+i).
Every noncentre neighbour of (c) allocated to (A) has the required
colour 1, while every other one has colour 2 or 3. The only centre edge in
the new case is (a_0a_1), whose endpoint colours are different. This
checks all edges of the entire infinite support, not merely the finite
intersection set or orbit patches.

## 7. Dominating-graph corollary and scope

If a finite unit-distance graph has a dominating triple containing an edge,
normalize that edge to (0,1). Every other vertex lies in (1), so restricting
the full-support colouring proves four-colourability in the exactly-one-edge
case. If the third centre has an edge to either endpoint, the dominating
triple is connected and the accepted connected-triple theorem applies.
Coincident or redundant centres reduce to the accepted two-centre theorem.

Therefore no five-chromatic plane unit-distance graph has a dominating triple
containing an edge. This is a structural global necessary condition, not a
vertex lower bound. An independent dominating triple remains open. No claim
is made about domination by four vertices or about points not dominated by
the named centres.

The universal geometric argument is written mathematics. The finite
parity-allocation lemma is exhaustive exact computation, independently
replayed by a different graph characterization. Exact orbit patches are
controls rather than the basis of the universal quantifier. Trust remains in
the proof, the elementary circle lemmas, CPython, and rational
multiquadratic arithmetic. There is no solver, floating-point predicate, CAS,
or omitted negative certificate.
