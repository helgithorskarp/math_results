# Gaussian set transfer and measure localization

This packet proves an exact measure-side reduction of the dimension-three
Gaussian-majorisation question and identifies a limit on atomic localization.
It does **not** settle the open conjecture or add a Kneser--Poulsen class.
Complete author proof; independent review pending.

For a compact support K, continuous map T, Gaussian variance s, and a set A
of finite positive volume v, define

    m(A) = min_mu [ sup_{|B|=v} integral_B (T#mu)*gamma_s
                                      - integral_A mu*gamma_s ].

The [proof](PROOF.md) establishes:

- An ordinary set B of volume v attains the equivalent max-min problem
  simultaneously over every centre in K. It is a superlevel set of a
  minimizing target Gaussian mixture. The minimizing measure is supported
  on the contact set of the resulting Gaussian mass potential.
- All-law Gaussian majorisation is exactly m(A)>=0 for every A. The
  [dominant fixed-atom reduction](../gaussian_majorisation_global_criterion/ANCHOR_REDUCTION.md)
  has an explicit version retaining compensation by the fixed atom.
- On a sphere under x -> cx, 0<c<=1, the corresponding minimizer for a
  centred-ball test is uniquely uniform surface measure, provided
  (cR)^2<=3s. This remains true with any fixed positive rare mass beside a
  dominant atom at zero. No finite prior attains the optimum; every fixed
  atom bound has a strictly positive optimization error.
- A delta-net still approximates the value within
  (1+Lip(T))delta/sqrt(2 pi s), multiplied by the rare mass in the anchored
  version. Strict negative witnesses remain finitely approximable.

The obstruction is to **exact optimizer localization**. It neither refutes
finite counterexample witnesses nor provides a counterexample to Gaussian
majorisation. The common-set inequality remains unproved for arbitrary
contractions. The sphere example already has a classical contracting motion.

Reproduce the compact algebra controls with standard-library Python 3.11+:

```sh
python3 verify.py --check
python3 -O verify.py --check
sha256sum -c SHA256SUMS
```

[EXPECTED.json](EXPECTED.json) contains exact rational checks of the
hyperbolic-series identity, the positive exponential-kernel tensor identity,
and finite-cell saddle controls. Finite-cell data are explicitly not Gaussian
contraction examples; their ties explain why the analytic no-plateau step
in the proof is needed. The universal result relies on the written proof,
standard minimax and analytic facts, not numerical integration or a solver.

See [SOURCES.md](SOURCES.md) for mathematical attribution, team dependencies,
the literature boundary, and the distinction from existing per-law endpoint
couplings and finite strict rational-witness reductions.
