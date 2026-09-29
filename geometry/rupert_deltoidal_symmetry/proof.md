# Exact exclusions for symmetry-axis passages of the deltoidal hexecontahedron

Author: six-rupert-1, researcher. Date: 2026-09-29.

Let $K$ be the standard deltoidal hexecontahedron, with McCooey's
coordinates reproduced by the five cyclic signed families in `verify.py`.
Write $s=\sqrt5$, $\phi=(1+s)/2$, and

$$u_2=(0,0,1),\qquad u_3=(1,1,1),\qquad u_5=(1,0,\phi).$$

Let $P_j$ be the orthogonal shadow along $u_j$, considered in an oriented
Euclidean plane. These represent the twofold, threefold, and fivefold
symmetry axes. Other axes of the same order give congruent shadows. An
axis means an unoriented line: distances below are the smaller spherical
angle after allowing the sign of its unit vector to change.

**Restricted exclusion lemma.** No two exact symmetry-axis shadows of $K$
give a Rupert passage, for any planar rotation and translation. If the
two axes have different orders, the same exclusion holds when each is
perturbed by an angle at most $1/1000$ radians.

**Exact scale lemma.** For the fivefold shadow inside the threefold
shadow, the largest scale allowing closed containment, with planar
rotation and translation optimized, is

$$\kappa_{5\to3}
 =\frac4{\sqrt{10+2\sqrt5}+\sqrt3(5\sqrt5-11)}.
 \tag{1}$$

Exact rational enclosures give
$0.971679451840<\kappa_{5\to3}<0.971679451841$.
This is a restricted projection-pair optimum, not the Nieuwland constant
of $K$. Neither lemma establishes that $K$ is globally non-Rupert.

**Local contact lemma.** Fix any one of the three symmetry-axis outer
orientations. Every nonzero three-dimensional rotation of angle at most
$1/10$ radians makes the inner shadow fail even closed containment in
that fixed outer shadow. In particular these three orientations are
not locally Rupert in Scott's sense. This is an exclusion for a fixed
outer orientation, not a claim about two outer and inner axes moving
together.

## Centering and exact shadow invariants

The standard passage criterion is strict inclusion of one orthogonal
shadow, after planar rigid motion, into the other. Since $K=-K$, both
shadows are centrally symmetric about zero. If $\lambda A+t\subseteq B$
for such convex sets, reflection gives $\lambda A-t\subseteq B$;
averaging yields $\lambda A\subseteq B$. The same argument applies to
strict containment. Thus translations do not improve the scale.
This is the centering observation of Steininger--Yurkevich, Proposition 2,
not a new result here.

For a polygon $P$, write $r(P)$ for its centered circumradius, $\iota(P)$
for its centered inradius, and $A(P)$ for its area. The checker proves
the following expressions using exact operations in $\mathbb Q(\sqrt5)$:

| Shadow | Vertices | $r(P)^2$ | $\iota(P)^2$ | $A(P)^2$ |
|---|---:|---|---|---|
| $P_2$ | 12 | $(25+10s)/9$ | $(95+40s)/41$ | $(138100+48000s)/1089$ |
| $P_3$ | 12 | $(70+30s)/27$ | $(715+315s)/302$ | $350/3+50s$ |
| $P_5$ | 20 | $5$ | $(335+145s)/142$ | $(16250+4750s)/121$ |

For clarity, no approximate convex hull is an input to this verification.
An exact monotone-chain construction finds each hull. For every hull
edge from $v$ to $w$, the vector $n=(w-v)\times u$ is an outward normal;
the checker verifies $n\cdot x\le n\cdot v$ for all 62 solid vertices.
Euclidean metric quantities use the three-dimensional orthogonal
projector $T_u=I-uu^t/(u\cdot u)$. In particular,

$$r^2=\max_v\|T_uv\|^2,\quad
 \iota^2=\min_{(v,w)}\frac{(n\cdot v)^2}{n\cdot n},\quad
 A^2=\frac{\big(\frac12\sum_{(v,w)}u\cdot(v\times w)\big)^2}{u\cdot u}.$$

## The fivefold-to-threefold optimum

The shadow $P_3$ has twelve vertices at equally spaced angles of $30$
degrees. Their radii alternate between

$$r=\sqrt5\quad\hbox{and}\quad
 a=\frac{5+3s}{3\sqrt3}.$$

All twelve edges are at the same distance $b$ from zero. Around each of
the six vertices of radius $r$, the adjacent outward normals are at
angles $-\delta,+\delta$ relative to that vertex, where

$$\tan\delta=\frac{r-a\cos30^\circ}{a\sin30^\circ}
 =\frac{\sqrt3}{\phi^4},\qquad b=r\cos\delta.\tag{2}$$

Consequently the twelve normal directions are two regular hexagons
offset by $2\delta$. The checker verifies the radii, angular spacing,
and the common squared distance $b^2=5/(1+3/\phi^8)$.

The shadow $P_5$ contains a regular decagon $D$ of circumradius $r$.
Its other ten vertices lie halfway between successive decagon vertices
and have common radius $\rho<99r/100$. These structural properties are
also checked exactly.

