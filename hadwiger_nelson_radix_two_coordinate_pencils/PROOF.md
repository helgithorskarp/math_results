# Complete exclusion of the two-coordinate five-pencil subset

## Statement and finite scope

Let `A5(z)=T+zT+z²T+z³T+z⁴T`, where `T={0,1,ω}` and
`ω²=ω−1`, with positive imaginary part. Use the original h4105 event-curve
IDs. HN3 h4171 identifies every possible exactly-five-active counterexample
with a full affine pencil of five F4 failure hyperplanes.

We decide the complete named subset in which the five normal directions are
supported on two of the four nonconstant radix positions. Equivalently its
sorted normal-support profile is `(1,1,2,2,2)`. There are **54 realized
pencils and 6,912 lifted curve quintets**. None has a common point even in the
complex affine parameter plane. The exclusion therefore also holds when more
than five curves are active. No other support profile is tested here.

## 1. Complete pencil enumeration

For a unit-normalized displacement row `(a_0,...,a_4)` over E=Z[ω], reduce its
coefficients in E/(2)=F4. Its failure hyperplane has equation
`sum_{j=1}^4 a_j w_j = a_0`, up to a common nonzero field scalar. Since a
nonzero displacement coefficient is an Eisenstein unit, its residue is
nonzero. Thus support in F4 is exactly support in the characteristic-zero row.

Choose positions `1<=i<j<=4`. The five projective normal directions in this
coordinate plane are `(1,0),(0,1),(1,1),(1,ω),(1,ω²)`. The first two affine
constants must be nonzero: constant zero there gives a monomial radial event,
not a noncircle curve. There are three choices for each constant, hence nine
realized full pencils for each of six position pairs. Their five buckets have
sizes 2,2,2,4,4; hence each pencil has 128 lifts and the total is 6,912.

The producer constructs these pencils by affine F4 linear combinations. The
independent checker instead enumerates five distinct directions from the 18
realized hyperplanes in F4² and tests that their masks cover all 16 points. It
finds exactly nine covers, embeds them in all six position pairs, and uses
the reviewer's independent h4151 row/norm inventory to reconstruct every
lift. Both paths agree on every normalized lift, not just the aggregate count.

## 2. Unit normalization and exact elimination

Fix one lift. Its two singleton equations can be normalized as

```
(1+U)(1+Z)=1,       (1+V)(1+W)=1,
U=alpha*u^i,       Z=conjugate(alpha)*v^i,
V=beta*u^j,        W=conjugate(beta)*v^j,
```

where alpha,beta are Eisenstein units. For a physical parameter,
`u=z`, `v=conjugate(z)`. More generally the invertible complex coordinate
change `u=x+i√3 y`, `v=x−i√3 y` turns the original real norm polynomials into
the same bilinear equations over the complex affine plane.

Each of the remaining three equations has form

`(a+bU+cV)(a*+b*Z+c*W)=1`,

where `*` conjugates coefficients in E. Unit row rescaling changes neither
equation. Dividing the two anchor rows out of the other coefficients and
canonicalizing gives **32 normal forms**, each representing exactly 216 of
the original 6,912 lifts. The checker verifies both normalized anchors, every
phase being a unit, every row's support, and the full normalization transcript.

The anchors imply `1+U != 0`, `1+V != 0` and

`Z=−U/(1+U)`, `W=−V/(1+V)`.

Put `D=(1+U)(1+V)`. For a remaining row define the exact cubic

```
g = (a+bU+cV) [a*(1+U)(1+V)−b*U(1+V)−c*V(1+U)] − D.
```

Every original common zero makes its three cubics zero and has D nonzero.
There is no division by a quantity that could vanish on an original solution.

## 3. Explicit polynomial certificates

For **31 normal forms**, the certificate supplies three multipliers in
Q(ω)[U,V] satisfying

`h_1 g_1 + h_2 g_2 + h_3 g_3 = D²`.

Thus these forms would force D=0, contrary to the anchor equations. All these
multipliers have degree at most two.

For the remaining form it supplies two identities:

```
sum h_k g_k = D²(U−V),
sum j_k g_k = D²(4V²+V+1).
```

Their multiplier degrees are at most three and four, respectively. The
13,081-byte certificate contains all **33 identities**. Its checker uses only
integer/Fraction arithmetic and explicit multiplication in Q(ω); it does not
trust a Gröbner-basis claim, modular lifting or a solver verdict. Generation
uses exact rational linear algebra in SymPy after splitting coefficients into
the basis {1,ω}. The Gröbner calculation used to find these targets is not a
proof dependency.

## 4. The exceptional form needs the common radix parameter

The exceptional normalized rows, in coefficient triples, are

```
(-1,-1,0), (-1,ω−1,−ω), (-1,−ω,ω−1), (-1,0,-1), (0,-1,-1).
```

The identities force `U=V` and `4V²+V+1=0`. The latter implies V nonzero.
The anchor formulas give `Z=W` and

`UZ=VW=−V²/(1+V)=1/4`.

Set `r=u*v`. Unit phases cancel, so `UZ=r^i`, `VW=r^j`. Hence
`r^i=r^j=1/4`. With `d=j−i>0`, this gives `r^d=1` and then both
`(r^i)^d=4^(−d)` and `(r^d)^i=1`, a contradiction in characteristic zero.
This treats all six exponent pairs and proves complex affine nonconcurrence.

The common-power step is essential. In a relaxation where U and V are
independent vectors, the exceptional form has the genuine solutions
`U=V=(−1±i√15)/8`, with squared modulus 1/4. The controls retain this
relaxation exactly by reducing on the diagonal modulo `4t²+t+1`. They reject
a certificate that replaces the exceptional step by a denominator
contradiction. No claim that all 32 free two-vector systems are inconsistent
is made.

## 5. Effect on the shared higher-incidence frontier

This removes all 54 two-coordinate pencils and all 6,912 of their lifts from
the h4171 necessary survivors. The earlier h4167 pair/triple rules removed
none of this profile, so the marginal reduction is exactly 6,912. The
remaining h4171 counts are **5,328 realized pencils and 132,225,984 quintets**.

Two distinct normal directions and their affine constants determine a unique
full pencil. Consequently, if a retained exact-five pair belongs to one of the
closed pencils, it cannot extend to a different exact-five pencil. Consuming
HN3's newest named mode/stabilizer interface identifies **192 such pair
representatives**: 164 with trivial stabilizer, 28 with order-two stabilizer.
Their product-surface allowance is 4,112 and their non-four orbit allowance is
3,860. They now require at least six active curves.

The exact-five mode therefore has 128,424 pairs and conservative allowance
3,763,324. The at-least-six mode has 2,932 pairs and allowance 83,380. The
whole frontier stays at **131,356 systems and allowance 3,846,704**: a pair
can participate in a larger cover without containing a forbidden quintet, so
no complete global pair is deleted. These mode counts import h4117 cover
completeness, h4171's exact-five classification and the newest HN3 accounting;
the standalone 6,912-quintet nonconcurrence theorem does not need those
global-cover assumptions.

This completes the declared named-subset decision. It does not close all
five-active or six-or-more-active cases, produce a physical non-four-colourable
graph, or improve the 509-vertex record.
