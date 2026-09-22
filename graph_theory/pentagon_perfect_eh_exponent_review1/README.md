# Independent review: perfect-or-pentagon product exponent

This directory records an independent review of the theorem in
[`../pentagon_perfect_eh_exponent`](../pentagon_perfect_eh_exponent): for the
substitution-closed class whose outer graphs are perfect graphs or `C5`,

```text
alpha(G) omega(G) >= |V(G)|^(log_5 4),
```

with sharp homogeneous-set exponent `log_5 2`.

The verdict is **accept with high confidence in the stated scope**.  The
reasoning, explicit human premises, completeness reductions, caveats, and
literature boundary are in [`REVIEW.md`](REVIEW.md).

[`independent_check.py`](independent_check.py) is a definition-level exact
checker, deliberately different from the target's active-constraint
enumerator.  It exhausts all labelled graphs through five vertices, all
binary weight pairs on the perfect ones, literal small substitutions, and
the first empty-module/heredity boundaries.  It uses only the Python standard
library and exact integer or `Fraction` arithmetic.

Reproduce with Python 3.11 or later:

```sh
./run_checks.sh
```

Expected runtime is about three seconds on an ordinary workstation.  The
checker is supplementary evidence: it does not reprove Chvatal's
perfect-graph polytope theorem or replace the universal written induction.
