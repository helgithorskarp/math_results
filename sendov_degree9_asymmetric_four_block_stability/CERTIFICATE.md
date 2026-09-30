# Exact sign certificate

Author **six-sendov-2**, role **researcher**.

The dummy third polynomial axis has degree zero and interval [0,1].
The following eleven two-dimensional boxes regenerate all 860 new rational
Bernstein coefficients. Nonnegative minima include collision boundaries;
strictly positive minima also give the stated cap lower bound.

| Certificate | First interval | Second interval | Tensor degree | Entries | Zeros | Minimum |
| --- | --- | --- | --- | --- | --- | --- |
| majority_cap | [0, 1/4] | [0, 1/4] | [9, 8] | 90 | 0 | 98784 |
| majority_exterior_0 | [1/2, 1] | [0, 1] | [10, 5] | 66 | 2 | 0 |
| majority_exterior_1 | [1/32, 1/2] | [1/2, 1] | [10, 5] | 66 | 0 | 18784495758391155/120259084288 |
| majority_exterior_2 | [17/64, 1/2] | [0, 1/2] | [10, 5] | 66 | 2 | 0 |
| majority_exterior_3 | [1/32, 17/64] | [1/4, 1/2] | [10, 5] | 66 | 0 | 944965601089735606137/18014398509481984 |
| majority_exterior_4 | [19/128, 17/64] | [0, 1/4] | [10, 5] | 66 | 0 | 211625309020860576770625/9223372036854775808 |
| majority_exterior_5 | [1/32, 19/128] | [0, 1/8] | [10, 5] | 66 | 0 | 2176547358021666009327/720575940379279360 |
| majority_exterior_6 | [1/32, 19/128] | [1/8, 1/4] | [10, 5] | 66 | 0 | 3841259900509715690925/576460752303423488 |
| majority_large_r | [0, 1/16] | [1/4, 1] | [10, 5] | 66 | 0 | 811797/16 |
| singleton_0 | [0, 1/7] | [0, 1] | [10, 10] | 121 | 4 | 0 |
| singleton_1 | [1/7, 1/3] | [0, 1] | [10, 10] | 121 | 4 | 0 |

The first cap polynomial is (j_N D-j_D N)/k in k,r. The seven
majority exterior boxes use h=k/2 and z=r/(1-h)^2, and the polynomial
is (780D-N)(2h,(1-h)^2z). They cover [1/32,1] x[0,1]. The next box
uses 780D-N in k,r on[0,1/16] x[1/4,1]. The two singleton boxes
use (780D_s-N_s)(t,(1-t)z) and cover [0,1/3] x[0,1].

Coverage checks every open cell induced by all rectangle boundaries,
requires exactly one covering rectangle, verifies containment and exact
total area, and uses closure for the boundaries. All transforms are
inverted back to the normalized power polynomial coefficient by coefficient.

The separate credited scalar-loss reproduction has six strictly positive
coefficients, minimum 141084. It is not included in the 860 new entries.

Complete coefficient-record SHA-256: 72bee72290d5662e8f8d42ee7fef4b5a1450b2b5a9edd552199f8bcbdfb49590.

The 21-term active trace numerator, 10-term discriminant, individual
polynomial and coefficient hashes, seventeen rational definition controls,
optimizer bracket, basin bracket, and shortcut obstruction are all in
expected.json. Every fixture field is regenerated and compared as one
complete object; checks remain active under optimized Python. The input
is compact source plus the small expected manifest, without solver or
floating arithmetic. The universal spectral, continuity, coverage and
basin interpretation is the ordinary proof in PROOF.md.
