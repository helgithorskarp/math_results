# Six completion bridges do not repair a deletion from Parts 509

## Result

Let `P` be the strict unit-distance graph on Jaan Parts's 509 record points.
Adjoin the following six points, written in
`Q(sqrt(3),sqrt(5),sqrt(11))`:

```text
b0 = (0,                 -sqrt(3)/6 + sqrt(11)/2)
b1 = (0,                  sqrt(3)/6 + sqrt(11)/2)
b2 = ((1+sqrt(33))/4,    -sqrt(3)/12 - sqrt(11)/4)
b3 = (-(1+sqrt(33))/4,   -sqrt(3)/12 - sqrt(11)/4)
b4 = ((-1+sqrt(33))/4,    sqrt(3)/12 - sqrt(11)/4)
b5 = ((1-sqrt(33))/4,     sqrt(3)/12 - sqrt(11)/4)
```

Call this set `B`. Exact reconstruction gives 2,482 unit pairs on the 515
points of `P union B`: the 2,442 Parts edges and 40 edges from `B` to `P`.
There is no unit edge inside `B`; the six degrees into `P` are
`7,7,7,7,6,6`.

The certified theorem is:

> For every subset `C` of `B`, the minimum order of a non-4-colourable
> induced subgraph of the strict graph on `P union C` is exactly 509.

Equivalently, for every nonempty `D subset P` and every `C subset B`, the
strict graph on `(P minus D) union C` is 4-colourable. Thus these six points,
even when all are added together, cannot repair the deletion of a single
Parts vertex and cannot produce a graph on at most 508 vertices.

This closes 64 augmentation subsets of one specific six-point family. It does
not cover arbitrary sets of six added points, other transformed completion
centers, or points outside the exact Parts completion pools.

## Why these points

The six points arose from an exact exploratory scan of the 1,158 external
completion centers in the sibling Parts census after applying the six
exceptional small-gadget rotations. Among the 2,462 distinct transformed
centers outside the full six-placement union, these were the only points in
that pool having a unit neighbor in each of its two 159-position extension
copies. Four have degree eight and two degree seven in that 692-vertex union.

That scan motivates the family but is not needed for this theorem. The
certificate defines the six coordinates explicitly and recomputes their
strict graph with `P` from scratch.

## Proof certificate

For every Parts vertex `v`, the certificate stores an explicit proper
4-colouring of

```text
(P union B) minus v.
```

If a non-4-colourable induced subgraph `H` of `P union B` omitted `v`, it
would be a subgraph of that colourable graph. Hence `H` contains every one of
the 509 vertices of `P`, proving `|H| >= 509`. Conversely, `P` itself is an
induced non-4-colourable subgraph, so equality holds.

Restricting a colouring to any `C subset B` proves the statement for all 64
augmentation subsets simultaneously. The lower bound uses only positive
colouring witnesses; no negative SAT or optimization answer is trusted.

## Verification

Run with Python 3.11 or later:

```bash
python3 verify.py
```

The standard-library verifier:

- pins the sibling `points.tsv` and Parts criticality certificate by SHA-256;
- reconstructs all 515 coordinates as integer coefficients at scale 96;
- tests all 132,355 unordered point pairs exactly in the eight-element
  radical basis;
- recovers the 2,442-edge Parts graph and all six bridge neighborhoods; and
- checks 1,258,414 edge incidences across the 509 deletion colourings.

The exact output is in `expected_check.txt`. Headline values are:

```text
vertices=515
edges=2482
bridge_degrees=7,7,7,7,6,6
base_deletion_colorings=509
augmentation_subsets_closed=64
minimum_non_four_colorable_order=509
edge_sha256=f665c9a30ed9e8691a0c2ffceb32bbe47e369ae74491b1aa2bba9e44496df20d
```

Certificate SHA-256:
`8251873913e844156f4f6608ac74ea0430271e901a68cfca2839edbf2f182c9b`.

## Regeneration

PySAT and CaDiCaL are needed only to regenerate positive witnesses:

```bash
python3 -m venv /scratch/parts509-six-bridge-venv
/scratch/parts509-six-bridge-venv/bin/pip install -r requirements.txt

/scratch/parts509-six-bridge-venv/bin/python generate_witnesses.py \
  /scratch/parts509-six-bridge-raw.json

python3 build_certificate.py \
  /scratch/parts509-six-bridge-raw.json \
  /scratch/parts509-six-bridge-certificate.json

cmp certificate.json /scratch/parts509-six-bridge-certificate.json
python3 verify.py /scratch/parts509-six-bridge-certificate.json
```

The tested run used CPython 3.11.8, `python-sat 1.8.dev24`, and CaDiCaL
1.9.5, took 119 seconds on one core, and reproduced the committed certificate
byte-for-byte. Solver determinism is convenient but not part of the proof:
any regenerated certificate is accepted only after every coloring is checked
directly.

## Trust boundary and provenance

The exact graph and all 509 positive witnesses are checked without a solver.
The statement that the embedded Parts graph is non-4-colourable depends on
the sibling DRAT-audited criticality artifact. Arithmetic trusts CPython
integers, tuples, JSON, Base64, and SHA-256; this is not a proof-assistant
formalization.

The base construction is from Jaan Parts,
*Graph minimization, focusing on the example of 5-chromatic unit-distance
graphs in the plane*, Geombinatorics 29(4) (2020), 137--166,
<https://arxiv.org/abs/2010.12665>. The completion-center context is from the
sibling `hadwiger_nelson_parts509_completion_census_degree9` artifact. No
unconditional historical-priority claim is made for the scoped augmentation
closure.

## Files

- `verify.py` is the solver-free exact checker.
- `certificate.json` stores the six coordinates and packed colourings.
- `generate_witnesses.py` regenerates the positive colourings with PySAT.
- `build_certificate.py` validates and packs a raw generator checkpoint.
- `requirements.txt` pins the generator-only dependency.
- `expected_check.txt` records the exact verifier output.
