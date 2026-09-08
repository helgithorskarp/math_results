# Arithmetic colouring and the VND root interface

Let V be the exact VND series-2 case-10 point set from the sibling
[verified source](../hadwiger_nelson_vnd_case10_verified_gate/PROOF.md).
It has 64,513 distinct plane points and 542,472 strict unit edges.
Its non-four-colourability is an imported, independently accepted result:
Discovery Net h3927, accepted at h3941. This package supplies the upper bound
and the consequences below; it does not repeat that SAT query or its proof.

**Result.** The chromatic number of V is exactly five. Removing its origin
gives a graph of chromatic number exactly four, with 64,512 vertices and
542,328 edges. Thus every non-four-colourable subgraph of this fixed support
contains the origin. The origin has 144 neighbours, and every proper
four-colouring after its deletion uses all four colours on those neighbours.

There is also a positive constraint on each of the two 32,257-point halves:
in every proper four-colouring, at least one of its 120 cross-interface
vertices has the same colour as the origin. This is an existential statement
about a set of 120 vertices. It is not a claim that a particular marked pair,
or every marked pair, is forced monochromatic.

## 1. A residue colouring of each half

Write

    t = exp(pi*i/12),       phi = (sqrt(6)+i*sqrt(3))/3,
    M1 = {0} union {t^j phi^k : 0<=j<24, -1<=k<=1},
    M2 = {z in M1+M1 : |z|<=1},
    M3 = M2+M1,             rho = (-7+i*sqrt(15))/8,
    V = M3 union rho*M3.

The source's exact construction and all strict unit pairs are already checked
in h3927/h3941. The halves intersect only at the origin.

The ring R=Z[t,1/3] lies in Q(t), with minimal polynomial
Phi_24(X)=X^8-X^4+1. Put F4=F2[w]/(w^2+w+1). Evaluation t -> w defines a ring
homomorphism r:R -> F4: Phi_24(w)=w^2+w+1=0, and 3 maps to the unit 1.
Conjugation on R corresponds to the Frobenius map on F4, because t^-1 maps
to w^-1=w^2. Thus for d in R with d*conjugate(d)=1,

    r(d) * r(d)^2 = 1,

so r(d) is nonzero. Consequently r is a proper four-colouring of UD(R).

The identities

    i=t^6,  sqrt(2)=t^3+t^21,  sqrt(3)=t^2+t^22

give r(i)=1, r(sqrt(2))=0, r(sqrt(3))=1, and r(phi)=1.
Both phi and phi^-1=conjugate(phi) belong to R. Hence M1, M2 and M3 are
subsets of R. Colour the first half by r(z), and the rotated half by
r(rho^-1 z). In both half-colourings the origin has colour 0.

This four-colouring statement concerns the localized ring R; it is not a
claim about every point of Q(t) or every union of rotated copies of R.

## 2. Exact finite interface calculation

Of the strict unit edges, exactly 120 join nonorigin points in different
halves. They form a matching, and **both endpoints of every one have colour
0 in their respective half-colourings**. The complete 120-element boundary
label sets are reproduced in EXPECTED.json.

Here is the exact arithmetic recipe used to check that calculation. Archive
coordinates have common denominator 96 and each x and y uses the ordered
real basis

    1, sqrt(2), sqrt(3), sqrt(6), sqrt(5), sqrt(10), sqrt(15), sqrt(30).

Use the first four coefficients of each component to form the polynomial P(t)
representing the part without sqrt(5) of 96z. For a first-half point,
P(t)=96z and every coefficient is divisible by 32. Reducing P/32 modulo 2
therefore gives r(z), since 96=32*3 and 3=1 in F4.

For a second-half point z=rho*u, with u in M3, the part without sqrt(5) is
P(t)=-84u. Every polynomial coefficient is divisible by 4. Reducing P/4
modulo 2 gives r(u), since -84/4=-21=1 in F4. Separating the two parts is
valid because sqrt(5) is not in Q(t): Q(t) is ramified only at 2 and 3,
whereas Q(sqrt(5)) is ramified at 5.

