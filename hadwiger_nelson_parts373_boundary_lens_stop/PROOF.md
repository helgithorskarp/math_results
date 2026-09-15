# Exact geometry and certificate argument

Let H and B be the frozen Parts373 host and boundary specified in README.md.
For distinct boundary points a,b set d=b-a and s=|d|^2. There is no common unit
neighbour for s>4, one (a+b)/2 for s=4, and exactly two for 0<s<4:

    (a+b)/2 +/- (i d/2) sqrt((4-s)/s).

The square root is the positive real root. This is the complete intersection
of the two unit circles. Taking every pair, both roots and every tangent,
then merging exact coincidences with H, defines the one simultaneous support.
No second layer or point selection occurs.

The coordinate field of H is K=Q(sqrt3,sqrt11), with independent basis
(1,sqrt3,sqrt11,sqrt33). Every generated point has the exact form

    A + U sqrt(r),  A,U in K^2,  r in K, r>=0.

Here r=(4-s)/s lies in Q(sqrt33); inversion is checked by multiplication in
that quadratic subfield. The checker treats r=0 separately. It does not
assume that any of the additional square roots are independent over K.

## Deciding equality and unit distance

The difference between a squared distance and its target (0 or 1) is

    a + b sqrt(r) + c sqrt(s) + d sqrt(r s),   a,b,c,d in K.

Write this as U+V sqrt(s), with U=a+b sqrt(r), V=c+d sqrt(r). If s=0,
only U is relevant. Otherwise it vanishes precisely when U and V both vanish,
or their signs are opposite and U^2-s V^2=0. The latter expression is

    e + f sqrt(r),
    e=a^2+r b^2-s(c^2+r d^2),  f=2(ab-s cd).

For r>0 and b nonzero, a+b sqrt(r)=0 is equivalent to a^2=r b^2 and opposite
signs of a and b. Zero coefficients and r=0 are handled directly. These
identities decide all candidate collisions and unit contacts in exact
rational arithmetic in K. Squaring alone is never accepted; positive-root
signs are checked. In particular, dependent radicals cause no false
independence assumption.

Rational interval arithmetic supplies real signs and quickly rejects pairs
that cannot have squared distance 0 or 1. A square-root enclosure for rational
x>=0 is produced by integer square root at a fixed dyadic denominator. Its
endpoints are checked to square below and above x. Addition and multiplication
use outward rational endpoints; final coordinate boxes are outward rounded
to multiples of 2^-128. Every all-pairs distance interval is then computed
with integers at denominator 2^256. A pair is discarded only when its closed
interval excludes the target. Every interval containing 1 is instead resolved
by the preceding exact algebraic identity. Likewise every possible collision
is decided exactly. A 192-bit replay produces the same physical graph.

Nonzero sign isolation tries only the declared precisions 128,256,512 and
fails explicitly if unresolved. It never equates a small interval with zero.
No tolerance, solver decision or floating selector is a premise of the proof.

## Colouring and stopping consequence

The supplied 488-character word is proper on all 2,200 reconstructed unit
edges. Its first 373 characters are the frozen full host word, and its
restriction to B is the stated row of the receiving relation. This direct
whole-graph check includes contacts to 58 host vertices outside B, so it does
not rely on a relation-composition argument with an incomplete boundary.
It proves a surviving receiver extension and retires this replacement.

The seven original host labels 0,149,152,312,151,154,314 induce eleven edges.
Exhausting all 3^7 assignments proves that this induced Moser spindle has no
proper three-colouring. Therefore the whole support has chromatic number
exactly four. Recolouring only the first vertex with colour 4 also gives a
checked proper five-colour word; it is only an upper-bound witness.

This result does not determine which other host patterns extend, does not
claim a neutral full interface, and does not prohibit another replacement.
Every subset of this fixed complete support is also four-colourable by
restriction of the same word; subset selection cannot rescue this driver.
The campaign stop includes its immediate enlargement, but no theorem about
second layers, more pins, or arbitrary added points is asserted.

## Trust boundary

The new proof trusts Python integers/Fractions, the elementary circle and
radical identities, the stated K basis, complete finite loops and ordinary
hardware. SHA-256 identifies the imported exact coordinate file. The checker
reconstructs the support without importing a sibling module, solver or
floating-point library. The host-colouring witness is checked directly;
R1's negative completeness and parent proofs are context, not premises of
this failed-replacement certificate. Author verification is not independent
review or proof-assistant formalization.
