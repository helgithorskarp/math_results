# Independent review of the weighted T721 fixed-host exclusion

Verdict: **accepted with high confidence at source commit
`b12741b584cf453511f1d8d88db3e4497c6290a2`**.

The accepted theorem is limited to one explicit host. Let `G` be the strict
unit-distance graph on the 1,441 points obtained by joining the pinned native
Heule `T721.vtx` support to its stated rotated copy. Every subgraph of `G` with
at most 573 vertices is four-colourable, including arbitrary vertex subsets and
arbitrary edge deletions. The host also contains no Moser spindle.

This is a strong negative fixed-host result. It is not a five-chromatic graph
below 509 vertices, a record improvement, a proof that an obstruction of order
574 exists, or a statement about other coordinate supports.

## Independent audit

[audit.py](audit.py) imports no code from the reviewed package and uses a third
geometry route:

1. SymPy's Mathematica parser reads the 721 native coordinates from the pinned
   40,529-byte input. Symbolic arithmetic applies the exact spindle rotation and
   collects coordinates in the eight-element multiquadratic basis at scale 96.
2. Two new ring projections, modulo 1,511 and 1,559, filter all 1,037,520 point
   pairs. Every survivor is decided in SymPy's exact
   `QQ<sqrt(2),sqrt(3),sqrt(5)>` algebraic field. This reproduces all 1,441
   points, 7,897 unit edges, both 3,948-edge halves, their sole shared anchor,
   and unique bridge, with the submitted coordinate and edge hashes.
3. A fresh decoder validates all 12 seed, 196 rotation, and 28 patch records.
   It checks 236 terminal-separating half omissions, then independently searches
   the palette maps and checks every one of the 475 full-host deletion words.
   The audit performs 933,264 half-edge and 3,746,101 global edge comparisons
   and reproduces the submitted global-word SHA-256.
4. The 89 positive integer weights are checked directly against the independent
   graph. Their total is 117, the mandatory-set incidence is 269, and every
   outside vertex has weighted incidence at most two except vertex 217, whose
   incidence is three.
5. A separate graph census finds 1,392 unit diamonds and no pair of their arms
   completing a Moser spindle.

The target's normal and optimized verifiers, controls, SHA-256 manifest, and
byte-for-byte certificate producer also passed. Those checks are corroboration;
the review verdict rests on the separate audit and the argument below.

## Re-derived lower bound

The deletion words give a 475-element set `M` such that `G-v` is four-colourable
for every `v` in `M`. Hence any non-four-colourable subgraph contains all of
`M`. Take a vertex-minimal non-four-colourable subgraph with vertex set `S`.
Every vertex of it has degree at least four, since a four-colouring after deleting
a vertex of degree at most three extends greedily.

For the certified weights `w_v`, put
`t_u = sum_{v adjacent to u} w_v`. Since the weights are supported on `M` and
`M` is contained in `S`, double counting gives

```text
468 = 4 * 117
    <= sum_{v in M} w_v |N(v) intersect S|
     = sum_{u in S} t_u
    <= 269 + 2(|S|-475) + 1.
```

Therefore `|S| >= 574`. Any non-four-colourable graph of order at most 573
would contain a vertex-minimal one of no greater order, a contradiction. Edge
deletions cause no issue: degrees in the strict host induced on `S` dominate
degrees in the selected edge subgraph.

## Reproduction

From the repository root, using Python 3.11+ and SymPy 1.14.0:

```sh
python3 -m venv /scratch/research-team-v2/tmp/reviewer-1/t721-review-venv
/scratch/research-team-v2/tmp/reviewer-1/t721-review-venv/bin/pip install \
  -r hadwiger_nelson_t721_weighted_cover_review1/requirements.txt
python3 -B hadwiger_nelson_t721_weighted_cover/fetch_input.py \
  /scratch/research-team-v2/tmp/reviewer-1/t721-review/T721.vtx
/scratch/research-team-v2/tmp/reviewer-1/t721-review-venv/bin/python -B \
  hadwiger_nelson_t721_weighted_cover_review1/audit.py \
  --target hadwiger_nelson_t721_weighted_cover \
  --input /scratch/research-team-v2/tmp/reviewer-1/t721-review/T721.vtx \
  --expected hadwiger_nelson_t721_weighted_cover_review1/expected.json
```

The audit is deterministic, single-threaded, and uses no solver or floating-point
acceptance decision.

## Provenance and trust boundary

Reviewed Discovery contribution:
`bafkreieuht6l4x46a65oihaiavxy4mbjt2dkurtit6fgbos5enqpy5snmq`.
The reviewed directory is unchanged from source commit
`b12741b584cf453511f1d8d88db3e4497c6290a2`.

The remaining trust base is the pinned native-coordinate file, SymPy's parser
and exact algebraic-number arithmetic, squarefree-radical linear independence,
CPython integer arithmetic, SHA-256 collision resistance, this checker, and the
short minimum-degree/double-count argument. The input's upstream authorship and
historical context are not independently audited. No SAT answer, LP optimality,
search completeness, floating-point equality, or imported assertion that the
full host is five-chromatic is used.
