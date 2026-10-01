# Closing the two-five row with two one-triangle fours

Actual author: **six-tammes-1**, role **researcher**, 2026-10-01.
Complete conditional hand proof with small exact local checks and a different
same-author representation. The written geometric and face/contact bridges
remain unformalized; independent mathematical review is pending.

## Statement

Let fifteen distinct unit points have minimum geodesic separation d and
c=cos(d). Assume their **complete** connected contact graph has degrees
3,4,5 and gives a cellular minor-geodesic sphere decomposition into simple
strictly convex hemispherical triangles T and quadrilaterals Q, with nine Qs.
On the **full open interval** `1/2<c<3/5`, the row

    n3=n5=2,n4=11,a=2,b=1,(f0,f1,f2)=(0,2,0)

is impossible. Original roles, always kept distinct, are

    U,V: zero-T threes; F,G: three-T fives;
    A,D: one-T fours; B: a zero-T four;
    eight remaining originals: ordinary two-T fours.

Here a,b count one-T and zero-T fours and f_j counts fives with4-j Ts.
All eight full-interval neighbor-family types are covered; no beta/H
assumption or full contact-map enumeration is used for this row.

The preceding [one-one-T-four exclusion](../tammes15_one_triangle_four_exclusion/PROOF.md),
source `8e69194e595ae7411d3624537473870f67ff79c8`, graph h8360
`bafkreicjsndjhrckpkt2flkpfa7pawhzyb6k4k6xpecudodmdmfvqb2aue`,
provides21 necessary beta profiles. Removing this exact row gives
**20 profiles,0/9/11 at r=n3=n5=1/2/3**. Beta is the unique root in
`(119/200,3/5)` of `1+4c+2c^2-4c^3-11c^4-24c^5`. This count corollary
keeps all prior catalogue hypotheses and excludes no additional row.
Global numerical Tammes-15 bounds, optimality, unrestricted optimizer
occurrence and larger-face coverage remain open.

## 1. Credited local facts and two star consequences

The [odd-degree reduction](../tammes15_nine_quad_odd_degree_reduction/PROOF.md),
source `d6547391ae745a70087f067568047c8dbba0e099`, graph h7817
`bafkreic6shrttfdlf7vbae5wye7eytruyxeeb7j6422ubytjcwlaadlkfa`,
proves throughout this full interval that threes have no Ts, fours have
at most two, fives at most four, and a three contacts only deficient
fours or fives. Two distinct unit points have at most two common contact
neighbors: their two contact planes meet in a line, intersecting the sphere
in at most two points; antipodal points have no such neighbor for c>0.

Every pair of neighbors of a zero-T three is noncontact, since they are
opposite in its simple Q face. Completeness forbids a contact diagonal
inside a convex Q. This is the credited local rule in the
[single-three branch proof](../tammes15_single_three_branch_exclusion/PROOF.md),
source `ea0e70fa3ae7c287f5f54b59b9a06cdc878c92ca`, graph h8307
`bafkreidhqy3zbi7rlzcuy44ve2zexokku44vktrsdyjw3p4o6pv6e7rj2a`.
It does not require a unique three.

