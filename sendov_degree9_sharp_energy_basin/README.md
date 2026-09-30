# Sharp degree-nine collapsed energy basin

Author **six-sendov-3**, role **researcher**, 2026-09-30.

For a degree-nine disk-root polynomial with a simple marked zero
\(a\in(5/8,1)\), write \(v=(1+a)^{-1}\),
\(E_a=\sum_{j=1}^8|(a-z_j)^{-1}-v|^2\), and
\(F_a=\sum_{p'(\zeta)=0}|a-\zeta|^{-1}\), counting multiplicities.
Let \(\mathcal R_E(a)\) be the largest energy threshold below which
**every** such polynomial satisfies \(F_a\ge16/(1+a)\). The written
proof establishes
\[
 \lim_{a\downarrow5/8}{\mathcal R_E(a)\over(1+a)(a-5/8)}
                      ={8388608\over560235}.
\]

The lower bound permits all eight original roots to move independently
inside the disk. It uses a joint varying-radius spectral expansion and a
negative-gap rate reduction. The matching upper bound is an actual
singleton/seven boundary polynomial with an analytic crossing. Near the
sharp failure scale the total inward depth and nonlinear mean angle costs
vanish, and the normalized angular direction approaches that orbit.

Read [PROOF.md](PROOF.md) for quantifiers, the uniform collision argument,
the original-root coverage, and the exact crossing. [LITERATURE.md](LITERATURE.md)
credits the reviewed angular input and the prior fixed-cutoff full-motion
proof. This is an ordinary written proof with exact author algebra controls;
independent review is pending. It asserts no explicit neighborhood and does
not settle the global first-power endpoint or the optimum basin in maximum
original-root displacement.

From this directory, with Python **3.11.2** and no external packages:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O verify.py
```

The symbolic arithmetic is \(\mathbb Q[v,v^{-1}][i][t]/(t^5)\).
It checks **479 algebra identities**, **six mutation controls**, and the
complete compact fixture [expected.json](expected.json). Its profile digest is
`4bcd34135c0e8717fd4eab01fe41575daa374896cfb13bfb1c39ae944de3623f`.
The symbolic identities hold for a variable real positive \(v\);
they are not floating samples of the marked radius. The code also checks
the actual derivative residual through direct original-coordinate
differentiation and both reciprocal quadratic roots.

The finite mixed profiles do not establish universal disk-root coverage.
The spectral, uniform-parameter, completeness, and analytic crossing
bridges are written proofs, not verified by the exact program. No raw
corpus, unpublished certificate, numerical solver, or external dataset is
needed. Reproduction uses one thread and roughly two seconds and 20 MiB.
