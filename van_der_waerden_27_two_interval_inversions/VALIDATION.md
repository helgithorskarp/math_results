Actual author: six-vdw-1, researcher. Source-only replay completed2026-10-01
with CPython3.11.2, Python-SAT1.8.dev24, CaDiCaL1.9.5 and a serial `cc -O2`
build of the attributed proof transformer. No private proof file was an input.

All16 required serial jobs completed. The canonical CNF, regenerated DRAT
trace and regenerated positive-hint LRAT trace matched the reference hashes
exactly. Both normal/O literal audits matched all32,589 clauses, including
every actual AP and fresh prefix-counter variable. Both strict Python proof
checks derived the empty clause after22,622 RUP additions and54,807 deletions.
Their2,859,457 ordered hint-clause checks agree exactly. No RAT is supported
or trusted by this checker. All36 mathematical corruption trials were
rejected, and four small valid proof checks passed.

The source-only replay took16.623s overall; longest child5.069s,
maximum charged construction/audit cases196,434, and maximum child RSS
68,712KiB. The RUP proof has110,018 proof-obligation/deletion cases,
7,114,054 literal inspections and96,666 negated proposed-clause literals;
these different workload measures are reported explicitly. All children
remain below30s and serial, with solver/BLAS/OpenMP threads one. The native
query requested9,500 conflicts, reported3,904, and returned an unchecked
proof proposal in1.421s before independent validation. An UNKNOWN, timeout,
incomplete trace or exceeded bound would stop without this conclusion.

Discovery queried eleven native instances. Ten actual3704 words were decoded
in normal/O and independently tested on all1,141,450 positive integer APs
each. Each was invalid; their verified bad APs enlarged the initial419-AP
pool to1,485. Neither those ten failures nor native UNSAT was treated as an
exclusion. The complete CNF reduction, positive-hint proof and strict checker
provide that conclusion. Discovery source and bulky traces remain in scratch.

Additional author validation: the two-interval gap identity matched actual
inequalities for all128 seven-bit patterns at each of three AP geometries
in[1,13], all1001 strict cut quadruples per pattern, both Python modes;
all28 corrupted identity fixtures failed. A nine-position CNF regression
checked all512 edit masks against direct run/AP definitions in both modes.
That small SAT regression is not negative proof evidence for3704.

Two pinned upstream native checkers also validated the original proof.
A wrapper then expected the wrong textual success label from the second
checker (`s VERIFIED` instead of its actual `c VERIFIED`). That wrapper
failure and successful native output were preserved separately; no native
rerun was used to repair metadata. The final strict Python RUP check and
source-only replay provide independent accepted evidence.

Public artifact boundary: base word, canonical AP list, explanatory source,
compact hashes and the attributed59,546-byte transformer source only.
The4MB DRAT trace,18MB LRAT trace, generated CNF and operational journals
are regenerated locally and omitted from Git. No archives, compression,
credentials, keys, ledgers, virtual environments or unrelated files are used
as publication artifacts. Trust remains the written reduction and explicit
integer checker executed by Python; no external acceptance is claimed.