Put `alpha=acos(c/(1+c)),phi=2*pi-4*alpha` and
`rho(u)=2*atan(1/(c*tan(u/2)))`. Opposite Q corners agree; adjacent
corners are related by the decreasing involution rho. Completeness gives
`alpha<u<2alpha`. These classical identities are credited to
[Musin--Tarasov, Proposition3.2](https://arxiv.org/abs/1410.2536) and the
[prior geometric audit](../tammes_15_triangle_quad_exclusion_review1/README.md),
source `f026ccec6854eb913e5c156f4ff0cf08ed5cb4a9`, graph h7182
`bafkreiflxdrel4fv4opchhucsisp7ylw2lsfgtrv4q7tya3o5vjh4ld53a`.
That audit does not review the present result.

A Q corner at any five is at most phi; the other four corners are at
least alpha. The established full-interval comparison is

    y=rho(phi)>pi-alpha>phi.

The numerator for the first inequality is
`(1+c)(1+c-4c^2)`. Its quadratic factor has positive Bernstein entries
`1/2,7/20,4/25` on `[1/2,3/5]`; the second is `3alpha>pi`.
Thus adjacent fives in a Q are impossible. An ordinary two-T four
can receive at most one such large corner, since two would sum to
more than `2pi-2alpha`, its total Q-corner budget. This is the credited
large-corner capacity behind h7817 and the
[ordinary-five corner proof](../tammes15_eight_quad_reduction/FIVE_CORNER_CAPACITY.md),
source `9f43d6fdac0c7b0e0333c527c739cb0c24c68afb`, graph h7444
`bafkreiasa2n2mywlaokeron7wkpsj4z2ows4asfkm5fbnf6gphzbgmtvba`.
In particular **a Q-Q contact neighbor of a five cannot be an ordinary
two-T four**, because both adjacent Q corners there exceed pi-alpha.
This uses the full local interval, not the beta comparison with2pi/3.

We repeatedly use the ordinary endpoint rule from the
[prior fan reduction](../tammes15_nine_quad_single_three_fan_reduction/PROOF.md),
source `276ec8b0508c7960aa73517f3b7e6e0ef03ca3cf`, graph h7912
`bafkreicjxhbyqcxdeplfvby6k2bysmhhk7fbksapoenneqsigtfos2dulu`.
In its center-free form, let ordinary E have T(H,E,R) and adjoining
Q(H,E,C,W). Its fourth neighbor J is distinct from H,R,C. The remaining
possible T is T(E,R,J) or T(E,C,J). Assume R's T quota is already full
and its other known Ts do not contain E. The first would be a new T
at R, so T(E,C,J) is forced. This proof uses the cyclic four-neighbor
link, full quota and original-triangle distinctness; it applies also
when R is a one-T four with its unique T already known. It forbids an
ordinary endpoint/internal pair on a side with zero-T opposite C.
This is also the mechanism of the
[disjoint fan-pair lemma](../tammes15_two_deficient_fives_fan_exclusion/PROOF.md),
source `4b8ae42b4c87cd223aecf9261319a1091a06bc4b`, graph h8328
`bafkreiflgwet2ctcbjwhldykxhpugeycu6arhs4fxprtoquhkui44cqeae`.
No old unique-five degree-four default is imported.

A full quota alone is insufficient if its other T could already be
T(E,R,J). This precise distinctness condition qualifies the schematic
endpoint wording in h8360; its actual fan/alias applications satisfy it.
Here an ordinary internal fan point's other T excludes the endpoint;
for propagated points the forced quotas below exclude the coinciding
aliases. No conclusion uses the bare schematic wording without this check.

Two elementary star facts will be useful. At a one-T four, the three
Qs form a consecutive chain and its two Q-Q contact edges are adjacent
in the neighbor cycle. If it contacts both U,V, its star therefore
contains a Q(U,A,V,W); W is another common neighbor of U,V. Consequently
the two threes must have at least two common contacts. At a three-T five
contacting a three, its two Qs are consecutive, so its three Ts form
a consecutive fan. Such a five contacts at most one three.

Known distinct face corners give edges in the cyclic neighbor link.
A complete three-cycle of known corners seals a degree-three link and
cannot be part of a degree-four link. Each original contact edge has
exactly two incident faces; three distinct claimed faces on it are
impossible. These statements follow from the stipulated simple cellular
embedding and are not conclusions about an arbitrary abstract graph.

## 2. Complete neighbor-family cover on the full interval

N(U),N(V) are distinct triples in `{A,B,D,F,G}`. A repeated triple
would give three common contacts to U,V. Each triple pair uses either
five at most once, by the three-T five capacity. There are36 ordered
pairs. Relabeling the equal-role originals U/V,A/D,F/G gives eight types:

    C1 ABD / ABF; C2 ABD / ADF;
    C3 ABD / AFG; C4 ABD / BFG;
    C5 ABF / ABG; C6 ABF / ADG;
    C7 ABF / BDG; C8 ADF / ADG.

This uses role renaming only, with no spatial symmetry assumption.
On beta, h7817 forbids two fives in one three's triple, leaving30
ordered pairs and six types (all except C3,C4). We nevertheless close
C3,C4 directly and do not extend that beta theorem outside its scope.

C3 and C6 both have U,V sharing only one contact, the one-T A.
The one-T star consequence in Section1 requires another common contact.
Both are impossible throughout the full interval.

In any F/U or F/V fan label the incident Ts as

    T(F,X,R),T(F,R,S),T(F,S,Z).

All four fan neighbors are distinct actual contacts of F. An internal
R or S already has two Ts, so cannot be A,D or any zero-T point.
An endpoint has a T. Only the other five can be a nonordinary internal
point, and it cannot be an endpoint because of adjacent fives in a Q.

## 3. C4: the zero opposite has no possible exception

Here N(U)=ABD,N(V)=BFG. The Q at V between F,G is Q(V,F,W,G), so F,G
are noncontacts and have common contacts V,W. W is a shared fan endpoint
of the two fives. It has a T at each, two distinct Ts because F,G do
not contact. Thus W is ordinary, not a one-T or zero-T point.

F's other fan endpoint Z is on the zero-B side, with Q(V,B,Z,F).
Its internal next point S is ordinary: A,D cannot be internal and
G is a noncontact of F. If Z were A or D, the Q boundary would make
it contact B, forbidden by N(U)=ABD. The other five cannot be an
endpoint. Therefore Z is ordinary too, and its endpoint rule forces
a T at zero-T B. This closes C4 without beta.

## 4. C2: both one-T sides force the other five

Now N(U)=ABD,N(V)=ADF, and the fan faces are

    T(F,X,R),T(F,R,S),T(F,S,Z),
    Q(V,F,X,A),Q(V,D,Z,F).

A,D are opposite and noncontact of F, so both are outside the fan.
G is internal R,S or outside; endpoints are forbidden adjacent fives.

For either ordinary endpoint E with an ordinary internal next point,
the rule forces T(H,E,J), where H=A or D is the one-T opposite.
If J is ordinary, H has exact contacts U,V,E,J, and E has its four
actual contacts F,its internal next point,H,J. U's Q between H,B
has opposite W contacting H,B. V cannot contact B, and E's complete
list cannot contain the zero-T B, so W=J. At J this Q and T force
another T at B, because ordinary E has its two Ts. Contradiction.
J cannot be the other one-T four because A,D are noncontacts. Thus
every such ordinary side requires J=G. Original J aliases at a fan
point are included by the complete-list argument; an already full
quota or a fifth contact is an earlier contradiction.

If G is outside, both sides require it. A,D then have three distinct
common contacts U,V,G, impossible. If G=R, the D-side forces J=G.
Exchanging A/D and reversing the fan names covers G=S.
G's five distinct contacts are F,X,S,Z,D, with three known Ts
GFX,GFS,GZD, exactly its quota. Up to reversal its two cycles are

    X F S Z D; X F S D Z.

In the first, the S/Z sector must be Q but has the contact diagonal
S-Z from T(F,S,Z). In the second Q(G,S,W,D), D's exact contacts
U,V,Z,G give W in U,V,Z. Ordinary S cannot contact either three,
so W=Z; G-Z is now a contact diagonal from T(G,Z,D). Both are forbidden.
All four oriented three-T stars are retained. This closes C2.

## 5. C1: a triangle chain leaves no Q-Q neighbor at G

Here N(U)=ABD,N(V)=ABF. The one-T A contacts both threes, so the shared
Q is Q(U,A,V,B). The F fan is

    T(F,X,R),T(F,R,S),T(F,S,Z),
    Q(V,F,X,B),Q(V,A,Z,F).

D cannot be internal (one T), at X (D-B noncontact from U), or at Z
(D-A noncontact from U), so it is outside. The zero-B side requires
G at X or R; X is forbidden adjacent fives in a Q. Thus R=G while
X,S,Z are ordinary. The A side forces T(A,Z,J).

J is ordinary or G: all zero-T points are ineligible, F is a noncontact
of A, and D is a noncontact of A. If J=G, its exact contacts F,X,S,Z,A
and known Ts GFX,GFS,GZA give the same four three-T star contradictions
as Section4, with A in place of D. The argument uses no G/three contact.

Suppose J is ordinary. Its alias J=X already gives ordinary X the five
distinct contacts F,G,B,Z,A. For every other actual ordinary J,

    N(A)={U,V,Z,J},N(Z)={F,S,A,J}.

U's Q between A,D has opposite W contacting A,D. Neither V (complete
N(V)=ABF) nor Z (its full four-neighbor list) can contact D, so W=J.
Thus Q(U,A,J,D) is actual. Ordinary Z is full with T(F,S,Z),T(A,Z,J),
and the endpoint rule at J forces T(J,D,K). D's unique T is now full;
J has its two Ts. K has a T and is ordinary or G. A is already full,
F is a noncontact of D, and the zero-T originals are ineligible.

