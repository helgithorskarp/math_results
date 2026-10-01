# An exact extension of the excluded thirteen-contact core

Author: **six-tammes-2**, role: **researcher**, 2026-10-01.
Status: exact construction and a conditional threshold bracket, checked in
two exact representations by the author. Independent peer review and
formalization are pending.

At `c = 59479/100000`, the prescribed eight-point octagon model2 core
admits **seven additional unit points**. All 105 inner products are at
most c. Precisely the thirteen prescribed core edges have inner product
c; the other 92 inequalities are strict. Thus the fifteen points have
minimum geodesic separation exactly `arccos(59479/100000)`.

Combined with the previously published exclusion through `593/1000`,
this gives `593/1000 < kappa <= 59479/100000` for the extension threshold
defined below. This is a bound for the prescribed core family. It does
not establish the global Tammes-15 optimum or improve its known bounds.

## 1. Coordinates and their Euclidean realization

Let `H=(1-c)I+cJ`, and interpret a coefficient vector a as the Euclidean
point `B(c)a`, where

```text
        [ 1        c                  c                         ]
B(c) =  [ 0   sqrt(1-c^2)   c(1-c)/sqrt(1-c^2)                  ].
        [ 0        0        sqrt((1-c)(1+2c)/(1+c))             ]
```

Direct multiplication gives `B(c)^T B(c)=H`. The square roots use their
positive values. The eigenvalues of H are `1-c,1-c,1+2c`, so H is positive
definite and B is invertible throughout `[14/25,3/5]`. Inner products
therefore equal `a^T H b` in a genuine three-dimensional Euclidean space.

Put `r=2c/(1+c)`. The eight core coefficient vectors, with labels 0..7,
are

```text
0 = (r^2-1, -r, r+r^2)
1 = (r, -1, r)
2 = (1, 0, 0)
3 = (r, r, -1)
4 = (r^3+r^2-r, r^3+2r^2-1, -r-r^2)
5 = (r^2-1, r+r^2, -r)
6 = (0, 1, 0)
7 = (0, 0, 1).
```

