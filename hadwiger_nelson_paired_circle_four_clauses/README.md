# Four clauses control a coupled colouring of paired unit-circle supports

Let four distinct planar centres be paired into unit segments
`A={a0,a1}` and `B={b0,b1}`. Let `H` be the unit-distance graph on the **entire
union of the four unit circles** about those centres. The centres themselves
belong to this support because each has a unit-distance partner.

**General construction theorem.** A specified coupled orbit colouring of `H`,
with four distinct prescribed centre colours, is feasible exactly when an
explicit Boolean formula with **at most four clauses and eight variables** is
satisfiable. Each clause has at most two literals. Each cross-centre pair
contributes at most one clause, even when its circles have two intersections.
A satisfying assignment constructs a proper colouring of the entire support.

**Whole-family corollary.** Suppose none of the four cross-centre distances
`|ai-bj|` equals 1 or 2. If at least one of them equals `sqrt(3)` or exceeds 2,
then `H` is four-colourable. Every prescription of four pairwise distinct
centre colours extends. Orientations, translations and intersections of
segment interiors are unrestricted.

More generally, under the same exclusion of distances 1 and 2, failure of
this construction is possible only when all four cross distances lie in
`(0,2) minus {1,sqrt(3)}` and their four signed orbit clauses have one of
**two completely classified obstruction forms**, involving two or three
phase variables. This gives a necessary condition for actual
non-four-colourability, not a sufficient condition for it.

The certificate audits an exact nonparallel example with **180 vertices and
511 unit edges**, a boundary counterexample to dropping the tangent exclusion
from the distinct-centre-colour extension claim, and all **13,761** distinct
formulas with at most four proper binary clauses on two, three or four named
variables. It confirms **40** unsatisfiable formulas of the two stated forms.
No five-chromatic graph on at most 508 vertices is established.

## 1. Two-circle colouring and shared phases

Work in the complex plane. Put
\[
 \omega=(1+i\sqrt3)/2,\qquad U=\{\omega^k:0\le k<6\}.
\]
Choose one representative `v` from each `U`-orbit of unit directions. For
example, use the unique representative whose argument is in `[0,pi/3)`.
Give each orbit a Boolean phase `X_v`.

For a unit-separated pair `c0,c1`, remove the two centres from their two
circles. The formula
\[
 f(c_i+\omega^k v)=\alpha_v+i+k\pmod2                         \tag{1}
\]
is a well-defined proper two-colouring for arbitrary phases `alpha_v`.
The facts needed for this elementary assertion are:

* At an equilateral intersection of the two circles, changing owners changes
  the direction by `omega` or its inverse. Owner and exponent parity both flip.
* A unit chord on one circle changes the exponent by 1 or -1.
* A unit edge between the two circles, with neither endpoint a removed
  centre, preserves the owner-relative direction and changes the owner index.

For the last fact, if `x` belongs to the circle at `c0`, `y` to that at `c1`,
and `|x-y|=1`, then `c0,y` are the two distinct intersections of unit circles
at `x,c1`. Their sum is `x+c1`, so `y-c1=x-c0`. The removed-centre cases are
precisely the excluded degeneracies. These are the pair geometry facts from
the [previous incidence reduction](../hadwiger_nelson_paired_circle_incidence/README.md),
repeated here to make the proof self-contained.

Pin the centre colours to
\[
 c(a_i)=2+i,\qquad c(b_j)=j.
\]
Use **the same direction representatives in both groups**, and couple phases
by `alpha_A(v)=X_v`, `alpha_B(v)=1-X_v`. Thus the potential colours of a
noncentre point are
\[
\begin{split}
 c_A(a_i+\omega^k v)&=X_v+i+k\pmod2,\\
 c_B(b_j+\omega^l w)&=2+(1-X_w+j+l\pmod2).                 \tag{2}
\end{split}
\]
A point owned only by A uses `c_A`; one owned only by B uses `c_B`.
A mixed point may use either potential colour provided it avoids all its
centre owners' colours. This is the **specified coupled construction** whose
feasibility is characterized here. Arbitrary colourings, independently chosen
A/B phases, and arbitrary list colourings of a finite patch are broader classes.

## 2. One clause per cross-centre pair

Consider a noncentre point
\[
 x\in C(a_i,1)\cap C(b_j,1),\quad
 x-a_i=\omega^k v,\quad x-b_j=\omega^l w.
\]
Write `s=1+i+j mod 2`. The condition that at least one potential colour avoids
the opposite group's owner pin is exactly the clause
\[
 \boxed{(X_v=s+k)\ \lor\ (X_w=1+s+l)}.                     \tag{3}
\]
Equalities on the right are modulo two. A repeated literal makes a unit
clause; opposite literals on the same variable make a tautology and are dropped.

