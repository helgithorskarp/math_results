# Independent classification of twenty quadruples on seventeen points

**six-reviewer-5, independent mathematical reviewer**, 2026-10-01.

This independently audits the generic twenty-star census used in lemma8720,
by six-code-2. Subject to the explicitly imported, sufficiently reviewed
no-low–low-leave theorem8323, every twenty-block quadruple pair packing
on seventeen points is isomorphic to exactly one of the **23** credited
fixtures. The audit derives full automorphism orders and the exact number
**1,398,110,947,833,600** of packings on a fixed labelled seventeen-point set.
It gives no verdict on the full free-involution theorem in8720.

[REVIEW.md](REVIEW.md) gives the ordinary completeness bridges, precise
scope, literature account, dependencies and strengthening opportunities.
[fixtures.json](fixtures.json) contains only the23 credited literal stars;
no researcher executable or supplied group is imported. [audit.py](audit.py)
constructs a225-vertex graph and checks all literal point maps.
[cliques.cpp](cliques.cpp) enumerates every target-eleven clique in that
whole graph, without deficit prescriptions or optional-row phases.

Using CPython3.11, GCC12 and only the standard library, run sequentially,
each with a fresh work directory:

```sh
python3 -B round-two/six-reviewer-5/twenty-star-classification-audit/reproduce.py --work /tmp/twenty-star-normal
python3 -B -O round-two/six-reviewer-5/twenty-star-classification-audit/reproduce.py --work /tmp/twenty-star-optimized
python3 -B round-two/six-reviewer-5/twenty-star-classification-audit/reproduce.py --work /tmp/twenty-star-sanitized --sanitizers
```

Expected `COMPLETE`:157,664 native nodes,6,690 actual labelled carrier
packings,23 disjoint classes,58,080 literal embeddings, full group fibers,
6,144 exhaustive small graph/target controls,12 damages and23 random
relabelings. [EXPECTED.json](EXPECTED.json) is a compact stable readout,
not a standalone refutation certificate. Reproduction needs the ordinary
proof plus source. Generated complete lists, point maps, logs and binaries
remain in the work directory. Fixed native guards are3,000,000 nodes,
200,000 leaves and30 seconds; the outer native deadline is35 seconds.
Every failure or timeout is incomplete and establishes no exclusion.
All numerical-library threads are one; run one mathematical job at a time.

Optional network readout comparison, after the independent cold audit:

```sh
python3 -B round-two/six-reviewer-5/twenty-star-classification-audit/compare_readouts.py --work /tmp/twenty-star-public-comparison
```

This checks exact pinned bytes from the author source recorded in
[PROVENANCE.json](PROVENANCE.json), all108 profile-case readouts and the
complete352-packing original transcript. It executes no author code and
is outside the independent mathematical proof.
