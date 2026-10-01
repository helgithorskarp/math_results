# Arbitrary F31 XOR C20 obstruction

Every binary coloring `C(x)=f(x mod31) XOR g(x mod20)` contains a
monochromatic nonconstant seven-term AP by one-based position2480.
Both factors are arbitrary. General period620 words and the3704-point
target remain open. See [PROOF.md](PROOF.md) for coverage and scope.

Reproduce from compact source with Python3.11 and GCC12.2 (C++17),
using only the standard libraries:

```sh
python3 -B reproduce.py --work /tmp/separable620-replay
```

All stages are sequential, use one thread and have a35-second child
deadline. Generated records, native builds, damages and per-stage receipts
go in the supplied work directory. A missing/failed/timed-out child or
changed frozen fixture stops the replay; it is not an exclusion.
`expected.json` must already exist and is never rewritten by the runner.
An optional `DISCOVERY_RESEARCH_TEAM_ROOT` environment variable makes
the runner honor campaign PAUSED/HANDOVER files before each child.

The replay enumerates1111350 field inputs, independently checks every
literal witness, checks exact transfer-trace domain sizes and uniqueness,
audits all2^20 row inputs and the complete affine quotient, matches
normal/-O and native sanitizer evidence, and rejects19 corruptions.
The final status is `COMPLETE_AUTHOR_CHECKED_SEPARABLE620_EXCLUSION`.
Same-author independent algorithms, no external reviewer verdict or
formalization, and no new W(2,7) bound are claimed.

The10.0MB witness corpus regenerates outside Git. Full replay needs no
solver, external data or previously published mathematical lemma.
All source is attributed to **six-vdw-1, researcher**.
