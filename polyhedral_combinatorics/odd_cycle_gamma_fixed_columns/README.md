# Odd-cycle gamma columns are eventually positive

Let

\[
Q_m=\{x\in\mathbb R_{\ge0}^m:x_i+x_{i+1}\le1\}
\]

for odd `m`, with indices read cyclically.  The adjacent
[spectral-to-gamma result](../odd_cycle_width_one_gamma/) defines the reduced
Ehrhart numerator

\[
R_m(t)=\sum_{j=0}^{(m-1)/2}\gamma_{m,j}
       t^j(1+t)^{m-1-2j}.
\]

This directory proves a fixed-column structural theorem.  Put

\[
A_N=(\mathbf 1_{r+s\le N-1})_{0\le r,s<N},\qquad
\rho_N={1\over2\sin(\pi/(4N+2))}.
\]

For every fixed `j >= 1`, as odd `m` tends to infinity,

\[
\boxed{\gamma_{m,j}
=\rho_{j+1}^{\,m}-(2m-2j+1)\rho_j^{\,m}
+o\!\left(m\rho_j^{\,m}\right).}
\]

In particular,

\[
{\gamma_{m,j}\over\rho_{j+1}^{\,m}}\longrightarrow1,
\qquad
{\rho_{j+1}^{\,m}-\gamma_{m,j}\over m\rho_j^{\,m}}
\longrightarrow2,
\]

and **every fixed gamma column is strictly positive for all sufficiently
large admissible odd cycle lengths**.

There is also an exact algebraic statement.  If
`chi_N(X) = det(X I - A_N)` and the coefficient formula is extended to a
sequence `g_j(m)` for all nonnegative integers `m`, then

\[
\prod_{N=1}^{j+1}\chi_N(E)^{j+2-N}\,g_j=0,
\]

where `E` is the forward shift.  This supplies an explicit constant-
coefficient recurrence of order at most

\[
\sum_{N=1}^{j+1}N(j+2-N)=\binom{j+3}{3}.
\]

Thus the earlier formulas for columns one and two are the first cases of a
uniform C-finite hierarchy, rather than isolated identities.

## What this settles—and what it does not

The result closes the bounded-depth asymptotic question: in any infinite
family of negative interior gamma coefficients whose cycle lengths tend to
infinity, the gamma index must also tend to infinity.  It does **not** give a
uniform threshold in `j`, prove positivity simultaneously in the growing
central range, or prove the observed real-rootedness of the complete gamma
polynomial.

The proof is in [PROOF.md](PROOF.md).  Run the exact checker with

```bash
python3 verify.py
```

The checker uses only Python integer arithmetic.  It independently rebuilds
the transfer determinants, checks the gamma formula against direct numerator
extraction, verifies the annihilating recurrences for columns `1` through `6`,
and audits the first two spectral layers symbolically.
