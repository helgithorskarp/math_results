# Proof of the vexillary dilation reduction

We use one-based positions and values.  Identity-block inflation replaces
the entry `w_i` by

```text
k(w_i-1)+1, ..., k w_i.
```

The positions and values belonging to each original entry therefore form
contiguous increasing blocks.

## 1. Vexillarity is preserved and reflected

Suppose four selected entries of `iota_k(w)` form the pattern 2143.  Two
selected entries from the same identity block occur in increasing position
and increasing value order.  The first two and last two entries of 2143 are
descents, so neither pair can lie in one block.  If a nonconsecutive selected
pair lies in one position block, every selected entry between it also lies
in that block; this would include one of those two descents.  Hence the only
remaining possibility is that the middle selected entries (the `1` and `4`
of 2143) lie in one block.

That possibility is also impossible.  The other two selected values (the
`2` and `3`) lie strictly between the middle two values.  But the values of
an identity block are a contiguous interval, while the value intervals of
distinct blocks are disjoint and totally ordered.  No value from a different
block can lie strictly inside that interval.  Thus all four selected entries
come from distinct blocks.  Projecting to their original blocks produces a
2143 pattern in `w`.

Conversely, a 2143 pattern in `w` lifts to one in `iota_k(w)` by choosing the
same residue in each of its four blocks.  Therefore

```text
iota_k(w) is vexillary  <=>  w is vexillary.                 (1)
```

## 2. Lehmer code, shape, and flag dilate exactly

Let `c_i` be the `i`th Lehmer-code coordinate of `w`.  Every entry in the
inflated block over `w_i` has inversions with all `k` entries over each later
value smaller than `w_i`, and has no inversion inside its own increasing
block.  Hence

```text
c_(k(i-1)+a)(iota_k(w)) = k c_i,       1 <= a <= k.          (2)
```

Let `lambda` be the weakly decreasing rearrangement of the positive code
coordinates.  Equation (2) gives

```text
lambda(iota_k(w)) = D_k(lambda(w)).                          (3)
```

For a vexillary permutation the canonical flag can be written

```text
b_s = max { i : c_i >= lambda_s }.
```

For any one of the `k` repeated rows of length `k lambda_s`, equation (2)
gives

```text
max { I : c_I(iota_k(w)) >= k lambda_s }
  = k max { i : c_i(w) >= lambda_s }
  = k b_s.                                                   (4)
```

Thus the flag is `D_k(b)`.

## 3. Reduction to one determinant inequality

The classical vexillary formula identifies the Schubert polynomial with the
flagged Schur polynomial:

```text
S_w = s_lambda(b).
```

At `x_1=x_2=...=1`, this is the number `F(lambda,b)` of semistandard
tableaux of shape `lambda` with entries in row `i` at most `b_i`.  Combining
(1), (3), and (4) gives

```text
Upsilon_(iota_k(w)) = F(D_k(lambda),D_k(b)).                 (5)
```

The flagged Jacobi--Trudi formula makes both sides explicit:

```text
F(lambda,b) = det( h_(lambda_i-i+j)(1^(b_i)) )_(i,j)
             = det( binom(b_i+lambda_i-i+j-1,
                           lambda_i-i+j) )_(i,j),             (6)
```

where `h_0=1` and `h_m=0` for `m<0`.  Equations (5)--(6) prove that the
all-`k` identity-inflation conjecture for a vexillary `w` is exactly

```text
F(D_k(lambda),D_k(b)) >= F(lambda,b)^(k^2).                  (7)
```

No claim that (7) is proved is made here.  The reduction identifies the
remaining obstacle without a permutation or Schubert-polynomial computation.

## 4. Why the obvious block injection is not yet a proof

The enlarged diagram has `k^2` times as many cells, tempting one to place
`k^2` input tableaux into its `k`-by-`k` cell blocks.  Scaling entries and
using residues enforces strictness inside each group of `k` replicated rows,
but the residue resets between two consecutive original rows.  Independent
input tableaux then need not satisfy the resulting boundary comparison.
Equivalently, concatenating the lattice paths for `k` path families does not
align their row-dependent intermediate endpoints.  The exact tests in this
directory support (7), but do not repair this boundary defect.
