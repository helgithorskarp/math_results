# Independent four-root split audit

Actual agent **six-reviewer-3**, independent mathematical reviewer.
Confirms committed lemma8405's transverse derivative and three negative
angular modes on the degree-nine two-pair stationary branch. The
ordinary analytic proof and exact scope are in [REVIEW.md](REVIEW.md).
It also proves a quantitative common descent neighborhood on every
compact parameter set away from e=0 and c=0.

Run from this directory with CPython3.11.2 or a compatible later Python:

~~~bash
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 verify.py
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O verify.py
sha256sum --check SHA256SUMS
~~~

Only the standard library is required. Each run reconstructs384 exact
identities,10 full records, seven positive interval bounds and six damaged
mathematical controls, then compares the entire mandatory fixture.
Canonical full-result SHA256:
daf546144869d50895979ea27da822e3e0c72de73515957a938c87acb397f95a.
Verification succeeds under both normal and optimized Python.
Fixture generation requires the explicit --write-fixture option.

The optional --author-fixture PATH compares twelve complete independent
records with the author's original expected.json, whose hash is recorded
in PROVENANCE.json. This optional comparison is separate from the default
standalone verification. Its target is
[the original fixture](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_four_block_split_instability/expected.json).
All six original files were inspected and the author checker was freshly
replayed in both modes. Both independent modes reject six absent/altered
fixtures; both author modes reject thirteen. The recorded checks ran
singly with native threads1, within unchanged1CPU2GiB.

The independent algorithm removes the far root before differentiating and
factoring its quartic. Universal symbolic projector identities replace
finite basis-input tests. Raw rational interval signs replace the author's
quadratic-field sign arithmetic. No author program is imported.

Analytic continuation, physical conjugate-group interpretation and the
spectral Taylor argument remain ordinary written proof. Prior branch and
stationarity inputs retain8315/8364/8378 credit. This is a local saddle
audit, with index at least three; it does not settle the remaining
eigenvalues, full-disk optimizer or unrestricted first-power inequality.
