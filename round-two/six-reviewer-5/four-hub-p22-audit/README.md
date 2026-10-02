# Reproduce the independent four-hub P22 audit

Actual agent six-reviewer-5, independent mathematical reviewer.
Read [REVIEW.md](REVIEW.md) for the conditional theorem, exact imported
premises, independent chronology and strengthening opportunities.

Use Python3.12.14 and the standard library. From this directory run the
following **serially**, with fresh nonexisting work directories:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 reproduce.py --work replay-normal
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O reproduce.py --work replay-optimized
```

The seven stages reconstruct the full broad diagnostic, all actual
four-hub/heavy placements, the pressure-filtered1822 populations, all
98315 unit masks, ordered support and the separate47-vector P20 boundary.
The complete generated records stay in the requested work directory.
The wrapper checks every complete record against its independent first
seal and checks source stability. The broad initial diagnostic drops only
an optional `physically_admissible_types:null` annotation when comparing
with its earlier sealed bytes; no mathematical field is normalized.

RESULT.json must equal [EXPECTED.json](EXPECTED.json), SHA256
`a3cb48186da34817ab4f909d272df91d89b136ee8a14e449f1145c15465f33d9`.
Normal and optimized complete records agree. Final observed costs are
44.910/45.206 seconds and maximum59040KiB child RSS. The fixed guard
limits and the initial incomplete unoptimized-factorization attempt are
reported honestly in REVIEW.md; an incomplete run proves no absence.

The source imports no researcher algorithm. The credited prior9422
pair/mask helper programs and literal Code2 fixture are unchanged.
Generic classification and the three-point carrier are explicit imported
mathematical results. Ordinary bridges remain unformalized.

For the optional late entry comparison, obtain the exact original25-file
source at commit0a4a877986c005c2d30f1949d8eb6c6d09e81d10, directory
`round-two/six-code-3/four_hub_p22_support`, and run its `reproduce.py`
in a fresh original work directory. Then run:

```bash
python3 compare_original.py --original-work ORIGINAL_WORK --own-work replay-normal
```

This reads original JSON only. It compares all426 original raw rows,
all60 color histograms, every218960 membership bit, every1822 vector and
old failure list, all98315 unit decisions and all837 physical signatures,
frequencies and literal witnesses. It does not replace the independent
proof. The stored [LATE-COMPARISON.json](LATE-COMPARISON.json) records the
completed comparison. Original native normal/optimized fourteen-stage
whole records were also byte-equal; those are corroboration only.

All files here are compact source or certificates. No private signing
key, node data, ledger, large enumeration corpus or unrelated artifact is
included. No solver, floating-point computation or purchased resource is
needed. One serial CPU-intensive job and native threads1 suffice.
