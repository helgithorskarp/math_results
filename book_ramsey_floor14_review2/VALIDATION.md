# Completed validation record

Actual agent **six-reviewer-2**, independent mathematical reviewer,
2026-10-01. All intensive jobs were sequential under unchanged1CPU/2GiB
limits; numerical threads were one. Generated data remains private scratch.

Final source was checked with CPython3.11.2, g++12.2.0, C++17, and
OpenSSL3.0.22 headers/library. Native release flags are
`-O2 -Wall -Wextra -Wpedantic -Werror`, linking `-lcrypto`.
Sanitizer flags are `-O1 -g -fsanitize=address,undefined
-fno-omit-frame-pointer`. Final strict compilation has zero diagnostics.

Two fully cold audit work directories regenerated core carrier, selected
rows, native input, executable and complete matrix proof. Their deterministic
result files agree byte-for-byte; time/RSS metrics are excluded from that
comparison. A preliminary complete run also matched before formatting-only
warning cleanup and addition of the separate control mode.

| Phase | Seconds | Parent peak KiB | Child/compiler peak KiB |
|---|---:|---:|---:|
| Final cold normal audit | 63.4645179150 | 20768 | 135476 |
| Final cold optimized audit | 64.4797992380 | 23104 | 135284 |
| Normal controls | 17.3203444820 | 19416 | 388348 |
| Optimized controls | 17.5606032480 | 21984 | 388260 |

Normal/optimized deterministic control files also agree byte-for-byte.
The child control peak includes sanitizer compilation. Per-phase parent
and child peaks are separate process statistics, not summed host peaks.
No resource setting or guard was increased.

Expected complete audit:2607 six-point graphs,11 F orbits,56 profiles,
256500 labeled local cores,933 selected row pairs,1747161 residual matrices,
16037994 pairing nodes, maximum64555 nodes in one fiber, and a checked
negative form for every matrix. The largest selected negative form is -1.
All fibers complete under200000-node/ten-second guards.

The audit's canonical JSON SHA256 is
`2b38198391b0339bcf6221ab896891a514ae89f332cf76c013e83b9d8a0bbb70`.
The combined compact evidence record canonical JSON SHA256 is
`6cf31b953c636fabd01834b537b70dae9f347e9b625bb112d4e6683e3b148e78`.
Here canonical JSON means sorted string keys, no insignificant whitespace,
and no trailing newline. Every key in these records is a string before
serialization, so encoding and JSON-roundtrip hashes use the same convention.

The full author-selected-pair and matrix-sequence SHA256 pins agree with
the independently regenerated sequences, both globally and per profile.
This is hash corroboration of the complete sequences, not an assertion that
an unpublished author corpus was obtained and compared entrywise.

Controls:512 weighted-graph domains match16077 direct Cartesian assignments
entrywise;56 local matrix conjugacies and15840 pair identities at352 roots
in16 arbitrary ten-regular graphs pass. Six malformed/noncertifying inputs
are rejected. Two tiny-guard cases return an explicit INCOMPLETE error.
One actual nonempty residual-matrix fiber passes address/undefined-behavior
sanitizers with zero diagnostics. These controls do not claim a valid
22-vertex host or a new primary lower-bound construction.

The saved-record verifier passes for both completed cold audit records and
both control records. Its publication-path invocation authenticates default
input bytes and checks completed evidence; that comparison is not an
additional cold proof run. Default verify.py regenerates everything.

The ordinary incidence, normalization, imported-premise transfers, defect
cycles, blue-degree consequences, spectral budget and witness centering
are reviewed written mathematics. refinements.py checks scalar identities
and exact endpoints; it does not formalize those universal arguments.
No solver, floating proof input or externally generated graph catalogue
enters this audit.
