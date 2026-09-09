# A finite exact obstruction for the complex-radix architecture

## Construction and claim

Put omega=(1+i sqrt(3))/2, T={0,1,omega}, and

    A5(z) = T + zT + z^2 T + z^3 T + z^4 T,   z in C.

Take the strict physical unit-distance graph: equal point coordinates are
identified, and every pair at Euclidean distance one is an edge. There are at
most 3^5=243 vertices. The arbitrary complex radix permits dilation as well as
rotation. This is not a restriction of the retired three-unit-wheel family.
For example, A5(3) has diameter at least 121, whereas every sum of three unit
wheels has diameter at most 6, invariant under Euclidean isometries.

**Computer-assisted theorem.** Every non-four-colourable member has a
parameter in an explicit finite set of at most **15,522,676** complex numbers.
The set consists of real solutions of **264,800** explicitly generated pairs
of coprime integer polynomials in x,y, with z=x+i sqrt(3)y, and roots of
**2,400** explicit nonzero-constant displacement polynomials over Q(omega).
The first part has at most 15,513,472 points; the second at most 9,204.
Every such parameter satisfies 1/2 < |z| <= 2. An injective possible
counterexample must lie on **at least four distinct active event curves**,
and its parameter field Q(x,y) has degree at most 64.

These are necessary conditions. The exceptional parameters have not been
claimed non-four-colourable, distinct, physically inequivalent, or all real
in the pair representation. The entire architecture has not been closed.
No five-chromatic graph or record improvement is established.

## Complete displacement and event inventory

The difference alphabet is T-T={0} union mu6. Every five-digit displacement
occurs between two of the 243 labels. Simultaneous multiplication of its
coefficients by a sixth root of unity preserves its norm and zero set. This
free action on nonzero coefficient words gives

    (7^5-1)/6 = 2801

canonical displacement polynomials P(z)=sum d_j z^j. The verifier enumerates
all 29,403 unordered label pairs and their canonical words; no candidate
selection is used in this inventory.

For z=x+i sqrt(3)y, write P(z)=(A(x,y)+i sqrt(3)B(x,y))/2. Then

    |P(z)|^2=1  iff  A^2+3B^2-4=0.

The coefficients of A,B are integers. The code constructs this identity in
two ways: recurrence for powers of x+i sqrt(3)y, and a separate binomial
expansion of P(Z) conjugate(P)(V)-1 with Z=x+i sqrt(3)y and V=x-i sqrt(3)y.
All 2,801 polynomial identities agree exactly after primitive normalization.

A constant unit displacement is an edge for every z; it gives 243 universal
edges, the 81 triangles obtained by varying the first digit. A nonconstant
monomial unit displacement has norm |z|^j and gives the single real event
S-1=0, where S=x^2+3y^2. The exact identities

    S^j-1 = (S-1)(1+S+...+S^(j-1)),  j=1,...,4

and S>=0 justify replacing these four events by the same circle. Every other
canonical displacement gives one active curve. The resulting 2,797 distinct
curves have total-degree histogram

    degree 2: 7;  degree 4: 48;  degree 6: 342;  degree 8: 2400.

## Absolute irreducibility and pairwise coprimality

The following elementary argument avoids trusting a CAS factorization.
If a nonconstant polynomial P over C has a simple root, then

    P(Z) conjugate(P)(V) - 1

is irreducible over C[Z,V]. Let beta be a simple root of conjugate(P), and
reverse the polynomial in Z, of degree n. The result is

    conjugate(P)(V) sum_{j=0}^n p_j X^(n-j) - X^n.

At the prime V-beta of C[V], its leading coefficient is nonzero modulo the
prime, all lower coefficients are divisible by the prime, and its constant
coefficient has valuation exactly one. Eisenstein's criterion proves
irreducibility over C(V). Its coefficient content in C[V] is one: a common
divisor would divide conjugate(P) and conjugate(P)p_0-1. Gauss's lemma and
reversal give the claim. The invertible complex linear change (Z,V) to (x,y)
preserves irreducibility.

