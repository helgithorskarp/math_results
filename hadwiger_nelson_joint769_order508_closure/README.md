# Complete order-508 closure of the 769-point fresh-triangle host

Let `S` be the certified 509-point nine-move seed. The sibling
[cyclic-batch package](../hadwiger_nelson_cyclic_batch_probe/README.md)
enumerates 126 fresh unit equilateral triangles in
`Q(sqrt(3),sqrt(5),sqrt(11))`. Their union has 260 points. Let `H` be the
strict unit-distance graph on `S` together with those 260 points.

This package proves the following finite-host theorem.

> **Theorem.** Every subgraph of `H` on at most 508 vertices is
> four-colourable.

Exact reconstruction gives 769 distinct points and 3560 unit edges: 2447
between seed points, 656 between the seed and added points, and 457 between
added points. Thus this entire joint host contains no graph that improves the
current target order. The search did not find a five-chromatic graph with at
most 508 vertices.

As of 7 September 2026, the comparison baseline remains Parts's
[509-vertex graph](https://arxiv.org/abs/2010.12665). Haugland's
[August 2026 manuscript](https://arxiv.org/abs/2608.04542) also identifies it
as the current record. No priority claim beyond the stated finite-host theorem
is made.

## Positive-certificate proof

Number the seed vertices `0,...,508` and the added vertices `509,...,768`.
For a vertex set `J` of order at most 508, let `D` be the seed vertices omitted
from `J` and let `A` be its retained added vertices. Then

```text
|A| <= |D| - 1.
```

The certificate first supplies a proper four-colouring of `H-u` for each of
501 seed vertices `u` outside

```text
T = {113, 114, 184, 186, 346, 349, 366, 367}.
```

It also supplies proper four-colourings after deleting either boundary pair

```text
{184,349}, {186,346}.
```

If `D` contains one of those 501 vertices or one of the two pairs, restricting
the corresponding colouring colours `J`.

It remains to handle the nonempty subsets `D` of `T` that contain neither
pair. There are exactly

```text
2^8 - 2^6 - 2^6 + 2^4 - 1 = 143
```

such patterns. Each has size at most six, so `|A| <= 5`. The certificate's 15
global rows each give a proper colouring of

```text
(S minus D0) union M,
```

where `D0` is one residual seed-deletion pattern and `M` is a subset of the
260 added vertices. A row applies to `D` whenever `D0` is contained in `D`.
For every one of the 143 patterns, the verifier proves that each added-vertex
set `A` of size at most `|D|-1` is contained in `M` for an applicable row.
It does this as a complete bounded hitting-set search on the complements of
the `M` sets. Restricting that row's colouring then colours `J`.

The four maximal residual patterns are

```text
{113,114,184,186,366,367}
{113,114,184,346,366,367}
{113,114,186,349,366,367}
{113,114,346,349,366,367}.
```

This argument uses 503 boundary colourings and 15 global cover colourings.
Every colour is checked on every retained edge. The theorem uses no SAT
verdict, UNSAT certificate, floating-point comparison, or assumption about
the private search that found the rows.

## Exact reconstruction and verification

From the repository root, CPython 3.11 or later and the standard library are
sufficient:

```sh
python3 hadwiger_nelson_joint769_order508_closure/reproduce.py \
  --output /tmp/hn-joint769-closure
python3 hadwiger_nelson_joint769_order508_closure/controls.py
```

The first command regenerates the complete sibling two-circle census and seed
certificate. It then scans all 295,296 unordered host pairs exactly in the
basis

```text
1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165),
```

reconstructs the edge digest, decodes all 518 colouring rows, and verifies all
143 cover cases. Expected output includes:

```json
{
  "all_checks": true,
  "host_vertices": 769,
  "host_edges": 3560,
  "positive_rows_checked": 503,
  "cover_rows_checked": 15,
  "residual_cases_checked": 143,
  "target_order": 508,
  "target_found": false,
  "solver_or_unsat_proof_inputs": 0
}
```

The complete geometry replay takes roughly two minutes on the recorded
machine. Expanded source geometry, host edges, and verification output are
written below the requested output directory and remain outside Git.

`certificate.json` stores two separately hash-bound
`base85(zlib(binary))` blobs. The first is 96,576 raw bytes for the 503
boundary rows. The second is 2,985 raw bytes for the 15 cover rows and their
small missing-point sets. `verify.py` checks the compressed and raw lengths,
the raw SHA-256 digests, colour padding, row boundaries, active vertex sets,
every proper colouring, and complete byte consumption.

## Scope and provenance

The theorem closes every subgraph of this exact 769-point host through order
508. It does not classify other field-valued circle intersections, non-field
intersections, different seed mutations, or supergraphs with additional
points.

Seventeen private multistart passes found critical cores from 529 to 563
vertices; the smallest retained 503 seed points and 26 added points. That was
candidate discovery rather than a minimality proof. The subsequent finite
boundary calculation produced the stronger full-host closure published here.
Private SAT runs and four DRAT traces were used to explore the host, but none
is a premise of this theorem or an input to the public verifier.

The source-package commits, hashes, search checkpoint, and primary-source
calibration are recorded in `provenance.json`. `expected.json` gives the
concise deterministic result.
