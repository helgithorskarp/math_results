# Odd-cycle graph polytopes: a spectral-to-gamma bridge

Let \(m=2q+1\ge 3\), and let

\[
Q_m=\{x\in\mathbb R_{\ge0}^m:x_i+x_{i+1}\le1\ (i\bmod m)\}.
\]

Write

\[
F_m(t)=\sum_{n\ge0}|nQ_m\cap\mathbb Z^m|t^n,
\qquad
H_m(t)=(1-t^2)^{m+1}F_m(t).
\]

The earlier [odd-cycle parity theorem](../odd_cycle_block_parity/) gives
\(H_m(t)=(1+t)^mR_m(t)\), where \(R_m\) is palindromic of degree
\(m-1\). Define its ordinary gamma polynomial by

\[
R_m(t)=(1+t)^{m-1}\Gamma_m\!\left(\frac{t}{(1+t)^2}\right),
\qquad
\Gamma_m(x)=\sum_{j=0}^{q}\gamma_{m,j}x^j.
\]

These are also the ordinary gamma coefficients of \(H_m\), because the
extra factor \((1+t)^m\) raises the palindromic degree by \(m\) without
changing the gamma vector.

[PROOF.md](PROOF.md) proves an exact bridge from the spectral transfer
matrix to every coefficient of \(\Gamma_m\). Let \(A_N\) be the
\(N\times N\) matrix

\[
(A_N)_{rs}=\mathbf 1_{r+s\le N-1}\qquad(0\le r,s<N),
\]

and put \(p_m(N)=\operatorname{tr}(A_N^m)\). Then

\[
\boxed{\quad
\gamma_{m,j}=[t^j](1-t)^{m+2}(1+t)^{\,2j+1-m}
              \sum_{n=0}^{j}p_m(n+1)t^n .\quad}          \tag{1}
\]

The traces in (1) require no matrix powering. If
\(D_N(z)=\det(I-zA_N)=\sum_k d_{N,k}z^k\), then

\[
D_{N+2}=(2-z^2)D_N-D_{N-2},                              \tag{2}
\]

with

\[
D_0=1,\quad D_1=1-z,\quad D_2=1-z-z^2,\quad
D_3=1-2z-z^2+z^3,
\]

and Newton's recurrence is

\[
p_r(N)=-r d_{N,r}-\sum_{k=1}^{r-1}d_{N,k}p_{r-k}(N).     \tag{3}
\]

Thus (1)--(3) are a finite exact recurrence for the complete gamma vector,
not interpolation from an Ehrhart table.

The bridge gives the first uniform positive prefix:

\[
\gamma_{m,0}=1,
\qquad
\gamma_{m,1}=L_m-2m+1>0,
\]

and, for every odd \(m\ge5\),

\[
\gamma_{m,2}=T_m+(3-2m)L_m+2m^2-6m+1>0.                 \tag{4}
\]

Here \(L_m\) is the \(m\)-th Lucas number and

\[
T_0=3,\quad T_1=2,\quad T_2=6,\qquad
T_r=2T_{r-1}+T_{r-2}-T_{r-3}.
\]

Together with the prior terminal formula
\(\gamma_{m,q}=(-1)^q\), this proves that all currently possible negativity
is confined to the unresolved interior indices \(3\le j<q\). In
particular, for the open class \(m\equiv1\pmod4\), both ends and the first
three entries are positive.

## Conjectural sharpening and exact evidence

The recurrence exposes a stronger, deliberately **unproved** statement:

> **Conjecture.** \(\Gamma_{2q+1}\) is real-rooted. If \(q\) is even, all
> roots are negative; if \(q\) is odd, exactly one root is positive and the
> others are negative.

This would classify ordinary gamma positivity exactly: it would hold
precisely for \(m\equiv1\pmod4\). The checker establishes, using exact
integer/rational arithmetic:

* the predicted coefficient signs through every odd \(m\le201\);
* the predicted root locations through every odd \(m\le41\), by Sturm
  sequences (multiplicities allowed; \(\Gamma_5=(1+x)^2\));
* the determinant, Newton, Lagrange-coefficient, and direct-count identities
  on independent small controls.

These finite checks support the conjecture and are not presented as its
proof.

## Reproduce

Tested with CPython 3.11.2; Python 3.11+ and the standard library suffice.
From this directory run

    python3 verify.py
    sha256sum -c SHA256SUMS

The first command must print a JSON object with status PASS. There is no
floating point, randomness, solver, network access, or unpublished
certificate.

## Prior work and scope

Ehrenborg's spectral treatment of the same cycle graph polytope supplies a
determinant for its Ehrhart quasipolynomial:
[European Journal of Combinatorics 118 (2024), 103906](https://doi.org/10.1016/j.ejc.2023.103906).
Equations (2)--(3) are recorded as the exact computational normalization of
that spectral input; no novelty is claimed for the transfer-matrix idea.

Hamano--Hibi--Ohsugi prove palindromicity and unimodality of the rational
Ehrhart numerator and list the cases \(m=3,5,7,9\):
[arXiv:1603.09613v2](https://arxiv.org/abs/1603.09613).
Liu later proves numerator palindromicity for all connected graph polytopes:
[arXiv:2409.11970](https://arxiv.org/abs/2409.11970).
Jiang--Yang--Zhong ask for a gamma-type understanding of odd cyclic
numerators in Problem 4:
[arXiv:2607.22008v1](https://arxiv.org/abs/2607.22008).

The contribution here is the Lagrange coefficient identity (1), its
Chebyshev--Newton realization, and the uniform positive-prefix theorem (4).
Priority is relative to the sources searched on 2026-09-20. The proof is
unformalized and awaits independent review. It does not prove the displayed
real-rootedness conjecture or the full \(m\equiv1\pmod4\) classification.

