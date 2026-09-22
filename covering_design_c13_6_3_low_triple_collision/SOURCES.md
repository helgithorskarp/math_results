# Sources and provenance

## Current parameter status

- Daniel M. Gordon, *La Jolla Coverings Repository*, version 1.2, Zenodo,
  2026, DOI [10.5281/zenodo.19735294](https://doi.org/10.5281/zenodo.19735294).
  The current dataset records `20 <= C(13,6,3) <= 21` and supplies a
  21-block covering.
- Daniel M. Gordon, Gregory Kuperberg, and Oren Patashnik,
  [*New constructions for covering designs*](https://arxiv.org/abs/math/9502238),
  Journal of Combinatorial Designs 3 (1995), 269–284.  This is background for
  covering-design definitions, bounds, and constructions.

## Imported graph result

The sole non-elementary input specific to the conditional profile is the
completed theorem that no three through-`h` residues share a low triple:

```text
bafkreiemdszyae62ido42owb745sx3mikydgjjlew434oov2df27ywtelq
```

Its public reproducible source is split across the preceding packages:

- [orbit-51 exclusion](../covering_design_c13_6_3_orbit51_exclusion/)
- [orbit-52 exclusion](../covering_design_c13_6_3_orbit52_exclusion/)

Those packages also document the classified optimal-link consequences used
to obtain row and column sums for the exceptional profile.

## Scope of the source check

The Zenodo record and current repository were refreshed on 2026-09-22.  A
bounded graph inspection found no matching maximum-intersection collision
table.  This supports describing the theorem as new to the searched graph
and sources, not as a claim of broad historical priority.

All remaining inputs in `PROOF.md` are elementary identities proved there.
The audit uses only exact Python integers and the standard library.

