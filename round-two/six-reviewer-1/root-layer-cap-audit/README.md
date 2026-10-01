# Independent all-order root-layer review

**six-reviewer-1**, independent mathematical reviewer, fresh round two.

[REVIEW.md](REVIEW.md) confirms committed lemma8256 on every integer n>=6,
with explicit inherited n=4/5 feasibility, and derives a rational lower
bound for the largest eigenvalue of any ordinary complement-only H matrix.
The cap is additional to H. General H/I and general capped feasibility are
unresolved by this review.

[audit.py](audit.py) imports no author executable. It reconstructs the complete
polynomial by exact interpolation with written degree bounds, checks all65
positive shifted coefficients, and validates the generic dual identity and
every free coefficient in full signed affine matrices at orders6/7.
The finite controls support the written all-order argument; they are not
a finite search for all matrices.

From the repository root, CPython3.11.2, standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -B round-two/six-reviewer-1/root-layer-cap-audit/audit.py \
  --check round-two/six-reviewer-1/root-layer-cap-audit/expected.json
```

Repeat with `python3 -B -O`. Both runs reproduce [expected.json](expected.json)
exactly: SHA256519c8ef85bd8c9e4281988c3819f2116d937c12502a9fc2cee18a1f9a12f945a.
Recorded runtime below one second, child RSS below21MiB, one local job and
one native thread. The optional `--author-certificate PATH` compares the
full independently generated arrays with the author's compact JSON.
[PROVENANCE.json](PROVENANCE.json) pins the reviewed source and methodology.
No solver, CAS, float, private input or omitted large certificate is required.
