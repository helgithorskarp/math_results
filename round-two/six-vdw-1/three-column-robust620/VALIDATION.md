# Author verification

six-vdw-1, researcher, 2026-10-01. This records author checks; independent
peer review and formalization remain unclaimed.

The pre-existing expected.json was frozen after the initial complete
production census and separate complete literal checks, before the fresh
source-only replay. The runner requires it and never rewrites it. Source
and compact evidence here suffice to regenerate every omitted artifact.

The complete fresh default replay finished with
`COMPLETE_AUTHOR_CHECKED_THREE_COLUMN_ROBUST620_LEMMA`:

| Measurement | Observed |
|---|---:|
| Normalized field/row cases |42|
| Independent literal coverage records |13285384|
| Generated record bytes |119568456|
| Sequential child invocations |133|
| Child timeout guard |35 seconds|
| Library threads |1|
| Total elapsed time |162.896242343 seconds|
| Peak child RSS, including compilation/sanitizers |453856 KiB|
| Small exact input controls |121513|
| Positive small controls |45561|
| Concrete corruption rejections |31|

Python3.11.2 and g++ (Debian12.2.0-14+deb12u1)12.2.0 were used. No SAT
or other solver ran. Each successful child's exit, output and duration
was durably journaled in the private work directory. No timeout, UNKNOWN
result or failed job is used as a mathematical premise.

Both Python modes regenerate byte-identical full row and triple data, and
the helper-free row/field auditors agree on their complete metadata. The
row census SHA256 is
`4279cfc97ba5cf70887c55d28f113ef0c225d51a57dba4d91dc1f975ba18a0e1`;
the field-triple census SHA256 is
`b8f449f031a95bf2d00fef6048a612870c8180234df23ab0b5b46e07586e339c`.
Every one of42 native case files is checked separately by the independent
domain-cardinality/membership/uniqueness/literal-AP auditor. The entire
deterministic output and all file hashes match the frozen evidence.

Address/undefined-sanitizer builds repeat all42 case generations and every
literal check, comparing all record bytes and complete check metadata to
the optimized builds. The small controls separately check linear paths and
punctured segments against direct exhaustive assignments, including
45561 positive cases and all-allowed/all-forbidden transition controls.
The repetition and paired edit arithmetic agrees in both Python modes.

Eleven native damages and five row plus five triple damages in both Python
modes are rejected. These test the independent checks rather than merely
the frozen hashes. They include a literal witness that touches an exception,
nonzero undefined hole bits, missing/extra/duplicate/truncated records,
wrong starts/colors/steps, missing cases and corrupted row/triple coverage.

The generated119.6 MB record corpus is omitted. Timing/version receipts
and private exploratory four-column pilots are also omitted. Pilot results
are not a complete four-column reduction or exclusion. The exact proof
boundary and ordinary CRT/affine bridges appear in PROOF.md; source hashes,
sanitizers and repeated author checks are not independent peer acceptance.
