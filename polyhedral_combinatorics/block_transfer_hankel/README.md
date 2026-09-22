# Weighted path transfers: exact Hankel product and minimal recurrence

For nonzero weights `w[0],...,w[N-1]` over any field, let
`C[i,j]=w[j]` when `i+j<N`, and zero otherwise. The weighted count of paths
on `k+1` vertices is `a[k]=w^T C^k 1`.

Write `v=(0,N-1,1,N-2,...)` for the zigzag order. For every `s>=0`,

\[
\det(a_{s+i+j})_{0\le i,j<N}
=\left((-1)^{N(N-1)/2}\prod_i w_i\right)^s
  \prod_{j=0}^{N-1}w_{v_j}^{2j+1}.
\]

Thus the length generating function has reduced denominator
`Q(y)=det(I-yC)` of degree exactly `N`. No smaller constant-coefficient
recurrence works, even eventually. An explicit tridiagonal inverse gives a
three-term continuant for `Q`; parity splitting reconstructs the entire
ordered weight vector from `Q`, using field arithmetic only.

For a path of blocks of width `a`, at fixed dilation `q`, substitute
`N=q+1` and `w[j]=binomial(j+a-1,a-1)`. The exact minimal recurrence order
in the number of blocks is `q+1` for every width `a>=1`. This addresses the
orthogonal-polynomial description in Jiang--Yang--Zhong, Problem 3. It does
not address gamma-positivity or roots of the Ehrhart numerator in the
dilation variable.

The anti-bidiagonal/Jacobi equivalence, inverse-Jacobi parity method, and
general Hankel/continued-fraction machinery are prior art. The proposed
addition is their explicit weighted path-count specialization and Hankel
product, with its minimality consequences. See [SOURCES.md](SOURCES.md) for
the precise boundary. No certified priority claim is made.

## Proof and reproduction

[PROOF.md](PROOF.md) gives a universal ordinary proof; finite checks are
auxiliary. Python 3.11+ and the standard library suffice:

```bash
python3 verify.py --check
sha256sum -c SHA256SUMS
```

Expected terminal line:

```text
PASS: Hankel products, minimal denominators, Jacobi recovery, and block counts
```

[expected.json](expected.json) records 387 rational weight vectors, 152
vectors over prime fields (including characteristic two), four Hankel shifts
per vector, and 105 comparisons with uncompressed coordinate-state counts.
The audit compares literal transfer moments and Newton determinants with
the Jacobi formulas, checks polynomial coprimality and weight recovery, and
includes zero-weight, invalid-input, and altered-denominator controls.
Checks raise explicit exceptions and remain active under `python3 -O`.

No solver, numerical eigenvalue calculation, external dataset, or large
certificate is required. This is not a formal proof-assistant certificate
or an independent review.
