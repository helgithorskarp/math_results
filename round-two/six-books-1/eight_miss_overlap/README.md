# Overlap at most one in the regular eight-row branch

Actual author **six-books-1**, role **researcher**, 2026-10-01.

For a red ten-regular, order-22 graph avoiding ordinary red B4 and blue
B7, an eight-point miss row forces the pattern `8+5+5+4^8` by
[parent lemma 8621](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/regular_eight_miss_rows/PROOF.md).
The two five-rows intersect inside the eight-row in **at most one point**,
sharpening that lemma's bound two. If they share a point a, their union
covers both omitted points, and the three local red neighbors of a
are exactly the complement of their Z union and W intersection.
[PROOF.md](PROOF.md) gives the precise formula and the ordinary proof.

The new bridge is short: shared Z points avoid both independent Z
parts and the shared W part. With two shared points, their neighbor
triples must lie in a four-point set and intersect in at least two
points, while the three large rows require intersection at most one.
With a single shared point, its three available neighbors are forced.

This is a complete analytic corollary, unformalized and conditional on
the parent's explicitly stated regular hypotheses. It is a strengthening
of a true parent statement. Independent review is pending. The
unrestricted Ramsey gap remains **22..23**, and the residual eight-row
host problem is unresolved.

Use **CPython 3.11.2**, standard library only, one command at a time from
the repository root:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B round-two/six-books-1/eight_miss_overlap/check.py
python3 -B -O round-two/six-books-1/eight_miss_overlap/verify.py
```

The generator checks all 38,416 ordered five-set pairs meeting the
fixed two-point W. The separate checker, with no generator imports,
derives every one of the 15 compact type records by a four-cell
multinomial and an independent W intersection count. Their full type
tables agree. The parent retains 32,480 templates; the new restrictions
retain 12,600 before any further local-graph or host constraint. These
are set-template counts, with no graph existence or finite host census
assertion. The four-point triple test covers all 16 ordered pairs.
Five damaged records are rejected with assertions disabled.

Both programs share the stated author. They compare
[expected.json](expected.json); the written proof is the mathematical
bridge. Provenance and measured resource costs are in
[provenance.json](provenance.json). The parent's public source retains
the freshly reproduced primary 21-point witness and current primary
literature links. No external data or solver is needed for these checks.
