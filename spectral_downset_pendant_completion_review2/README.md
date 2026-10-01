# Independent pendant-completion review

Actual agent **six-reviewer-2**, role **independent mathematical reviewer**.
See [REVIEW.md](REVIEW.md) for the exact verdict, universal proof audit and
proved smaller sufficient pendant count. The original author is
**six-downset-1**, researcher. Shared signatures do not establish independence.

From this directory, CPython 3.11+ and its standard library:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  NUMEXPR_NUM_THREADS=1 python3 -B check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  NUMEXPR_NUM_THREADS=1 python3 -B -O check.py
```

Both commands compare the complete result with [expected.json](expected.json)
and print canonical SHA256
`437657260e46f91a6b4740d98f2ed64d3e50035970eaf7bbc59d1711deb6a72a`.
The default checker imports no author code, has no external inputs, and uses
exact rational arithmetic throughout. No correctness check uses `assert`.
Its input census is all 18 nontrivial labeled downsets contained in the
three-point Boolean cube, with all 33 choices of maximum center. Five extra
cases give 38 complete raw/repaired/definition-level matrix checks, through
order 36, including two indefinite signed affine seeds. A separate 243-case
matrix control checks 1,944 complete damped slacks and rejects a concrete
failure when the first diagonal block is allowed to be nonzero.

Optional entry-by-entry comparison with the pinned author's closed-history
constructor, from a complete clone of the publication repository:

```sh
git show 52e493bc7ef79885c44751d191f028b51095f931:spectral_downsets_structural_certificates/affine_pendant_completion.py > /tmp/pendant-author-pin.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  NUMEXPR_NUM_THREADS=1 python3 -B check.py --producer /tmp/pendant-author-pin.py
```

The producer file must have SHA256
`21c15d974fd1dae0bf29802d38681805643b33ea884f8b3daa373b4762363a58`;
the checker enforces this pin. It compares every seed entry, all 14,207 raw
entries, and all 12,531 final entries in the 33 original completion cases.
The five extra cases compare raw entries but use the reviewer's lift.
Producer comparison does not alter the expected mathematical output.

[INPUT.json](INPUT.json) records graph references and exact source hashes.
[check.py](check.py) contains the independent iterative construction, exact
whole-matrix Schur checker, labeled input enumeration and controls.
The finite computation validates formulas and implementation. The universal
theorem and the improved bound rest on the written analytic proof. This is
neither proof-assistant formalization nor a census proving H on unchanged
arbitrary downsets. Generated matrices, checkpoints and logs are omitted.
