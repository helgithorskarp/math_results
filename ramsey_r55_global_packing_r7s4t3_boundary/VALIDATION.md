# Validation and trust boundary

The production CNF was emitted by the exact immutable h3835 `model.py` at
source commit `3f06352ae0735101a04afa1ba7b055736e7300f7`.  Before solving, the
handoff manifest, task registry, source manifest, source module, formula,
auditor, audit record, solver, checker, and gate were frozen by SHA-256.

`audit.py` imports no h3835 module.  It independently reconstructs the block
partition, all 57 fixed edges, the lexicographic map of all 846 free edges,
the 3,360 root clauses, and both applicable target polarities for every one of
the 962,598 five-sets.  It parses the full DIMACS stream and compares every
literal in order.  Normal and assertion-disabled runs return the same record.

The production command made one CaDiCaL 3.0.1 call with a fixed 1,800-second
wall limit and proof output enabled.  It exited zero after 1,800.033 seconds,
used at most 622,648 KiB resident memory as observed by the wrapper, and wrote
the ten bytes `c UNKNOWN\n`.  No candidate was emitted.

The partial binary DRAT output has SHA-256
`261a64a840dee16a5fe9b0da8712edd3bcb4b651e755fe0aedee38c89174321b`
and size 1,507,230,814 bytes.  It lacks an UNSAT solver result, is not a
certificate, was not passed to `drat-trim`, and remains private.  Its hash is
recorded only to identify the incomplete run output.

`reproduce.py` checks the exact h3835 source hashes, regenerates the full CNF
in a temporary directory, and invokes `audit.py` under normal and `-O`
interpreters.  It does not rerun the 1,800-second solver call.  Remaining
trust includes the independently reviewed h3835 cover, CPython and subprocess
semantics, SHA-256, CaDiCaL execution, the wrapper's resource observation,
the independent audit transcription, and ordinary hardware.
