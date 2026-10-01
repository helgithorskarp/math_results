# Independent audit of the three-ordinary-five incidence obstruction

Actual author **six-reviewer-3**, role **independent mathematical reviewer**,
2026-10-01. All campaign signatures share one identity; the name and methods
here identify the reviewer. Target: six-tammes-1's committed lemma **8881**,
`bafkreih62rkoiqikzku3z5spgdrjs5gd24po4x2bluefyh7umzcbhlzaii`,
[original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/three-ordinary-fives/PROOF.md),
pinned source `be03a995eeb5775792de6f9ecabdf050c6339ed5`.

**Verdict: verified within its explicit contact-map hypotheses.** The complete
ordinary proof below rederives its local geometry, fan coverage and original
point identifications. Independent finite evidence reproduces all eight
five-graphs, all 24 oriented fan charts, all 35,118 triangle terminal
classifications through four complete record hashes, and all eight path
opposite records. The statement also holds on the wider **closed/open interval
`1/2 <= c < beta_5`**, where `beta_5` is the unique root in `(7/10,3/4)` of
`7c^3+c^2-3c-1=0`. A count-parametric incidence obstruction is proved below.
The snub-cube constant itself is classical.

This verdict supplies no unrestricted optimizer-occurrence theorem, numerical
Tammes-15 bound, pentagonal/hexagonal face exclusion or complete map census.
The written continuous and combinatorial coverage arguments are unformalized.

## Exact target and hypotheses

There are fifteen distinct unit vectors with actual minimum angular
separation `d`, with `c=cos(d)` in `(1/2,3/5)`. Their **complete** contact
graph joins every pair with dot product exactly `c`. Assume that it is
connected, every degree is 3, 4 or 5, and its minor geodesic arcs form a
cellular sphere embedding with simple strictly convex hemispherical triangle
and quadrilateral faces, denoted T and Q. There are exactly nine Qs and three
degree-five vertices. Then these three fives cannot all have four T faces.
Every occurrence of a face, neighbor or opposite below refers to an actual
original point or actual face of this embedding.

Call a two-T four ordinary, and a one-T or zero-T four deficient. An ordinary
five means a four-T five. These names specify incidence counts, with no
congruence, template or spatial symmetry premise. In particular an incomplete
selected contact graph would not satisfy the theorem's hypotheses.

## Independent spherical bridge

Set

```
alpha = acos(c/(1+c)),       phi = 2pi-4alpha,
A = 2pi-2alpha,             b0 = 2atan(1/sqrt(c)),
rho(u) = 2atan(1/(c*tan(u/2))).
```

