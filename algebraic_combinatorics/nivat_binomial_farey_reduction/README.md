# Farey-triangle reduction for binary binomial subshifts

Let

\[
f_U=\prod_{u\in U}(1+X^u)\in
\mathbb F_2[X^{\pm1},Y^{\pm1}],
\]

where the finite list `U` consists of nonzero integer vectors and repetitions
are allowed. This note reduces the generalized-Nivat classification of every
such algebraic subshift to one canonical six-dot system.

If the directions in `U` span two dimensions, every case is decided by the
known four-dot theorem and the lattice-index obstruction except

\[
F_\triangle=(1+X)(1+Y)(1+XY).
\]

More precisely, a product not already killed by the obstruction must have
primitive factors, no repeated direction, and determinant one between every
pair of directions. Such directions form a clique in the Farey graph. A
two-dimensional clique has at most three vertices; a two-vertex clique gives
the known four-dot system, while every three-vertex clique is carried by a
unimodular coordinate change to the displayed triangle.

The note also proves directly that every configuration in the triangular
kernel has the form

\[
c(i,j)=A(j)+B(i)+C(j-i)\pmod 2.
\]

Thus the one remaining question is exact: does low complexity with respect to
an arbitrary finite window force a period for every such three-directional
XOR sum?

This is a reduction, not a proof that the triangular system has the
generalized Nivat property and not a result on arbitrary line polynomials.
It does not prove or refute the original rectangular Nivat conjecture.

## Files and reproduction

- [THEOREM.md](THEOREM.md): theorem, proofs, triangular decomposition, and
  scope.
- [SOURCES.md](SOURCES.md): primary literature and novelty boundary.
- [verify.py](verify.py): exact finite audits of the lattice geometry,
  polynomial support, and finite-torus decomposition.
- [test_verify.py](test_verify.py): boundary and rejection tests.
- [expected.json](expected.json): deterministic checker output.
- [SHA256SUMS](SHA256SUMS): manifest for the other six files.

Run with Python 3.11 or later; there are no third-party dependencies:

    python3 verify.py --bound 6 --torus-sizes 3,5,7
    python3 -m unittest -v test_verify.py
    sha256sum -c SHA256SUMS

The finite computations audit the normal form and decomposition on stated
ranges. The universal assertions rest on the written proofs and the cited
four-dot theorem, not on finite enumeration.
