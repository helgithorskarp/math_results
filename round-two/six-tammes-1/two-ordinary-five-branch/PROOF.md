# The two-five nine-quadrilateral branch cannot have both fives ordinary

Actual author **six-tammes-1**, role **researcher**, 2026-10-01.
Status: complete author-checked conditional geometric proof with exact
rational-function and finite contact checks. Independent mathematical
review and proof-assistant formalization are pending.

## 1. Statement, novelty and scope

Let fifteen distinct unit points have minimum geodesic separation d,
and put c=cos(d), with **1/2<c<3/5**. Assume their **complete**, connected
contact graph has degrees in{3,4,5}. Its minor-geodesic edges are assumed
to give a cellular sphere embedding into simple strictly convex
hemispherical triangle(T) and quadrilateral(Q) faces. Assume nine Qs
and exactly two degree fives.

**Theorem.** The two degree fives cannot both have four T faces.
Thus at least one of them has at most three Ts.

A two-T four and a four-T five are called ordinary. A one-T or zero-T
four is deficient. Euler gives E=30,T=8,n3=n5=2,n4=11. If a,b count
one-T and zero-T fours, respectively, the two ordinary fives give

    a+2b=6, ordinary fours O=11-a-b=5+b.

The four possible rows(a,b,O) are(6,0,5),(4,1,6),(2,2,7),(0,3,8).
The(2,2,7) row was already excluded by the published
[two-ordinary-fives proof](../../../tammes15_two_ordinary_fives_exclusion/PROOF.md),
source6dffbb940c10f415b71e275a45010a7141d1ee4e; that source was not
graph-committed. Section5 gives a different short proof of that credited
case. The new content is closing the other rows and the adjacent case
with two degree threes. No historical priority claim is made.

The older [adjacent-fives proof](../../../tammes15_adjacent_fives_exclusion/PROOF.md),
source21d7c373cfa2234494841a11642b53baf0380b7b, lemma7631
`bafkreiekk7nnksnqfuav2yd2bezeildzxvcpp25ymk75ho4s7nqhumwvhi`,
already constructs the local fourteen-position core used in Section3.
Its exclusion theorem assumes thirteen degree fours and is not applied
here. We credit and reconstruct its local core. Our new completion
obstructions use the two threes, triangle counts and zero-T fours.

The theorem uses no beta threshold, metric symmetry, incumbent proximity
or optimizer-irreducibility premise. It excludes one specified complete
T/Q branch; it does not improve a global numerical Tammes bound, exclude
larger faces or prove that an unrestricted optimizer has these hypotheses.

## 2. Credited local geometry, rederived

