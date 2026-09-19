# Eleven high-degree vertices: excluding the ten-cubic complement

**No flag generalized homology 5-sphere has one-skeleton complement of
degree sequence `3^10 4^8`.** Together with the preceding reductions, this
implies that an eighteen-vertex sphere whose one-skeleton has maximum
degree fourteen has at least **eleven** vertices attaining that degree.

The [proof](PROOF.md) excludes the whole remaining ten-cubic profile,
including all three previously named ten-edge cubic graphs. The full
eighteen-vertex Charney--Davis problem remains unresolved: this note does
not settle profiles with eleven or more cubic complement vertices.
Independent review is outstanding.

The new mechanism is a local suspension-compatibility lemma. If a quartic
complement vertex has two cubic neighbors, its suspension link forces
those neighbors to be endpoints of a three-edge path in the cubic
subgraph, with both internal vertices of degree two. The internal vertices'
unique quartic neighbors are also forced. This rules out all components
containing a degree-three vertex. Cycle and path arguments then exhaust
the maximum-degree-two case.

## Dependencies and scope

The [premise ledger](PREMISES.md) distinguishes external topology,
preceding campaign lemmas, and the new graph-local argument. The proof
uses the structural part of the
[two-triangle note](../charney_davis_18_two_triangles/README.md); its `T<=2`
inequality is not needed. Only the eleven-vertex corollary additionally
uses the [ten-high-degree theorem](../charney_davis_18_ten_high_degree/README.md)
and [ten-cubic profile reduction](../charney_davis_18_ten_cubic_rigidity/README.md).
The earlier independent review covers the nine-high-degree result alone.

This is a human combinatorial proof with supplementary exact checks.
There is no sphere census, search through quartic attachments, solver
certificate, or proof-assistant formalization. Publication and successful
checks do not replace independent scrutiny of the written proof or its
dependencies.

## Reproduction

Python 3.11.2 was used, with only the standard library. From this directory:

```sh
python3 verify.py > /tmp/charney18-eleven.json
diff -u EXPECTED.json /tmp/charney18-eleven.json
python3 -O verify.py > /tmp/charney18-eleven-optimized.json
diff -u EXPECTED.json /tmp/charney18-eleven-optimized.json
sha256sum -c SHA256SUMS
```

The checker runs in under one second on the publication host. It audits:

- all 100 local suspension-pair patterns, with four surviving orientations
  of the proved cubic-path configuration;
- 282 rooted component models, covering 471 possible middle edges with
  degree-two endpoints, with no compatible quartic pair;
- paths on one through ten vertices, cycles on five through ten vertices,
  and the exact quartic-incidence identities.

The local pattern check uses necessary inequalities on a seven-vertex
induced configuration, rather than assuming that configuration is already
a sphere. The rooted and path/cycle checks corroborate the universal
arguments in PROOF.md. All checks remain enabled under `python -O`.
`EXPECTED.json` and `SHA256SUMS` give compact expected output and integrity
checks; no external data are required.

Primary literature and relevant graph feedback were refreshed on
19 September 2026. No exact competing exclusion was found in the searched
sources. Novelty is search-relative, not a claim of global priority.
