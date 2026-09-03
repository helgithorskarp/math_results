# Independent audit of the Dean-5 periodic split-apex arithmetic

This directory supports a scoped review of Section 11, Appendix A, and
Proposition B.9 of Elias Botsford, *Cycles of length divisible by five in
graphs of minimum degree five*, version 1.0.1
(<https://doi.org/10.5281/zenodo.22182448>).  The associated computational
supplement is <https://doi.org/10.5281/zenodo.22167084>.

`audit_periodic.py` is a clean-room standard-library implementation.  It does
not import the supplement.  It checks:

- the exact tight-pair and bad-root tables from their displayed definitions;
- the published Appendix B.9 row counts (115,173 and 2,846);
- the periodic formulas through odd order 501, well beyond the
  distributed order-119 cutoff;
- the pairwise-compatible tight-support shapes used in (A.13);
- connectivity of every tested bad-root graph `Gamma_d` in the stated ranges;
- the special distance-five and distance-seven tables; and
- the split-side exceptional congruence and its remote-root elimination.

Run with Python 3.11 or later:

```bash
python3 audit_periodic.py
```

Expected output:

```text
Appendix B.9 published-range row counts: tight=115173, module=2846
Exact table formulas through d=501: tight=8458569, module=50390: OK
Derived support shapes through d=201: OK
Bad-root graph connectivity through d=501: OK
Distance-five and distance-seven tables: OK
Split-side and remote-root arithmetic through d=501: OK
```

The finite run is evidence for the arithmetic layer, not a proof of the graph
theorem.  The accompanying review separately audits the map from a hypothetical
split-apex counterexample to these states: shortest-path normalization,
off-cycle attachment bounds, rooted-path degree conditions, module simplicity,
block-tree concentration, long congruence classes, the two exceptional short
distances, and lifting back to the Type-II graph.  It relies on the published
Chiba--Ota--Yamashita admissible-path theorem and standard connectivity facts.