At X, its fourth neighbor N is distinct from F,G,B. Given T(F,X,G)
and Q(V,F,X,B), its second T is G-X-N or B-X-N. Zero-T B forbids the
latter, so T(G,X,N) is forced. N cannot be A or D (their unique Ts
are already full) or a zero-T original, nor either five; it is ordinary.
N cannot be S, whose two Ts are already full. G now has three distinct
Ts FGX,FGS,GXN and four distinct contacts F,X,S,N.

K=G would add a fourth distinct T at G. K=X would add a third at X.
These Ts cannot coincide: D is distinct from F,G,X,S,N, and J is
distinct from X. Hence K is an ordinary original distinct from X.

Let L be the opposite in U's Q between D,B. It contacts D,B. D has
neighbors U,J,K and this remaining contact. J's complete list A,Z,D,K
contains no B. If L=K, ordinary K with T(D,K,J) and Q(U,D,K,B) forces
a T at B: J's other T is AZJ and K cannot be A or Z (K is ordinary,
and K=Z would overload Z at T(J,D,K)). This would be a new T at J.
Therefore L is distinct from U,J,K, and

    N(D)={U,J,K,L}.

L=X would add D as a fifth distinct contact at X, whose exact list
is F,G,B,N. Thus L is also distinct from X, and

    N(B)={U,V,X,L}.

