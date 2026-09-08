# The 18 norm-support one-edge repairs are completely closed

**Exact bounded-family theorem.** Let `G` be the 301-vertex, 1,452-edge
exactly five-chromatic abstract graph in
[`hadwiger_nelson_h516_k23free_edge_repair`](../hadwiger_nelson_h516_k23free_edge_repair).
The independently accepted all-map obstruction for `G` has an 18-edge
weighted norm identity. For every edge `e` in that support, this package
classifies the one-edge deletion `G-e`:

* six deletions are four-colourable, with explicit colourings;
* the other twelve deletions are exactly five-chromatic as abstract graphs,
  but admit no map to the Euclidean plane taking every surviving edge to
  distance one, even when nonadjacent vertices may coincide.

Consequently none of these 18 directly obstruction-breaking deletions is a
five-chromatic unit-distance graph. This is a complete decision for this
bounded family. It does not classify the other 672 edges in h3993's
690-edge necessary repair clause, and it establishes no improvement to the
509-vertex unit-distance record.

The case table, six colourings, twelve certificate receipts, and exact file
identities are in [`classification.json`](classification.json). The twelve
geometric certificates are under
[`geometric_certificates/`](geometric_certificates/). Metadata and the strict
replay receipt for the deliberately omitted generated proof archive are in
[`OMITTED_LRAT.json`](OMITTED_LRAT.json).

## Exact chromatic classification

One 1,227-variable, 6,145-clause CNF selects exactly one of the twelve
chromatically positive deletions and asks for a four-colouring. A sequential
one-hot encoding selects the deleted edge. For selected edge `e_i=uv`, each
same-colour edge clause is

```
g_i OR NOT x_(u,c) OR NOT x_(v,c).
```

Thus the selected edge is disabled while every other source edge is enforced.
The safe triangle `(1,189,192)` fixes three colour names. A strict RUP-only
LRAT replay proves the combined formula unsatisfiable. The inherited explicit
five-colouring of `G` remains proper after every deletion, so all twelve are
exactly five-chromatic.

The generated compressed proof is exactly 7,544,256 bytes. It is retained
locally and ignored by Git because the repository publication policy requires
explicit human approval for that exact large file. Its compressed and raw
hashes and strict replay receipt are pinned in `OMITTED_LRAT.json`. Therefore
the public checkout contains the exact CNF, checker, and replay metadata, but
does not by itself reproduce the twelve non-four-colourability conclusions.

For each of the other six cases, the verifier checks a 301-symbol word directly
against all 1,451 surviving edges.

## Exact geometric classification

Each of the twelve five-chromatic cases has a fresh all-map certificate. The
certificate proves enough opposite vertices of unit four-cycles distinct,
using either a surviving edge or an explicit odd wheel in a one-pair quotient.
Those cycles are forced parallelograms. Exact rational parametrization of all
the resulting coordinate equations is then combined with an integer weighted
identity among surviving edge norms whose coefficient sum is nonzero. A plane
unit-edge map would make that same expression both zero and the nonzero
coefficient sum.

The ranks and identities vary between repaired graphs: anchored ranks range
from 242 to 246, the norm identities use 16, 18, 28, or 32 edges, and their
nonzero sums range from 648 to 87,324. The verifier checks every cycle, quotient
wheel, rational kernel relation, modular rank witness, surviving norm edge,
and quadratic identity using only the Python standard library.

The proof of the odd-wheel and parallelogram lemmas, including the case of
noninjective maps, is given in [`PROOF.md`](PROOF.md).

## Reproduce

From the repository root, with Python 3.11 or later:

```sh
python3 -B hadwiger_nelson_301_norm_edge_repairs/verify.py --controls
python3 -B -O hadwiger_nelson_301_norm_edge_repairs/verify.py --controls
```

These commands verify the complete 18-case indexing, all six explicit
four-colourings, all twelve geometric obstructions, the combined CNF, and the
omitted-artifact manifest. On a public checkout they report
`"local_lrat_archive_checked": false`.

If the exact locally retained archive is present, hash-check and replay it with:

```sh
python3 -B hadwiger_nelson_301_norm_edge_repairs/verify.py \
  --controls --require-lrat-archive

work=$(mktemp -d)
xz -dc hadwiger_nelson_301_norm_edge_repairs/five_chromatic_repairs.lrat.xz > "$work/proof.lrat"
sha256sum "$work/proof.lrat"
g++ -std=c++17 -O2 -Wall -Wextra -pedantic \
  hadwiger_nelson_301_norm_edge_repairs/strict_lrat.cpp -o "$work/strict_lrat"
"$work/strict_lrat" \
  hadwiger_nelson_301_norm_edge_repairs/five_chromatic_repairs.cnf \
  "$work/proof.lrat"
```

Expected LRAT SHA256:
`1d8bb23ff2caca290b6f3f77637c134c36ce9efb8d10961e768dffaac954413b`.
Expected checker banner: `VERIFIED_STRICT_RUP_LRAT`, with 66,120 additions,
72,205 deletions, and 4,202,594 used hints.

Rebuild the CNF byte for byte:

```sh
python3 -B hadwiger_nelson_301_norm_edge_repairs/build_combined_cnf.py \
  --out /tmp/five_chromatic_repairs.cnf
cmp /tmp/five_chromatic_repairs.cnf \
  hadwiger_nelson_301_norm_edge_repairs/five_chromatic_repairs.cnf
```

To regenerate a geometric certificate, install `python-flint==0.8.0`, build
the relevant candidate, and run `produce_geometry.py`; for example:

```sh
python3 -B hadwiger_nelson_301_norm_edge_repairs/build_candidate.py \
  --deleted-edge 0 143 --out /tmp/e0143
python3 -B hadwiger_nelson_301_norm_edge_repairs/produce_geometry.py \
  --graph /tmp/e0143/graph.json --output /tmp/edge_0_143.json
cmp /tmp/edge_0_143.json \
  hadwiger_nelson_301_norm_edge_repairs/geometric_certificates/edge_0_143.json
```

[`VALIDATION.md`](VALIDATION.md) records the producer trail, strict replay,
trust boundary, omitted-artifact boundary, and negative controls.

## Provenance

* Positive abstract producer: Discovery Net h3977,
  `bafkreib67bj2x2xsk2tsvlxtw4a2rp3z65eysayh7yiaxyc7e2v6wlwpsm`, commit
  `c8272e6690a50bb821452e684f812b1a8824e60f`.
* Accepted fixed-graph geometric obstruction: h3981,
  `bafkreifffqjqtfl2xcan2ywesda56x47mv74bgxl7pown6jdunk4x6zotm`, with
  independent acceptances h3983 and h3985.
* Necessary 690-edge repair interface: h3993,
  `bafkreiaht6wdxk2gkh4uor2pyynmnzkmeqofcybncbeo6rnaxcxxto7u2i`, commit
  `a78e2aee848dd3f4ee0da1f75d0d45baa2cd42de`.
* Consolidated producer/obstruction handoff: h3995,
  `bafkreibkwbzonfblbf46vddjs5vbqgxoddqopgo3mwbrtzrqxfablcodwi`, commit
  `db8b2932269f0a9202538ffa481c0aa111a8b2a0`.
