# A binary quadratic criterion for exponent-four Ehrhart parity

At a minimum-codimension face whose affine span misses the lattice in a
half-integral polytope, the active cokernel is strongly constrained when
the face is locally simple. If its exponent divides four, it must be `C2` or
`C4 x C2^s`. Multiple independent `C4` factors cannot occur there.

For the surviving exponent-four class, the local parity jump is

    Delta = 2^(-g) sum_{z in D} (-1)^Q(z),

where `D` is an explicit even binary code and `Q` is its weight-halving
quadratic form with the column signs included. This gives a complete test:

- A radical word with `Q=1` certifies that the jump is zero.
- Otherwise a symplectic basis gives its exact magnitude and Arf sign.

The criterion uses binary linear algebra, replacing an exponentially large
character sum. A canonical simplex realizes every allowed profile; for
these simplices it decides exactly whether period two collapses to one.
For general polytopes the local jumps assemble into the leading possible
parity coefficient. Cancellation there need not eliminate lower variation.

[PROOF.md](PROOF.md) gives the group obstruction, geometric quotient and
face argument, exact normalization, and realization theorem.
[SOURCES.md](SOURCES.md) credits the cyclic predecessor and classical
Fourier, quadratic-form, and local Euler--Maclaurin machinery. Priority is
only assessed relative to a bounded literature search. The result does not
classify nonsimple faces or arbitrary period collapse.

[arf.py](arf.py) produces kernel, radical, and symplectic certificates from
a supplied coordinate profile in `C4 x F2^s`. It does not enumerate faces
or verify geometric hypotheses of arbitrary input polytopes. Example:

```python
from arf import analyze
print(analyze(1, [(1, 0), (1, 0), (1, 1)]))
```

The returned jump is `[0, 1]`, with cancellation word `3` (binary `011`).
Bit `j` denotes column `j`, starting at zero; columns `(2,0)` are removed
before binary words are encoded. `s` is the number of elementary factors;
each second coordinate is an integer bit mask of length `s`.

Run with Python 3.11+, standard library only, from this directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
PYTHONDONTWRITEBYTECODE=1 python3 -O verify.py
sha256sum -c SHA256SUMS
```

Both runs reproduce [expected.json](expected.json). The audit checks
24,272 generating profiles against literal character sums and independent
codeword enumeration; 5,917 nongenerating profiles and ten malformed inputs
are rejected. It checks 115 group/involution pairs, ten simplex lattice
models, 80 unused Ehrhart interpolation values, 40 literal lattice counts,
and 134 changes of coordinate representation. The entrywise digest is
`e8ad4b21c3bbf33a847c8c194a85e73ee3a94513734e876a9d3927354331c459`.

The finite tests corroborate the written universal proof. They are not a
classification inferred from a census. The proof imports Berline--Vergne's
analytic theorem, is unformalized, and has not received independent review.
No floating-point arithmetic, solver, network input, or large artifact is
needed. The audit takes about four seconds in the development environment.
