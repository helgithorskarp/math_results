# Sharp62 in the X20/Y18 involution family

six-code-2, researcher. A five-subset packing on18 points, invariant under
an involution of cycle2^8*1^2, with fixed-point replications20 and18 and
fixed-point pair multiplicity4, has at most62 words. A literal62-word
construction attains the bound. The four-fixed-Y-word subfamily has
sharp maximum60. Independent review is pending; ordinary coverage
bridges and the imported twenty-star classification are explicit in
[PROOF.md](PROOF.md). Unrestricted campaign bounds69--71 are unchanged.

The smallest existence check uses only Python3.11 standard library:

```sh
python3 round-two/six-code-2/two_fixed_y18_upper62/check_witness.py
```

For the complete upper-bound computation, use Python3.11 and GCC12 with
C++20. There are no third-party Python packages. From a full checkout:

```sh
python3 round-two/six-code-2/two_fixed_y18_upper62/reproduce.py \
  --work /tmp/six-code-2-y18-normal
python3 -O round-two/six-code-2/two_fixed_y18_upper62/reproduce.py \
  --work /tmp/six-code-2-y18-optimized
python3 round-two/six-code-2/two_fixed_y18_upper62/reproduce.py \
  --work /tmp/six-code-2-y18-sanitized --sanitizers
```

Work directories must be new and outside the source bundle. A sparse
checkout must include the two preceding six-code-2 directories
free_involution_upper68 and two_fixed_saturated_upper60, plus
constant_weight_upper71_review1, constant_weight_absent_pair_review1,
and constant_weight_pair_two_review2. The44 required input files are
byte/hash checked before research-module imports. Missing inputs abort;
the reproducer neither guesses replacements nor changes the checkout.

The default command replays the pinned prior proof and three reviewed
validators, generates all3498 Y18 stars by two orders, and compares every
maximum family from coloring and P/X pivot search. The complete stable
record must match [expected.json](expected.json) byte for byte. It is
4028 bytes; larger generated corpora stay in the work directory. Exact
input provenance is in [DEPENDENCIES.json](DEPENDENCIES.json), and measured
validation costs are in [VALIDATION.json](VALIDATION.json).

All numerical/OpenMP threads are set to1; subprocesses are sequential.
Per-case guards remain200000 nodes/10s for star enumeration,3000000
nodes/30s for coloring, and30000000 nodes/30s for native pivoting. A
guard failure, unexpected larger clique, timeout, or incomplete child
aborts without a bound. After separately replaying the old proof,
--skip-dependency-replay still checks all44 input pins and performs all
new computations. This switch does not bypass a partial new census.

The native implementation retains192-vertex bitsets and the inherited
guards. Its added pruning is a proper first-fit coloring in static
degree order; the primary Python search uses a different coloring
order and branching rule. Both algorithms belong to the same author.
Their entrywise agreement and controls are computational validation,
not a formal proof or an independent reviewer verdict.
