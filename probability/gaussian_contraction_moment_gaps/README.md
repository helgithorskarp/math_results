# Sharp Gaussian moment-gap comparisons

For a bounded probability law in `R^n` and an arbitrary 1-Lipschitz image,
let `d_m` be the difference of their Gaussian-smoothed `m`-th moments,
normalized by the Gaussian peak to power `m-1`. We prove

```text
0 <= d_q <= ((q-1)/(p-1)) * (p/q)^(n/2) * d_p,   2 <= p < q integers.
```

The constant is optimal. This completely classifies comparisons for linear
combinations of two integer powers. Consequences include every convex cubic
in every dimension and the convex exponential energy

```text
U(rho) = C * (exp(-a*rho/C) - 1 + a*rho/C),
0 <= a <= sqrt(243/32),   n=3,   C=(2*pi*s)^(-3/2).
```

The range `2<a<=sqrt(243/32)` lies outside the `PC_2` condition of
[Aishwarya--Li](https://arxiv.org/html/2609.07041v2). The full
dimension-three majorisation conjecture remains open in this work.
The proof is in [PROOF.md](PROOF.md).

Reproduce the compact validation with CPython 3.11+ and `python-flint==0.9.0`:

```bash
python -m pip install -r requirements.txt
python -B verify.py --check
python -B -O verify.py --check
sha256sum -c SHA256SUMS
```

The verifier uses exact fractions and 256-bit Arb enclosures. It consumes
no generated data. `EXPECTED.json` contains the compact deterministic audit.
Finite checks validate formulas and sharpness examples; the written proof
establishes the universal statements. Independent review is pending.
