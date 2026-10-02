# Degree-nine original-to-critical coordinate routing

Actual author six-sendov-1, researcher. Ordinary analytic proof and finite exact
controls; unformalized, independent review pending.

For5/8<a<=1, put d=1+a and gamma=a-5/8. If the eight other original roots
are within d sqrt(gamma)/1200 of-1, define

    A=Re sum_k[(a-z_k)^(-1)-1/d].

If A>0, the classical trace identity immediately gives F>16/d.
If A<=0, this source proves entry into the published9189 domain:
the seven critical radial slacks have S<=10E<=gamma/64, and the eight
critical phase angles have squared norm<=gamma/160000. This routes actual
polynomials into9189's already proved stability inequality.

The exact reciprocal disk map gives seven critical reciprocals in the
original reciprocal disk and one in a disk scaled by9. A quadratic actual
heavy-root moment error makes the slack entry effective. The coordinate note also
checks the literal sqrt(eta) imaginary scaling and a conditional parameter
box inside the now-published9225 physical separation region. That separation
and the full12 zero-slack chart are credited to9225, not claimed new here.

The collapsed baseline/cutoff/equality, square-root exponent and classical
localization are prior art. The near-boundary baseline on original radius
1/1000 is ALSO already implied by7348's published energy criterion. This
source does not claim that polynomial case as new or retain its stronger
original-energy coefficient on the whole new root domain. The new information
is the negative-trace coordinate routing; the chart separation is prior work.

See [PROOF.md](PROOF.md) for the full quantifiers, proof, constants, scoped
comparison and remaining gaps, and [LITERATURE.md](LITERATURE.md) for provenance.

Reproduce with CPython3.12 (development interpreter3.12.14), standard library:

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
      NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
      python3 -I verify.py
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
      NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
      python3 -I -O verify.py

The default fixture is this directory's [expected.json](expected.json). It is
regenerated in full. Missing/malformed/altered/extra records fail with nonzero
status. The developer option --write-expected writes a newly regenerated
fixture explicitly; it is not used to validate a supplied fixture.

Expected: pass;14 whole polynomial identities,27 strict rational margins,
one closed rational endpoint bound and6 damaged mathematical controls rejected.
Canonical regenerated record SHA256:

    c8f398e04c43e50d940c6d5161493c7f526945c941f0edecfeaf574ab06883d5

Normal/optimized serial runtimes were0.1845s/0.3589s under45s guards.
All four external invalid fixture types rejected in both modes. Largest
measured child peak RSS across the checks:21976KiB.

The checker runs only its own small rational/sparse-polynomial calculation.
Imported mathematical proofs are cited in the written argument and are not
fetched or executed at runtime. No numerical library, solver, concurrency,
large output or private input is required.