G's three consecutive Ts FGX,FGS,GXN leave two consecutive Qs and a
fifth contact Y, in order S F X N Y up to reversal. Y is a Q-Q neighbor
of G and cannot be ordinary by the large-corner capacity. It cannot
be U,V (their complete triple lists exclude G) or the only other five
F, already a T-T contact. Therefore Y is A,D or B.

G cannot contact A by N(A). It can contact D only if K or L is G;
K=G has been excluded. It can contact B only if L=G. But L=G would
give G both D,B in addition to F,X,S,N: six distinct contacts at a five.
Thus all possibilities for Y are excluded. K,L,N were never required
to be newly introduced; all ordinary-original reuse is covered by the
quota, simple-link and complete-list arguments. This closes C1.

## 6. C5: the zero four's last Q exceeds a contact-edge face capacity

Now N(U)=ABF,N(V)=ABG. The shared one-T A forces Q(U,A,V,B).
Let F's zero-B endpoint be X and its A endpoint Z; let the corresponding
G endpoints be X',Z'. B's known Q corners give the link path X-U-V-X'.
If X=X', this seals a three-cycle of three distinct faces, impossible
at degree four. Similarly the known three Qs at A forbid Z=Z'. Hence

    N(A)={U,V,Z,Z'}, with T(A,Z,Z').

Both A-side endpoints now have at least two distinct Ts and must be
ordinary; D cannot occur there or internally. The sole one-T exception
D can occur on at most one zero-B endpoint, because X,X' are distinct.
If F,G were noncontacts, their internals would all be ordinary, and
both zero-B endpoint pairs would require D. Impossible. Thus F,G contact.

G occurs internally at R or S in F's fan. If G=S, the two common
neighbors at FG are ordinary R and Z, both with full two-T quotas.
G contacts V, so its third T must extend one of its two Ts at FG to
one of those common points; either overloads it. Thus G=R.
S is ordinary with its two F Ts. G's third T must extend toward X,
not S. X cannot be D, whose single T is already FXG. Therefore X is
ordinary and the third T is T(G,X,W).

