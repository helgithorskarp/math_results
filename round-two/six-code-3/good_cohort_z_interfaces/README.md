# Local two-interface classification and upper64

Actual author: **six-code-3, researcher**. The [local theorem](PROOF.md)
specifies two degree20 stars, their row and isolation hypotheses, and an
uncovered-triangle condition. It forces pair multiplicity3 at the deficient
hub and total size at most64;61/64 apply to its two surviving interfaces.
The bounds are not asserted sharp. No hub multiplicity, other replication
profile or whole-code symmetry is assumed.

All360 normalized marked products are complete. Block-tail matching and
a separate literal point-assignment DFS agree on933120 partial maps,
representing5598720 full maps, and all34 compatible36-word unions.
Thirty-two have actual forbidden triangles; the two others match the
[published seeds](../two_saturated_seed_interfaces/README.md).
No new coloring search is needed.

From the repository root, using Python3.11+ and its standard library:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 round-two/six-code-3/good_cohort_z_interfaces/reproduce.py \
  --work scratch/good-z-normal
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -O round-two/six-code-3/good_cohort_z_interfaces/reproduce.py \
  --work scratch/good-z-optimized
```

Both commands cold-regenerate every product and compare the full pre-existing
[expected](expected.json) and [34-map bridge](BRIDGE.json). They independently
check45 triangle witnesses, both inherited color certificates and30 semantic
damage controls. Three relabelings of all23 fixture stars also pass.
Recorded complete times106.222s/57.587s, peak child25700KiB; each run is serial
with unchanged1CPU/2GiB scope,200000 DFS states/10s per product and60s per
subprocess. Guards and incomplete output prove no mathematical absence.

The positive/triangle/cap bridge can also be checked independently of the
complete carrier:

```bash
python3 round-two/six-code-3/good_cohort_z_interfaces/check_bridge.py \
  --bridge round-two/six-code-3/good_cohort_z_interfaces/BRIDGE.json \
  --fixtures round-two/six-code-3/good_cohort_z_interfaces/fixtures.json \
  --seeds round-two/six-code-3/good_cohort_z_interfaces/seed_certificates.json
```

That small check alone does not establish completeness of the34-map list.
The full carrier and ordinary reduction are also needed. Point masks use
bit p for point p. Carrier hashes use compact sorted-key JSON without a
newline; inherited seed candidate hashes keep their original final newline.

[DEPENDENCIES.json](DEPENDENCIES.json) credits the reviewed generic23-star
classification and byte-pinned fixtures, and the earlier literal seed
certificates. [VALIDATION.json](VALIDATION.json) records actual checks.
Same-author algorithm independence is not a new independent peer verdict.
Ordinary bridges are unformalized and historical priority is unassessed.
Unrestricted campaign bounds remain69--71. The separate two-unsaturated
charging and profile transfer retain their own premises and review status.
