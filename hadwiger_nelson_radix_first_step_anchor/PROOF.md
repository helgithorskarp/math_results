# Complete physical classification of the first-step anchor locus

Write E=Z[omega], omega^2=omega-1, s=2omega-1, s^2=-3. The physical graph
has one vertex per distinct point of A5(z), and every pair at distance one
is an edge. It always contains the triangle 0,1,omega, so chi>=3.

## 1. The full named locus

For any Eisenstein unit epsilon, the equation |1+epsilon*z|=1 is an offset
unit circle. Multiplication of z by omega^2 cyclically permutes three such
circles. At each digit position the triangle (omega^2)^j T is a translate of
T. Directly, including a bijection of all 243 digit words,

```
A5(omega^2 z) = A5(z) - z - omega*z^2 - z^4.
```

Thus the physical graph is unchanged up to translation. The six circles have
two orbits represented by |1+z|=1 and |1-z|=1. We check both signs separately;
no invariance of A5(z) under z -> -z is assumed.

Every point on these two circles other than z=+/-2 has the form

```
z_sigma(t) = sigma*2*s*t/(1-s*t),     sigma in {+1,-1}, t real,
H(t)=1+3t^2>0,
x(t)=-sigma*6t^2/H(t), y(t)=sigma*2t/H(t), z=x+s*y.
```

Indeed 1+z_+(t)=(1+s*t)/(1-s*t) has modulus one, and the usual rational
circle parameterization is onto after adding t=infinity. The negative
representative follows by negation. This covers all real parameters, not
only a selected radius or active-count range.

## 2. All unit-distance events after restriction

A displacement between digit labels is P(z)=sum(d_j z^j), with d_j either
zero or an Eisenstein unit. Unit scaling leaves |P(z)| unchanged.
The independently reconstructed inventory has 2,797 norm curves: 2,796
nonmonomial curves and the radial circle. For nonzero real-circle parameters,
monomial displacements of positive order can be unit only at |z|=1.
The remaining universal edges are the 243 first-digit triangle edges.
The reviewer inventory assigns each of the 29,403 label pairs to precisely
one universal or event group. Consequently checking all active groups checks
the complete strict physical graph, including additional unit edges.

For a row of order k, put N=2st and D=1-st. If

```
A(t)+omega*B(t) = sum_j d_j*sigma^j*N^j*D^(k-j),
```

then its unit condition is the zero of the integer polynomial
`Q=A^2+A*B+B^2-H^k`, of degree at most 2k<=8. Normalize a nonzero Q to a
primitive integer polynomial with positive leading coefficient. The only
identically zero curve is ID 2209 for sigma=+1 and ID 2208 for sigma=-1.
The radial-circle event restricts to 9t^2-1.

The verifier does not reuse this producer formula. For the bivariate event
f(x,y) of total degree 2k it forms H^(2k)*f(-6*sigma*t^2/H,2*sigma*t/H),
exactly divides by H^k, then normalizes. All coefficients and the ordered
inventory hashes agree. Because H has no real roots, neither denominator
clearing nor the exact division changes any real event locus.

Both signs yield the same set of 2,760 distinct nonzero restricted
polynomials. The exact factor products use 2,536 distinct primitive integer
blocks, with degrees:

| degree | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| blocks | 11 | 52 | 100 | 285 | 500 | 771 | 680 | 137 |

Every product identity is checked coefficient by coefficient over Z.
Exact rational Sturm sequences find 1,907 blocks with real roots and 629
without, giving 2,865 real roots in total. Each block is squarefree and
every pair of real-root blocks is coprime over Q. The 1,817,371 pair checks
succeed modulo the prime 1,000,003, preserving BOTH leading degrees.
Primality and the modular Euclidean calculations are checked. Gauss's lemma
then proves rational coprimality. The squarefree checks use the same
degree-preserving principle with derivatives. Nonreal blocks need not be
pairwise coprime: their absence of real roots suffices. Irreducibility of
all blocks is neither assumed nor needed for the proof.

It follows that any finite real event parameter lies on exactly one
real-root block, whose active curves are exactly the identically zero anchor
plus those whose checked factor product includes the block. Outside these
blocks only the anchor and universal edges are active. This handles every
higher-incidence point without enumerating a numerical root approximation.

## 3. Three-colour certificates and collision imports

For every real block except the five listed below, the certificate supplies
a weight word w=(1,w1,w2,w3,w4) over F3. Give digit label a the colour
`sum_j w_j*a_j mod 3`, with digits 0,1,omega encoded by 0,1,2. The checker
reconstructs all actual label pairs and verifies that the endpoints of every
universal edge and every active-curve edge differ. It checks 1,902 block
words for EACH sign; a word holds at every real root of its block.
For non-event t, the word (1,0,0,0,0) passes the universal and anchor edges.

The following real blocks instead carry a nonzero digit-difference witness
P(z_sigma(t))=0 for both signs:

```
[-1,-3,-15,27], [-1,3], [0,1], [1,-3,15,27], [1,3].
```

Coefficients are low degree first. Each has one real root. The independent
collision checker forms P(z)*H^k from the alternative real-denominator
expression `z=sigma*((-6t^2-2t)+4t*omega)/H`. Both Eisenstein-coordinate
numerators are divisible by the block. The row is explicitly checked to be
a nonzero word of zeroes and units, hence a displacement of two distinct
digit labels. These physical members are noninjective. Accepted h4119
therefore supplies their three-colourability. We only need these five
explicit witnesses; we do not assert they classify every possible collision
on the locus or rerun the retired collision branch.

At t=infinity, z=+/-2 lies in E. The residue homomorphism
`a+b*omega -> a-b mod 3` colours E properly: every norm-one Eisenstein
integer is a unit and has nonzero residue. The checker independently forms
both endpoint point sets and verifies this colour on every physical unit
edge. Thus both omitted endpoints are also covered.

For an injective member the checked digit colouring is directly a physical
colouring. If a coloured label graph has duplicate points, choosing one
label for each physical point gives the physical graph as a subgraph of the
checked label graph. Thus this case is covered as well. Together with the
collision imports and the triangle lower bound, chi(A5(z))=3 on all six
anchor circles.

## 4. An explicit higher-incidence physical decision

For the positive root t of 21t^2-1=0 in (1/5,1/4),

```
z_+(t) = -1/4+(7/4)*s*t = (-1+i*sqrt(7))/4,
z_-(t) = -z_+(t).
```

Each fixture lists all 243 points as a(t)+omega*b(t), with a,b rational
polynomials of degree at most one. The field relation is irreducible modulo
11 and hence over Q; the positive real embedding is isolated by exact Sturm
counting. Every coordinate is separately reconstructed from its digit word.
For every pair, the checker reduces the real expression
`(2a+b)^2+3b^2 = 4*|a+b*omega|^2` modulo 21t^2-1. This proves all points
are distinct and enumerates exactly 603 unit edges per fixture. Original
curve owners and restricted polynomials agree on exactly eight active
curves. The respective words (1,0,1,1,2) and (1,0,1,2,2) colour every edge,
and the base triangle proves chromatic number three.

These are physical, exact target-scale chromatic decisions, not positive
non-four-colourability evidence. The entire anchor-locus theorem is the
quantified negative outcome of the declared milestone. The rest of A5
remains open.
