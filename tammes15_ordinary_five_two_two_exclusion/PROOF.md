# Tammes-15: the ordinary-five profile (0,2,2) is impossible

Author: **six-tammes-1**, role: **researcher**, 2026-10-01.
Status: complete author-checked conditional hand proof, exact original-face
alias covers, and a separate algorithm checking every block boundary.
The written geometric bridges are unformalized; independent mathematical
review is pending. All team signatures use one shared identity.

## Statement and scope

Let fifteen distinct unit points have minimum geodesic separation d and
c=cos(d), with **1/2<c<3/5**. Assume their **complete** contact graph,
whose edges join pairs with inner product c, is connected and has degrees
3..5. Its minor geodesic edges give a cellular sphere decomposition into
simple strictly convex triangles T and quadrilaterals Q, each contained in
an open hemisphere. Assume exactly nine Qs and exactly one degree-three
vertex U. Euler then gives eight Ts, one degree-five F and thirteen fours.
For a vertex v let t(v) count its incident triangles. Write

    delta=4-t(F), a=#{fours with t=1}, b=#{fours with t=0}.

**Theorem. The profile (delta,a,b)=(0,2,2) is impossible.**
The proof concerns actual original faces and all possible identifications
of their vertex positions; it does not assume an isolated drawn strip.

Together with the preceding [four-profile theorem](../tammes15_delta_one_three_one_exclusion/PROOF.md),
source 02dfda9a2152480d4803caa7c14cc75c1bd4aded, committed h8100,
bafkreianh25uvoqubpzijxt547ykijbkftegfuuy2qgvnvljbul5bk2zj4,
this leaves **three necessary single-three count profiles** on the full
open interval:

| delta | a | b |
|---:|---:|---:|
| 0 | 6 | 0 |
| 0 | 4 | 1 |
| 1 | 5 | 0 |

On 1/2<c<beta, beta the unique root in (119/200,3/5) of

    1+4c+2c^2-4c^3-11c^4-24c^5,

the [older odd-degree count cover](../tammes15_nine_quad_odd_degree_reduction/PROOF.md),
source d6547391ae745a70087f067568047c8dbba0e099, h7817,
bafkreic6shrttfdlf7vbae5wye7eytruyxeeb7j6422ubytjcwlaadlkfa,
therefore has **26 necessary profiles, 3/12/11 for r=n3=n5=1/2/3**.
The r=2,3 rows are imported unchanged. Counts are not complete contact
maps, realized packings or a census of global optimizers. Unrestricted
Tammes-15 numerical bounds and optimality are unchanged.

## 1. Angular facts and actual links

The full-interval angle and endpoint inputs are proved in the
[single-three fan reduction](../tammes15_nine_quad_single_three_fan_reduction/PROOF.md),
source 276ec8b0508c7960aa73517f3b7e6e0ef03ca3cf, h7912,
bafkreicjxhbyqcxdeplfvby6k2bysmhhk7fbksapoenneqsigtfos2dulu.
Its metric collar certificate is not needed here. We recall the inputs
and their use to make the geometric bridge explicit.

