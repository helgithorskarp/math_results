# Fresh q8 matching descent: four nonzero endpoints

The four declared construction trials reached complete matching-coordinate
stationarity with **no good43 and no original-task exclusion**. The objective
counts all red K5s, blue K5s, and red K4s in the required maximal-packing tail.

| r | original core index | initial total | final total | final red K5 | final blue K5 | final tail K4 |
|---|---:|---:|---:|---:|---:|---:|
| 5 | 0 | 1726 | 314 | 130 | 166 | 18 |
| 6 | 182118 | 1855 | 303 | 147 | 146 | 10 |
| 7 | 364237 | 1834 | 312 | 149 | 158 | 5 |
| 8 | 546355 | 2508 | 317 | 175 | 142 | 0 |

Each trial began with fresh deterministic cross-pair bits, retaining eight
prescribed monochromatic K4 blocks and an eleven-vertex Ramsey(4,4) core.
A matching meets a five-set in at most two pairs, so the complete obstruction
count is an exact quadratic function of the matching's edit bits. Every
matching optimization exhausts all its edit subsets. Only strict decreases
are accepted, and a complete unchanged sweep ends a trial.
[PROOF.md](PROOF.md) gives the identity and finite termination argument.

The runs accepted 432 edits in batches across 1,462 exact matching
minimizations. They used 41.27 seconds of aggregate process wall time on one
core, excluding preparation and independent verification; peak per-process
RSS was 54,056 KiB. The runs ended by their mathematical stopping rule.
There was no solver timeout, randomized restart, or partial proof admission.
The independent audit checked all 432 accepted edits, all 172 endpoint
matching neighborhoods, and every physical five-set in all four endpoints.
These are author checks, not reviewer-1's independent verdict.

## Check the compact evidence

Requirements: Python 3.11+, g++ with C++20, standard libraries. From the
repository root, choose a fresh output directory outside the checkout:

```sh
python3 -B ramsey_r55_q8_matching_descent/reproduce.py /tmp/r55-q8-matching-check
```

This regenerates the initial graphs from four included graph6 cores and the
specified SplitMix64 seeds, reconstructs the saved edit paths, checks all
literal endpoint obstructions, and independently proves no improving edit
in any of the 43 declared matching neighborhoods. Expected terminal status:
`REPRODUCED_NONZERO_CONSTRUCTION_BOUNDARY`, with zero targets and exclusions.
No graph catalog download or target construction replay is needed.

For an independently requested full reproduction of the original construction,
add `--search` with a different fresh output directory. That builds the
producer, runs the small literal controls and regenerates exactly the four
trajectories before the same independent audit. The campaign did not repeat
those target trajectories during publication. Executed-source and binary
hashes, compiler flags, control scope and original resources are recorded in
EXECUTION.json, TOOLS.json, PREFLIGHT.json and EXECUTION_RESULT.json.

[VERIFY.md](VERIFY.md) describes the distinct verification algorithms and
trust boundaries. Only compact physical inputs, endpoints and accepted edit
paths are committed. Binaries, generated coefficient streams and verbose
execution traces remain in the immutable local checkpoint.

## Scope and boundary

The quadratic identity applies throughout the global q8 family. Four fresh
trajectories do not exhaust that family. Their original IDs are
bo1-q8-r5-c000000, bo1-q8-r6-c182118, bo1-q8-r7-c364237, and
bo1-q8-r8-c546355. All four tasks remain UNKNOWN, as do all 2,185,424 q8 tasks.
Root and block label ordering need only be normalized if a target is found;
it is not imposed on intermediate graphs. No valid target was found.

The cores are four literal records of the original hash-pinned
[McKay catalog](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html), whose
file hash and selected indices are in INPUTS.json. Every supplied core is
checked for both forbidden four-sets. Catalog completeness is unnecessary
for these four trials. Fresh cross-pair generation uses no historical
43-vertex graph, symmetry source, incomplete trace, or q10 survivor.

This finishes a failed construction mechanism at its declared gate. The
exact four trajectories and their matching neighborhoods are parked; this
checkpoint does not launch new seeds, plateau moves, a new factorization,
a larger edit class, or another construction phase. The whole registry
remains 518 excluded original IDs and 2,188,660 UNKNOWN original IDs. No
Discovery Net mathematical contribution, new Ramsey bound, or historical
novelty for coordinate descent, Gray code, or quadratic optimization is claimed.