The producer checks all eight coefficient divisibilities for all 64,513
points, using exact FLINT arithmetic modulo Phi_24. The standard-library
checker instead uses the two integer linear forms in CERTIFICATE.json to
compute the colour bits directly from the archive's radical coefficient
rows. It then checks the assigned colours against every author edge.
For the upper bound, this direct assignment check is sufficient independently
of the algebraic motivation of the recipe.

The two half-colourings are proper on all their internal edges, including
their edges to the common origin. Each half has colour counts
(7177,8360,8360,8360), counting its own origin. Every joining edge has colour
pair (0,0). Therefore precisely the 18 palette permutations p with p(0)!=0
avoid all cross-edge conflicts when the origin is deleted; all 24
permutations are checked. This classifies relative permutations of these
two particular colourings, not all colourings of the two halves.

## 3. Five colours and deletion of the origin

Use the original residue colours 0,1,2,3 on the nonorigin first half. On the
nonorigin second half, interchange 0 and 1. Give the origin the new colour 4.
Internal edges remain proper under these palette permutations, each joining
edge now has colours 0 and 1, and all edges to the origin have different
endpoint colours. The five colour-class sizes are

    15536, 15536, 16720, 16720, 1.

The 64,513-byte word, encoded as one byte 0..4 per source vertex in label
order, has SHA256

    29c1812533c1c173c1491fe88dc7f358477c92dec0d5b4ce2abe21be0d473f36.

Thus chi(V)<=5; the imported non-four-colourability gives chi(V)=5.
Deleting the origin leaves an explicit proper four-colouring. A
three-colouring of that deletion could be extended by a new fourth colour
at the origin, contradicting the imported lower bound. Hence chi(V-0)=4.
Every subgraph omitting the origin inherits a four-colouring. Finally, if a
four-colouring of V-0 omitted a colour among the 144 origin-neighbours, that
colour could be assigned to the origin, again contradicting the lower bound.

## 4. The 120-port root-colour constraint

Let B_L and B_R be the sets of endpoints of the cross matching in their
respective halves. Suppose a proper four-colouring c of the first half gave
every vertex of B_L a colour different from c(0). Permute its palette to make
c(0)=0. Colour the other half by its canonical residue colouring: it has
colour 0 both at the origin and at every vertex of B_R. The colourings agree
on their sole common vertex. Every joining edge has unequal endpoint
colours, so together they would give a proper four-colouring of V. This
contradicts h3927. Therefore some b in B_L satisfies c(b)=c(0).
The argument with the halves interchanged proves the other statement.

This is a checkable positive boundary consequence of the existing
non-four-colourable construction. The weak existential constraint by itself
does not prove that two replacement modules form a non-four-colourable graph:
the two same-colour witnesses need not be endpoints of the same matching edge.
No smaller forcing module, physical support reduction, or <=508 candidate
is supplied.

## 5. Provenance and trust boundary

The primary paper is Voronov, Neopryatnaya and Dergachev,
[arXiv:2106.11824v4](https://arxiv.org/html/2106.11824), sections 5--8.
It already calls this a five-chromatic graph and notes in section 8 that
colouring the origin with a fifth colour makes the remaining four-colouring
easy. We claim no priority for the chromatic number or the origin strategy.
This package independently supplies an algebraic word and a compact checkable
recipe, and derives the stated boundary constraint.

The complete strict geometry and non-four-colourability depend on h3927 and
its independent acceptance h3941. The upper bound is checked directly on the
pinned source graph; no new SAT answer or unverified proof is used. The
normalized coordinate bytes are checked against their earlier audited hash.
The fresh-input script uses the earlier safe source parser, so that part is
shared infrastructure, not a newly independent parser. Residual trust includes
the elementary reasoning here, the earlier geometry and strict LRAT checks,
CPython, FLINT for the optional producer, and hardware. This is not a formal
proof-assistant development or independent peer review of the new package.

The previous fixed-LRAT-base retention route remains retired. Its support
floor 26,885 is neither changed nor used as a bound on this semantic interface.
The accepted 1,003-vertex EI graph remains the team's smallest exact
five-chromatic intermediate result. No record improvement is established.
