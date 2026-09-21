# Directional rank in the Farey-triangle kernel

This note gives an intrinsic algebraic stratification of the one unresolved
binary binomial-product case from the preceding
[Farey-triangle reduction](../nivat_binomial_farey_reduction/).

Every configuration in that kernel can be written

\[
c(i,j)=A(j)+B(i)+C(j-i)\pmod 2.
\]

Although the triple is not unique, the number of its nonperiodic sequences is
unique.  Call it the **directional rank** `rho(c)`.  The main theorem proves

\[
c\text{ is periodic}\quad\Longleftrightarrow\quad \rho(c)\leq 1.
\]

It also recovers `rho(c)` from the whole Laurent-polynomial annihilator ideal.
If

\[
F=(1+X)(1+Y)(1+XY),
\]

then the greatest common divisor of all nonzero binary annihilators of `c` is,
up to a Laurent monomial,

\[
(1+X)^{\epsilon_A}(1+Y)^{\epsilon_B}
(1+XY)^{\epsilon_C},
\]

where `epsilon_A,epsilon_B,epsilon_C` record whether `A,B,C` are nonperiodic.
Thus a nonperiodic member has exactly two or three mandatory Farey directions
in every annihilator.  This separates the remaining generalized-Nivat problem
into an exact rank-two periodic-mask stratum and a rank-three stratum whose
annihilator ideal has gcd `F`.

This is a structural reduction, not a proof that the triangle kernel has the
generalized Nivat property.  In particular, low complexity has not been ruled
out in either nonperiodic stratum.

## Files and reproduction

- [THEOREM.md](THEOREM.md): statements and self-contained proofs.
- [SOURCES.md](SOURCES.md): primary literature and novelty boundary.
- [verify.py](verify.py): exact finite cyclic audits of the gauge and period
  criteria, plus direct checks of the factor-avoiding annihilators.
- [test_verify.py](test_verify.py): boundary and regression tests.
- [expected.json](expected.json): deterministic checker output.
- [SHA256SUMS](SHA256SUMS): manifest for the other six files.

Run with Python 3.11 or later; no third-party packages are needed:

```text
python3 verify.py
python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
```

The computations audit finite cyclic instances of the formulas.  The
bi-infinite theorem rests on the written proof, not on enumeration.
