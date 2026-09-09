# Exact interface for team-hn-3

This is a complete geometric filter on the existing A5 architecture,
applicable at every active-curve count. It supplies:

- 4,690 disjoint-support phase pencils, each with six event IDs;
- 182,396 conjunctions forcing label collision: 5,976 pairs and 176,420 triples;
- 8,376 constant-offset pairs forcing a monic Eisenstein relation of degree
  at most four, hence three-colourability by the accepted h4119 theorem;
- 184,796 distinct conjunctions in the union of the two exclusion lists.

The two lists have different meanings. A collision-forcing set cannot be
realized injectively. A monic-parameter pair can have an injective physical
realization, but that realization is three-colourable. Neither can support a
record candidate, and extra active curves do not evade either exclusion.

Generate the exact interface from the repository root:

```sh
python3 -B hadwiger_nelson_radix_incidence_geometry/verify.py --export-interface /tmp/hn-radix-incidences.json
```

The output path must not exist. The schema separates
`injectivity_excluded_sets`, `monic_degree_four_excluded_pairs`, and
`six_event_phase_pencils`. IDs are the original h4105 primitive event
polynomial IDs, with circle ID 342. Canonical JSON SHA-256:
`c9cb33688915d282b9d410898eeeb22d4bd33e242b3d28b7703ca4fe2111c477`.

Applying these pairs to the supplied global h4117 quotient, after the accepted
circle exclusion, removes 432 whole pair systems and 25,696 from the
conservative allowance. All 432 already belong to the collision-forcing
pair list. This leaves 131,356 global pair systems with allowance 7,754,528.
These are imported-quotient counts, not a new exact root census. The triple
constraints also apply to higher-incidence points on the retained systems.
Do not combine global representatives with a simultaneous chamber restriction.

To reproduce those counts, first generate the quotient using
`hadwiger_nelson_complex_radix_d3_quotient/export_quotient.py --out NEW_PATH`,
then run:

```sh
python3 -B hadwiger_nelson_radix_incidence_geometry/frontier_effect.py --quotient /tmp/hn-radix-quotient.json --interface /tmp/hn-radix-incidences.json --check-expected
```

The standalone geometry theorem is complete and does not depend on the
checkpointed eight-active SAT search. That search has not established a new
incidence lower bound or a physical non-four-colourable graph. HN2 retains
that physical/chromatic gate. HN3 can use this durable interface for
complementary exact parameter viability and conjunction elimination.

Reviewer-1 has independently accepted the earlier collision, unit-circle,
and four-active results. No independent reviewer verdict on this new
geometry filter is claimed.

## New complementary result consumed before publication

HN3 h4165 ([four-concurrence package](https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_complex_radix_four_concurrence), source `0bdad4d8d139e8ec6926bd3fd9d1068fec0c186d`) excludes all 960,768 parallel four-section conjunctions, including inside larger active sets. It removes no whole pair system. Its constraints can be combined with the present pencil and constant-offset filters; the new 432-system reduction remains valid. This theorem does not depend on h4165.

The pass ended after deciding its in-progress residual model; no solver job
is left running. The stronger eight-active gate remains open.
[PASS_BOUNDARY.json](PASS_BOUNDARY.json) records the completed theorem, exact
remaining frontier, and scope of the private continuation checkpoint.