The equilateral triangle/rhombus identities are credited to
[Musin--Tarasov, Proposition4.1](https://arxiv.org/abs/1312.5450)
and their [N14 paper](https://arxiv.org/abs/1410.2536). The following
full-interval corner and three-neighbor facts occur in
[lemma7817](../../../tammes15_nine_quad_odd_degree_reduction/PROOF.md)
and [the local part of lemma7912](../../../tammes15_nine_quad_single_three_fan_reduction/PROOF.md).
They do not require a unique three. We include their derivation so the
present statement does not import a unique-three reduction.

Put alpha=acos(c/(1+c)), phi=2pi-4alpha,
b0=2atan(1/sqrt(c)), rho(u)=2atan(1/(c*tan(u/2))). A T has corner alpha.
Opposite Q corners agree; adjacent Q corners u,v satisfy
cot(u/2)cot(v/2)=c, equivalently v=rho(u). Taking the axis through
the sum of an opposite pair puts a Q in the form
(x,0,z),(0,s,w),(-x,0,z),(0,-s,w), with positive entries,
x^2+z^2=s^2+w^2=1 and zw=c. The two positive half-angle cotangents
are wx/s and zs/x. This follows from the two common-contact solutions
of the opposite pair; convexity and the hemispherical cell select the
minor boundary. A diagonal across corner u has inner product
c^2+(1-c^2)cos(u). Both diagonals are strict noncontacts by completeness.
Together with rho(alpha)=2alpha this gives

    alpha<u<2alpha, 3pi/8<alpha<2pi/5, alpha<phi<pi/2.       (1)

The endpoint comparisons reduce to529>512 and49>45. Angle sums now
give zero Ts at a three, at most two at a four and at most four at
a five. Every Q corner at a three or ordinary four is **greater than
phi**: subtract the other two Q corners, or the other Q corner and
two alphas, using(1). An ordinary five's sole Q corner is exactly phi.
No Q can have adjacent fives, because their corners are at most phi
and their half-angle cotangent product would exceed1, whereas c<1.
No ordinary five can have a three or ordinary four opposite it in Q.

For adjacent Q corners, u+rho(u)<=2b0. For half-tangents with product
1/c>1, their arctangent sum is largest when equal. Also b0<pi-alpha,
since cos(b0)=(c-1)/(c+1)>-c/(c+1)=cos(pi-alpha), using2c>1.
At a three, the two Q corners surrounding a contact have sum greater
than A=2pi-2alpha. The corresponding two neighbor corners have sum
less than4b0-A<A. This excludes another three and an ordinary four,
whose two Q corners would sum to A. An ordinary five has just one Q
and cannot supply both sectors. Thus in the branch under study,

    every contact of either three leads to a deficient four.           (2)

Two distinct unit points have at most two common positive-c contact
neighbors: their affine contact planes intersect in a line meeting the
sphere in at most two points. The only dependent distinct case is
antipodality, which has no common contacts for c>0.

At every original vertex the face corners form one cycle on its
distinct contact neighbors. In an actual T/Q sector, its two neighbors
contact exactly when that sector is T. A Q sector's neighbors are a
strict noncontact diagonal. This rule concerns consecutive link pairs,+not arbitrary pairs of neighbors. We use it only after their cyclic
adjacency is forced by already known faces.

Each ordinary five has one linear five-neighbor path with four T
sectors and one closing Q. An internal path neighbor has two Ts;
an endpoint has at least one. Apart from the other five, internals
are ordinary fours and endpoints are one-T or ordinary fours.
Noncontacting fives cannot share an internal or have an internal reused
as the other's endpoint: the distinct fan Ts would exceed the nonfive
two-T ceiling. A one-T four cannot contact both noncontacting fives:
its unique T would contain both and imply that they contact.

First exclude b=3. Then a=0, so(2) forces both threes' three distinct
neighbors to be precisely the three zero-T fours. They would have
three common contacts. Hence **b<=2 and O<=7** for the rest of the proof.

## 3. Contacting fives: credited core, new completion obstruction

If the ordinary fives F,G contact, their edge is T-T. Its two distinct
thirds exhaust their common contacts, giving eight distinct originals
in their two fans. Orient each fan consistently across this edge.
The other five occupies positions i,j in{1,2,3}. The complete nine
paired-fan cases and the two-T ceiling at the shared thirds leave
only(i,j)=(1,1),(3,3). They are the same full labeled face patch under
actual-role relabeling. The checker verifies the complete face and Gram
correspondence, not a numerical congruence or symmetry assumption.

Label F=0,G=1. One representative has paths

    F:2,1,3,4,5; G:3,0,2,6,7;
    T faces012,013,034,045,126,167.                       (3)

Vertices2,3,4,6 are ordinary fours;5,7 are at least one-T fours.
The old core construction now applies locally without assuming that
every other original is a four. In an equilateral coefficient basis
at1,6,7, the Gram matrix is H=(1-c)I+cJ. Its eigenvalues1-c,1-c,1+2c
are positive. Let r=2c/(1+c). Set a1=e0,a6=e1,a7=e2 and successively

    a2=r(a1+a6)-a7; a0=r(a1+a2)-a6; a3=r(a0+a1)-a2;
    a4=r(a0+a3)-a1; a5=r(a0+a4)-a3.

These are the second unit common-contact solutions across actual
T edges. For Q with old opposite f and its neighbors a,b, its other
opposite is

    q=2c/(1+<a,b>)(a+b)-f.                              (4)

Cauchy--Schwarz at its common-contact f gives1+<a,b>>=2c^2>0.
Original injectivity chooses the solution different from f.
The sole Qs at F,G, followed by the closing degree-four sectors at
2,3,4,6, force the actual faces

    (0,2,8,5),(1,3,9,7),(2,6,10,8),(3,4,11,9),
    (4,5,12,11),(6,7,13,10).                            (5)

For example the first Q and Ts at2 give link path8-0-1-6;
the other sector6-8 is Q. The exact audit proves all fourteen positions
distinct, justifying each new original label before its contact/link
count is used. The same audit checks all unit identities, all poles,
all91pair relations, and that these Q-closing pairs are noncontacts.

There are25fixed contacts,62strict packing gaps c-<ai,aj>>0 throughout
the whole open interval, and four exceptions:

    class A:(8,12),(9,13); class B:(10,12),(11,13).         (6)

The two packing gaps in each class are identical rational functions.
For all exceptional pairs1-<ai,aj>>0 is proved, even if their packing
gaps are negative. Thus all fourteen positions are distinct everywhere;
they need not form a packing everywhere. An actual packing has both
class gaps nonnegative and either whole class can contact only at zero.

The fixed degrees are5 at0,1;4 at2..7;3 at8..11;2 at12,13.
Let v=14 be the remaining actual original. It has degree3 or4, since
the only fives are0,1. Its removal leaves30-deg(v) core contacts.
If deg(v)=4, the required26 is impossible: the count is25 plus an
even number from(6). Therefore deg(v)=3 and the core has27contacts:
**exactly one exceptional class contacts**. The full degrees then
leave precisely four neighbor triples per class, obtained by omitting
one vertex from the following sets:

| Class | All possible neighbors of v are three of |
|---|---|
| A | {10,11,12,13} |
| B | {8,9,12,13} |

The omitted vertex is the other degree three. This covers all original
contacts of v; no spatial position for v is assumed.

In A, omitting10 or11 makes that three contact ordinary6 or4,
respectively, contradicting(2). Omitting12 or13 fails as follows.
The full link at5 has known sectors0-4(T),0-8(Q),4-12(Q), leaving
8-12. Class A makes that sector T. Thus12 belongs to T(5,8,12)
and cannot be a zero-T three. Likewise the link at7 forces T(7,9,13).
Every A triple is excluded.

In B, omitting8 or9 makes that three opposite ordinary five0 or1
in its Q, contradicting the unequal phi corners. If instead12 or13
is omitted, v contacts8 and9. At8, the two known Q corner pairs
are2-5,2-10. Its fourth neighbor is the zero-T three v, so both
remaining sectors5-v,v-10 are Q. Thus8 is a zero-T four. The same
argument makes9 a zero-T four. The now complete contacts of10 are
{6,8,13,12}; known Q corners6-8,6-13 leave8-12,12-13, both strict
noncontacts (class A is absent). Thus10 is also zero-T. At11, neighbors
{4,9,12,13} give the same conclusion from4-9,4-12 and9-13,13-12.
This gives four distinct zero-T fours8,9,10,11, contrary to b<=3
from the triangle census (even before the stronger b<=2). Every B
triple is excluded. The contacting-fives case is empty.

## 4. Opposite fives in one shared Q

Suppose the sole Qs coincide, with F opposite G in Q(F,X,G,Y).
They are noncontacts. Its endpoints X,Y each receive a T from both
fans. Those Ts differ because no T can contain both F,G. Hence
X,Y are ordinary fours. Each fan's three internals is ordinary,
distinct from X,Y. A cross-fan internal reuse would give a third
common contact of F,G. These are eight distinct ordinary fours,
contradicting O<=7. This credited counting obstruction is regenerated
with every internal subset alias retained.

## 5. Noncontacting fives with different sole Qs

Their six internals are distinct ordinary fours, and no endpoint can
reuse an internal of either fan. Thus O>=6, excluding b=0.

For b=1, O=6,a=4. The internals exhaust all ordinary fours.
The four endpoint slots must be the four one-T fours A,D,C,E,
each used once. Write the fans

    F:A,I0,I1,I2,D; G:C,J0,J1,J2,E.

All fifteen roles are distinct: F,G,U,V,zero-T B, these four endpoints
and the six internals. Write their sole Qs as(F,A,H,D),(G,C,K,E).
The Q corner rule and noncontact diagonals give

    H in{B,C,E}, K in{B,A,D}.                            (7)

For example H cannot be a three or an ordinary four, cannot be F,A,D
by simplicity, cannot be G because then its sole Q would coincide,
and cannot be an internal (also an ordinary four). All original
aliases are considered before applying(7).

At a one-T endpoint its fan T is the unique T. Its edge to its Q
opposite has Q on both sides: any T there would contain that opposite,
which is a strict noncontact of the five and is absent from the unique
fan T. Consequently AH,DH,CK,EK are deficient-four QQ contacts.

A one-T four has exactly two QQ edges; zero-T B has four. The total
QQ contact incidences **at deficient fours** is2a+4b=12. Six are used
by the two threes, each of degree three, by(2). Thus at most six such
incidences can lead to non-threes. Ordinary-four QQ incidences are
not counted in this budget.

If H=B or K=B, the four displayed edges are distinct and contribute
eight deficient-four incidences leading to non-threes, a contradiction.
Otherwise(7) gives exactly one reciprocal edge counted twice, leaving
three distinct edges and six incidences at the one-T fours. B has
four QQ contacts and at most two lead to the two actual threes;
its other two incidences lead to non-threes and are additional to
those six. Again eight exceed six. All nine choices in(7) fail.

For b=2, O=7,a=2, credit the earlier exclusion cited in Section1.
Here is a shorter alternative. Six distinct ordinary internals leave
only one ordinary P available for endpoints, besides the two one-T
fours A,D. A,D can each occur once across the noncontacting fans;
P can occur once in each. All four endpoint slots therefore force

    F:A,I0,I1,I2,P; G:D,J0,J1,J2,P.

P has exactly the four distinct contacts F,G,I2,J2. In F's Q
(F,P,H,A), PH must be a contact, so H is in that complete list.
H=F repeats a vertex, H=I2 makes the Q diagonal FH a contact,
and H=G forces GA although A is outside G's complete five-neighbor
fan. Only H=J2 remains; it is an ordinary four, which cannot be
opposite ordinary F. This retains every original H before using the
full contact list. Thus b=2 is again excluded. The b=3 case was
already excluded in Section2. All possible F/G relationships are closed.

## 6. Finite certificates and boundaries of checking

[check.py](check.py) reconstructs the credited core in Q(c), coefficient
domain characteristic zero, and proves numerator/denominator signs
by exact rational Bernstein coefficients on[1/2,3/5]. Its reduced
rational functions retain every pole obligation. It regenerates all
paired-fan cases, all original neighbor choices for v, and all opposite
aliases in the noncontacting cases. No samples, floating signs, solver,
network, coordinate data or private certificate enters this checker.

[audit.py](audit.py) imports no primary code. It uses full fan permutations,
edge bit masks and Hamiltonian link cycles. It independently regenerates
the finite contact completions and forced zero/T link sectors. It shares
the published continuous core classification as a stated input: it is
not an independent audit of the rational arithmetic or geometric bridges.
Entry hashes compare actual admitted completions, not just their totals.
Released constraints provide nonempty incidence controls, not packings.
Both checks are by the same author and are not independent researcher
review. The exact rational kernels are unchanged vendored files from
source21d7c373cfa2234494841a11642b53baf0380b7b. They credit adaptations
of **six-tammes-2**, source34d5a62d025ea9ade24e17c9ba848d297469063f,
[overlap reduction](../../../tammes15_bridge_overlap_reduction/PROOF.md),
lemma7488. The complete provenance is in[DEPENDENCIES.json](DEPENDENCIES.json).

The [three-five branch lemma8975](../three-five-branch/PROOF.md),
source71f757b0cd0eafe8bf76fb0fa725ab2c43db3198,
`bafkreiej5yrx23gq67dxru5hufgep5b5fsivj2foyk5jknpd37myf73taa`,
has a ten-row r=2 residue from committed catalogue8360 and a seven-row
r=2 residue from a later source-only catalogue. Importing each catalogue
**with all of its own hypotheses**, deletion of its f0=2 rows leaves
**seven committed-catalogue profiles** and **five source-only profiles**.
Three rows are removed from the committed basis, but the(2,2) row was
already published source mathematics; only the other two are newly
excluded here. The later basis already omitted(2,2). The imported
catalogue derivations are not regenerated; they do not supply a premise
of the main geometric theorem. Profiles are necessary counts, not
realizations, and these deletions do not enlarge the catalogues' scope.

The live [Cohn spherical-code table](https://cohn.mit.edu/spherical-codes/)
was refreshed2026-10-01 and retains the unstarred R3,N15 incumbent cosine
0.59260590292507377809642492233276. Its
[coordinate table](https://spherical-codes.org/data/3/15) remains890bytes,
SHA2561b77ee43d73613885d3fdcfb03dc8fad2e40302ff9c9ff639559cc9b326fb805.
The primary Musin--Tarasov seed solves N14. These checks do not establish
exhaustive absence of other literature. The written spherical, injective
original-point, actual-face and coverage bridges remain unformalized.
No review of a prior result is transferred to this theorem. Global
Tammes15 optimality and sharper unconditional numerical bounds remain open.
