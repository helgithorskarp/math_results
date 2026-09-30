# Independent saturated absent-pair audit

Author: **six-reviewer-1**, role: **independent mathematical reviewer**,
2026-09-30. The shared graph signing key does not establish distinct authorship.

The audit confirms the exact maximum **56** for five-subset packings on
18 points with pairwise intersections at most two, two distinguished point
degrees 20, and no word containing both distinguished points. Consequently
every pair occurs in any hypothetical 72-word `(18,6,5)` code, using Brouwer's
established point-degree bound.

It also classifies equality: **two code isomorphism types**, with degrees
`[15]*16+[20,20]` and automorphism group orders **32** and **8**. Their residual
words are uniquely determined by their two saturated stars. See
[REVIEW.md](REVIEW.md) for the reduction, complete coverage, symmetry proof,
prior-art qualifications and precise trust boundary.

From this directory, Python 3.10+ standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B audit.py --check expected.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B -O audit.py --check expected.json
```

The program regenerates every instance without reading campaign modules,
downloaded catalogs or solver output. `expected.json` is a compact replay
record, not a stand-alone refutation certificate. Complete normal and
optimized runs took about 7.5 and 15 seconds locally and less than 50 MiB
peak RSS. A node cap raises
`INCOMPLETE`; incomplete output proves no upper bound. `--pilot N` intentionally
returns an incomplete prefix and cannot be combined with a certification check.

The independent second-plane algorithm uses exact cover of point pairs.
The source author instead completes Latin grids and separately checks
parallel-class cliques. The residual algorithm here solves maximum
independent sets in the conflict graph with memoized include/exclude
recursion. All guards remain active under Python `-O`.

Optional comparison against the author's pinned manifest, after full
regeneration:

```sh
python3 -B audit.py --compare-author /path/to/original/expected.json
```

Original source commit: `2e5f4a01e3f4e4f0983a11690d7b0df9b621c0e8`, directory
[`coding_theory/a18_6_5_saturated_absent_pair`](https://github.com/helgithorskarp/math_results/tree/2e5f4a01e3f4e4f0983a11690d7b0df9b621c0e8/coding_theory/a18_6_5_saturated_absent_pair).
That comparison checks all 93 second-plane lists, common-five-arc lists,
maxima, 38 representatives/orbit sizes and branch completion counts entry
by entry. No original data enter the independent proof enumeration.

To reconstruct an attaining code, take the first field plane from
`expected.json`, any case with `maximum == 16`, append coordinate 16 to
each first-plane line and coordinate 17 to each second-plane line, and
include all 16 `common_five_arcs`. Masks use bit `i` for coordinate `i`.
The independent audit directly checks all resulting word pairs and degrees.
The three ordered-center representatives are recorded in
`attaining_configuration_orbits`; the last two become isomorphic when the
center order is forgotten.

The global interval remains **69--72**. No unrestricted upper-bound
improvement, global code census or historical-priority claim is made.
