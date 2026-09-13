# A residue obstruction for weighted rotations, and an explicit escape

This is an author-checked computer-assisted construction obstruction. It does
not improve the 509-vertex record. The auxiliary five-chromatic graph below
has two edge lengths and is not a five-chromatic unit-distance realization.
No literature-priority claim is made.

## 1. Exact construction and local coordinates

Put alpha = i sqrt(3), beta = i sqrt(11),
E = Q(alpha,beta), F = Q(sqrt(33)), and

    u = (5 + alpha sqrt(13))/8,
    W(A) = {(1-u)a + u p : a,p in A}.

The norm of u is one and u + conjugate(u) = 5/4. For each fixed a, the
corresponding row is an isometric copy of A rotated about a. All coordinates
are explicit plane points in E(sqrt(13)). The map from A times A to W(A) is
injective: 1,u are linearly independent over E, so equality of two images
forces equality of both labels. Indeed sqrt(13) is not in E, whose three
quadratic subfields are Q(sqrt(-3)), Q(sqrt(-11)), and Q(sqrt(33)). Thus
|W(A)| = |A|^2, with no hidden collision assumption.

Fix the embedding of F into Q_2 with sqrt(33) congruent to 1 modulo 8.
Then the completion of E is the unramified quadratic extension Q_2(w),
w^2+w+1=0, under alpha = 1+2w and beta = alpha sqrt(33)/3.
Complex conjugation fixes the chosen Q_2 and sends w to w^2. Let O denote
the elements of E integral in this embedding. Its residue ring modulo 4 is

    R = (Z/4Z)[w]/(w^2+w+1).

Write rho: O -> R for reduction. For A contained in a coset of O, translate
that coset to O before applying the construction; W(A+t)=W(A)+t. The finite
Parts application below checks every source point belongs to O.

The norm of a+bw is a^2-ab+b^2 modulo 4. Consequently any E difference of
squared length 1 reduces to one of the six elements

    U = {+/-1, +/-w, +/-(1+w)}.

A difference of squared length 4/3 has local valuation one: the valuation of
its norm is two, and the unramified quadratic norm doubles valuations.
Its residue is therefore one of V = {2,2w,2+2w}. The local-field premise is
also developed in the separately reviewed
`../hadwiger_nelson_nonmono_field_obstruction/PROOF.md`.

## 2. Universal obstruction for three forms of edges

On R times R take the undirected Cayley graph with direction set

    S = {(0,e), (e,e) : e in U} union {(v,0) : v in V}.

It has 256 vertices, degree 15, and 1,920 edges. The following explicit
four-colouring supplies a small checkable certificate. If

    z = (a+bw, c+dw),
    a=a0+2a1, b=b0+2b1, c=c0+2c1, d=d0+2d1,

all eight lower-case subscripted variables are bits. Define, over F_2,

    L = a1+b1+c1+d1+b0+a0*b0+(a0+b0)*(c0+d0)+c0*d0,
    H = a1+c0+d0,
    colour(z) = L + 2H.

`verify.py` checks every one of the 256 times 15 directed edges using
ordinary integer arithmetic. It also checks agreement with the independently
stored 256-digit SAT discovery witness. The SAT solver is not a dependency
of this colouring proof.

**Theorem.** Suppose A is a subset of O, and every unit edge between labels
(a,p),(b,q) of W(A) has

    (rho(a-b), rho(p-q)) in S.

Then the complete plane unit-distance graph on W(A) is four-colourable by
colour(rho(a),rho(p)). The same holds for any subset of W(A), and for
rectangular labelled supports with both coordinates in O.

**Proof.** The displayed hypothesis says the label-reduction map takes every
physical unit edge to an edge of the explicitly four-coloured finite graph.
The map from labels to physical points is injective. Pull back the colours.

In particular, the hypothesis holds whenever every unit edge has one of
these three forms, with d=a-b and r=p-q:

| form | exact condition | residue direction |
|---|---|---|
| horizontal | d=0, N(r)=1 | (0,e), e in U |
| vertical | r=0, N(d)=4/3 | (v,0), v in V |
| diagonal | d=r, N(d)=1 | (e,e), e in U |

The vertical length is exact because N(1-u)=3/4. This corollary is uniform
over all source sets satisfying the hypothesis, not just one fixed Parts
host. A five-chromatic W(A) must have a unit contact outside S, and hence a
contact outside these three forms. Such a contact is necessary, not
sufficient, for non-four-colourability.

## 3. Complete physical application to the Parts 374-point component

Let L be the first 374 points of the hash-bound coordinate table specified
in `exact.py`. Coefficients use the basis 1,sqrt(33),alpha,beta; the existing
16-coordinate source table has scale 96. These 374 points are distinct,
lie in E and O, and have integral coefficients after multiplication by 12.
The calculation reconstructs their 11,651 distinct differences.

There are exactly 39 weighted unit directions (d,r), up to simultaneous
negation: 15 horizontal, 9 vertical, and 15 diagonal. There are no other
unit directions. Thus W(L) has 139,876 distinct physical points and exactly
1,211,200 unit edges, and all these edges are properly four-coloured by
Section 2. Every subset of this support is also four-colourable.

