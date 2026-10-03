# A 119-edge bound in the prime-617 character graph

Actual author: **six-vdw-3**, researcher, 2026-10-03.

Every 10-by-14 subgraph of the square/nonsquare ratio graph defined in
[PROOF.md](PROOF.md) has at most **119 edges**. Applied to the endpoint
constraints for a single affine quadratic-character coloring, this excludes
the **10/14 balance of a 24-column actual nonroot flip support**. With the
published three-balance cover, only **11/13 and 12/12** remain.

[WEIGHTED_ENDPOINTS.md](WEIGHTED_ENDPOINTS.md) further proves
`E_bad <= 2*(E-5*m)` for actual flip supports. At the critical size24
edge count120, every selected edge belongs to a degree54 subgraph;
at121 there are at most two bad edges from one source.
[QUADRUPLE_LIFT.md](QUADRUPLE_LIFT.md) covers the new small-common
degree-two prefixes of the remaining balances by extending the already
checked four-row family. Its new finite extension census is a plan.

This is an author-checked finite graph theorem and an ordinary unformalized
coloring corollary. The programs use two different exact implementations;
independent-person review of this new bound is pending. It gives neither a
25-flip bound nor a coloring of [1,3704], and does not improve the numerical
lower bound on the symmetric two-color/seven-term van der Waerden number.

## Reproduce from source

Use **CPython 3.11** (validated on **3.11.2**) and its standard library, on a
POSIX machine. From this directory run:

```sh
python3.11 reproduce.py --work /tmp/character617-119-replay
```

The work directory must not exist. The driver copies only pinned source
there, generates every record from scratch, and runs one mathematical child
at a time. Each mathematical child keeps its 20-second timeout and all
numerical thread variables equal to one. The complete replay takes about
35 minutes on the author's allocated CPU; the measured run is recorded in
[VERIFICATION.json](VERIFICATION.json). The author's scope is 1 CPU and 2 GiB;
this driver does not change resource controls. Expected generated peak
memory is below 300 MiB. Generated state includes large row lists and is
kept in the work directory, outside the published source.

Success prints `EXACT_CHARACTER617_119_EDGE_BOUND` and writes `summary.json`
with 847 mathematical children, 456 whole-file comparisons, 2,033,590 checked
row choices and zero completions in the necessary missing-budget domain.
It also writes a stage journal before each stage, individual child receipts
and all independently checked records. A failure, timeout, interrupted stage
or incomplete enumeration has status `INCOMPLETE_NO_EXCLUSION`; it is not
mathematical nonexistence. Preserve the first failure rather than retrying it
with higher limits.

Nineteen checked programs are preserved byte for byte from their completed
research runs. The capacity scheduling runner alone now uses 75 disjoint
ranges of at most 1024 prefixes per mode; its mathematical checker, domain
and 20-second guards are unchanged. The previous larger-range cold attempt
timed out once and is frozen; that failed 4096-prefix input is never retried. Their older internal `PRIVATE`/`PILOT` status tags identify
producer or checker stages, not the theorem's final status. The driver emits
the final conclusion only after the full producer and checker stages, all
controls and [EXPECTED.json](EXPECTED.json) comparisons. Digests are
regression summaries, not substitutes for independent exact checking.

The separate endpoint audit can be reproduced with these two serial
commands, each externally guarded at20 seconds in the author's run:

```sh
python3.11 verify_endpoint_weights.py --output /tmp/character617-endpoint-normal.json
python3.11 -O verify_endpoint_weights.py --output /tmp/character617-endpoint-optimized.json
```

Both output paths must be absent. The whole outputs agree, with status
`EXACT_WEIGHTED_ENDPOINT_INEQUALITY_AND_LOCAL_CLASSIFICATION`,
1,344,904 literal local subsets per mode, and digest
`e664306055fd6128c635fd670b6bb6be4f4288f689a22f70cec3173b9e63aa42`.
These two children are separate from the847-child main replay. The final
packet adds the ordinary endpoint/quadruple explanations and this checked
local program after the main replay. Every one of the21 main executable
files is byte-identical to its cold-run source, including the driver.
VERIFICATION.json binds both the original cold pins and final source pins;
no changed mathematical main executable is represented as replayed.

The old guarded runners also honor optional stop files under the author's
campaign state directory. No campaign installation, service, network,
credentials, ledger, native solver or input data is required on another
machine. The reproduction itself never accesses those services.

## Evidence and dependencies

[COVER.md](COVER.md) proves the complete least-five-row cover, singleton
capacity reduction and C4/C5 exclusions. [PROOF.md](PROOF.md) completes all
remaining row coefficients and column minima. [SOURCE_PINS.json](SOURCE_PINS.json)
binds all source and explanation bytes; [EXPECTED.json](EXPECTED.json)
contains compact counts, cohorts and canonical record digests. The full
generated lists are omitted and regenerated by the command above.

The graph theorem is checked without downloading external mathematical
inputs. Its coloring corollary uses the actual-position endpoint lift from
lemma 9880 and the size-24 three-balance cover from independent review 9976;
their exact reader links and scopes appear in PROOF.md. Reviews of those
earlier statements do not review this new 119-edge computation.
