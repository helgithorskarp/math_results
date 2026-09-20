# Independent review: uniform Erdős–Szekeres blow-up obstruction

This directory independently reviews the positive-excess identity and
hereditary witness extraction for Baek–Balko's uniform blow-up construction.

The review's verdict is **accept with high confidence**.  The all-parameter
proof is correct under its stated hypotheses.  In particular, a uniform
blow-up cannot create a counterexample at the first polygon size where the
Erdős–Szekeres bound fails.  This does not address arbitrary nonuniform
blow-ups or solve the general conjecture.

See [`REVIEW.md`](REVIEW.md) for the human premise audit, primary-source check,
adversarial cases, and limitations.

## Reproduce

Python 3.11 or later is sufficient; there are no third-party dependencies.

```sh
python3 audit.py
```

The first line must be:

```text
PASS: independent audit matches expected.json
```

Use `python3 audit.py --emit` to recompute the summary without comparing it.

The checker imports no target code, fixtures, or certificates.  It compares
the complete affine coefficient vectors of the excess identity, counts the
binary suffix partition with a finite-state dynamic program, exhausts a box of
formal profiles, and checks all general-position permutation diagrams through
seven points using a Carathéodory containment test rather than a hull routine.
The finite computation corroborates the proof; it does not replace the
all-parameter summation and extraction arguments.
