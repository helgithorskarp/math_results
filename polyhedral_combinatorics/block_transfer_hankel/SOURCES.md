# Sources and attribution boundary

Checked against primary text on 2026-09-22. The proposed contribution is
the explicit full shifted Hankel product for weighted path counts and
its minimal/recoverable transfer description. The abstract matrix and
continued-fraction methods are prior art. Bounded searching did not locate
this exact weighted product; that is not a certified priority result.

1. **Jiang, Yang, Zhong, _Transfer Matrices and Ehrhart Theory for Path
   and Cyclic Block Polytopes_, arXiv:2607.22008v1.**
   [Primary text](https://arxiv.org/html/2607.22008v1).
   Theorems 1.1--1.3 give the height compression, recursive visible
   numerator/denominator, and determinant formula. Lemma 2.3 gives degree
   `q+1`; Corollary 2.4 gives a recurrence, without the present minimality
   conclusion. Problem 3 asks for a compact or orthogonal-polynomial
   description in the length direction. Their visible-fraction convention
   does not assert cancellation actually occurs. Our application proves
   that it never occurs for these positive weights and supplies a finite
   Jacobi description for every width. It does not resolve their separate
   gamma-positivity question or assert a named classical-polynomial form.

2. **Olga Holtz, _The inverse eigenvalue problem for symmetric
   anti-bidiagonal matrices_, Linear Algebra Appl. 408 (2005), 268--274.**
   [Primary preprint](https://arxiv.org/pdf/math/0505095).
   Theorem 1 and its proof identify the anti-bidiagonal/Jacobi equivalence
   and unique inverse realization. Equations (7)--(10), followed by the
   backwards reconstruction on printed pages 4--5, supply the parity and
   three-term inverse method. Our sign convention and endpoint order
   differ. We explicitly transport that classical procedure to the path
   weights; coefficient parity selection also permits field arithmetic
   in characteristic two. We claim no new abstract inverse-spectral
   theorem, anti-bidiagonal normal form, or root-interlacing principle.

3. **Olga Holtz and Mikhail Tyaglov, _Structured matrices, continued
   fractions, and root localization of polynomials_, SIAM Review 54
   (2012), 421--509.**
   [Primary preprint](https://arxiv.org/pdf/0912.4703).
   Section 1.1 discusses finite Hankel rank (including Kronecker's theorem);
   Section 1.4, especially Corollary 1.25 and Theorem 1.26, develops the
   classical Jacobi-fraction/Hankel-product relationship. These general
   mechanisms are credited background, not claimed discoveries here.
   Our proof evaluates the specialized path-count determinant by a direct
   Krylov determinant calculation, then extends its polynomial identity
   to every commutative ring.

4. **Miklos Bona, Hyeong-Kwan Ju, Ruriko Yoshida, _On the Enumeration of
   Certain Weighted Graphs_, Discrete Appl. Math. 155 (2007), 1481--1496.**
   [Primary preprint](https://arxiv.org/pdf/math/0606163).
   Section 2.1, Theorems 2.1--2.2, already gives the unit-layer-weight path
   transfer, its determinant denominator, and continued fractions. Their
   terminology “weighted graph” refers to the integer vertex heights.
   No first transfer-matrix, rationality, or unweighted fraction claim is
   made here. Arbitrary layer multiplicities `w_j` and the specialized
   all-shift Hankel product are the present scope.

The Discovery Net selection used the path-block problem and nearby
unit-weight spectral-to-gamma and fixed-column C-finite results. Those
branches concern different targets; this package concerns exact order
and identifiability of the weighted path counts at fixed dilation.
Independent review of this package is pending.
