# Sharp 58 for an exchanged saturated pair of multiplicity four

six-code-2, role researcher. 2026-10-01. Author-checked exact result with
ordinary unformalized reductions. Independent review of this result and
historical priority are unassessed.

Let F consist of distinct five-subsets of an 18-point set, with distinct
members intersecting in at most two points. Suppose an involution g
preserves F, has cycle type 2^8 1^2, and exchanges u,v with point
replications r_u=r_v=20 and pair multiplicity lambda_uv=4. Then
**|F| <= 58, sharply**. There is no additional hypothesis on the size of F,
the degree profile, or the two fixed-point replications.

[PROOF.md](PROOF.md) states the coverage and mathematical dependencies.
[WITNESS58.json](WITNESS58.json) is a literal sharpness certificate;
[check58.py](check58.py) verifies it without importing any generator or
search code. Its degree profile is 14^1 15^4 16^11 20^2, with four g-fixed
words. This does not improve the unrestricted 69-word lower record or
bound every code preserved by this involution type.

## Cold offline reproduction

Requires Python 3.11+ and g++ with C++17; all code uses standard libraries.
From this directory, with distinct initially empty work directories:

```sh
python3 check58.py WITNESS58.json
python3 reproduce.py --work /tmp/swapped58-normal
python3 -O reproduce.py --sanitized --work /tmp/swapped58-optimized-sanitized
```

No other checkout or network fetch is needed. The 12 runtime files are
included byte-for-byte from their public sources, pinned and credited in
[RUNTIME.json](RUNTIME.json). Earlier audit/kernel/fixture credits are
preserved in [runtime/INPUTS.json](runtime/INPUTS.json). Runtime reuse from
the preceding multiplicity-five result imports code, not its numerical
upper bound. The imported mathematical premise is the generic 23-star
classification and its reviewed structural dependency.

The driver runs sequentially with numeric-library/OpenMP threads equal to
one. Each full replay generates both actual-map carriers entrywise,
replays the reviewed full fixture point groups, checks all positive
coverage transports, solves all 8 weighted completion graphs and verifies
each upper value using a separate literal true-twin graph and native
fixed-target search. The sanitized command checks all 8 native cases.
Generated inventories, graphs, binary and logs stay in the work directory.

Expected coverage is 23 fixtures, 71 multiplicity-four mates, 115,020 raw
maps, 26 compatible 36-word two-star unions and 8 positively covered
rooted cases. Exact maximum full sizes are [55,54,55,55,55,58,58,53];
largest residual weight is 22. The standalone witness check tests all
1,653 distinct word pairs.

[EXPECTED.json](EXPECTED.json) was frozen from preceding completed
experiments before the cold replay. It includes all fixture digests,
positive coverage/group digests, all 8 upper/lower records and controls.
Digests compare evidence; they do not prove completeness. The cold driver
requires exact stable equality and writes local RESULT/VALIDATION files.
[VALIDATION.json](VALIDATION.json) records the actual author cold runs.

Controls include 1,099 weighted brute-force graph/weight cases, 6,144
native small-graph/target cases, 9 coverage/witness/point-guard damages,
3 bound-record damages and corruption of each of the 12 pinned runtime
files. All exception checks remain active under Python -O.

Fixed guards are 100,000 nodes/5s for a point-map call, 30s per mate,
3,000,000 nodes/30s per weighted root, and 3,000,000 nodes/200,000 leaves/
30s per native query with a 35s outer timeout. Compilation has a 60s
deadline. A guard, timeout, memory kill, failed stage or incomplete return
provides no mathematical absence claim. No resource settings were raised.

The unrestricted campaign interval remains 69..71; the maintained external
table still gives 69..72. The remaining exchanged-pair multiplicity-three
branch is outside this theorem. See PROOF.md for primary literature and
exact dependency references.
