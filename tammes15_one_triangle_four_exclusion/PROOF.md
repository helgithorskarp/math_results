# Closing the two-five row with one one-triangle four

Actual author: **six-tammes-1**, role **researcher**, 2026-10-01.
Status: complete conditional hand proof with small exact local checks and
a separate same-author finite representation. Independent mathematical
review and formalization are pending.

## Statement and scope

Let fifteen distinct points on the unit sphere have minimum geodesic
distance d and c=cos(d). Assume their **complete** contact graph is
connected, has degrees 3,4,5, and its minor geodesic edges give a cellular
sphere decomposition into simple strictly convex triangles T and
quadrilaterals Q, each in an open hemisphere. Assume exactly nine Qs.
On the **full open interval** `1/2<c<3/5`, the following row is impossible:

    n3=n5=2,n4=11; a=1,b=2; (f0,f1,f2)=(1,1,0).

Here a,b count one-T and zero-T fours; f_j counts fives with 4-j Ts.
There are eight ordinary two-T fours. Name the exceptional original
vertices as follows:

    U,V: zero-T threes; F: three-T five; G: four-T five;
    A: one-T four; B,C: zero-T fours.

All seven originals are distinct and keep these fixed roles. The proof
uses no beta/H assumption and no finite enumeration of complete maps.
Its new step is propagation through A's forced T, followed either by
a forced T at a zero-T four or an overloaded ordinary five star.

Together with the preceding [disjoint fan-pair exclusion](../tammes15_two_deficient_fives_fan_exclusion/PROOF.md),
source `4b8ae42b4c87cd223aecf9261319a1091a06bc4b`, graph h8328
`bafkreiflgwet2ctcbjwhldykxhpugeycu6arhs4fxprtoquhkui44cqeae`,
the necessary beta catalogue now has **21 profiles,0/10/11 at
r=n3=n5=1/2/3**. The full prior catalogue and r=1 exclusion are credited
dependencies, not re-proved here. Beta is the unique root in
`(119/200,3/5)` of `1+4c+2c^2-4c^3-11c^4-24c^5`.
The new row exclusion itself holds throughout `1/2<c<3/5`.

These are conditional count profiles, not realized contact maps or
packings. Global Tammes-15 numerical bounds and optimality, unrestricted
optimizer occurrence and larger-face coverage remain open.

## 1. Prior local geometry, with its original interval

The [odd-degree reduction](../tammes15_nine_quad_odd_degree_reduction/PROOF.md),
source `d6547391ae745a70087f067568047c8dbba0e099`, graph h7817
`bafkreic6shrttfdlf7vbae5wye7eytruyxeeb7j6422ubytjcwlaadlkfa`,
proves on this full interval that threes have no Ts, fours have at most
two, and fives at most four. A three contacts only deficient fours or
fives. Two distinct points have at most two common contact neighbors.
These facts do not require beta or triangle-freeness of H.

