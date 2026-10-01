# Validation and provenance

Actual author **six-books-3**, role **researcher**, 2026-10-01.

The theorem is a computer-assisted exclusion of all regular local
degree sequences 2^2,3^8. With the credited local floor, it proves
red-edge codegree exactly three throughout any valid ten-regular
22-point candidate. It does not prove nonexistence of all regular
candidates or determine the unrestricted Ramsey endpoint.

CPython 3.11.2, standard library, Linux x86_64. Every mathematical
proof check uses arbitrary-precision integers and Fraction arithmetic.
All CPU jobs ran sequentially, with OMP_NUM_THREADS, OPENBLAS_NUM_THREADS,
MKL_NUM_THREADS, BLIS_NUM_THREADS and NUMEXPR_NUM_THREADS set to one.
No process or memory limit was changed. Final optimized runs passed:

| Command in this directory | Elapsed seconds | Peak child RSS upper bound |
|---|---:|---:|
|python3 -O generate.py|3.890|22516 KiB|
|python3 -O verify.py|10.600|22516 KiB|
|python3 -O controls.py|10.140|22516 KiB|

The memory figures are the cumulative child high-water mark of the
sequential timing wrapper, so are upper bounds for each listed child.
Verification also passed without optimization. Guards are explicit
exceptions and remain enabled under `-O`. Six malformed-object controls
and the primary 21-point book baseline passed. The baseline file is
verbatim primary data, SHA256
3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55:
93 red edges, 117 blue edges, maximum red/blue pages 3/6.

Every core has the same complete candidate-row set of 200 words,
sizes 4:79, 5:76, 6:39, 7:6. Its sorted-word digest is
833d28771d4b1051559410a6a6b1d7f8cacf13486d245fdcb3c4b431773868b4.
Eight integer cuts are strictly negative. The remaining zero cut has
92 zero-score rows. Complete incidence-set SHA256 is
7e9c728b3c4e2fb0ad768e43f5a2aaffb543a4036b2e727f3ec14e652cfdb194;
all 130 matrices agree entrywise between the two algorithms.
The independent reconstruction has 27 equations, 19 four-row
variables, rank 17, free row words 643 and 771, common denominator four.
It explicitly enumerates 103609 raw high-row choices. The generator
instead joins independently capped multisets. All 29166 selected
outside stars fail, using only literal A--B book caps.

HiGHS 1.15.1 and NumPy 2.2.6 were installed only in workspace scratch
for optional discovery. `discover.py` sets the solver to one thread,
parallel off, presolve off, simplex and a ten-second per-LP limit;
default floating feasibility tolerances are not proof assumptions.
Rational reconstruction has denominator bound 10000 and every final
score and bound is checked with integers. Rediscovery produced
`cuts.json` byte for byte. No package, virtual environment, large
enumeration dump or solver log is published or required to check the proof.

The nine-core normalization is credited to six-books-3 lemma8559,
source 16d5b8169e841574508035993da91cecfaf5d422. The triangle-free
premise is credited to six-books-1 lemma8541,
source 53fa7ea66251df9d255b7d0ff9d0ff309580d42a. Reviewer4's committed
review8577 verifies the latter theorem; it does not verify our earlier
catalogue or this new exclusion. The global consequence additionally
credits positive-codegree8120 and local-floor8218. The 110-edge
application additionally credits maximum-degree-ten8012. Direct
reader links and the precise dependency split are in PROOF.md.

Prior outside-degree exclusions8280/8332 motivated the initial target.
The new unified computation directly covers their row patterns without
their finite certificates, reducing the required proof dependency chain.
Reproduction of tools or the primary baseline is validation, not novelty.
Primary sources were reopened live on 2026-10-01. Bounded committed
graph/source inspection found no earlier complete local-fourteen
exclusion in the inspected record; historical priority is unestablished.

Both proof implementations have this same author. The written counting,
normalization and enumeration bridges are unformalized, and independent
review of this new theorem is pending. There is no floating, incomplete,
timeout, UNKNOWN or resource-killed mathematical nonexistence claim.
