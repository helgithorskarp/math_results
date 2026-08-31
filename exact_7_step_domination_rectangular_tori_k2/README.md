# Exact-7 obstruction for rectangular three-tori times `K_2`

## Result

Let

\[
G=C_m\mathbin\square C_n\mathbin\square C_p\mathbin\square K_2,
\qquad m,n,p\ge3.
\]

Then `G` has no exact 7-step dominating set of cardinality four or six.
Equivalently, no four or six translates of its radius-seven sphere partition
its vertex group.

This is a degree-seven abelian Cayley obstruction with exactly one
involutory coordinate generator.  It extends the rectangular three-torus
case, but does not cover arbitrary marked abelian quotients with three inverse
pairs and one involution.

## Finite reduction

Write `T` for the vertices at distance exactly seven from zero.  If `S` is an
exact 7-step dominating set, the translates `s+T`, for `s` in `S`, partition
the group.  Therefore

\[
2mnp=|S||T|.
\]

The exact Lee shells in three dimensions have sizes
`4r^2+2`.  The `K_2` coordinate is used zero or one time in a geodesic, so

\[
|T|\le(4\cdot7^2+2)+(4\cdot6^2+2)=198+146=344.
\]

Thus `2mnp <= 6*344 = 2064`, or `mnp <= 1032`.  The cycle-distance
enumerator

\[
P_q(x)=1+2\sum_{j=1}^{\lfloor(q-1)/2\rfloor}x^j
+[2\mid q]x^{q/2}
\]

gives the exact sphere formula

\[
|T|=[x^7](1+x)P_m(x)P_n(x)P_p(x).
\]

There are 1,106 unordered triples `3 <= m <= n <= p` under the product
bound, of which 1,074 have group order divisible by four or six.  Exact
evaluation leaves no four-center counting case and only four six-center
cases:

| `(m,n,p)` | `|T|` | projection modulus | fiber profile |
|---|---:|---:|---|
| `(4,9,9)` | 108 | 4 | `20,28,32,28` |
| `(6,7,11)` | 154 | 7 | `16,22,24,23,23,24,22` |
| `(6,9,10)` | 180 | 9 | `12,19,23,23,19,19,23,23,19` |
| `(8,9,9)` | 216 | 9 | `16,24,29,27,20,20,27,29,24` |

## Cyclotomic projection obstruction

Project a hypothetical translate partition onto the coordinate of the
displayed modulus `q`.  Let `c_r` count centers in coordinate fiber `r`, and
let `f_r` be the displayed sphere-fiber profile.  Summing the partition over
fibers gives

\[
c*f=|B|\mathbf 1_{\mathbb Z_q}.
\]

At every nontrivial `q`-th root of unity `zeta`, this implies
`C(zeta)F(zeta)=0`.  Exact polynomial division gives the following nonzero
remainders of `F` at every nontrivial cyclotomic factor:

```text
(4,9,9), q=4:    F mod Phi_2 = (-4); F mod Phi_4 = (-12)
(6,7,11), q=7:   F mod Phi_7 = (-6,0,2,1,1,2)
(6,9,10), q=9:   F mod Phi_3 = (-3); F mod Phi_9 = (-11,-4,4,0,-4)
(8,9,9), q=9:    F mod Phi_3 = (-3); F mod Phi_9 = (-11,-5,5,0,-9,-4)
```

Hence `C` vanishes at every nontrivial character, so the integer center
profile `c` is constant.  This forces `q` to divide the number of centers,
but none of `4, 7, 9, 9` divides six.  All four cases are impossible.

As an independent finite check of the last implication, the Python program
enumerates every weak composition of six into `q` fiber counts and directly
tests the cyclic convolution.  It rejects respectively 84, 924, 3,003, and
3,003 possible center profiles.

## Independent computations

The C++ enumerator scans the full triple universe and counts the sphere by
directly iterating over all vertices and their product-graph distances.  The
Python checker independently rescans with polynomial convolution, reconstructs
each surviving sphere by direct Cartesian enumeration, checks the exact
cyclotomic remainders, and exhausts all projected center profiles.

```bash
g++ -std=c++20 -O3 -DNDEBUG -march=native \
  -Wall -Wextra -Wpedantic \
  enumerate_rectangular_tori_k2.cpp \
  -o /scratch/enumerate_rectangular_tori_k2

/scratch/enumerate_rectangular_tori_k2 \
  /scratch/rectangular-tori-k2-candidates.txt

python3 check_rectangular_tori_k2.py \
  /scratch/rectangular-tori-k2-candidates.txt
```

A fresh run used GCC 12.2.0 and Python 3.11.2.  The deterministic four-line
candidate file and sources have SHA-256 values

```text
candidate file                         a76c8bd37db2e8dc8b05ee509fc064b90264f51725fc28963427b74cc4bd1ac1
enumerate_rectangular_tori_k2.cpp      b3bdbb9d82f734aa19148c8c29ed231e3ee4b3ab9b7f7697022fbd47d981128a
check_rectangular_tori_k2.py           aed381357b0ffeb4cc869580c60a8fc142a2112ef09608d77a51ac36a8a3e24f
```

Generated candidates and command output belong under `/scratch` and are not
committed.

## Status, trust boundary, and novelty scope

This is an exact computer-assisted theorem with a short algebraic obstruction
for every surviving counting case.  Its trust boundary is the
translate-partition reduction, the product-distance and shell formulas, the
complete bounded triple scans, exact cyclotomic arithmetic, the two
implementations, and their compiler/runtime.  All decisive arithmetic is
integral.  No heuristic result, SAT verdict, solver trace, or floating-point
calculation enters the theorem.

Targeted searches through 2026-08-31 found the foundational unique-coverage
exact-step papers and recent work using a different exact-distance convention,
but no prior obstruction for this family.  The result is therefore apparently
new to the searched sources, not a priority claim.

- P. Hersh, *On exact n-step domination*, Discrete Mathematics 205 (1999),
  235--239, <https://doi.org/10.1016/S0012-365X(99)00024-2>.
- L. K. Williams, *On Exact n-Step Domination*, Ars Combinatoria 58 (2001),
  13--22,
  <https://combinatorialpress.com/article/ars/Volume%20058/volume-58-paper-2.pdf>.
- S. Das, S. Das, and A. Sadhukhan, *Exact-Distance Domination in Grid
  Graphs*, arXiv:2607.29648 (2026), <https://arxiv.org/abs/2607.29648>.
