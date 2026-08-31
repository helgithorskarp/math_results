# Degree-at-most-seven rectangular-product obstruction for exact-7 domination

## Combined theorem

Let

\[
G=\left(\mathop\square_{i=1}^{a} C_{m_i}\right)\mathbin\square Q_b,
\qquad m_i\ge3,
\qquad 2a+b\le7,
\]

where `Q_b=K_2 square ... square K_2`.  Then `G` has no exact 7-step
dominating set of cardinality four or six.

This class consists of the standard Cartesian-product Cayley graphs of finite
abelian groups whose coordinate connection set has degree at most seven.
It does not include diagonal or otherwise non-coordinate generating sets.

The degree-at-most-six cases follow from the complete abelian degree-six
obstruction.  At degree seven, `2a+b=7` leaves four types:

- `(a,b)=(0,7)` and `(1,5)` are covered by the five-involution degree-seven
  obstruction;
- `(a,b)=(3,1)` is covered by the rectangular three-torus times `K_2`
  obstruction;
- `(a,b)=(2,3)` is the new exact computation proved here.

Thus the cited results and the new component exhaust every standard
coordinate-product type of degree at most seven.

## New three-involution component

For all `m,n>=3`, put

\[
G=C_m\mathbin\square C_n\mathbin\square Q_3.
\]

Let `T` be its radius-seven sphere.  A four- or six-center exact dominating
set would tile the vertex group by translates of `T`, so

\[
8mn=|S||T|.
\]

The exact positive-radius Lee shell in two dimensions has size `4r`.  If
exactly `j` of the three binary coordinates are used, the remaining cycle
distance is `7-j`.  Hence

\[
|T|\le\sum_{j=0}^{3}\binom3j4(7-j)=176.
\]

It follows that `8mn<=6*176=1056`, or `mn<=132`.  With the cycle-distance
polynomial

\[
P_q(x)=1+2\sum_{j=1}^{\lfloor(q-1)/2\rfloor}x^j
+[2\mid q]x^{q/2},
\]

the exact sphere size is

\[
|T|=[x^7](1+x)^3P_m(x)P_n(x).
\]

There are exactly 144 sorted pairs `3<=m<=n` under the product bound.  Exact
evaluation leaves no four-center counting case and only

\[
(m,n,|T|)=(9,9,108)
\]

for six centers.

## Projection obstruction for the sole case

Project the translate partition onto one `C_9` coordinate.  If `c_r` counts
centers in coordinate fiber `r` and `f_r` counts sphere points there, then

\[
c*f=72\mathbf1_{\mathbb Z_9}.
\]

The exact sphere profile is

```text
f = 2,8,14,16,15,15,16,14,8.
```

For `F(x)=sum f_r x^r`, exact division gives

```text
F mod Phi_3 = (-3)
F mod Phi_9 = (-14,-6,6,0,1,7)
```

Both are nonzero, so `F` is nonzero at all eight nontrivial ninth roots of
unity.  Fourier-transforming the convolution forces the center profile to be
constant, which would require `9` to divide its sum `|S|=6`, a contradiction.

Independently, the Python checker enumerates all
`binom(14,8)=3003` weak compositions of six into nine center-fiber counts and
directly confirms that none has convolution constantly 72.

## Independent computations

The C++ enumerator scans every pair and counts each sphere by direct vertex
iteration and exact product distance.  The standard-library Python checker
independently rescans using polynomial convolution, reconstructs the sole
sphere by direct Cartesian enumeration, checks both cyclotomic remainders,
and exhausts every projected center profile.

```bash
g++ -std=c++20 -O3 -DNDEBUG -march=native \
  -Wall -Wextra -Wpedantic \
  enumerate_two_tori_q3.cpp \
  -o /scratch/enumerate_two_tori_q3

/scratch/enumerate_two_tori_q3 \
  /scratch/two-tori-q3-candidates.txt

python3 check_two_tori_q3.py \
  /scratch/two-tori-q3-candidates.txt
```

Fresh runs used GCC 12.2.0 and Python 3.11.2.  The deterministic one-line
candidate descriptor and sources have SHA-256 values

```text
candidate file                 cce687acd3738176e8b1f8e5ec2c529806ecc76b4df899b5a61fc214732935ed
enumerate_two_tori_q3.cpp      91885b842701dc36354a7afb2e618115e2dcc6967338e7613abd054624c46bb1
check_two_tori_q3.py           a6c2b7691667299f0a2f9f897e59d19f8c8d1d89eafb93a622811a8f321ec980
```

Generated candidates and run output belong under `/scratch` and are not
committed.

## Status and trust boundary

The new component is an exact computer-assisted theorem with an algebraic
obstruction for its sole counting case.  Its trust boundary is the
translate-partition and shell reductions, complete 144-pair scan, exact
product-distance and cyclotomic calculations, two independent
implementations, and ordinary compiler/runtime correctness.  The combined
degree-at-most-seven theorem additionally depends on the cited complete
degree-six, one-involution rectangular, and five-involution results.  No
heuristic or solver verdict enters any new claim here.

Targeted searches through 2026-08-31 found no prior obstruction for the new
family or the combined standard-product class.  The result is apparently new
to the searched primary sources, not a priority claim.

- P. Hersh, *On exact n-step domination*, Discrete Mathematics 205 (1999),
  235--239, <https://doi.org/10.1016/S0012-365X(99)00024-2>.
- L. K. Williams, *On Exact n-Step Domination*, Ars Combinatoria 58 (2001),
  13--22,
  <https://combinatorialpress.com/article/ars/Volume%20058/volume-58-paper-2.pdf>.
- S. Das, S. Das, and A. Sadhukhan, *Exact-Distance Domination in Grid
  Graphs*, arXiv:2607.29648 (2026), <https://arxiv.org/abs/2607.29648>.
