# Independent audit of the complete three-five T/Q obstruction

Actual author **six-reviewer-3**, role **independent mathematical reviewer**,
2026-10-01. All campaign signatures share one identity; this name and the
independent methodology below identify the reviewer. Target: six-tammes-1's
committed lemma **8975**, artifact
`bafkreiej5yrx23gq67dxru5hufgep5b5fsivj2foyk5jknpd37myf73taa`,
[original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/three-five-branch/PROOF.md),
source **71f757b0cd0eafe8bf76fb0fa725ab2c43db3198**.

**Verdict: verified within its explicit contact-map hypotheses.** The new
zero-, one- and two-ordinary-five cases are independently rederived here.
All nineteen triangle censuses, all 30,451 labeled three-neighbor rows,
their complete classification hashes, the two residual role orbits and
every terminal original-point alias agree with the published evidence.
The older all-three-ordinary case is an explicit, already sufficiently
reviewed premise, not a new audit or a transferred verdict.

**Proved refinements:** the exclusion, and its at-most-two corollary, hold
on the wider **closed** interval

\[
\frac12\le c\le\eta=\frac{1+\sqrt{17}}8,
\qquad
\frac{640388203202}{10^{12}}<\eta<
\frac{640388203203}{10^{12}}.
\]

A self-contained degree-bound argument below removes the need to import
the whole earlier lemma7817 for this corollary. The catalogue consequences
remain conditional on the earlier lists and all their hypotheses. This
review proves no unrestricted optimizer-occurrence theorem, global
Tammes-15 numerical bound, larger-face exclusion or complete map census.
The written geometric and global-to-local coverage arguments remain
unformalized.

## Exact hypotheses and dependency boundary

There are fifteen distinct unit vectors with actual minimum angular
separation \(d\), and \(c=\cos d\). The **complete** contact graph contains
every pair with dot product exactly \(c\). It is connected; each degree is
3, 4 or 5. Minor geodesic edges give a cellular sphere embedding whose
faces are simple, strictly convex, hemispherical triangles and
quadrilaterals, denoted T and Q. Exactly nine faces are Q. The original
claim assumes \(1/2<c<3/5\); the arguments below use the closed interval
specified above. Every face and unnamed point is an actual original face
or one of the fifteen original points.

A two-T degree-four point is **ordinary**; one-T and zero-T fours are
deficient. A four-T five is ordinary. These are incidence roles, not
geometric congruences. Euler and edge-face incidence give
\(E=30,T=8,n_3=n_5=r,n_4=15-2r\).

The new deficient-five branches use no beta cutoff, incumbent coordinates,
template, proximity, irreducibility or spatial symmetry. The all-ordinary
\(r=3\) case is imported from
[8881](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/three-ordinary-fives/PROOF.md)
and its already committed
[independent review8953](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/incidence-audit/REVIEW.md),
source `ac895797cfcd1c04ba37d727c0bb9fe664160387`, artifact
`bafkreid4wwif27qam7uovxjgwklyqe7guki55nwjs5uzpy7ppqvw476sfm`.
That review proves the all-ordinary statement on \([1/2,\beta_5)\), with
\(\beta_5>7/10>\eta\). Its precise scope therefore supplies this one
missing case on the entire new interval. Its previous verdict alone
does not justify the new cases.

The classical corner identities and prior local contact/QQ facts are
credited to Musin--Tarasov and campaign7817/7912, but rederived here. No
unique-three fan collar or full beta catalogue is imported into the new
exclusion. In particular the alternative upper-three proof below does
not certify7817's separate lower bound or its full profile classifier.

## Independent spherical and endpoint bridge

Set

\[
\alpha=\arccos\frac{c}{1+c},\quad \phi=2\pi-4\alpha,
\quad A=2\pi-2\alpha,\quad b_0=2\arctan\frac1{\sqrt c},
\quad \rho(u)=2\arctan\frac1{c\tan(u/2)}.
\]

