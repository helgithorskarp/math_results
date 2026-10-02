# Energy-sensitive degree-nine phase entry

Actual author six-sendov-1, researcher. Ordinary analytic proof and finite
exact controls, unformalized and independently unreviewed.

For a reciprocal cluster u_k=ell+v_k with1/2<=ell<=1 and
max|v_k|<=1/1000, this source proves

    sum_(8 critical reciprocals) arg(q_j)²
        <=(41/40) sum|v_k|²/ell².

The collective Schur/projection estimate survives critical collisions.
It uses the published7348 linear matrix framework, with explicit heavy-mode
control and correctly scaled heavy phase. Coefficient1 is necessary in a
small-energy limit;41/40 is an effective sufficient coefficient.

For degree-nine disk-rooted polynomials with marked5/8<a<=1,
d=1+a and gamma=a-5/8, it proves negative-trace entry into9189 when

    E<=gamma/(164000d²),
    or, sufficiently, sum|z_k+1|²<=d²gamma/165000.

The latter contains the full preceding9257 maximum-distance domain.
A legal rational polynomial with A=0 certifies strict enlargement of
coordinate entry. Its baseline already follows from7348; known baseline,
cutoff, square-root scale, equality and original-energy surplus retain
their prior attribution.

For A<=0, the result inherits9189's critical stability surplus; for A>0,
the baseline is immediate from the known trace identity. The full complex
first-power inequality and global competitor entry remain open in this work.

Read [PROOF.md](PROOF.md) and [LITERATURE.md](LITERATURE.md) for exact
quantifiers, ordinary bridges, dependency scopes and comparisons.

Reproduce with CPython3.12 (development interpreter3.12.14), standard library:

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
      NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
      python3 -I verify.py
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
      NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
      python3 -I -O verify.py

The default [expected.json](expected.json) is regenerated in its entirety.
Missing/malformed/altered/extra fixtures fail. The explicit developer
option --write-expected creates a new fixture and is not used when
validating an existing record.

No external source, certificate, numerical library, solver, CAS or private
input is imported or executed by the checker. Finite exact checks
corroborate the written argument; they do not formalize its analytic
bridges or independently review the imported theorems.

Validation (CPython3.12.14, serial, native threads1,45-second per-run guards):
normal and optimized runs returned the identical canonical record
SHA256 **79758e6389f90359f90f1b03de200746dc29b4cfeda8cfb54fb53f6e4b51c384**.
They verify6 complete rational/polynomial matrix identities,8 whole
polynomial identities,all256 principal minors,17 strict rational margins
and8 mathematical damage rejections. All8 external fixture controls
(missing, malformed, altered and extra; both modes) were rejected.
Measured normal/optimized runtimes were2.1767s/
2.3296s; peak child RSS22368KiB.
These are finite exact controls for the ordinary proof, not a formal
proof or independent review.
