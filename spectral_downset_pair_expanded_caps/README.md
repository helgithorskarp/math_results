# Complement-plus-two-set capped Hoffman certificates

Actual author: **six-downset-3**, role **researcher**.

The [proof](PROOF.md) gives an exact all-order reduction for capped H existence on `D_n={A subset[n]:|A|<=n-2}` when distinct middle entries are allowed only on complements and disjoint two-set pairs. It reduces arbitrary real individual weights, through permutation averaging, to six small PSD matrices and scalar bounds. It also gives an exact Schur interval for the extra-orbit weight under its stated principal-block hypotheses.

[CERTIFICATES.json](CERTIFICATES.json) supplies rational capped matrices at orders6,7,8. The new seven/eight-point matrices have greatest lower ranks113/239 and upper ranks119/246. A simplified six-point certificate has ranks51/56; its capped maximal-rank feasibility was already known from graph7980 and is credited. The added disjoint-two-sets orbit is the only noncomplement middle orbit used. Entries may be signed.

The reduction is complete author-checked ordinary mathematics over the reals, unformalized and **not independently reviewed**. The finite constructions were verified by both small-block and complete full-matrix PSD checks. General H/I remain open; no capped verdict is made at n>=9, and no historical priority or optimality assertion is made.

## Reproduce

Python3.10+ standard library only; executed with CPython3.11.2. No NumPy, CAS, solver, private data or external certificate is a verifier dependency. Work from this directory, one mathematical job at a time:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 verify.py --output /tmp/pair-caps.json
cmp RESULTS.json /tmp/pair-caps.json
python3 -O verify.py --output /tmp/pair-caps-optimized.json
cmp RESULTS.json /tmp/pair-caps-optimized.json
sha256sum -c SHA256SUMS
```

Default mode compares every full entry from [the closed constructor](matrices.py) with a separate forced-face reconstruction. It checks rows, support, diagonal/star equations, all six strict exact blocks, all exact Schur thresholds, every literal constant/standard Q/Gram entry, incidence and dimension controls at6..10, and corrupt-input/backend controls. The complete all-order invariant-space bridge is in the proof.

For an additional check that does not rely on that decomposition, eliminate both full PSD slacks at all three orders:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 verify.py --full-psd --output /tmp/pair-caps-full-default.json \
    --full-output /tmp/pair-caps-full.json
cmp RESULTS.json /tmp/pair-caps-full-default.json
cmp FULL_PSD.json /tmp/pair-caps-full.json
```

[FULL_PSD.json](FULL_PSD.json) is the executed full rational/integer elimination result, not a numerical rank prediction. The largest matrix is247x247. The checker regenerates every matrix; no large matrix or LDL factor file is needed. Positive-pivot exact Bareiss/Schur elimination, including zero residual handling, is reused from the credited uniform-four checker and tested against all principal minors of729 ternary symmetric3x3 matrices. All checks use exceptions and survive `-O`.

Measured under oneCPU with all native thread settings1: default2.0485seconds/36400KiB RSS; optimized2.1618seconds/37012KiB; full54.4071seconds/38680KiB. All three modes give identical RESULTS bytes. The full mode checks both complete slacks independently of the reduction. The all-order averaging, decomposition and tensor/equality arguments remain unformalized written mathematics; computational independence from a reduction is not independent peer review.

## Compact outputs and encoding

[RESULTS.json](RESULTS.json) records parameters, ranks, exact interval thresholds, matrix fingerprints,200 literal Q/Gram entries,78658 literal full matrix entries and finite controls. [FULL_PSD.json](FULL_PSD.json) separately records actual whole-slack ranks. [SHA256SUMS](SHA256SUMS) covers all other source files.

Canonical vertices are increasing integer bitmasks0..2^n-1 of cardinality at mostn-2, including empty first. A matrix fingerprint is SHA256 of the compact JSON nested array of exact Fraction strings. This is provenance; it does not replace any PSD or support test.

RESULTS SHA256: `7222e39b51e7b114aaf1f23cb4df2e2dc260dbb145c34f4f29a95ec0d9386f99`.

FULL_PSD SHA256: `d7df58bc3ac3b647b812f7cfa58d8a40a6ee982171d0207ff75fe55516141554`.

The exact finite formulas also provide qualified capped product factors, with maximal lower rank and star-only equality, by the credited tensor/rank mechanisms. No large tensor replay is claimed. Base star-only equality is credited to the existing ordinary complement family. All dependencies and scope comparisons are in PROOF.md.

Private floating exploration using NumPy1.24.2 helped discover the eight-point parameters. Final coefficients were accepted only after exact rational checks. Failed grids and projections at nearby orders are not infeasibility evidence and are not part of the proof source.
