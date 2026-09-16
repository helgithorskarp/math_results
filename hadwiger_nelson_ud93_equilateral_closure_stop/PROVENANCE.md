# Provenance and trust boundary

- Source parametrization: Parcly Taxel, Shibuya repository, commit
  `218097c9971db2b60ab94a0b8dae20d76741cc43`, file
  `shibuya/graphs/pegg.py`, function `ud93_vertices`.
- Exact source used here: the unique root of the four rational quadratic
  equations and rational isolating certificate in this directory.  The proof
  does not import or execute Shibuya.
- Producer: CPython 3.11.2, `mpmath==1.3.0`,
  `python-sat==1.9.dev15`; the positive SAT word is untrusted output.
- Verifier: CPython 3.11 standard library, exact `fractions.Fraction`
  arithmetic.  It regenerates the support and edge set and checks the colour
  word directly.
- Publication repository:
  <https://github.com/helgithorskarp/math_results>.
- Stable directory:
  <https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_ud93_equilateral_closure_stop>.
- Verified mathematical publication commit:
  `9ac74f0c9858aa04d84a72e13f1b903f2dacb978`.

The trust boundary is the written rational arithmetic, the contraction
argument, exhaustive finite loops, CPython, and hardware.  The result is
author-side exact evidence until independently reviewed.
