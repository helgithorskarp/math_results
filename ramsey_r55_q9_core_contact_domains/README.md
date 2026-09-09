# Exact q9 contact domains for the complete R(5,5) carrier

The joint contacts between each four-clique block and its entire seven-vertex core remove **85.309046% of the current complete h4035 bare carrier**. All 1,810 q9 task carriers shrink; each loses more than 59.24%. The other classes stay as specified by the accepted family. No task is excluded and no good43 is produced.

See [PROOF.md](PROOF.md) for the globally covering family, exact count, and trust boundary; [HANDOFF.md](HANDOFF.md) for the physical interface. `COUNTS.tsv` contains all 362 records as `core_index plain_count joint_count complement_index packed_permutation`. The permutation sends catalogue positions to the source core's labels; its entries occupy consecutive three-bit fields, low field first.

From the repository root, with Python 3.11+ and g++ 12+:

```sh
python3 -B ramsey_r55_q9_core_contact_domains/reproduce.py /tmp/r55-contact-inputs /tmp/r55-contact-replay
```

The output directory must not exist. Only the pinned 2,172-byte public seven-vertex core catalogue is downloaded if absent. Required parent source packages are already in this repository and their manifests are checked. The replay compiles both independent native counts, runs the complete release and sanitizer censuses, checks every count and complement certificate, and verifies the physical interface and rejection controls in normal and `-O` Python modes. Expected status: `REPRODUCED_Q9_CONTACT_GLOBAL_REDUCTION`.

The generated 23,912,272-byte prefix table, binaries, fixture streams, and logs stay outside Git. The prefix table is regenerated in seconds; its format and SHA256 are in `TABLE.json`. Exact aggregate results and compact control receipts are in `EXPECTED.json`. The three public fixtures are failed colorings used for interface verification.

This package does not inspect the 161 q10 children, revisit any fixed neighborhood-gluing subsystem, use symmetry-derived sources, or extend the previous augmentation rule. The new milestone is the measured reduction of a complete physical carrier.
