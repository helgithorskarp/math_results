# Fresh validation, 2026-10-01

Agent **six-vdw-2**, role **researcher**. Same-author distinct algorithms;
no independent peer-review verdict or proof-assistant formalization.

The published generator and separate literal auditor rebuilt all 18 models
in a fresh external directory. All CNFs matched the original experiment
byte for byte. All native proofs were newly proposed under the unchanged
50,000-conflict / 30-second process cap, converted, and checked by the
SHA-pinned positive-RUP kernel in normal and optimized Python.

- Final status: `EXACT_PHASE_ENDPOINTS_7_37_EXCLUDED`; nonconstant phase band `[8,36]`.
- 18 exact refutations; 202015 checked additions and 3622090 checked hints per replay.
- All 18 LRAT files reproduced their recorded bytes and counts exactly.
- Fresh complete generation/audit/proposal/conversion/replay: 120.643 seconds.
- Peak child / parent RSS: 73336 / 27024 KiB.
- Largest native conflict count: 34009; no UNKNOWN or stage timeout.
- Literal AP census: 375760 retained, 4312 through zero removed, 26488 signed supports.
- Packing cover: 28 rooted profiles, four cyclic orbits, 176 labeled phase words per endpoint.
- Exact controls: 16160 anchors, 61888 signed rotations, 67836 threshold cells, 2044 exact-five checks.
- All 12 concrete corruption probes rejected in both interpreter modes: 18.878 seconds.

The corruption probes remove one packing case and one close case, flip the
actual final counter unit, change a helper before import, and supply an
empty proof without valid hints or a proof using a nonexistent live hint.
`guards.py` reconstructs these probes without an uploaded corpus. Positive
QR controls and the complete source/definition/certificate checks remain
separate obligations.

Runtime: Python 3.11.2, python-sat 1.8.dev24, six 1.17.0, CaDiCaL195.
All solver/BLAS/OpenMP threads were one, with one CPU-intensive subprocess
at a time. Definition stages used 55-second deadlines; converter used
25 internal / 30 external seconds. No resource or infrastructure settings
were changed.

The run used the README commands with an existing equivalent virtual
environment and pinned converter. Generated CNFs, traces, logs, environments
and binaries stay outside Git. Exact per-case hashes are in EXPECTED.json,
and the source manifest is SHA256SUMS.

The mathematical window lemmas are imported from the precisely cited
source/graph contributions. Native status, timeout, fixtures or metadata
flags are not substituted for their proofs or for the new exact checks.
