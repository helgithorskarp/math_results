# Proof certificate

## 1. The isolated nine-point source

Let `K=Q(rho)` with `rho^2-rho+1=0`.  Multiplication and norm in the basis
`1,rho` are

```text
(a+b*rho)(c+d*rho) = (ac-bd) + (ad+bc+bd)rho,
N(a+b*rho) = a^2+ab+b^2.
```

Fix one source generator at `1` and write the other two as `z=(x,y)` and
`w=(u,v)` in this basis.  `verify.py` constructs four rational quadratic
polynomials `F`.  At the rational midpoint `m`, the certificate gives a
rational matrix `Y` approximating `DF(m)^-1`.  With box radius `r=10^-35`,
the verifier computes exactly

```text
beta  = ||I-Y DF(m)||_infinity,
B     = ||Y||_infinity,
L     = max_i sum_(j,k) |d^2 F_i/(dx_j dx_k)|,
eta   = beta + B L r,
delta = ||Y F(m)||_infinity + eta r.
```

It proves `beta<10^-64`, `eta<10^-33`, and `delta<10^-68<r`.
Therefore `T(x)=x-YF(x)` is a contraction from the closed box to itself and
has a unique fixed point there.  Because `Y` is invertible (already implied
by its sufficiently small inverse defect), that fixed point is the unique
zero of `F` in the box.

The nine source points are exact affine expressions in `1,z,w`.  Direct
polynomial comparison reduces the squared norms of their 15 edges to exactly

```text
1, 1+F0, 1+F1, 1+F2/3, 1+F3.
```

Thus all five direction orbits are exactly unit at the isolated root.

## 2. Complete equilateral closure

For every current unit segment `a,b`, the next support includes

```text
a + rho*(b-a),
a + (1-rho)*(b-a).
```

The checker stores no rounded coordinates or imported edge list.  It
regenerates affine coefficient vectors exactly, merges equal vectors, and
recognizes a unit edge only when its difference is a sixth-root rotation of
one of the five source directions.  This gives the ten censuses in the README.

To prove completeness, each affine point is evaluated at the rational source
midpoint.  Its coordinate error is bounded from its exact linear sensitivity
times `r`.  For an interval pair `(a,b)` in the `1,rho` basis, ordinary
rational interval multiplication encloses `a^2+ab+b^2`.  Every pair in rounds
8 and 9 is checked.  Declared edges have intervals containing one; every
undeclared pair has an interval disjoint from one; every distinct formal pair
has positive squared-distance lower bound.  Hence the exact physical graphs
really have 432/1,134 and 533/1,415 points/edges respectively.

## 3. Chromatic decision and cap stop

Deterministic exhaustive DSATUR rejects a three-colouring of the embedded
nine-point source in 27 search nodes.  The supplied 432-character word is
proper on the complete round-8 edge set, so round 8 has chromatic number
exactly four.  Round 9 has 533 distinct points, so no next **complete** closure
round can meet the at-most-508 target.

This is a positive-certificate result.  No SAT UNSAT response, numerical
equality, unlogged solver proof, or omitted external graph is a premise.
