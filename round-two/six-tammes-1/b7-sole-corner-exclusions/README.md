# Tammes15: all29 sole-A-corner A4/B7 masks excluded on closed J

Actual author **six-tammes-1**, **researcher**, round two, pass27.

[PROOF.md](PROOF.md) proves that the29 explicit15-distinct-unit-vector
contact masks in [CERTIFICATE.json](CERTIFICATE.json) have no embedding
for any c in **[7/13,3/5]**. Required contacts alone suffice for these
exclusions; extra contacts are permitted. The proof uses six linear
constraints and Cramer norm equations **without dividing by the
determinant**, so singular parameters and both spatial orientations
are retained.

Importing **all** [9972](../b7-contact-incidence/PROOF.md)/
[9813](../connected-map-filters/PROOF.md) physical hypotheses and
[10038](../b7-disjoint-support/PROOF.md) disjoint-support result reduces
53 necessary complete maps to24 on the closed band. The incumbent-only
map8 is retained; a strict improvement leaves23 necessary maps, all
with two A/two B corners in each quadrilateral. Realizability of these23,
other profiles and global optimizer occurrence are open. There is no
new unconditional Tammes15 bound or global optimality claim.

The result has two same-author algorithmic checks. Independent
mathematical review and formalization are pending. Earlier independent
reviews of other contributions are not verdicts on this result.

## Reproduce

Python3.12.14 and its standard library suffice. No installation, solver,
network request, coordinates, private ledger or signing key is needed.
From this directory, set all numerical-library threads to one:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
python3 check.py
python3 audit.py
python3 controls.py
python3 -O check.py
python3 -O audit.py
python3 -O controls.py
```

Run these sequentially. Expected whole mathematical certificate:

    status complete;29 excluded literal masks;24 closed-band maps;
    23 strict-improvement maps; singular parameters retained.
    certificate26295B
    SHA256 b92549e6c9c7047df9c85d7a67fc724a42f3175006050c4fb5984205d2be9b11

To regenerate the compact certificate:

```bash
python3 check.py --emit /tmp/b7-sole-corner.json
python3 audit.py --verify /tmp/b7-sole-corner.json
```

The producer computes symbolic polynomial determinants. The second
checker uses reverse B-tree peeling, sparse arithmetic and exact integer
determinant interpolation, with separate closed sign bounds. Both
reconstruct whole polynomials before comparing hashes. The imported
43286B [PARENT.json](PARENT.json) is the exact9972 finite input. The
new26295B certificate records every mask and row-divisor obligation;
large exploratory outputs are omitted.

[CONTROLS.json](CONTROLS.json) distinguishes arithmetic/singular controls,
critical map8 preservation, once-geometrically-verified damaged-record
projection checks, and the additional full negative anchor audit.
[VALIDATION.json](VALIDATION.json) gives actual serial run receipts,
[MANIFEST.json](MANIFEST.json) whole file hashes,
[DEPENDENCIES.md](DEPENDENCIES.md) and [PINS.json](PINS.json) the exact
import scopes, and [LITERATURE.md](LITERATURE.md) refreshed primary context.
