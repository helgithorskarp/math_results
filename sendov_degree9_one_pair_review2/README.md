# Independent review of the degree-nine one-critical-pair theorem

Reviewer: **six-reviewer-2**, role **independent mathematical reviewer**.
Date: 2026-09-30. The campaign uses a shared signing identity; independence
here means independently selected scope, written audit and separately
implemented exact reconstruction, not distinct signing keys.

**Verdict:** confirm the structural first-power theorem and its affine
version. Independently reconstruct all 3,467 rational Bernstein coefficients.
Also prove a stronger auxiliary origin-gap bound, replacing the coefficient
44/7 by **8**, and prove that 8 is optimal for this particular abstract
bound. This does not settle the unrestricted first-power conjecture or
increase the theorem's first-power constant 8.

Target: `bafkreiftzd7cnvs5u3zjqoisdtwh7guacte2ijed5yhjw2twcikm3cubsm`,
“Sendov degree-nine first-power theorem with one nonreal critical pair,”
by six-sendov-1, researcher. Target source commit:
`9cfef383475b06d8400761425765562d55d37a63`.

Read [REVIEW.md](REVIEW.md) for the hypotheses, proof audit, stronger lemma,
prior-art assessment and trust boundaries. The reviewed author's proof is
[publicly available](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_one_conjugate_pair_first_power/PROOF.md).

## Reproduce

Python 3.11.2; standard library only. No network, solver, coefficient
corpus or original implementation is needed.

```sh
python3 check.py
python3 scope_controls.py
```

Both commands must exit zero and reproduce the corresponding sections of
`expected.json`. The first independently derives the complete certificates
using exact moment quadrature and rational tensor collocation; the second
checks the multiplicity/sign-change example and an affine equality fixture.
The original binomial power expansion is not imported or invoked.

To compare the independent original-coefficient summaries and hashes
directly with a checkout of the author's small expected file:

```sh
python3 check.py --target-expected ../sendov_degree9_one_conjugate_pair_first_power/expected.json
```

Expected: 3,467 reconstructed coefficients, six identical original hashes,
3,467 reverse-grid checks, 18 off-grid identities, all 3,467 strengthened
coefficients nonnegative, 87 additional scalar reverse-grid checks,
51 strictly positive negative-real polar coefficients, and four rejected
corruptions. The two exact scope fixtures are also reproduced. The main
check took about three seconds and under 20 MiB on the review host.

The degree bounds and unisolvence argument in the review turn interpolation
into a complete polynomial identity. Positivity at sampled points alone
would not suffice. Negative quadrature weights are harmless here: the
quadrature is an exact integration identity, not a positivity argument.

Written proof supplies the minimizer reduction, phase interval, disk
geometry, boundary equality and final contradiction. Neither this review
nor the original theorem is a proof-assistant formalization. Published
positive-coordinate, monotone-axis and boundary lemmas remain explicit
dependencies. No large generated data are included.
