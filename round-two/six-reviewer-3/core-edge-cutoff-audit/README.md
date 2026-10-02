# Independent core-edge cutoff audit

Actual agent **six-reviewer-3**, independent mathematical reviewer. Confirm
LEMMA9766 in its complete specified core-face scope, with explicitly imported
prior spectral and positive-tail premises. New proof: all four parameters
may vary in conservative explicit boxes around the q16/q17 certificates.
[REVIEW.md](REVIEW.md) states the verdict and trust boundary;
[PROOF.md](PROOF.md) contains the independent ordinary argument.

With CPython3.12 (measured3.12.14), standard library only, from this directory:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 -I -B audit.py
python3 -I -B -O audit.py
python3 validate.py
python3 -I -B structural.py
python3 -I -B compression.py
sha256sum -c CORE.sha256
sha256sum -c SHA256SUMS
```

The entire independent mathematical record has SHA256
`62cc8aea6cdf1f666b8b555121c02ef1b26331ad3f8a2ac15e37c43529fb72da`.
It contains every dual profile, complete symbolic polynomials, complete
physical endpoint/floor matrices and congruence pivots. The explicit
`--generate` option regenerates data; it is not an external-fixture check.
All mathematical conditions raise under optimized Python.

[audit.py](audit.py) imports only the independently written actual-set
[original.py](original.py), signed-permutation polynomial [uniform.py](uniform.py)
and credited unchanged owned [exact.py](exact.py). It never imports the
author's code or frozen data. [validate.py](validate.py) runs normal/optimized
checks and fresh semantic/malformed/duplicate-key fixtures, plus three
meaningful source changes in both modes, one math child at a time with
45-second guards. Timeout is inconclusive. The proof's infinite spectral
and tail premises remain explicit imports, not finite extrapolation.

For the separate postseal comparison, from a full repository checkout:

```sh
mkdir -p scratch
python3 export_target.py --record scratch/author-export.json
python3 -I -B compare_target.py scratch/author-export.json ../../six-downset-3/core-edge-five-cutoff/RESULT.json
python3 replay_target.py --receipt scratch/native-replay.json
```

Both adapters check every pinned target file before importing or executing.
The native target itself checks its two historical executable dependencies
before import. Optional `--target-directory PATH` accepts an immutable tree
with the same directory layout and whole bytes. [TARGET_ACCESS.json](TARGET_ACCESS.json)
records the complete source pins and source commit separately. Both actual
public adapters were run successfully after the independent seal; no
private exporter is needed to reproduce the comparison.

[INDEPENDENCE.json](INDEPENDENCE.json) gives the first seal chronology;
[ADAPTER_VALIDATION.json](ADAPTER_VALIDATION.json), [VALIDATION.json](VALIDATION.json),
[TARGET_COMPARISON.json](TARGET_COMPARISON.json) and [NATIVE_REPLAY.json](NATIVE_REPLAY.json)
provide compact full comparison/measurement evidence. [STRUCTURAL.json](STRUCTURAL.json)
records the independent six-edge completeness check, crediting9735.
The structural addendum is postseal; all five original executable/proof files stay
unchanged. The frozen record was normalized to plain canonical JSON
after the seal; every decoded value and its full canonical hash remain
identical. Both original/published byte hashes are disclosed. No optimizer, floating spectrum, solver result, imported
large proof corpus or external CAS is a mathematical premise.
