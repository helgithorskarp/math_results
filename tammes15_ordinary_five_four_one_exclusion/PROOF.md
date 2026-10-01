# Tammes-15: exclude the ordinary-five profile (0,4,1)

Author: **six-tammes-1**, role: **researcher**, 2026-10-01.
Status: complete author-checked conditional geometric reduction and exact
original-face exclusion, with a separate exhaustive algorithm. Written
geometric bridges are unformalized; independent mathematical review is
pending. Shared team signatures do not establish separate authorship.

## Statement and scope

Let fifteen distinct points on the unit sphere in R^3 have minimum geodesic
separation d and c=cos(d), with **1/2<c<3/5**. Assume their **complete**
contact graph joins exactly the pairs with inner product c, is connected,
and has degrees 3..5. Its minor geodesic edges form a cellular sphere
embedding with simple strictly convex triangular and quadrilateral faces,
each contained in an open hemisphere. Assume nine quadrilaterals Q and
exactly one degree-three U. Euler gives eight triangles T, one degree-five
F and thirteen fours. Let t(v) count incident Ts, and define

    delta=4-t(F), a=#{one-T fours}, b=#{zero-T fours}.

**Theorem. The profile (delta,a,b)=(0,4,1) is impossible.**
The reduction retains every possible identification of the original face
positions, including later names for already present vertices.

With the preceding [three-profile theorem](../tammes15_ordinary_five_two_two_exclusion/PROOF.md),
source 639f1d7c63d6c02f9b40ce56b9efc0ad6f5edc6d, committed h8132,
bafkreifovwzx75mz2fcwrzkfq2sgxsp2l5ni7jypcyi5jx5gf6eykwh7qu,
this leaves **two necessary single-three count profiles** on the full open
interval:

| delta | a | b |
|---:|---:|---:|
| 0 | 6 | 0 |
| 1 | 5 | 0 |

On 1/2<c<beta, where beta is the unique root in (119/200,3/5) of

    1+4c+2c^2-4c^3-11c^4-24c^5,

the [older odd-degree cover](../tammes15_nine_quad_odd_degree_reduction/PROOF.md),
source d6547391ae745a70087f067568047c8dbba0e099, h7817,
bafkreic6shrttfdlf7vbae5wye7eytruyxeeb7j6422ubytjcwlaadlkfa,
therefore has **25 necessary count profiles, 2/12/11 for r=n3=n5=1/2/3**.
The r=2,3 rows are imported unchanged. These counts are not complete
contact maps, realized packings or a census of global optimizers.
Unrestricted Tammes-15 numerical bounds and optimality are unchanged.

## 1. Geometric inputs and necessary original-face constraints

The full-interval angle and endpoint facts are in the
[single-three fan reduction](../tammes15_nine_quad_single_three_fan_reduction/PROOF.md),
source 276ec8b0508c7960aa73517f3b7e6e0ef03ca3cf, h7912,
bafkreicjxhbyqcxdeplfvby6k2bysmhhk7fbksapoenneqsigtfos2dulu.
Its metric collar certificate is not used here. Put

    alpha=acos(c/(1+c)), phi=2pi-4alpha, A=2pi-2alpha,
    rho(u)=2atan(1/(c tan(u/2))).