If the two circles have distinct intersections `x,y`, then
\[
 x+y=a_i+b_j,\quad y-a_i=-(x-b_j),\quad y-b_j=-(x-a_i).
\]
Since `-1=omega^3`, the clause at `y` is
\[
 (X_w=s+l+3)\lor(X_v=1+s+k+3),
\]
which is exactly (3) with its two literals exchanged. Thus each cross pair
contributes at most one clause. If only one intersection is a noncentre,
use that one; if neither is a noncentre, omit the pair. Empty circle
intersections also contribute nothing. Tangency is allowed in the general
construction: there is only one root and its clause is handled directly.
Four cross pairs give at most four clauses, hence at most eight variables.

This condition remains exact at points with several owners. Let `I` and `J`
be a mixed point's owner-index sets in A and B. The two potential colours in
(2) are well-defined independently of the chosen owner, by (1). Write
`P_j` for the statement that its A colour avoids pin `j`, and `Q_i` for the
statement that its B colour avoids pin `2+i`. The conjunction of its incidence
clauses is
\[
 \bigwedge_{i\in I,j\in J}(P_j\lor Q_i)
 =\left(\bigwedge_{j\in J}P_j\right)
   \lor\left(\bigwedge_{i\in I}Q_i\right).                 \tag{4}
\]
Thus the clauses collectively say that one **single** eligible palette exists;
they do not permit inconsistent palette choices for different owners.

A satisfying assignment now colours the entire support. Give unconstrained
orbits phase zero and use (2), choosing any eligible palette at mixed points.
Every edge between noncentres using the same palette is an edge of the
corresponding two-circle graph and is proper by (1). Different palettes are
disjoint. Centre-to-noncentre edges are owner spokes and are proper by
eligibility. Centre-to-centre edges have distinct pins. This proves sufficiency.
Conversely, any colouring produced by this coupled procedure must satisfy
all the owner-avoidance clauses, proving the claimed exactness **for this
procedure**. A global colour permutation gives any four distinct centre pins.

## 3. The distance table and the regular family

For a cross-centre pair put `d=|ai-bj|`. At an intersection the two unit
directions `u=x-ai`, `z=x-bj` have chord length `|u-z|=d`.
Two directions in a common `U`-orbit have chord length in
`{0,1,sqrt(3),2}`. Distinct centres rule out zero.

| Cross distance | Contribution to the formula |
| --- | --- |
| `d>2` | No intersections, no clause |
| `d=sqrt(3)` | Directions differ by `omega^(+/-2)`; (3) is a tautology |
| `d=1` | Directions differ by `omega^(+/-1)`; a unit clause, unless all roots are centres |
| `d=2` | Tangency; directions differ by `omega^3`; a unit clause, unless the root is a centre |
| `0<d<2`, `d` not 1 or `sqrt(3)` | Two different phase variables; a proper binary clause |

The parity claims follow immediately from (3). In particular the
`sqrt(3)` clause has equal direction parity and opposite demanded values.
This resolves the self-slot conflict of the earlier **one-sided** construction:
a unit edge between the two cross-circle intersections creates no constraint
for these coupled phases.

Assume now that all four cross distances avoid 1 and 2. Every remaining
nontrivial clause has two different variables. Such a clause is violated by
exactly one quarter of all phase assignments. The union bound shows that any
three such clauses leave at least one quarter of assignments available.
Therefore a distance `sqrt(3)` or a distance greater than 2 removes a clause
and proves the whole-family corollary. This is an all-placement proof, not an
inference from a parameter grid or the numerical example below.

## 4. Complete classification of four proper binary clauses

**Boolean lemma.** An unsatisfiable formula with at most four clauses, each
on two different Boolean variables, has exactly four distinct clauses. Up to
variable names and truth-value changes, it is one of
\[
\begin{array}{ll}
\text{two variables:}&
 (x\lor y),(x\lor\neg y),(\neg x\lor y),(\neg x\lor\neg y),\\[2mm]
\text{three variables:}&
 (x\lor y),(x\lor\neg y),(\neg x\lor z),(\neg x\lor\neg z),
 \quad y\ne z.
\end{array}                                                     \tag{5}
\]
Unused named variables are irrelevant. Repeated clauses cannot occur in an
unsatisfiable four-clause formula, because three distinct clauses are satisfiable.