Now reduce the outer normal directions modulo the $36$-degree spacing
of $D$. A regular hexagon of normals becomes three residues spaced by
$12$ degrees. The two hexagons together therefore have alternating
gaps

$$2\delta-24^\circ,\qquad 36^\circ-2\delta.$$

We have $12^\circ<\delta<15^\circ$, so the second gap is the larger.
For any rotation of $D$, one of the twelve normals is within

$$t=18^\circ-\delta$$

of a decagon vertex. Conversely, placing the decagon phase at the
midpoint of a largest gap makes the smallest such angular distance
exactly $t$. Equivalently,

$$\min_\alpha\max_{n\in N_3}h_{R_\alpha D}(n)
 =r\cos(18^\circ-\delta),$$

where $N_3$ contains unit outward normals of $P_3$. This is a covering
argument on the circle of length $36$ degrees; it optimizes over every
planar rotation, not a grid of rotations.

The ten additional vertices of $P_5$ cannot affect this optimum:
$t<6^\circ$ implies $r\cos t>99r/100>\rho$. At the phase just constructed
all their supports are at most $\rho$, while the largest support of $D$
is $r\cos t$. Thus the optimized largest support for the full $P_5$ is
also $r\cos t$. Since every side of $P_3$ is at distance $b$, the optimal
closed scale is

$$\frac b{r\cos t}
 =\frac{\cos\delta}{\cos(18^\circ-\delta)}
 =\frac1{\cos18^\circ+\tan\delta\sin18^\circ}.$$

Using $\cos18^\circ=\sqrt{10+2s}/4$ and
$\sin18^\circ=(s-1)/4$ gives (1). In particular the scale is below one:
the two terms in the final denominator are strictly greater than
$19/20$ and $3/40$, respectively, so $\kappa<40/41<1$.

Here are elementary bounds used in the circle argument. Exact field
inequalities give $\tan\delta>1/4$ and
$\tan\delta<2-\sqrt3=\tan15^\circ$. With $\pi<22/7$,
$\tan12^\circ\le x/(1-x^2/2)<1/4$ for $x=22/105$.
Also $\cos6^\circ\ge1-(\pi/30)^2/2>99/100$.

## The other symmetry-axis pairs

Strict containment forces a strict area inequality. It also forces a
strict circumradius inequality, and it forces the inner inradius to be
strictly smaller than the outer inradius. For the last assertion, a
centered disk of radius $\iota(A)$ lies in $A$; it cannot lie strictly
inside a polygon with a supporting side at smaller distance.
The exact invariant table gives:

| Inner to outer | Obstruction |
|---|---|
| $2\to3$, $2\to5$ | $r(P_2)>r(P_3)>r(P_5)$ |
| $3\to2$ | $A(P_3)>A(P_2)$ |
| $3\to5$ | $r(P_3)>r(P_5)$ |
| $5\to2$ | $\iota(P_5)>\iota(P_2)$ |
| $5\to3$ | exact optimized scale (1) is less than one |
| equal orders | congruent polygons have equal area |

This exhausts the nine ordered pairs.

There is also a global necessary restriction on the *inner* direction.
The maximum-radius vertices of $K$ are its twelve fivefold-axis
vertices, with squared radius $R^2=(25+10s)/9$. If an inner direction is
perpendicular to any of them, its centered shadow has circumradius
$R$, while every outer shadow has circumradius at most $R$. Hence no
strict passage can use that inner direction, regardless of the outer
direction. Thus the six great circles perpendicular to the fivefold
axes are excluded. This uses the elementary circumradius obstruction.

## Explicit neighborhoods for axes of different orders

If an axis moves through angle at most $\varepsilon$, choose the
minimal three-dimensional rotation aligning it with its original
axis. After identifying the projection planes by that rotation, the
Hausdorff distance between the two shadows is at most

$$\eta=R\varepsilon.$$

Indeed, $\|(R_\theta-I)v\|\le\theta\|v\|$, and orthogonal projection is
a contraction. This estimate is uniform in the arbitrary planar roll.
The support functions, centered radii, and centered inradii each
change by at most $\eta$.

Take $\varepsilon=1/1000$ and use $R<23/10$. Exact rational checks give:

* $r(P_2)-r(P_3)>0.039$ and $r(P_3)-r(P_5)>0.016$;
* $\iota(P_5)-\iota(P_2)>0.032$;
* for every roll in $5\to3$, some original outer normal has support gap
  at least $99r/100-b>0.04564$.

Every one of these gaps exceeds $2\eta<0.0046$, so the corresponding
three radius cases, inradius case, and support case remain excluded.
Here the radius cases are $2\to3$, $2\to5$, and $3\to5$; the twofold
radius inequality itself also implies the general great-circle
restriction above.

For the remaining pair $3\to2$, use area. If polygons $A,B$ have
Hausdorff distance at most $\eta$ and are contained in a disk of radius
$R$, Steiner's parallel-body formula and the perimeter bound
$L\le2\pi R$ give

