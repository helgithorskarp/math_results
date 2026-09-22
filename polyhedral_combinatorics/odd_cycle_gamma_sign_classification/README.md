# Odd cycles: complete ordinary gamma-sign classification

For the fractional stable-set polytope of the odd cycle `C_(2q+1)`,
**every nonterminal reduced gamma coefficient is positive, and the
terminal coefficient is `(-1)^q`**. Consequently its fixed rational
Ehrhart numerator is ordinary gamma-nonnegative exactly for cycle
lengths congruent to one modulo four.

More precisely, for

\[
 Q_m=\{x\ge0:x_i+x_{i+1}\le1\ (i\bmod m)\},\quad
 H_m(t)=(1-t^2)^{m+1}\sum_{n\ge0}|nQ_m\cap\mathbb Z^m|t^n,
\]

write, with `m=2q+1`,

\[
 H_m(t)=(1+t)^{2m-1}G_q\!\left(\frac{t}{(1+t)^2}\right),\qquad
 G_q(x)=\sum_{j=0}^q g_{q,j}x^j.
\]

The theorem is `g_(q,j)>0` for `0<=j<q`, and `g_(q,q)=(-1)^q`.
In the full ordinary gamma vector of `H_m`, all indices above `q`
vanish. For example,

| Cycle length | Reduced gamma polynomial |
|---|---|
| 3 | `1-x` |
| 5 | `1+2x+x^2` |
| 7 | `1+16x+27x^2-x^3` |

Combining the theorem with the earlier [uniform-width obstruction](../odd_cycle_block_parity/README.md)
closes the equal-width ordinary-gamma classification: **for odd cycle
length `m>=3` and equal positive integer block width `a`, nonnegativity
holds exactly when `a=1` and `m=1 (mod 4)`**, using palindromic degree
`2a(m-1)+1`. The width-`a>=2` exclusion is an imported prior result.

## Proof mechanism

[PROOF.md](PROOF.md) supplies an all-length proof. It combines:

1. An exact cycle--path identity from normalized transfer eigenvectors,
   `4 L_(C_m)(n)=(2n+3)L_(P_(m-1))(n)+L_(C_(m-2))(n)`.
2. An injection on canonical linear extensions of even fences. If
   `a_(q,j)` is the gamma vector of the path on `2q` vertices, then
   `a_(q+1,j)>=(j+1)a_(q,j)+(2q-2j+1)a_(q,j-1)`.
3. A simultaneous induction proving the desired signs and the auxiliary
   coefficientwise bound `g_(q,j)<=a_(q+1,j)`.

The canonical-representative interpretation is Brändén's prior orbit
theorem. The injection prepends a new smallest negative label and inserts
a new largest positive label in explicitly counted positions. Its use
with the cycle--path identity supplies the missing uniform comparison;
fixed-column asymptotics alone do not provide it.

## Prior work and limits

The [earlier cycle package](../odd_cycle_width_one_gamma/README.md)
gave an exact evaluator, the first two positive columns, the terminal
sign, and finite evidence. The [fixed-column package](../odd_cycle_gamma_fixed_columns/README.md)
proved eventual positivity for each fixed index. The new conclusion
covers **every interior index at every odd length**.

The proof credits [Brändén, Theorem 6.3](https://arxiv.org/pdf/math/0610185)
and [Petersen--Zhuang, Theorem 2.5](https://arxiv.org/html/2403.07181v4)
for fence gamma theory, and [Hamano--Hibi--Ohsugi](https://arxiv.org/abs/1603.09613)
and [Ehrenborg](https://doi.org/10.1016/j.ejc.2023.103906) for prior
fractional-polytope and spectral machinery. Full references and
normalization alignment are in the proof.

This settles the specific ordinary-basis frontier arising from
[Jiang--Yang--Zhong, Problem 4](https://arxiv.org/html/2607.22008).
That paper asks a broader gamma-type question. Real-rootedness, unequal
widths, and alternative bases are not settled here. Width-one
unimodality was already known. Novelty is relative to the graph and
primary sources checked on 2026-09-22, not a certified historical
priority claim.

This is a conventional unformalized proof with an explicitly cited
external theorem. It has not yet received independent peer review.
Finite computations below check its components and normalizations;
the universal theorem follows from the proof, not extrapolation.

## Reproduce the exact checks

Python 3.11+ and its standard library suffice; tested with CPython 3.11.2.
From this directory:

```sh
python3 verify.py --check
sha256sum -c SHA256SUMS
```

[verify.py](verify.py) must reproduce [EXPECTED.json](EXPECTED.json)
and exit successfully. The principal checks are:

* Definition-level tuple enumeration against the path and cycle DPs.
* 165 cycle--path identities and 152 gamma recurrence coefficients.
* 51,973 linear extensions, including 6,364 canonical representatives,
  and all 45,537 distinct images of the proposed insertion on these
  representatives. Order validity, boundary double descents, inverse
  deletion, multiplicities, and injectivity are checked separately.
* Ehrhart numerators computed independently from lattice counts against
  the canonical-representative gamma counts, and the full numerator's
  higher zero gamma coefficients.

Runtime is about one second and peak memory about 24 MiB in the recorded
environment. All mathematical comparisons use exact integers. No
solver, floating point, external data, randomness, or network is needed.
The package is self-contained for the width-one theorem's computation;
the imported larger-width corollary points to its separately published
proof and evidence.
