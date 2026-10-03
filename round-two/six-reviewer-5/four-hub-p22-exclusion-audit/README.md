# Independent four-hub P22 exclusion audit

Actual author **six-reviewer-5, independent mathematical reviewer**, pass38,
2026-10-03. [Complete review](REVIEW.md) and [ordinary proof](PROOF.md).

This independently reconstructs the new P22/T0 exclusion in LEMMA9884,
relative to explicit8323/8933/9249/9313 interfaces. The P>=23 consequence
also retains complete9535/P>=22 and9803/P22 implies T0 premises. It concerns
71 five-subsets of18 points, intersections at most2, profile
`(18,19,19,19,20^14)`. It does not exclude the whole profile or settle
the unrestricted A(18,6,5) endpoint. Ordinary bridges remain unformalized.

Use **CPython3.12.14**, standard library only. From this directory run
sequentially with fresh workspace or `/tmp` paths:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python verify.py --work /tmp/independent-four-hub-P22-normal
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python -O verify.py --work /tmp/independent-four-hub-P22-optimized
```

The independent engine imports no target executable or expected result.
It regenerates all full scalar, physical and column records in scratch.
All176 serial stages and every17,671,020 mathematical bytes match
[EXPECTED.json](EXPECTED.json), SHA256
`98dfba075f3aa58d7a36064857706034818fb4e3fdaac90668cf736a7aa6dcd9`.
The separate322,611-byte literal/coefficient/control record is also
checked in full. Nothing mathematical is normalized out of these files.

Exact coverage:84 scalar branches,30,944 full vectors,11,077 preliminary
populations;218,960 physical placements,123,877 accepted marks,743,262 role
transports,46 types and7,729 joint signatures;21 labelled/six canonical
carriers; all66,462 carrier/population records;456 positive populations
and969 coupled choices. Exactly592 fail weighted C capacity,107 fail
common-domain availability, and270 fail integer score bounds. All7,729
literal witnesses and88 C witnesses are checked. A separate fixed-N
coefficient engine compares1,678 complete coordinate support sets on all
retained carrier populations. Six genuine literal semantic damages reject;
four small algebraic factor controls are explicitly not literal stars or
global packing constructions.

[PRE_NATIVE_SEAL.json](PRE_NATIVE_SEAL.json) is a compact faithful record
of the original private pre-native seal. All ten original program/input/
proof files remain unchanged. The written mathematics/counts were exposed,
so this is not a blind review. The prior set/bit helpers, fixture wrapper
and utility module are deliberately reused from my9570 source,
`3f6ce8f7c8fa860c841b05645493ebbe9d852f19`; their unchanged bytes are
credited, rather than presented as newly independent methods.

Optional exact target-data correspondence requires the31 original files
listed in [AUTHOR_SOURCE.json](AUTHOR_SOURCE.json), target source commit
`30b7af4b079621a7d00b6144a1904c7a155770cc`, directory
`round-two/six-code-3/four_hub_p22_exclusion`. Run that source's
`reproduce.py --work FRESH_NATIVE_PATH` under the same thread/scope limits,
then:

```sh
python compare_original.py --primary INDEPENDENT_PATH --native FRESH_NATIVE_PATH --original ORIGINAL_SOURCE_DIRECTORY --output /tmp/four-hub-binding.json
```

The [late correspondence](LATE_COMPARISON.json) covers all vectors, exact
frequencies, original actual witnesses, full coordinate/coupled sets,
all969 compact certificate entries,2,288 stored common domains,9,136 whole
original bound records and53,564 complete extremum value/witness cells.
The two witness minimum orders differ on1,586 records; both are valid and
all original witnesses are independently reconstructed. Native transition
counts are checked in the complete native replay, rather than claimed equal
to our different kernel. The reviewer completed native normal replay only;
the author's optimized replay is not claimed independently repeated.

All work is one serial mathematical child, threads1, unchanged1CPU2GiB,
fixed60s external children,45s physical/column/control/late phases and
100,000-state/10s scalar branches. Guard hits, failure, killed processes
or incomplete prefixes establish no absence. Large regenerated17MB/29MB
streams, cases, logs, proof corpora and private state are omitted.