Put alpha=acos(c/(1+c)), phi=2pi-4alpha, A=2pi-2alpha, and
rho(u)=2atan(1/(c tan(u/2))). Every T corner is alpha. Opposite Q
corners are equal; adjacent ones are related by rho. Completeness and
strict convexity give alpha<u<2alpha at every Q corner. These are
classical identities; see [Musin--Tarasov, Proposition 3.2](https://arxiv.org/abs/1410.2536)
and the [earlier geometric audit](../tammes_15_triangle_quad_exclusion_review1/README.md),
source f026ccec6854eb913e5c156f4ff0cf08ed5cb4a9, h7182,
bafkreiflxdrel4fv4opchhucsisp7ylw2lsfgtrv4q7tya3o5vjh4ld53a.
That audit does not review the present result.

Here pi/3<alpha<2pi/5. Angle sums imply that a three has no Ts,
a four at most two, and a five at most four. Call a two-T four ordinary.
Every Q corner at a three or ordinary four is greater than phi:
the other two corners at a three are less than 2alpha, and at an
ordinary four the two Q corners sum to A while each is less than 2alpha.
An ordinary five has sole Q corner exactly phi. Its Q opposite is
therefore a deficient four, rather than U or an ordinary four.

A three contacts only deficient fours in the current delta-zero row.
For completeness, at a three the two Q corners u,v next to an edge
satisfy u+v>A. Put b0=2atan(1/sqrt(c)). The previously established
inequality u+rho(u)<=2b0<A gives

    rho(u)+rho(v) < 4b0-A < A.

An ordinary four needs its two Q corners at that edge to sum to A,
which is impossible. An ordinary five has only one Q and cannot have
the two Qs required at an edge incident with a three. Thus U's three
distinct contacts are among exactly the four deficient fours. The
inequality and corner capacity are also recorded in the
[ordinary-five corner proof](../tammes15_eight_quad_reduction/FIVE_CORNER_CAPACITY.md),
source 9f43d6fdac0c7b0e0333c527c739cb0c24c68afb, h7444,
bafkreiasa2n2mywlaokeron7wkpsj4z2ows4asfkm5fbnf6gphzbgmtvba.

Two distinct points have at most two common contact neighbors: their
affine contact planes intersect in a line with at most two sphere
intersections. Antipodal points have none since c>0. A contact K4 is
impossible since its Gram matrix has eigenvalues 1-c,1-c,1-c,1+3c
and rank four. A Q diagonal is a noncontact in the complete graph.

The incident faces at a vertex form one simple cyclic link of length
its degree. A proper closed link, conflicting predecessor or successor,
or too many distinct contact neighbors is impossible. Repeated
descriptions of the same actual face coalesce, but opposite orientations
cannot describe the same strictly convex hemispherical cell. All face
words below follow one orientation of the sphere.

## 2. The ordinary-five star and its adjacent strip

F has four consecutive Ts. The following eight original anchors are
distinct:

    F,U,X,R,S,T,Z,D.

Here T is also the name of an internal fan vertex; a parenthesized
three-letter face word denotes a triangle. F's complete cyclic contact
list is X,R,S,T,Z, and its actual faces are

    (F,X,R), (F,R,S), (F,S,T), (F,T,Z), (F,Z,D,X).

The last face is a Q. Its opposite D is a deficient four and a
noncontact of F; it is not any F neighbor. U is not a contact of F
and cannot equal D by the small opposite corner. This proves the eight
anchor identities without assuming eight independent coordinates.

R,S,T already have two Ts. Their fourth neighbors L,K,M are respectively
distinct from their three known neighbors. Closing their four-links
forces these actual Qs, with P,Q their as-yet unidentified opposites:

    (R,L,K,S), (R,X,P,L), (S,K,M,T), (T,M,Q,Z).       (1)

Every later letter may equal an earlier original unless a necessary
condition excludes the identification. In particular L=T/Z and M=X/R
are not banned by an unsupported outside-the-fan assumption.

K is outside F and all five F contacts. It is not F,R,S,T because
it is S's fourth contact. K=X gives contact K4 F,X,R,S; K=Z gives
contact K4 F,S,T,Z. Hence F-K is a noncontact. Also K is neither U
(S is ordinary) nor D (F,D would have common contacts X,Z,S).
Thus K is a four different from D. Similarly L is a four other than
U,D,F,R,X,S; L=D gives F,D common contacts X,Z,R. M is a four
other than U,D,F,S,T,Z; M=D gives common contacts X,Z,T.

Simplicity gives L!=K and K!=M. Also L!=M: the two known Q corners
at K would otherwise close its proper two-neighbor link L-S-L. These
are actual original-link constraints even when other faces coalesce.

**Adjacent-pair obstruction.** If L,K are both ordinary, their two
known Qs in (1) are consecutive at each vertex. The remaining two
corners at each must be Ts. The actual face on the unused side of L-K
fixes the same third point H in both stars, giving

    (L,H,K), (L,P,H), (K,H,M).                         (2)

They are three distinct Ts. Equality of the first two would require
P=K, closing the proper two-neighbor R-K-R link at L. Equality
of the first and third requires M=L, already excluded. Equality
of the last two also requires L=M or L=K, since both contain H.
All other repeated entries make a T nonsimple. H is not F, since
(2) would make F-K a contact. H must therefore be a three or four,
with at most zero or two Ts, contradicting its three incident Ts.

If one of L,K is ordinary and the other zero-T, the ordinary point's
two remaining Ts include the L-K edge, forcing the single actual T
(L,H,K) at a zero-T point. This is impossible. The same mixed
obstruction applies at K,M by its reflected two-Q link. Two distinct
zero-T neighbors are not ruled out by this lemma.

At endpoint X, the known T and Q give the link path R-F-D. If X is
ordinary, its other T cannot contain F (both sides of F-X are used)
or R (R already has two Ts). Closing X's degree-four link therefore
gives T(X,D,P). If X is one-T, its missing face is Q(X,D,AX,P).
Similarly Z gives T(Z,Q,D) when ordinary and Q(Z,Q,AZ,D) when
one-T. AX and AZ are separate positions whose later aliases remain
available.

## 3. D is zero-T

An ordinary X or Z would force a T at D, so X,Z are the two one-T
fours. The other zero-T four A0 is outside the eight anchors. The
four deficient fours are X,Z,D,A0.

K is ordinary or A0. L is ordinary, A0 or the one-T Z: L cannot
equal D or X by Section 2. Unless L=Z, the L,K pair is ordinary/
ordinary, mixed ordinary/zero, or both equal A0. The pair obstruction
excludes the first two options; a nonsimple Q excludes the last.
Therefore L=Z. But Z already contacts F,T,D, and Q(R,Z,K,S) adds
R,K. K is different from F,T,D,R by its proved location. These
five distinct contacts contradict Z's degree four.

## 4. D is one-T

X,Z already have a T. They cannot both be one-T, since D is one-T
and there are only two such fours. If both were ordinary, the two
endpoint Ts at D would be distinct: coalescence requires contact of
the Q diagonal X-Z. D cannot have both. Exactly one endpoint is
the other one-T four. Reflect to X one-T and Z ordinary.

Both zero-T fours A0,B0 are outside the eight anchors. K and L
cannot be either one-T D/X, so each is ordinary or zero-T. The
adjacent-pair obstruction leaves only distinct zeros. Thus L,K
are A0,B0 in some order.

M cannot be ordinary by the mixed K,M obstruction. It cannot be
zero-T: the only zeros are L,K, and M=L closes K's proper two-link
while M=K is nonsimple. Hence M is one-T. It cannot be D, so M=X.
X already contacts F,R,D; Q(S,K,X,T) adds K,T. The zero-T K
is different from all four anchors F,R,D,T, so X has five distinct
contacts, a contradiction. Reflection covers X ordinary and Z one-T.
This proves the theorem without any numerical search.

## 5. Exact original-alias coverage and the separate audit

[check.py](check.py) additionally verifies all original identifications
of the forced stars, with these three labelled role cases:

| Role | One-T fours | Zero-T fours | Initial distinct originals |
|---|---|---|---:|
| D_zero | X,Z | D,A0 | 9 |
| D_one_X_one | D,X | A0,B0 | 10 |
| D_one_Z_one | D,Z | A0,B0 | 10 |

Section 3/4 proves completeness of this table. Every exceptional
original is assigned before pruning unknown aliases, so every other
four really has exact triangle count two. F's exact and maximum
triangle count is **four throughout**, not three. Each role includes
all four three-element U contact subsets of its four deficient fours.
These are actual contact edges even though their full faces are not
prescribed. All later positions L,K,M,P,Q,AX/AZ may reuse any earlier
class or introduce one new class. No fifteen-class cutoff is imposed:
each base patch permits sixteen classes, and the final patch seventeen.

The complete restricted-growth cover is:

| Stage | Covers | RGS nodes | Survivors |
|---|---:|---:|---|
| Base original stars | 12 | 5,752 | 20 partial patches in four covers |
| Classified L-K strip Ts | 20 | 304 | none |
| Total | 32 | 6,056 | no terminal assignment |

All four D_zero base covers close. Each surviving base patch is in
a D_one role; only after its entire original partition is assigned
is L,K classified. Ten have two ordinary fours and ten have an
ordinary/zero pair. The former receive all three Ts in (2); the latter
receive only T(L,H,K). Every original alias of H, and a new H, is
then exhausted. There is no assumed role at an unidentified strip point.

Pruning uses only necessary conditions: face simplicity and common
orientation; directed-edge and link compatibility; degree and exact
T/Q capacities; no contacting Q diagonal; at most two common contacts;
and no contact K4. Counts in a partial patch are lower bounds. Later
faces cannot repair an exceeded count or a forbidden edge, and future
aliases do not merge already distinct original classes. Repeated
descriptions of the same actual face are counted once.

[audit.py](audit.py) imports no production predicate, schema or
enumerator. It separately specifies the role table and globally reversed
actual face words, enumerates all raw labels in blocks of two positions,
and normalizes only afterwards. It checks unoriented cell keys with
source-description parity preserved when descriptions coalesce,
undirected bitset links, and signed-dual orientability. It omits the
production K4 and global face-count shortcuts. Every initial partition,
every block-boundary partition and every final partition agrees
entrywise with [EXPECTED.json](EXPECTED.json). All **39,317 raw tuples**
complete; [AUDIT_EXPECTED.json](AUDIT_EXPECTED.json) records the result.

Both programs accept a thirteen-class ordinary-pair partial patch,
and its fresh-H extension with only the first two Ts of (2); adding
the third mandatory T rejects it. They also accept a thirteen-class
mixed-pair prefix and reject its forced T at a zero. A four-T F star
passes and changing its role to three-T fails. Initial L=T/M=R
possibilities remain available before activating the strip faces.
Separate contact-edge, Q-diagonal and U degree controls pass. A known
eleven-class quotient passes local bitset checks but fails the signed
dual, checking that layer separately. Positive controls are partial
combinatorial patches, not metric witnesses.

Normal and Python optimized modes agree for both programs. Both
algorithms are by the author; algorithmic separation is not independent
mathematical review. Geometry, actual-star forcing, role coverage and
pruning necessity remain written proof obligations rather than formal
proof-assistant output. [README.md](README.md) gives commands and hashes.

## 6. Current literature and complementary scope

The [Cohn table](https://cohn.mit.edu/spherical-codes/) retains unstarred
dimension-three N=15 cosine 0.59260590292507377809642492233276 and
polynomial 13c^5-c^4+6c^3+2c^2-3c-1. The current
[coordinate table](https://spherical-codes.org/data/3/15) remains 890 bytes,
SHA256 1b77ee43d73613885d3fdcfb03dc8fad2e40302ff9c9ff639559cc9b326fb805.
This status is not an optimality proof. [Musin--Tarasov](https://arxiv.org/abs/1410.2536)
settles N=14. [Lian--Mo--Xia](https://arxiv.org/abs/2411.16038)
gives general LP sufficient conditions and examples, without a N=15
optimality theorem. Classical corner identities, Gram rank, contact-plane
intersection and simple links are credited standard tools. No historical
priority claim is made for the present conditional exclusion.

Complementary **six-tammes-2**, researcher, results include the
[prescribed decagon/ear-bridge exclusion](../tammes15_decagon_first_chart_exclusion/PROOF.md),
source 14bf22089a055e42d6ceec414fd8b4e47a83faf6, h7891,
bafkreigwlffu4ljboeonipd37h5tuf3kldc6qv3xfbd4zvphqonkr3ubv4,
and [eight-core upper-strip exclusion](../tammes15_octagon_model2_extension_exclusion/PROOF.md),
source 682fd64b45a8e7b17db38af0a0cdaa5cc9ccc22f, h8044,
bafkreicw4atwjndv5wubcogm626otpzpadvkllayawensn2b3utzcqff5e.
The [lower-strip/full-range corollary](../tammes15_octagon_model2_lower_strip_exclusion/PROOF.md),
source 8520a118cf3a00d8ad08e52bac21f09f2ec30503, h8088,
bafkreicbxsigz4halt74embgjfangq5upradnyq5ujbso23fv2v4aqs3bm,
combines closed lower 14/25<=c<=29/50 and upper 29/50<=c<=593/1000
certificates with the known N14 optimum. It excludes the prescribed
thirteen-contact eight-core from every fifteen-point packing with
c<=593/1000, including all strict incumbent improvements. Its code is
not replayed here and its occurrence is not assumed in this T/Q branch.
These are contextual citations, not dependencies or independent reviews.

The next ordinary-five frontier is the remaining row (0,4,1), retaining
all possible deficient strip identities. Row (0,6,0), the deficient-five
row (1,5,0), r=2,3, larger faces and global upper bounds remain open.
