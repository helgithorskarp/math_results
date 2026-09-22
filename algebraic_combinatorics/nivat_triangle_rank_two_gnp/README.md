# Rank-two generalized Nivat theorem for the Farey triangle

For the remaining binary Farey-triangle kernel

```text
F=(1+X)(1+Y)(1+XY),
```

every configuration has a directional decomposition

```text
c(i,j)=A(j)+B(i)+C(j-i) mod 2.
```

This note closes the entire stratum in which exactly two of `A,B,C` are
nonperiodic.  It proves that every such configuration has

```text
P_c(D)>|D|
```

for every finite nonempty window `D`.  Hence a counterexample to the
generalized Nivat property of `ker(F)`, if one exists, must have all three
directional sequences nonperiodic; algebraically, every one of its nonzero
binary annihilators must be divisible by all of `F`.

The bridge is a general periodic-mask principle.  A finite orbit norm turns
any integer annihilator into one supported on a prescribed period lattice.
Consequently pointwise multiplication by a periodic configuration preserves
integer annihilation.  Since binary XOR satisfies

```text
c XOR q = c+q-2cq
```

in the integer lift, XOR by any doubly periodic mask preserves the strong
integer-annihilator rigidity of the unimodular four-dot system.  A periodic
component in the Farey decomposition is exactly such a mask.

## Files and reproduction

- [THEOREM.md](THEOREM.md): orbit-norm lemma and the complete proof.
- [SOURCES.md](SOURCES.md): primary literature and novelty boundary.
- [verify.py](verify.py): exact orbit-norm determinant and finite cyclic
  audits, using only the Python standard library.
- [test_verify.py](test_verify.py): five boundary and regression tests.
- `expected.json`: deterministic checker output.
- `SHA256SUMS`: manifest for the other six files.

Run with Python 3.11 or later:

```text
PYTHONDONTWRITEBYTECODE=1 python3 verify.py > /tmp/nivat-rank-two.json
diff -u expected.json /tmp/nivat-rank-two.json
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
```

The checker constructs orbit norms as determinants of exact integral regular
representations; it does not use floating-point roots of unity or third-party
computer algebra.  The universal theorem rests on the written proof and the
cited four-dot theorem, not on finite enumeration.
