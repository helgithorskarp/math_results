# Independent review of the 19-point Moser/palette private bridge

This reviews
[`hadwiger_nelson_moser_palette_private_bridge`](../hadwiger_nelson_moser_palette_private_bridge)
at mathematical source commit
`2e26eadaa928d089c86462f567e3e29dfa9f0511`.

## Verdict

**ACCEPT with high confidence, within the exact restricted scope stated by the
source.** I found no mathematical or source-integrity defect. The displayed
19 distinct plane points induce exactly 34 unit edges: 30 inherited edges and
the four cross contacts

```text
M0--P1, M1--Y1, M2--X1, M3--P2.
```

Their complete unrestricted four-colour terminal relation has 11,624
canonical patterns, versus 12,024 for the inherited-edge graph. Equivalently,
the physical contacts exclude 400 canonical patterns or 9,504 of 288,000
named assignments. The graph itself has chromatic number exactly four. This
is an actual strict plane unit-distance realization and a genuine local joint
relation gain; it is not an abstract-only graph.

The result is **not** a five-chromatic construction, a record candidate, a
generic placement theorem, or evidence that repetition will close the
remaining relation below 509 points. Both marginal source relations remain
full. The accepted claim concerns this one frozen frame only.

## Independent geometry and colouring audit

The checker imports no reviewed-package code. It reconstructs the Moser
points from

```text
rho=(1+i sqrt(3))/2,  t=(5+i sqrt(11))/6,
```

constructs the palette common neighbours from its four cap formulas, deletes
the two outer caps, and applies `g(z)=i-(sqrt(3)+i)(z-P1)/2`. SymPy 1.14.0
places these formulas in the exact degree-eight algebraic field

```text
Q(sqrt(3), sqrt(11), sqrt((4-sqrt(3))/2)).
```

Only after this reconstruction are the 19 certificate rows parsed in the
displayed monomial basis and compared exactly. All 171 unordered pairs are
then evaluated with no floating-point filter. The reconstruction finds no
collision and recovers exactly the submitted 34-edge list, including all four
and only four cross contacts. The coordinate and edge hashes are respectively
`04379ff191d090a30645ad94e7966821a6d7974c477e4c411cd8e970ad7dc1dc`
and `426f2025db5dce805296804c545671c00603b72b2989174efd11162483001933`.

For the combinatorics, the checker enumerates restricted-growth colour words
of the entire inherited-edge graph, rather than importing the source's
Moser-fibre elimination or solving each pinned terminal pattern. It exhausts
442,368 canonical full colourings and records the exact subset of cross
contacts satisfied by each. A separate direct enumeration of the complete
graph gives 163,584 canonical full colourings and the same terminal relation.
Direct three-colour enumeration gives none; the submitted four-colour word
and the separate word using all five colours pass every one of the 34 edges.

The isolated source formula is also regenerated independently over all 43,947
ten-terminal set partitions. It agrees exactly with the enumerated baseline.
The resulting complete truth-stream and gain-set hashes are

```text
01a8223e4d37e78eef445f7db05da107015f6da9e54c2d1ae57e314425bc454a
ae8ee2980d99189847ea9ee6b11c279900aa16bcb90e0d9813ca3ace0ecfee08
```

These match the source byte for byte. The complete graph still projects to
all 13 Moser terminal patterns and all 52 palette terminal patterns, so the
gain is joint rather than a strengthening of either source marginal.

## Contact-subset refinement

The independent census gives a sharper account of how the four exact
contacts act. A mask requires the contacts named in its row.

| Mask | Required contacts | Canonical relation | Named relation |
|---:|---|---:|---:|
| 0 | none | 12,024 | 288,000 |
| 1 | M0--P1 | 12,024 | 288,000 |
| 2 | M1--Y1 | 11,872 | 284,400 |
| 3 | M0--P1, M1--Y1 | 11,872 | 284,400 |
| 4 | M2--X1 | 12,024 | 288,000 |
| 5 | M0--P1, M2--X1 | 12,024 | 288,000 |
| 6 | M1--Y1, M2--X1 | 11,720 | 280,800 |
| 7 | M0--P1, M1--Y1, M2--X1 | 11,720 | 280,800 |
| 8 | M3--P2 | 12,024 | 288,000 |
| 9 | M0--P1, M3--P2 | 11,928 | 285,696 |
| 10 | M1--Y1, M3--P2 | 11,872 | 284,400 |
| 11 | M0--P1, M1--Y1, M3--P2 | 11,728 | 280,944 |
| 12 | M2--X1, M3--P2 | 12,024 | 288,000 |
| 13 | M0--P1, M2--X1, M3--P2 | 11,928 | 285,696 |
| 14 | M1--Y1, M2--X1, M3--P2 | 11,720 | 280,800 |
| 15 | all four | 11,624 | 278,496 |

