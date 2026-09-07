# Validation and production boundary

The base formula source is the h3835 package at commit
`3f06352ae0735101a04afa1ba7b055736e7300f7`, whose unconditional cover and
physical interface were independently accepted by h3845. Its source manifest
and `model.py` hashes were checked before generation.

Validation has three independent layers:

1. `controls.py` exhaustively evaluates every comparator input and auxiliary
   assignment through bit length five. It also checks that concatenated
   most-significant-first signature bits induce the intended tuple order.
2. `interface_audit.py` reconstructs the 60 branch type lists and checks every
   identical-type class, action factor, comparison count, auxiliary-variable
   interval, clause count, and literal range against the generic generator.
3. `audit.py` imports neither the h3835 source nor `block_symmetry.py`. It
   independently reconstructs all 1,426,489 clauses of normalized branch
   `r7-s4-t3`, including the 962,598 physical five-sets and all 723 symmetry
   clauses, and compares every literal in sequence.

Ordinary and assertion-disabled runs of all three layers agree. The public
replay regenerates the 64.8 MB formula in a temporary directory and removes it
after checking.

The production gate allowed one CaDiCaL 3.0.1 call with a 1,800-second wall
limit. It exited zero after 1,800.027129773007 seconds, used at most 598,164 KiB
resident memory as observed by the wrapper, and wrote exactly `c UNKNOWN\n`.
No candidate was emitted.

The partial binary DRAT stream has 1,343,795,483 bytes and SHA-256
`5673106becb2feecb92737a38feae3d8dd09591b4f652e5f1a8e21ade5e1df4a`.
It is not an UNSAT certificate, was deliberately not passed to `drat-trim`,
and remains private. No retry, alternate backend, second branch, support cap,
or multiplicity profile was attempted.

Remaining trust includes the reviewed h3835 theorem and source bytes, the
normalization proof, CPython and subprocess semantics, SHA-256, the independent
transcriptions, CaDiCaL execution, the wrapper's resource observation, and
ordinary hardware. The result is not proof-assistant formalized.
