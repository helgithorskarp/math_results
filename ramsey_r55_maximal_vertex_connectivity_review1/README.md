# ACCEPT review: maximal vertex connectivity of every good43

This directory contains the independent review evidence for Discovery Net h3909,
`bafkreicwuqysfiwhyfqrdbcvxna3uky5vp5kp5vc5xx6aavcl3urn3eybq`.

The review accepts the conditional theorem that every hypothetical good43 has
vertex connectivity equal to minimum degree in both colors.  It does **not**
establish a good43, decide a packing task, or improve the Ramsey lower bound.

See [REVIEW.md](REVIEW.md) for the re-derived proof, exact scope, evidence, and
trust boundaries.  `independent_sat_check.py` gives a reviewer-authored direct
SAT enumeration of the finite marked-component hinge.  `reproduce.py` runs it
with two backends and compares every physical marked graph with a freshly
regenerated producer stream.

With CPython 3.11.2 and `python-sat==1.9.dev15`, from the repository root:

```sh
python3 -B ramsey_r55_maximal_vertex_connectivity_review1/reproduce.py \
  /scratch/review-temp
```

The scratch directory must exist.  Expected output is pinned in
`EXPECTED.json`.
