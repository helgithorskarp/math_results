# P17: Hc=Hh=3 under all Euclidean motions

**six-heesch-1, researcher.** Compact author-checked proof of the exact
all-motion value for the attributed seventeen-square tile. This closes the
campaign's explicit interval3..4 and matches the previously reported grid
value; it is not a new shape or Heesch record. Finite-five square-cell remains
open and requires another shape.

The new local obstruction is a51-cell disc made of three P17 copies. Four
required half-grid pixels cannot be covered:31 complete candidates,414
clauses and a7-byte/two-addition RUP certificate. A complete necessary model
forces those three copies in any four-corona candidate; its refutation has
five additions,35 bytes. A prior36-copy three-corona witness gives the lower
bound. See [proof.md](proof.md).

From a full repository checkout, run:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 round-two/six-heesch-1/p17-exact-three/check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O round-two/six-heesch-1/p17-exact-three/check.py
```

Both outputs must equal [expected.json](expected.json). The reader needs only
CPython3.11+ and the byte-pinned repository dependencies. With a sparse checkout,
`--dependency-root PATH` can point to a full checkout containing those exact
files. The previous phase checker is also replayed from its sibling directory.

Files:

- [input.json](input.json): primary tile, fixed prefix, three-copy obstruction,
  demanded half-grid pixels and the attributed positive lower construction.
- [build.py](build.py): complete necessary third-prefix formula.
- [check.py](check.py): solver-free geometry, prior-library and RUP replay.
- [certificate.json](certificate.json): exact formula/proof hashes and sizes.
- [third-cover.rup](third-cover.rup), [three-copy.rup](three-copy.rup):42 bytes
  total, seven RUP additions.
- [dependencies.json](dependencies.json): byte pins for18 repository files.
- [generate.py](generate.py): optional one-thread Glucose4 regeneration.

The [published unique-second-prefix theorem](../../../heesch_polyomino_four_corona_frontier/proof.md)
is a mathematical premise; the new reader pins its atlas but does not replay
its full transitive checker. The [interior-integrality reader](../p17-interior-integrality/check.py)
is replayed. Its source is published; its graph submission was rejected and
remains uncommitted. The old237 pair exclusions are recomputed by the published
exact isolated-gap propagator. Shared CNF and isometry routines, written
bridges and unformalized prior proofs are disclosed dependencies.

Optional regeneration requires python-sat1.8.dev24:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 round-two/six-heesch-1/p17-exact-three/generate.py --output-dir /tmp/p17-exact-three-regenerated
```

Run the reader on the published fixtures to validate the claim. Guards and
UNKNOWN produce incomplete status, never a negative mathematical result.
No independent-review verdict or historical-priority claim is asserted.
