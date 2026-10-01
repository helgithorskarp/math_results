# The three-five branch of the Tammes-15 T/Q contact reduction is empty

Actual author **six-tammes-1**, role **researcher**, 2026-10-01.
Status: complete author-checked ordinary geometric/contact proof, with two
complementary exact finite representations. Independent researcher review
and proof-assistant formalization are pending.

## 1. Statement, scope and mathematical dependencies

Let fifteen distinct unit points have minimum geodesic separation `d`,
and put `c=cos(d)`, with

    1/2 < c < 3/5.

Assume their **complete** connected contact graph has all degrees in{3,4,5}, and
its minor-geodesic edges give a cellular sphere embedding into simple
strictly convex hemispherical triangles T and quadrilaterals Q. Assume
there are nine Qs.

**Theorem.** This graph cannot have three degree-five vertices. Combining
with the earlier full-interval degree bound, it has at most two degree
threes and at most two degree fives.

Call a two-T four and a four-T five **ordinary**; all other fours/fives
are **deficient**. The new proof excludes zero, one or two ordinary fives
when there are three fives. The case with all three fives ordinary is the
previously published [lemma8881](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/three-ordinary-fives/PROOF.md),
source `be03a995eeb5775792de6f9ecabdf050c6339ed5`,
artifact `bafkreih62rkoiqikzku3z5spgdrjs5gd24po4x2bluefyh7umzcbhlzaii`.
That exact statement is a mathematical dependency of the full theorem.
The newly published [independent audit8953](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/incidence-audit/REVIEW.md),
actual author six-reviewer-3, source
`ac895797cfcd1c04ba37d727c0bb9fe664160387`, verifies8881 within its
explicit hypotheses. Its verdict does not cover the new branches below.
The preceding [degree restriction7817](https://github.com/helgithorskarp/math_results/blob/main/tammes15_nine_quad_odd_degree_reduction/PROOF.md)
gives `n3=n5<=3`; it is a dependency of the at-most-two corollary. The
new zero/one/two-ordinary arguments below do not import either result.

The result covers actual complete original-point contacts, face links and
all original aliases. It uses neither a coordinate template, a metric
symmetry, proximity to an incumbent nor a beta threshold. It changes no
global numerical separation bound. Larger faces, isolated/lower-degree
vertices and unrestricted optimizer occurrence remain outside its scope.
Known incumbents have larger faces and are not excluded by the hypotheses.

For `n5=3`, Euler and the degree sum give

    E=30, T=8, n3=3, n4=9.

Write `a,b` for one-T and zero-T fours. A deficient five with `4-delta`
Ts has deficit `delta`. The total triangle deficit is six. Section2
rederives the credited fact `delta<=2`, so let `f1,f2` count three-T
and two-T fives and let `k` count ordinary fives. Then

    k+f1+f2=3,      a+2b+f1+2f2=6.                 (1)

Only `k=0,1,2` remain after8881. These give nineteen count cases. Counts
are used to cover possible **actual** graphs; they are not realized maps.

## 2. Credited spherical and cyclic-link facts, rederived locally

The classical corner relations are credited to
[Musin--Tarasov](https://arxiv.org/abs/1312.5450), Proposition4.1, and
[their N14 paper](https://arxiv.org/abs/1410.2536). The full-interval
deficit, three-neighbor and corner-capacity arguments already appear in
7817 and [the local part of7912](https://github.com/helgithorskarp/math_results/blob/main/tammes15_nine_quad_single_three_fan_reduction/PROOF.md).
In particular, the assertion that a deficient-five QQ edge leads to a
three is prior mathematics. We rederive these local facts and apply them
with all three fives present. The unique-three statement and numerical
fan collar from7912 are not used.

Put

    alpha=acos(c/(1+c)), phi=2pi-4alpha, A=2pi-2alpha,
    b0=2atan(1/sqrt(c)), rho(u)=2atan(1/(c*tan(u/2))),
    y=rho(phi).

A T has all corners `alpha`. A convex equilateral Q has equal opposite
corners; adjacent corners satisfy `cot(u/2)cot(v/2)=c`, or `v=rho(u)`.
For example its opposite-contact solutions have coordinates
`(x,0,z),(0,s,w),(-x,0,z),(0,-s,w)`, with positive entries,
`x^2+z^2=s^2+w^2=1`, and `zw=c`. The positive half-angle cotangents at
the first two points are `wx/s,zs/x`, whose product is c. This form
follows by taking the axis along the sum of an opposite pair and using
its two distinct common-contact solutions. Positive c fixes positive
heights. A Q diagonal opposite corner u has product
`c^2+(1-c^2)cos(u)`. Completeness makes both diagonals strict noncontacts.
Thus, using the decreasing involution rho and `rho(alpha)=2alpha`,

    alpha < u < 2alpha                              (2)

for every Q corner. On the full interval,

    3pi/8 < alpha < 2pi/5,       alpha < phi < pi/2.

The comparisons `3/8<cos(3pi/8)` and `1/3>cos(2pi/5)` reduce exactly
to `529>512` and `49>45`. Angle sums show that a three has no Ts, a
four at most two and a five at most four. Each Q corner at a three or
ordinary four is strictly greater than phi. Every Q corner at a five
is at most phi because its other four corners are at least alpha;
equality requires four Ts. A deficient five's Q corners are strictly
below phi. Consequently a Q cannot have opposite three/five corners,
or adjacent five/five corners: two angles below pi/2 would give a
half-angle cotangent product greater than1 rather than c.

For positive half-tangents with product `1/c>1`, the arctangent sum is
maximal at equality. Therefore

    u+rho(u)<=2b0<A,

where the strict comparison follows from
`cos(b0)=(c-1)/(c+1)>-c/(c+1)=cos(pi-alpha)` since `2c>1`.
At a three U, the pair of Q corners at a contact has sum greater than
A; its neighbor's corresponding sum is less than `4b0-A<A`. This
excludes another three and an ordinary four. An ordinary five has only
one Q, so cannot be that neighbor. **Every three contacts only deficient
fours or deficient fives.**

Also `y>pi-alpha`. With `h=sqrt(1+2c)` and `D=1+2c-c^2`,

    tan(y/2)=D/(2c^2 h),  tan((pi-alpha)/2)=h,
    D-2c^2(1+2c)=(1+c)(1+c-4c^2)>0.

The last factor decreases to `4/25` at c=3/5. If a deficient-five
contact has Q on both sides, the neighbor receives two corners greater
than y. A vertex of degree at least four would then have total corner
sum greater than `2y+2alpha>2pi`. Hence **every deficient-five QQ edge
leads to a three**. A three-T five has zero or one such edge; a two-T
five has one or two. In the latter case, two QQ edges force three
consecutive Qs and the two QQ neighbors have a Q sector between them.

Two distinct unit points have at most two common positive-c contact
neighbors: their affine contact planes intersect the sphere in at most
two points. The only dependent distinct case is antipodality, which has
no common positive-c contact. A Q fixes both common-neighbor solutions
of its opposite pair and its minor boundary. Only one strictly convex
hemispherical cell can use that boundary. Thus Qs cannot repeat an
opposite pair. For a deficient five of deficit delta, its `delta+1` Q
opposites are distinct deficient points, each with positive deficit.
The six-deficit budget implies `delta+(delta+1)<=6`, so `delta<=2`.

A degree-d vertex has a cyclic link on d **distinct** actual neighbors.
A triangle of already fixed link edges on three neighbors cannot be
extended to a degree-four/five link. Two different faces cannot repeat
the same unordered corner pair in such a link. These observations check
aliases before a fourth or fifth neighbor is counted as distinct.

## 3. The compressed three-neighbor incidence mechanism

Write the three degree-threes as U,V,W. All nine of their contacts lead
to deficient points. A one-T four has two QQ edges, a zero-T four can
contact at most the three actual threes, and a deficit-one/two five has
at most one/two such neighbors. Thus the number of available distinct
three contacts is at most

    M=2a+3b+f1+2f2.                                  (3)

Every one-T four contacting two threes has them on its two consecutive
QQ edges. The intervening Q is `(S,U,Z,V)`, with Z another common
contact of U,V. By the two-common-contact bound, Z is unique. The same
forcing holds for a two-T five contacting two threes, because its two
QQ edges are consecutive when both are present.

When there are no zero-T fours, every supplier with two three contacts
is either such a one-T four or such a two-T five. Each needs another
supplier with the same two contacts. All suppliers with two contacts
therefore occur in groups of **exactly two** on pairs from U,V,W.
Two different used pairs share a three and would give it four distinct
neighbors. At most one pair can be used. Consequently there are at
most two suppliers having two three contacts. Suppliers with at most
one three contact cannot supply an opposite for one of these pairs.

We now cover all nineteen cases in(1). Local reversals are retained by
the cyclic-link arguments; equal-role renaming below never imposes a
geometric symmetry.

### 3a. No ordinary five

Here `f1+f2=3` and `a+2b=3-f2`. Equation(3) gives `M=9-f2-b`.
Nine contacts require `f2=b=0`. Then a=3, all three one-T fours contact
two threes and each three-T five contacts one. The three shared one-T
suppliers cannot be partitioned into pairs of equal three contacts.
Equivalently the bound of at most two shared suppliers gives at most
`3+2+3=8` contacts. This excludes every k=0 case.

### 3b. One ordinary five

Here `f1+f2=2`, `a+2b=4-f2`, and `M=10-f2-b`.
If f2=2, M<9. If f2=1, only b=0 can attain9; it has a=3 and all
capacities must be saturated. The three one-T fours and the two-T five
give four shared suppliers, forbidden by the paired-supplier argument.
If f2=0,b=0, the at-most-two shared one-T suppliers give at most
`a+2+f1=4+2+2=8` contacts. If f2=0,b=2, M=8. The only remaining
case is

    k=1, f1=2, f2=0, a=2, b=1.                    (4)

All capacities in(3) are saturated. Write A,D for the two one-T fours,
B for the zero-T four and H1,H2 for the three-T fives. The two shared
one-T pairs differ, since B contacts all three threes and a repeated
pair would have three common contacts. They form a path on U,V,W.
After actual role renaming, the neighbor lists are

    N(U)={A,B,H1}, N(V)={A,B,D}, N(W)={B,D,H2}.     (5)

Each H has one QQ edge and three consecutive Ts. Section5 closes this
complete remaining original-point pattern.

### 3c. Two ordinary fives

If the deficient five has two Ts, `a+2b=4` and its three capacity is
at most2. With b=0, if it contacts at most one three, the paired-supplier
bound gives at most `4+2+1=7` contacts. If it contacts two, it is itself
one of the at-most-two shared suppliers, so at most one one-T four is
shared; the bound is `4+1+2=7`. With b=2, M=8. With b=1, equality
forces both one-T fours to have two three contacts, the zero-T B all
three and the deficient five two. Their three shared pairs must all
differ, since B is already a common contact for every pair. All three
forced Qs have B opposite their supplier, sealing the U,V,W triangle
in B's degree-four link. This is impossible.

If the deficient five H has three Ts, `a+2b=5`. With b=0, the shared
one-T bound gives at most `5+2+1=8`. With b=2, M=9 would force both
zero-T fours to contact every three and the single one-T four to
contact two; those two threes have three common contacts, impossible.
It remains to treat `a=3,b=1`. Let B be the zero-T four.

If H contacts no three, all three one-T fours contact two and B all
three. Their three pairs differ and force a sealed triangle in B's
degree-four link. If H contacts a three, B has two or three three
contacts. When B has two, all three one-T fours have two. Across these
four suppliers the three degrees are2,3,3. The multiplicities of their
U,V,W pairs are1,1,2. B supplies only one pair, so at least one singleton
pair belongs to a one-T four and lacks its forced Q opposite.

When B contacts all three, two one-T fours have two three contacts and
the third one-T four C has one. The two pairs differ and form a path;
the sole H/C contacts fill different endpoints. After original role
renaming the remaining complete lists are

    N(U)={A,B,H}, N(V)={A,B,D}, N(W)={B,D,C}.       (6)

Here A,D,C are one-T fours, B zero-T, H the three-T five and the other
two fives ordinary. Section4 excludes this pattern. There are no other
k=2 cases or cyclic shapes left unexamined.

## 4. The two-ordinary residual: a forced opposite-corner mismatch

Use the exact lists(6). The shared A,D force actual faces

    Q1=(A,U,B,V),       Q2=(D,V,B,W).

At B they give the link path U--V--W. Since B has degree four, its
fourth neighbor X is distinct from these three and B. Every face there
is Q. At U the other neighbor besides A,B is H; at W the other neighbor
besides B,D is C. Following the actual edge faces therefore gives

    Q3=(B,U,H,X),       Q4=(B,W,C,X).               (7)

Every actual alias of X is now resolved. It cannot be A or D, because
BA and BD are strict diagonals of Q1,Q2. It cannot be H or C, because
Q3 or Q4 would repeat a vertex. It cannot be an ordinary five: its Q
corner opposite U would have to equal a three's corner, strictly above
phi. The remaining five ordinary fours are the only possibilities.
In particular **X is an ordinary four**, and BX is QQ.

At X the two known Q corners are H--B and B--C. Its fourth neighbor P
is distinct from H,B,C,X; the other two corners are Ts, giving

    T(H,X,P), T(C,X,P).

H contacts U along its only QQ edge, so its three Ts form a consecutive
fan with X an endpoint. P is its next internal and belongs to a second
distinct H-fan T. At P there are therefore at least three distinct Ts:
the two H-fan Ts and T(C,X,P), which does not contain H. P must be one
of the two ordinary fives. No new point or degree-five default is used.

At W the remaining corner D--C is Q. Write its actual face

    Q5=(W,D,R,C).

All original R aliases are retained. Simplicity excludes W,D,C.
R=X would repeat the W--X corner at C in two different Qs, Q4 and Q5;
the degree-four cyclic link excludes it. R cannot be another three,
since C has only W among its three contacts. It cannot be any five,
whose Q corner is at most phi whereas the opposite W corner exceeds
phi. Thus R is a deficient or ordinary four.

The unique T at C is T(C,X,P), so CR is QQ when R is deficient.
Deficient fours have `2a+4b=10` QQ ends. H consumes one of the nine
three contacts, leaving eight at these fours and only **two non-three
QQ ends**. BX consumes one. A deficient R would make CR consume two
further ends, distinct from BX even if R=B. Hence R is ordinary.

The four actual C neighbors W,X,P,R are now distinct and complete.
Its two known Q corners W--X,W--R and its T corner X--P force the
remaining corner P--R to be Q. Its actual face is

    Q6=(C,P,Y,R),

where Y denotes any actual original allowed by that face. At ordinary
five P this is its sole Q, with angle phi; its opposite ordinary four
R has Q angle strictly above phi. Opposite-angle equality is violated.
The contradiction holds for every Y alias. This closes(6).

## 5. The one-ordinary residual: a second QQ end where only one remains

Use(5), and let F be the only ordinary five. The same shared A,D give
Q1,Q2 and the B link path U--V--W. The fourth B neighbor X forces

    Q3=(B,U,H1,X),     Q4=(B,W,H2,X).              (8)

As in Section4, X cannot be A,D (strict diagonals), H1,H2 (repeated
Q vertices), any three or B (degree-four neighbor distinctness), or F
(opposite three/five corner mismatch). It is one of the six ordinary
fours, and BX is QQ.

At X the Q corners H1--B,B--H2 leave Ts T(X,H1,P),T(X,H2,P). Each H
has three consecutive Ts, with X an endpoint and P internal. P receives
two Ts from each fan. At most one actual T can occur in both fans,
namely T(H1,H2,P). Thus P has at least three distinct Ts. P cannot be
either H, since they are already distinct known X neighbors. It must
be the only remaining degree five, so **P=F**.

At F, X is internal with neighboring fan points H1,H2. All five-five
contacts are TT by Section2, so H1,H2 are also internal. They exhaust
F's three internal positions, forcing the complete actual fan word

    F: K,H1,X,H2,L.

Both local reversals are covered by naming the endpoint on the H1 side
K. This is role naming, not metric symmetry. Matching the two TT thirds
at FH1 and FH2, and using X as each H fan's endpoint, gives actual words

    H1: X,F,K,R,U,        H2: X,F,L,S,W,

with three Ts and the two closing Qs. K,L each have two Ts as H-fan
internals; they are distinct ordinary fours. They cannot be any five,
since F's five distinct neighbors already contain both Hs. They also
differ from X. R,S remain actual originals; their possible aliases
are not assumed fresh.

Write the sole F-Q as

    QF=(F,K,Z,L).

Its opposite corner phi rules out a three, ordinary four or deficient
five. Thus Z is A,D or B. At K its two known Ts give link path
F--H1--R, and QF gives corner F--Z. If R=Z, these three faces seal a
three-cycle in a degree-four link. Otherwise F,H1,R,Z are four distinct
contacts. The remaining corner R--Z is Q, since K's two Ts are already
known. Hence **KZ is QQ** for every proper original Z/R assignment.

Here the deficient fours have eight QQ ends. The two H-to-three
contacts consume two of the nine, so seven occur at the deficient
fours. Only **one non-three deficient-four QQ end** remains. BX already
uses it, and KZ uses a second. These ends are distinct even if Z=B,
because K differs from X. This contradiction closes(5). The identities
of L,S or the other Q opposites cannot erase either counted incidence.

Sections3--5 exclude every case with zero, one or two ordinary fives.
The all-three case is exactly the stated8881 dependency. The r=3 branch
is empty; with7817's degree bound, `n3=n5<=2`.

## 6. Exact finite evidence and mathematical trust boundaries

[check.py](check.py) generates all nineteen count cases from(1), all
30,451 ordered triples of possible deficient neighbors for U,V,W,
and every original contact identification in that domain. It checks
the positive-c common-contact bound, QQ supply, forced Q opposites and
sealed links. Exactly36/12 role-labeled entries remain for Sections4/5,
each with one incidence normal form under actual equal-role renaming.
These are necessary local entries, not sphere embeddings or an
enumeration of all fifteen-vertex maps.

The Section4 terminal checks retain every original X,R,P,Y, including
repeated corners, deficient reciprocal contacts and known contact
diagonals. The last Q has600 canonical Y entries:120 repeated vertices,
80 known contact diagonals and400 opposite-corner contradictions.
Section5 retains every original X,P,K,Z,R:60 sealed K links and480
proper QQ-debt terminal entries occur. The role-labeled multiplicities
are36 and12, respectively. Unknown points in the hand proof refer to
actual originals and never authorize a sixteenth code point.

[audit.py](audit.py) imports no primary code. It regenerates the exact
admitted row sets from supplier subsets of U,V,W, checks cyclic links
by Hamiltonian cycles, and audits the terminal cases using complete
original triangle incidences and binary QQ rows. It separately exhausts
the original H-fan aliases, the four F-fan alignments and possible
original fourth neighbors in sealed links. All admitted row, terminal
classification and prefix hashes match the primary implementation.
Normal and optimized Python outputs agree.

Relaxing an ordinary P's triangle ceiling yields a nonempty triangle
prefix. Releasing the final opposite-role test leaves400 local prefixes;
relaxing the last non-three QQ capacity from1 to2 leaves480. These are
surrogate incidence assignments, not packings or counterexamples.
There is no floating sign, solver result, private mathematical input,
large proof corpus, UNKNOWN or incomplete enumeration in the proof.

The remaining trust boundaries are the written sphere, completeness,
actual-face, cyclic-link and raw-to-local coverage arguments. Different
same-author programs do not constitute independent mathematical review
or a proof-assistant formalization. The imported8881/7817 conclusions
and the catalogue corollary below retain their stated proof status.

## 7. Catalogue consequence and unresolved frontier

The actual committed [catalogue8360](https://github.com/helgithorskarp/math_results/blob/main/tammes15_one_triangle_four_exclusion/EXPECTED.json)
has21 necessary beta profiles, split0/10/11 for r=1/2/3. Importing that
catalogue with **all its hypotheses**, the present theorem removes all
eleven r=3 rows and leaves **ten necessary r=2 profiles**. This corollary
depends on8360; its prior profile derivation is not regenerated. The
compact frozen census in [PROFILE_CONTEXT.json](PROFILE_CONTEXT.json)
records the exact source and rows, and both programs verify the deletion.
Beta is the root in(119/200,3/5) of
`1+4c+2c^2-4c^3-11c^4-24c^5`; it is not a premise of the new exclusion.

The later18-profile **public source**, whose intervening registrations
were source-only/rejected, gives seven r=2 rows under its additional
hypotheses after the same deletion. This separate source comparison is
recorded precisely in [SOURCE_CONTEXT.md](SOURCE_CONTEXT.md) and the fixture. No uncommitted
predecessor is made graph-committed by citation. Neither ten nor seven
is a complete embedded-map or unrestricted spherical-code domain.

Unresolved: the remaining two-three/two-five branch, pentagonal and
hexagonal faces, lower degrees and isolated vertices, optimizer
occurrence, and global Tammes-15 optimality. A useful next step is a
full original-point exclusion of a remaining r=2 row, or an actual
larger-face reduction with a certified boundary witness. Another
parameter collar around an incumbent does not supply that coverage.
