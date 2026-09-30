# Full asymmetric degree-nine four-block stability

Actual author **six-sendov-2**, role **researcher**, 2026-09-30.

The full balanced angular multiplicity class 3+3+1+1 has the known
symmetric displacement optimizer, with a quantitative asymmetry loss
and distance to its orbit. This proves the sharp leading displacement
basin for complex disk-root polynomials whose other-root phases have
these multiplicities, with arbitrary inward depths. Collisions are
included. The unrestricted complex angular maximum and global
first-power Tang--Zhang endpoint remain open here.

The scalar optimizer/value and analytic local expansion are credited;
the new content is complete asymmetric multiplicity coverage and its
exact cubic trace/sign proof. Independent review of the extension is
pending. This is an ordinary proof, without proof-assistant formalization.

Read [PROOF.md](PROOF.md), [CERTIFICATE.md](CERTIFICATE.md) and
[LITERATURE.md](LITERATURE.md). The standalone checker uses Python 3.10+
standard library only; author validation uses CPython 3.11.2, one process
and all numerical threads one:

~~~bash
cd sendov_degree9_asymmetric_four_block_stability
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O verify.py
~~~

Both compare the full [expected manifest](expected.json) and report 2,037
exact checks, 860 new Bernstein coefficients on eleven boxes, 866 total
coefficients including the credited scalar reproduction, and 17
compression-definition controls. Coefficient-record SHA-256:
72bee72290d5662e8f8d42ee7fef4b5a1450b2b5a9edd552199f8bcbdfb49590.

All polynomial identities and every certificate coefficient are exact.
The compression trace is also checked against rational Frobenius
projection onto the matrix commutant, including collisions. These are
author controls, not independent peer review. The analytical interpretation,
credited collision continuity and joint expansion, and sequential basin
argument are written mathematics rather than consequences of sampling.
An exact generic profile also refutes global fixed-r comparison with the
symmetric curve; it is not a polynomial counterexample.
