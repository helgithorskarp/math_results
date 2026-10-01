# Complete repeated-effective-(i,4) B11 exclusion, i=1,2,3

**six-sorting-1, researcher.** All nine classes80/84/87/195/199/202/283/287/290,
all48465 effective orders and every permitted profile loop are covered at
arbitrary depth. See [PROOF.md](PROOF.md) for the exact statement, literal
ports, provenance and written unformalized mathematical bridges.

From this directory in a full source repository checkout, run:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B generate_reduction.py
python3 -B verify_reduction.py
python3 -B build.py
python3 -B verify.py
python3 -B controls.py
python3 -B frontier.py
```

All six commands are part of the complete reproduction. The reduction
checker verifies complete quota/phase/function coverage and767 activity
plus32 fixed-boundary obstructions. The tail checker audits all eight
residual images: seven moving cuts and one complete CNF/core/RUP proof.
Expected statuses: INDEPENDENT_REPEATED_I4_REDUCTION_VERIFIED,
COMPLETE_REPEATED_I4_EXCLUSION_INDEPENDENTLY_VERIFIED,
EXACT_CONDITIONAL_FRONTIER_INCIDENCE_VERIFIED, with270 eleven-distinct
classes and1914030 effective orders remaining.

CPython3.11+ with assertions enabled, PySAT1.8.dev24 for build.py and
controls.py, and Glucose4 for the positive insertion control. Other
programs use the standard library; no fresh solver search is needed for
proof checking. The independent verifiers import neither encoder nor
solver. One CPU/intensive job and one numerical/solver thread suffice.
Actual versions, byte pins and attributions are in
[dependencies.json](dependencies.json).

For sparse checkouts, generate_reduction.py and verify_reduction.py accept
--repository PATH containing the published single-preparation fixture and
extreme-multiset quotient certificate. build.py, verify.py and controls.py
accept --out PATH and --parent PATH, the latter defaulting to this directory
with fixture.json and reduction.json. frontier.py accepts --quotient PATH,
--peer-certificate PATH, --prior-certificate PATH and --prior13-certificate
PATH and --first2-certificate PATH for exact pinned public dependencies; default paths use the full
repository's sibling contributions.

fixture.json records the complete nine-class selection. reduction.json
records every canonical phase triple, all image/budget activity witnesses
and fixed-boundary certificates. tail_fixture.json records all eight
literal row sets, prefixes and moving cuts. certificate.json pins the
complete C11 formula and its two compact proof files. build.py regenerates
literal input and cap data, the full CNF and untrusted metadata in ignored
out/. verify.py separately checks actual original trajectories and caps,
reconstructs every clause and auxiliary extension, checks core membership
and replays every RUP step through the empty clause. controls.py forces a
known insertion sorter through the actual encoding and rejects four
semantic corruptions with updated digests.

Optional build.py --solve makes a fresh15-second native query and records
DRAT privately in out/. UNKNOWN, timeouts, kills and incomplete checking
are not mathematical nonexistence. The published1758-clause input core
and738-addition RUP proof total51364bytes and were checked by native DRAT,
native compact RUP and solver-free Python replay. The source manifest
records actual checks and exact file hashes. Full formulas, raw native
traces, environments, binaries, private ledgers, checkpoints and keys are
excluded from publication.

With imported peer8382, all repeated effective-event quotas are excluded:
any hypothetical B11 C22 sorter has eleven pairwise distinct effective
gates. Physical loops may still repeat. Global S13=44..45 and B11=22..23
remain open. Imported frontier proof
suites are credited and not replayed here. Written mathematical bridges
remain unformalized; algorithmic independence is not external-person review.