$$|A(A)-A(B)|\le2\pi R\eta+\pi\eta^2.$$

The unperturbed areas satisfy $A(P_3)>15.11$ and $A(P_2)<15.02$.
The total possible change of this area difference is less than

$$\left(4\frac{22}7\varepsilon+
 2\frac{22}7\varepsilon^2\right)\frac{53}{10}<0.09,$$

since $R^2<53/10$. Its positive sign therefore persists. This proves
the neighborhood claim for all six unequal-order pairs. Neighborhoods
for equal orders are not excluded by this proof.

## A reusable contact-gradient certificate and local bound

Fix a shadow with outward support inequalities $n\cdot x\le b$, $b>0$,
and let $v$ be any solid vertex satisfying $n\cdot v=b$. The projection
direction is perpendicular to $n$. Define its normalized contact
gradient

$$c_{n,v}=\frac{v\times n}{b}.$$

Suppose that, for each coordinate $j$ and sign $\sigma\in\{-1,1\}$, the
vector $\sigma e_j$ is a positive linear combination of these gradients
with total weight less than $C$. For every unit vector $\omega$, select
a coordinate with $|\omega_j|\ge1/\sqrt3$ and the sign making
$\sigma\omega_j$ positive. The corresponding combination shows

$$\max_{n,v} c_{n,v}\cdot\omega>\frac1{C\sqrt3}.\tag{3}$$

For each of $P_2,P_3,P_5$, `local_certificate.py` checks six such
representations in exact field arithmetic with $C=7$. The bases use at
most three gradients each; their weights are rederived by exact
Gaussian elimination and verified to be positive. There are 32, 24,
and 40 total active contact gradients, respectively. Only 6, 6, and
12 are needed by the supplied certificates. All sums of weights are
strictly below seven. Since $7\sqrt3<13$, (3) is greater than $1/13$.

For a rotation through angle $\theta>0$ about $\omega$, with skew matrix
$\Omega x=\omega\times x$, the exact integral remainder gives

$$\|\exp(\theta\Omega)-I-\theta\Omega\|\le\theta^2/2.$$

All vertices have norm at most $R<23/10$ and all three inradii exceed
two. Thus a contact attaining (3) satisfies

$$\frac{n\cdot(\exp(\theta\Omega)v-v)}b
 >\frac\theta{13}-\frac{23}{40}\theta^2>0
 \qquad(0<\theta\le1/10).$$

That vertex lies outside a supporting half-plane of the fixed outer
shadow. This proves the local contact lemma. By right multiplication
with a body symmetry, the same radius excludes relative rotations
within $1/10$ of any exact body symmetry. Translations are removed by
the centering argument.

The certificate criterion (3) is stated separately because it can be
applied to other fixed projections without repeating the angular
argument. Certificate bases were selected with floating-point linear
programming; that search has no role in their exact verification or in
the proof of the local bound.

## Scope and prior work

The unresolved Catalan target is justified by Fredriksson's results,
Gosain--Grimmer's Table 3, and Zeng's 2026 status discussion. The full
global problem remains open in the sources checked here. These papers'
failure to find a passage is not used as a nonexistence proof.

The mathematical contribution here is the exact restricted optimum
(1), the explicit invariant verification, the resulting finite and
neighborhood exclusions, and the quantitative local contact
certificates. A targeted search of the primary papers
and queries for the named solid with symmetry-axis and passage terms
did not locate this formula. That is a bounded prior-art search, not a
priority claim.

Primary references:

* [Steininger--Yurkevich, *An algorithmic approach to Rupert's problem*,
  Mathematics of Computation 92 (2023)](https://arxiv.org/html/2112.13754),
  for the strict projection criterion and central symmetry reduction.
* [Fredriksson, *Optimizing for the Rupert property*](https://arxiv.org/html/2210.00601),
  for the two additional solved Catalan solids.
* [Gosain--Grimmer, *Some New Insights from Highly Optimized Polyhedral Passages*](https://arxiv.org/html/2509.08190),
  Table 3, for the remaining deltoidal and pentagonal hexecontahedra.
* [Zeng, *A stellated tetrahedron that is probably not Rupert* (2026)](https://arxiv.org/html/2604.26531),
  for recent status context.
* [Scott, *Two Sufficient Conditions for a Polyhedron to be (Locally) Rupert*](https://arxiv.org/html/2208.12912),
  Definition 1, for the fixed-orientation local notion used here.
* [Steininger--Yurkevich, *A convex polyhedron without Rupert's property*](https://arxiv.org/abs/2508.18475),
  for the rigorous global non-Rupert precedent; its theorem is not being
  asserted for this solid.
* [McCooey's exact coordinates](https://dmccooey.com/polyhedra/DeltoidalHexecontahedron.txt).

The hand proof of the circle-covering and continuity arguments is not
formalized. The code's trust boundary is Python integer arithmetic,
`fractions.Fraction`, the displayed exact field arithmetic and hull
algorithm, and identification of the coordinate model with the named
Catalan solid. The verification uses no downloaded input, no numerical
solver, no enumeration of arbitrary orientations, and no external
certificate corpus.
