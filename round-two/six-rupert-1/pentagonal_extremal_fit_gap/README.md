# Pentagonal hexecontahedron: a quantified passage-scale gap

**six-rupert-1, researcher; 2026-10-01.** Author-checked exact intermediate
result, unformalized and independently unreviewed. Full Rupert status
remains **OPEN**.

The exact minimum-area 26-corner shadow cannot fit inside the maximum-area
20-corner shadow at any scale **at least 200/201**, even with arbitrary
proper roll and translation. Thirty-eight positive balanced edge stresses
cancel every translation; their coefficient polygon contains the disk
of radius201/200, covering the entire roll circle.

This obstruction survives source normals within chord **1/500** of any
area minimum and receiving normals within chord **1/500** of any area
maximum, at all scales at least one. These are **coupled source/receiver
caps**, with both hypotheses required.

Combining them with exact global area localizers proves

\[
1\le\mu(K)<\sqrt{A_{\max}/A_{\min}}-10^{-6}<1.012389033.
\]

The [proof](PROOF.md) provides the explicit positive decrement below the
previous exact area-ratio bound. It does not decide whether a passage at
unit scale exists. A numerical fitting calculation suggested an optimum
near0.990843 for the frozen pair; that value remains heuristic, while
the stated obstruction and global decrement are certified exactly.

## Reproduce

Run from the repository root with **CPython3.11+**, standard library only,
one process and all numerical threads one:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B round-two/six-rupert-1/pentagonal_extremal_fit_gap/check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B -O round-two/six-rupert-1/pentagonal_extremal_fit_gap/check.py --negative-controls --emit
```

The checker regenerates the pinned parent's area and polygon premises,
then checks all38 exact stress rows,1368 strict dual-polygon supports,
38 disk and38 turn gates,92 original circumradius comparisons,38 transport
bounds,58 nonminimum facet levels,258 nonmaximum cube-image levels and
the final scalar margins. `--negative-controls` rejects four damaged
witnesses with guards active under optimization. `--emit` prints the
complete regenerated [expected record](expected.json).

[certificate.json](certificate.json) holds only original edge and vertex
indices. All positive weights are regenerated exactly. No floating solver
or angle grid is a replay input. Radical signs and bounds use outward
rational intervals and integer square roots, with zero floating proof
decisions. See [VALIDATION.json](VALIDATION.json) for measured runs and
source hashes. The optional author `--discovery` flag skips only expected
fixture comparison; the advertised reproduction commands perform it.

The neighboring `pentagonal_area_spectrum` and `pentagonal_minimum_diameter`
directories are required, with fixed small-file SHA256 hashes in the
checker/expected record. Mathematical prerequisites are graph lemma8743,
sourcee48f7eb2dda6f347ed98fc1eb1d11a76dc0a58e5, and named-model lemma8547,
source86ab225fb8becbe66601a5da0b5b017e872e1833. Prior independent J74 review
verdicts do not audit this contribution. The older rejected cap submission
is no premise. Written geometric bridges and Python remain unformalized
trust boundaries; interrupted or inconclusive computations prove nothing.
