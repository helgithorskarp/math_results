# Degree-nine boundary stability for Sendov's problem

Agent: **six-sendov-2**, role: **researcher**, 2026-09-29.

Let a degree-nine complex polynomial have all roots in the closed unit disk
and a boundary root `a`, with `|a|=1`. Define
`delta = (1/8) sum |a-zeta_j|^-2 - 1`, the deficit in the known boundary
quadratic Tang–Zhang inequality. It is nonnegative. If
`0 <= delta <= 2*10^-5`, then

- the eight critical points satisfy `sum |zeta_j|^2 <= 9 delta`;
- the nine roots admit a bijective labeling, with `z_0=a`, such that
  `|z_k - a exp(2 pi i k/9)| <= 500 delta`.

There is also a direct Sendov-distance version. If every critical point is at least
`1-epsilon` from `a`, where `0 <= epsilon <= 10^-5`, then

- the eight critical points, counted with multiplicity, satisfy
  `sum |zeta_j|^2 <= 20 epsilon`;
- after a bijective labeling of the nine roots, with `z_0=a`,
  `|z_k - a exp(2 pi i k/9)| <= 1000 epsilon` for every `k`.

The exponents `1/2` for individual critical-point displacement and `1` for
root displacement are optimal for both versions. An explicit polynomial
family proves this.
The constants above are conservative and are not claimed optimal.

[proof.md](proof.md) contains a complete ordinary mathematical proof, a
general boundary deficit identity, the coefficient argument, and the
sharpness construction. [literature.md](literature.md) records the current
status correction and the limits of the novelty search. This is a
quantitative boundary result, not a new proof of the already resolved
all-degree Sendov or Phelps–Rodriguez assertions.

## Reproduction

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 sendov_degree9_boundary_stability/verify.py
```

Run from the repository root. Python 3.11.2 was used; only the standard
library is required. The program performs exact rational polynomial and
constant checks, exercises a mutation rejection, and prints a compact
certificate followed by a pass count. It performs no floating-point root
search and no enumeration.

Expected final line:

```text
PASS: 46 exact checks; derivative mutation rejected.
```

The code checks arithmetic supporting the written proof. It does not
formalize the Schur transform, Rouché's theorem, the implicit-function
argument, or the surrounding quantified theorem. No solver, generated
dataset, external certificate, or large artifact is required. The external
Lean proof mentioned in the literature note was inspected at the theorem
statement level, not rebuilt in this workspace.

Claim status: proved quantitative lemma with exact arithmetic checks;
no independent reviewer verdict or proof-assistant certification is claimed.
The estimate and sharpness construction were not found in the bounded
searched sources; this is not a priority claim.
