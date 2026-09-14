# All Parts-pole inversions are four-colourable

Invert the Parts509 point set about any one of its 509 vertices, omit that
pole, and apply any positive scale. **Every resulting strict plane unit-distance
graph on 508 distinct points is four-colourable.** Its unit-edge count is at
most **486**, attained by inversion about source point 0 followed by scale 2/3.
No smaller five-chromatic graph was found.

This covers every Möbius image with pole at one of the source points, up to
similarity and reflection. It is a restricted nonlinear construction theorem,
not a global vertex bound or a classification of free-pole inversions.
[PROOF.md](PROOF.md) gives the exact scope and proof.

The construction genuinely changes coordinates and rebuilds all contacts.
The earlier affine-frame, fixed-host edit and deletion-only exclusions do
not establish this result. The input is the hash-pinned Parts coordinate
list, reused from an existing repository package.

| Complete gate | Result |
|---|---:|
| Source poles | 509 |
| Distinct physical points per drawing | 508 |
| Labelled scale representatives | 65,548,002 |
| Nonempty residue supergraphs | 56,554,414 |
| Supergraphs certified 3-degenerate | 56,554,397 |
| Remaining positive four-colour words | 17 |
| Sharp maximum physical unit-edge count | 486 |

Residue buckets can combine different exact scales. Every true unit edge
survives into the appropriate supergraph, so its positive colouring suffices.
The table's bucket count is not a count of exact graphs or distinct real scales.

## Reproduce

From this directory in a complete checkout, with Python 3.11+, NumPy and a
C++17 compiler:

```sh
python3 -m venv /tmp/hn-inversion-venv
/tmp/hn-inversion-venv/bin/pip install -r requirements.txt
/tmp/hn-inversion-venv/bin/python -O verify.py --work /tmp/hn-inversion-check --sanitize
sha256sum -c SHA256SUMS
```

Expected: `PASS`,17 checked words,65,548,002 entrywise modular comparisons,
and an exact508-point/486-edge fixture. Runtime is about 48 seconds with the
recorded versions. The two geometry routes use norm ratios and explicit
inverted coordinates respectively. The fixture separately reconstructs all
128,778 physical pairs in an eight-radical Cartesian basis. No SAT solver is
needed for replay.

The generated uint32 comparison stream is about262MB. It, executables,
per-pole inventories and scratch results stay in the requested work directory
outside the repository. Source plus compact evidence is sufficient; no
unprovided search dump or proof trace is required.

Optional positive-word regeneration:

```sh
/tmp/hn-inversion-venv/bin/pip install -r requirements-discovery.txt
/tmp/hn-inversion-venv/bin/python generate.py --work /tmp/hn-inversion-producer --output /tmp/hn-inversion-producer/certificate.json
cmp certificate.json /tmp/hn-inversion-producer/certificate.json
```

The 10,062-byte certificate SHA256 is

```text
821d530500889925b044eaf0dedb937f827ff36c7b269a2f41791386a682a29a
```

`expected.json` supplies the complete compact census, checksums and fixture
result. `VALIDATION.json` records actual runs and versions. Verification is
author-side; no independent peer review or formalization is claimed.

## Provenance and record consequence

The only source input is
[`certificate_D7.json`](../hadwiger_nelson_parts509_degree_pool_minimum/certificate_D7.json),
SHA256 `41a47be8d0568be7e1497f16a45c17d433e31e01fb62877856189fbf1ad53729`.
Only its 509 original coordinate rows are used. No earlier non-four assertion,
source deletion word or source chromaticity proof is imported as a premise.

The supported record remains [Parts509/2442](https://arxiv.org/abs/2010.12665),
also stated in [Haugland's August 2026 introduction](https://arxiv.org/html/2608.04542v4),
refreshed 2026-09-14. Current team directions and new repository evidence were
inspected. Discovery Net's index remained stale at 4363; current durable
repository sources were used alongside it.

The complete declared inversion gate is retired. No free/midpoint pole
expansion is proposed. At the next natural campaign boundary, this lane
switches to selecting a small exact physical source with a useful composable
colour relation before expanding another family. No such successor is claimed
by this package.
