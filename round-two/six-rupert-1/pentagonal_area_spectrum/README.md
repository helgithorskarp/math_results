# Pentagonal hexecontahedron: exact global shadow areas

Actual author **six-rupert-1**, role **researcher**, 2026-10-01.
Author-checked, unformalized and independently unreviewed intermediate
result. **Full Rupert status: OPEN.**

The standard pentagonal hexecontahedron has global minimum shadow area
in **30 projective generic directions** and maximum shadow area at its
**15 twofold axes**. In McCooey's original coordinate normalization:

| Quantity | Strict rational enclosure |
|---|---|
| Minimum shadow area | (13.656085205, 13.656085206) |
| Maximum shadow area | (13.996580274, 13.996580275) |
| Exact area-ratio scale ceiling \(U\) | (1.012390032, 1.012390033) |

Minimum shadows have **26** strict corners, maximum shadows **20**.
The minimum shadow's unique-length edge makes its proper planar
isometry group trivial. All closed fits at every minimum-area receiver,
with arbitrary proper source/roll, projected translation and scale
at least one, have unit scale, zero translation and a proper body
symmetry. The passage-scale supremum satisfies \(1\le\mu<U\), strictly
below the exact ceiling; no additional numerical decrement is claimed.
These statements apply to either handed form with same-handed moving
copies. They improve the earlier diameter bound below 1.054495196.

See [PROOF.md](PROOF.md) for exact formulas, geometric reductions,
motion scope, provenance, and the compactness/corner-count argument.
The result supplies no unit-scale passage or global non-Rupert proof.
Positive receiving neighborhoods around these generic minimum directions
are not claimed: two facet projections collapse into boundary edges.

## Reproduce

CPython **3.11+**, standard library only; one process and all numerical
threads one. Run from the repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B round-two/six-rupert-1/pentagonal_area_spectrum/check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B -O round-two/six-rupert-1/pentagonal_area_spectrum/check.py --negative-controls --emit
```

The first prints `PASS` only after all exact gates and the complete
expected-record comparison pass. `--emit` prints that regenerated
compact record, and `--negative-controls` also rejects six damaged
polygon witnesses. There is no solver, external hull library, live
network input or unpublished proof corpus.

The checker verifies 60 area vectors, 59 complete symmetry-reduced
facet-normal charts, 3,540 exact height signs, all 260 exposed-face
cube images, full minimum/maximum equality orbits, 4,232 projected
support signs, 46 strict turns and 25 unique-edge length comparisons.
The cover comprises 3,300 oriented brightness-zonotope facets. The
eight cube images on a hexagonal facet include possible interior points;
they are not all called vertices.

`polygons.json` stores just the two literal hull cycles and their seeds;
`expected.json` stores the compact regenerated result including exact
algebraic coefficients. Optional `--progress PATH` writes private
incomplete progress until every check passes. Interrupted or timed-out
work supplies no global result.

## Fixed prerequisite and trust

The neighboring `pentagonal_minimum_diameter` directory is required.
Its three small files have pinned SHA256 hashes:

| File | SHA256 |
|---|---|
| `verify.py` | `12c94ea3ab9d7bc42e2086dbb5fbb9154306d6fd7095a8be4b25bb44fefd5339` |
| `model.py` | `aa8512eed3abe60c8d897f725f7015ffb22617cf0287c3f0533ed23805c8084c` |
| `model.json` | `e1ce268370de64b35be62bd14ed36b63fe48dc240e5a73a80b5fe5136a2eec8e` |

Its named-solid/facet audit is a cited prerequisite, graph lemma8547,
source commit `86ab225fb8becbe66601a5da0b5b017e872e1833`.
This contribution reconstructs and matches its exact named vertex
orbits and then verifies every new area and polygon assertion. It does
not claim an independent implementation or a new review of that model.
See [VALIDATION.json](VALIDATION.json) for the final complete replay
times, observed peak memory, control outcomes and source hashes.

Arithmetic uses rational coefficients in
\(\mathbb Q(\phi)[x]/(x^3-2x-\phi)\) and outward rational intervals at
the positive root, with zero floating proof decisions. The trust boundary
is the Python implementation, the prerequisite model identification and
facet proof, and the written brightness, zonotope, planar-isometry and
compactness arguments. None is proof-assistant formalized.

Peer J74/RID brightness work and the independent J74 strict-supremum
refinement are credited in the proof. Their reviews apply to their own
targets. The earlier explicit fivefold-cap source is a separate result;
its rejected graph submission is no premise here.
