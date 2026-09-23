# Hasse obstructions for order-23 Ehlich-block Gram matrices

## Result

Let

\[
G(r_1,\ldots,r_s)=20I_{23}-J_{23}+4\bigoplus_{i=1}^sJ_{r_i},
\qquad r_1+\cdots+r_s=23,
\]

be an order-23 Ehlich-block matrix.  The published determinant record for a
sign matrix of order 23 is

\[
L=2^{22}\,3\,5^6\,67\,211
 =2^{22}\cdot662671875
 =2779447296000000.
\]

This artifact proves the following finite reduction.

> **Theorem.** Among the 1,255 integer partitions of 23, exactly 894 give
> `det(G) >= L^2`.  Exactly 16 of those determinants are rational squares, a
> necessary condition for `G=RR^T`.  Eleven of the 16 matrices are not even
> rationally congruent to the identity, and hence cannot equal `RR^T` for any
> rational matrix `R`, much less for a sign matrix.  The five partitions not
> excluded by this rational obstruction are
>
> ```text
> (9,8,2,2,2)
> (9,5,5,2,2)
> (5,5,5,5,1,1,1)
> (5,5,5,4,1,1,1,1)
> (5,5,5,3,2,1,1,1)
> ```

The full list of 16 candidates, square roots of their determinants, and every
bad finite prime found is in [`certificate.json`](certificate.json).  In
particular, this reduces the Ehlich-block part of any attempted improvement on
the order-23 record from 16 arithmetically possible partitions to five.

This does **not** determine the maximal determinant in order 23.  It neither
rules out the five rational survivors nor treats non-Ehlich-block Gram
matrices.

## Exact argument

The matrix determinant lemma gives

\[
\det G=20^{23-s}\prod_i(20+4r_i)
\left(1-\sum_i\frac{r_i}{20+4r_i}\right).
\]

If `G=RR^T`, then `det(G)=det(R)^2`.  Exact enumeration using the displayed
formula therefore leaves only the 16 square candidates above the record
threshold.

Now regard `G` as a quadratic form over the rationals.  If `G=RR^T` for a
nonsingular rational matrix `R`, then `G` is rationally congruent to the
identity.  By Hasse--Minkowski, its determinant square class and its local
Hasse invariants must agree with those of the identity.  For an exact rational
diagonalization

\[
G\sim\langle d_1,\ldots,d_{23}\rangle,
\]

the invariant at `p` is

\[
c_p(G)=\prod_{i<j}(d_i,d_j)_p.
\]

The verifier evaluates the rational Hilbert symbols directly.  A value
`c_p(G)=-1` is a checkable certificate of indecomposability.  The eleven
excluded candidates have the following bad places:

| partition | bad primes |
|---|---:|
| `(11,3,3,3,1,1,1)` | 3, 5 |
| `(11,3,3,1,1,1,1,1,1)` | 2, 3 |
| `(9,5,2,2,2,1,1,1)` | 2, 5 |
| `(9,4,2,2,2,1,1,1,1)` | 2, 5 |
| `(9,3,2,2,2,2,1,1,1)` | 2, 5 |
| `(8,5,5,5)` | 2, 5 |
| `(8,4,4,4,1,1,1)` | 2, 5 |
| `(6,6,6,2,1,1,1)` | 2, 3, 5, 11 |
| `(6,2,2,2,2,2,2,2,1,1,1)` | 2, 3, 5, 7 |
| `(5,5,2,2,2,2,2,1,1,1)` | 3, 7 |
| `(5,3,3,3,3,2,2,2)` | 2, 5 |

Primes outside 2 and the prime divisors of the diagonal coefficients have
trivial symbols, so the local check is finite.  Positivity handles the real
place, and Hilbert reciprocity is checked: every obstruction list has even
cardinality.

## Reproduction

Python 3.10 or later is sufficient; there are no third-party dependencies.

```bash
python3 verify.py
python3 independent_check.py
```

`verify.py` does all of the following with exact integer or rational
arithmetic:

1. verifies the published 23-by-23 record matrix and its determinant;
2. enumerates all 1,255 partitions of 23;
3. evaluates every Ehlich-block determinant;
4. directly recomputes each of the 16 candidate determinants by the Bareiss
   algorithm;
5. diagonalizes each candidate by rational symmetric elimination and computes
   every relevant local invariant; and
6. compares all results byte-for-byte with `certificate.json`.

As positive controls, it confirms that the supplied record Gram matrix and the
known decomposable order-15 optimum `G(4,4,4,3)` have no Hasse obstruction.

`independent_check.py` regenerates the partitions in the opposite order,
computes all determinants directly rather than with the closed formula, and
uses a second diagonalization.  It first splits off each block's internal
zero-sum directions and then diagonalizes only the block-sum core.  The two
diagonalizations agree on all bad-prime sets.

Typical runtime is under two seconds on an ordinary workstation.

## Known frontier and sources

Order 23 remains the smallest unresolved order of the Hadamard maximal
determinant problem.  Orrick, Solomon, Dowdeswell, and Smith published the
record matrix reproduced in `record23.txt` and the value `L` above in [*New
lower bounds for the maximal determinant problem*](https://arxiv.org/abs/math/0304410).
The corresponding general Ehlich bound quoted there is

\[
2^{22}\,3\,5^6\,675\sqrt{505}
\approx 2.9822953216\times10^{15}.
\]

The Ehlich-block determinant formula and broader state of the problem are
reviewed in [Browne--Egan--Hegarty--Ó Catháin](https://arxiv.org/abs/2104.06756).
The use of Hasse--Minkowski invariants as an exact indecomposability test for
candidate maximal-determinant Gram matrices is described by
[Brent--Orrick--Osborn--Zimmermann](https://arxiv.org/abs/1112.4160), and
[Tamura](https://doi.org/10.1002/jcd.20103) applies the same arithmetic
framework to block-structured D-optimal designs.

## Trust boundary

The mathematical input trusted here is the Hasse--Minkowski classification of
rational quadratic forms and the standard formulas for rational Hilbert
symbols.  The record matrix itself is checked, not trusted as a numeric
constant.  Exhaustiveness is over all integer partitions defining
order-23 **Ehlich-block** matrices; no claim of exhaustive enumeration of all
positive-definite candidate Gram matrices is made.  Absence of a bad prime is
only failure of this obstruction, not evidence that a sign decomposition
exists.
