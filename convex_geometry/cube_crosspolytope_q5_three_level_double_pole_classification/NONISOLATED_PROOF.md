# No non-isolated double-pole missing wall in active dimension five

## 1. Strengthened theorem

Fix ordered active weights

\[
                   (1,1,a,a,b),\qquad 0<b<a<1,\qquad B>0.     \tag{1}
\]

A *double-pole missing wall* is a missing wall reached by at least one
structural row whose supplier retains multiplicity two.  No restriction is
placed on how many other rows reach the wall.

**Theorem.**  Every double-pole missing wall under (1) is isolated: exactly
two rows reach it, one with unit supplier and one with \(a\)-supplier.
Consequently the three families in [`PROOF.md`](PROOF.md) are the complete
classification of **all** double-pole missing walls for (1), without an
isolation hypothesis.

The three surviving walls and exact parameters are unchanged:

1. \(b=N_1/D_1\), \(P_1(a)=0\), wall \(2b\);
2. \(b=N_2/D_2\), \(P_2(a)=0\), wall \(2a\);
3. \(b=-N_3/D_3\), \(P_3(a)=0\), wall \(2(2a+b)\),

with the polynomials, rational root intervals, and boundary values defined in
the earlier proof.

## 2. Why the previous leading classification remains complete

For five active coordinates, a residual double pole contributes \(H_3\) and
\(H_4\).  A residual simple pole contributes only \(H_4\).  Therefore a
simple-pole row joining a candidate wall cannot alter its leading \(H_3\)
equation.

Rows of the same repeated supplier have distinct walls under (1).  Hence a
vanishing \(H_3\) coefficient still requires one unit-supplier double-pole
row and one \(a\)-supplier double-pole row.  The 36-pair reduction in
[`PROOF.md`](PROOF.md) applies verbatim.  Five leading branches are uniformly
inadmissible, and every remaining candidate lies on one of these eight
rational branches:

| name | tail pattern \((\ell,h,i,g)\) | \(b\) |
|---|---|---|
| B01 | \((0,1,0,0)\) | \(N_1/D_1\) |
| B10 | \((1,0,0,0)\) | \(N_2/D_2\) |
| B11 | \((1,1,0,1)\) | \(-N_2/D_2\) |
| B20 | \((2,0,0,1)\) | \(N_3/D_3\) |
| B201 | \((2,0,1,1)\) | \(N_4/D_4\) |
| B21 | \((2,1,0,0)\) | \(-N_3/D_3\) |
| B211 | \((2,1,1,0)\) | \(-N_4/D_4\) |
| B212 | \((2,1,2,0)\) | \(N_1/D_1\) |

The notation \(D_j,N_j\) is equation (2) of the earlier proof.  These eight
branches are analyzed over the larger interval \(0<a<1\), before imposing
\(0<b<a\) or \(B>0\).  This makes the exclusion below stronger than needed.

## 3. Collision-factor reduction

On one of the eight branches, let \(\omega(a)\) be the common wall of the two
double-pole rows.  For every structural row \(r\), substitute the branch into
its wall and form

\[
                     d_r(a)=\omega_r(a)-\omega(a).       \tag{2}
\]

The complete row list has 33 elements: 12 unit-supplier, 12 \(a\)-supplier,
and 9 \(b\)-supplier rows.  Exactly the intended two differences vanish
identically on every branch.  Each of the other 31 is rational in \(a\).

Factor the numerator of every nonzero \(d_r\) over \(\mathbb Q\), and discard
factors having no root in \((0,1)\).  The resulting exact census is:

| branch | collision factors | roots in \((0,1)\) |
|---|---:|---:|
| B01 | 0 | 0 |
| B10 | 13 | 13 |
| B11 | 14 | 14 |
| B20 | 6 | 7 |
| B201 | 7 | 11 |
| B21 | 4 | 5 |
| B211 | 9 | 12 |
| B212 | 6 | 6 |
| **total** | **59** | **68** |

The maximum factor degree is 19.  This table is not a numerical root search:
factorization is over \(\mathbb Q\), and every open-interval root count is a
Sturm count.  After all recorded factors are divided from each wall-difference
numerator, the residual polynomial has no root in \((0,1)\).  Thus every
possible additional row collision is covered.

## 4. Aggregate coefficient certificate

Fix one recorded collision factor \(F(a)\).  Let \(S_F\) contain the two
generic double-pole rows and every other row whose difference numerator in
(2) is divisible by \(F\).  At a root of \(F\) where the parameters are
defined, \(S_F\) is exactly the set of rows at the wall.  Different recorded
factors on the same branch are pairwise coprime, and the verifier also rejects
any proper nonconstant gcd between \(F\) and a row-difference numerator.  This
prevents an unrecorded partial-factor stratum.

Let

\[
                        C_F(a)=\sum_{r\in S_F}c_{4,r}(a)             \tag{3}
\]

be the full aggregate \(H_4\) coefficient, including all labeled-tail
multiplicities.  Exact reduction gives

\[
                 \gcd\!\left(F,\operatorname{num} C_F\right)=1     \tag{4}
\]

for each of the 59 factors.  Therefore no root of a collision factor can
make the aggregate \(H_4\) coefficient vanish.  If a denominator also
vanishes, the branch or row is undefined there and cannot supply an
admissible parameter; it creates no exception to (4).

Thus a candidate with an additional row never disappears.  Every
double-pole missing wall is isolated, and the earlier exact three-family
classification is complete. \(\square\)

## 5. Reproducible certificate and trust boundary

[`COLLISION_CERTIFICATE.json`](COLLISION_CERTIFICATE.json) stores the 59
primitive collision polynomials in ascending coefficient order, their exact
open-unit root counts, the rows colliding on each factor, and the degree-zero
aggregate gcd result.  Its canonical JSON SHA-256 is

```text
81d03a5d6051fd1f94a933b348b0fff00373a1606a2f5bfeaf525fbe64ea95f0
```

`derive_nonisolated.py` reconstructs the complete global expansion in SymPy
1.13.3 and generates the certificate.  `verify_nonisolated.py` imports no
SymPy code.  Using only standard-library integer and rational arithmetic, it
reconstructs all 33 rows from regularized principal parts and tail moments,
checks the certificate coverage by Sturm sequences, recomputes every
colliding-row set, and verifies all 59 gcds.

The strengthened theorem inherits the global weighted ray-chamber formula
and the eight-branch leading classification.  The new finite certificate
closes exactly the previously excluded non-isolated strata.  No floating-point
quantity is used to decide a claim.