A T corner is alpha. Opposite Q corners are equal and adjacent ones are
related by rho. Completeness, both noncontact Q diagonals and convexity
give alpha<u<2alpha for every Q corner. These classical identities are
in [Musin--Tarasov, Proposition 3.2](https://arxiv.org/abs/1410.2536) and the
[earlier geometric audit](../tammes_15_triangle_quad_exclusion_review1/README.md),
source f026ccec6854eb913e5c156f4ff0cf08ed5cb4a9, h7182,
bafkreiflxdrel4fv4opchhucsisp7ylw2lsfgtrv4q7tya3o5vjh4ld53a.
That earlier audit does not review the present result.

Here pi/3<alpha<2pi/5. Angle sums force t(U)=0, t<=2 at a four,
and t<=4 at a five. A two-T four is called ordinary. Every Q corner
at a three or ordinary four exceeds phi: the other two corners at a
three are less than 2alpha; an ordinary four's two Q corners sum to A
and each is less than 2alpha. An ordinary five's sole Q corner is phi,
so its opposite is a deficient four rather than U or an ordinary four.

U contacts only deficient fours in this delta-zero row. At a three the
two adjacent Q corners u,v satisfy u+v>A. The established inequality
u+rho(u)<=2b0<A, b0=2atan(1/sqrt(c)), gives

    rho(u)+rho(v) < 4b0-A < A.

An ordinary four needs its two received Q corners to sum to A, a
contradiction. An ordinary five has only one Q, whereas a U edge needs
Qs on both sides. The angle inequality and capacity facts are also
recorded in the [ordinary-five corner proof](../tammes15_eight_quad_reduction/FIVE_CORNER_CAPACITY.md),
source 9f43d6fdac0c7b0e0333c527c739cb0c24c68afb, h7444,
bafkreiasa2n2mywlaokeron7wkpsj4z2ows4asfkm5fbnf6gphzbgmtvba.
Thus U's three distinct contacts are among the **five** deficient fours.

Two points have at most two common contact neighbors, by intersecting
their affine contact planes with the sphere. Antipodal points have none
since c>0. A contact K4 is impossible: its Gram eigenvalues are
1-c,1-c,1-c,1+3c, of rank four. A complete contact cannot be a Q diagonal.

At every vertex the actual incident faces have one simple cyclic link
of length its degree. A proper closed sublink, conflicting successor or
predecessor, repeated oriented boundary edge or excess number of contacts
is impossible. Descriptions of the same actual face coalesce and are
counted once. Opposite orientations cannot describe the same convex
hemispherical cell: its complementary side is not another such cell.
All displayed face words follow one sphere orientation.

## 2. Four-T fan, adjacent strip and endpoint faces

F is ordinary with four consecutive Ts. The eight anchors

    F,U,X,R,S,T,Z,D

are distinct, with T also the name of an internal fan vertex. F's entire
cyclic contact list is X,R,S,T,Z and its actual faces are

    (F,X,R),(F,R,S),(F,S,T),(F,T,Z),(F,Z,D,X).

The last face is a Q. D is its small-corner deficient-four opposite,
a noncontact of F, and hence outside F and all five F contacts. D is
not U by the opposite angle. U is not a contact of ordinary F. This
proves anchor distinctness without assigning independent coordinates.

Internal R,S,T have two Ts and are ordinary fours. Their fourth contacts
L,K,M and unknown Q opposites P,Q force the actual quadrilaterals

    (R,L,K,S),(R,X,P,L),(S,K,M,T),(T,M,Q,Z).           (1)

These are closures of the degree-four original links. All later names
may reuse earlier actual vertices until a necessary condition rejects
the alias. In particular the initial alternatives L=T/Z and M=X/R
are retained, rather than assumed outside the fan.

K is not F,R,S,T, since it is S's fourth contact. K=X or K=Z would
give contact K4 F,X,R,S or F,S,T,Z. Therefore F-K is a noncontact.
K is not U (S is ordinary), or D (F,D would share X,Z,S). Similarly
L is a four other than U,D,F,R,X,S, and M a four other than
U,D,F,S,T,Z. L=D or M=D gives F,D three common contacts. Further,
L=T or M=R gives K4 F,R,S,T; L=Z gives five Z contacts F,T,D,R,K;
M=X gives five X contacts F,R,D,K,T. Thus the three fourth contacts
are outside the eight anchors. They are distinct: L=K or K=M is
nonsimple, and L=M closes K's proper two-neighbor link L-S-L.
The checker still permits these names initially and checks their actual
consequences; it does not hard-code an outside-strip rule.

If a strip point is ordinary, its two known consecutive Q corners in
(1) leave two Ts, with a fourth contact denoted by its own H position:

    L ordinary: (L,HL,K),(L,P,HL);
    K ordinary: (K,HK,M),(K,L,HK);
    M ordinary: (M,K,HM),(M,HM,Q).                     (2)

HL,HK,HM are separate positions and keep all original aliases. When two
ordinary points are adjacent, the actual triangle on the unused side
of their shared edge forces the matching H positions. The three-T strip
obstruction of h8132 then applies: three distinct Ts meet H!=F because
F-K is absent. A mixed ordinary/zero pair forces a T at zero. Also,
ordinary L,M with one-T K force two distinct Ts at K; their only possible
coalescence T(L,K,M) closes its proper three-neighbor link L-S-M-L.
These facts help explain the finite cover, but are not imposed as role
assumptions at unidentified positions.

At X the known T and two Q corners form the link path D-F-R-P. Its
missing face is T(X,D,P) if ordinary, or Q(X,D,AX,P) if one-T.
Similarly Z's missing face is T(Z,Q,D) or Q(Z,Q,AZ,D). In particular
an ordinary endpoint forces a T at D. AX and AZ remain separate
positions whose possible aliases are checked later.

## 3. Complete role coverage

D is zero-T or one-T. If zero, neither endpoint can be ordinary,
so X,Z are one-T. The two other one-T fours E,G lie outside the
eight anchors; there is no other zero.

If D is one-T, both endpoints cannot be ordinary: their two Ts at D
are distinct, since coalescence contacts Q diagonal X-Z. At least
one endpoint is one-T. **Both one-T endpoints are now allowed**, since
there are four one-T fours, rather than the preceding row's two.
This gives the four labelled roles:

| Role | One-T fours | Zero-T four | Outside exceptional originals |
|---|---|---|---|
| D_zero | X,Z,E,G | D | E,G |
| D_one_X_one | D,X,E,G | A0 | E,G,A0 |
| D_one_Z_one | D,Z,E,G | A0 | E,G,A0 |
| D_one_both_one | D,X,Z,E | A0 | E,A0 |

Every exceptional original is distinct from the anchors and the others
by this classification, and is assigned before pruning unknown aliases.
Every remaining four therefore has exact t=2; F has exact and maximum
**t=4 throughout**. Each role includes all **ten three-of-five U contact
sets**, added as actual edges without guessing their surrounding faces.
Both endpoint reflections are explicit labelled roles, without a symmetry
quotient. E,G need no canonical order; either labelling is covered.

After the initial originals, add L,K,M,P,Q and AX/AZ when needed. Every
base case has seventeen positions. Each unknown may equal any earlier
class or one new class in a complete restricted-growth enumeration.
No fifteen-class cutoff is used. The ordinary-star completion can have
twenty positions, and final closures twenty-one. The actual fifteen-point
configuration would be a subset of this relaxed cover.

## 4. Two local closure rules

**New fourth neighbor at a one-T four.** Suppose an exact one-T four
has exactly two known Q corners, making a three-neighbor link path.
Its two remaining faces use its fourth contact. One is a T and one a Q,
so that fourth contact belongs to a T. Consequently U cannot be the
fourth contact, since t(U)=0. If an actual U edge is already present,
U must be among the three neighbors shown by the Q path. This is not
a prohibition on every U/one-T-four edge: the known-Q neighbor control
is accepted. This necessary rule rejects sixteen of the thirty-six
ordinary-star patches.

**Last face after three corners.** At an exact-role four with three known
actual corners, a passing prefix has a simple four-neighbor link path.
Let its directed endpoints be a,b. Its fourth face must close the path
b to a. If one T remains it is T(v,a,b); if no T remains it is
Q(v,a,J,b), where J is a new face position retaining every original alias.
Any coalescence, contact diagonal, improper link or incorrect role is
checked on the actual substituted words. The production algorithm takes
the lowest labelled eligible vertex; choosing a different eligible vertex
would impose another necessary condition, not change the coverage logic.

This closure never assumes an ordinary role at an unknown point. Roles
are read from the original exceptional identities already assigned, or
from the proven exact-two default. The number of remaining T corners is
computed only after all names in the current patch are assigned. A known
closed star is not forced again. A depth cap raises INCOMPLETE rather
than a mathematical verdict; all completed branches stay below that cap.

## 5. Complete finite cover and positive controls

[check.py](check.py) exhausts all original identities, coalesces repeated
actual faces, and applies only the necessary conditions of Sections 1--4.
The completed cover is:

| Stage | Covers | RGS nodes | Partial survivors |
|---|---:|---:|---:|
| Four roles, ten U sets each | 40 | 58,618 | 708 |
| Classified ordinary L/K/M stars | 708 | 13,841 | 36 |
| Forced last faces | 42 | 558 | 0 terminal patches |
| Total | 790 | 73,017 | 0 |

The thirty-six patches are only in the D_one_X_one and D_one_Z_one
roles. Sixteen reject by the new-U fourth-neighbor rule. The other
branches close by forty-two last-face covers. Counts, links and contacts
in a partial patch are lower bounds; later names do not merge distinct
classes already assigned. An exceeded capacity or forbidden existing
edge cannot be repaired by a later face. This justifies pruning before
all later positions are assigned.

A positive fourteen-class patch has case D_one_X_one with U contacts
X,E,A0. In order F,U,X,R,S,T,Z,D,E,G,A0,L,K,M,P,Q,AX,HM its partition is

    0,1,2,3,4,5,6,7,8,9,10,8,9,11,1,12,10,13.

Its first forced Q is (D,Q,J18,A0), with J18=HM. Its next forced Q
is (G,E,J19,HM), with J19=A0. Both pass all necessary checks. Only
then is the mandatory T(E,U,A0) forced and rejected. This prevents the
uncompleted ordinary-star patch from being mistaken for an exclusion.
These are combinatorial partial patches, not metric witnesses.

Other controls accept the ordinary F four-T star and reject a wrong
three-T role. A one-T-four/U edge outside its two-Q link is rejected,
while a U already in that link is accepted. Both algorithms reproduce
these positives and negatives. A known eleven-class quotient passes local
bitset checks and fails the signed dual, checking orientability separately.

## 6. Separate audit, completeness and temporary trace

[audit.py](audit.py) imports no production schema, predicate, enumerator
or forcing function. It separately writes the four roles and globally
reversed actual face words, generates U contacts by their omitted pair,
and uses unoriented cell keys, undirected bitset links and a signed dual.
Source-description orientation parity is retained when actual cells
coalesce. The production K4 and global face-count shortcuts are omitted.
Missing fourth faces are independently sewn to the endpoints of an
unoriented path using the actual directed source boundary arcs.

The first full raw-label audit in two-name blocks hit its 45-second limit
and gave **no mathematical verdict**. The replacement normalizes after
each assigned name and prunes an impossible prefix earlier. This changes
execution, not the mathematical domain: every alias or new class occurs
among the raw labels, normalization preserves all early exceptional
identities, and the monotone necessary conditions cannot reject a prefix
that later becomes possible. Nontrivial D_zero and D_one base cases are
also rechecked with both one- and two-name blocks, with entrywise agreement
of their final lists and all compared boundaries. Limits are unchanged.

The complete separate audit finishes with **83,219 raw assignments**, and
**all 2,346 initial, every-depth, suffix and final partition boundaries**
agree entrywise. All forty base cases, 708 ordinary-star covers, thirty-six
closure roots, sixteen U obstructions and forty-two last-face covers are
accounted for. Matching aggregate counts alone is not used as evidence.

[EXPECTED.json](EXPECTED.json) records the compact production summary and
SHA256 of the full deterministic partition trace:

    41e88f1d0e02f212260ac6d3494e70eb972318c985967f44c08f74a909007e40

The 662,761-byte temporary trace is deliberately not published. It is
regenerated from the source with --export-partitions, verified against
that hash, and then compared entrywise by the separate audit. The audit
reconstructs and exhausts each case; it does not trust a supplied list as
an exhaustive domain. No external private data or downloaded certificate
is required. [AUDIT_EXPECTED.json](AUDIT_EXPECTED.json) is the compact
separate summary, including the raw-block reference controls.

Both algorithms are by this author. Their different representations and
enumerations supply an algorithmic check, not independent peer review.
Geometric hypotheses, original-star forcing, exhaustive role coverage
and necessity of pruning remain written, unformalized proof bridges.
Normal and Python optimized modes agree. [README.md](README.md) gives
commands, timings, unchanged resource caps and compact source hashes.

## 7. Current literature and complementary scope

The [Cohn table](https://cohn.mit.edu/spherical-codes/) retains unstarred
N=15 in dimension three, cosine 0.59260590292507377809642492233276 and
polynomial 13c^5-c^4+6c^3+2c^2-3c-1. The current
[coordinate table](https://spherical-codes.org/data/3/15) is unchanged,
890 bytes, SHA256 1b77ee43d73613885d3fdcfb03dc8fad2e40302ff9c9ff639559cc9b326fb805.
The table is status context rather than an optimality proof.
[Musin--Tarasov](https://arxiv.org/abs/1410.2536) settles N=14.
[Lian--Mo--Xia](https://arxiv.org/abs/2411.16038) gives general LP sufficient
conditions and examples without a N=15 optimality theorem. Classical
corner identities, Gram rank, contact-plane intersection, simple links
and partition enumeration are credited standard tools. No historical
priority claim is made for this conditional row exclusion.

Complementary **six-tammes-2**, researcher, results include the
[prescribed decagon/ear-bridge exclusion](../tammes15_decagon_first_chart_exclusion/PROOF.md),
source 14bf22089a055e42d6ceec414fd8b4e47a83faf6, h7891,
bafkreigwlffu4ljboeonipd37h5tuf3kldc6qv3xfbd4zvphqonkr3ubv4,
[eight-core upper-strip theorem](../tammes15_octagon_model2_extension_exclusion/PROOF.md),
source 682fd64b45a8e7b17db38af0a0cdaa5cc9ccc22f, h8044,
bafkreicw4atwjndv5wubcogm626otpzpadvkllayawensn2b3utzcqff5e,
and [lower-strip/full-range corollary](../tammes15_octagon_model2_lower_strip_exclusion/PROOF.md),
source 8520a118cf3a00d8ad08e52bac21f09f2ec30503, h8088,
bafkreicbxsigz4halt74embgjfangq5upradnyq5ujbso23fv2v4aqs3bm.
The latter excludes its prescribed thirteen-contact eight-core in every
fifteen-point packing with c<=593/1000 using its two closed-strip
certificates and known N14 optimum. Its published proof was read;
its checker is not rerun here and no occurrence premise or review
is transferred to this T/Q branch. These are citations, not dependencies.

The next ordinary-five frontier is (0,6,0), whose Q opposite and every
other deficient four are one-T. The deficient-five row (1,5,0), r=2,3,
larger faces and unrestricted numerical upper bounds remain open.
