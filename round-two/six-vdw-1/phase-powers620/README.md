# Canonical affine phase powers on the regular residues modulo 620

Author: **six-vdw-1, researcher**.

Every coloring in the explicitly specified primitive-root-3 phase-power family
has a nonconstant monochromatic seven-term arithmetic progression avoiding the
modulus-31 poles. The exact local reductions leave **92,800 parameter pairs**;
phase conjugacy covers them with **1,120 profiles**, each carrying an actual bad
progression in [catalogue.csv](catalogue.csv). Parameter counts can include
duplicate colorings. [PROOF.md](PROOF.md) specifies all quantifiers and the
conditional order-three subgroup reduction.

This is a finite construction-family exclusion. The 3704-point coloring target,
arbitrary regular period620 cores and arbitrary order-three-invariant cores
remain unresolved. No numerical van der Waerden improvement is asserted.

Use Python 3.10 or newer and the standard library. The completed checks used
Python 3.12.14 on Linux. There is no native solver, proof converter, package
installation, network access or prior campaign artifact in the reproduction.
From this directory, choose a fresh output directory:

```sh
python -I -B reproduce.py --work /tmp/phase-power-replay
```

The runner verifies [SOURCE_PINS.json](SOURCE_PINS.json) before executing source,
then runs a fresh generator, the separate checker in normal and optimized
Python, and controls in both modes. It compares whole result objects against
[EXPECTED.json](EXPECTED.json) and the entire regenerated catalogue against
the published bytes. Five children run sequentially, with one numerical thread
and a 35-second process-group guard for each child. A timeout, changed input or
rejection aborts reproduction; it supplies no exclusion. Expected total work
is roughly 17 seconds and tens of MiB, with machine-dependent timings.

For direct inspection:

```sh
python -I -B check.py catalogue.csv
python -I -O -B check.py catalogue.csv
python -I -B controls.py catalogue.csv
```

The generator uses iterative permutation powers. The checker independently
uses affine-power sums, actual CRT residues, the complete local truth table
and phase-group conjugacy. Every negative certificate is a seven-term integer
progression whose terms are regular and lie in [0,2479]. Nonclosed profiles
are retained as genuine canonical-log colorings. The generator's 9,600-point
search domain is a complete cross-AP cover **only for closed transport**; for
the other cases it is solely a witness search. The actual negative witnesses
prove the stated exclusion in both cases.

The controls include full small physical positive and negative examples,
arbitrary first-field color pairs, and 14 deliberately damaged catalogues.
Damage checks omit the expensive conjugacy/diagonal bridges explicitly; both
production checker runs include them. Details are in [VALIDATION.md](VALIDATION.md).

The trust boundary is author-written exact source plus the ordinary mathematical
reductions in PROOF.md. Separate algorithms written by one author do not claim
another person's independent review or proof-assistant formalization. The source
pin file does not hash itself. Generated replay receipts stay in the selected
output directory; large solver models, private pilot traces and campaign records
are absent from this contribution.
