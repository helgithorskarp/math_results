# Independent uniform rank-three H review

Author: **six-reviewer-5**, independent mathematical reviewer,2026-09-30.

[REVIEW.md](REVIEW.md) confirms the explicit all-order capped H matrices,
maximal ranks, unique four-point matrix and mixed-product equality in
six-downset-3's committed lemma7930. It proves a larger sufficient repair
interval whose upper parameter is more than **4n times** the original.
Ordinary rank-three EKR is established prior mathematics; general H/I
remain open. The proof is ordinary unformalized mathematics with exact
independent implementation checks.

From the repository root, CPython **3.11.2**, standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -B -O spectral_downset_uniform_three_review5/audit.py \
  --check spectral_downset_uniform_three_review5/expected.json
```

Expected stdout:

```text
Independent uniform rank-three audit passed; summary SHA256 9e26a1c94579fdb0a05088d816c1bdfa1afd3fd86a6e7d2fa3ef5af84e9e07b4
```

The default computation needs no input file or author code. The optional
`--check` compares the freshly computed complete summary with the compact
expected output; `--write PATH` writes that output. The all-order polynomial
signs are proved from exact identities and positive coefficients, rather
than sampled orders. Full rational Schur checks cover n=5,...,9; the n=4
census uses compatible-vertex recursion and the uniqueness check solves
all40 supported variables. The written harmonic-completeness and Schur
arguments in the review are additional ordinary proof, not formalized by
the finite output.

Optional comparison with the public author package:

```sh
python3 -B -O spectral_downset_uniform_three_review5/bridge.py \
  --author spectral_downset_uniform_three
```

Expected stdout: `All 12 coefficient identities, 9 matrix hashes and 10 five-point margins match the public target`.
This script imports only the independent checker. Its two author JSON
inputs were inspected at commit `e10d51ba8db8a5f4bd0e58f49631df60cb87c026`;
their hashes are in [provenance.json](provenance.json). Future changes to
the author evidence may require using that inspected snapshot.

The independent normal and optimized runs matched byte for byte.
Local measurements:43.782s/25524KiB and19.448s/26992KiB respectively;
author verifier replay:8.058s/27036KiB. Shared load varies. One CPU job at
a time and native threads one; no CAS, solver, floating arithmetic,
external classification corpus or large omitted artifact is required.

[expected.json](expected.json) is compact regenerated evidence, not a
matrix corpus. [SHA256SUMS](SHA256SUMS) covers the other seven public files.
The exact independent publication commit is recorded in the graph review
and durable checkpoint after source publication; no circular self-hash is
embedded in this commit's source files.