Put `alpha=acos(c/(1+c)),phi=2*pi-4*alpha` and
`rho(u)=2*atan(1/(c*tan(u/2)))`. A T corner is alpha; opposite Q corners
agree and adjacent ones are related by rho. Completeness gives strict
Q-corner bounds `alpha<u<2alpha`. These classical identities are from
[Musin--Tarasov, Proposition 3.2](https://arxiv.org/abs/1410.2536), with
the [prior geometric audit](../tammes_15_triangle_quad_exclusion_review1/README.md),
source `f026ccec6854eb913e5c156f4ff0cf08ed5cb4a9`, graph h7182
`bafkreiflxdrel4fv4opchhucsisp7ylw2lsfgtrv4q7tya3o5vjh4ld53a`.
That audit does not review the present result.

Every Q corner at a five is at most phi, since its other four corners
are at least alpha. The established full-interval comparison

    y=rho(phi)>pi-alpha>phi

therefore forbids **adjacent degree fives in any Q**. Indeed one corner
at most phi gives its adjacent corner at least y, above the five bound.
The second inequality is `3alpha>pi`. For the first, with H=1+2c and
D=1+2c-c^2, comparison of positive half-angle tangents reduces to

    D-2c^2 H=(1+c)(1+c-4c^2)>0.

The quadratic has exact positive Bernstein coefficients
`1/2,7/20,4/25` on `[1/2,3/5]`. This is a replay of the credited h7817
comparison, also present in the [ordinary-five corner proof](../tammes15_eight_quad_reduction/FIVE_CORNER_CAPACITY.md),
source `9f43d6fdac0c7b0e0333c527c739cb0c24c68afb`, graph h7444
`bafkreiasa2n2mywlaokeron7wkpsj4z2ows4asfkm5fbnf6gphzbgmtvba`.
It supplies no new metric bound or closed-endpoint graph theorem here.

Every pair of contact neighbors of a zero-T three is a noncontact pair:
the two neighbors are opposite in one of its three simple Q faces,
whose contact diagonal is forbidden by completeness. This fact is in
the [single-three branch proof](../tammes15_single_three_branch_exclusion/PROOF.md),
source `ea0e70fa3ae7c287f5f54b59b9a06cdc878c92ca`, graph h8307
`bafkreidhqy3zbi7rlzcuy44ve2zexokku44vktrsdyjw3p4o6pv6e7rj2a`,
Section 5, and does not depend on having a unique three.

We use the elementary ordinary endpoint rule from the
[prior fan reduction](../tammes15_nine_quad_single_three_fan_reduction/PROOF.md),
source `276ec8b0508c7960aa73517f3b7e6e0ef03ca3cf`, graph h7912
`bafkreicjxhbyqcxdeplfvby6k2bysmhhk7fbksapoenneqsigtfos2dulu`:
if an ordinary four X has T(H,X,R) and adjoining Q(H,X,D,W), and
ordinary R already has two distinct Ts including that T, X's second
T is T(X,D,J), with J its fourth contact neighbor. It cannot use H
because HX already has its T and Q, nor R whose T count is full.
The proof requires no degree-five assumption on the center H. We
will also apply it with the center H=A, a one-T four.

## 2. Three possible original neighbor families

The full-interval neighbor restriction gives N(U),N(V) subset A,B,C,F;
the ordinary G is ineligible. F has at most one three contact: its
cyclic five-sector star with three Ts and two Qs has at most one
Q-Q edge, and every edge to a three is Q-Q.

The only triples are ABC,ABF,ACF,BCF. At most one can contain F.
Both cannot be ABC because U,V would then have three common contact
neighbors. Thus, after exchanging the names U,V, the exhaustive list is

    N(U)={A,B,C}, N(V)={F,A,B}, {F,A,C}, or {F,B,C}.

This directly proves all three families on the full interval. It does
not extend the beta catalogue's "one five per three" assertion outside
its proved interval. In particular AB,AC,BC are all noncontact pairs
by the U-star rule in Section 1.

## 3. Closing the FBC family

F contacts V, so its two Qs are consecutive and its three Ts form a
fan with four distinct actual neighbors X,R,S,Z. Its Q opposites are
B,C, both with zero Ts. The preceding h8328 local lemma requires an
exception, a one-T four or a five, in each disjoint pair {X,R},{Z,S}.

Only A and G can be exceptions. A cannot be internal R or S because
an internal point already has two Ts. At an endpoint X or Z, the
actual Q boundary makes A contact B or C, contrary to the AB/AC
noncontacts from N(U)=ABC. So A is outside the fan. The single G
cannot cover both disjoint pairs. This family is impossible.

## 4. The FAB/FAC fan and forced triangle at A

B and C have identical degree/T roles. Exchanging their names is an
involution on the original vertices, preserving all faces and contacts;
it is a relabeling, not a spatial symmetry assumption. It suffices to
handle N(V)=FAB, with the zero-B side of F's fan labeled X,R and the
one-A side labeled Z,S. The actual faces are

    T(F,X,R), T(F,R,S), T(F,S,Z),
    Q(V,F,X,B), Q(V,A,Z,F).

The fan neighbors X,R,S,Z are four distinct contacts of F. A is opposite
F in the second Q, so is a noncontact of F and cannot occupy a fan
position. All fan points have a T. They are ordinary fours unless one
is the only other five G.

If X,R were both ordinary, the endpoint rule would force a T at B,
contradicting its zero count. Therefore X or R equals G. X=G is
impossible because Q(V,F,X,B) would have adjacent fives F,G. Hence

    R=G; S,Z are ordinary fours.

The endpoint rule at Z next to ordinary S now forces T(Z,A,J), where
J is Z's fourth contact neighbor, distinct from F,S,A. This is A's
unique T. J has a T, so is an ordinary four or G. It cannot be U,V,B,C
(zero Ts), A (simple face), S (already a distinct contact of Z) or F
(noncontact of A). Any remaining ordinary original point is allowed.
In particular the proof does not assume J is newly introduced.

## 5. Ordinary J forces a forbidden T at C

Suppose J is ordinary. The four actual contacts U,V,Z,J of A are
distinct: U,V have no Ts, Z,J have Ts, and Z is distinct from J.
They therefore form its complete neighbor list. Similarly

    N(A)={U,V,Z,J}, N(Z)={F,S,A,J}, N(V)={F,A,B}.

In U's Q between the neighbors A,C, its opposite W contacts A,C and
is distinct from U. Since it contacts A, W is one of V,Z,J.
V cannot contact C by its complete degree-three neighbor list. Z
cannot contact C by its complete degree-four list: F,S,A,J all have
Ts whereas C has none. Thus W=J and Q(U,A,J,C) is an actual face.

At J the known faces include T(A,J,Z) and Q(A,J,C,U). Ordinary Z
already has its two distinct Ts T(F,S,Z),T(Z,A,J). The endpoint rule,
with the center A, forces J's second T to include C. This contradicts
t(C)=0.

All actual aliases remain. For example J=X is already impossible:
the known faces give ordinary X five distinct contacts F,G,B,Z,A.
For any other ordinary J, the preceding complete-neighbor argument
forces the Q and contradiction. No additional distinctness of a
fourth J neighbor, beyond the required simple degree-four link, is
assumed. Its possible reuse of another original cannot repair a T at C.

## 6. The remaining alias J=G overloads its star

If J=G, all five actual contacts of G are

    F,X,S,Z,A.

They are distinct: F,X,S,Z are distinct fan vertices/center, and A is
a noncontact of F whereas X,S,Z contact F. The three already known
Ts at G are

    T(G,F,X), T(G,F,S), T(G,Z,A).

G is the ordinary four-T five and needs one further T. The first two
Ts force X,F,S consecutive in G's cyclic neighbor order. The last
forces Z,A consecutive. Up to reversing the cyclic order the two
possible orders, written from X, are

    X F S Z A; X F S A Z.

In the first order the additional T is either T(G,S,Z) or T(G,A,X).
The former gives a third T at S, which already has T(F,G,S),T(F,S,Z).
The latter gives a second at A, which already has T(G,Z,A).
In the second order the choices are T(G,S,A) or T(G,Z,X). The former
overloads S and A; the latter gives a third T at Z, already incident
with T(F,S,Z),T(G,Z,A). Every possible fourth G triangle is impossible.

These additional Ts differ from the prior Ts as sets of original
vertices, by the distinctness just proved. All cycle orders and both
orientations are retained, including every choice of the unique Q.
The cases ordinary J and J=G exhaust the third point of A's T, so
FAB and its B/C exchange FAC are impossible. Together with Section 3
this excludes the stated row.

## 7. Exact local checks and the catalogue corollary

[check.py](check.py) enumerates all 16 ordered triple pairs and checks
the six permitted labeled families. It retains all 25 A/G placement
choices in a fan before rejecting the four inside collisions of
distinct role originals; all 21 remaining entries are classified for
FBC and FAB. One-T A at an internal point is rejected by its exact
T count; A outside and G internal R is the sole retained FAB placement.
FAC follows by the explicit original B/C role exchange.

The checker treats ordinary J=X and an arbitrary other ordinary J,
reconstructs the full A/Z/V neighbor lists and Q-opposite domain,
then checks both ordinary J link orientations. It checks all eight
oriented G=J stars consistent with the three known Ts and four-T G.
Every extra T overloads at least one original. These are exact finite
checks of the hand proof's local cases, not a full packing enumeration.

[audit.py](audit.py) imports no production code. It loops over all
256 ordered binary neighbor-mask pairs, binary fan-role masks, and
raw ordinary-J neighbor permutations with binary face words. For G=J
it enumerates all 252 five-edge subsets of K5, selects all 12 undirected
Hamiltonian cycles, computes actual triangle incidence counts, and
expands both orientations afterward. All permitted local entries are
compared individually. This representation is different from the
production cyclic-permutation enumeration; it is still a same-author
audit, not independent mathematical review.

Nonempty controls relax the U-neighbor independence, F's one-three
capacity, exclusion of repeated ABC triples, G's four-T count, or
A/Z triangle saturation. The latter two reopen two G stars each,
and the three-T G control has four oriented stars. These controls
are relaxed necessary-role assignments, not spherical packings.
The three credited Bernstein coefficients are checked separately.

The preceding h8328 source supplies 22 necessary beta profiles. Exactly
one is the newly excluded r2,a=1,b=2,(f0,f1,f2)=(1,1,0) row. Removing
it gives 21, with counts0/10/11. [EXPECTED.json](EXPECTED.json) lists
all 21 rows; [AUDIT_EXPECTED.json](AUDIT_EXPECTED.json) records the
separate entry comparisons. No full prior catalogue enumeration is
replayed. Its hypotheses and all preceding r1 exclusions remain
dependencies with their original scope.

[DEPENDENCIES.json](DEPENDENCIES.json) pins five already-public sibling
proof/catalogue files, read and hash checked without importing their
code. No unique-five degree-four-default kernel, solver, floating-point
sign, metric collar, private corpus, coordinate input or live network
input is used. CPython>=3.11 with its standard library suffices.
Reproduction commands are in [README.md](README.md).

The written spherical geometry, complete-face/contact correspondence
and the prior theorems remain unformalized trust boundaries. Exact
finite replay and source publication do not independently prove those
bridges. Current [Cohn table](https://cohn.mit.edu/spherical-codes/) and
[15-point coordinates](https://spherical-codes.org/data/3/15) were refreshed:
the N=15 row remains unstarred with cosine
0.59260590292507377809642492233276 and unchanged coordinate bytes.
The primary Musin--Tarasov seed proves N=14. A targeted live primary
search found no N=15 solution, without an exhaustive absence or priority
claim. Global numerical bounds remain unchanged.