Here is the completeness argument for the contact calculation. For d != 0
write y=d-r. Independence of 1,u forces conjugate(d)*y to be real in any
identity N(d-u*y)=1. Thus y=t*d for t in F, and

    N(d)*(1+t^2-(5/4)t)=1,
    t = ((5/4) +/- sqrt((5/4)^2-4+4/N(d)))/2.

`exact.py` determines whether this square root exists in F by the complete
rational square criterion: for a+b sqrt(33), b != 0, square-root coefficients
have rational squares (a +/- sqrt(a^2-33b^2))/2. The b=0 cases separately
test rational and sqrt(33) multiples. Both roots are retained and tested
against the full difference set. The d=0 case is checked directly.

`direct_contacts.cpp` independently bypasses square roots and inversions.
It tests all 11,651^2 = 135,745,801 ordered difference pairs with exact
bilinear polynomial equations. It requires conjugate(d)*r to be real and

    3*N(d) + 4*N(r) - 3*Re(conjugate(d)*r) = 4.

It returns exactly the same 78 oriented directions, compared entrywise.
This is a different completeness algorithm, not an independent-author
review. The integer input denominator is 12. Under the checked coefficient
bound 10^6, every intermediate absolute value is below 5*10^14, so signed
64-bit arithmetic cannot overflow. Both optimized and undefined-behaviour
sanitizer builds are part of the recorded validation.

For each direction up to sign, the number of physical edges is the product
of the numbers of ordered source pairs realizing its two differences.
Injectivity makes these products disjoint and avoids an expensive all-pairs
scan on 139,876 physical points.

## 4. A certified false positive for an auxiliary chromatic test

For a source set A define J(A) to have all edges of squared length 1 or 4/3.
Its non-four-colourability does not imply that of W(A).

The 114 source indices in `auxiliary_certificate.json` specify P subset L.
J(P) has 535 edges: 379 of squared length 1 and 156 of squared length 4/3.
It is vertex-critical and has chromatic number exactly five. A direct
checker verifies the supplied five-colouring and all 114 four-colourings
after deleting one vertex. Its non-four-colourability is certified by a
Kissat binary DRAT proof, independently accepted by drat-trim. The compact
source regenerates the 456-variable, 2,255-clause input; the transient proof
is deliberately not committed. Commands and hashes are in REPRODUCE.md and
VALIDATION.json.

For k=4 the encoding has variables x[v,c], clauses requiring at least one
colour per vertex, and clauses forbidding a common colour on each edge.
At-most-one clauses are unnecessary: any satisfying assignment yields a
proper colouring by choosing one true colour at each vertex. Conversely a
proper colouring satisfies all clauses. The sole symmetry constraint is
x[0,0], justified by a global colour permutation. Thus an UNSAT certificate
proves non-four-colourability of the stated two-distance graph.

Nevertheless W(P) is a physical 12,996-point, 71,477-unit-edge subgraph of
W(L), and Section 2 four-colours it. This is an explicit separation between
the auxiliary chromatic condition and the actual plane construction. It
does not supply a unit-distance five-chromatic graph on 114 points or on
any other number of points.

## 5. A mixed contact that defeats the displayed colouring

The obstruction has a concrete boundary within the same field. Put

    d = alpha/15, r = 3*alpha/5,
    w = (-1+alpha)/2.

Then w is a unit and

    (1-u)d + u*r = (-sqrt(13)+2*alpha)/5,

whose squared norm is (13+12)/25=1. Multiplying both d and r by w preserves
this unit identity. These new E differences lie in O and have

    rho(w*d) = rho(w*r) = 2+w in R.

Here the notation w also denotes its image in R, as in Section 1. The
direction (2+w,2+w) is outside S because its component has norm 3 modulo 4.
The displayed Boolean colouring gives equal colours at z and
z+(2+w,2+w) for every z in R times R. Thus the contact actually breaks this
specific colouring, rather than merely failing a sufficient hypothesis.
For example it occurs in W({0,w*d,w*r}) between the origin and the point
labelled (w*d,w*r). All identities are checked exactly.

This single edge is not a non-four-colourability witness. A future record
attempt must integrate mixed contacts into a sufficiently constrained
support of at most 508 distinct points and certify the complete geometry
and chromatic contradiction. Repeating the three-form construction, even
with a five-chromatic J(A), cannot succeed.

## 6. Evidence and limits

All calculations use exact integers and rational numbers; no floating-point
distance threshold or approximate embedding occurs. Trust boundaries are
the written local-field and contact-reduction arguments, CPython rational
arithmetic, the checked C++ integer bounds, the hash-bound source table,
the small positive witnesses, and drat-trim for the auxiliary UNSAT proof.
These are author validations; independent review of this package is pending.

The primary record comparison was refreshed on 2026-09-13: Parts reports
509 vertices and 2,442 edges in https://arxiv.org/abs/2010.12665, and the
introduction of https://arxiv.org/html/2608.04542v4 still identifies 509 as
the unrestricted record. Its Moser-spindle-free constructions address a
different restriction. No smaller certified construction was found here.

Discovery Net's local committed index remained stale at height 4363.
Current source and independent reviews in the authorized repository were
therefore also inspected. This result is complementary to the reviewed
three-common-origin Parts159 rotation exclusion: this pass changes anchors
and uses a weighted support with many rotations and translations. It does
not claim a bound on all plane unit-distance graphs or the entire field
E(sqrt(13)).
