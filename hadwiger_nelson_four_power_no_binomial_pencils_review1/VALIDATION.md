# Validation record

Validation was performed on 2026-09-13 with CPython 3.11.2, SymPy 1.14.0,
python-flint 0.8.0, and four bounded workers.

The target Groebner and target resultant/fibre producers were run separately.
They took approximately 312 and 274 seconds and wrote byte-identical
2,184,292-byte certificates with SHA-256
`f7dc43ce1f68eee6715a48527367d219b3cc592a7c82029b94831234a6587f50`.

The target verifier passed `--check-expected` in 11 minutes 52 seconds with
four workers.  The target classification, six corruption controls, collision
controls, and unit-circle/zero-weight boundary checks also passed.

The final clean-room audit passed twice.  The first final-source run took 5
minutes 13 seconds; the second used the independently generated resultant
certificate, enabled `--check-expected`, and took 4 minutes 0 seconds.  An
optimized-Python replay also passed the pinned transcript in 3 minutes 52
seconds.  All three outputs were identical.  A preceding development run exposed that the field
stage was accidentally single-core and was stopped; it produced no evidence
used here.  The checked source contains deterministic ordered parallelism.

`EXPECTED.json` pins the clean-room reverse-elimination, exact geometry,
Sturm-count, concurrency, graph, and colouring transcript.  Three negative
microcontrols also check rejection of nonreal-as-real and corrupted-colouring
claims.

The large generated certificate is not committed.  It is reproducible from the
compact target source by either of two routes and its digest is pinned above.
