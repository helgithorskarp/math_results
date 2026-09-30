# Three preparations before the minimum merge

**six-sorting-1, researcher.** Every20-gate completion of the fixed Y1/Y2
images, and every18-gate completion of the common R137 image, needs a unary
minimum-kernel event and at leastthree nonkernel gates before its last
minimum merge. Read [PROOF.md](PROOF.md) for the exact quantifiers and imports.
Y20/R18 and the global44-versus45 question remain open.

Standard-library Python3.11+, without `-O`, one CPU/job at a time:

```sh
python3 generate.py
python3 verify.py
python3 verify_R.py
```

Expected:21311 states/1172105 transitions/no accepting terminal, state hash
03b463a9c967daa8d02cad597f73848cdeff3df70566da20509a3b635d81af96;
R137 size18..19 and16384 full45 control executions. Local regeneration
takes approximately6seconds/31MiB, independent checking10seconds/33MiB,
and the Boolean R replay less thanone second. The unchanged algorithmic
budget is50000states/45seconds; reaching it fails loudly, never proves
exclusion. No full graph dump or solver package is needed.

[fixture.json](fixture.json) includes the exact prefixes, rows, checked
controls and imported route premises. [certificate.json](certificate.json)
is a compact hash/count certificate, with full states regenerated in RAM.
[generate.py](generate.py) and [verify.py](verify.py) use different transition
representations and traversal orders; the latter imports no generator/SAT.
The earlier minimum-one-passage result is imported from source
9a5d74c698bd8583f4bedbd50e10bbdb89d763e5 /
graph bafkreibd7xjljyxowbj3ly35iccehent53fkktliol35knttxsgblu56wu.
This is algorithmic independent checking, not an external reviewer verdict.

No known19 positive control is asserted to obey the18-budget q1=2 or
preparation constraints. Solver UNKNOWN and the unfinished unrestricted
closure are explicit limitations, not certificates. Large transient CNFs,
native traces, private checkpoints, keys and ledgers are excluded.
