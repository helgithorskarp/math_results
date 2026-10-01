# Closing the four-triangle/two-triangle pair of fives

Actual author **six-tammes-1**, role **researcher**, 2026-10-01.
Complete conditional hand proof with small exact local checks and a
different same-author finite representation. Written spherical and
face/contact bridges remain unformalized; independent mathematical review
is pending.

## Statement and inherited scope

Let fifteen distinct unit points have minimum geodesic separation d,
c=cos(d). Assume the **complete** connected contact graph has degrees
3,4,5 and a cellular minor-geodesic sphere embedding into simple strictly
convex hemispherical T/Q faces, with nine quadrilaterals. Throughout the
**full open interval** `1/2<c<3/5`, the row

    n3=n5=2,n4=11,a=2,b=1,(f0,f1,f2)=(1,0,1)

is impossible. Its actual, distinct original roles are

    U,V: zero-T threes; F: four-T five; G: two-T five;
    A,D: one-T fours; B: zero-T four;
    eight remaining originals: ordinary two-T fours.

Here f_j counts fives with4-j triangles. No beta/H assumption is used for
this new row. All twelve ordered neighbor pairs and four equal-role
families are covered. No complete contact-map or packing enumeration is
asserted.

The preceding [two-one-T-four source proof](../tammes15_two_one_triangle_fours_exclusion/PROOF.md),
verified commit `71535b1c836995acfe9b6f6bef3727b97af82c09`, provides the
checked20-profile beta cover. Its original graph package was rejected and
is **not committed**. Removing exactly the new row gives **19 profiles,
0/8/11 at r=n3=n5=1/2/3**, with all preceding cover hypotheses retained.
Beta is the unique root in `(119/200,3/5)` of
`1+4c+2c^2-4c^3-11c^4-24c^5`. This corollary concerns a source catalogue;
it does not turn any rejected graph attempt into a committed claim.
Global numerical Tammes15 bounds, optimality, unrestricted optimizer
occurrence and larger-face coverage remain open.

## 1. Credited corner, link and endpoint facts

The [odd-degree reduction](../tammes15_nine_quad_odd_degree_reduction/PROOF.md),
source `d6547391ae745a70087f067568047c8dbba0e099`, graph h7817
`bafkreic6shrttfdlf7vbae5wye7eytruyxeeb7j6422ubytjcwlaadlkfa`,
proves the full-interval degree/corner facts. Put

    alpha=acos(c/(1+c)),phi=2pi-4alpha,
    rho(u)=2atan(1/(c*tan(u/2))),y=rho(phi).

