# Exact moment obstruction for all 16 record-level candidates

## Statement

For a partition `r=(r_1,...,r_s)` of 23, write

\[
G(r)=20I_{23}-J_{23}+4\operatorname{diag}(J_{r_1},\ldots,J_{r_s}).
\]

The determinant enumeration in `verify.py` leaves exactly 16 Ehlich-block
partitions whose determinants are squares at least as large as the square of
the published order-23 record.  None of those 16 matrices has a decomposition
`G(r)=XX^T` with `X` a 23-by-23 sign matrix.  Consequently no order-23 sign
matrix at or above that record can have an Ehlich-block row Gram matrix.

This proof is independent of the Hasse--Minkowski exclusions in
`certificate.json`: it uses only finite block-sum enumeration and exact second
moments.

## Necessary column types

Suppose for a contradiction that `G=XX^T`.  Put

\[
H=20I_{23}+4\operatorname{diag}(J_{r_1},\ldots,J_{r_s}),
\quad G=H-\mathbf1\mathbf1^T,
\]

and set `d_i=20+4r_i` and

\[
q=1-\sum_i\frac{r_i}{d_i}>0.
\]

On block `i`,

\[
H^{-1}=\frac1{20}I-\frac1{5d_i}J,
\qquad H^{-1}\mathbf1=\frac1{d_i}\mathbf1.
\]

Sherman--Morrison therefore gives, for a sign vector `v` with block sums
`u_i`,

\[
v^TG^{-1}v=\frac{23}{20}-\sum_i\frac{u_i^2}{5d_i}
 +\frac{(\sum_i u_i/d_i)^2}{q}.
\]

Every column `v` of `X` satisfies `v^TG^{-1}v=1`, since
`X^TG^{-1}X=I`.  Hence its block-sum vector must satisfy

\[
\boxed{
 \sum_i\frac{4u_i^2}{d_i}
 -\frac{20}{q}\left(\sum_i\frac{u_i}{d_i}\right)^2=3.}
\tag{1}
\]

Moreover,

\[
u_i\equiv r_i\pmod2,\qquad |u_i|\le r_i.
\tag{2}
\]

Multiplying a column of `X` by `-1` leaves `XX^T` unchanged.  Because the
column length is odd, choose each sign so that

\[
\sum_i u_i\equiv3\pmod4.
\tag{3}
\]

Equations (1)--(3) define a finite and complete list `T(r)` of normalized
column types.

## The moment identity

Let `P` sum coordinates inside each row block.  If the normalized columns of
`X` have types `u^(1),...,u^(23)`, then

\[
\sum_{a=1}^{23}u^{(a)}u^{(a)T}=PXX^TP^T=PGP^T=W,
\tag{4}
\]

where

\[
W_{ij}=r_i(20+4r_i)\delta_{ij}-r_ir_j.
\tag{5}
\]

Thus a quadratic polynomial

\[
f(u)=c+\sum_{i\le j}a_{ij}u_i u_j
\]

that is nonnegative on `T(r)` must obey

\[
0\le\sum_{a=1}^{23}f(u^{(a)})
=23c+\sum_{i\le j}a_{ij}W_{ij}.
\tag{6}
\]

For 15 candidates, the following exact certificates make the right side of
(6) negative.  The remaining partition has no type satisfying (1)--(3), so a
hypothetical matrix could not have even one column.  Indices in the table are
one-based.

| partition `r` | `|T(r)|` | polynomial `f(u)` | range on `T(r)` | value from (6) |
|---|---:|---|---:|---:|
| `(11,3,3,3,1,1,1)` | 2 | `-3 - u1u2` | `[0,4]` | -36 |
| `(11,3,3,1,1,1,1,1,1)` | 1 | `-3 - u3u7` | `[0,0]` | -66 |
| `(9,8,2,2,2)` | 3 | `6u1u3 + 14u2u3 - 13u3u4` | `[0,0]` | -280 |
| `(9,5,5,2,2)` | 22 | `5u1u2 + 5u1u3 - u2u3 + 10u2u4 + 10u2u5 - u3^2 + 10u3u4 + 10u3u5` | `[0,0]` | -1000 |
| `(9,5,2,2,2,1,1,1)` | 2 | `-81 + u1^2` | `[0,0]` | -1440 |
| `(9,4,2,2,2,1,1,1,1)` | 4 | `u1^2 - 81u9^2` | `[0,0]` | -1440 |
| `(9,3,2,2,2,2,1,1,1)` | 4 | `u1^2 - 81u9^2` | `[0,0]` | -1440 |
| `(8,5,5,5)` | 4 | `-1 + u2u3` | `[0,24]` | -48 |
| `(8,4,4,4,1,1,1)` | 3 | `u3u6 + 4u5u6` | `[0,6]` | -8 |
| `(6,6,6,2,1,1,1)` | 1 | `-2 - u4u7` | `[0,0]` | -44 |
| `(6,2,2,2,2,2,2,2,1,1,1)` | 43 | `u10u11 - u11^2` | `[0,0]` | -24 |
| `(5,5,5,5,1,1,1)` | 37 | `-1 + u5u6` | `[0,0]` | -24 |
| `(5,5,5,4,1,1,1,1)` | 46 | `5u1u2 + 5u1u3 + 6u1u5 + 4u2u3` | `[0,380]` | -380 |
| `(5,5,5,3,2,1,1,1)` | 13 | `u1u5 + 10u6u7` | `[0,16]` | -20 |
| `(5,5,2,2,2,2,2,1,1,1)` | 0 | no column type exists | — | — |
| `(5,3,3,3,3,2,2,2)` | 2 | `-2u1u6 - 5u6^2` | `[0,0]` | -240 |

Each row is already a contradiction, proving the statement.

## Exhaustive verification

`moment_obstruction.py` enumerates the Cartesian product in (2), filters it
by (1) and (3) using `fractions.Fraction`, and checks all 16 obstructions
against `moment_certificate.json`.  The certificate records the SHA-256 hash
of every canonical type list.  As a positive control on (1)--(5), the script
constructs a Sylvester Hadamard matrix of order 8, deletes its normalized
first row and column, and verifies the resulting order-7 decomposition and
all of its column moments.

`independent_moment_check.cpp` starts instead from all `2^23` sign columns for
each candidate.  It keeps the half with normalized total sum, projects them to
block sums, and checks a denominator-cleared integer form of (1).  It
independently obtains all 16 type sets and certificate ranges.  Its largest
common denominator is 3,360, its largest absolute weighted sum is 2,235, and
the largest square term used in the cleared identity is below 100,000,000, so
signed 64-bit arithmetic has a wide safety margin.

The finite block-sum criterion is a direct specialization of the imbalanced
Ehlich-block necessary conditions described by Hiroki Tamura in [*Ehlich
block matrices*](https://www.kurims.kyoto-u.ac.jp/~kyodo/kokyuroku/contents/pdf/1465-8.pdf),
Theorem 4.  The derivation above is included so that the proof does not depend
on interpretation of the scanned source.
