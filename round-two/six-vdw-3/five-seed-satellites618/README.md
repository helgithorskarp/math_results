# Five-seed satellite growth for outside-carrier XOR618

Author: **six-vdw-3, researcher**.

The [proof](PROOF.md) shows that a monochromatic field-five seed avoiding
at most three exceptional mod103 columns must have an opposite-color
regular satellite among its specified eight neighboring field points.
An exact local path/triple cover leaves only six exceptional hole sets;
three reflection classes are refuted with strict positive-RUP certificates.
The source also gives all 93 local hole profiles and 49 reflection classes.
This is a necessary restriction, with no 3704-point coloring or new W bound.

The conditional growth proof is self-contained apart from the pinned
strict-checker software. The [earlier seed lemma](../deleted-cycle-ascent618/PROOF.md),
commit 6b8943141b20b4726904e2c027bff62d5870023c and graph 9170,
is an explicit mathematical premise only for seed existence and the
combined interval consequence. Its old mathematical refutations are not
substituted for these three new certificates.

Use Python 3.11.2, a C compiler and the pinned dependencies:

```bash
python3 -m venv /tmp/vdw-five-satellite-env
/tmp/vdw-five-satellite-env/bin/pip install -r round-two/six-vdw-3/five-seed-satellites618/requirements.txt
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  /tmp/vdw-five-satellite-env/bin/python \
  round-two/six-vdw-3/five-seed-satellites618/reproduce.py \
  --work /tmp/vdw-five-satellite-proof
```

Expected final status: `VERIFIED_FIVE_SEED_SATELLITE_GROWTH`, three cases,
137150 checked additions and 4252189 propagation hints per Python mode.
The runner downloads SHA-pinned checker/converter sources, compiles the
untrusted converter, checks complete local coverage and nonvacuous small
controls, regenerates/literal-checks every CNF and strictly replays each
fresh proposed trace normally and under -O. A native UNKNOWN/timeout/SAT
cannot complete this reproduction. No setting silently raises a cap.

[expected.json](expected.json) is a frozen 89898-byte fixture, SHA256
`c6d5c8c9f375de16e7b1470ac2092f32801c49d1cc9c7062561fc95dbbd458a4`.
The runner neither generates nor rewrites that fixture. It is untrusted
expected evidence, compared against separate literal checks and actual
proof replay. [verification.json](verification.json) distinguishes full
source restart from a fresh selected-case smoke check.

`--resume PATH` accepts previously generated `case-N/model.lrat` bytes as
untrusted candidate traces. It still regenerates/audits all models and
checks every hint and empty conclusion. `--only N` checks a selected native
pipeline and explicitly cannot establish the uniform lemma by itself.
`--tools PATH` supplies a scratch directory with the same pinned helper
sources. Proofs/models/binaries are generated in the selected work directory
and are omitted from Git.

[local.py](local.py) proposes the path/triple profile table;
[check_local.py](check_local.py) independently reconstructs every actual
cyclic blocked local word, all 4864 local inputs and 152096 raw hole triples.
[generate.py](generate.py) proposes the three rooted-pair models;
[check.py](check.py) checks the entire literal cyclic/seed CNFs and supports
small positives and partial-witness decoding. Model, coverage and proof
damage guards are part of the public reproduction.

Use a single CPU job with solver/BLAS threads one. Original proposals
used the existing 100000-conflict/35-second native cap; converter 25/30,
replay 50 seconds, and the 1CPU/2GiB scope stayed unchanged. A stronger
no-six harmonic pilot returned UNKNOWN and is absent from the proof.
The next concrete step is to insert these valid thirteen-point mixed
cuts in an outside-carrier search, preserving all orientations and the
same caps. Independent peer review and formalization remain unclaimed.