The verifier proves that each of the 2,796 non-monomial P has a simple root.
It works exactly in Q(omega)[z]. If g=gcd(P,P'), q=P/g, then

    q / gcd(q,P')

has precisely the simple roots of P and has positive degree in every case.
The degree histogram is 1:24, 2:102, 3:330, 4:2340. The circle corresponds to
P=z and has the same irreducibility proof. The normalized curve polynomials
are checked distinct by exact coefficient comparison. Since they are
absolutely irreducible, any two distinct active curves are coprime even over
C. No unverified factor irreducibility or specialized resultant is imported.

## Colour words and a finite covering set

Index T as (0,1,omega). In F3 use the ring map omega -> -1; in F4 use
omega -> t with t^2+t+1=0. Let e_c(a) denote the corresponding residue of a.
For weights w_0=1,w_1,...,w_4 in the chosen field, assign the label colour

    C_w(a_0,...,a_4) = sum w_j e_c(a_j).

The first weight makes every universal triangle proper. An active curve is
bad for a word exactly when some edge belonging to that event has equal
label colours. All bad sets are reconstructed directly from the complete
label-pair inventory. In the injective case the label word is an actual
physical colouring whenever none of its bad curves vanishes.

Six simple F3 words cover every individual curve: weights (1,0,0,0,0),
(1,e_j) for j=1,...,4, and (1,1,1,1,1). For a non-monomial event with d_0
nonzero the first word works. If d_0=0, select a nonzero later coefficient.
Its residue and every sixth-root multiple are nonzero in F3, so the selected
word works. The all-ones word works on the circle. The verifier additionally
checks every one of these assertions on the explicit edge lists.

For the smaller finite covering set, the compact certificate uses five words:

    F3: (1,0,0,0,0)
    F4: (1,0,1,0,1), (1,1,0,0,1), (1,1,0,0,2), (1,1,1,1,1).

The primary F3 word has 397 bad curves, with degree sum 3,050. For each such
curve f the certificate names a protecting word C(f) for which f is not bad.
The checker verifies the complete deterministic assignment. It forms all
unordered pairs (f,g) where f is a primary bad curve and g is bad for C(f),
removing duplicates. There are exactly 264,800 pairs, and f is never g.

If an injective physical graph is not four-colourable, the primary word
fails, so some f vanishes. Its protecting word also fails, so some g vanishes.
This puts the parameter on a listed pair. The sum of degree(f)*degree(g)
over that exact list is 15,513,472. Classical projective Bezout, applied to
the coprime complex curves, bounds their affine common points by these
products. Infinite points, nonreal points and multiplicities only make the
bound conservative. Each product is at most 64; hence each finite point's
coordinate field over Q has degree at most 64. The map from a real (x,y) to
z is injective.

## At least four simultaneous curves

A single non-monomial event has a nonzero tail coefficient modulo 2. Among
all 256 F4 words with w_0=1 and arbitrary tail weights, its failure equation
is one nonconstant affine linear equation, with exactly 64 solutions. Thus
at most three such curves exclude at most 192 words and cannot prevent a
four-colouring.

If the circle is active, restrict to the 81 words whose four tail weights
are nonzero. Each non-monomial failure equation excludes at most 27 of these:
fix three coordinates, and the remaining nonzero-coefficient coordinate has
at most one forbidden value among its three choices. The circle plus at
most two other curves therefore excludes at most 54 words. These two cases
prove the four-curve necessary condition for every injective non-four-
colourable parameter. This is a stronger necessary incidence condition,
not a claim that four curves suffice for non-four-colourability.

## Coincidences, small radii, and large radii

If two labels coincide, a nonzero displacement polynomial P vanishes. For
z nonzero remove the initial zero coefficients; remove trailing zeros too,
and normalize by sixth-root multiplication. The full distinct inventory of
nonconstant polynomials with nonzero constant coefficient has counts

    degree d: 6*7^(d-1), d=1,2,3,4.

It contains 2,400 polynomials, whose degrees sum to 9,204. Every nonzero
collision parameter is therefore among at most 9,204 complex roots. These
polynomials have degree at most 4 over Q(omega). No root isolation or
assumption of distinctness among their root sets is needed for this bound.
The remaining parameter z=0 gives A5(0)=T and is three-colourable.

For |z|<=1/2, the tail displacement has norm at most

    |z|+|z|^2+|z|^3+|z|^4 <= 15/16.

Distinct first digits cannot coincide, and equal first digits cannot be a
unit edge. Colouring by the first digit therefore descends to the physical
quotient and is proper. For |z|>2 and highest nonzero displacement index m>=1,

    |P(z)| >= |z|^m - sum_{j<m}|z|^j > 1.

Thus the labels are injective and the only edges are the universal triangles.
Both radial arguments are independent of the finite algebraic cover.

## Exact interface and trust boundary

The exported interface gives each curve as integer triples (x exponent,
y exponent, coefficient), a canonical complex displacement, all pair IDs,
and the full nonzero collision polynomial list. All list orderings and
hashes are deterministic. Generation, verification and export require only
the CPython standard library. SymPy factorization and a larger character
catalog were exploratory aids; neither is a proof premise. No SAT or UNSAT
verdict is used.

The field arithmetic, finite inventory, colour checks, and all counts are
computer checked. Eisenstein/Gauss, Bezout, the counting argument over F4,
and the Euclidean reduction are written mathematical arguments, not
proof-assistant formalizations. Review acceptance is not claimed.
