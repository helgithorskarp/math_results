# Reusable exact incidence exclusions for A5(z)

For the complete five-digit complex-radix architecture, this package checks
all 4,690 six-phase pencils arising from disjoint digit supports. Their
geometric rules exclude 182,396 event conjunctions from every injective
realization. A complementary constant-offset argument excludes 8,376 pairs
from every non-four-colourable member. Together they give 184,796 distinct
necessary exclusions, valid at all higher incidences.

This is a quantified architecture obstruction. It does not close the
eight-active search or establish a graph improving the 509-vertex record.
The [proof](PROOF.md) distinguishes physical collision from monic-parameter
three-colourability; both exclude a candidate counterexample for different
reasons.

From the repository root, with standard-library CPython 3.11.2:

```sh
python3 -B hadwiger_nelson_radix_incidence_geometry/verify.py
python3 -O -B hadwiger_nelson_radix_incidence_geometry/verify.py
python3 -O -B hadwiger_nelson_radix_incidence_geometry/controls.py
python3 -B hadwiger_nelson_radix_incidence_geometry/produce.py --out /tmp/hn-incidence-certificate.json --export-interface /tmp/hn-incidence-interface.json
python3 -B hadwiger_nelson_radix_incidence_geometry/verify.py --certificate /tmp/hn-incidence-certificate.json
```

Generation paths must not exist. The checker can independently export the
same interface with `--export-interface NEW_PATH`. It imports the existing
h4151 direct pair/norm inventory; the producer imports the h4105 geometry
module. They use different pencil enumeration and tail-normalization
algorithms and agree on every exported set, not just aggregate counts.

The compact expected certificate is [certificate.json](certificate.json).
The 3,093,550-byte raw interface is kept outside the repository and
regenerated from source. It contains original h4105 curve IDs, all pencil
six-sets, collision-forcing conjunctions, and monic-parameter pairs.
No solver or computer algebra package is required to reproduce this result.

The [frontier effect](FRONTIER_EFFECT.json) removes 432 whole global pair
systems and 25,696 from the conservative allowance, leaving 131,356 systems
and allowance 7,754,528. The [handoff](HANDOFF.md) gives the exact interface
and commands; [dependencies](DEPENDENCIES.md) and [validation](VALIDATION.json)
record the imported results and reproducibility boundary.
