# Excluding the (1,3,1) single-three profile in the nine-Q Tammes-15 branch

Author: **six-tammes-1**, role: **researcher**, 2026-09-30.
Status: complete conditional written proof with exact original-face alias
covers and a separate same-author audit. Independent mathematical review
and formalization are pending.

## Statement and scope

Let fifteen distinct unit points have minimum geodesic separation d and
c=cos(d), with **1/2<c<3/5**. Assume their **complete** contact graph is
connected, has degrees 3,4,5, and its minor geodesic edges form a cellular
sphere decomposition into simple strictly convex geodesic triangles T and
quadrilaterals Q, each contained in an open hemisphere. Assume exactly
nine Q faces and exactly one degree-three vertex U.

Euler and the degree sum give eight Ts, thirty edges, thirteen degree-four
vertices, and one degree-five vertex F. Let t(v) count incident Ts, let
delta=4-t(F), and let a,b count degree-four vertices with t=1,0,
respectively. The profile

    (delta,a,b)=(1,3,1)

is impossible. The new argument below excludes **F-U noncontact**.
The [previous contact exclusion](../tammes15_delta_one_contact_exclusion/PROOF.md),
verified source 533d295e875be49fe6b16ec736bcb5ff4a303d28, committed
h8054, bafkreif42cz7msxygskgu25pd2zzi2yvunywppxz4seoqvbe6r3qqsghti,
excludes F-U contact under exactly these hypotheses. Combining the two
therefore excludes the whole count row.

The [preceding five-profile reduction](../tammes15_unique_three_deficit_two_exclusion/PROOF.md),
original source 1ee0a05f438bbb5aef81e2d6cde0f1739d8bfbb1, corrected
exposition 7534341f913f641497fa57834077d34984c53eb8, committed h7986,
bafkreiejoywl27drbyso6ozgpuxymbn2yu7bu3oujtgh3irplrc5r5spri,
thus leaves **four necessary r=1 count profiles** on the full open interval:

| delta | a | b |
|---:|---:|---:|
| 0 | 6 | 0 |
| 0 | 4 | 1 |
| 0 | 2 | 2 |
| 1 | 5 | 0 |

On 1/2<c<beta, where beta is the unique root in (119/200,3/5) of

    1+4c+2c^2-4c^3-11c^4-24c^5,

the [older odd-degree cover](../tammes15_nine_quad_odd_degree_reduction/PROOF.md),
source d6547391ae745a70087f067568047c8dbba0e099, committed h7817,
bafkreic6shrttfdlf7vbae5wye7eytruyxeeb7j6422ubytjcwlaadlkfa,
now has 27 necessary profiles: 4,12,11 for r=n3=n5 equal to 1,2,3.
The twelve and eleven rows are imported unchanged. Count rows are not
complete contact maps, realized packings, or a census of global optimizers.
Unrestricted Tammes-15 bounds and optimality are unchanged.

## 1. Geometric and local-star inputs

We use the full-interval angle facts and endpoint rule from the
[single-three fan proof](../tammes15_nine_quad_single_three_fan_reduction/PROOF.md),
source 276ec8b0508c7960aa73517f3b7e6e0ef03ca3cf, committed h7912,
bafkreicjxhbyqcxdeplfvby6k2bysmhhk7fbksapoenneqsigtfos2dulu.
Its metric three-T collar is needed by the earlier contact exclusion,
but is not used in the new noncontact argument.

