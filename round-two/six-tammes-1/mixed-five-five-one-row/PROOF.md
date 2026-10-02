# Excluding the r2/a5/b0 mixed-five contact-map row

Actual author **six-tammes-1**, role **researcher**, 2026-10-02.
Complete exact computer-assisted author proof. Independent mathematical
review and proof-assistant formalization are pending.

## 1. Statement

Let fifteen distinct unit points have all pair products at most c, with
**1/2<c<3/5**. Their **complete** contact graph joins precisely pairs
with product c. Assume its minor geodesic embedding is connected and
cellular on the sphere, with degrees 3,4,5 and simple strictly convex
hemispherical triangular and quadrilateral faces, exactly nine Q faces.
The following profile is impossible:

* Two degree threes U,V.
* Two degree fives F,D, with respectively four and three T corners.
* Five one-T degree fours A,B,C,E,H, and six two-T degree fours.

There is no zero-T four. In the existing catalogue notation the row is
`(r,a,b,f0,f1,f2,O)=(2,5,0,1,1,0,6)`. The degree sum and Euler identity
give thirty edges, eight T faces and nine Q faces.

The main lemma uses no beta threshold or optimizer irreducibility. It is
a local contact-map exclusion, not a proof that an unrestricted optimizer
has this map class, a larger-face/low-degree exclusion, or an unconditional
numerical bound for Tammes-15.

The [three-five reduction8975](../three-five-branch/PROOF.md), source
`71f757b0cd0eafe8bf76fb0fa725ab2c43db3198`, and
[two-ordinary-five exclusion9025](../two-ordinary-five-branch/PROOF.md),
source `4634cb9daf85bf0c54aafe76f6141b03dabc1341`, leave this row in
their qualified catalogues. [The distinct r2/a3/b1 row9125](../mixed-five-three-one-row/PROOF.md),
source `154f38507807d7384a715926ab474072494dab37`, is prior work. Its
predicate implementation is adapted with the explicit new fifteen-point
role table; its old supplier/forced-face cover and zero-four role are
not reused as this row's data. The new cover and three-star completion
are specified below. No old fourteen-position ordinary-five core is used.

## 2. Credited geometry and necessary map tests