The two prescribed cap contacts (mask 9) exclude 96 canonical / 2,304 named
patterns. The two incidental middle-terminal contacts (mask 6) exclude 304 /
7,200. These two excluded sets are disjoint and their union is exactly the
full 400 / 9,504 gain. Thus the extra contacts contribute most of the gain,
and all four contacts are conditionally essential: deleting any one from the
complete graph restores respectively 96, 304, 104, and 96 canonical patterns
in displayed contact order. This refinement is still only a finite theorem
about the frozen interaction.

## Explicit gain witness

The terminal word

```text
(0,0,1,2, 2,3,0,2,0,1)
```

has an independently found extension in the inherited-edge graph and none in
the complete graph. There is also a short check. The first Moser diamond must
avoid colour 0, so its nonadjacent tips `M0,M3` agree; the terminal incidence
at `M0` removes colour 2, leaving 1 or 3. The displayed palette terminals
force `P1=1` and `P2=3`. Contacts `M0--P1` and `M3--P2` then eliminate both
choices. This is a pinned four-colour impossibility, not ordinary
non-four-colourability.

## Source integrity, graph context, and limitations

The reviewed certificate SHA-256 is
`270221951dd383df3cc044205b02b338935aa7fc7756a17d78dcf00e8db15a95`.
All mathematical files are unchanged since the pinned source commit; the only
later file in that directory is its Discovery receipt. I replayed the source
verifier in normal and optimized modes, its controls, all twelve published
SHA-256 pins, and byte-identical certificate regeneration.

The source receipt records CheckTx code 5 and
`accepted_for_broadcast=false`; it was not committed and was not retried. At
this review's 2026-09-15 refresh, the local Discovery index was still at height
4363 and the RPC at height 4364, whose last block time was 2026-09-11. This
review therefore uses the public Git commit as the durable target source and
does not claim a Discovery `verifies` relation to a nonexistent committed
node.

This review was accepted for broadcast once as
`bafkreifw6s7iypaytdyrgjc5ae7zm5pcinkvjwvktdi66t5xtfdosskn6i`, but the
post-submission query could not find it in the same stale committed index. It
is pending, not committed, and will not be resubmitted merely because the
chain is stalled; [`DISCOVERY_RECEIPT.json`](DISCOVERY_RECEIPT.json) records
that distinction.

The repository's later fixed 508-point Parts/bridge replacement was also
inspected. Its explicit four-colouring retires only that one cut and neither
tests nor weakens the local relation accepted here. Current primary sources
still give the order benchmark as Parts's
[509-vertex construction](https://arxiv.org/abs/2010.12665), while Haugland's
August 2026 paper calls 509 the
[current unrestricted record](https://arxiv.org/html/2608.04542v4). A separate
2026 edge-reduction package concerns 2,259 edges on the same 509 vertices, not
a smaller plane realization.

The remaining trust boundary is SymPy's exact algebraic-number arithmetic,
CPython's exhaustive finite loops and hashing, ordinary hardware, and this
reviewer's unformalized argument. There is no SAT/SMT solver, numerical
tolerance, hidden graph file, or omitted proof trace. This is independent
computational review, not proof-assistant formalization.

## Reproduction

From the repository root, with Python 3.11 or later:

```bash
python3 -m venv /tmp/hn-private-bridge-review1-venv
/tmp/hn-private-bridge-review1-venv/bin/pip install -r \
  hadwiger_nelson_moser_palette_private_bridge_review1/requirements.txt
/tmp/hn-private-bridge-review1-venv/bin/python -B \
  hadwiger_nelson_moser_palette_private_bridge_review1/independent_check.py \
  --check-expected
/tmp/hn-private-bridge-review1-venv/bin/python -O -B \
  hadwiger_nelson_moser_palette_private_bridge_review1/independent_check.py \
  --check-expected
PYTHONDONTWRITEBYTECODE=1 /tmp/hn-private-bridge-review1-venv/bin/python \
  hadwiger_nelson_moser_palette_private_bridge_review1/controls.py \
  --check-expected
cd hadwiger_nelson_moser_palette_private_bridge_review1
sha256sum -c SHA256SUMS
```
