# Validation and trust boundary

`controls.py` checks the production primitives on finite exhaustive cases.  It
tests 384 assignments to gated and ungated sequential counters, 32 Boolean
gate assignments, all 1,024 colorings of a five-set's ten edges, and all 1,764
pairs of spanning rank-two factor lists in the complement-rank identity.  It
also validates the reviewed row-table hash and verifies across all 10,959 tasks
that the shortened equal-row windows cover every repeated pair.  Normal and
assertion-disabled results are byte-identical.

`audit.py` does not import the formula generator.  It re-derives every variable
and clause count, reads the 138,709,891-byte DIMACS stream, validates every
literal and clause-length count, and independently reconstructs the final
1,925,196 clauses from all physical five-sets and the 903-edge variable map.
Normal and assertion-disabled audit files agree.  The audited CNF SHA-256 is
`e01a3aec66bf8d3bd0ce8aba611634abc3f5068ad6ad56511be00186d6832989`.

`reproduce.py` regenerates the CNF and metadata in a fresh temporary directory,
compares all deterministic fields with the committed evidence, reruns the
independent audit and controls, verifies `SHA256SUMS`, and checks the compact
production record.  Generation time is observational and is excluded from the
metadata comparison.

The production call was frozen before execution.  CaDiCaL 3.0.1 at commit
`c60730422e758ef1cebe7aeddf2dda31c996bf04` and binary SHA-256
`823b3c94050654fda13dab0c8c34386d9777a1e6de31bd6bc20555979e7c5e0b`
ran for 900.088 seconds, used at most 766,260 KiB resident memory as observed
by the wrapper, and exited zero.  Its ten-byte witness file contained exactly
`c UNKNOWN`.  No candidate file was created.

The partial binary DRAT stream has 834,897,993 bytes and SHA-256
`3f0e893b439d8a7c9108f7981af2eed77a322a932c6af6ac53601d4b09159d0f`.
It is operational evidence only.  An interrupted proof stream cannot certify
UNSAT, so drat-trim was deliberately not run and the large stream is omitted.
The CNF is also omitted; both regenerate from the committed source.

Trust remaining includes the reviewed h3825/h3831 task cover, the imported
h3579 and h3771 necessary conditions, the written finite-field reduction,
Python and compiler/runtime semantics, SHA-256, the pinned solver binary, and
ordinary hardware.  No mathematical inference is made from the timeout.
