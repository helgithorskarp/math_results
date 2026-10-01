# The r2/a3/b1 mixed-five row is excluded

Actual author: **six-tammes-1**, role **researcher**, 2026-10-01.
Exact computer-assisted author proof. Independent researcher review and
proof-assistant formalization are pending. The finite checks use integers
and finite sets; the geometric bridges below are unformalized.

## 1. Statement and precise scope

Let fifteen distinct unit vectors have all pair products at most c, with
`1/2<c<3/5`. Their **complete** contact graph has an edge exactly when the
product is c. Assume its minor geodesic embedding is connected and cellular
on the sphere, with simple strictly convex hemispherical triangle and
quadrilateral faces, exactly nine quadrilaterals, and degrees 3,4,5.
The following profile is impossible:

* Two degree threes U,V and two degree fives F,D.
* F has four triangular corners and D has three.
* Among eleven degree fours, A,B,C have one triangular corner each,
  Z has none, and seven have two each.

In the previous catalogue notation this is
`(r,a,b,f0,f1,f2,O)=(2,3,1,1,1,0,7)`.
The degree sum gives E=30; Euler gives eight triangles and nine quadrilaterals.
This statement assumes no beta threshold or optimizer irreducibility.
It does not prove occurrence of this contact-map class in an unrestricted
optimizer, exclude larger faces or lower degrees, or improve an unconditional
numerical Tammes-15 bound.

The [three-five reduction8975](../three-five-branch/PROOF.md), source
`71f757b0cd0eafe8bf76fb0fa725ab2c43db3198`, and
[two-ordinary-five exclusion9025](../two-ordinary-five-branch/PROOF.md),
source `4634cb9daf85bf0c54aafe76f6141b03dabc1341`, leave this row in both
of their qualified residues. Closing this mixed row is the new result.
We import neither a global optimizer classification nor an old local
fourteen-position core for two ordinary fives.

## 2. Credited local geometry and two small completion rules

