# Complete rotation-only pair stratum

Let omega=(1+i sqrt(3))/2, T={0,1,omega}, and

```
A5(z) = {sum(a_j*z^j,j=0..4) : a_j in T}.
```

The strict graph has the distinct physical points as vertices and every
distance-one pair as an edge. The unit triangle 0,1,omega is always present.

## Selection and exact source equations

In the h4191 residual, the only global pairs with nontrivial setwise D3
stabilizers are

```
(318,340), (318,341), (319,340), (319,341).
```

Each has stabilizer exactly `{1,R,R^2}`, where R(z)=omega^2*z. Conjugation C
provides its other orbit image. The verifier reconstructs the full named action
from the independently reviewed bivariate norm curves, checks the stabilizers
and canonical representatives, and verifies the elementary physical identities

```
A5(omega^2*z) = A5(z)-z-omega*z^2-z^4,
A5(conjugate(z)) = omega*conjugate(A5(z)).
```

Thus eight distinct pair conjunctions are covered by the four representatives.
These are pair stabilizers, not claims that a physical parameter is fixed by
a rotation. The original four rows remain separate throughout the computation.

The reviewed displacement rows are

```
P318 = -z+(omega-1)*z^4,
P319 = -z+omega*z^4,
P340 = -z-z^4,
P341 = -z+z^4.
```

Curve c means `|Pc|^2=1`. For z=x+i sqrt(3)y the equations are real integral
bivariate polynomials. Their differences factor as `(x^2+3y^2)` times a cubic.
The radial factor cannot vanish at a physical solution: z=0 makes both norms
zero. This explains the low-dimensional exact geometry; the proof below uses
the full original equations and does not discard a factor by heuristic division.

## Complete algebraic cover and real embeddings

For each pair, regard the original equations as polynomials in x with
coefficients in Z[y]. Compute their Sylvester determinant by fraction-free
Bareiss elimination; every division is checked exact. Each determinant is
nonzero. Every common finite zero therefore projects to its zero, including
specializations where leading coefficients vanish.

The compact certificate supplies factors q(y). Their exact product equals the
primitive determinant, with multiplicities included. In Q[y]/(q), univariate
Euclidean division in x ends at `x-X(y)`. Every inverted leading coefficient
has its inverse identity checked modulo q. Therefore each division specializes
validly at every characteristic-zero root of q. The resulting chart is complete
and has no omitted exceptional fibre. Direct substitution independently checks
that `(X(y),y)` satisfies both original equations modulo q.

No irreducibility assumption is needed: quotient-ring operations invert only
checked units. The producer independently obtains the same rational coordinates
and factors from lexicographic Groebner bases. Every coordinate function is
compared exactly, not just by aggregate root counts.

The complete cover is:

| pair | off-circle chart degree | real off-circle values | unit-circle chart degree | circle slots |
|---|---:|---:|---:|---:|
| 318,340 | 24 | 6 | none | 0 |
| 318,341 | 21 | 3 | 3 | 3 |
| 319,340 | 21 | 3 | 3 | 3 |
| 319,341 | 24 | 6 | none | 0 |

Every q is checked squarefree. Rational Sturm counts verify one simple real
root in each stored interval and equality of the interval count with the total
real-root count. Thus all real embeddings are covered. A real y gives real
X(y); the verified norm equations make it an actual Euclidean parameter.
Complex roots are irrelevant to physical embeddings but may remain in algebraic
edge tests as a safe stronger obligation.

Both circle charts have q(y)=24y^3-6y-1. Their x coordinates are respectively
`2+3y-12y^2` and its negative. Exact reduction gives `X(y)^2+3y^2=1` in each
chart. The accepted h4139 theorem therefore disposes of these six parameter
slots. No new colouring search of the unit circle is performed.

## Exact coordinates and strict unit edges off the circle

For each real root y in an off-circle chart, the certificate defines

```
z = X(y)+i*sqrt(3)*y,
v_a = sum(d(a_j)*z^j,j=0..4),
d(0)=0, d(1)=1, d(2)=omega, a in {0,1,2}^5.
```

This is a complete exact coordinate specification of all 243 labels, with a
rational isolating interval for each embedding. The producer computes in the
Eisenstein basis `U+omega*V` using omega^2=omega-1. The verifier instead computes
Cartesian coordinates `A+i sqrt(3) B`, using

```
(A,B)*(C,D) = (A*C-3*B*D, A*D+B*C).
```

All coefficient polynomials are reduced modulo q. The 243 coordinate pairs
agree entry by entry through a canonical coordinate hash after the producer's
conversion `(U,V) -> (U+V/2,V/2)`.

For every label pair, squared physical distance is the exact rational polynomial
`N=(A_i-A_j)^2+3*(B_i-B_j)^2` modulo q. If N-1 is zero, the unit edge is verified
by a characteristic-zero polynomial identity. Otherwise the verifier checks
that N-1 is a unit modulo q over F_p with p=1,000,003. It similarly checks that
N is a unit for every displacement, ruling out every physical collision.
The prime is verified, q retains its degree, and every rational denominator
used in a checked residue remains nonzero modulo p.

The modular implication is exact. Localize Z by these denominators and q's
leading coefficient. The monic form of q gives a finite free coefficient
algebra. Multiplication by the tested polynomial is invertible modulo p, so its
determinant is nonzero over Q. It is therefore a unit over Q and cannot vanish
at any characteristic-zero q-root. This requires no irreducibility or
squarefreeness premise for the unit argument.

There are 29,403 label pairs per chart, or 117,612 across the four off-circle
charts. The checker reuses a norm result only after exact normalization by a
verified norm-one Eisenstein unit, leaving 2,801 distinct displacement classes
per chart. All 11,204 class checks are performed. The same proved edge set
applies to every real embedding in its chart; we do not claim 18 separate
repetitions of the label-pair loop.

Each strict graph has 243 distinct vertices and 405 edges. Inventory ownership
of every actual unit edge shows that the only active curves are its two source
curves. All four edge sets are coloured by

```
colour(a_0,...,a_4) = a_0+a_4 mod 3.
```

Every edge is checked against this word, and the permanent unit triangle proves
chromatic number exactly three. Within a chart distinct isolated y roots give
distinct parameters. Different source pairs cannot share an off-circle physical
parameter because each has exactly its own two active curves. Hence the four
canonical systems contain exactly 18 distinct off-circle parameter values.
We do not claim 18 nonisomorphic graphs.

## Frontier consequence and limits

The four systems were all in the inherited at-least-six mode: a counterexample
on one would have required more active curves, while its entire off-circle
physical locus has exactly two. The new proof supplies eight additional exact
forbidden pair conjunctions and deletes four global systems with conservative
allowance 40. Combined with h4191, no nontrivial-stabilizer pair system remains.

This is a complete decision of the declared finite stratum, with modest numerical
effect. It does not close all A5 graphs, prove a five-chromatic candidate, or
propagate all existing pair exclusions through the remaining pencils. The
remaining global accounting and its dependencies are stated in FRONTIER.md.
The new theorem is author-checked and awaits independent reviewer-1 assessment.
