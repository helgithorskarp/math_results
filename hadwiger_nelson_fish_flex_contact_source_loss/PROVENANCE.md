# Provenance and novelty boundary

The 23-vertex fish graph is due to Hochberg and O'Donnell:

- R. Hochberg and P. O'Donnell, *Some 4-Chromatic Unit-Distance Graphs without
  Small Cycles*, Geombinatorics 5 (1996), 137--141.

The numerical discovery script follows the flexible parameterization in
Parcly Taxel's open-source Shibuya collection:

- [`hodfish_vertices` in `pegg.py`](https://github.com/Parcly-Taxel/Shibuya/blob/main/shibuya/graphs/pegg.py),
  repository HEAD `218097c9971db2b60ab94a0b8dae20d76741cc43` at retrieval on
  2026-09-15; retrieved file SHA-256
  `2ba335b24fd02294030595d9b0ae055b30b10b4dfc886f183eb27321c0de75c1`.
- [Taxel's construction discussion](https://math.stackexchange.com/questions/3958839/are-4-chromatic-3-connected-unit-distance-graphs-always-rigid), which records
  that the fish is flexible and explicitly motivates watching a nonedge reach
  unit distance during a flex.

The package claims no novelty for the fish, its flexibility, or the general
self-contact idea.  Its new claim is deliberately narrower: the selected
pair `(10,21)` has been isolated at an exact real root, all physical contacts
have been certified, and explicit complete input colour words prove strict
source loss and survival on that same root.

The earlier repository packages
[`hadwiger_nelson_fish_spindle_pair_gate`](../hadwiger_nelson_fish_spindle_pair_gate)
and
[`hadwiger_nelson_fish_selfsum_fourcolour_stop`](../hadwiger_nelson_fish_selfsum_fourcolour_stop)
concern a fixed symmetric fish realization in two different compositions.
Neither varies the internal fish flex or certifies this self-contact event.