Put `alpha=acos(c/(1+c))`, `phi=2pi-4alpha` and
`rho(u)=2atan(1/(c tan(u/2)))`. We credit the spherical triangle/rhombus
identities to [Musin--Tarasov1312.5450, Proposition4.1](https://arxiv.org/abs/1312.5450)
and [their N14 paper1410.2536](https://arxiv.org/abs/1410.2536).
Their local consequences on our whole **open** interval are derived in
8975/9025 following the credited7817/7912 reductions:

1. A T has corner alpha. A Q has equal opposite corners; adjacent corners
   are u,rho(u). Completeness makes its diagonals strict noncontacts and
   `alpha<u<2alpha`. Also `3pi/8<alpha<2pi/5` and `alpha<phi<pi/2`.
2. A three has no T: one T and two Qs would sum to less than `5alpha<2pi`.
   A four has at most two Ts, and a five at most four. A Q corner at a
   three or two-T four exceeds phi, since its other corners sum to less
   than4alpha. F's sole Q corner is phi. D's two Q corners each are
   smaller than phi: they sum to `2pi-3alpha` and each exceeds alpha.
   Consequently a Q opposite F or D is one of **A,B,C,E,H**. The
   other five has an incompatible corner, and there is no zero-T four.
3. A three contacts only a one-T four or D. Every edge at a three is QQ.
   The two adjacent corners there sum to more than `2pi-2alpha`.
   For adjacent Q corners, `u+rho(u)<=4atan(1/sqrt(c))<2pi-2alpha`.
   Add this bound for each of the two Qs and subtract the sum at the
   three. The corresponding corners at the other endpoint sum to less
   than `2pi-2alpha`. Another three exceeds that value and a two-T four
   has exactly that value at a QQ edge. F has no QQ edge.
4. A QQ edge at D leads to a three. Its two corners at D are below phi,
   so the other endpoint receives two corners exceeding `y=rho(phi)`.
   The inequality `y>pi-alpha` is equivalent to
   `(1+c)(1+c-4c^2)>0`, valid here. A four's two remaining corners are
   at least alpha, giving total greater than2pi; a five also fails.
   Hence D has no three contact when its Qs are separated, or exactly
   one when they are adjacent. In the latter case both D Qs contain
   that three as an adjacent boundary neighbor.
5. Two distinct unit points have at most two common positive-c contacts.
   Their two contact planes meet in a line with at most two sphere
   intersections. The dependent antipodal case has no common contact.

Here QQ means Q on both sides of an edge. Counting consecutive Q sectors
in each neighbor cycle gives QQ caps: three3, one-T four2, two-T four1,
D1, F0. Known QQ edges count at **both** endpoints.

Every contact triangle is an actual T face. For its corners a,b,d and
another point p in the closed minor triangle, write
`p=lambda_a a+lambda_b b+lambda_d d`, with coefficients nonnegative
and sum L. Unit norm implies L>=1, whereas
`p.(a+b+d)=(1+2c)L>=1+2c>3c`, contrary to packing. Thus the minor
triangle has no other original, including boundary interiors, and the
noncrossing cellular embedding makes it a face. This is not an assertion
that arbitrary longer contact cycles are faces.

At each original, its corners form one cycle on its distinct contact
neighbors. Consecutive contacting neighbors give a T; a Q sector gives
a strict noncontact diagonal. A proper closed subcycle is impossible.
If one neighbor is still undetermined and the known corners span a path
on all other neighbors, that neighbor must join the two path ends.
Any additional T needs unused T capacity at its corresponding end
original. Too little capacity excludes the patch, even when the missing
original is a previously named point.

If both endpoints of a contact edge have complete known neighbor sets
and one known face, all compatible neighbor cycles give all possibilities
for its other face. Its two new neighboring roles coincide for a T,
or form a Q otherwise. The checker tries every such possibility and
rejects only when none passes the necessary constraints. It requires
no sufficient criterion for a spherical realization.

## 3. All supplier patterns and role assignments

Each of U,V has three neighbors among the five one-T fours and D.
D cannot meet both, since it has at most one QQ edge. If a one-T four
meets both U,V, these are its two QQ neighbors; their intervening
sector is Q. Its opposite is another common supplier. The two-plane
bound then makes the common set size exactly two, both one-T fours.
Otherwise the common set is empty.

The checker starts with all `20^2=400` ordered supplier pairs. Exactly
140 satisfy these necessary conditions. Permuting the **actual original
labels** of the five one-T fours and exchanging U,V gives precisely:

| N(U) | N(V) | ordered assignments |
|---|---|---:|
| A,B,C | A,B,E | 60 |
| A,B,C | A,B,D | 60 |
| A,B,C | E,H,D | 20 |

The first two force Q(A,U,B,V). The third has no shared supplier.
Every admitted ordered pair is mapped to a representative, not merely
counted. This renaming is not a spatial symmetry assumption.

Fixed ordinary roles are assigned the first available ordinary labels.
Other distinct fan slots are assigned each one-T label or an unused
ordinary original; unused ordinary labels are injected in first-occurrence
order. Two slots give31 words, four slots501 words. This is exhaustive
because ordinary labels have the same quotas and no three contact. Every
later unknown role ranges over **all fifteen actual labels**. In particular
Q opposites may reuse earlier boundary roles whenever simplicity and
the necessary constraints permit it; they are not presumed new.

## 4. Noncontacting F,D

Write F's four-T path `e,I,R,S,p`, with Q(F,e,h,p).
I,R,S are three distinct ordinary fours, each with both Ts full.
The endpoints e,p are distinct one-T or ordinary fours and h is one-T.
All three supplier families,31 endpoint words and five opposite labels
give **465** initial patches, including nonsimple assignments which
the necessary tests reject. Seventy-one are admitted.

If an endpoint is ordinary, it needs a second T. Its inward ordinary
neighbor has both Ts full. The known neighbor path is inward-F-h;
the missing neighbor must close its two ends. The new T cannot use
the saturated inward original, so it is T(endpoint,h,J).
All fifteen J labels are tried. If both endpoints are ordinary the
same argument applies to each; two coincident Ts would contact across
the Q diagonal and are rejected. The885 first-step tests admit80
prefixes, and there is no surviving second-step branch. Including the
one-T/one-T cases leaves **92** partial patches for Section6.

## 5. Contacting F,D

FD cannot be a Q side: both five corners would be at most phi<pi/2,
whereas the rhombus equation is
`cot(u/2)cot(v/2)=c<1`. Thus FD has T on both sides. Their two distinct
thirds a,b exhaust F,D's common contacts; all other fan roles are
distinct originals.

In D's cycle `(a,F,b,c,d)`, sectors a-F and F-b are T and its third
T is in one of the other three sectors. F's D position has three
possibilities. The complete nine-case cover leaves five, as follows;
the other four force a third T at a nonfive.

| F D-position | D third-sector index | representative |
|---:|---:|---|
|1|3|separated, first form|
|1|4|adjacent|
|2|3|separated, second form|
|3|2|adjacent, reversed original roles|
|3|3|separated first form, reversed original roles|

Sector indices use0-based pairs in `(a,F,b,c,d)`. Reversal just renames
actual originals. It assumes no metric symmetry.

For **separated** D Qs, D has no three contact and only the first supplier
family remains. F's paths are `a,D,b,x,y` or `x,a,D,b,y`, and D's isolated
third T is T(D,c,d). The two full ordinary internals are fixed. Four
other distinct at-least-one-T slots have501 words. The Qs are

`Q(F,first,h,last), Q(D,b,k,c), Q(D,d,l,a)`.

All `5^3` actual h,k,l labels are retained. The **125,250** initial
patches admit12, which are passed to Section6.

For **adjacent** D Qs, rename its unique three contact V. Both D-containing
supplier families remain, with all shared opposite aliases retained.
The paired fans have F path `I,D,R,S,e` and D T path `R,F,I,w`.
Their five distinct Ts are FID,FDR,FRS,FSe,DIw; I,R,S are ordinary
with full two-T quotas. Distinct e,w have31 one-T/ordinary words.
The Qs are

`Q(F,I,h,e), Q(D,w,k,V), Q(D,V,l,R)`.

The **7,750** initial patches admit18. The complete link at I forces
Q(I,w,J,h); all fifteen J labels give270 tests and18 prefixes.
The complete link at R then forces Q(R,S,M,l); all fifteen M labels
give270 tests and48 prefixes. These forced faces are Q because the
two existing Ts at the respective ordinary vertex are full.
All48 prefixes proceed to Section6.

## 6. Completing the two degree-three stars

The supplier edges already determine the complete neighbor set of each
three. Every pair among its three neighbors is consecutive, and every
sector is Q. For any still missing pair a,b at v in{U,V}, its face must
be Q(v,a,X,b). Try all fifteen actual originals X and retain precisely
the patches passing the necessary tests of Section2.

At each recursive state the implementation examines every missing sector,
then chooses the sector with fewest surviving opposites, breaking ties
by `(v,a,b)`. If that set is empty the state is impossible. Otherwise
every surviving actual-original assignment for that chosen sector is
continued. Each step fills at least one new three corner, so recursion
terminates after at most six added faces. Any actual map would survive
one child at every choice and eventually supply all six corners.

| input case | starting patches | recursive states | opposite tests | empty-sector leaves | completed stars |
|---|---:|---:|---:|---:|---:|
|noncontacting|92|116|6,480|96|0|
|separated D Qs|12|14|810|12|0|
|adjacent D Qs|48|84|3,240|48|0|

Every branch ends at an empty necessary sector. Thus no initial case
can complete, proving the row exclusion.

## 7. Reproducibility, dependencies and remaining frontier

[patch.py](patch.py) is the finite-set predicate, and [check.py](check.py)
regenerates the entire cover without numerical signs, samples, a solver,
network access or external runtime inputs. [audit.py](audit.py) imports
no primary source: it uses edge/neighbor bit masks, contact-triangle
extraction by common neighbors, directed face boundaries and recursive
neighbor-cycle walks. Its supplier and ordinary-slot generators use
separate algorithms. The written geometric premises and forced-face
case specification are shared. This is a separate same-author exact
audit, not independent researcher review or a formal proof.

Both implementations agree on every tested admission bit, every selected
three corner, and every admitted intermediate tuple, including the full
**145,420** patch-test digest
`c9956095697e3d5b5b561d6022cd436f161a40b646eb6980438df1176ac9f3cf`.
The admitted-prefix/selected-corner digest is
`915facaa0cfcb33696113b97e0d1bcac5eda53a50d4833b725e524161af64c1c`.
[EXPECTED.json](EXPECTED.json) is the compact complete output.
[controls.py](controls.py) checks positive partial incidences, damaged
faces/diagonals/links/QQ capacities, a missing-star capacity release,
and an admitted paired-fan prefix whose three missing corners each
reject all fifteen original opposites. Such positive prefixes are
necessary incidence data, not asserted sphere packings.
[VALIDATION.json](VALIDATION.json) records normal and optimized runs.
Bulk case traces are regenerated and omitted. The main trust boundary
is the written geometry-to-finite-cover argument above.

Deleting this literal row after9125 changes the committed qualified
catalogue from **six to five**, and the later source-only catalogue from
**four to three**. Every original catalogue hypothesis, including any
beta assumption, remains on this optional corollary. Their derivations
are imported, not regenerated; catalogue rows do not assert realizations.
[DEPENDENCIES.json](DEPENDENCIES.json) records exact sources and scopes.

The [two-five review9119](../../six-reviewer-3/two-fives-audit/REVIEW.md),
source `3cd270405739c719b1add3891475c99b5586ef39`, independently reviews
9025 and extends its own interval/endpoint statements. It supplies no
verdict or closed-interval extension for this new row. The peer's
[G22 frame9149](../../six-tammes-2/twenty-two-contact-frame/PROOF.md),
source `07f591fe1c8e3eeb8f125c7c40dc22c8d1c2a637`, has nine contact
triangles and belongs to a different prescribed-motif class; its
packing orientation/Gram bound is complementary context, not a premise.

The live [fifteen-point coordinate file](https://spherical-codes.org/data/3/15)
was refreshed2026-10-02:890bytes, SHA256
`1b77ee43d73613885d3fdcfb03dc8fad2e40302ff9c9ff639559cc9b326fb805`.
The last successful [Cohn table](https://cohn.mit.edu/spherical-codes/)
refresh on2026-10-01 had unstarred incumbent cosine
`0.59260590292507377809642492233276`; the2026-10-02 table fetch failed
and is not claimed as a new successful refresh. Musin--Tarasov1410.2536
solvesN14. The bounded current primary-literature/repository search
supports no globalN15 theorem or exhaustive historical-priority claim.

The next qualified count frontier is two three-T fives,
`(r,a,b,f0,f1,f2,O)=(2,4,0,0,2,0,7)`. The unrestricted larger-face,
low-degree and optimizer-coverage bridges remain separate open work.
