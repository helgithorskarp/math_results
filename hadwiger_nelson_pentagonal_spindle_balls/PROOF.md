# Pentagonal Moser-direction balls and a dyadic escape test

Put rho=exp(i*pi/3), zeta=exp(2*pi*i/5), eta=(5+i*sqrt(11))/6, and
delta=(eta-1)*(1+rho). Each of rho, zeta, eta and delta has modulus one.
All roots and square roots refer to these stated physical complex values.

## 1. A direction obstruction

Let A=Z[1/3,rho,eta], a subring of E=Q(i*sqrt(3),i*sqrt(11)).
There is a ring homomorphism r:A -> F4 sending rho and eta to omega, where
omega^2+omega+1=0. Indeed, their monic equations are

    rho^2-rho+1=0,       eta^2-(5/3)*eta+1=0,

both reducing to X^2+X+1 in characteristic two. The two quadratic fields
are independent, so 1,rho,eta,rho*eta are linearly independent over Q.
The quotient by these monic relations is free of rank four over Z[1/3]
and embeds into E. This proves that the stated reduction is well-defined,
rather than assuming a map from an entire characteristic-zero field to F4.

Complex conjugation takes rho to 1-rho and eta to 5/3-eta. Therefore

    r(conj(a)) = r(a)^2,          a in A.

If a is a unit complex direction in A, its norm is one and
r(a)^3=1. In particular r(a) is nonzero.

The intersection E cap Q(zeta) is Q. The only quadratic subfield of Q(zeta)
is Q(sqrt(5)), whereas the quadratic subfields of E have radicands -3,-11,33.
Thus Phi5 stays irreducible over E. In A[zeta], the only dependence among
1,zeta,...,zeta^4 has all five coefficients equal. Choose the five nonzero
weights in F4

    (w0,w1,w2,w3,w4)=(1,1,1,omega,omega^2).

Their sum is zero. Consequently

    L(sum(j=0..4) a_j*zeta^j) = sum(j=0..4) r(a_j)*w_j       (2)

is a well-defined additive map A[zeta] -> F4. If a in A has norm one,
then L(a*zeta^j)=r(a)*w_j is nonzero.

**Direction theorem.** Every plane unit-distance graph whose edge displacement
vectors belong to

    union(j=0..4) {zeta^j*a : a in A, a*conj(a)=1}

is four-colourable. In each connected component translate one vertex to zero.
Every other vertex then belongs to A[zeta], by adding displacements along a
path, and (2) gives a proper colour. This is a conditional theorem about
the complete edge-direction set, not a four-colouring of the entire plane or
the entire coordinate field. In a strict graph all accidental unit edges
must also satisfy the direction condition before the theorem can be applied.

The method is an additive residue colouring. No novelty is claimed for
finite-field colouring methods; the concrete pentagonal module, its weights,
and their application to the candidate family are the contribution here.

## 2. A complete 451-point family inside one exact host

Take the ten six-direction orbits

    O_(h,j) = {eta^h*zeta^j*rho^k : k=0,...,5},
    h=0,1, j=0,...,4.

Choose any five orbits, let U be their union, and use P=U+U as the physical
support. There are binomial(10,5)=252 named choices. Each U has 30 distinct
unit directions and is closed under negation and 60-degree rotation.

Each P has exactly 451 points. There are 465 unordered pairs with repetition
from 30 directions. The 15 antipodal pairs all sum to zero. Every other
unordered pair has a different, nonzero sum: the midpoint of a chord of a
circle determines that chord's unordered endpoints, except for diameters.
Hence there are 465-15+1=451 distinct sums. Each original direction is already
a sum of its two 60-degree neighbours. The same argument gives 1801 points
for the host H formed using all 60 directions.

Exact all-pairs reconstruction gives **7170** unit edges in H. Its 90 directed
unit displacements are precisely

    {zeta^j*rho^k*t : j=0,...,4, k=0,...,5, t in {1,eta,delta}}.

This equality is checked on the full exact edge inventory, not inferred from
the generating directions. Since 1,eta,delta are unit elements of A, the
direction theorem colours H. Thus every subgraph of H is four-colourable,
including arbitrary supports of at most 508 points in H, not just the 252
named 451-point candidates. The edge histogram of those candidates is

    1650:20, 1668:130, 1686:100, 1740:2.

The coordinate field is E(zeta), of degree 16. It contains E(sqrt(5)), the
Parts coordinate field, so whole-field four-colour exclusions of other
extensions cannot be applied here. The older integral-CM theorem does not
apply either: eta is not an algebraic integer, as its quadratic trace is
5/3. Our direction theorem uses integrality over Z[1/3] and a direction
restriction, not integrality at every prime.

## 3. The selected Moser interface does not strengthen

Use the aligned Moser spindle

    M=(0,1,rho,1+rho,eta,eta*rho,eta*(1+rho)).

