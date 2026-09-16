# Independent review: the generated-anchor golden network is three-chromatic

## Verdict

`ACCEPT_AND_STRENGTHEN_GOLDEN_NETWORK_TO_EXACT_THREE_CHROMATIC`.

The frozen generated-anchor construction at mathematical commit
`3beda50683c9d24e033e30e4b35e9d0d5927f0d7` is independently confirmed to
be an actual strict plane unit-distance graph on **462 distinct points and
1,532 complete unit edges**. Its submitted four-word is valid, so the
author-side stopping conclusion is sound.

The graph is in fact **exactly three-chromatic**. If a stored point is

```text
q*(a0 + a1*zeta + a2*zeta^2 + a3*zeta^3),
```

then

```text
colour = a1 + 2*a2 + a3 mod 3
```

properly colours all 1,532 unit edges. The source labels
`6-3-1-2-5-6` form an exact unit five-cycle, proving that two colours do not
suffice. The resulting three-word has SHA-256

```text
3d554880750584f595f70c72c1b76a26d5f64dd7b373973e61645741fae0987a
```

## Module obstruction

The coloring is structural, not special to these 462 points. Let

```text
Z_(3) = {m/n in Q : 3 does not divide n},
zeta  = exp(2*pi*i/5),
q     = 1/abs(1-zeta).
```

The complete strict unit-distance graph on

```text
q * Z_(3)[zeta]
```

has chromatic number exactly three under the same coefficient-residue map.
Thus no finite unit-distance graph whose points all remain in this module can
be four- or five-chromatic. This includes both the generated-anchor network
and the earlier 1,386-point registered fixed-base reciprocal overlay. The
review independently reconstructs that overlay and sharpens its published
four-colourability conclusion to exact three-chromaticity.

This is a module obstruction, not a coloring of the whole plane. Points with
coefficients nonintegral at 3, other coordinate fields, and operations that
leave the module are outside the theorem. No historical-priority claim is
made for the residue coloring.

## Independent construction audit

[`independent_check.py`](independent_check.py) imports no target executable.
For the finite network it uses the explicit integer matrix for multiplication
by `-zeta-zeta^3` and a direct Gram form, rather than either target field
implementation. It reconstructs:

- the 16-point source and its complete 28 unit and 28 golden pairs;
- all 162 whole reciprocal-scale copies and their 448-point address box;
- the two base/grid coincidences and final 462-point quotient;
- all 161 generated-anchor parent faces and the terminal unique corner;
- all 106,491 pair distances and the complete 1,532-edge stream;
- the 1,386-point registered overlay and the 406 network points outside it.

The point and edge files are reproduced byte-for-byte. The full graph is
connected, has no articulation or bridge, and has a 428-vertex four-core and
332-vertex five-core. Those density facts do not prevent the global residue
three-coloring.

## Reproduce

From the repository root with CPython 3.11 or later and only the standard
library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  hadwiger_nelson_golden_generated_anchor_box_stop_review1/independent_check.py \
  --check-expected

PYTHONDONTWRITEBYTECODE=1 python3 -O \
  hadwiger_nelson_golden_generated_anchor_box_stop_review1/independent_check.py \
  --check-expected

PYTHONDONTWRITEBYTECODE=1 python3 \
  hadwiger_nelson_golden_generated_anchor_box_stop_review1/controls.py

cd hadwiger_nelson_golden_generated_anchor_box_stop_review1
sha256sum -c SHA256SUMS
```

The independent check takes about eighteen seconds on the review host. The
controls compare the Gram norm with direct cyclotomic multiplication on 625
small rows, check all 64 basis associativity triples, exercise the residue and
graph reductions, and reject nine semantic certificate corruptions.

See [PROOF.md](PROOF.md) for the module theorem and finite reconstruction,
[REVIEW.md](REVIEW.md) for the exact verdict and limitations, and
[PROVENANCE.md](PROVENANCE.md) for source integrity and trust boundaries.
