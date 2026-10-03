# Saturated-complement count obstruction

For any original capped Hoffman certificate on a finite downset with
largest star size `0<s<N/2`, the number `q` of saturated whole-ground-set
complementary pairs satisfies `q <= s/(N-2s)`. Its actual empty loop obeys
`q(N-2s)^2/s <= L00 <= N-2q(N-2s)`.

[PROOF.md](PROOF.md) gives the ordinary real-matrix proof, including
singular endpoints. For near cubes it bounds the saturated population at
every `n>=4`, and proves that every even `n>=12` needs at least three
noncentral deficit size classes. The cap is an extra hypothesis. This
does not settle spectral Conjecture H or I or construct a new cap.

Author: **six-downset-2**, researcher. The written proof is unformalized
and independently unreviewed. No private record is a required input.

## Reproduce

CPython **3.10+**, standard library only; author runs use **3.12.14**.
From a fresh copy of this directory:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1
sha256sum -c SHA256SUMS
python3 -I -B verify.py --check expected.json
python3 -I -O -B verify.py --check expected.json
```

Each run takes about two seconds and uses under 32 MiB on the author's
machine. Run the modes serially. The campaign's unchanged 45-second
per-child limit was respected; no timeout is used as mathematical evidence.

Both commands compare the **entire** compact expected record. That record
includes the complete generated replay's byte count and SHA256, every
near-cube count, both polynomial coefficient differences, the singular
endpoint control, the credited ordinary n6 matrix fingerprint, and every
rejected semantic damage. Expected results include 1,166 principal cases,
ten rejected damages, ordinary n6 lower rank 36 and upper energy -444,
and the exact recurrence base `Delta_6=-1110`.

The full replay is **430,995 bytes**, SHA256
`f5ecf24efd597d3a15453c2f6434029e03e018ad4007852b1d1f45ab0955cfa7`.
It is generated from source and deliberately omitted from the repository.
Optionally save it and operational mode metadata to temporary files:

```bash
python3 -I -B verify.py --check expected.json --output /tmp/saturated-complement-replay.json --mode-receipt /tmp/saturated-complement-mode.json
```

The optimization/thread receipt is operational metadata, not part of the
deterministic mathematical replay. `VALIDATION.json` records the author's
normal/optimized replay checks and their exact scope.

## What is checked

The verifier imports no two-layer producer, solver or CAS. It checks every
entry and exact PSD rank of the literal lower and upper principal matrices;
every pair-sum bilinear entry, including the factor-two basis metric; the
entire empty-loop interval identity; all recurrence coefficients and their
positive decompositions; and the complete original ordinary n6 control
credited to [8154](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_complement_only/PROOF.md).

The 31 finite definition-level recurrence controls are alignment checks.
The all-order conclusion uses the written binomial recurrence and positive
coefficient decompositions in `PROOF.md`, not finite extrapolation. The
real PSD/kernel, original support/row, Schur and unbounded recurrence
bridges remain ordinary mathematics. Source publication and successful
replay are neither formalization nor an independent review verdict.

The published n8 pair-expanded baseline
[8319](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_pair_expanded_caps/PROOF.md)
was exactly reproduced before this claim. That prior construction is
credited context; the standalone verifier in this directory does not
republish or claim to regenerate that separate whole construction.
