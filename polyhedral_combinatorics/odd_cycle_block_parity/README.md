# Odd cyclic block polytopes: exact parity and a gamma obstruction

For an odd cycle of length `m >= 3`, give its blocks positive integer widths
`a_i`. The polytope has nonnegative coordinates in each block and requires
the sum of every two consecutive block totals to be at most one.

Write `d = sum(a_i)`, `b_i = a_i - 1`, `k = d - m`, and fix the rational
Ehrhart numerator normalization

\[
H(t)=(1-t^2)^{d+1}\sum_{n\ge0}|nP\cap\mathbb Z^d|t^n.
\]

[PROOF.md](PROOF.md) proves the following structural statements for all
parameters, using the unique fractional row vertex and its parity-filtered
tangent cone.

* The lattice count is `A(n) + (-1)^n B(n)`, where `B` has exact degree `k`
  and leading coefficient `1 / (2^(d+1) product(b_i!))`. Thus its minimal
  quasiperiod is **exactly two**, including unequal positive widths.
* `H(t) = (1+t)^m R(t)` with `R(-1) = k! / product(b_i!) > 0`.
  The multiplicity of the root at `-1` is exactly the number of blocks.
* When all widths equal `a >= 2`, the last two nonzero coefficients in the
  **ordinary gamma basis** have opposite signs. Hence **every such odd
  cyclic block numerator fails ordinary gamma nonnegativity**.

More explicitly, for equal widths set

\[
b=a-1,\quad D=2a(m-1)+1,\quad J=(D-m)/2,\quad M=(mb)!/(b!)^m.
\]

The numerator is palindromic of degree `D`. In
\(H(t)=\sum_j\gamma_jt^j(1+t)^{D-2j}\), all terms with `j > J` vanish, and

\[
\gamma_J=(-1)^J M,\qquad
\gamma_{J-1}=(-1)^{J-1}M\frac{b(4b+3)(m^2-1)}{24(mb-1)}.
\]

The second formula requires `a >= 2`. For example, `(m,a)=(5,2)` gives
`gamma_5 = -210` and `gamma_6 = 120`.

## Scope and prior work

This addresses the ordinary gamma interpretation of Problem 4 in
[Jiang--Yang--Zhong, arXiv:2607.22008v1](https://arxiv.org/abs/2607.22008).
It does **not** settle unimodality or exclude other gamma-type bases.
At width one, symmetric unimodality and several small numerators are
already in [Hamano--Hibi--Ohsugi, arXiv:1603.09613v2](https://arxiv.org/abs/1603.09613).
In particular, their triangle already exhibits a negative ordinary gamma
coefficient. No novelty is claimed for that example. The contribution here
is the exact general parity mechanism and the formulas excluding the
entire equal-width family `a >= 2`; priority is relative to the sources
searched on 2026-09-20.

The proof imports rational Ehrhart theory, reciprocity, and Brion's
rational vertex-cone identity. It supplies the family-specific geometric,
lattice, differential, and coefficient calculations. It is an
unformalized proof, not an independently reviewed or machine-checked
theorem. Finite computation below corroborates it and does not replace
the universal argument.

## Reproduce

Tested with CPython 3.11.2; Python 3.11+ and its standard library suffice.
No solver, network, external data, randomness, or floating point is used.
From this directory:

```sh
python3 verify.py --check
sha256sum -c SHA256SUMS
```

The deterministic JSON output must match [EXPECTED.json](EXPECTED.json)
and report `status: PASS`. [verify.py](verify.py) checks:

* 24 parameter cases: 16 uniform and eight nonuniform;
* 19 direct full-coordinate counts against the weighted transfer recurrence;
* complete even/odd interpolation, plus 144 extra dilation values;
* nine full alternating polynomials against an independent multivariate
  cone expansion, not just their leading terms;
* exact numerator division, terminal gamma formulas, and 4,914 slack
  integrality/parity comparisons;
* known width-one numerators and four invalid-input rejections.

Every equality uses Python integers or `fractions.Fraction`. Failure raises
an exception and exits nonzero, including when Python optimization is on.
The checker has no certificate files beyond the small expected JSON, and
needs no unpublished artifact. `SHA256SUMS` covers the four other files.