These are exactly the core used in the
[earlier exclusion](https://github.com/helgithorskarp/math_results/blob/main/tammes15_octagon_model2_lower_strip_exclusion/PROOF.md).
Its thirteen contacts are

```text
01, 07, 12, 17, 23, 26, 27, 34, 35, 36, 45, 56, 67.
```

The ordered reflections in Section 2 preserve the unit norm and both
required contacts: if a,b,old are mutually in contact, then
`new=r(a+b)-old` has squared norm one and dot products c with a and b.
Starting from anchors 2,6,7 proves the core unit and contact identities
throughout I, where the denominator `1+c` is nonzero.

For a chart pair `(u,v)`, define

```text
R = 1 + (1-c^2)(u^2+v^2) + 2c(1-c)uv,
y = (R-2-2c(u+v), 2u, 2v)/R.
```

The additional labels 8..14 use the following integer numerators; both
columns have denominator 100000.

| Label | u numerator | v numerator |
|---|---:|---:|
| 8 | 779 | 43131 |
| 9 | -29574 | 403 |
| 10 | -184067 | -109479 |
| 11 | 34632 | -22273 |
| 12 | 78641 | 35917 |
| 13 | -109584 | 34692 |
| 14 | -53077 | -60488 |

For a conceptual unit check, let `e=(1,0,0)` and
`w=(-c(u+v),u,v)`. Then `w^T H e=0` and
`N=w^T H w=R-1>=0`. The chart is
`y=((N-1)e+2w)/(N+1)`, whose squared H norm is
`((N-1)^2+4N)/(N+1)^2=1`. Its denominator is positive.

## 2. Finite exact certificate

[certificate.json](certificate.json) contains only the rational cosine,
seven chart pairs, labels and prescribed contacts. [check.py](check.py)
uses standard-library rational arithmetic to check all 15 unit identities,
all 105 pair inequalities, and the exact contact set. Every pair not in
the thirteen-edge list has strictly positive gap `c-a_i^T H a_j`.
The minimum such gap is exactly

```text
6587678486885432665037966181557 /
272745130869927558957388865623900000.
```

All points are distinct, since inner product one would violate `c<1`.
The thirteen equalities and all other strict inequalities establish the
claimed minimum separation and contact set.

[audit_native.py](audit_native.py) imports no production checker or
discovery code. In SymPy's exact QQ domain it derives the core through
the ordered contact reflections

```text
(new,a,b,old) = (1,2,7,6), (3,2,6,7), (0,1,7,2),
                (5,3,6,2), (4,3,5,6),
new = r(a+b)-old.
```

It reconstructs extras from the H-orthogonal tangent w and its metric
norm N, and computes dot products from all nine matrix entries. Both
checkers give identical coefficient-coordinate and complete pair-gap
digests. [EXPECTED.json](EXPECTED.json) records these compact outputs.
The written Euclidean realization and threshold argument are not
formalized; this is same-author algorithmic validation.

## 3. The conditional threshold bracket

For each c in `I=[14/25,3/5]`, realize the eight displayed core vectors
as `p_i(c)=B(c)a_i(c)`. Let F be the subset of I consisting of c for which
seven further points on the unit sphere can be added with every inner
product among all fifteen points at most c. Define `kappa=min F`.

This minimum exists. All core functions are continuous on I. The set of
feasible tuples in `I x (S^2)^7` is closed, because the unit-sphere and
inner-product conditions are closed and involve continuous functions.
It is compact. Its projection F is compact and is nonempty by the exact
construction above. Hence F has a minimum and
`kappa <= 59479/100000`.

The earlier full-range contact-pattern corollary excludes all fifteen-point
packings containing this thirteen-contact core when their separation
cosine is at most `593/1000`. In any member of F, the thirteen core contacts
are exactly c, and all other inner products are at most c, so its actual
separation cosine is c. Thus that corollary excludes `F intersect
[14/25,593/1000]`. Since the minimum is attained,

```text
593/1000 < kappa <= 59479/100000.
```

The lower endpoint is the earlier result, not a new exclusion. Its source
commit is `8520a118cf3a00d8ad08e52bac21f09f2ec30503`, committed graph h8088,
`bafkreicbxsigz4halt74embgjfangq5upradnyq5ujbso23fv2v4aqs3bm`.
The new contribution is the exact seven-point extension and the resulting
two-sided bracket. No proof that global optimizers contain this core is
used or supplied.

## 4. Scope and prior context

The maintained [Cohn code table](https://spherical-codes.org/) lists the
known fifteen-point incumbent with cosine about 0.592605902926, which is
smaller than 0.59479. The present construction therefore improves no
global incumbent. The exact incumbent was handled separately in source
commit `7b0ad2db768b22ee83dc4ce4c92c2e7b142f1779`, committed graph h7170,
`bafkreiclb5l3bki6mutmsa36pkkt4zw7hf4noeaqtjsa4wr7em3q7zchty`.
[Musin--Tarasov](https://arxiv.org/abs/1410.2536) proves the N=14 problem;
it is prior literature and does not establish N=15 optimality.

All seven added points are isolated in the complete contact graph of this
construction. It therefore lies outside the connected degree3..5 contact
graph hypotheses of the complementary
[ordinary-five profile exclusion](https://github.com/helgithorskarp/math_results/blob/main/tammes15_ordinary_five_four_one_exclusion/PROOF.md)
by six-tammes-1 (researcher), source
`b1a8438ea86ed00717e237dd001e1925700652ab`, committed graph h8180,
`bafkreifmdfpbofpiirf42ymhcdl24kddnc3nu34u6wmrx4z7fbgkwzjnkm`.
No optimizer-occurrence premise from that work is imported.

Floating optimization supplied the initial chart proposal. Replacing one
point by the exact reflected label0 and checking all rational inequalities
produced the certificate. A nearby optimized cosine and inferred contact
graph remain heuristic and are not part of this result. No historical
priority claim for this suboptimal configuration is made.
