# Three-deletion boundary and two-deletion continuation

six-downset-3, researcher. For the exact affine triangle-majority table
and scalar four-edge repair on D(q,Z), |Z|=3, capped H feasibility
holds precisely for integer q>=8 (within the standing q>=4 domain).
The all-real-parameter exclusions at q4..7 use explicit PSD duals.
Four original corner pairs prove the q8 real rectangle; finite cap
continuity covers q9..11; credited9195 covers the unbounded tail.
The same bridge completes the credited two-deletion construction to
every q>=4. See [PROOF.md](PROOF.md) for hypotheses and full proof.

This is an author-checked, unformalized computer-assisted lemma.
Independent review is pending. General H/I and certificates outside
the specified table/repair ansatz are not decided here.

Reproduce from this directory using Python3.11+ and the standard library:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O verify.py
sha256sum -c SHA256SUMS
```

The replay requires the compact SHA-pinned files in the sibling
triangle-majority, two-deletion-kappa and adaptive-deletions directories.
Obtain them from the same repository; their historical source commits
and seven byte hashes are in [bootstrap.py](bootstrap.py). No private
input, search transcript, dataset, solver or large proof corpus is
needed. The independently evaluated upper duals can also be checked
alone with `python3 duals.py`; this uses only literal.py and DUALS.json.

[entries.py](entries.py) constructs individual rational whole M entries
without allocating a domain, including the actual empty loop and row.
It retains exactly the proved real parameter regions but accepts exact
rational inputs. q8 requires3/8<=t<=1/2; it does not allow every smaller
positive t. The dense finite checker has a separate q<=11,N<=137 guard.

[EXPECTED.json](EXPECTED.json) is the entire frozen mathematical record,
[DUALS.json](DUALS.json) contains the small literal upper dual vectors,
and [RESULTS.json](RESULTS.json) records compact validation provenance.
The public replay is serial, single-threaded and fixed60s per process;
an operational timeout reports an incomplete run, never nonexistence.
