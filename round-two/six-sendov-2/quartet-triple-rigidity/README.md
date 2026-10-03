# Positive quartet structure for the degree-nine angular frontier

Actual **six-sendov-2**, role **researcher**,2026-10-03. Complete ordinary
author proof, unformalized and independently unreviewed.

[PROOF.md](PROOF.md) proves rigidity of a triple positive quartet with its
first/third/fifth powers fixed, covers every zero boundary, excludes all
original triples from competitive two-odd-moment-zero angular profiles, and
gives a feasible positive-root quartic interval and actual symmetric midpoint.
Competitive constrained local maxima retain only one, two or three doubles.
The actual first-power problem and angular monotonicity remain open.

From the repository root, Python3.10+ standard library:

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B round-two/six-sendov-2/quartet-triple-rigidity/verify.py --self-test
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B -O round-two/six-sendov-2/quartet-triple-rigidity/verify.py --self-test

The checker compares the complete typed/canonical [expected.json](expected.json)
record. Expected output: PASS, two complete equal-support zero openings,
twelve whole positive Bernstein polynomials, nine normalized octic coefficients,
two different actually positive quartet controls and five semantic rejections.
The whole record SHA256 is
`5192c8fe5d77ae76a6fec1efff4b9aee715a6f442500266e95410066ec47524b`.

An optional corroboration, with **SymPy1.14.0** already available:

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B round-two/six-sendov-2/quartet-triple-rigidity/compare_cas.py

This separately encoded dense CAS route imports no native arithmetic,
reconstructs Bernstein vectors by exact interpolation, and compares the
entire record and bytes. It is same-author corroboration, not independent
review. No CAS is needed for the standalone checker.

External compact fixtures can be supplied with `--expected PATH`. Generation
with `--write-record PATH` rebuilds all exact identities before writing; it
does not independently prove the surrounding universal argument. Explicit
exceptions enforce all checks even under Python optimization.

The record uses arbitrary-precision rational coefficient maps with ordered
variables, complete Laurent terms, rational numerator/denominator polynomials,
and both coefficients in QQ[sqrt57]. Negative exponents only clear the known
nonzero S or the symbolic x factor in a polynomial identity. All zero-root,
rank-deficient and equality bridges are explained in the ordinary proof.
There is no numerical search, floating predicate, optimizer, external proof
corpus, solver timeout or incomplete enumeration premise.

Validation used Python3.12.14, unchanged1CPU2GiB, one serial child and all
six native thread variables one, with45s child/50s outer guards. Local/cold
normal/optimized checks and malformed/semantic fixtures were retained privately;
the compact public record and all source are sufficient to reproduce the
finite arithmetic. [LITERATURE.md](LITERATURE.md) names exact mathematical
dependencies and their trust boundaries. Angular comparison along the actual
pencil interval is the concrete next frontier.
