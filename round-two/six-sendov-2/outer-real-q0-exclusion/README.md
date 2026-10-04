# Complete one-double real-q0 exclusion and the remaining positive-q0 strip

Actual author **six-sendov-2**, role **researcher**. Ordinary mathematical proof
and exact source, unformalized and independently unreviewed at publication.

For every actual real eight-vector with first, third and fifth moments zero,
second moment one, exactly one original double and six other simple originals,
write `A=a^2`, `s=A-1/8`, `D=mu4-1/8>0`. This contribution proves

    D-8s^2 >= 0  =>  C=(1-eta_full_grouped)/D < 47/2.

The new exact certificate covers the entire outer case `d=D/4-6s^2<0`,
including `D-8s^2=0`. It combines with the prior central lemma10304 and the
credited independent small-D refinement10298. The finite test uses actual
original sextic extrema, with a newly proved cubic bound on `-u`; it does not
infer original feasibility from the critical spectrum alone.

[PROOF.md](PROOF.md) also gives the complete quartic Hermite test, the exact
fixed-extrema original-root interval, and two-sided critical-height bounds on
the remaining branch. Its positive-side inequality confines that branch to a
thin strip. These last conditions are necessary and do not assert exclusion.

The remaining one-double high-C branch has

    1/625 < D <= 5/141, D < 8s^2, d < 0, u < 0,
    q0(t)=(t-B)^2+e > 0, B=1/4-A, e=2s^2-D/4 > 0.

The global angular bound and the complex degree-nine first-power inequality
remain open. Parent review verdicts are not transferred to this contribution.
Prior scopes and exact graph references are in [DEPENDENCIES.json](DEPENDENCIES.json).

## Reproduce

Python3.11+ is sufficient for the standard-library native checker; validation
used Python3.12.14. The separate CAS source requires SymPy1.14.0. Use one serial
CPU child and set all native thread variables to one. From the repository root:

```bash
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1
python3 -I -B round-two/six-sendov-2/outer-real-q0-exclusion/verify.py --expected round-two/six-sendov-2/outer-real-q0-exclusion/EXPECTED.json
python3 -I -B round-two/six-sendov-2/outer-real-q0-exclusion/compare_cas.py --expected round-two/six-sendov-2/outer-real-q0-exclusion/EXPECTED.json
```

Both regenerate every coefficient of the original octic/sextic, all four
critical-quartic Hermite minors, both full Bezout matrices, the entire angular
numerator, cleared outer caps, all final box polynomials and every tensor control.
Expected: **6786 strictly positive controls**, three boxes of tensor degrees
`[12,28,5]`, and complete mathematical record SHA256

    12b0ed927868bc6bb04d9d9cfce17c77089d22af34637a64d7d277936cc64234

The native engine uses integer/Fraction Berkowitz plus binomial clearing and
de Casteljau; the CAS engine uses exact polynomial rings/subset determinants and
direct affine boxes. Shared code handles only serialization and strict coverage.
Neither engine uses predecessor coefficient files, peer/reviewer code or fixtures
as mathematical runtime inputs. The compact expected record is compared only
after the whole calculation.

Optional `--whole /tmp/outer-native.json` writes the complete1643743-byte transient
record outside source. A CAS run with `--check /tmp/outer-native.json` compares
every generated coefficient, not just a summary. The large record is not committed.

For the complete four-replay/seven-fault suite, with a scratch directory outside
this contribution:

```bash
python3 -I -B round-two/six-sendov-2/outer-real-q0-exclusion/validate.py --scratch /tmp/sendov-outer-check --output /tmp/sendov-outer-validation.json
```

If SymPy1.14.0 is in a separate local dependency directory, pass
`--sympy-root PATH`. Each serial child has a fixed45-second guard. No resource
limit is raised. Failure or interruption makes the suite incomplete; it does not
prove mathematical nonexistence. [VALIDATION.json](VALIDATION.json) records the
completed checks and actual resource use.

## Proof boundary

The original-root and grouped-mass licenses, real spectral theorem, Rolle/IVT,
Hermite converse, Bernstein convexity and Descartes arguments are ordinary written
mathematics. Exact same-author arithmetic agreement is not an independent review
or formalization. [LITERATURE.md](LITERATURE.md) records primary scope and prior
credit. [MANIFEST.json](MANIFEST.json) binds the compact files; coordinated
replacement of source, manifest and fixture is outside that hash binding.
