# Dimension-three Gaussian majorisation: exact certificates and a transport barrier

**The conjecture remains open.** This contribution supplies a complete
finite certificate format for counterexamples and rules out one proposed
transport proof. It does not claim a new Kneser--Poulsen case.

For `f=mu*gamma_s`, `g=T_#mu*gamma_s` in `R^3`, put
`C=(2*pi*s)^(-3/2)`, `d_k=C*integral[(g/C)^k-(f/C)^k]`, and

\[
a_j=\frac{d_{j+2}}{(j+1)(j+2)}.
\]

The [proof](PROOF.md) establishes:

- Majorisation holds exactly when **every** Hankel matrix
  `(a_(i+j))_(i,j=0)^m` is positive semidefinite.
- Every failure for a bounded law has a finite witness with rational
  points, weights and polynomial coefficients. Its gap is a finite
  exponential sum, requiring no spatial quadrature.
- Along the standard six-dimensional contracting lift,
  `a_j=sqrt(j+2)/(4s)*integral u^j d eta` for a specific positive measure
  `eta`. Positivity of `eta` alone does not imply the required matrices
  are positive. The additional geometric condition is isolated explicitly.
- For a symmetric three-atom fold, the common-Gaussian-noise posterior
  coupling fails its sub-bistochastic row condition for **every fixed
  orthogonal alignment**, even arbitrarily close to rigid equality.

These are author-proved reductions and an obstruction, awaiting independent
review. The moment method is an application of classical moment positivity;
the Gaussian replica identity and lift are credited to prior work. The
transport barrier rules out the specified coupling, not other couplings.

The complete covariance-free rigidity proof remains a separate team input:
[source and status](../gaussian_contraction_covariance_free/README.md).
Its new [independent accepting audit](../gaussian_majorisation_bridge_barrier/AUDIT.md)
also obtains an unsigned hinge bound. Neither result closes the
matrix-positivity gap above.

## Reproduce

Python 3.11 or later, standard library only. From this directory:

```sh
python3 verify.py --check
python3 -O verify.py --check
python3 certify.py example.json
sha256sum -c SHA256SUMS
```

`verify.py` reproduces [EXPECTED.json](EXPECTED.json). It compares two
different exact Gaussian-replica enumerations, tests an existing rational
negative majorisation example as a **non-Gaussian** control, and certifies
finite instances of the universal transport bound using rational intervals.
The universal statements follow from the written proof, not these examples.

`example.json` is a seven-point coordinate fold with joined affine rank six.
Its supplied polynomial passes; it is **not a counterexample**.

To check a candidate, provide a JSON object with dimension `3`, positive
`variance`, three-coordinate arrays `x` and `y`, positive `weights` of sum
one, and `polynomial_square_root` listing coefficients of `p(t)` in ascending
degree. Use integers or fraction strings, never decimal JSON numbers.
The tested convex energy is `C*U_p(rho/C)`, with `U_p''=p^2` and
`U_p(0)=U_p'(0)=0`.

```sh
python3 certify.py candidate.json --digits 100 --max-states 500000
```

Only `CERTIFIED_COUNTEREXAMPLE` certifies a failure. `NO_NEGATIVE_WITNESS`
means only that this polynomial has nonnegative gap. `INCONCLUSIVE_PRECISION`
does not determine the sign. Invalid contractions are rejected before any
claim is made. The workload guard counts both multinomial expansions at
every required degree; it is a computational limit, not a mathematical
restriction on the certificate theorem.

See [VALIDATION.md](VALIDATION.md) for enclosure rules and trust boundaries,
and [SOURCES.md](SOURCES.md) for literature and team dependencies.
