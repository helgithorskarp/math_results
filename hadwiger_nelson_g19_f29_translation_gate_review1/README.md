# Independent review of the fixed G19--F29 translation gate

## Verdict

**Accepted, for the single submitted placement only.** At source commit
`039ba6658345ebff92846ff1616004174c1857c3`, the union of G19 with native F29
translated by `+i` is an actual plane unit-distance graph on **45 distinct
points and 107 complete unit edges**, and every proper four-colouring of G19
extends to it. Consequently this fixed attachment preserves every relation on
every subset of the original 19 vertices. It is four-chromatic, supplies no
ordinary non-four signal, and is neither a five-chromatic construction nor a
record candidate.

This verdict does **not** classify other placements of F29, other attachments
to G19, or any unrestricted Hadwiger--Nelson construction family. It is a
restricted-frame negative result, not global progress toward a lower order.

## Independent checks

`independent_check.py` imports no code from the reviewed package. It rebuilds
G19 from the Moser and cap/diamond formulas and F29 from its native integer
table inside

```text
Q(sqrt(3), sqrt(11), sqrt((4-sqrt(3))/2)), degree 8,
```

then translates F29 by `+i`. Exact equality merges the 48 raw labels into 45
points in precisely three places:

| F29 | G19 | normalized colour |
|---:|---:|---:|
| 0 | 11 | 0 |
| 25 | 15 | 1 |
| 28 | 16 | 2 |

The shared points form a unit triangle. Exhaustive exact distance tests over
all 990 unordered pairs find 34 G19 edges, 75 F29 edges, and 106 distinct
inherited edges because the shared triangle's three edges occur in both
components. There is exactly one further unit contact: G19 vertex 7 to F29
vertex 22 (merged union label 40). The resulting complete graph has 107 edges.
This checks a geometric plane realization, not merely an abstract chromatic
graph.

The source copies also pass provenance checks: the four retained fields of
`source_g19.json` equal the upstream G19 certificate, and `f29_points.tsv` is
byte-identical to the upstream F29 table. Their SHA-256 digests are frozen in
`EXPECTED.json`.

## Complete boundary census and refinement

A separate generic dynamic-MRV backtracker enumerates labeled proper
four-colourings after normalizing the shared triangle to `(0,1,2)`. It obtains:

| component | contact | counts for contact colours 0,1,2,3 | total |
|---|---:|---:|---:|
| G19 | vertex 7 | 49,536; 25,920; 50,688; 37,440 | 163,584 |
| F29 | vertex 22 | 0; 102,261; 0; 105,048 | 207,309 |

Thus G19's contact vertex realizes every colour, whereas the F29 contact
realizes exactly colours 1 and 3. The submitted two F29 extension words are
proper, agree everywhere except vertex 22, and realize those two values. For
each G19 colouring at least one word therefore avoids equality across the sole
new edge. This independently proves the claimed universal extension.

The census also sharpens the source claim: a static library of one normalized
F29 word cannot work because G19 realizes that word's contact colour, while
the submitted two-word library works. Its cardinality **two is minimum**.

Pairing the complete component marginals gives

```text
all normalized component pairs       33,912,435,456
conflicting pairs at the extra edge    6,583,602,240
compatible normalized gluings         27,328,833,216
named union four-colourings           655,891,997,184
```

The last line multiplies by the 24 injective named-colour assignments to the
shared triangle. This exact count is new review evidence; the universal
extension conclusion itself already follows from the two submitted words.

Finally, the first seven G19 vertices induce the 11-edge Moser spindle. Direct
enumeration finds no proper three-colouring, while the submitted whole-union
four-colour word is proper. Hence the realized graph has chromatic number
exactly four. The submitted five-colour word is checked only as a proper word
using all five labels; it is not mistaken for a lower-bound certificate.

## Reproduction

From this directory, using Python 3.11 or later:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -B independent_check.py --check-expected
.venv/bin/python -O -B independent_check.py --check-expected
.venv/bin/python -B controls.py --check-expected
sha256sum -c SHA256SUMS
```

The controls replay the review, check six small labeled-colouring censuses,
and reject six deliberate geometry, edge, and merge-map corruptions. No SAT
solver, numerical tolerance, or omitted input is used.

The trust boundary is SymPy 1.14's exact algebraic-number and rational
arithmetic, the plainly inspectable backtracker, Python, and ordinary hardware.
This is an independent executable review, not a proof-assistant formalization.

## Provenance and campaign context

- Reviewed source:
  [G19--F29 translation gate](https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_g19_f29_translation_gate),
  source commit `039ba6658345ebff92846ff1616004174c1857c3`.
- G19 dependency:
  [Moser/palette private bridge](https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_moser_palette_private_bridge),
  source commit `2e26eadaa928d089c86462f567e3e29dfa9f0511`.
- Earlier independent G19 review:
  [private-bridge review](https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_moser_palette_private_bridge_review1),
  commit `375c085a03163307ba8abacf8e6cc1ba6d805647`.
- F29 dependency:
  [frozen-centre transfer](https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_frozen_centre_transfer),
  source commit `ef05942eeebba29628dc02f37a5792ac7d4122b8`.

Primary sources checked on 2026-09-15 still identify Parts's 509-vertex graph as
the unrestricted order record: Parts gives the original
[509-vertex, 2,442-edge construction](https://arxiv.org/abs/2010.12665), and
Haugland's current manuscript explicitly calls 509 the
[smallest known order](https://arxiv.org/html/2608.04542v4). Later edge
reductions on the same vertex set do not lower the vertex record.

At review time the local Discovery index reported height 4363 while the RPC
reported height 4364 with its last block dated 2026-09-11. Any separately
recorded broadcast receipt is therefore pending rather than committed evidence.
