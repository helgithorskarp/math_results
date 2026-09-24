# Proof of the local Gram classification

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
\binom{253}{3}=2667126,
\qquad
\binom{253}{4}=166695375
\]

matrices at distances three and four.  As an auxiliary overlapping control,
choosing four of the 45 existing `3`-edges to delete gives

\[
\binom{45}{4}=148995.
\]

Within each domain the loops use increasing edge indices, so every matrix
occurs exactly once.

For every matrix, `enumerate.cpp` computes (4) modulo each of 48 primes until
it finds the first nonresidue witness.  The program verifies primality by
trial division, checks that no prime divides `Q`, and validates the record
determinant modulo every prime.  It also checks the complete vector of first-
witness counts stored in `certificate.json`; those counts plus the survivor
count equal the domain size in every case.

## 4. Exact survivors and equality classification

The residue sieve leaves no one-edit or four-deletion matrix.  It leaves 756
two-edit matrices, 24 three-toggle matrices, and 372 four-toggle matrices.
`verify.py` applies direct 23-by-23 integer Bareiss elimination to all 1,152
matrices.  Every survivor does have square determinant, so the modular sieve
loses no further information.  There are 13 determinant values in the
two-edit case, two in the three-toggle case, and five in the four-toggle
case; `certificate.json` records every value, square root, and multiplicity.

The largest roots are respectively

\[
2743271424000000<L,
\qquad
2740715520000000<L.
\]

Among the four-toggle survivors, 360 have root at most

\[
2760297676800000<L.
\]

The remaining twelve have root exactly `L`.  The `3`-edge graph of `G0`
contains the three blocks

\[
\{3,4\mid5,6\},\qquad
\{7,8\mid9,10\},\qquad
\{11,12\mid13,14\}.
\tag{6}
\]

Within each block all four vertices form a clique.  The two vertices to the
right have the same two neighbors in the core triangle, while the two on the
left have neither core neighbor.  Transposing one left vertex with one right
vertex therefore removes two core edges and adds two core edges, changing
exactly four Gram entries.  There are `3*2*2=12` such transpositions, and
simultaneously applying one to the rows and columns gives

\[
M=\Pi G_0\Pi^T=(\Pi R_0)(\Pi R_0)^T.
\tag{7}
\]

The Python checker constructs the edit set of every transposition in (6)
directly from `G0` and verifies that these are exactly the twelve survivors
with root `L`.  Hence every graph-valued square determinant at least `L^2`
through distance four is permutation-congruent to `G0`.  Together with the
arbitrary-entry searches at distances one and two, this proves the lemma in
`README.md`.