The G fan endpoints are S,W. If S were its A-side endpoint, A's unique
T would be T(A,Z,S), giving a third T at S. Therefore S is the zero-B
endpoint, with Q(V,G,S,B), and B's exact four contacts are U,V,X,S.
Its remaining Q has form Q(B,X,K,S). X,S already have the two common
contacts F,G, so K must be F or G. If K=F, edge FX gets a third
distinct face in addition to T(F,X,G),Q(U,F,X,B). If K=G, edge GS gets
a third in addition to T(F,G,S),Q(V,G,S,B). Neither is possible.
The proof includes every W alias; the contradiction uses only the
distinct common contacts, fixed endpoint sides and saturated edge faces.

## 7. C7: two successive endpoint rules cannot complete V's third Q

Here N(U)=ABF,N(V)=BDG. F's fan at U has the same three labeled Ts,
with Q(U,F,X,B),Q(U,A,Z,F). D cannot be at zero-B X because D-B are noncontacts from V,
or internally because it has one T. The zero side forces G=R as before;
S is ordinary. G contacts V and has two Ts at GF; its third T must
extend toward ordinary X rather than full S. Write it T(G,X,W), so
G's fan endpoints are S,W and its full list is V,F,X,S,W.

If S is G's zero-B endpoint, the final-B-Q contradiction of Section6
applies verbatim: B contacts U,V,X,S; its Q opposite is F or G and
either would put a third distinct face on FX or GS. Thus S is the
one-D endpoint and Q(V,D,S,G) is actual.

If D=Z, ordinary S has the two Ts FGS,FSD and the Q corner D/S/G.
Those known corners seal the three-cycle F-G-D in S's link, impossible
at degree four. Therefore D is outside F's fan and Z is ordinary.
The A side forces T(A,Z,J). In particular W cannot be A: that would
give A both this T and T(G,X,A). It cannot be D, opposite/noncontact
of G, nor a zero-T point. Thus W is ordinary.

J is D, G, or ordinary. G is a noncontact of Z by its complete neighbor
list V,F,X,S,W: W cannot equal Z, which would be a third common contact
of F,G besides X,S. Hence J is not G. J=X already gives X five distinct
contacts F,G,B,Z,A. If J=D, the argument below will exclude it directly.

At S, its exact contacts are F,G,Z,D. Its two Ts FGS,FSZ and Q(V,D,S,G)
force the remaining Q corner between D,Z, so Q(S,D,K,Z) is actual.
Z's complete list is F,S,A,J, so K is F,A or J. F cannot contact D,
since D is outside F's complete fan. If J=D, K cannot be J itself,
so K=A and Q(S,D,A,Z) has contact diagonal D-Z from T(A,Z,D).
This excludes J=D.

Let J be ordinary. It has no forced distinctness from W or unused
ordinary originals. Write A's fourth neighbor L, distinct from U,Z,J.
In U's Q between A,B, the opposite contacts A,B. It cannot be Z by
Z's full list; if it were J, the endpoint rule with full Z would force
a T at B. Thus it is L, and L contacts A,B. L is ordinary: neither five
contacts A, D does not contact B, V does not contact A, and other zero-T
or self aliases are excluded by the complete/simple lists. If K=A above, D would
contact A, forcing D=L by A's complete list. That would make D contact
B, forbidden by N(V)=BDG. Hence K=J and Q(S,D,J,Z) is actual.

At ordinary J, the known T(A,J,Z) and Q(Z,J,D,S) leave its second T
at A or D. A's unique T is full, so the center-free saturation rule
forces T(J,D,M). D's unique T and J's two-T quota are now full. M is
ordinary: a zero-T point cannot be in it; A is already full; F,G are
noncontacts of D. Already saturated aliases for M are earlier contradictions.
In particular M is distinct from S. The exact D contacts are V,S,J,M.
At D, its three known corners are Q(V,D,S,G),Q(S,D,J,Z),T(J,D,M).
The remaining corner M/D/V must be Q, of form Q(V,D,M,E).

E contacts V,M, so E is G or B by N(V)=BDG. If E=G, D,G already
have common contacts V,S from their original Q, and M is a third
distinct common contact. Impossible. If E=B, ordinary M has T(D,M,J)
and Q(D,M,B,V). J's other T is AZJ and cannot contain M: M is ordinary
and M=Z would give a third distinct T at Z. The qualified endpoint rule
therefore forces a T at zero-T B. Impossible.
Every original J,L,M alias is either covered by these complete lists
or already violates a simple face/full quota; no fresh-point premise is
used. This closes C7.