Its exact graph has seven vertices and eleven edges. Enumerating all
canonical proper colourings with at most four colours gives exactly 16
equality patterns; each uses all four colours. This also directly checks
its four-chromaticity. All 16 patterns extend to proper four-colourings of H,
as witnessed by the sixteen 1801-entry words in the certificate.

Rotations by zeta and rho permute the 60 generating directions, as does the
reflection z -> eta*conj(z). These isometries therefore preserve H=U+U.
The same extension conclusion holds for the aligned rotated/reflected copies
of M and, by restriction, for any named 451-point member containing such a
copy. No claim is made about arbitrary terminal sets or all possible
translated spindles in the host. This is precisely the chosen interface gate.

## 4. A bounded dyadic escape also remains neutral

The first family and its selected interface were closed before this next
test was chosen. Let

    w=(7+i*sqrt(15))/8.

It has modulus one. It is not integral at 2: its quadratic trace is 7/4.
Thus w does not belong to A[zeta], which is integral over Z[1/3]. The previous
additive colour does not automatically extend to constructions using w.
This is a concrete way to violate the obstruction, not evidence of chi five.

For each j=1,...,4 and h,l=0,1 choose five phase orbits with representatives

    1, eta, w, eta*w, zeta^j*eta^h*w^l.

Multiply each by all six powers of rho and again take U+U. All sixteen
supports have 451 distinct plane points. Each has exactly **1740** unit edges.

There is a natural common labelling: label zero first, then the unordered
nonantipodal pairs of the 30 ordered unit directions. Complete exact edge
reconstruction proves that all sixteen labelled graphs have the **same**
edge set. One set of sixteen 451-entry positive words therefore extends
every canonical Moser pattern in every case. These graphs are four-chromatic
because they contain M. Neither the non-four test nor the selected interface
test supplies a new forcing signal. Their arbitrary unions are not classified.

## 5. Exact reconstruction and independent author checks

The producer uses Q(zeta15,eta), with

    Phi15=X^8-X^7+X^5-X^4+X^3-X+1,
    3*eta^2-5*eta+3=0.

For a point x+eta*y with integral cyclotomic coefficient vectors,

    3*N(x+eta*y)
       = 3*(x*conj(x)+y*conj(y)) + 5*x*conj(y)
         + 3*eta*(y*conj(x)-x*conj(y)).

The dyadic point vectors have a common physical denominator 8. A checked
ring projection modulo 1000000411, with zeta15->539108921 and eta->98299921,
screens all pairs, then exact integer polynomial norm tests confirm every
survivor. There are no numerical distance thresholds. The proof of
completeness is that a genuine polynomial norm equality survives reduction;
primality, generator order and polynomial roots are explicitly checked.

The verifier independently constructs the directions using

    Q(zeta5,alpha,beta), alpha^2=-3, beta^2=-11,
    rho=(1+alpha)/2, eta=(5+beta)/6.

It uses sixteen tensor coefficients and denominator 96. It checks entire
coordinate sets, or ordered coordinate lists, against the producer via the
exact conversion zeta15=-rho*zeta5^2. Then a C++ kernel tests **all 3,244,500
point pairs directly**, without a modular filter, by multiplying each
complex difference by its conjugate in this alternate basis. All 35,010
edge entries match the producer exactly. This covers the 1801-point host
and all sixteen 451-point dyadic cases; the 252 original candidates are
explicit exact subsets of the host.

The kernel rejects coordinates with any coefficient exceeding 10^6.
Differences have coefficients at most 2*10^6 and their conjugates at most
8*10^6. A norm coefficient is bounded by
256*(2*10^6)*(8*10^6)*33 < 2^63, including the tensor factors and cyclotomic
reduction. Thus signed 64-bit arithmetic is sufficient. Full replay also
uses undefined-behaviour sanitization. Python coefficient arithmetic uses
arbitrary-precision integers and Fractions; NumPy's sieve products have
absolute value less than p^2 < 2^63.

The verifier regenerates all sixteen Moser patterns, checks each positive
word edge by edge and on its terminals, checks the direction formula and
field relations, and rejects malformed words and ring projections. SAT is
only an optional producer of positive words. No negative SAT verdict is used.

Trust remains in the written algebra and geometric reductions, the two
ordinary arithmetic implementations, Python/NumPy/C++ semantics and the
compiler. The alternate checker is author-run cross-validation, not an
external review or formal proof. All required input is generated from the
displayed equations; there are no unprovided graphs or large certificates.

## 6. Construction consequence

This is a direction obstruction and two exact finite construction decisions,
not a global lower bound on the order of five-chromatic unit-distance graphs.
The 509-vertex record is unchanged. Both declared cohorts are retired:
additional orbit counts or arbitrary eta-power sweeps are not justified by
these neutral results. The theorem identifies what future use of this
material would need to change, but no successful successor is claimed.
