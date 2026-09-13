# A5 C0 star: 251 actual parameters, all exactly three-chromatic

This package closes one named asymmetric residual class from the Hadwiger–Nelson complex-radix frontier. It solves all 76 h4195 `remaining_six` curve pairs containing

    C0: |-z+(1-omega)z^2-z^3|=1,  omega=(1+i sqrt(3))/2.

The complete real intersection set contains **251 distinct parameters**. At 247 of them, A5(z) has 243 distinct points and exactly two active event curves. All higher-order concurrence is at omega, conjugate(omega), i or -i. The corresponding graphs have 27 or 84 physical points. Every graph is **exactly three-chromatic**.

This is actual algebraic and physical closure of the explicit class, with no conditional orbit allowances used. It leaves the rest of A5 and the five-chromatic record target unresolved. [PROOF.md](PROOF.md) gives the exact statement, full reduction, exceptional fibers, distinctness argument, and trust boundary.

The producer uses Groebner decomposition and event-derived edges. The separate solver-free checker uses resultants and gcds over exact number fields, then constructs physical coordinates and all pairwise Euclidean unit edges directly. It checks all color witnesses, including collision quotients. No floating-point equality or solver UNSAT claim is used. This is author-checked work awaiting external independent review.

| Parameters | Physical graph order | Unit edges |
|---:|---:|---:|
| 240 | 243 | 279 |
| 7 | 243 | 351 |
| 2 | 27 | 63 |
| 2 | 84 | 312 |

[REPRODUCE.md](REPRODUCE.md) gives the commands. The 196,796-byte [certificate.json](certificate.json) contains exact field coordinates, component coverage, physical edge and collision hashes, and three-colour words. [pairs.json](pairs.json) fixes the finite class explicitly. [EXPECTED.json](EXPECTED.json) records the checked result; [CONTEXT.json](CONTEXT.json) pins dependencies and the campaign boundary.

The latest primary literature checked on 2026-09-13 still identifies Parts' 509-vertex construction as the record: [Parts](https://arxiv.org/abs/2010.12665), corroborated in the introduction of [Haugland v4, 17 August 2026](https://arxiv.org/html/2608.04542v4). This package does not improve it.
