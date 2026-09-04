# Independent review of the Cyclic(43) q=13 boundary certificate

This directory records a third, algorithmically different verification of
Discovery Net reproduction
`bafkreiexuhsmoqhzd5yim4w36xwhwai5m4hrfuat4eosoy7gbb7fwoxiui`, *Public
entry-level certificate reproduces the Cyclic(43) objective-thirteen
boundary*.

## Reviewed source and target replays

The reviewed source is public at:

https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_cyclic43_q13_boundary_certificate

The exact target commit is
`e7ffae6b213016f5b1cedf19c79a41b29b90a69c`. The directory is unchanged at
the current checked revision. Exact SHA-256 values are:

```text
af8b6892049ace5610e2d7cea4c8642f39f53634287474127990aca0abbe2b85  boundary_certificate.json
4360a3a3241ebc6d97f6a514dcdf81bda66f0e930bdc2f83b2e8252e365acee1  generate_boundary.py
4803b2e40dba06c0f82c3d23cbd5ae0a9127da0db24e5655971fff179fb68ec3  objective-twelve-component-fast.json
55bdf9d61abb6993b7ab19dba573cdd2ed6b89920fe3a97346d070bfa0e50ae7  test_boundary.py
17023cb2518b175af1ebfd5e4daebf8416ca90433cd3c7759576ecd1e89b70dd  verify_certificate.py
```

With CPython 3.11.2, one process pinned to one CPU core, I obtained:

- generator PASS in 15.505 seconds, with a byte-for-byte identical certificate;
- all six focused tests PASS in 0.332 seconds;
- target independent verifier PASS in 75.362 seconds.

Both full target runs reported:

```text
sources=238 raw=1924 pairs=1923 targets=1785
components=164 simple_cycle_rank=64 multigraph_cycle_rank=65
```

## Independent all-five-subsets checker

[`independent_five_set_check.py`](independent_five_set_check.py) uses neither
reviewed program. Both reviewed implementations count triangles in common
color neighborhoods. This checker instead materializes every one of the
`C(43,5) = 962,598` five-vertex sets and its ten edge IDs.

For each of the 238 source states, it updates the five-set red-edge counts
from the cyclic seed. A flip destroys a monochromatic five-set exactly when
its red-edge count is 0 or 10. It creates one exactly when the count is 1 or 9
and the flipped edge is the unique minority edge. Summing those definition-
level effects reconstructs the objective after all 903 flips without a
common-neighborhood triangle counter.

The checker independently reconstructs and compares, entry by entry:

- all 238 sorted canonical objective-12 source rows;
- all 1,785 sorted canonical objective-13 target rows and their free
  `C_43` orbits;
- all 1,923 source-target records and their multiplicities;
- all degree and support-signature histograms;
- all three source-family summaries;
- all 164 bipartite component profiles and both cycle ranks; and
- the complete published `claims` dictionary.

Three one-core runs passed; the final run took 32.993 seconds and used 92,764
KiB peak RSS. It printed:

```text
PASS clean-room all-five-subsets verification of Cyclic(43) q=13 boundary
python=3.11.2 five_sets=962598 cpu_processes=1
sources=238 raw=1924 pairs=1923 targets=1785
components=164 simple_cycle_rank=64 multigraph_cycle_rank=65
parallel_pair=source[232]->target[270] flips=[(83, (2, 3), 1), (407, (11, 12), 1)]
families={'cycle_only': 190, 'two_16_one_5': 38, 'two_17_one_21': 10}
certificate_sha256=af8b6892049ace5610e2d7cea4c8642f39f53634287474127990aca0abbe2b85
peak_rss_kib=92764
elapsed_seconds=32.993
```

Checker SHA-256:

```text
18f226475a3ad6beba2db3b55baf4a3e5479a570c57de698311407d8b1e4ce93  independent_five_set_check.py
```

Run from the repository root:

```bash
taskset -c 0 python3 \
  ramsey_r55_q13_boundary_review/independent_five_set_check.py \
  ramsey_r55_cyclic43_q13_boundary_certificate/objective-twelve-component-fast.json \
  ramsey_r55_cyclic43_q13_boundary_certificate/boundary_certificate.json
```

The implementation uses only the Python standard library, exact integers,
packed integer/array data, and no floating point, randomness, network input,
solver, or target-project import.

## Mathematical conclusion and scope

For the hash-pinned list of 238 source orbits, all 214,914 one-edge moves are
accounted for. Exactly 1,924 moves land at objective 13. Rotation
canonicalization gives 1,923 distinct source-target pairs and 1,785 distinct
target orbits; precisely one pair has multiplicity two. This explains the
simple rank 64 and multigraph rank 65. Independent bipartite search produces
164 components and none mixes the three source-support families.

The unique parallel pair is certificate source 232 to target 270. Its two
preimages are flips of length-one edges 83 = `{2,3}` and 407 = `{11,12}`;
both canonicalize to the same cycle-only target. This gives an explicit,
independently reconstructed witness for the sole extra multigraph incidence.

The three family totals are independently confirmed: 190 cycle-only sources
reach 1,381 targets in 122 components; 38 `{5,16,16}` sources reach 386
targets in 34 components; and 10 `{17,17,21}` sources reach 18 targets in
eight acyclic components. The last 18 targets are exactly the seed family
used by the separately reviewed six-component small-support q=13 closure.

The result is conditional on the 238-state source array. Its hash and internal
format are checked, but this review does not regenerate the upstream
69,071,588-orbit primary sublevel-12 closure or establish that these 238
states are the complete additional objective-12 family. It proves the exact
q=13 boundary map from those sources, not completeness of the global q=13
layer, absence of disconnected low-objective components, existence of a
43-vertex Ramsey graph, or `R(5,5) >= 44`.
