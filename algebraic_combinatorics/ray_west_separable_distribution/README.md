# Algebraic distribution of the Ray--West correction on separable permutations

This directory proves that the Ray--West codimension-two correction has an
explicit bivariate algebraic generating function on the complete class of
separable permutations.  It also derives the exact first-moment generating
function and the asymptotic mean `n/2+O(1)`.

The structural mechanism is local: in the canonical signed Schroeder tree,
the correction counts adjacent decreasing children at direct-sum nodes and
adjacent increasing children at skew-sum nodes.  A two-state transfer matrix
then gives the quadratic equation.

See [THEOREM.md](THEOREM.md) for the statement and proof and [SOURCES.md](SOURCES.md)
for the literature and novelty boundary.

## Reproduction

Python 3.11 or later and only the standard library are required.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py | diff -u EXPECTED_OUTPUT.json -
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
```

The full audit takes roughly half a minute on the publication machine.  It:

- solves the bivariate quadratic through `z^30` using exact coefficient
  polynomials;
- verifies the differentiated first-moment identity through `z^30`;
- enumerates every permutation through length seven;
- identifies the 2,321 separable permutations among them by canonical
  decomposition;
- recomputes their correction independently from the Ray--West active
  two-insertion definition;
- compares the resulting distributions with the algebraic equation.

## Trust boundary

The finite audit depends on the inspected Python source, the Python interpreter,
and hardware.  It is corroborative: the formal-series theorem and asymptotic
statement rest on the proof in `THEOREM.md`.  No generated dataset, solver,
floating-point computation, random choice, or external package is used.

## Scope

This is a distribution theorem for `Av(2413,3142)`.  It does not replace the
general intrinsic rooted-lens formula, solve codimension three, or claim that
the classical signed-Schroeder-tree encoding or Ray--West insertion theory is
new.
