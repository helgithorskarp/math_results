# Every 214-gadget anchor at the fixed inner origin is four-colorable

Let `A` and `V` be the archived Parts 159- and 214-vertex gadgets, and fix

```
t = (5+i sqrt(11))/6
B = A union tA.
```

**For every Euclidean isometry `g` such that `0` belongs to `g(V)`, the
strict unit-distance graph on `B union g(V)` is four-colorable.** Its order
is at most 505. This allows any of the 214 vertices of `V` to be attached
to the fixed origin of `B`, at every angle and in either orientation.

The theorem strengthens the prior
[single-anchor exclusion](../hadwiger_nelson_mixed505_anchor0/README.md).
It keeps the inner union and its attachment point fixed. Attachments at
other vertices of `B`, disjoint placements, and other inner unions remain
open. No five-chromatic graph or record improvement is produced.

The [proof](PROOF.md) classifies the distinct vectors in `V-V` once, then
projects each complete quadratic cross-edge class to every anchor that
uses it. All 4,163,154 anchor/class cases have explicit four-colorings from
the same five component rows used in the single-anchor result. No new
coloring or SAT solve was needed.

| Exact quantity | Value |
|---|---:|
| Vertices / strict edges of `B` | 292 / 1,251 |
| Vertices / strict edges of `V` | 214 / 977 |
| Nonzero ordered differences before deduplication | 45,582 |
| Distinct nonzero displacement vectors | 4,418 |
| Nonzero `B`-vertex / displacement pairs | 1,285,638 |
| Outside-field ambient quadratic classes | 140,110 |
| Distinct outside-field unit multipliers in the ambient census | 280,220 |
| Anchor/class cases with at least one new cross edge | 4,163,154 |
| Maximum new cross edges outside the base field | 26 |
| Uncovered anchor/class cases | 0 |

## Reproduce

From this directory in a complete repository checkout, with Python 3.11 or
later and only the standard library:

```bash
python3 verify.py --anchors /tmp/mixed505-anchors.tsv > /tmp/mixed505-all.json
cmp expected.json /tmp/mixed505-all.json
python3 audit.py > /tmp/mixed505-all-audit.json
cmp expected_audit.json /tmp/mixed505-all-audit.json
python3 check_example.py > /tmp/mixed505-all-example.json
cmp expected_example.json /tmp/mixed505-all-example.json
sha256sum -c SHA256SUMS
```

On the producing host, CPython 3.11.2 took 19.8 seconds for the integer
verifier (125 MiB peak RSS), 356.3 seconds for the rational audit
(223 MiB), and 3.4 seconds for the direct examples (17 MiB).

The optional TSV lists every anchor's count and cross-edge histogram; its
hash is in `expected.json`. The same complete per-anchor data is committed
in compact JSON form in `screen.json`. That file is a summary, not a dump
of individual placements.

`verify.py` uses arbitrary-precision integer geometry, exact square tests,
and primitive rational projective keys. It checks the component colorings,
projects every complete class, intersects finite coloring-permutation
masks, and directly checks the selected coloring against every projected
cross edge. It invokes no external package or solver.

`audit.py` imports the prior rational monic-quadratic implementation,
reconstructs the displacement set independently, and replays all 1,285,638
pair classifications and all 4,163,154 anchor/class colorings. It uses
explicit color-permutation searches rather than the integer verifier's
masks. It matches the complete classification, ambient edge partition,
chosen-witness stream, and per-anchor counts and histograms.

`check_example.py` uses the separate integer radical arithmetic from the
prior direct-coordinate checker. It reconstructs both roots of an explicit
26-contact class at source anchor 10. Each graph has 505 distinct vertices
and 2,254 strict unit edges. All 127,260 vertex pairs and an actual proper
coloring are checked for each root.

## Evidence, dependencies, and scope

The 1,309 bytes of positive coloring data are reused from
`../hadwiger_nelson_nonmono159_moser_triple/colors_B.txt` and
`../hadwiger_nelson_mixed505_anchor0/colors_H.txt`. The latter rows also
color the untranslated `V`, since translation preserves its internal
edges. Each anchor color is normalized to zero before gluing.

The small coordinate tables and their
[provenance](../hadwiger_nelson_nonmono159_214_lowden2/SOURCE.md) are reused
from the earlier mixed-gadget package. The in-field branch imports the
[four-coloring theorem for the restricted complex field](../hadwiger_nelson_nonmono_field_obstruction/PROOF.md)
`E=Q(i sqrt(3),i sqrt(11))`. Imported source and input files are hash-pinned.

The continuous-to-finite argument remains ordinary unformalized algebra.
The finite evidence trusts exact Python arithmetic, the published programs
and inputs, and ordinary execution. The checks use different arithmetic
and grouping methods, but are author cross-checks, not an independent peer
review of this new result. There are no approximate unit-distance tests,
UNSAT assumptions, or unavailable large input certificates.

The complete ambient edge-partition SHA-256 is
`e8d2ebb6b59d8702c47c590e189c06d21f5facadef9ca09b9b40b999e2431659`.
