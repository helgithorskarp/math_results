# Tammes-15: exclude the ordinary-five profile (0,6,0)

Author: **six-tammes-1**, role: **researcher**, 2026-10-01.
Status: complete author-checked conditional geometric reduction, exact
original-face cover and metric exclusions, with a separate exhaustive
algorithm and separate rational arithmetic. The geometric and analytic
bridges below are written and unformalized. Independent mathematical review
is pending; shared team signatures do not establish separate authorship.

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

**Theorem. The profile (delta,a,b)=(0,6,0) is impossible.**

The proof covers every identification of original face positions in an
actual fifteen-point packing. Its finite cover gives two closed
combinatorial maps. Neither is a spherical packing: Sections 6--8 exclude
both by exact angle inequalities, using the known fourteen-point optimum
only to bound c from below.

The preceding [two-profile theorem](../tammes15_ordinary_five_four_one_exclusion/PROOF.md),
source b1a8438ea86ed00717e237dd001e1925700652ab, committed h8180,
bafkreifmdfpbofpiirf42ymhcdl24kddnc3nu34u6wmrx4z7fbgkwzjnkm,
therefore leaves **one necessary single-three count profile**, (1,5,0),
on the full open interval. On 1/2<c<beta, where beta is the unique root
in (119/200,3/5) of

    1+4c+2c^2-4c^3-11c^4-24c^5,

the [older odd-degree cover](../tammes15_nine_quad_odd_degree_reduction/PROOF.md),
source d6547391ae745a70087f067568047c8dbba0e099, h7817,
bafkreic6shrttfdlf7vbae5wye7eytruyxeeb7j6422ubytjcwlaadlkfa,
has **24 necessary count profiles, 1/12/11 for r=n3=n5=1/2/3**.
The r=2,3 rows are imported unchanged. Counts are not complete contact
maps, realized packings or a census of global optimizers. Unrestricted
Tammes-15 numerical bounds and optimality are unchanged.

## 1. Geometric inputs

The [single-three fan reduction](../tammes15_nine_quad_single_three_fan_reduction/PROOF.md),
source 276ec8b0508c7960aa73517f3b7e6e0ef03ca3cf, h7912,
bafkreicjxhbyqcxdeplfvby6k2bysmhhk7fbksapoenneqsigtfos2dulu,
supplies full-interval angle and endpoint facts; its collar certificate is
not used. Put

    alpha=acos(c/(1+c)), phi=2pi-4alpha, A=2pi-2alpha,
    B=2pi-alpha, rho_c(u)=2atan(1/(c tan(u/2))).

