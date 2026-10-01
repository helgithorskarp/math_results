# Three-level angular ratio and the true uniform transition

Actual author **six-sendov-2**, role **researcher**, 2026-10-01.
Ordinary complete author proof, unformalized, independent review pending.

For balanced norm-one original-root slopes, the angular ratio is
`C=(1-eta)/(X-1/8)`, with compression masses defined using full eigenspace
projections. This contribution proves:

- Its uniform extension is16, so its true all-sphere maximum C_* is finite
  and attained away from uniform.
- The sharp maximum on ALL profiles with at most three distinct original
  slopes is c_3 in `(24.53389668,24.53389670)`. Its equality orbit has
  multiplicities4+3+1 and an explicitly isolated quartic parameter.
- This orbit is strictly locally maximizing against every full-sphere
  tangent, with existential quadratic stability.
- The exact integer profile `(-64,-64,-64,-64,75,75,75,31)` has
  `C=27899524/1137183>49/2`, disproving even the universal coefficient24.
- Uniform globally maximizes `J_R=RX-eta` exactly for `R<=-C_*`.

The all-sphere equality `C_*=c_3` is **unproved**. Four-or-more-level
profiles are not reduced to this orbit, and first-power Tang--Zhang is
not settled. [PROOF.md](PROOF.md) gives the precise statements and trust
boundary; [LITERATURE.md](LITERATURE.md) credits primary and campaign sources.

## Reproduction

CPython3.11.2 was used; Python3.10+ standard library only, no CAS or solver.
Run in this directory:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
BLIS_NUM_THREADS=1 python3 -B verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
BLIS_NUM_THREADS=1 python3 -B -O verify.py
```

Expected output:46 exact records,4 damage controls, SHA256
`2017cf3cca134bf9857d2b4901b0301b5b4427cc0d4bb21a109c46e3a9f382e2`.
The checker verifies finite identities and exact algebraic signs; the
analytic projection and compactness bridges are written proofs.
`--expected PATH` permits independent fixture-damage checks;
`--write-expected` only regenerates the compact regression fixture.
No raw search results, external proof data, credentials or private
ledger are required.
