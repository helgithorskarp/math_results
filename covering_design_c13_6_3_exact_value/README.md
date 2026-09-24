# The covering number C(13,6,3) is 21

This directory supplies a complete computer-assisted proof that twenty
six-subsets cannot cover all triples of a thirteen-element set. The known
21-block witness is checked directly, giving **`C(13,6,3)=21`**.

The reduction joins two complete degree-nine point links from the
[107-class catalogue](../covering_design_c12_5_2_classification/), then
exhausts the six or seven blocks left over. It covers all three possible
global point-degree profiles uniformly:

| Profile | Primary roots / completion instances | Independent roots / completion instances |
|---|---:|---:|
| `(12,9^12)` | 954 / 72,730 | 1,284 / 176,343 |
| `(11,10,9^11)` | 8,451 / 999,042 | 14,124 / 2,786,106 |
| `(10^3,9^10)` | 12,819 / 1,849,757 | 23,540 / 6,179,962 |
| Total | 22,224 / 2,921,529 | 38,948 / 9,142,411 |

Every instance is unsatisfiable in both full runs. The primary proof uses
shared-row identifications and uncovered-triple branching. The independent
proof uses point bijections, every labeled excess decoration, and branching
on entire point stars. See [PROOF.md](PROOF.md) for completeness, symmetry,
and pruning arguments.

External review of this proof and the 107-class catalogue is **pending** at
publication. These are exact reproducible computations and internal
algorithmic checks, not proof-assistant verification or independent peer
review. The catalogue's upstream maximum-degree-five result still carries
its documented SAT/DRAT trust boundary.

## Reproduce the result

Run these commands from this directory. The primary proof requires Python
3.11 or later and only its standard library. The native independent audit
additionally requires a C++20 compiler. Production used Python 3.11.2 and
GCC 12.2.0 on Linux x86-64.

```bash
sha256sum -c SHA256SUMS
python3 check_upper.py
python3 verify.py --workers 3

c++ -std=c++20 -O3 -Wall -Wextra -Wpedantic -Wconversion \
  -fPIC -shared star_audit.cpp -o star_audit.so
python3 verify.py --method audit --workers 3

python3 controls.py
python3 join_controls.py
python3 validate_native.py
```

Both full searches must exit successfully with status
`NO_TWENTY_BLOCK_C13_6_3_COVER`. They compare all totals and all 321
per-design records against [EXPECTED.json](EXPECTED.json) and
[AUDIT_EXPECTED.json](AUDIT_EXPECTED.json), including digests covering every
root and every joined configuration. `check_upper.py` must report
`VERIFIED_C13_6_3_UPPER_BOUND_21` and 286 covered triples.

The audit has a slower, entirely Python execution path:

```bash
python3 verify.py --method audit --python-audit --workers 3
```

This uses the same expected results and removes the C++/FFI dependency from
the local audit. The production audit used the native engine. Its outputs
were compared with 13,214 completed Python reference roots, covering
3,559,694 instances; a full Python audit was not completed in this pass.

`--workers 1` is supported. For each profile with `N` roots, `w` workers
process the disjoint intervals `[floor(N*i/w),floor(N*(i+1)/w))`. Worker
exceptions propagate, and the merge requires every root index exactly once.
The commands impose no search time or node limit. An interrupted run does
not produce an exclusion result. `--write-reference` is provided only for
regenerating comparison files; ordinary verification should omit it.

## Checking build and controls

```bash
c++ -std=c++20 -O1 -g -Wall -Wextra -Wpedantic -Wconversion \
  -DCOVER_AUDIT_MAIN -fsanitize=address,undefined -fno-omit-frame-pointer \
  star_audit.cpp -o star_audit_sanitize
python3 validate_native.py --sanitizer ./star_audit_sanitize
```

The native/reference validation covers 150 inputs: 142 negative instances,
seven positive completions, and one inconsistent-degree case. It compares
verdicts, both state counters, and witnesses exactly. The checking build
must produce no sanitizer diagnostics. `controls.py` separately checks
21 positive completions across the three engines and three negative degree
mutations. `join_controls.py` recovers a real two-link union from the known
21-block cover, exercising both join algorithms and the maximal-link
normalization.

The packaged primary replay took about 16.5 minutes and the independent
replay about 7.2 minutes, each with three workers on the research host.
Complete measured costs and comparison results are
recorded in [VALIDATION.json](VALIDATION.json). Runtime depends on interpreter,
hardware, and concurrent work; elapsed time is not part of the proof output.

## Inputs and proof dependencies

[LINKS.json](LINKS.json) is a compact projection of the upstream catalogue:
IDs, blocks, point signatures, point orbits, and automorphism orders. Its
file SHA-256 is
`9692432b695c08e844deefa60c727f603cbf59c0fa7cc6d9d00bcbc9a2944887`.
Each mask uses one bit per point, with indexing starting at zero. The upper
witness [UPPER21.json](UPPER21.json) instead lists points `1,...,13` explicitly
and credits its source.

To replay the imported classification, follow the commands in its
[README](../covering_design_c12_5_2_classification/README.md). Both its primary
and independent classification runs were replayed for this result. The
classification's maximum-degree-five prerequisite and the known lower
bound `C(12,5,2)>=9` are mathematical inputs, detailed in
[SOURCES.md](SOURCES.md).

No earlier global degree-profile exclusion or triple-multiplicity cap is
needed by this proof. The 107-class catalogue and its prerequisites remain
essential. Source and compact input/output summaries are supplied; large
search logs, proof trees, upstream DRAT traces, caches, and binaries are
omitted. The hashes are reproducibility checks, not independent UNSAT
certificates. Rechecking nonexistence requires executing the exhaustive
algorithms and accepting their documented trust boundaries.
