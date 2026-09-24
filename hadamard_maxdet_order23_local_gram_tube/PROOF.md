# Proof of the local Gram exclusion

## 1. Necessary Gram entries

After parity normalization, the row Gram matrix `G` of an order-23 sign
matrix has

\[
G_{ii}=23,\qquad G_{ij}\equiv23\equiv3\pmod4.
\]

If the sign matrix is nonsingular, two rows cannot agree up to sign, so
`|G_ij|<23`.  The complete allowed off-diagonal set is therefore

\[
\{-21,-17,-13,-9,-5,-1,3,7,11,15,19\}.
\tag{1}
\]

Direct multiplication of the published record matrix gives a Gram matrix
`G0` with 208 off-diagonal entries `-1` and 45 entries `3`, and exact Bareiss
elimination gives

\[
\det G_0=L^2,
\qquad L=2779447296000000.
\tag{2}
\]

## 2. Low-rank determinant certificate

The exact inverse reconstructed in both checkers has the form

\[
G_0^{-1}=P/Q,
\qquad Q=170492220,
\tag{3}
\]

where `P` is the integral matrix embedded in `enumerate.cpp`.  Both programs
check `G0 P = Q I` rather than trusting the table.

Let `E=M-G0`, and let `U` be the set of row indices incident with an edited
off-diagonal position.  Write `m=|U|`.  Since `E` is supported on `U x U`,
the matrix determinant lemma gives

\[
\frac{\det M}{\det G_0}
=\det(I+G_0^{-1}E)
=\frac{N}{Q^m},
\quad
N=\det(QI_m+P_{U,U}E_{U,U})\in\mathbb Z.
\tag{4}
\]

Because `det(G0)=L^2` is already a square, `det(M)` can be an integer square
only if the rational number `N/Q^m` is a rational square.  Equivalently,

\[
NQ^m \text{ is an integer square}.
\tag{5}
\]

For every prime `p` not dividing `Q`, condition (5) implies

\[
NQ^m\pmod p
\]

is zero or a quadratic residue.  Thus a single prime for which it is a
nonresidue is an exact nonsquare certificate.

## 3. Exhaustive domains

There are `binom(23,2)=253` off-diagonal positions.  Each entry of `G0` has
ten alternative values in (1).  Hence the arbitrary-edit searches contain

\[
253\cdot10=2530,
\qquad
\binom{253}{2}10^2=3187800
\]

matrices.  The graph-valued neighborhood toggles `-1` and `3`, giving

\[
\binom{253}{3}=2667126
\]

matrices at distance three.  Finally, choosing four of the 45 existing
`3`-edges to delete gives

\[
\binom{45}{4}=148995.
\]

The loops use increasing edge indices, so every matrix occurs exactly once.

For every matrix, `enumerate.cpp` computes (4) modulo each of 48 primes until
it finds the first nonresidue witness.  The program verifies primality by
trial division, checks that no prime divides `Q`, and validates the record
determinant modulo every prime.  It also checks the complete vector of first-
witness counts stored in `certificate.json`; those counts plus the survivor
count equal the domain size in every case.

## 4. Exact survivors

The residue sieve leaves no one-edit or four-deletion matrix.  It leaves 756
two-edit matrices and 24 three-toggle matrices.  `verify.py` applies direct
23-by-23 integer Bareiss elimination to all 780 matrices.  Every survivor
does have square determinant, so the modular sieve loses no further
information.  There are 13 determinant values in the two-edit case and two
in the three-toggle case; `certificate.json` records every value, square
root, and multiplicity.

The largest roots are respectively

\[
2743271424000000<L,
\qquad
2740715520000000<L.
\]

Together with the unedited record matrix, this proves all three parts of the
lemma in `README.md`.
