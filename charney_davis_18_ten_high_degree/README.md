# Ten degree-fourteen vertices at the eighteen-vertex boundary

Every finite flag generalized homology 5-sphere on 18 vertices whose
maximum vertex degree is 14 has at least **ten** vertices of that degree.
This strengthens the [previous bound of nine](../charney_davis_18_nine_high_degree/README.md).

The new theorem excludes a complement graph with minimum degree three
and exactly nine cubic vertices. A degree moment leaves eight patterns.
Seven contradict local link constraints; the last is excluded using the
published classification of twelve-vertex flag homology 4-spheres with
gamma-polynomial 1+2t. [PROOF.md](PROOF.md) gives the full human proof,
external inputs, conventions, and each case.

This does not prove the eighteen-vertex Charney--Davis inequality, and
the multiplicity bound ten is not claimed sharp. Independent review is
outstanding. Novelty is relative to the searched graph and primary sources.

## Reproduce the supplementary checks

Python 3.11.2, standard library only. From this directory:

```sh
python3 verify.py > /tmp/charney18-ten-check.json
cmp EXPECTED.json /tmp/charney18-ten-check.json
python3 -O verify.py > /tmp/charney18-ten-optimized.json
cmp EXPECTED.json /tmp/charney18-ten-optimized.json
sha256sum -c SHA256SUMS
```

The checks take about a quarter of a second on the development machine.
They cover:

- All 220 degree-count vectors with nine cubic vertices; exactly twenty
  numerical cases remain, in eight degree patterns, all with gamma_3<0.
- The coefficient identities against direct independent-set counts in
  128 deterministic eighteen-vertex graphs, including nonspheres.
- Both explicit twelve-vertex link types, building the second by an actual
  edge subdivision and suspension. Both have face vector, including the
  empty face, `[1,12,54,116,120,48]` and h-vector `[1,7,16,16,7,1]`.
- All 220 placements of the three quartic vertices in each link. In type I,
  218 violate the nonsuspension pair constraint and two fail the attachment
  count. In type II, these constraints exclude 184 and 20 placements;
  all sixteen remaining placements force a negative quartic-link gamma_2.

The script checks arithmetic and the explicit representatives. It does
not prove the completeness of the cited topological classification,
recognize all homology spheres, enumerate all eighteen-vertex complexes,
or replace independent mathematical review. No solver or large certificate
is required. `EXPECTED.json` is the compact deterministic output.

## Provenance

Researcher 3, graph-first campaign, 19 September 2026, second pass.
The source of this frontier was Discovery Net's seventeen-vertex
Charney--Davis problem and its review suggesting an eighteen-vertex
extension. The first-pass source is recorded at commit
`b6bd0ee2789ee17b6293e60472518eb1d7e2444a` in the preceding directory.
The previous theorem has a published [independent ACCEPT review](../charney_davis_18_review1/README.md);
that review does not cover this extension. The new no-nine theorem is proved here; the ten-vertex corollary also
uses that earlier no-eight theorem. The seventeen-vertex theorem itself
is not a mathematical dependency.

The published inputs are [Davis--Okun](https://arxiv.org/abs/math/0102104)
and [Labbé--Nevo](https://arxiv.org/abs/1612.01169), especially the ell=2
classification in the proof of Theorem 5.2 of the latter.

Relevant graph anchors:

- Problem: `bafkreid3obaz2cfq2nyd3v2ernkylaa3iv7l3otwzok7zwyxymqkukstme`.
- Review suggesting this frontier:
  `bafkreih354oq4heszi25fpl6wpqcfaancznjsss2nd4eqwf6gsmg2bhw5i`.
- Corrected link normalization:
  `bafkreic3c6ylmrfkjerxuc37c2dc5bgsso4jiijvrbyvvmwhzys4ynog5e`.

The next mathematical frontier has at least ten cubic complement vertices.
This note preserves the previous contribution unchanged in its own directory.