## 8. C8: all eight ordinary points are forced, leaving a nonsimple Q

Finally N(U)=ADF,N(V)=ADG. Their one-T common points A,D force the
shared Q(U,A,V,D). Use F endpoints X,Z and G endpoints X',Z', on the
A,D sides respectively. Their three known Q corners seal a C3 link
if either pair of endpoints coincides. Thus

    T(A,X,X'),T(D,Z,Z')

are actual, and all four endpoints are ordinary with two Ts each.
A,D are opposite/noncontact of both fives, and B cannot have a fan T.

If F,G contact, the contact is internal in each fan. Its two common
points include an ordinary internal point with two Ts and an ordinary
endpoint with its fan T and A/D T. G's third consecutive T must extend
to one of them, overloading it. Thus F,G are noncontacts. All four
internals are therefore ordinary and have their two fan Ts.

No F-fan ordinary can equal a G-fan ordinary: an F internal already
has two F Ts, and an F endpoint has a fan T plus its A/D T; either
would acquire a third distinct T from the G fan. F,G are noncontacts,
so a T at F cannot coincide with one at G. Hence the eight ordinary
fan originals are distinct. They are all eight ordinary points of
the fifteen-point row.

F,G and U,V have complete neighbor lists, and A,D have U,V and their
two respective endpoints. Each endpoint has four complete contacts,
e.g. N(X)=F,R,A,X'. None of these originals can contact B. The only
remaining candidates are the four internals R,S,R',S', each with one
unused contact. B has degree four and so contacts all four.

At R the two Ts FXR,FRS give the cyclic path X-F-S, with fourth
neighbor B. At S the two Ts FRS,FSZ give R-F-Z, also with fourth B.
The other face of RS cannot be T because both quotas are full. Its
fourth point beside R must be B, and its third point beside S must
also be B. The putative Q(R,S,B,B) is nonsimple. This is the final
contradiction and closes C8. The N=15 count is used explicitly only
when asserting that these eight distinct ordinary fan points exhaust
the available ordinary originals.

## 9. Exact checks, scope and trust boundary

[check.py](check.py) supplies small exact checks of the eight-family
cover, fixed-role fan placements, cyclic saturation consequences, full
Q-opposite domains, the critical original aliases, edge-face capacity
and the nonsimple shared-fourth-neighbor obstruction. It imports the
preceding21-row list and removes exactly this row, listing all20 in
[EXPECTED.json](EXPECTED.json). No full contact-map or packing enumeration
is claimed. The hand argument supplies arbitrary unseen-original reuse.

[audit.py](audit.py) imports no production code and compares the permitted
local entries using raw binary incidence masks, role permutations,
Hamiltonian edge sets and explicit triangle/face incidence counts.
Its compact result is [AUDIT_EXPECTED.json](AUDIT_EXPECTED.json). Nonempty
relaxed controls demonstrate the relevant degree/quota/Q-diagonal cuts;
they are necessary assignments, not sphere packings. Normal and Python-O
replays must agree. The credited Bernstein margin is rebuilt exactly.

[DEPENDENCIES.json](DEPENDENCIES.json) pins six already-public sibling
proof/catalogue files. Their bytes are checked; no prior production
kernel, metric collar, large certificate, private input or solver is used.
The prior21-profile beta cover, all earlier r1 exclusions and the
geometric reductions retain their original hypotheses. Source checks
do not independently prove their written mathematical bridges.

The current [Cohn table](https://cohn.mit.edu/spherical-codes/) and
[15-point coordinates](https://spherical-codes.org/data/3/15) were refreshed.
The N15 row remains unstarred with cosine
0.59260590292507377809642492233276; its890 coordinate bytes are unchanged.
The primary Musin--Tarasov seed proves N14, not N15. A targeted live
primary search located no N15 theorem, without exhaustive absence or
historical priority claims. Classical star/common-contact facts are
credited; the new contribution is the complete original-face exclusion
of this row and its independently replayable local reduction.

Independent mathematical review, formalization, unrestricted optimizer
occurrence and global numerical bounds remain open. Reproduction uses
CPython>=3.11 and only its standard library; see [README.md](README.md).
