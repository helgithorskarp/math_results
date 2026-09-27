# One completely signed Gaussian rational-frontier cell

This package certifies full Gaussian majorisation at variance one for every
point of an explicit 42-coordinate parameter box. Sources lie within
coordinate distance 1/256 of (0,+/-e1,+/-e2,+/-e3); every target lies in
[-1/16,1/16]^3; the weights are (24,22,22,22,22,22,22)/156.

After separate anchoring of source and target label 0, the lattice slice
belongs to R3's existing strict rational frontier R^c_1. The literal slice
x_0=y_0=0 is a 36-coordinate box in that gauge. The cell contains injective
paired-rank-six maps. The exact adverse
hinge bound is below -1/200 on the entire interval [1/256,11/16]. Analytic
signs cover both complementary threshold ranges, including zero. This is
parameter-box and threshold coverage, not a finite sample of configurations.

- [Proof and precise scope](PROOF.md)
- [Cell and explicit rank-six member](CELL.json)
- [Exact replay](verify.py) and [expected record](EXPECTED.json)
- [Dependencies, attribution and review boundary](SOURCES.md)

From this directory, with standard-library Python 3.11 or later:

```sh
python3 -B verify.py
python3 -B -O verify.py
sha256sum -c SHA256SUMS
```

Expected status: `GAP_FREE_FRONTIER_CELL_PASS`. Runtime is about two seconds
on one CPU. The symmetric reference grid has 11,390,625 points, reconstructed
from 246,905 representatives with exact multiplicities. No large certificate
is omitted. The actual cell is asymmetric and includes all its permitted
coordinate perturbations.

**Author proof; independent review pending.** Qualitative stability around
point-target comparisons was already known in the campaign. This supplies
explicit finite radii and a uniform, replayable middle margin. It is not a
new abstract stability theorem, a full-frontier cover, an all-variance class,
or a new Kneser--Poulsen consequence. Full R3 Gaussian majorisation remains
open. The seven-factor beta obligation is closed and is not extended here.