Write T,Q for triangle and quadrilateral faces. Put
`alpha=acos(c/(1+c))`, `phi=2pi-4alpha`, and
`rho(u)=2atan(1/(c tan(u/2)))`.
The equilateral triangle and rhombus identities are credited to
[Musin--Tarasov1312.5450, Proposition4.1](https://arxiv.org/abs/1312.5450)
and [their N14 paper](https://arxiv.org/abs/1410.2536).
The interval facts used here are rederived in9025 Section2 and
[8975 Section2](../three-five-branch/PROOF.md), following7817/7912.
Their relevant conclusions are:

1. A T has corner alpha. Opposite Q corners agree; adjacent corners
   are u,rho(u). Completeness makes both diagonals strict noncontacts,
   giving `alpha<u<2alpha`, `3pi/8<alpha<2pi/5`, and `alpha<phi<pi/2`.
2. A three has no T. A four has at most two Ts, and a five at most four.
   Every Q corner at a three or two-T four exceeds phi. F's sole Q
   corner is phi; each of D's two Q corners is strictly smaller than phi,
   since the other corner exceeds alpha and their sum is `2pi-3alpha`.
   Thus any Q opposite F or D is one of A,B,C,Z.
3. A three can contact only a deficient four or D. To see the exclusion
   of a three or ordinary four, adjacent Q corners have sum at most
   `2b0`, where `b0=2atan(1/sqrt(c))<pi-alpha`. The two corners at a
   three surrounding an edge have sum greater than `2pi-2alpha`, so
   their neighboring corners have smaller sum than this; another three
   or an ordinary four cannot supply them. F has only one Q.
4. D's QQ edges lead to threes. Indeed, their neighboring Q corners
   exceed `y=rho(phi)>pi-alpha`. The last inequality is equivalent to
   `(1+c)(1+c-4c^2)>0`, valid throughout our interval. A neighboring four
   would have total angle greater than `2y+2alpha>2pi`; a five also fails.
   Thus D either has separated Q corners and no three contact, or adjacent
   Q corners and exactly one three contact. In the latter case **each
   Q at D contains that three as an adjacent boundary neighbor**.
5. Two distinct unit points have at most two common positive-c contacts:
   their contact planes intersect in a line meeting the sphere at most
   twice. The only dependent distinct case, antipodality, has none.

Here and throughout, a QQ edge has Q on both sides. A four with one T has
exactly two QQ edges; a four with two Ts has at most one; D has at most one;
F has none. A zero-T endpoint makes every incident edge QQ, at both ends.

We also use the elementary **empty contact triangle** fact. If another original p
lay in the closed minor spherical triangle of three mutually contacting
unit vectors a,b,e, write `p=lambda_a a+lambda_b b+lambda_e e`, with
nonnegative coefficients and sum L. Unit norm and the triangle inequality
give L>=1, whereas
`p.(a+b+e)=(1+2c)L>=1+2c>3c`.
Thus p violates at least one packing product. Boundary interiors are also
excluded. In the noncrossing cellular contact embedding, this empty minor
triangle is a face. Every contact three-cycle therefore gives an actual T;
this assertion is not made for arbitrary longer cycles.

The face corners at a degree-d original form **one cycle on its d distinct
contact neighbors**. A consecutive pair contacts exactly in a T sector;
a Q sector is a strict noncontact diagonal. A known proper closed subcycle
cannot be part of that link. Two forced corners at an edge determine the
other T or Q at that edge, including its opposite boundary contact.
These statements are used only for actual consecutive sectors.

A useful completion rule is the following. Suppose an original has one
contact still undetermined and its known corners form a spanning path on
its other neighbors. The missing neighbor must join the two path ends.
Each additional T needs unused T capacity at the corresponding end
original. If the vertex needs more Ts than its two ends can supply, its
star cannot be completed. This remains valid when the missing neighbor is
any previously named original; no new-point assumption is involved.

Finally, in F's four-T path an ordinary endpoint E with inward ordinary
neighbor I has second T through F's Q opposite H, **provided I already
has both Ts and its other T excludes E**. Its fourth neighbor J then gives
T(E,H,J). The alternatives are a third T at I or the forbidden Q diagonal
FH. We only apply this qualified rule when those premises have been checked.

## 3. Complete three-neighbor cover

Every contact of U or V lies in `{A,B,C,Z,D}`. Each three chooses three
distinct suppliers. D cannot supply both. A one-T supplier meeting both
threes has its two QQ edges consecutively and forces Q(S,U,K,V), where K
is another common contact. The common-contact bound limits the shared
suppliers to two. A shared Z alone need not force this Q; it is retained.

Of the 100 ordered pairs of supplier triples, 10 have three common
contacts, 30 further pairs exceed D's capacity, and 18 further pairs
violate the forced paired supplier. The 42 necessary pairs have six
families, under A/B/C renaming and U/V exchange:

| U suppliers | V suppliers | Labeled pairs |
|---|---|---:|
| A,B,C | A,B,Z | 6 |
| A,B,C | A,B,D | 6 |
| A,B,Z | A,B,D | 6 |
| A,Z,B | A,Z,C | 6 |
| A,Z,B | A,Z,D | 12 |
| A,B,Z | C,Z,D | 6 |

These are necessary incidences, not geometric realizations. Renaming actual
originals is not a metric symmetry assumption.

## 4. Noncontacting F,D

F has path `E,I,R,S,P`, with four Ts and Q(F,E,H,P). The three internals
I,R,S are distinct ordinary fours with full two-T quotas; D is not a
neighbor. Endpoints are one-T or ordinary fours. H is one-T or Z.
If both endpoints were ordinary, the qualified rule would give two
**distinct** Ts at H. They cannot coincide because that would introduce
a contact across a Q diagonal. At least one endpoint is therefore one-T.

A one-T endpoint cannot meet both threes: F, its inward neighbor and H
are three distinct non-three contacts. A one-T opposite H also cannot
meet both: its four neighbors would be the two endpoints and U,V, its
known endpoint-pair sector is Q, and every other sector contains a three.
This would give no T at H. Shared one-T suppliers are unavailable in these
collar positions.

An endpoint E-H edge is QQ if E is one-T. If E and H meet the same three,
its contact triangle contradicts that QQ edge. If both endpoints are
one-T and H has a three contact, H's sole T would use an endpoint whose
unique fan T is already full. If just E is one-T, P ordinary, and E,H
both have three contacts u,v, their full stars force the other face at
EH to be T when u=v, or Q(E,H,v,u) when u differs from v. The latter
would make U,V contact, which is forbidden. If H=Z and P ordinary, the
qualified endpoint rule forces a T at Z.

[check.py](check.py) retains every endpoint and opposite assignment:
seven endpoint roles (A/B/C and four unused ordinary originals), ordered
distinct endpoints, and all four H roles with repeated Q vertices excluded.
This gives **5,544 collars**. Applying the preceding justified rules leaves
only two orientations, with 96 labeled collars each. The exact complete
role maps, not merely the totals, are checked. In both orientations

`N(U)={A,Z,B}, N(V)={A,Z,D}`,

C meets neither three, P is ordinary, and the one-T endpoint/opposite
are C/B or B/C. Normalize I,R,S,P as four distinct ordinary originals.
Every remaining unknown is assigned **all fifteen actual labels**.

* Endpoint C, opposite B: P forces T(P,B,J). The other face at CB is
  Q(C,B,U,K), so K meets U. Repeated vertices exclude B; K=A cannot
  complete its one-T star with saturated C and zero-T V as its path ends.
  Thus K=Z. The shared Q(A,U,Z,V) and the full link at C now force
  Q(C,Z,M,I). The full contacts of I leave M=F or R; F is a Q contact diagonal,
  so M=R. The next face forces the
  next ordinary internal S to contact U or V. The finite audit retains
  every J,K,M alias and checks these star/edge consequences.
* Endpoint B, opposite C: P forces T(P,C,J). C's remaining QQ contact K
  appears in Q(B,C,K,U). Its shared-A choice cannot complete A's star;
  its Z choice forces Q(U,B,I,A) from the full links at U,B. A's
  remaining T would then use saturated I, which is impossible.
  All fifteen choices of J and K are checked without inventing a new label.

Neither orientation completes. Hence F,D must contact in a hypothetical row.

## 5. Contacting F,D: all paired fans and actual opposites

Five-five contacts cannot lie in Q, by the rhombus corner identity (both
five corners are at most phi). Thus FD is T-T. Its two distinct third
vertices exhaust the possible common contacts of F,D. Apart from these,
their fans have no original aliases.

F has four T sectors. Orient D's cycle as `(a,F,b,c,d)` around their
shared thirds a,b; its T sectors a-F and F-b are known. Its third T is
in one of the three remaining sectors. F's D-position has three choices.
The complete **nine-case** cover leaves
`(position,third_sector)=(1,3),(1,4),(2,3),(3,2),(3,3)`;
the other four force a third T at a nonfive. Reversal identifies two
separated-Q forms and one adjacent-Q form, by explicit original-role
renaming, not a spatial symmetry.

### Separated Qs at D

D has no three contact. The supplier cover leaves only shared AB with
extras C/Z, or shared AZ with extras B/C. F's representative paths are

`a,D,b,x,y` or `x,a,D,b,y`,

and D's isolated third T is T(D,c,d). The three actual Qs are

`Q(F,first,H,last), Q(D,b,K,c), Q(D,d,L,a)`.

The two full ordinary F-internal roles are fixed; the four remaining
at-least-one-T slots are distinct one-T or ordinary fours. Ordinary
originals are renamed in order of first occurrence: there are 73 slot
words. All `4^3` choices H,K,L in A/B/C/Z remain, including endpoint
aliases. The **18,688** complete initial patches all fail the necessary
map tests. In particular, releasing the spanning-path T-capacity rule
leaves exactly two labeled necessary patches: both have ordinary F
endpoints with zero-T Z opposite. Their inward ordinary neighbors have
both Ts full, so the endpoints' required second Ts cannot exist.
These released patches are not asserted to be sphere packings.

### Adjacent Qs at D

Rename D's unique three contact V. The sole paired-fan form is

`F: I,D,R,S,E`, `D T-path: R,F,I,W`.

Its five distinct Ts are FID,FDR,FRS,FSE,DIW. I,R,S are ordinary fours,
and E,W each have at least one T. The actual Qs are

`Q(F,I,H,E), Q(D,W,K,V), Q(D,V,L,R)`.

K,L are deficient-four contacts of V. If L were a shared one-T supplier,
its known Q corners V-R and U-V would force its unique T through R,
whose two Ts are full. This excludes both shared-AB supplier families.
The only remaining necessary supplier rows, up to original renaming, are

`N(U)={A,Z,B}, N(V)={D,A,Z}` or
`N(U)={A,B,Z}, N(V)={D,C,Z}`.

The E,W slots cannot coincide or reuse I,R,S: that would repeat a fan
neighbor or give a third common contact of F,D. Their one-T/ordinary
assignments have 13 canonical words, with every one-T alias retained.
All H,K,L choices give **1,664** initial patches. Eight pass the local
necessary tests. The full link at I forces Q(I,W,J,H); all fifteen J
originals give 120 tests and sixteen admitted prefixes. The full link at
R then forces Q(R,S,M,L); all fifteen M originals give 240 tests and
**no admitted prefix**. This closes the contacting case and the row.

## 6. Exact finite verification and trust boundary

[patch.py](patch.py) checks necessary consequences of an actual map:
simple faces, Q noncontact diagonals, degree and T quotas, facial contact
triangles, common-contact capacity, the proved five-opposite and D-three
corner rules, QQ capacities, partial link degrees/closed subcycles,
spanning-path T capacity, and every compatible full neighbor cycle.
For an edge with one known face and full stars at both endpoints it tries
all possible other T/Q faces. If none can satisfy the necessary tests,
that edge cannot complete. It does not require these tests to be sufficient
for spherical realization; excluding every necessary case is enough.

[check.py](check.py) regenerates the covers. [audit.py](audit.py) imports
no primary source: it uses contact bit masks, common-neighbor triangle
extraction, directed face boundaries and recursive link walks. It separately
regenerates supplier sets and canonical ordinary slot words. It shares the
written geometric premises and forced-face case specification, so this is
a separate same-author finite audit, not independent researcher review.
The entire expected report agrees, including every tested state's admission
bit and every admitted intermediate tuple, not only aggregate empty totals.

The 20,907 tested local patches have canonical full case SHA256
`edced34501840ef605e136571a0a678174b0b1605c62470b0b61a78131e413bd`;
the admitted-prefix SHA256 is
`39fce097163c340be528c9567a837368cb767a96649ba1f286067038a0362f16`.
[EXPECTED.json](EXPECTED.json) supplies the full compact output.
[controls.py](controls.py) checks positive partial-incidence fixtures,
repeated/diagonal/closed-link/QQ damages and the exact two-patch release.
[VALIDATION.json](VALIDATION.json) records normal and optimized runs.
Bulk case traces are regenerated, not published. No samples, floating-point
signs, solver, network data or private corpus enter a check.

Deleting this row from9025's qualified residues changes the committed
catalogue basis **seven to six** and the later source-only basis **five to
four**, with every original catalogue hypothesis retained. Catalogue
membership is not a realization claim. [DEPENDENCIES.json](DEPENDENCIES.json)
records exact source/graph premises and distinguishes local facts from
these optional catalogue corollaries.

The full [three-five review9043](../../six-reviewer-3/three-five-audit/REVIEW.md),
source `cbcba14f1a1b573739e5c2c2f0c2ec73e59e1f2c`, was read before this work.
Its independent verdict and wider closed interval belong to8975, not to
this new row theorem. [The peer negative-core extension9057](../../six-tammes-2/negative-core-extensions/PROOF.md),
source `62ac057c7ae5efeb6cfc865d3a96e2164e777402`, concerns a different
prescribed contact motif and is not a premise here.

The live [Cohn table](https://cohn.mit.edu/spherical-codes/) and
[fifteen-point coordinates](https://spherical-codes.org/data/3/15) were
refreshed2026-10-01. The unstarred incumbent cosine remains
`0.59260590292507377809642492233276`; the 890-byte coordinate table SHA256
is `1b77ee43d73613885d3fdcfb03dc8fad2e40302ff9c9ff639559cc9b326fb805`.
The primary seed1410.2536 solves N14. The bounded current literature and
repository search does not establish historical priority or global N15
optimality. Larger-face and optimizer-coverage problems remain separate.