A T corner is alpha. Opposite Q corners agree; adjacent corners are
related by the decreasing involution rho. Completeness and strict convexity
give `alpha<u<2alpha` for every Q corner. These classical identities are
credited to [Musin--Tarasov, Proposition3.2](https://arxiv.org/abs/1410.2536)
and the [prior geometric audit](../tammes_15_triangle_quad_exclusion_review1/README.md),
source `f026ccec6854eb913e5c156f4ff0cf08ed5cb4a9`, graph h7182
`bafkreiflxdrel4fv4opchhucsisp7ylw2lsfgtrv4q7tya3o5vjh4ld53a`.
That earlier review does not review this result.

Every Q corner at a five is at most phi. F's sole Q corner is exactly
phi; all three Q corners at deficient G are strictly smaller. Q corners
at an ordinary two-T four or a three are strictly greater than phi.
Hence F's Q opposite lies in `{A,D,B}`, and G's three Q opposites do too.
They are distinct: two actual points have at most two common contact
neighbors, and a simple Q already supplies both. Thus G's Q opposites
are **exactly A,D,B**, and G contacts none of them.

The established strict comparison is `y>pi-alpha>phi`. Its first numerator
is `(1+c)(1+c-4c^2)`; the quadratic's Bernstein coefficients on
`[1/2,3/5]` are `1/2,7/20,4/25`. Adjacent fives in a Q are impossible.
Two consecutive small Q corners at a deficient five would give their
common contact neighbor two corners greater than y. A vertex of degree
at least four cannot receive these: its other corners contribute at
least2alpha, giving a sum greater than2pi. Thus every Q-Q contact at G
leads to a three. This general local consequence is **already proved** in
the [single-three fan reduction](../tammes15_nine_quad_single_three_fan_reduction/PROOF.md),
source `276ec8b0508c7960aa73517f3b7e6e0ef03ca3cf`, graph h7912
`bafkreicjxhbyqcxdeplfvby6k2bysmhhk7fbksapoenneqsigtfos2dulu`,
Section1. Its proof needs no uniqueness of the three or five. That
section also proves on the full interval that a three contacts only
deficient originals: its two adjacent Q corners have sum greater than
`2pi-2alpha`, while their neighboring corners have sum strictly smaller
than that quantity. This excludes an ordinary four and a second three;
an ordinary five has no Q-Q edge. The
[prior corner-capacity proof](../tammes15_eight_quad_reduction/FIVE_CORNER_CAPACITY.md),
source `9f43d6fdac0c7b0e0333c527c739cb0c24c68afb`, graph h7444
`bafkreiasa2n2mywlaokeron7wkpsj4z2ows4asfkm5fbnf6gphzbgmtvba`,
supplies credited background.

Consequently G with one three contact has its two Ts separated. All
four other contacts are T-Q; it cannot contact F. With two three contacts,
its two Ts form a consecutive fan `GXR,GRZ`; its Q-Q neighbors U,V are
adjacent in the link. Its endpoints X,Z are ordinary: G has no A/D/B
contact, threes have no Ts, and F cannot be adjacent to G in a Q. The
internal R is ordinary or F. These assertions retain both star orientations.

Every neighbor pair of a zero-T three is noncontact, since it is opposite
in that three's Q. This is credited original-face reasoning in the
[single-three closure](../tammes15_single_three_branch_exclusion/PROOF.md),
source `ea0e70fa3ae7c287f5f54b59b9a06cdc878c92ca`, graph h8307
`bafkreidhqy3zbi7rlzcuy44ve2zexokku44vktrsdyjw3p4o6pv6e7rj2a`;
it does not require a unique three.

F has four consecutive Ts with five distinct contact neighbors, a fan
`FXR,FRS,FST,FTZ`, and sole Q(F,X,H,Z). Its internals have two F Ts;
they are ordinary or G. Endpoints are ordinary or A/D; zero-T originals
cannot occur and adjacent fives in the Q forbid endpoint G. F cannot
contact any zero-T point, since its single Q leaves no Q-Q contact edge.
A one-T neighbor of F must be a fan endpoint: every internal has two Ts.

We use the **qualified** ordinary endpoint rule: for ordinary E with
T(H,E,R),Q(H,E,C,W), its fourth neighbor J gives the second T at R or C.
If R's quota is full and its other known Ts exclude E, the R choice is
a new T and is impossible; T(E,C,J) is forced. In the ordinary fan pair
uses below, R's other fan T excludes E because all fan neighbors are
distinct. A full quota alone is insufficient. The explicit qualification
in the preceding source is retained; no unique-five degree default is used.

If both endpoints of F are ordinary and both neighboring internals are
ordinary, this forces a T at each endpoint through the same Q opposite H.
Zero-T H fails immediately. A one-T H could have the two forced Ts coincide
only as T(H,X,Z), making X-Z a contact diagonal of F's Q. Otherwise H
gets two distinct Ts. Thus a zero/one-T opposite is impossible in this
all-ordinary pair situation.

## 2. Complete four-family cover

F has no three contact, and a three contacts only deficient fours or
fives. N(U),N(V) are distinct triples in `{A,B,D,G}`. A repeated triple
would give three common contact neighbors. Their twelve ordered pairs,
under U/V and A/D renaming only, have four types:

    C1 ABD / ABG (4 ordered entries),
    C2 ABD / ADG (2),
    C3 ABG / ADG (4),
    C4 ABG / BDG (2).

F/G cannot be exchanged because their triangle quotas differ. Every pair
has exactly two common contacts. A shared one-T four has adjacent Q-Q
contacts U,V and forces a Q through the other common contact. In C4 the
double-three G star forces it. Thus the respective common Qs are

    Q(U,A,V,B),Q(U,A,V,D),Q(U,A,V,G),Q(U,B,V,G).

This uses equal-role renaming, not spatial symmetry. No beta restriction
is extended to the full interval.

## 3. C1 and C2: the ordinary-five fan cannot have an exception

Here U has neighbors A,D,B, making AD,AB,DB noncontacts. G contacts only V,
so its Ts are separated and FG is a noncontact. All three internal fan
neighbors of F are therefore ordinary. Its sole Q opposite H lies in
A,D,B. Any one-T endpoint A or D would contact another member of this
independent triple across the Q boundary, impossible. Thus both endpoints
are ordinary. The all-ordinary pair consequence in Section1 contradicts
the zero/one-T quota at H. Both families are closed.

## 4. Local shared-opposite obstruction at adjacent fives

We isolate the small original-face lemma used below. Let F be a four-T
five, G another five, H a one-T four, and V a zero-T three. Suppose

    T(F,G,Z),Q(V,G,Z,H),Q(F,P,H,Q)

are actual faces, Z is ordinary, and V contacts H. The Q(F,P,H,Q) is F's
sole Q. Then this local configuration is impossible.

If Z=P or Q, the three distinct known corners at ordinary Z give link
edges F-G (T),G-H (Q),H-F (Q). They seal a three-cycle, which cannot fit
Z's degree-four cyclic link. The two Qs are distinct since F cannot
contact the zero-T V.

Otherwise Z is an internal F-fan point, hence has two F Ts. H has the
four distinct contacts V,Z,P,Q. H is a noncontact of F because they are
Q opposites, so neither known F T at Z contains H. Any T at H containing
Z would therefore be new and would exceed Z's quota. H's unique T
cannot contain zero-T V either; it must be T(H,P,Q), making P-Q a
contact diagonal of F's Q. This is
impossible by completeness. No extra point is introduced. The alternative
Z=P/Q is handled before using the four-distinct-contact list.

The proof uses a degree-four link and actual quotas, not numeric coordinates
or an assumed planar completion. Releasing Z's quota leaves four abstract
one-T H stars, a nonempty necessary control rather than a packing.

## 5. C3: ABG/ADG

Now A contacts both threes, and the G fan has faces

    T(G,X,R),T(G,R,Z),
    Q(U,G,X,B),Q(V,G,Z,D),Q(U,A,V,G).

Its endpoints are ordinary. If R is ordinary, the qualified rule at X
forces a T at zero-T B. Thus R=F, so FG is a T-T contact. In F's fan G
is one of the three internals; its two neighboring fan originals are
exactly the two ordinary G endpoints X,Z.

F's sole Q opposite H is A,D or B. H=A is impossible: A then has the
four contacts U,V and F's two Q endpoints. Its unique T must join those
endpoints, a forbidden Q diagonal. H=D is impossible by Section4: use
T(F,G,Z),Q(V,G,Z,D) and F's Q with opposite D. This handles every F-fan
position and the alias of Z with either F endpoint.

Suppose H=B. A cannot be an F endpoint since AB is a noncontact; the only
one-T endpoint exception is D. If G is the middle F internal, at least
one ordinary endpoint has an ordinary neighboring internal, forcing a T
at B. If G is next to one F endpoint, the other endpoint must be D;
otherwise that ordinary endpoint/internal pair again forces a T at B.

Reverse the fan names if needed. It is then

    F-neighbor path Y,G,W,L,D,
    with Ts FYG,FGW,FWL,FLD and Q(F,Y,B,D).

All five are distinct actual F neighbors; Y,W are the two G endpoints.
D's unique T is FLD, and its exact contacts are `{F,L,B,V}`. But the
G Q with opposite D requires D to contact one of Y,W. Both differ from
F,L,B,V. This would be a fifth contact at D. The contradiction closes C3.

## 6. C4: ABG/BDG

Here the G fan has

    T(G,X,R),T(G,R,Z),
    Q(U,G,X,A),Q(V,G,Z,D),Q(U,B,V,G).

Its endpoints are ordinary; R is ordinary or F. AB and DB are noncontacts,
and A,D each contact just one of the threes.

If R is ordinary, the two qualified endpoint rules force T(A,X,J) and
T(D,Z,K). In this case F and G are noncontacts. Suppose A contacts F.
A is a one-T F endpoint, so its unique T must be T(F,A,X), identifying
J=F. X is then an internal F-fan neighbor, with two distinct F Ts, in
addition to T(G,X,R). This exceeds X's two-T quota; the G T differs from
both F Ts because FG is a noncontact. Hence AF is impossible. The same
argument excludes DF. All five F neighbors are therefore ordinary, and
the all-ordinary pair consequence contradicts its Q opposite in A,D,B.

Suppose R=F. For H=A or D, Section4 applies to its G-side Q and F's sole
Q: the one-T H contacts its associated zero-T U or V, and the G endpoint
in that Q is ordinary. Thus neither is an F Q opposite.

For H=B, neither A nor D can be an F endpoint because AB,DB are
noncontacts. Both endpoints are ordinary. G is a single internal original
and cannot occupy both disjoint endpoint/internal pairs. At least one
pair is ordinary, and its qualified rule forces a T at B. This closes C4.

All four families and all actual-original reuse are now covered. The proof
never assigns a degree-four default to G and never declares F saturated
merely from the two shared FG triangles: its full four-T fan is used.

## 7. Exact checks and evidence boundary

[check.py](check.py) checks the complete12/4 cover, all separated/single-three
and consecutive/double-three G stars, F's four-T stars, the shared-opposite
lemma's link alternatives, opposite quotas/diagonals, all F-internal positions
and last one-T endpoint contact lists. [audit.py](audit.py) imports no
production code and rebuilds the permitted entries using binary incidences,
role permutations and Hamiltonian edge sets. Normal/-O outputs must match
[EXPECTED.json](EXPECTED.json) and [AUDIT_EXPECTED.json](AUDIT_EXPECTED.json).
The credited Bernstein margin is rebuilt exactly. Nonempty released-quota
and released-diagonal controls are abstract necessary assignments, not
spherical packings or counterexamples to the geometric theorem.

[DEPENDENCIES.json](DEPENDENCIES.json) pins seven public sibling proof and
catalogue files. The preceding20-row source cover is imported, not regenerated,
and exactly one row is removed. No previous metric collar, solver, private
input, float sign or exhaustive packing corpus is used. The written geometric
and original-face bridges remain separate, unformalized obligations.

The live [Cohn table](https://cohn.mit.edu/spherical-codes/) retains the
unstarred N15 row and cosine0.59260590292507377809642492233276; the
[coordinate table](https://spherical-codes.org/data/3/15) remains890bytes.
The primary Musin--Tarasov seed proves N14, not N15. No exhaustive absence
or historical-priority claim is asserted. The new content is the complete
conditional row exclusion and the local shared-opposite obstruction;
classical and earlier campaign facts are explicitly credited.

Independent review, formalization, unrestricted optimizer occurrence and
global numerical bounds remain open. See [README.md](README.md) for exact
reproduction and the source-versus-graph publication status.
