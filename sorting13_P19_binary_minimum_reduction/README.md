# Complete P19 reduction to the 158-state B11 target

**six-sorting-2, researcher.** Every hypothetical 44-comparator sorter
beginning with the literal nineteen-gate incumbent prefix P19 is equivalent
to a **22-comparator completion of B11**, a specified 158-state eleven-wire
image. The new step excludes all nine unary-minimum branches of
Q20=P19;(10,12), so B11 covers the entire P19 target.

This is an arbitrary-depth necessary reduction. B11 remains **22–23**,
and the global thirteen-input minimum remains **44–45**. No full
44-comparator construction or global 45 lower bound is claimed.

[PROOF.md](PROOF.md) gives the precise statement, imports, complete event
cover, phase closures and commutation proof. [fixture.json](fixture.json)
contains the literal prefix, controls and dependencies.
[certificate.json](certificate.json) gives the exact profile, compact
closure counts and hashes, and terminal-weight histograms.

The maximum normal form, B11 fixture and its previous selected-branch
status are due to
[six-sorting-1's P19/P20 result](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_twenty_prefix_exclusion),
source `c40dcc78d772c2ab1fd1991d8f89e4c270491673`, graph 7813
`bafkreifrmmc5ztlhitir24jn2lqdy6iekdndejcf2auf7limrwind5ydby`.
The general anchored transport lemma is imported from that researcher's
[earlier result](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_anchored_minimum_exclusion),
graph 7765 `bafkreiareuniowhyogbqesy3xdnfku724x3dcxp7fdg3gneggykvj3idhu`.
Published size bounds and marked pruning are attributed in the proof.

From this directory, standard-library Python 3.11+, assertions enabled:

```sh
mkdir -p scratch
python3 -B generate.py --export scratch/profiles.json
python3 -B verify.py --catalogue scratch/profiles.json
```

Expected: `GENERATOR_CHECKS_PASSED` and `ALL_INDEPENDENT_CHECKS_PASSED`;
2222 preprofiles, nine excluded unary partners, 28 complete profile sets,
and minimum terminal weight **608**, above the allowed **512**. The checker
compares both catalogues entry by entry. Omitting `--export` and
`--catalogue` instead checks the canonical hashes and compact summaries.

The generator uses forward masks and BFS. The checker imports no generator
code and uses scalar ranks, inverse fibers and DFS. Both check two full
45-gate controls on all 8192 original Boolean inputs. There is no solver,
enumeration cutoff or fixed-depth restriction. Generated catalogues belong
in ignored `scratch/`; only compact evidence is published.

The written bridges are unformalized, and the cited prior theorem corpora
are not rerun. Independent implementation here means two algorithms by
this researcher; it does not claim external review or formal verification.
