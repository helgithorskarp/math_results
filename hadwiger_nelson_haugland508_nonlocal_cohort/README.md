# Sixteen nonlocal 508-point Haugland subsets are four-colourable

Every graph in the frozen cohort below has **508 distinct exact plane points**
and a directly checked proper four-colouring of its **complete** unit graph.
The 16 supports are distinct and connected, retain both cross-half edges of
Haugland's graph, and have 2,105–2,142 unit edges. This closes this finite
extraction attempt. It does not classify arbitrary subsets of the parent,
all deletion orders, or any five-chromatic critical core.

The cohort was frozen in full before the ordinary four-colour solver queries.
There was no terminal-relation census or conditional input colouring.

## The precise cohort

Use the exact labels of `G3` in the pinned sibling
[`graph.json`](../hadwiger_nelson_haugland2131_exact_reproduction/graph.json).
Its order is 2,131 and it has 12,530 complete unit edges. Its two 1,066-point
halves share vertex 0. The left private labels are 1–1065 and the right private
labels are 1066–2130. The only cross-half edges are `(303,1368)` and
`(435,1500)`.

For each seed `s=0,...,7` and each orientation `o=0,1`, start with all points.
Never delete a vertex in `{0,303,435,1368,1500}`. The target private-half
counts are `(254,253)` for orientation zero and `(253,254)` for orientation
one. A nonmandatory vertex is eligible for deletion only while its half has
more points than its target. Delete the eligible vertex with the smallest
tuple

```text
(current induced degree,
 SHA256(ASCII("HN2131-nonlocal-cap508-v1:s:v")),
 original vertex label v).
```

Here `s` and `v` in the string are replaced by their decimal integers with
no padding; SHA-256 digests are ordered as their 32 unsigned bytes. Recompute
the degree after every deletion. Stop when 508 vertices remain. The rules
define exactly 16 supports, without a solver-dependent selection step.

| Seed | Edges, orientation 0 | Edges, orientation 1 |
|---:|---:|---:|
| 0 | 2109 | 2110 |
| 1 | 2105 | 2106 |
| 2 | 2134 | 2133 |
| 3 | 2142 | 2141 |
| 4 | 2140 | 2139 |
| 5 | 2121 | 2122 |
| 6 | 2115 | 2115 |
| 7 | 2129 | 2129 |

All have minimum degree three; no exact chromatic-number-four claim is
needed or made. The literal four-colour words prove the required stop.
A checked restriction of the parent's proper five-colouring is also supplied
by the verifier; that upper bound does not make any support five-chromatic.

## Exact geometry and proof

The coordinates are indexed restrictions of the exact Appendix-A
reconstruction in `Q(zeta_84,sqrt(5))`. The earlier complete strict-edge
census is a pinned dependency. The new `--geometry` check reconstructs the
parent points from those paths, checks their coordinate hash and distinctness,
and reconstructs every unit pair in the 952-point union of the frozen
supports. A no-false-negative two-prime sieve rejects nonunit pairs; every
survivor is tested in the exact rational cyclotomic extension. Restricting
this complete edge list therefore proves completeness for all 16 supports.
The 952-point union is used only for geometry: its chromaticity is not tested
or claimed.

`verify.py` regenerates the selection by recomputing degrees directly from
induced neighbor sets. This differs from the producer's incrementally updated
priority heap. It checks the support and edge hashes, every literal colour
inequality, connectedness, and both retained cross edges. No SAT verdict is
trusted by the positive certificates.

The parent has a published five-chromaticity claim in
[Haugland's paper](https://arxiv.org/html/2608.04542v4). The earlier independent
repository reproduction left its endpoint-forcing lower-bound certificate
unfinished. This package neither assumes nor completes that missing proof:
the new result needs only the exact physical coordinates and positive words.

## Separation from earlier closed scopes

The verifier recomputes that the largest parent graph-distance ball of order
at most 508 has only 507 vertices. Thus none of these 508-point supports is
contained in a target-sized metric ball.

The triangle-isometry host lies in `K=Q(zeta_84)` in complex coordinates.
Our supports contain many left-half points in `K` and right-half points
outside `K`, whose nonzero `sqrt(5)` coefficients are checked exactly.
They cannot lie in an isometric image of that host: two distinct left-half
points would force the isometry's complex multiplier and translation into
`K`, since `K` is closed under conjugation; its whole image would then be in
`K`. The quadratic extension is genuine because 5 ramifies in `Q(sqrt(5))`
but not in `Q(zeta_84)`.

Finally, deleting source vertices is not an edge-preserving pointwise Galois
map of all 2,131 vertices. No folding, source-coordinate change or relaxed
realization is used here. These observations establish scope separation,
not evidence that the extracted graphs must require five colours.

## Reproduce

Run from this directory, using CPython 3.11 or newer and the standard library:

```sh
python3 -B verify.py > /tmp/hn508-checked.json
diff -u EXPECTED.json /tmp/hn508-checked.json
python3 -B verify.py --geometry > /tmp/hn508-geometry.json
diff -u GEOMETRY_EXPECTED.json /tmp/hn508-geometry.json
python3 -B controls.py
sha256sum -c SHA256SUMS
```

The sibling inputs must be present in the repository. `DEPENDENCIES.json`
pins their commits and hashes. To rerun the untrusted positive-word producer,
use Kissat 4.0.4 and an empty work directory outside the repository:

```sh
python3 -B produce.py --work /tmp/hn508-new-run --solver /path/to/kissat
```

Each query has a 10-second/100,000-conflict limit; any `UNKNOWN` stops the
cohort rather than granting a rerun. The recorded 16 queries were all SAT,
with about two seconds total solver wall time. Production CNFs, logs and
proof-output files stay outside Git. The verifier needs no solver.

The trust boundary is the pinned path transcription and exact geometry code,
the explicit cyclotomic and scope arguments, CPython arithmetic/parsing,
the deterministic finite loops and the supplied positive words. The different
selection implementations and malformed-word controls are author checks,
not independent peer review or proof-assistant formalization.

This is a scoped finite stop, not a record improvement. No extra seeds,
changed half quotas, additional points or follow-up deletion cohort is implied.
