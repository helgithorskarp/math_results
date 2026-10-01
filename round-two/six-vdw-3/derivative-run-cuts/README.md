# Stronger derivative restrictions for the separable period618 family

Every valid coloring `c(t)=u(t mod103) XOR 000111(t mod6)` has even
shift distances **32..72** and orientation weight **20..83**. This
sharpens the earlier necessary ranges28..76 and17..86. A general
combinatorial run-packing lemma also gives derivative minority density
at least **5/19**, for unit shifts at every q>=23 coprime to6.

The finite strengthening excludes exactly three distance classes28,30,74
with complete models and exact proof replay. At weight20 it additionally
requires difference multiplicity at most4, at least74 distance32 shifts,
and at least155 specified extended ordered pairs. The entire family
and the length3704 witness remain open; **no W(2,7) bound improves**.

Author: **six-vdw-3, researcher**. The proofs and implementations are
author checked; no independent peer verdict or formalization is claimed.
See [PROOF.md](PROOF.md) for quantified coverage and [VALIDATION.md](VALIDATION.md)
for the audit record.

## Reproduce

From the repository root, with Python3.11 and GCC:

```sh
python3 -m venv scratch/derivative-cut-env
scratch/derivative-cut-env/bin/pip install -r round-two/six-vdw-3/derivative-run-cuts/requirements.txt
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  scratch/derivative-cut-env/bin/python round-two/six-vdw-3/derivative-run-cuts/reproduce.py \
  --workdir scratch/derivative-cut-check
```

Expected final status: `VERIFIED_DERIVATIVE_RANGE_32_72_AND_WEIGHT_20_83`.
The driver fetches three checksum-pinned public source files, builds the
untrusted converter, regenerates each model, audits its entire clauses
separately, proposes three bounded proofs and checks every RUP addition
in normal and optimized Python. It runs complete small-family positive
and coverage controls, exact-cardinality truth tables, symbolic/run
boundary checks, malformed-model/proof controls and one-conflict UNKNOWN
controls. Jobs are serial, with native threads1. Each proof proposal
has a100000-conflict cap and external35-second timeout; conversions
have an internal25-second and external30-second timeout.

No SAT/UNKNOWN/timeout result, missing model audit, malformed trace or
unverified empty clause supports an exclusion. New proof bytes must
verify against the exact audited models. Reference proof hashes and
counts in [expected.json](expected.json) are reproducibility diagnostics;
the driver records an independently valid differing trace rather than
use a hash match as a proof. Generated CNFs, proofs, sources, binaries
and logs remain in the work directory and are omitted from Git.

Files: [encoder](generate.py), [independent definition audit](check.py),
[combinatorial boundary checks](elementary.py), [driver](reproduce.py),
[pinned requirements](requirements.txt), [compact references](expected.json).
The actual mathematical boundaries, hypotheses and normalization are
proved in the unformalized written argument, rather than inferred from
small checks.

The full-family SAT probe previously returned UNKNOWN; it is not a
premise. A fifteen-period derivative relaxation passes telescoped
steps1..5 while having minority density4/15, so that relaxation cannot
alone prove density3/11. This is a useful method limit, independently
checked in elementary.py. It is not a coloring witness. Larger automaton
exploration was stopped at preset operational caps without an exclusion.

This extends [our published pair-parity ladders](../parity-ladders/README.md).
The full proof gives credit and direct links for the normal form and
reused strict RUP checker. Sparse phase exclusions remain the separate
[signed-defect contribution](../signed-phase-defects/README.md).
