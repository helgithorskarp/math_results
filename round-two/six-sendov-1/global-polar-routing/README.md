# Global low-sublevel routing for degree-nine first-power Sendov

Actual author **six-sendov-1**, researcher,2026-10-02. Ordinary analytic
author proof, unformalized and independently unreviewed.

For actual marked disk-rooted complex degree9, on
\(0<\eta=1-a\le2^{-16}\), \(F\le8+3\eta\), the global result proves
\(H<2^{28}\eta\), reciprocal angular defect \(<9\eta\), radial variance
\(<13\), imaginary critical energy \(<144\eta\), and weighted original
radial deficit \(<10\eta\). No critical radius, energy or coefficient cap
is assumed. The resulting global linear annulus is
\[
0<1-|a|\le2^{-37}\quad\Longrightarrow\quad
F>8+\frac83(1-|a|)-\frac43(1-|a|)^2>8+\frac{13}{5}(1-|a|).
\]
The stronger bound is credited to9620 **after** the new global carrier
establishes its fixed-energy hypothesis. The unrestricted first-power
endpoint remains open. Read [PROOF.md](PROOF.md) and
[LITERATURE.md](LITERATURE.md) for hypotheses and dependencies.
The fresh9667 independent audit confirms9620 and adds9/57820 to its
linear coefficient. The proof separately credits and transports that
stronger bound to the same global2^-37 annulus; no verdict transfers
to the new global carrier.

Use CPython3.10+ standard library; verified with3.12.14, no packages.
Run from the repository root, all native thread variables one:

    env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 -I -B round-two/six-sendov-1/global-polar-routing/verify.py
    env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 -I -B -O round-two/six-sendov-1/global-polar-routing/verify.py
    env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 -I -B round-two/six-sendov-1/global-polar-routing/validate.py

Expected PASS: whole exact record
6ffd3a3f6bc620f758ba4c3b5d54d55b3c18be6c7637e1b11c6591fd10b69eac,
full polynomials of degrees48,24,24,16 strict whole-window margins,
10 complete Gaussian-rational controls,three actual multiplicity
controls,six rejected mathematical budgets and eight rejected altered
record controls. [EXPECTED.json](EXPECTED.json) is reconstructed
independently of its values and compared as a complete typed record.

[validate.py](validate.py) runs children serially with45s guards and
six native thread variables one. It verifies the sealed
[MANIFEST.json](MANIFEST.json), positive normal/optimized outputs,
28 external fixture rejection runs and four copied source-pin rejection
runs. Evidence is in [VALIDATION.json](VALIDATION.json). Default
invocations leave source and fixtures unchanged. Explicit fixture
regeneration is verify.py --emit; explicit source/evidence resealing is
validate.py --seal. Neither is used by default or by rejection controls.

Two finite algebra routes construct the complete balanced polar
polynomial; this is author cross-checking, not independent review.
The checker has no solver, floats, numerical root finder, campaign
executable imports, heuristic universal inference or large certificate.
The mathematical controls at the collapsed actual family lie outside
the low-sum cut and only corroborate identities.

The ordinary proof supplies the identities, Maclaurin, integration and
norm estimates, floor-preserving normalization and all case coverage.
The full real defect8656, phase estimate7244 and fixed-energy9620 are
explicit written dependencies; checking this fixture does not formalize
or re-audit them. Source publication and graph commitment are separate
from mathematical review.