A T corner is alpha. Opposite Q corners are equal and adjacent ones are
related by rho. Completeness, both noncontact Q diagonals and convexity
give **alpha<u<2alpha** for each Q corner. Classical corner identities
are in [Musin--Tarasov, Proposition 3.2](https://arxiv.org/abs/1410.2536)
and the [earlier geometric audit](../tammes_15_triangle_quad_exclusion_review1/README.md),
source f026ccec6854eb913e5c156f4ff0cf08ed5cb4a9, h7182,
bafkreiflxdrel4fv4opchhucsisp7ylw2lsfgtrv4q7tya3o5vjh4ld53a.
That earlier audit does not review this result. In particular rho(alpha)
=2alpha and rho(2alpha)=alpha.

Here pi/3<alpha<2pi/5. Angle sums force t(U)=0, t<=2 at a four,
and t<=4 at a five. A two-T four is called ordinary. An ordinary four's
two Q corners sum to A. Every Q corner at a three or ordinary four exceeds
phi, whereas the ordinary five's sole Q corner is exactly phi. Its
opposite is consequently a deficient four, rather than U or an ordinary
four. In this row there are six one-T fours and no zero-T four.

U contacts only deficient fours. Across a U edge its two Q corners u,v
satisfy u+v>A. The established inequality

    u+rho(u)<=2b0<A, b0=2atan(1/sqrt(c)),

implies rho(u)+rho(v)<4b0-A<A. An ordinary four on the other end of
that edge needs the received corners to sum to A, a contradiction.
Ordinary F has only one Q, whereas a U edge needs Qs on both sides.
The [ordinary-five corner capacity proof](../tammes15_eight_quad_reduction/FIVE_CORNER_CAPACITY.md),
source 9f43d6fdac0c7b0e0333c527c739cb0c24c68afb, h7444,
bafkreiasa2n2mywlaokeron7wkpsj4z2ows4asfkm5fbnf6gphzbgmtvba,
records these facts. Thus U's three distinct contacts lie among the six
one-T fours.

Two distinct points have at most two common contact neighbors: intersect
their two affine contact planes with the sphere. Antipodal points have
none because c>0. A contact K4 is impossible because its Gram matrix has
eigenvalues 1-c,1-c,1-c,1+3c and rank four. A complete contact cannot
be a Q diagonal. At every vertex, actual incident faces have one simple
cyclic link of length its degree. A proper closed sublink, incompatible
successor or predecessor, repeated oriented edge or excess contacts is
impossible. Descriptions of the same actual face coalesce and count once;
opposite orientations cannot describe one convex hemispherical cell.
All source face words follow one sphere orientation.

## 2. Four-T fan and the strip

Eight distinct anchors are

    F,U,X,R,S,T,Z,D.

T is also the name of an internal fan vertex. The ordinary-five star is

    (F,X,R),(F,R,S),(F,S,T),(F,T,Z),(F,Z,D,X).

D is the small-corner deficient-four opposite of F in its sole Q. It is
a noncontact of F and is distinct from U and all five contacts of F.
U is not a contact of F. These facts prove all anchor identities are distinct.

The internal ordinary fours R,S,T have fourth contacts L,K,M and
unknown Q opposites P,Q, forcing

    (R,L,K,S),(R,X,P,L),(S,K,M,T),(T,M,Q,Z).          (1)

Later positions may always reuse earlier actual vertices. K is not
F,R,S,T because it is S's fourth contact. K=X or K=Z gives a contact
K4, so F-K is absent. K is not U because S is ordinary, or D because
F,D would share X,Z,S. Likewise L and M are fours other than U,D:
L=D or M=D gives F,D three common contacts. L=T or M=R gives K4;
L=Z or M=X creates five endpoint contacts. Thus L,K,M are outside
the eight anchors. They are pairwise distinct: adjacent equality is
nonsimple, and L=M closes K's proper two-neighbor link. The source
nevertheless checks all these aliases, rather than hard-coding that
outside location at the unknown positions.

If a strip point is ordinary, the two remaining faces at it are

    L: (L,HL,K),(L,P,HL);
    K: (K,HK,M),(K,L,HK);
    M: (M,K,HM),(M,HM,Q).                            (2)

HL,HK,HM are separate positions, each retaining every original alias.
If L,K are both ordinary, the unused side of their common edge makes
HL=HK=H and forces three distinct Ts (L,H,K),(L,P,H),(K,H,M).
Coalescence of the first two requires P=K, closing L's proper two-link;
coalescence involving the third requires L=M or a nonsimple triangle.
H!=F since F-K is absent. Every other vertex supports at most two Ts,
so this is impossible. Reflection excludes ordinary K,M.

If L,M are ordinary and K is one-T, their two unused-side Ts at K must
coalesce or contradict t(K)=1. Coalescence forces T(L,K,M), which closes
K's proper three-neighbor link L-S-M-L, also impossible. Consequently
only the classified strip role sequences

    (1,1,1),(1,1,2),(1,2,1),(2,1,1)

are possible. The new check is imposed only after all L,K,M names have
been assigned. Before then every alias survives unless a prior necessary
constraint rejects it. These written local arguments are also present in
the [preceding original-face proof](../tammes15_ordinary_five_two_two_exclusion/PROOF.md),
source 639f1d7c63d6c02f9b40ce56b9efc0ad6f5edc6d, h8132,
bafkreifovwzx75mz2fcwrzkfq2sgxsp2l5ni7jypcyi5jx5gf6eykwh7qu.

At X the known faces form the link path D-F-R-P. Its missing face is
T(X,D,P) if ordinary, or Q(X,D,AX,P) if one-T. At Z it is T(Z,Q,D)
or Q(Z,Q,AZ,D). Both endpoints cannot be ordinary: their two forced
Ts at the one-T D are distinct, since coalescence would contact the
Q diagonal X-Z. Thus there are three labelled roles.

## 3. Complete original identities and the renaming reduction

| Role | One-T fours | Outside exceptional originals |
|---|---|---|
| D_one_X_one | D,X,E,G,B,C | E,G,B,C |
| D_one_Z_one | D,Z,E,G,B,C | E,G,B,C |
| D_one_both_one | D,X,Z,E,G,B | E,G,B |

All exceptional originals are assigned as distinct identities before
unknown aliases are pruned. Every other four therefore has exact t=2,
F has exact and maximum t=4, and U exact t=0 throughout. Each role
has twenty possible three-of-six U contact sets. These are actual edges;
no surrounding faces are guessed. Both endpoint reflections are explicit.

The free outside exceptional originals have no intrinsic order. Relabel
those contacted by U first, keeping D,X,Z and all anchors fixed. For
single-X and single-Z roles, this gives four representatives with weights
4,6,6,4: outside E,G,B; endpoint,E,G; D,E,G; endpoint,D,E.
For the both-one role the representatives and weights are

    EGB:1, XEG:3, ZEG:3, DEG:3,
    XZE:3, XDE:3, ZDE:3, XZD:1.

Thus **sixteen representative cases cover all sixty labelled cases**.
This is a relabelling of arbitrary exceptional point names, not a geometric
symmetry assumption. The audit explicitly checks a free-name bijection
for each of the sixty contact sets and every multiplicity.

Each base chart has eighteen positions: its eleven or twelve original
identities, L,K,M,P,Q, and the one or two required AX/AZ positions.
Restricted-growth enumeration allows each later position to equal any
previous class or to introduce one new class. At most fifteen actual
classes are retained, an explicit consequence of the fifteen-point
hypothesis. Earlier distinct classes cannot merge later. This cardinality
cut is new relative to the relaxed preceding-row cover; it is not a bound
on the number of face positions. Ordinary completion and last faces may
use twenty-two positions while representing at most fifteen points.

A one-T four with exactly two known Q corners has a three-neighbor link
path. Its unknown fourth neighbor lies on its remaining T. Hence it
cannot be U. An existing U edge must therefore occur among the three
known link neighbors. This rule is applied immediately after the base
chart, and again after later forced faces; it allows a known-Q U neighbor.

At an exact-role four with three actual corners, its simple four-neighbor
link path has one missing face. Closing its two endpoints forces a T if
one T remains, or a Q with one further aliasable opposite position if
none remains. The lowest-labelled eligible vertex is chosen. Closure
uses the original exact roles, and never presumes an ordinary role at a
name that has not been assigned. A closed star is not forced again.

All prefix constraints are necessary and monotone: face/contact counts
are lower bounds; an incompatible link, existing forbidden edge or excess
classes cannot be repaired by adding a later face. Repeated actual faces
are coalesced before counting. Exhaustion caps raise INCOMPLETE, not an
exclusion. The complete run stays below all caps.

## 4. Complete finite cover and the two maps

[check.py](check.py) imports a hash-guarded [prior public original-face kernel](../tammes15_ordinary_five_four_one_exclusion/check.py).
It adds the three role schemas, free-name representatives, fifteen-class
cut and early strip condition. The full representative cover is:

| Stage | Covers | RGS nodes | Partial or terminal survivors |
|---|---:|---:|---:|
| Original identities and U edges | 16 | 59,962 | 1,374 partial |
| Classified ordinary-strip completion | 96 | 1,376 | 80 partial |
| Forced last faces | 216 | 2,536 | 16 closed maps |
| Total | 328 | 63,874 | 2 map isomorphism classes |

Of the 1,374 base survivors, 1,278 reject by the early new-U rule, leaving
96 ordinary covers. There are eighty closure roots. **No open terminal
patch remains.** All sixteen terminal maps have fifteen vertices, thirty
edges, eight Ts and nine Qs, closed degree-correct links, and the required
six one-T fours. A smaller closed component would contradict connectedness;
none survives here.

[MAPS.json](MAPS.json) gives both complete canonical cell complexes,
including faces, edges and cyclic rotations. Their structural hashes are
SHA256 of compact sorted-key JSON containing those three arrays:

| Map | U | D | F-U distance | U-D edge | Representative terminal occurrences |
|---|---:|---:|---:|---|---:|
| M1, 9e75c890402048caf6dc42f456efc364be64daa9a33c646809f8f29d55b9fdfa | 6 | 7 | 2 | no | 8 |
| M2, cde759765dedf9a482dc6bc05de9f8219240108e73a636e78043d44264691df5 | 13 | 7 | 3 | yes | 8 |

F=0 and its sole Q is (0,2,7,1) in both. Production canonicalization
starts at this unique Q and breadth-first traverses cyclic links in both
global orientations. The separate audit instead finds explicit graph and
unoriented cyclic-cell isomorphisms by backtracking. The F-U distance
shows the two maps are nonisomorphic even as abstract graphs. Map hashes
alone are not used to infer isomorphism or exhaustion.

Both closed maps are positive combinatorial controls and pass the necessary
checks; forcing F to have three Ts or assigning sixteen distinct points
rejects. A local strip prefix of types (2,1,2) passes the prior local
kernel and fails the new forced-strip condition. This separates the new
written obstruction from pre-existing bitset/link pruning. These positive
patches and maps are not metric witnesses.

## 5. Known fourteen-point lower bound for c

The **known** [Musin--Tarasov fourteen-point optimality theorem](https://arxiv.org/abs/1410.2536)
and the exact [maintained spherical-code table](https://cohn.mit.edu/spherical-codes/)
identify its cosine kappa as the positive root of

    g(c)=4c^4-2c^3+3c^2-1.

Here g'(c)=c[16(c-3/16)^2+87/16]>0 for c>0, and

    g(14/25)=-6661/390625<0,
    g(57/100)=663851/25000000>0.

Thus kappa>14/25. Deleting one point gives d15<=d14 and therefore
**every fifteen-point packing has c>=kappa>14/25**. This is prior global
mathematics, credited rather than claimed as a new bound. The same
comparison is written in the complementary [eight-core lower-strip proof](../tammes15_octagon_model2_lower_strip_exclusion/PROOF.md),
source 8520a118cf3a00d8ad08e52bac21f09f2ec30503, h8088,
bafkreicbxsigz4halt74embgjfangq5upradnyq5ujbso23fv2v4aqs3bm.
Its separate finite certificates and an occurrence premise are not imported.

## 6. Exclude M2 by concavity

At D=7 the sole-F-Q corner is phi and exactly one T contributes alpha.
The other two Q corners u,v are the D corners of the two faces sharing
the D-U edge, so u+v=2pi-phi-alpha=3alpha. At U, their adjacent
corners are rho(u),rho(v). U's third Q corner is less than 2alpha, hence

    rho(u)+rho(v)>A.

For 0<c<1 and 0<u<pi, with D0=cos^2(u/2)+c^2 sin^2(u/2),

    rho'_c(u)=-c/D0,
    rho''_c(u)=c(c^2-1)sin(u)/(2D0^2)<0.

Thus rho is concave, and rho(u)+rho(v)<=2rho(3alpha/2).
For **c>=14/25**, the latter is strictly less than A, as follows.
Put q=tan^2(alpha/4). Then

    c=(1-6q+q^2)/(8q),
    P(q)=q^4-10q^3+76q^2-38q+3.

The function c(q) decreases on 0<q<1, and
c(97/1000)=427409/776000<14/25, with difference 7151/776000.
Consequently q<97/1000<1/10. On 0<q<1/10,

    P'(q)<=4(1/10)^3+152(1/10)-38=-5699/250<0,
    P(97/1000)=20045799281/10^12>0.

So P(q)>0. Writing r=sqrt(q), the positive denominators in

    tan(alpha/2)=2r/(1-q),
    tan(3alpha/4)=r(3-q)/(1-3q)

show that P(q)>0 is equivalent to tan(alpha/2)<c tan(3alpha/4).
Because both comparison angles are in (0,pi/2), this is equivalent to
rho(3alpha/2)<pi-alpha=A/2. The required corner sum is therefore both
>A and <A, a contradiction. Section 5 supplies c>=14/25 for every
actual fifteen-point packing, excluding M2 over the full stated interval.

## 7. Exact M1 corner transfer and its incompatible equations

For M1 define

    psi=rho(phi), z0=psi, z_(j+1)=rho(A-z_j), j=0,1,2,3.

The ordinary stars at 2,3,4,5 and then 8,13,14 propagate the following
Q corners. Faces and corner vectors have the same cyclic order:

| Q face | Corner vector |
|---|---|
| (0,2,7,1) | (phi,psi,phi,psi) |
| (2,3,9,8) | (A-psi,z1,A-psi,z1) |
| (3,4,10,9) | (A-z1,z2,A-z1,z2) |
| (4,5,11,10) | (A-z2,z3,A-z2,z3) |
| (1,6,11,5) | (z4,A-z3,z4,A-z3) |
| (7,8,13,12) | (z2,A-z1,z2,A-z1) |
| (9,10,14,13) | (z3,A-z2,z3,A-z2) |
| (6,12,14,11) | (A-z3,z4,A-z3,z4) |
| (1,7,12,6) | (rho(x),x,rho(x),x) |

Production checks this table as formal linear corner expressions against
all nine actual Q faces, the ordinary angle sums, and U,D,X incidences.
The auditor derives the table separately from the seven ordinary stars,
using opposite-corner equality and formal rho pairs; it does not import
or read the production table. Their checks verify incidences, while the
trigonometric interpretation is the written bridge in Section 1.

At U=6 the three Q corners sum to 2pi, giving
x=2pi-2(A-z3)=2z3-phi. At the one-T D=7,
phi+alpha+z2+x=2pi, so

    z2+2z3=B.                                       (D)

At the one-T X=1 its angles give

    psi+z4+rho(x)=B.                                (X)

Combining (D) with x=2z3-phi gives x=3alpha-z2 and
A-z3=pi-x/2. In an actual packing **alpha<x<2alpha**. Thus (X) is

    psi+rho(pi-x/2)+rho(x)=B.                       (X')

We exclude both sides of **c0=57/100** by the exact endpoint signs in
Section 8. Rho decreases in both its angle and c. Alpha decreases with c,
whereas A,phi,B increase. Hence psi decreases. If c>=c0, induction
compares the recurrence at the actual c to its endpoint: z_j(c)<=z_j(c0)
implies A(c)-z_j(c)>=A(c0)-z_j(c0), and therefore
z_(j+1)(c)<=z_(j+1)(c0). All actual arguments are Q corners in (0,pi),
and all endpoint arguments are in (0,pi) by Section 8; no extension
through an inadmissible interval is assumed. The endpoint inequality

    z2(c0)+2z3(c0)<B(c0)

then gives z2+2z3<B, contradicting (D).

For 1/2<c<=c0, let f(x)=rho(pi-x/2)+rho(x). Both affine arguments
remain in (0,pi) for x in [alpha,2alpha], so f is concave. Its minimum
is at an endpoint. Since rho(alpha)=2alpha and rho(2alpha)=alpha,

    f(alpha)=2alpha+rho(pi-alpha/2),
    f(2alpha)=alpha+rho(pi-alpha).

Also |rho'|<=1/c, because D0>=c^2. The arguments differ by alpha/2,
so rho(pi-alpha)-rho(pi-alpha/2)<=alpha/(2c)<alpha. Thus
f(alpha)>f(2alpha) and f(x)>=alpha+rho(pi-alpha). Each of psi,
alpha and rho_c(pi-alpha) decreases with c; B increases. Section 8 gives

    psi(c0)+alpha(c0)+rho_c0(pi-alpha(c0))>B(c0).

Consequently the left side of (X') is strictly greater than B(c) when
c<=c0, another contradiction. Together the two cases exclude M1 on
the full open 1/2<c<3/5 interval without a floating-point angle decision.

## 8. Rational certificates for the M1 endpoint signs

At c0=57/100 set H=1+2c0=107/50 and h=sqrt(H)>0. The half-angle
identity is tan(alpha/2)=1/h. With a_j=h tan(z_j/2),

    a0=(H-c0^2)/(2c0^2),
    a_(j+1)=H(a_j-c0)/(c0(H+c0 a_j)).

The exact values are

    a0=18151/6498, a1=1969228/880479,
    a2=5953/3249, a3=87762898/58972599.

All a_j>c0, so every recurrence argument A-z_j lies in (0,pi) at
c0. All denominators are positive. The rational inequalities
H<a2^2<3H and H<a3^2<3H imply pi/2<z2,z3<2pi/3.
Thus (z2+2z3)/2 lies in (3pi/4,pi), while B/2 lies in (pi/2,pi),
where tangent is increasing. Set

    E=H-a3^2-2a2 a3,
    N=a2(H-a3^2)+2a3 H.

Then tan((z2+2z3)/2)=N/(hE), tan(B/2)=-1/h, and the exact signs

    E=-320432929472008631/57962790546913350<0,
    N+E=198953174499314672393/282481659730382211225>0

imply N/(hE)<-1/h. This proves the first strict endpoint inequality.

For the other inequality set b=1/c0 and R=H-a0 b. The half-angle
sum S/2 for S=psi+rho(pi-alpha) is
atan(a0/h)+atan(b/h), lying in (pi/2,pi) because

    R=-25561849/9259650<0.

Its tangent is h(a0+b)/R, and tan(A/2)=-h/c0. The exact sign

    c0(a0+b)+R=-6236197/37038600<0

therefore gives tan(S/2)>tan(A/2), hence S>A. This is equivalent to
psi+alpha+rho(pi-alpha)>B. Every branch and denominator sign used
in the angle comparisons is explicit; squaring occurs only for positive
half-angle quantities.

The checker recomputes these fractions and all four positive tangent-branch
margins with Fraction arithmetic. The auditor instead obtains the a_j by
powers of the rational projective matrix

    [[H,-H c0],[c0^2,c0 H]],

then separately verifies branches and endpoint signs. It also derives the
M2 polynomial coefficients by convolution and evaluates them by Horner's
rule. No approximate trigonometric evaluation, solver result or numerical
root finding contributes a sign decision. Combining Sections 4--8 proves
the theorem.

## 9. Separate exhaustion audit and trust boundary

[audit.py](audit.py) imports only the hash-guarded [prior public separate audit](../tammes15_ordinary_five_four_one_exclusion/audit.py),
never production predicates, schemas, enumeration, face forcing or
canonicalization. It manually writes the three roles, sixteen representatives
and reversed face words; generates U sets by their omitted triples; and
uses raw labels, independent normalization, unoriented cyclic cells,
bitset links, orientation parity and a signed dual. The classified strip
condition is independently stated as logical cases, rather than reading
the production tuple table. The production K4 and global face-count
shortcuts are omitted.

At every forcing step the missing face is independently sewn between
endpoints of an unoriented link using the actual directed boundary arcs.
The complete separate cover checks **76,740 raw assignments** and
**668 initial, every-depth, suffix and final partition boundaries entrywise**.
All sixteen base covers, ninety-six ordinary covers, eighty closure roots,
216 last-face covers and 1,278 early U obstructions are accounted for.
All sixteen terminal maps have explicit independently found cell
isomorphisms, using 272 backtracking nodes altogether, with eight occurrences
of each map. Closed links, edge-two incidences, cyclic rotations and
Euler characteristic two certify the displayed orientable sphere complexes.
Matching aggregate counts alone is not the certificate.

[EXPECTED.json](EXPECTED.json) and [AUDIT_EXPECTED.json](AUDIT_EXPECTED.json)
are compact complete summaries. The source regenerates the deterministic
partition trace, checks its recorded SHA256 and byte size, and the auditor
compares each exhaustion boundary. The large trace is deliberately omitted
from publication. Its hash is in the compact fixture; it is not an external
private input. The audit reconstructs the full domain rather than trusting
a supplied survivor list.

An initial sixty-case pilot reached its unchanged forty-five-second guard
and supplied **no mathematical exclusion**. The sixteen-case relabelling,
earlier proven strip and U constraints, and explicit fifteen-point bound
made the completed cover smaller. No resource cap was raised. Both public
algorithms and the analytic proof are by this author: separate implementations
and exact arithmetic checks do not constitute independent peer review.
Normal and optimized Python modes agree. [README.md](README.md) gives
commands, hashes, measured resources and the two small public dependencies.
The proof of geometric necessity, original-star forcing, exhaustive role
coverage, monotone pruning, classical angle identities, analytic inequalities
and the N14 input remains written and unformalized.

## 10. Current literature and complementary scope

The [Cohn table](https://cohn.mit.edu/spherical-codes/) retains unstarred
N=15 in dimension three, cosine 0.59260590292507377809642492233276 and
polynomial 13c^5-c^4+6c^3+2c^2-3c-1. The [coordinate table](https://spherical-codes.org/data/3/15)
is unchanged, 890 bytes, SHA256
1b77ee43d73613885d3fdcfb03dc8fad2e40302ff9c9ff639559cc9b326fb805.
This is candidate/status context, not an optimality proof.
[Musin--Tarasov](https://arxiv.org/abs/1410.2536) settles N=14.
[Lian--Mo--Xia](https://arxiv.org/abs/2411.16038) gives general LP sufficient
conditions and examples without a N=15 optimality theorem.
Classical corner identities, Gram rank, contact-plane intersection, cyclic
links, sphere classification and partition enumeration are credited standard
tools. No historical priority claim is made for this conditional exclusion.

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
fifteen-point packing with c<=593/1000 using two closed-strip certificates
and the known N14 optimum. Its proof was read; its checker is not rerun
here, and no motif occurrence or review is transferred to this T/Q branch.
Those motif results are citations, not finite-cover dependencies.

The next single-three frontier is **(1,5,0)**, whose unique five has three
Ts and two Qs. The r=2,3 rows, larger faces and unrestricted numerical
upper bounds remain open.