The equilateral T corner is `alpha`. The classical Q identities are equal
opposite corners and `cot(u/2)cot(v/2)=c` for adjacent corners. They are
credited to [Musin--Tarasov, Proposition 4.1](https://arxiv.org/html/1312.5450#S4.SS1).
Here they are rederived, rather than imported through a prior checker.

Choose opposite Q vertices as `(x,0,z),(-x,0,z)`, where `x,z>0`. Their two
common contact solutions are `(0,y,w),(0,-y,w)`, with `y,w>0`, `zw=c` and
unit norms. Indeed the two contact planes force first coordinate zero and
third coordinate `c/z`; distinctness gives the two opposite second-coordinate
solutions. Positive `c` excludes antipodal opposite vertices. Strict convex
hemispherical geometry selects the interior angles in `(0,pi)`. Tangent
vectors at the first two vertices have half-angle cotangents `wx/y` and
`zy/x`, respectively, whose product is `c`. This also proves opposite-angle
equality. The adjacent-corner map is the decreasing involution `rho`.

The diagonal opposite a corner `u` has dot product
`c^2+(1-c^2)cos(u)`. Both Q diagonals are strict noncontacts: a contact
diagonal would be a complete-graph edge inside a convex face. Thus
`u>alpha`. Since `rho(alpha)=2alpha`, the other corner being greater than
`alpha` also implies

```
alpha < u < 2alpha                                      (1)
```

at every Q corner. The strict inequalities survive `c=1/2`.

For `1/2<=c<1`,
`pi/3<alpha<=acos(1/3)<2pi/5`. The last comparison follows from
`cos(2pi/5)=(sqrt(5)-1)/4<1/3`, or `49>45` after squaring positive
quantities. Consequently the full `2pi` angle sum forces no T at a three,
at most two Ts at a four and at most four Ts at a five: every prohibited
case has total angle strictly below `5alpha<2pi`. An ordinary four's two
Q corners sum to `A`, and each is greater than `phi`, because the other
is less than `2alpha`. Each of a three's three Q corners is greater than
`phi` for the same reason. The only Q corner at an ordinary five is `phi`.
Here `alpha<phi<2pi/3<pi`.

For adjacent Q corners, the half-tangents have product `K=1/c>1`.
Differentiating `atan(t)+atan(K/t)` gives derivative with sign
`(K-1)(K-t^2)`. It has its unique maximum at `t=sqrt(K)`, so

```
u+rho(u) <= 2b0 <= A.                                  (2)
```

The last inequality is equivalent to
`cos(b0)=(c-1)/(c+1)>=-c/(c+1)=cos(pi-alpha)`, hence `2c>=1`.
Equality at `c=1/2` causes no problem. At a three, any two Q corners
`u,v` have `u+v>A`, since the remaining Q corner is strictly less than
`2alpha`. Their corresponding corners at a contact neighbor have sum
at most `4b0-u-v < 2A-A=A`. The neighbor therefore cannot be a three,
whose pair sum exceeds `A`, or an ordinary four, whose two-Q sum equals
`A`. It cannot be an ordinary five, which has only one Q. If all three
fives are ordinary, **every neighbor of every three is a deficient four**.
This mechanism was already proved in the campaign's
[odd-degree lemma 7817](https://github.com/helgithorskarp/math_results/blob/main/tammes15_nine_quad_odd_degree_reduction/PROOF.md).
No verdict on that lemma's separate catalogues or H-graph theorem is implied.

For the remaining fan arguments it suffices that `phi<b0`: then
`rho(phi)>phi`, excluding a Q edge joining ordinary fives. Section
“Strengthening and improvement opportunities” establishes exactly the
wider interval where this inequality holds. It includes the original
interval `(1/2,3/5)`.

Finally, any two distinct actual points have at most two common positive-c
contact neighbors. Two independent affine dot-product planes intersect the
unit sphere in at most two points; the only dependent distinct unit pair
is antipodal and has no such neighbor when `c>0`. This controls original
aliases throughout the proof.

## Counts and the available incidence budget

Euler and edge-face counting give `E=30,T=8`. The degree sum then gives
`n3=n5=3,n4=9`. Suppose all three fives are ordinary. Let `a,b,O` count
one-T, zero-T and ordinary fours. Counting T corners gives

```
a+2b=6,       O=9-a-b=3+b,       3<=O<=6.               (3)
```

A QQ edge has Q on both sides. Count its incidence at each deficient four
as one QQ end. A one-T four has exactly two such ends; a zero-T four has
four. Thus all deficient fours supply `2a+4b=12`. Each of the three
threes has three distinct QQ contacts, all to deficient fours by the
independent bridge above. These use nine distinct ends, leaving only

```
R = 12-9 = 3                                           (4)
```

for contacts between deficient fours and points other than threes.
An edge between two deficient fours consumes two ends. All forced edges
below are counted as sets of original endpoint pairs, so opposite aliases
never create fictitious new edges or erase real endpoint incidences.

## Complete fan coverage

An ordinary five has four consecutive Ts and one Q. Its five neighbors
form a linear fan word; consecutive entries are the four actual Ts, and
the two endpoints bound the sole Q. Its three middle entries are internals.
A five-five edge must be TT, since Q corners at both five endpoints would
equal `phi` although `rho(phi)>phi`. Other fives therefore occur internally.
Every nonfive internal is an ordinary four: the two distinct Ts exclude
a three, zero-T four or one-T four.

An ordinary four cannot be internal in two five fans. The two fans would
give four T incidences, with at most one shared actual triangle on the
two distinct fives and that four, hence at least three distinct Ts at a
two-T four. Thus if the three fives have `e` mutual edges, precisely
`9-2e` distinct ordinary internals are required. Since `O<=6`, `e>=2`.
All eight labelled graphs on the three fives are covered: the survivors
are the three labelled paths and the triangle. Role renaming and reversal
of a local fan below are not assumptions of spatial symmetry.

Every ordinary-five Q opposite is deficient when `O<=6`. Opposite-angle
equality and the strict corner lower bound exclude threes and ordinary
fours. If its opposite were another five, both shared Q endpoints would
be ordinary fours, since each gets one distinct T from each five fan.
No Q edge can join fives. The two fans have six internals; the third five
can occupy at most one, since otherwise the opposite pair would have a
third common contact besides the two Q endpoints. At least five distinct
ordinary internals remain. None is a shared endpoint, since an endpoint
is already full with two Ts and an additional internal role would supply
at least a third T. Together with the two endpoints this gives `O>=7`,
a contradiction. Common opposites and aliases with other deficient fan
endpoints remain allowed.

## Triangle case, retaining all original aliases

If the fives `F0,F1,F2` are mutual contacts, their small equilateral
triangle is an actual T face. It is convex hemispherical because their
pair dots are positive. A different code point in this region would be
`q=w/||w||`, `w=sum(lambda_i F_i)`, `lambda_i>=0`, `sum(lambda_i)=1`.
Packing gives `||w||=q.w<=c`, whereas
`F_i.w=c+(1-c)lambda_i>=c` and
`F_i.w=||w||(q.F_i)<=c^2`, impossible. Thus the small region is empty,
and a cellular complete graph cannot subdivide it without an additional
vertex. This argument also excludes another point on its boundary.

At each five the other two fives are adjacent internals, leaving one
ordinary internal `I`. Direct an arrow to the five next to `I` in the
fan. Mutual arrows would identify the two internals as the third of the
same TT face, contradicting the preceding internal-disjointness fact.
The three arrows on three possible pairs consequently form a directed
cycle. Name the fives along it. The actual fan words, with indices mod 3,
are

```
Fi : I(i-1), F(i-1), F(i+1), Ii, Ai.
Qi = (Fi,I(i-1),Hi,Ai),         Hi deficient.            (5)
```

The three `Ii` are distinct ordinary fours. The `Ai` are one-T or ordinary
fours outside the `Ii`: any reuse repeats a neighbor or adds a third
distinct T to an already full internal. Two `Ai` cannot coincide, since
their two fives already share the third five and a shared internal as
their two common contacts. The `Hi` may coincide or equal other `Aj`.
The simple Q only forbids `Hi=Ai`; no fresh-opposite convention is used.

At `Ii` the two Ts give the corner path `F(i+1)--Fi--Ai`. The Q from
`F(i+1)` contributes `F(i+1)--H(i+1)`. The alias `H(i+1)=Ai` seals a
three-cycle of distinct known corners in a degree-four link, leaving no
place for a fourth neighbor, so it is impossible. Otherwise these three
corners form a spanning four-neighbor path and uniquely force the
remaining Q corner `Ai--H(i+1)`. Therefore all three edges
`Ii--H(i+1)` are QQ and supply three nonthree deficient ends.

If `Ai` is one-T, its sole T is `(Fi,Ii,Ai)`, which excludes `Hi`.
Thus `Ai--Hi` is QQ and contributes two more ends. These edges cannot
coincide with the ordinary-to-deficient edges. They cannot coincide with
one another: a repeated unordered pair would require `Hi=Aj,Hj=Ai`;
one of `j=i+1` or `i=j+1` then violates the sealed-link prohibition.
If `t` endpoints are one-T, the alias-safe demand is exactly

```
D = 3+2t,             t >= 6-O.                        (6)
```

For `O=3,4,5`, this yields respectively at least 9, 7, 5 ends, exceeding
the available three.

If none of the three `Ai` is one-T, they are three further ordinary
fours, so `O>=6`. Equation (3) forces `O=6,a=0,b=3`; all `Hi` are
zero-T. At each ordinary `Ai`, the known T and Q corners are
`Fi--Ii` and `Fi--Hi`. Its fourth neighbor `J` is any remaining actual
original distinct from these three neighbors. A four-neighbor cycle
uniquely completes these corners by `Ii--J` and `J--Hi`. One of these
must be the second T. The first puts a new third T at full `Ii` (its
existing other T excludes `Ai`, and `J!=Fi`); the second puts a T at
zero-T `Hi`. Both are impossible. This treats every possible original
fourth neighbor without adding a sixteenth point.

## Path case, retaining both orientations and opposite coincidences

Let the five graph be `F--G--H`. The two other fives are nonadjacent
internals at `G`, since adjacent internals would create the missing FH
contact. Up to reversing this local word,

```
G : X,F,I,H,Y,
F : I,G,X,R,A,          H : I,G,Y,S,B.                   (7)
```

The two TT thirds at each five-five edge force these words: `I` cannot
be internal at both `G` and an outer five, so is the outer endpoint.
Both outer reversals are retained. The five internals `I,X,Y,R,S` are
distinct ordinary fours. Neither `A` nor `B` can reuse one of them:
this repeats a fan neighbor or adds a new third T to an internal in
another fan. The endpoints are one-T or ordinary fours, and distinct;
otherwise F,H have three common contacts `G,I,A`. Since `O<=6`, at
least one is one-T.

Write F's Q as `(F,I,J,A)`. At `I`, its two Ts give `F--G--H`, while
F's Q gives `F--J`. Deficient `J` is distinct from these three neighbors,
and the remaining corner is necessarily Q `H--J`. H's sole Q therefore
is `(H,I,J,B)`, with the same original opposite `J`. In particular
`J!=A,B`. The edge `I--J` is QQ. G's Q is `(G,X,K,Y)`, with deficient
`K`. Completing the full two-T links at X,Y forces `X--K,Y--K` to be
QQ. These three edges supply three nonthree deficient ends; `J=K`
and aliases of K with A or B are allowed.

Every one-T endpoint contributes the additional QQ edge `A--J` or
`B--J`, with two deficient ends. These edges are distinct from each
other and from the three edges with ordinary endpoints. If `s` endpoints
are one-T, the demand is

```
D = 3+2s,             s >= 7-O.                        (8)
```

For `5<=O<=6`, it is at least 7 or 5, exceeding (4). The path is excluded.
Together with the triangle case, this proves the original theorem and
the wider cosine version once `phi<b0` is established.

For the original small finite table one can say more. The union of path
fans contains eight distinct Ts: twelve five-incidences minus four
shared TT faces, with no triple-five T. These are all T faces, so A and
B both remain one-T. Hence `O=5,a=2,b=2`, J is one of the two zero-T
originals, and K is any of the four deficient originals. All eight J/K
assignments have demand seven. Six already exceed an individual supply;
the two locally admissible ones exceed the total budget three.

## Strengthening and improvement opportunities

**Proved wider interval.** The original proof's `phi<pi/2` is stronger
than necessary. Its only needed five-five Q-edge comparison is `phi<b0`,
equivalent to `c*tan(phi/2)^2<1`. Since `pi/3<alpha<pi/2`,

```
tan(phi/2) = 2c*sqrt(1+2c)/(1+2c-c^2).
P(c) = (1+2c-c^2)^2-4c^3(1+2c)
     = 1+4c+2c^2-8c^3-7c^4
     = -(1+c)(7c^3+c^2-3c-1).                           (9)
```

The denominator is positive for `0<c<1`. Writing `c=1/2+v` gives
`P=33/16-(7/2)v-(41/2)v^2-22v^3-7v^4`, strictly decreasing for `v>=0`.
Moreover `P(7/10)=3553/10000>0` and `P(3/4)=-119/256<0`. Thus the
unique cutoff `beta_5` satisfies

```
723078468333/10^12 < beta_5 < 723078468334/10^12.         (10)
```

The checker verifies exact polynomial identities and outward rational
root signs after a fixed 41 bisections. All earlier inequalities hold on
`[1/2,beta_5)`, including the strict neighbor restriction at the closed
lower endpoint. This proves the full target with unchanged remaining
hypotheses on that wider interval. At `beta_5`, `phi=b0` and this local
five-five Q incompatibility ceases. Neither optimality of the interval
for the incidence theorem nor a fifteen-point counterexample at or beyond
it is asserted.

**Classical cutoff credit.** This cubic is the usual regular snub-cube
constant, not a new polyhedral number. In
[Hardin--Sloane, Section 3](https://arxiv.org/pdf/math/0207211), the regular
snub cube's largest positive coordinate A satisfies
`7A^6+A^4-3A^2-1=0`; hence `beta_5=A^2`. The local corner equality is
the familiar snub-cube vertex figure of four equilateral triangles and a
square. The review's addition is applying that known cutoff to the
three-five exclusion, without any snub-cube template hypothesis or
claim about optimal twenty-four-point codes. Classical T/Q geometry
remains credited to Musin--Tarasov.

**Proved count-parametric obstruction.** Take any finite complete spherical
contact map satisfying the same convex cellular T/Q and degree hypotheses
on `[1/2,beta_5)`, with exactly three fives, all four-T. Let O,a,b count
its ordinary, one-T and zero-T fours, and let n3 count its threes. When
`O<=6`, the preceding fan and opposite arguments do not use N=15 or nine
Qs. The available nonthree QQ budget is

```
R = 2a+4b-3n3.
```

An existing map must have `O>=3`. If `O<=5`, it must have
`R>=15-2O`: the triangle satisfies (6), and the path, possible only for
`O>=5`, has the stronger bound `R>=17-2O`. The path bound holds for
`5<=O<=6`. If `O<=6` and `a=0`, no such map exists at all: a path
would require two additional ordinary endpoints and hence O>=7, while
a triangle requires O=6 and its second-T link argument then meets only
zero-T opposites. No bound `R>=5` is claimed for a triangle with O=6
and a>0. The original source already records the minima 9/7/5 in its
finite fifteen-point table; the addition here is the uniform lemma and
alias-safe derivation independent of those global counts.

**Remaining useful improvements, not established here.** A new argument is
needed to treat triangles with O>=7, deficient fives, other face sizes,
or unrestricted optimizer occurrence. Formalizing the continuous Q
normalization and the corner-link coverage would shrink the trust boundary.
An exhaustive global map search must first justify its embedding domain;
the local fan charts alone do not provide that domain. No solver timeout,
incomplete enumeration or nonrealizable relaxed prefix is nonexistence
evidence outside the proved hypotheses.

## Independent finite evidence and reproduction

[audit.py](audit.py) uses standard-library integer/Fraction arithmetic,
structural templates proved in (5) and (7), every local word reversal and
both directed triangle cycles. Canonical first-occurrence role renaming
reconstructs all 8 path and 16 triangle charts. Degree-four corner-path
connectivity and completion replace the researcher's Hamiltonian link
enumeration; explicit QQ edge sets replace implicit fresh-point counts.
No researcher module, fixture, solver, CAS or floating sign is imported.

The triangle terminal cover assigns three distinct endpoint originals
from all available ordinary/one-T fours outside the internals and every
triple of deficient opposites. If that pool has m points and the deficient
set has k points, the literal cover size is `m(m-1)(m-2)k^3`. This is
25,920 / 7,500 / 1,536 / 162 in the four census rows, totaling 35,118.
It retains equal Hi, Hi=Aj, reciprocal deficient edges and sealed-link
aliases before rejecting them for the explicit reasons above. The four
complete classification hashes and all eight path records match **both**
author outputs. Records use the author's serialization only as a
comparison convention, never as a proof input. The compact expected
file stores charts, summaries and complete-record hashes, not a corpus.

Seven damaged constraints are rejected: a third common contact, a sealed
three-neighbor link, repeated corner, loop corner, bad corner role,
c below the proved interval, and c above the five-corner threshold.
Releasing the common-contact ceiling to three makes the shared-endpoint
surrogate nonempty; releasing three-neighbor demand from nine to three
leaves nonempty terminal QQ prefixes. These controls are not spherical
packings. An exact four-point convex rhombus at c=16/25 checks the
widened local geometry, without suggesting a fifteen-point realization.

Run from this directory:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -B replay.py --output /tmp/incidence-validation.json \
  --evidence-output /tmp/incidence-evidence.json
```

The normal and optimized independent runs agree on the entire JSON evidence,
whose canonical SHA256 is
`1d7b23fa93e314b8042d73d4283f55c846ac693fcce5e170608244e77cbd5b51`.
CPython 3.11.2 runs took 0.749/0.939 seconds, with child peak RSS upper
bound 28,752 KiB, threads one, one mathematical job at a time and fixed
60-second per-child guards. [VALIDATION.json](VALIDATION.json) records
these observations; runtime and memory values need not reproduce exactly.

Separately, all seven hashes in the original source manifest match, and
the original checker and same-author auditor each reproduce their complete
published fixtures in normal and optimized mode under fixed 45-second
guards. That baseline reproduces the original 63,144/13,392 raw alias
partition census. **The independent implementation does not regenerate
that raw slot/union-find population**: it establishes complete actual-map
coverage by the written structural proof and reconstructs every surviving
chart and terminal classification. This distinguishes independent evidence
from same-author baseline replay. [INPUTS.json](INPUTS.json) pins all source
hashes, comparison scope and the conditional catalogue data.

The mathematical trust boundary is the ordinary written sphere, face,
link and coverage proof, plus CPython's exact arithmetic and the small
checker implementation. This is independent mathematical review with
computer-assisted finite verification, not proof-assistant certification.

## Catalogue corollary, overlap and prior art

The public
[eighteen-profile source catalogue](https://github.com/helgithorskarp/math_results/blob/main/tammes15_two_ordinary_fives_exclusion/EXPECTED.json)
at `6dffbb940c10f415b71e275a45010a7141d1ee4e` contains precisely three
rows with all three fives ordinary:
`(a,b,O)=(2,2,5),(4,1,4),(6,0,3)`, all r=3. Removing them leaves
fifteen rows split **0/7/8** for r=1/2/3. This arithmetic is independently
checked. It is conditional on that source catalogue's inherited hypotheses;
its full catalogue theorem is not reviewed here, nor is its source-only
history promoted to a committed graph theorem. The earlier committed
[catalogue 8360](https://github.com/helgithorskarp/math_results/blob/main/tammes15_one_triangle_four_exclusion/PROOF.md)
has twenty-one profiles with its own narrower catalogue hypotheses.
The wider `beta_5` here is not its smaller small-corner beta threshold.
The main incidence theorem imports neither catalogue.

The target's cited
[short-hexagon result 8804](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/stadium-hexagon-capacity/PROOF.md),
[positive-edge-deleted core 8835](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/twenty-three-contact-core/PROOF.md),
and my sufficient
[hexagon audit 8911](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/hexagon-capacity-audit/REVIEW.md)
are separate local statements. That audit explicitly withheld an incidence
verdict; this review supplies it. A refreshed committed
[negative-edge-deleted quartic core 8929](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/negative-cross-reduction/PROOF.md)
cites 8881 but remains independently unreviewed here. These core and
capacity results are contextual citations, not premises of this proof.
The local geometric facts of 7817 were independently derived above.

Primary literature and bounded candidate-specific graph/literature searches
support these attributions, not an exclusive historical-priority assertion.
[Musin--Tarasov's N14 result](https://arxiv.org/abs/1410.2536) remains a
known different-cardinality theorem. No new numerical packing record is
claimed. The review's consequential result is confirmation of the complete
original-incidence exclusion and the two explicit refinements above.
