# Exact integer cutoffs for the labelled deletion ansatz

Actual author **six-downset-3**, role **researcher**. For every integer
k>=5,q>=max(4,k), the specified capped affine-table/four-repair-edge ansatz
is feasible exactly when (2q-6k+25)^2-28k^2-36k>=81, except(k,q)=(5,18).
For k>=6 the cutoff is ceil((6k-25+sqrt(28k²+36k+81))/2); for k5 it is19.
[PROOF.md](PROOF.md) gives the ordinary unbounded proof and exact scope.
Finite k5..24 is credited9582. The new increment is the complete k>=25
classification. Negative cases exclude this capped ansatz. General H/I,
and arbitrary matrices on these downsets, are not resolved here.

From the repository root, run (CPython3.12.14 tested):

```bash
cd round-two/six-downset-3/integer-deletion-cutoff
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
PYTHONDONTWRITEBYTECODE=1 python3 -O verify.py
sha256sum -c SHA256SUMS
```

The verifier uses the standard library only. Keep the credited sibling
source directories from the repository; [INPUTS.json](INPUTS.json) pins
all13 mandatory imported executables and both whole mathematical JSONs,
plus two additional optional CAS executables. Each check explicitly raises
on failure under normal and optimized Python. [EXPECTED.json](EXPECTED.json)
freezes the **entire** new coefficient record and replayed check;
[RESULTS.json](RESULTS.json) records its expected successful digest.
Do not substitute a hash match for the independently reconstructed identities.

Optional exact characteristic-zero generation requires SymPy1.14.0:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 derive_integer_gap.py
python3 verify.py
```

The generator reproduces [INTEGER-GAP.json](INTEGER-GAP.json), including
all210 derivative coefficients, the entire norm57 quotient/remainder/shift
and10 sandwich coefficients, plus exhaustive residues modulo121 and25.
[check_integer_gap.py](check_integer_gap.py) rebuilds these using a different
standard-library algorithm, verifies all20 credited finite joins, and rejects
six semantic damages without using hash-only failure. [cutoffs.py](cutoffs.py)
implements the proved cutoff with integer square roots. It returns a decision
for this ansatz; the credited positive parent gives the rational matrix parameters.

The whole-space/counting/Schur/rank/actual-empty-lift bridges are ordinary
proofs, not proof-assistant formalized. All new work remains independently
unreviewed. Same-author algorithm independence does not imply peer review.
[VALIDATION.json](VALIDATION.json) records full normal/optimized agreement,
complete private/public mathematical equality and measured bounds. Compact
source only is included; the diagnostic4976-row scan is unnecessary for this
unbounded proof and is not part of this packet.
