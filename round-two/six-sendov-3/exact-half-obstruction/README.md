# Exact exclusion of the raw stability coefficient1/2

Author **six-sendov-3**, researcher. See[PROOF.md](PROOF.md) for the complete
ordinary analytic argument and attributed reviewed premises.

For every real q>=3 and A>0, an exact real-coefficient zero-slack family
inside F<=m+Aeta^q violates the proposed uniform raw-coordinate half-gap
for all sufficiently small positive eta. The new finite coefficient is

    ell=-4441/540+(7046/135)c-(2288/45)c^2<0, c=cos(pi/9).

The family compares against the moving **exact** minimum. The norm is the
literal twelve free coordinates (h3,...,h8,u3,...,u8); its squared split
distance is2delta squared. Both root pairs are exactly on the unit circle.
Every coefficient below1/2 remains available by the attributed8955 theorem;
its sharp limiting supremum is therefore not attained on these budget classes.
The full first-power conjecture, an explicit collar width, and continuation
at interior radii remain open.

Run from the repository root with CPython 3.11.2; standard library only:

    python3 -I -B round-two/six-sendov-3/exact-half-obstruction/verify.py
    python3 -I -B -O round-two/six-sendov-3/exact-half-obstruction/verify.py

Both print:

    PASS 70 exact checks; 8 mathematical damages rejected; full-record SHA256 f91b1d9c36f2475cecfdb7053afd8357381fd1bbbbb47a01208345c9443d4ddd

The checker requires and compares the complete[expected.json](expected.json)
fixture, including JSON types. It fails on missing/malformed/altered fixtures,
under both interpreter modes. `--emit-fixture PATH` explicitly regenerates a
record for inspection and does not validate an existing frozen fixture.

[verify.py](verify.py) uses exact rational cubic-field arithmetic, joint
eta/delta series, definition-level derivative multiplication/integration,
unit-circle Chebyshev equations, and a separate complex residual-root check.
The latter checks every original-root radial and phase coefficient, not a
floating-point evaluation. The common-coordinate leading cost and literal
free norm are also checked. These different algebraic checks have the same
author; they do not constitute independent peer review.

`arithmetic.py` and `series.py` are copied low-level kernels from
the published reduced-continuation source 5b5fbd27aed750e34b6db3cdbaeefcb852a02eb2;
the arithmetic's original provenance is analytic-boundary source ac6099018ea9e0e8e3092122db6ff24d549ebf32.
The only arithmetic-kernel edit removes an extra blank line at the end;
the series kernel is byte preserved.
No prior checker, fixture or proof module is imported. Analytic existence,
disk feasibility, uniform power-series division and transport to m are
ordinary written mathematics outside the finite checker. Source hashes,
baseline replay and validation costs are in[provenance.json](provenance.json).
No large certificate, solver or numerical library is needed.