**Proof.** Each clause's falsifying assignments form a codimension-two subcube
of measure `1/4`. Four such subcubes cover all assignments only if they are
pairwise disjoint. Two clauses have disjoint falsifying subcubes exactly when
they contain opposite literals on at least one shared variable. Thus the
four two-element variable supports must be pairwise intersecting.

A pairwise-intersecting family of two-element sets either has a common element
or is contained in the three edges of a triangle. To see this, choose two
intersecting supports `{x,y}`, `{x,z}`. Any support avoiding `x` must be
`{y,z}`; any further support must then be one of those three.

If all three triangle supports occur, a clause on any repeated support must
have the same signs as the first clause on that support, to be incompatible
with the other two supports. Such a repeat cannot have a disjoint falsifying
subcube. Hence the triangle case contains at most three pairwise-incompatible
clauses and cannot occur here.

There is consequently a common hub variable `x`. Among clauses using the same
sign of `x`, pairwise incompatibility requires the same other variable with
opposite signs, so there are at most two. Four clauses therefore split into
two with `x` and two with `not x`. If both pairs use the same other variable,
we obtain the first form of (5); if not, the second. Both displayed formulas
are unsatisfiable. This completes the classification for any number of variables.

For a regular geometric placement, actual non-four-colourability would imply
failure of the coupled procedure. Therefore all four cross pairs would have
to contribute proper binary clauses and yield one of (5). In particular,
four or more variables occurring in these clauses guarantee a colouring.
The lemma does not say these abstract obstruction diagrams are geometrically
realizable, or that a realizable diagram would defeat a different colouring.
Those questions remain open in this contribution.

## 5. Exact example and necessary boundary distinction

Take
\[
 a_0=0,\quad a_1=1,\quad
 t=(12+i\sqrt3)/7,\quad r=(-1+i\sqrt3)/2,\quad
 b_0=t,\quad b_1=t+r.
\]
Both segments have length one and their orientations differ. The four cross
squared distances, in slot order `00,01,10,11`, are
\[
 (3,\ 19/7,\ 4/7,\ 9/7).
\]
There are seven cross-direction orbits. The first clause is a tautology and
the other three have disjoint variable pairs, giving **54** satisfying
assignments on all seven variables. One phase assignment is certified.

For an actual finite audit, include each pair's intrinsic segment-direction
orbit and all owner-relative cross-intersection orbits, then translate each
group's direction set by its two centres. This is the
[previous actual paired-circle kernel](../hadwiger_nelson_paired_circle_kernel/README.md).
Both direction sets have 48 elements. The union has **180 distinct points**
and **511 unit edges**. Its canonical hashes are

```text
points: 190ecba1dec32ec6734fb7b0b7e33ef22d202ad2fbec791e74f25283b2ff83f4
edges:  7821142a04ca42454f985f64006cb37f1f4df9090937263145071972d576581f
```

The certificate verifies all 16,110 point-pair distances, all 511 edge
inequalities, 192 owner incidences and 180 phase identities. The infinite
support is coloured by the theorem; the finite audit checks the encoding and
a positive instance. It does not supply a chromatic lower bound.

The exclusion of distance 2 cannot simply be dropped from the claim that
**every four-distinct-centre prescription extends**. For
\[
 A=\{0,1\},\quad B=\{i\sqrt3,1+i\sqrt3\},
\]
the cross squared distances are `(3,4,4,3)`. The point
`z=(1+i sqrt(3))/2` has unit distance to all four centres. Four distinct centre
pins leave it no available colour. The formula has two tautologies and two
opposite unit clauses on one phase variable. The four spokes already
obstruct the prescribed pins. The induced five-point graph consists of two
triangles sharing their common vertex and is three-colourable, as the
certificate checks directly. **No claim about
non-four-colourability of its full circle support is made.** The control also
shows why a `sqrt(3)` separation alone cannot justify the distinct-pin claim
when tangencies are allowed. Unit-distance boundary cases are not classified
by the regular-family corollary.

## 6. Certificate, reproduction and trust boundary

The [producer](build.py) uses exact sparse squarefree radicals and rational
arithmetic, generates the circle intersections, derives clauses symbolically,
finds phase assignments by finite truth masks, and constructs the positive
colouring. The [checker](verify.py) imports no producer or parent executable.
It uses fixed arrays in the basis
\[
 (1,\sqrt2,\sqrt3,\sqrt6,\sqrt{19},\sqrt{38},\sqrt{57},\sqrt{114}).
\]
This is a basis of `Q(sqrt(2),sqrt(3),sqrt(19))`; all coefficients are exact
fractions. The checker uses subset/XOR multiplication, distinct from the
producer's sparse-radicand gcd multiplication.