The equilateral T corner is \(\alpha\). For an equilateral Q, opposite
corners are equal and adjacent corners satisfy
\(\cot(u/2)\cot(v/2)=c\), hence \(v=\rho(u)\).
These classical relations are credited to
[Musin--Tarasov, Proposition4.1](https://arxiv.org/html/1312.5450#S4.SS1).
Here is the independent geometric derivation needed for the scope.

Rotate an opposite pair to \((x,0,z),(-x,0,z)\), with \(x,z>0\). Positive
\(c\) and two common contacts exclude an antipodal pair. Their common
contact planes give the other two vertices \((0,y,w),(0,-y,w)\), with
\(y,w>0\), unit norms and \(zw=c\). The tangent half-angle cotangents at
the first and second vertices are respectively \(wx/y\) and \(zy/x\).
Their product is \(c\); reflection gives equality of opposite angles.
Strict convex hemispherical geometry chooses the interior angles in
\((0,\pi)\).

The diagonal opposite a corner \(u\) has dot product
\(c^2+(1-c^2)\cos u\). A contact diagonal would be an edge of the
complete graph inside this convex face; both diagonals are therefore
strict noncontacts. It follows that \(u>\alpha\). Since
\(\rho(\alpha)=2\alpha\) and \(\rho\) decreases,

\[
\alpha<u<2\alpha.                                      \tag{1}
\]

Throughout our interval \(\pi/3<\alpha<2\pi/5\). For the upper estimate,
\(\alpha\le\arccos(1/3)<2\pi/5\), since
\(\cos(2\pi/5)=(\sqrt5-1)/4<1/3\). Thus
\(\alpha<\phi<\pi\). Three Ts at a four, or a T at a three, make the
corner sum less than \(2\pi\) by (1). A five has at most four Ts because
\(5\alpha<2\pi\). Consequently threes have no Ts, fours at most two,
and fives at most four.

The two Q corners at an ordinary four sum to \(A\), so each is strictly
above \(A-2\alpha=\phi\). Every Q corner at a three is also strictly
above \(\phi\). The sole ordinary-five Q corner is exactly \(\phi\).
At a deficient five with deficit \(\delta\ge1\), the \(\delta+1\) Q
corners sum to \(\phi+\delta\alpha\); each other Q exceeds \(\alpha\).
Every such corner is **strictly below** \(\phi\). All five Q corners
are thus at most \(\phi\).

For \(0<u<\pi\), differentiating \(u+\rho(u)\) gives a unique maximum
at \(u=b_0\), with value \(2b_0\). Also
\(\cos b_0=(c-1)/(c+1)\ge-c/(1+c)=\cos(\pi-\alpha)\) for
\(c\ge1/2\). Therefore

\[
u+\rho(u)\le2b_0\le A.                                \tag{2}
\]

An edge at a three has Qs on both sides. Its two three-end corners sum
to more than \(A\), because the third corner is less than \(2\alpha\).
Applying (2) to both incident Qs leaves a sum **strictly less than**
\(A\) at the other end. This excludes a three or an ordinary four there.
An ordinary five has only one Q and cannot be a QQ-edge end. Thus every
three contacts only deficient fours or deficient fives. At \(c=1/2\),
the weak equality in (2) causes no loss of this strict conclusion.

Five-five contacts cannot bound any Q. Put
\(D=1+2c-c^2>0\). Since
\(\tan(\phi/2)=2c\sqrt{1+2c}/D\),

\[
D^2-4c^3(1+2c)
=-(1+c)(7c^3+c^2-3c-1).                                \tag{3}
\]

The cubic \(P(c)=7c^3+c^2-3c-1\) increases for \(c\ge1/2\), as
\(P'(c)=21c^2+2c-3\ge13/4>0\). Its value at \(13/20\) is
\(-4841/8000\), and \(\eta<13/20\). Hence (3) is strictly positive
on our interval, meaning \(\cot(\phi/2)^2>c\). Two adjacent five Q
corners, each at most \(\phi\), cannot satisfy the Q product equality.
Every five-five contact is TT. No assumption \(\phi<\pi/2\) is needed.

Finally let \(y=\rho(\phi)\), and \(h=\sqrt{1+2c}\). The exact identity

\[
\tan(y/2)=\frac{D}{2c^2h},\qquad
\tan((\pi-\alpha)/2)=h,\qquad
D-2c^2(1+2c)=(1+c)(1+c-4c^2)                            \tag{4}
\]

shows \(y\ge\pi-\alpha\) precisely through the positive root \(\eta\).
A deficient-five QQ edge gives the other end two corners **strictly
above** \(y\). If that end had degree at least four, at least two more
corners would be at least \(\alpha\), so its total would exceed
\(2y+2\alpha\ge2\pi\). Thus every deficient-five QQ edge leads to a
three, including at \(c=\eta\). A three-T five has zero or one QQ edge;
a two-T five has one or two. If the latter has two, its three Qs are
consecutive and its two QQ neighbors bound an intervening Q.

Two distinct unit vectors have at most two common positive-\(c\)
contacts: two independent affine contact planes intersect the sphere
in at most two points. The only dependent distinct case is antipodality,
with no such common contact. A Q opposite pair fixes both other
vertices and its unique minor convex hemispherical cell. Different Qs
cannot repeat an opposite pair. At a deficient five all its Q opposites
have corner below \(\phi\), ruling out a three, ordinary four or ordinary
five. They are distinct positive-deficit points. The total deficit from
the four/five triangle maxima is
\(2n_4+4n_5-3T=30-24=6\). Hence
\(\delta+(\delta+1)\le6\), so each deficient five has \(\delta\le2\).

These facts prove every continuous inequality and strict boundary used
below. A closed interval is obtained by preserving strict face-diagonal
and deficient-five inequalities; endpoint inclusion is not inferred
from numerical samples.

## Complete census and three-contact coverage

Assume now \(r=3\). Let \(k,f_1,f_2\) count ordinary, three-T and two-T
fives. Let \(a,b\) count one-T and zero-T fours. Then

\[
k+f_1+f_2=3,\quad a+2b+f_1+2f_2=6,
\quad O=9-a-b.                                          \tag{5}
\]

For \(k=0,1,2\), exactly nineteen nonnegative cases result. A one-T
four has two QQ edges, a zero-T four can contact at most the three
actual threes, and deficient fives supply at most one or two contacts.
The nine three contacts therefore require

\[
9\le M=2a+3b+f_1+2f_2.                                 \tag{6}
\]

Let the actual threes be U,V,W. A one-T four contacting two threes has
them on its consecutive QQ edges, forcing a face \((S,U,Z,V)\). The
same holds for a two-T five with two three contacts. Here Z is another
supplier on that exact pair, uniquely so by the common-contact bound.
When \(b=0\), every supplier with two three contacts is of one of these
forcing types, and they occur in pairs of exactly two suppliers on the
same pair. Two different used pairs share a three and would give it
four neighbors. There are at most two shared suppliers. A supplier
with only one three contact cannot provide the opposite required by a
shared pair.

Here is the complete case reduction, with all count possibilities
obtained from (5).

* **\(k=0\).** Now \(M=9-f_2-b\). Only \(f_2=b=0,a=3\) can supply
  nine contacts. Three shared one-T suppliers cannot occur in pairs;
  all cases fail.
* **\(k=1\).** Now \(M=10-f_2-b\). If \(f_2=2\), capacity fails.
  If \(f_2=1\), only \(b=0,a=3\) can attain nine; its three one-T
  fours and two-T five give four shared suppliers, impossible. If
  \(f_2=0\), \(b=0\) permits at most \(4+2+2=8\) contacts, while
  \(b=2\) has capacity eight. Only
  \((k,f_1,f_2,a,b)=(1,2,0,2,1)\) remains, with all capacities saturated.
* **\(k=2,f_2=1\).** Here \(a+2b=4\). At \(b=0\), whether the
  deficient five contacts one or two threes, the paired-supplier bound
  gives at most seven contacts. At \(b=2\), capacity is eight. At
  \(b=1\), the two one-T fours and two-T five must share three
  different pairs; zero-T B is the other contact on each pair. Their
  forced corners seal the U,V,W triangle in B's degree-four link.
* **\(k=2,f_1=1\).** Here \(a+2b=5\). At \(b=0\), there are at most
  eight contacts. At \(b=2\), both zero-T fours contact all three
  threes and the one-T four contacts two, making three common
  neighbors for that pair. At \(b=1,a=3\), if H contacts no three,
  three different shared pairs seal B's link. If B contacts just two
  threes and H one, the four double suppliers have pair multiplicities
  1,1,2; only one singleton can be B, so another forcing supplier
  lacks its opposite. If B contacts all three, exactly two one-T
  fours are shared; their different pairs form a path, while C and H
  supply the two different endpoints. This is the sole remaining
  case \((2,1,0,3,1)\).

A vertex's link is a cycle on its **distinct actual neighbors**. A
triangle component already closed on three neighbors cannot extend
to a degree-four or degree-five link. Repeated unordered corner pairs
cannot belong to different faces. These facts justify the sealed-link
tests without assuming that an unnamed neighbor is a fresh point.

The two residual patterns, after equal-role naming only, are

\[
\begin{array}{ll}
k=2:&N(U)=\{A,B,H\},\ N(V)=\{A,B,D\},\ N(W)=\{B,D,C\};\\
k=1:&N(U)=\{A,B,H_1\},\ N(V)=\{A,B,D\},\ N(W)=\{B,D,H_2\}.
\end{array}                                             \tag{7}
\]

Here B is zero-T, A,D and C where present are one-T fours, and every H
is a three-T five. This naming imposes no metric symmetry. Cyclic
reversals and role permutations remain covered.

## Independent terminal proof: two ordinary fives

The shared pairs force \(Q_1=(A,U,B,V)\) and \(Q_2=(D,V,B,W)\).
B's link contains the path U--V--W. Its fourth actual neighbor X
forces the remaining Qs

\[
Q_3=(B,U,H,X),\qquad Q_4=(B,W,C,X).                     \tag{8}
\]

X differs from B and U,V,W. X cannot be A,D, since BA,BD are strict
diagonals of the first two Qs. It cannot be H,C, by face simplicity.
It cannot be an ordinary five, since its opposite three Q corner is
above \(\phi\). Thus X is one of the five ordinary fours, and BX is QQ.

X's known Q corners H--B and B--C leave two Ts with its fourth
neighbor P: \(T(H,X,P)\) and \(T(C,X,P)\). The three-T H fan has X as
an endpoint and P as its next internal point, so P receives a further
distinct H-fan T. It has at least three distinct Ts, and is one of the
two ordinary fives. This is an incidence deduction, not a new-point
or default-degree assumption.

The remaining corner D--C at W forces \(Q_5=(W,D,R,C)\).
Face simplicity excludes W,D,C as R. The alias R=X repeats the W--X
corner at C in two Qs. R cannot be another three, since C has only W
among its three contacts. R cannot be any five, whose corner is at
most \(\phi\), opposite W's corner above \(\phi\). Thus R is a four.

C's unique T is already \(T(C,X,P)\), so CR is QQ. The deficient fours
have \(2a+4b=10\) QQ ends. Eight of the nine three contacts go to them;
H consumes the other one. Only two non-three deficient-four QQ ends
remain. BX uses one. A deficient R would make CR use two more, since
C is also deficient. Those ends are distinct from BX even if R=B.
Thus R is ordinary.

The four distinct C neighbors W,X,P,R are now complete. Its corners
W--X, W--R and X--P force the remaining P--R corner to be Q, giving
\(Q_6=(C,P,Y,R)\) for some actual original Y. P's opposite corner is
\(\phi\), while ordinary R's is strictly above \(\phi\), impossible.
All Y aliases are covered: repeated vertices and contact diagonals
already fail face requirements; every other alias has this mismatch.

## Independent terminal proof: one ordinary five

The same Q1,Q2 force
\(Q_3=(B,U,H_1,X),Q_4=(B,W,H_2,X)\). The identical original-alias
argument makes X one of the six ordinary fours; BX is QQ. At X the
remaining Ts are \(T(X,H_1,P),T(X,H_2,P)\). P is internal to both
three-T H fans, receiving two Ts from each. They can share at most
the one actual triangle \(T(H_1,H_2,P)\), so at least three distinct
Ts occur at P. It differs from the known X neighbors H1,H2. It must
be the sole ordinary five F.

All five-five edges are TT. At F the neighbors H1,X,H2 exhaust its
three internal T-fan positions. Its complete fan word, up to actual
endpoint naming and both local orientations, is K,H1,X,H2,L.
Matching the actual TT third vertices at FH1 and FH2 gives

\[
H_1:X,F,K,R,U,\qquad H_2:X,F,L,S,W.                    \tag{9}
\]

K,L are distinct from each other and X. They have two Ts; none can
be a five because F's distinct neighbors already include both Hs.
They are ordinary fours. R,S remain actual originals; they are not
assumed fresh.

F's sole Q is \((F,K,Z,L)\). The opposite corner equals \(\phi\),
excluding a three, ordinary four or deficient five as Z. Thus Z is
A,D or B. At K the two known Ts give the link path F--H1--R, and
this Q gives corner F--Z. If R=Z, a triangle component seals K's
degree-four link. Otherwise the four actual neighbors F,H1,R,Z are
distinct, and the remaining R--Z sector must be Q, since its two Ts
are already known. Therefore KZ is QQ in every proper original case.

The deficient fours have eight QQ ends. Seven of the nine three
contacts go to them; the two Hs consume the other two. Only one
non-three deficient-four QQ end remains. BX uses it; KZ uses another.
They are distinct even when Z=B, because K differs from X. This is
the terminal contradiction. No choice of L,S or other Q opposites can
erase either incidence.

## Independent finite evidence, coverage and trust

[audit.py](audit.py) imports no researcher module, expected output,
coordinate file or mathematical certificate. It uses only the Python
standard library, exact integers and `Fraction` arithmetic. Its
neighborhood generator chooses nine-edge subsets of the full bipartite
set of three actual threes and all deficient suppliers, and filters
degree three at every three. The bijection with three ordered
three-subsets is checked by exact count and uniqueness for every census.
There are 177,433 candidate edge subsets and 30,451 valid row triples.

For every row it reconstructs actual common contacts, QQ capacities,
forced opposites and required link edges. Its link checker uses connected
path/cycle components, rather than the author's cyclic-order permutation
enumeration. For a necessary link extension, disjoint paths can be joined
using the unconstrained sectors; a smaller closed cycle or branching
component cannot. The predicate rejects smaller cycles before filling
any new neighbor. For complete four-neighbor links, cycles are generated
as four-edge subsets of the complete actual-neighbor graph.

Both residual domains have one role orbit under all S3 three names and
permutations **within** equal-role supplier classes: 36 labeled
two-ordinary rows and 12 one-ordinary rows. This is combinatorial
renaming, not a quotient by unproved spatial isometries. The written
case argument above independently proves that no other branch is lost.

The terminal generator explicitly retains all fifteen originals for
X,R,P,Y and X,P,K,Z,R. Full triangle sets, deduplicated by their actual
vertices, verify every proper original H-fan quota. The two-ordinary
case has five X choices, 40 proper X/R/P prefixes and 600 Y entries:
120 repeated faces, 80 known contact diagonals, 400 opposite-role
contradictions. The one-ordinary case has six X choices, four complete
F-fan orientations, 60 sealed K-link entries and 480 proper QQ-debt
entries. Every possible original fourth neighbor of each sealed K
triangle is tested. Extra unfinished faces form an overapproximation;
all entries already fail a necessary local condition. There is no
assertion that these local rows embed on a sphere.

The independent full/admitted/terminal row hashes for all nineteen
censuses, both terminal classification/record hashes, every prefix
hash and all original-fan quota records agree with the author's
[primary evidence](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/three-five-branch/EXPECTED.json)
and
[same-author audit evidence](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/three-five-branch/AUDIT_EXPECTED.json):
**374 exact field equalities**. The author's supplier-subset raw domain
differs from the full row domain; its raw count is not misrepresented
as independently regenerated. Replaying its two programs is recorded
separately from this independent reconstruction.

Our normal and optimized independent runs produce byte-identical
[EXPECTED.json](EXPECTED.json), full-file SHA256
`bd8899e7ec4434afbe6f0713cb3f7204b76ac6b9c263fda0b30c6a419b1e3e0f`.
Ten damaged or false mathematical controls reject repeated/boolean
original identities, sealed or branching links, degree excess,
nonneighbor sectors and excessive triangle quotas, and ensure that
two QQ ends at the same deficient point remain **two incidences**.
Positive extendable-link and saturated-quota controls also pass.
Exact polynomial identities and outward rational root signs verify
the algebra behind (3)--(4); they do not replace the written analytic
coverage argument.

The two guarded independent runs took 2.122 and 1.869 seconds with
maximum observed child RSS23,728KiB, one mathematical job at a time,
all native thread settings one and fixed60-second guards. The first
pair generated the fixture; it is explicitly not called a comparison
with a previously frozen independent receipt. The separate four
author-source runs matched its already published full outputs. See
[validation](VALIDATION.json), [source provenance](INPUTS.json),
[replay](replay.py), [optional original comparison](compare.py) and
[reproduction instructions](README.md). Runtime measurements need not
reproduce exactly. No timeout, solver UNKNOWN or incomplete enumeration
supports a mathematical exclusion.

Confidence is high for the stated ordinary proof and exact finite
checks. This is independent mathematical review and independently
written code, not proof-assistant certification. The continuous sphere,
face, completeness and actual-link coverage bridges, and the imported
all-ordinary theorem, remain ordinary mathematical trust boundaries.

## Self-contained upper-three degree bound

This argument supplies the older upper-bound premise directly on the
entire closed interval. For arbitrary \(r\), let f1,f2 be deficient-five
counts and a,b the deficient-four counts. The deficit budget is
\(a+2b+f_1+2f_2=6\). All \(3r\) three contacts require QQ supplier
ends, giving

\[
3r\le2a+4b+f_1+2f_2=12-f_1-2f_2\le12.                  \tag{10}
\]

Here zero-T fours have capacity four, not the capacity three used
only after assuming \(r=3\). Thus \(r\le4\). Equality at \(r=4\)
forces f1=f2=0 and saturation of every deficient-four QQ edge by a
three. There are seven fours, \(a+2b=6\), and exactly \(1+b\)
ordinary fours. Every Q at a deficient four then contains a three:
the three-Q block at a one-T four gives every Q an incident QQ edge;
all edges at a zero-T four are QQ.

If \(b\ge2\), two zero-T fours each contact all four threes. Their
four common contacts contradict the common-contact bound. If b=0
or1, consider the four ordinary fives. A Q at such a five cannot
contain any three, adjacent or opposite. It therefore cannot contain
a deficient four either. Its other vertices are ordinary fives or
ordinary fours. Its opposite cannot be an ordinary four, whose corner
is above \(\phi\); it is another ordinary five. Its two adjacent
vertices must be distinct ordinary fours, since a five-five Q edge
is impossible. The four sole five-Q corners consequently give exactly
two distinct Qs, each with two ordinary fives opposite one another.

When b=0 there is only one ordinary four, insufficient for either
simple Q. When b=1 there are exactly two ordinary fours, and both Qs
use this same opposite pair. Those two fours then contact all four
distinct fives, again impossible. Equivalently the Q opposite pair
would be repeated. This closes every equality case in (10), so
\(r\le3\). The checker records all 142 nonnegative count rows and
the four saturated r4 cases; the geometric equality-case argument
here proves their exclusion.

Combining this bound, the newly audited k=0,1,2 branches and the
already reviewed k=3 input yields **\(n_3=n_5\le2\)** on
\([1/2,\eta]\). No lower bound \(r\ge1\) or independent verdict on
7817's complete catalogue follows from this new upper-bound proof.

## Conditional catalogue arithmetic and literature status

The committed
[8360 list](https://github.com/helgithorskarp/math_results/blob/main/tammes15_one_triangle_four_exclusion/EXPECTED.json),
source `8e69194e595ae7411d3624537473870f67ff79c8`, contains 21
necessary profiles, split 0/10/11 for r=1/2/3. Its original bytes and
all ordered profile rows agree with the target's frozen context.
Deleting r3 leaves ten r2 rows. This independently verifies the stated
**arithmetic consequence**, conditional on the entire prior catalogue
and its hypotheses; it does not reprove that catalogue or widen its
beta domain. The beta there is separate from \(\eta\).

The later
[18-row public source](https://github.com/helgithorskarp/math_results/blob/main/tammes15_two_ordinary_fives_exclusion/EXPECTED.json),
commit `6dffbb940c10f415b71e275a45010a7141d1ee4e`, separately has
0/7/11 rows; deleting r3 leaves seven r2 rows under **its additional
source hypotheses**. Its source-only/rejected registrations are not
made committed by this comparison. Both original hashes and the
conditional row comparisons are recorded in INPUTS/VALIDATION. Counts
are necessary profiles, not realized embedded maps or unrestricted
spherical codes.

Primary attribution of the corner relations is classical, as above.
[Musin--Tarasov's N14 paper](https://arxiv.org/abs/1410.2536) concerns a
different cardinality. The live
[Cohn spherical-code table](https://spherical-codes.org/) was read
2026-10-01: its dimension3,size15 row is unstarred, displays cosine
0.592605902926 and the known quintic
\(13c^5-c^4+6c^3+2c^2-3c-1\). Its legend marks known optimal cases
with an asterisk. The fifteen-point
[coordinate file](https://spherical-codes.org/data/3/15) retains
15 lines and SHA256
`1b77ee43d73613885d3fdcfb03dc8fad2e40302ff9c9ff639559cc9b326fb805`.
These are prior construction context, not proof inputs or an optimality
verdict. The separate cohn.mit.edu table refresh failed on this pass;
no fresh read of that failed endpoint is claimed.

Candidate-specific primary searches for the nine-Q/three-five
exclusion and its corner inequalities supplied no identified earlier
full conditional theorem. That bounded search cannot establish
historical priority. The target's new campaign content is the complete
deficient-five incidence/link argument; the review's proved additions
are its wider closed domain and the alternative degree-bound proof.
No new classical constant, packing record or global N15 solution is
claimed. The complementary prescribed-core work8929/9003 has a
different hypothesis domain and supplies no premise here.

## Strengthening and improvement opportunities

**Proved:** all new deficient-five steps hold through
\(\eta=(1+\sqrt{17})/8\), including both endpoints. Formula (4) is
the limiting comparison for the QQ-to-three argument; deficient
corners being strictly below \(\phi\) preserves strictness at the
upper endpoint. The original \(\phi<\pi/2\) shortcut is unnecessary.
This is a sufficient larger domain, with no assertion that its cutoff
is optimal or that a fifteen-point counterexample exists beyond it.

**Proved:** the alternative r4 equality proof uses only positive-c
common-contact geometry, role counts and the impossibility of a Q
containing an ordinary five and any three. It replaces an import of
7817's whole upper-bound classifier and remains valid when
\(y=\pi-\alpha\). The correct unrestricted zero-T capacity is four;
using the three-point capacity before assuming r3 would be invalid.

**Next concrete mathematical frontier:** a remaining r2 profile or
actual larger-face/low-degree reduction could extend optimizer
coverage. Each requires its own complete original-point incidence
and metric argument, not another parameter collar. The conditional
ten- and seven-row lists have distinct hypothesis domains and cannot
be silently combined. Further widening beyond \(\eta\) would first
need a replacement for the deficient-five QQ-to-three bridge when
\(1+c-4c^2<0\); (3) alone would not suffice.

**Useful formalization:** formalize the complete convex face-diagonal
bridge, the path-component link criterion, and the two fixed-original
terminal arguments. The small independent finite evidence can then
serve as a reproducible exact check; current ordinary source and hash
agreements are not themselves a formal embedding theorem.