Write alpha=acos(c/(1+c)), phi=2pi-4alpha, and
rho(u)=2atan(1/(c tan(u/2))). Every T corner is alpha; opposite Q
corners are equal and adjacent ones are related by rho. Every Q corner
is strictly between alpha and 2alpha, because its diagonal is not a
contact. These identities are classical; see
[Musin--Tarasov, Proposition 3.2](https://arxiv.org/abs/1410.2536)
and the [geometric audit](../tammes_15_triangle_quad_exclusion_review1/README.md),
source f026ccec6854eb913e5c156f4ff0cf08ed5cb4a9, h7182,
bafkreiflxdrel4fv4opchhucsisp7ylw2lsfgtrv4q7tya3o5vjh4ld53a.

On the full interval, threes have no Ts, fours have at most two, and
fives have at most four. A three contacts only vertices of positive
triangle deficit, namely t<2 at a four or t<4 at a five. To recall
the angle comparison, put A=2pi-2alpha and b0=2atan(1/sqrt(c)).
At a three, two adjacent Q corners u,v have u+v>A. Their neighbor
receives rho(u),rho(v), with sum less than 4b0-A<A. This excludes an
ordinary two-T four, another three, or an ordinary four-T five.

Two consecutive Q sectors at a deficient five force their shared
neighbor to be a three. Indeed both received corners exceed rho(phi),
and rho(phi)>pi-alpha; a vertex of degree at least four cannot have
two such corners. This capacity and its strict inequalities are in the
[ordinary-five corner proof](../tammes15_eight_quad_reduction/FIVE_CORNER_CAPACITY.md),
source 9f43d6fdac0c7b0e0333c527c739cb0c24c68afb, h7444,
bafkreiasa2n2mywlaokeron7wkpsj4z2ows4asfkm5fbnf6gphzbgmtvba.
Consequently, when F has three Ts and does not contact the unique U,
its two Q sectors are separated. Its T sectors split into a two-T fan
and an isolated T.

If an ordinary four is an endpoint of a T fan and the next fan vertex
already has two Ts, its second T uses the adjoining Q opposite of F.
The two occupied sides of its F edge and the saturated next fan vertex
leave precisely that free T sector. In particular that Q opposite has
a T. We use this endpoint rule only for the two-T fan.

Two distinct unit points have at most two common contact neighbors:
their affine contact planes intersect in a line with at most two unit
points. Antipodal points have none since c>0. Four pairwise contacting
points are impossible: their Gram matrix has eigenvalues 1-c and 1+3c
and rank four. A complete contact edge cannot be a Q diagonal.

At any vertex the link of incident faces is one simple cycle whose
length is its degree. A proper closed subcycle, an incompatible
successor, a repeated directed boundary edge, or too many contacts is
impossible. If three consecutive corners at a four have link path
p,q,r,s, those four neighbors must be distinct, and its last face
closes the path. If an identification closed a two- or three-neighbor
cycle, degree four would already be impossible. The fourth face is a
T or Q according to the vertex's remaining exact triangle count.
These are statements about the original embedded faces, rather than
separately normalized drawings.

## 2. The original noncontact star

Assume now F does not contact U. Choose a common orientation of the
sphere. The following nine anchors are distinct:

    F,U,X,R,S,V,W,B,C.

F's cyclic neighbors are X,R,S,V,W, and its actual faces are

    Ts: (F,X,R), (F,R,S), (F,V,W);
    Qs: (F,S,B,V), (F,W,C,X).

The small Q opposites B,C are deficient fours and are noncontacts of F.
They cannot be U: their corner equals F's small corner, whereas a Q
corner at a three is large. They are distinct because the same
opposite pair F,B cannot support two different strictly convex Q
cells. F's neighbors are distinct actual contacts; neither B nor C
is among them. U is not a neighbor of F. This proves the nine-anchor
statement without inventing nine independent coordinates.

R already has two Ts and is an ordinary four. Its fourth contact L
and the Q opposites P,Q give the forced faces

    (R,L,Q,S), (R,X,P,L).

L may initially equal V or W. No exclusion of those aliases from the
earlier contact-strip argument is imported.

At X and S the endpoint rule and the degree-four link give:

| Vertex role | Forced last endpoint face |
|---|---|
| X ordinary | T(X,C,P) |
| X one-T | Q(X,C,AX,P) |
| S ordinary | T(S,Q,B) |
| S one-T | Q(S,Q,AS,B) |

AX and AS are separate face positions. They can coincide later only
through an allowed original alias.

At V and W, an ordinary four's second T either shares the V-W edge,
or uses V-B and W-C, respectively. If it shares V-W, both V,W are
ordinary and the actual paired faces are

    T(W,V,H), Q(V,B,M,H), Q(W,H,N,C).                 (1)

Otherwise every ordinary V requires T(V,B,JV), and every ordinary W
requires T(W,JW,C). A one-T V or W cannot be in the paired second T.
These possibilities exhaust the two free sectors in their four-links.

In the paired case H is outside the nine anchors. H=F would repeat
the original T across V-W with reverse orientation, requiring its
complementary nonhemispherical region as a second convex T cell.
H=U gives a T at U. H=X,S,R gives five contacts at that four:
respectively F,R,C,V,W; F,R,B,V,W; F,X,S,V,W.
H=B gives F,B common contacts S,V,W, and H=C gives F,C contacts
X,W,V. H=V,W makes a nonsimple T.

If S is ordinary, B's known neighbors are S,V,Q,M, with Q in its
endpoint T. Thus U-B implies M=U. If X is ordinary, similarly U-C
implies N=U. If X is one-T and C is one-T, three Q corners force
T(C,N,AX), so neither N nor AX is U and U-C is absent. The reflected
statement holds for one-T S and one-T B.

The remaining forced B,C faces in a paired case are exactly:

| Roles | Forced fourth face |
|---|---|
| B one-T, S ordinary | Q(B,Q,JB,M) |
| B one-T, S one-T | T(B,AS,M) |
| B zero-T, S one-T | Q(B,AS,JB,M) |
| C one-T, X ordinary | Q(C,N,KC,P) |
| C one-T, X one-T | T(C,N,AX) |
| C zero-T, X one-T | Q(C,N,KC,AX) |

They close the known three-corner paths. Any repeated neighbor or
coalescence that would shorten those paths closes a proper link and
is already impossible. All later positions L,P,Q,AX,AS,H,M,N,JB,KC
retain every original alias not excluded by these necessities.

## 3. Both B,C one-T

The other deficient fours are a one-T E and a zero-T Z0. Z0 is outside
all nine anchors, since F's five neighbors each have a T, and B,C have
one. E is X,S,V,W, or outside the nine anchors; R already has two Ts.
U must contact three of the four deficient fours B,C,E,Z0.

If E=V, ordinary W cannot pair its second T with one-T V. It needs
its W-C T. Ordinary X already gives C its sole T; the two cannot
coalesce because X-W is the noncontact Q diagonal. E=W is reflected.
Thus V,W are ordinary in the remaining cases. They must pair: a
separate V-B T conflicts with ordinary S's sole T at B, or a separate
W-C T conflicts with ordinary X's sole T at C. The coalescences would
force the respective Q diagonals S-V or X-W to be contacts.

If E=X, S is ordinary. U-C is absent by T(C,N,AX). U-B would force
M=U and hence U-H in (1). H has a T and is outside the anchors, but
the only deficient four there is zero-T Z0. This contradicts the
three's neighbor restriction. U has only E,Z0 available, fewer than
three contacts. E=S is reflected.

It remains that E is outside the anchors. Both endpoints are ordinary.
U contacts B or C because E,Z0 alone are insufficient. Reflect so
U-B. Then M=U, and U-H forces H=E, since H is outside the anchors
and has a T. If U-C too, N=U and the three known H corners close
its proper three-neighbor link V-W-U. Hence U-C is absent, and U's
complete contact set is B,E,Z0.

At H=E the missing fourth face is Q(H,U,JH,N). JH is a contact of U.
It cannot be H (nonsimple face), nor B (a proper two-neighbor U link
with Q(V,B,U,H)). Hence JH=Z0 and

    Q(H,U,Z0,N)                                             (2)

is forced.

N is ordinary. It differs from H,C,Z0 by the two Q simplicities,
from U by U-C absence, and from F because W-F would be a contact
diagonal of Q(W,H,N,C). It cannot be B: B already has four distinct
contacts S,V,Q,U; Q cannot equal C because S-C would give F,C the
three common contacts X,W,S. N=B would therefore add a fifth B
contact through N-C. These exclusions remove F,U and every deficient
four B,C,E=H,Z0, so N is an ordinary two-T four.

The two Qs at N in (1),(2) give link path Z0,H,C. Its two remaining
faces must be Ts, including one incident to Z0, contrary to t(Z0)=0.
This proves the case. The exact checker instead completes C's mandatory
Q from the table and rejects the same prefix by link or Q capacity;
it does not assign N an ordinary role by assumption.

## 4. B zero-T and C one-T

Reflection covers the reversed roles separately in the finite audit.
The endpoint rule makes S one-T. The third one-T E is X,V,W, or
outside the anchors.

If E=W, ordinary V can neither pair with W nor put a T at B.
If E=V, X,W are ordinary and W's separate C triangle conflicts with
ordinary X's sole C triangle, since X-W is a Q diagonal. Thus V,W
are ordinary and must pair, and E is X or outside.

The zero-T B has neighbors S,V,AS,M. U-B means AS=U or M=U.

If E=X, both X,S are one-T. T(C,N,AX) prevents U-C. M=U would
force U-H, but there is no deficient four with a T outside the
anchors. AS=U would make Q a contact of U through Q(S,Q,U,B).
The allowable deficient contacts are B,C,S,X. Q=B,S is nonsimple;
Q=C gives F,C common contacts X,W,S; Q=X makes the existing R-X
contact a diagonal of Q(R,L,X,S). All are impossible. Therefore
U-B also is absent, leaving only S,X for three required neighbors.

Suppose E is outside the anchors. X is ordinary; U-C means N=U and
then U-H forces H=E. U must contact at least one of B,C because
only S,E are otherwise available.

If U-B via AS=U, Q is a contact of U. Among B,C,S,E only E is possible:
Q=B,S is nonsimple and Q=C gives the above three-common-contact
contradiction. Thus Q=E. S's full contacts F,R,B,E exclude U, so
U must also contact C, giving N=U and H=E. Now E contacts
V,W,U,S,M. M is not V by Q simplicity, W by the F,B common contacts
S,V,W, or S by a proper two-neighbor B link. M=U closes B's known
three-neighbor link S,V,U, contradicting degree four. Thus E has
five distinct contacts, impossible.

If U-B via M=U, H=E. U-C would give N=U and a proper three-neighbor
H link, so U-C is absent. U's full contacts are B,E,S.
S's fourth neighbor Q must therefore be U. Q(R,L,U,S) makes L a
contact of U. L is neither S nor B: L=S makes the Q nonsimple;
L=B gives F,B common contacts S,V,R. Hence L=E. E contacts
V,W,U,R,N. N cannot be W by Q simplicity, U by the just-excluded
proper link, or V,R by the F,C common contacts X,W,N. The five
contacts are distinct, again impossible.

Finally cover U-B absent, without using the invalid reflection that
would interchange a zero and a one. U's full contacts must be C,S,E.
N=U and H=E, while U-S gives Q=U. Q(R,L,U,S) forces L to be E:
L=S is nonsimple and L=C gives F,C common contacts X,W,R.
Now E contacts V,W,U,R,M. M is not V by simplicity, W or R by the
F,B common contacts S,V,M, or U because U-B is absent. This is
again five distinct contacts. These cases exhaust the noncontact row.

## 5. Exact finite coverage and completeness

[check.py](check.py) enumerates all thirteen labelled role cases:

| B,C roles | Possible additional one-T E | Additional zero |
|---|---|---|
| one,one | X,S,V,W,outside | outside Z0 |
| zero,one | X,V,W,outside; S is one | B |
| one,zero | S,V,W,outside; X is one | C |

For each, U's three-element contact set is each of the four subsets
of its four deficient fours. These are added as actual contact edges,
without inventing their faces. Every additional deficient original is
assigned **before** pruning later aliases. Outside E or Z0 is distinct
from the nine anchors and from the other deficient originals by the
role classification. All later names can reuse any earlier actual class
or introduce one new class, via a complete restricted-growth-string
enumeration. No fifteen-class cutoff is used; even twenty classes are
permitted in the largest final patch.

The complete finite cover is:

| Stage | Labelled covers | RGS nodes | Full survivors |
|---|---:|---:|---:|
| Unpaired isolated edge | 52 | 7,854 | 0 |
| Paired, completed B,C stars | 28 | 6,316 | 4 partial assignments in two covers |
| Forced final H quadrilateral | 2 | 1,438 | 0 |
| Total | 82 | 15,608 | 0 terminal assignments |

The paired basic survivors occur only when both B,C are one-T, E is
outside, and U's contacts are B,E,Z0 or C,E,Z0. All four original
assignments have H=E. The final-Q stage is invoked only after the
entire preceding alias cover has established that classifier; it does
not impose a one-T role at an unclassified H.

One representative partial assignment, in the nineteen-position order

    F,U,X,R,S,V,W,B,C,E,Z0,L,P,Q,H,M,N,JB,KC,

is

    0,1,2,3,4,5,6,7,8,9,10,11,12,13,9,1,14,10,10.

It has fifteen actual classes and passes every local necessary check.
The other assignment on that side has KC a new class 15. Reflected
assignments interchange the U positions at M,N and the last two
opposites. These are partial combinatorial patches, not metric witnesses.
They are accepted as positive controls, preventing a false claim that
the uncompleted paired patch already excludes fifteen points.

Pruning uses only necessary conditions: nonsimple or reversed faces;
consistent coalescence of repeated descriptions of one actual face;
directed-edge and link compatibility; exact degree and T/Q capacities;
contacts on Q diagonals; at most two common contacts; and the impossible
contact K4. Face counts and missing neighbors are lower bounds in a
partial patch. Once exceeded, adding further actual faces or aliases
cannot repair them; both endpoints of any counted constraint have
already been assigned. The early assignment of every exceptional
original makes default ordinary roles sound under every later alias.

[audit.py](audit.py) imports no production schema, predicate or enumerator.
It specifies a separate explicit role table and globally reversed source
face words, enumerates exhaustive raw labels in blocks of two positions,
normalizes only afterwards, and checks unoriented cell keys, undirected
bitset links, and signed-dual orientability. When descriptions of one
unoriented cell coalesce, their orientation parity must agree: opposite
sides of the same convex hemispherical cell cannot be identified.
No production K4 or global face-count shortcut is used.

All **68,306 raw tuples** complete. Every initial partition, every
two-position block-boundary partition, and every final partition matches
[EXPECTED.json](EXPECTED.json) entrywise. [AUDIT_EXPECTED.json](AUDIT_EXPECTED.json)
records the separate result. Both normal and Python optimized modes
agree. Positive fifteen-/sixteen-class partial patches, initially allowed
L=V/W aliases, and separate-contact-edge controls pass; all sixteen
extensions of the positive patch by its forced final Q reject. A known
eleven-class quotient passes the local bitset conditions but fails the
signed dual, checking the orientability layer.

The written bridges from geometry to these actual oriented faces,
anchor distinctness, role coverage, face forcing, and pruning necessity
remain unformalized. Both programs are by this author. Neither constitutes
an independent mathematical review or proves global optimizer coverage.

## 6. Reproduction, literature and complementary scope

[README.md](README.md) gives exact standard-library commands and hashes.
No floating arithmetic, solver, CAS, external private input, or omitted
large certificate is required. The two small fixtures preserve all
boundary partitions for direct comparison.

The current primary [Cohn spherical-code table](https://cohn.mit.edu/spherical-codes/)
retains unstarred dimension-three N=15 cosine
0.59260590292507377809642492233276, with polynomial
13c^5-c^4+6c^3+2c^2-3c-1. The
[coordinate table](https://spherical-codes.org/data/3/15) is unchanged,
890 bytes, SHA256
1b77ee43d73613885d3fdcfb03dc8fad2e40302ff9c9ff639559cc9b326fb805.
These are status context, not a proof of global optimality.
[Musin--Tarasov](https://arxiv.org/abs/1410.2536) solves N=14.
[Lian--Mo--Xia](https://arxiv.org/abs/2411.16038) gives general LP
sufficient conditions and examples, not a fifteen-point theorem.
The corner identities, contact-plane intersection argument, link
topology, and restricted-growth enumeration are credited standard tools.
No historical priority claim is made for the new conditional row exclusion.

Complementary work by **six-tammes-2**, researcher, includes the
[prescribed-decagon/ear-bridge theorem](../tammes15_decagon_first_chart_exclusion/PROOF.md),
source 14bf22089a055e42d6ceec414fd8b4e47a83faf6, h7891,
bafkreigwlffu4ljboeonipd37h5tuf3kldc6qv3xfbd4zvphqonkr3ubv4,
and the [eight-core extension exclusion](../tammes15_octagon_model2_extension_exclusion/PROOF.md),
source 682fd64b45a8e7b17db38af0a0cdaa5cc9ccc22f, h8044,
bafkreicw4atwjndv5wubcogm626otpzpadvkllayawensn2b3utzcqff5e.
The latter applies to thirteen prescribed contacts among eight points
and at most six arbitrary extras on closed 29/50<=c<=593/1000.
Its published proof and reproduction instructions were read, but its
checker was not rerun and its contact pattern is not assumed to occur
in this T/Q branch. These are citations, not dependencies or reviews.

A newly committed [lower-strip and full-range corollary](../tammes15_octagon_model2_lower_strip_exclusion/PROOF.md),
verified source 8520a118cf3a00d8ad08e52bac21f09f2ec30503, h8088,
bafkreicbxsigz4halt74embgjfangq5upradnyq5ujbso23fv2v4aqs3bm,
adds closed 14/25<=c<=29/50 coverage. With h8044 and the published N14
optimum it excludes that same prescribed eight-core in every fifteen-point
packing with c<=593/1000, including every strict improvement of the
incumbent. Its committed proof and source reproduction instructions were
read. Its checker was not replayed and no occurrence of that pattern is
inferred in the present face structures. This is additional complementary
context, not a dependency or an independent review.

The next local frontier is the remaining ordinary-five row (0,2,2),
starting with its zero-T Q opposite. The other three retained rows,
r=2,3, larger faces, and the unrestricted numerical bound remain open.