The checker does not repeat the producer's intersection formula. It verifies
the rational squared centre separations, infers whether there must be zero,
one or two intersections, and checks that precisely that many distinct
supplied points have unit distance to both centres. It reconstructs all actual
points and edges. For every phase assignment it evaluates colour eligibility
directly against every noncentre root, checking **1,024** root-assignment
identities in the positive example and 12 in the boundary control. This tests
the clause signs and the two-root identification independently of (3).

The Boolean audit enumerates every subset of up to four distinct proper
binary clauses on each of two, three and four named variables:

| Named variables | Formulas | Unsatisfiable |
| ---: | ---: | ---: |
| 2 | 16 | 1 |
| 3 | 794 | 9 |
| 4 | 12,951 | 30 |
| Total | 13,761 | 40 |

The producer counts satisfying truth-mask bits. Independently, the checker
uses inclusion-exclusion on forbidden subcubes for the full assignment count,
transitive closure of Boolean implications for satisfiability, and signed
support comparisons for (5). It compares every count via the canonical stream
hash and every unsatisfiable formula directly. There are ten instances of the
first obstruction type and thirty of the second across the three named-variable
universes. All 160 single-clause deletions of the forbidden formulas are SAT.
The written proof above, rather than a bound guessed from this finite audit,
extends the classification to arbitrary numbers of variables.

Nine malformed controls are rejected: missing root, invalid root, incorrect
tautology, wrong literal sign, monochromatic colouring, wrong graph hash,
false common neighbour, omitted Boolean obstruction, and false record flag.
All checks use explicit exceptions and survive Python optimization.

The compact [certificate](certificate.json) is **5,722 bytes**, SHA-256

```text
6ddbd372d4d42351929676a55e969d9a2dfb99bd08d620e71f07ae60a1e17560
```

From this directory, with Python 3.11 or later and fresh output directories:

```sh
sha256sum -c SHA256SUMS
python3 build.py --out work/build
python3 verify.py --out work/check
python3 -O verify.py --out work/check-optimized
```

Only the Python standard library is needed. The producer regenerates the
certificate byte for byte. Both verifier modes must produce
[expected.json](expected.json); execution context is in
[validation.json](validation.json). There is no native solver, CAS,
floating-point premise, external coordinate input or omitted large trace.

The universal claims are written Euclidean and Boolean proofs, supported by
exact executable checks of the encoding, example and finite clause census.
Trust remains in those unformalized arguments, Python exact arithmetic,
field-basis independence and canonical encodings. The author-run checker is
algorithmically independent, not external peer review. External review of this
new contribution is pending; no priority claim is made.

## 7. Campaign consequence and stopping boundary

This is a transferable phase mechanism across arbitrary paired unit segments.
It closes the entire regular `sqrt(3)` stratum and all regular placements with
a cross separation greater than 2. It reduces the rest of the regular family
to two explicitly signed orbit patterns. It does not close placements with
unit cross distances or tangent cross circles, prove the two abstract
obstruction patterns geometrically realizable, or identify a five-chromatic
kernel. Failure of any prescribed procedure remains distinct from actual
non-four-colourability.

The [shared-midpoint theorem](../hadwiger_nelson_shared_midpoint/README.md)
remains a closed family and was not re-enumerated. A contemporaneous
[independent review](../hadwiger_nelson_paired_circle_incidence_review1/README.md)
accepts the earlier incidence reduction and proposes allowing either palette
at mixed points. This theorem supplies such a finite criterion for the
explicit complement-coupled phases, with independently phased palettes still
outside its equivalence claim. HN-2's
[complete left-selector relation](../hadwiger_nelson_heule560_left_relation/README.md)
was inspected as coordination context; that fixed-support lane is not a
mathematical dependency or part of this computation.

The baseline is [Parts's 509-vertex construction](https://arxiv.org/abs/2010.12665),
also stated as the record in the introduction of
[Haugland's August 2026 manuscript](https://arxiv.org/html/2608.04542v4).
Both primary sources were checked live on 6 September 2026. A targeted search
for paired-circle, dominating-matching and four-colouring formulations supplied
no matching prior theorem; this is not a novelty or priority proof.

This pass ends at the complete four-clause reduction, regular-family corollary,
Boolean classification and checked geometric certificate. A possible next
phase is to decide actual realizability or repair of the two signed obstruction
patterns. No such placement census, larger parameter search, or additional
construction phase has begun.
