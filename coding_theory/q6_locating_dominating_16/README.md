# A 16-word locating-dominating code in the binary 6-cube

This directory gives two solver-free verifiers for the construction

\[
C=\{(x_1,\ldots,x_6)\in\mathbb F_2^6:
x_2=x_1+x_4+x_5+x_6,\quad
x_3=x_1+x_4+x_6+x_1x_5+x_1x_6\}.
\]

All operations in the displayed definition are in `F_2`.  Equivalently, in
lexicographic binary notation the code is

```text
000000 000101 001011 001110 010010 010111 011001 011100
100010 100100 101001 101111 110011 110101 111000 111110
```

Both programs independently construct the closed neighborhoods in `Q_6`,
check that every non-codeword has a nonempty signature, and check that all 48
non-codeword signatures are distinct.  They also check the published lower
bound

\[
\gamma^{LD}(Q_n)\ge
\frac{n^2 2^{n+1}}{n^3+2n^2+3n-2},
\]

whose ceiling at `n=6` is 16.  The construction and lower bound together give
`gamma^LD(Q_6) = 16`.

## Reproduce

Python 3.11 or later, using only the standard library:

```bash
python3 verify_q6_ld16.py
python3 verify_q6_ld16.py --show-signatures
```

C++17 or later, also using only the standard library:

```bash
g++ -std=c++17 -O2 -Wall -Wextra -pedantic \
  verify_q6_ld16.cpp -o /scratch/verify_q6_ld16
/scratch/verify_q6_ld16
```

Expected summary from either implementation:

```text
code size: 16
non-codeword signatures: 48 distinct, 0 empty
signature-size distribution: 1:16 2:16 3:16
published lower-bound ceiling at n=6: 16
verified: gamma^LD(Q_6) = 16
```

## Trust boundary

The upper bound is a direct enumeration of 64 vertices and does not use an
optimizer or SAT solver.  The lower bound is the theorem of Honkala, Laihonen,
and Ranto, *On Locating-Dominating Codes in Binary Hamming Spaces*, DMTCS 6(2)
(2004), 265--282, DOI
[`10.46298/dmtcs.322`](https://doi.org/10.46298/dmtcs.322).  The programs check
only its arithmetic specialization at `n=6`, not the published proof of the
general theorem.
