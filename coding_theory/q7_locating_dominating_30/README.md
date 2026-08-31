# A 30-word locating-dominating code in the binary 7-cube

## Result

The following set is a locating-dominating code in `Q_7`:

```text
0000000 0000110 0001011 0010011 0010101 0011010 0011101 0100010
0100101 0101000 0101111 0110000 0110111 0111001 0111100 1000010
1000111 1001001 1001100 1010101 1010110 1011000 1011111 1100001
1100100 1101011 1101110 1110111 1111010 1111101
```

Thus

\[
\gamma^{LD}(Q_7)\le 30,
\]

improving the previously published upper bound 32.  The general lower bound
of Honkala--Laihonen--Ranto specializes to

\[
\gamma^{LD}(Q_7)\ge
\left\lceil\frac{7^2 2^8}{7^3+2\cdot7^2+3\cdot7-2}\right\rceil
=\left\lceil\frac{3136}{115}\right\rceil=28.
\]

The resulting current interval is therefore

\[
\boxed{28\le\gamma^{LD}(Q_7)\le30}.
\]

## Direct certificate

For each of the 98 non-codewords, the programs construct the closed
radius-one neighborhood and its intersection with the displayed code.  All
98 signatures are nonempty and pairwise distinct.  Their cardinality
distribution is

```text
size 1: 22
size 2: 54
size 3: 15
size 4:  6
size 5:  1
```

The unordered codeword-pair distance distribution is

```text
distance 1:   3
distance 2:  73
distance 3: 156
distance 4:  98
distance 5:  66
distance 6:  39
```

## Reproduce

The Python checker uses only the standard library:

```bash
python3 verify_q7_ld30.py
```

The independent C++17 checker can be compiled outside the repository:

```bash
g++ -std=c++17 -O2 -Wall -Wextra -pedantic \
  verify_q7_ld30.cpp -o /scratch/verify_q7_ld30
/scratch/verify_q7_ld30
```

Both print the same certificate summary and the interval `28 <= gamma^LD(Q_7) <= 30`.

## Discovery and scope

The starting size-32 code was the two-layer lift of the newly found optimum
`Q_6` code.  A SAT encoding produced a 31-word code; a checked two-for-one
exchange then produced the displayed 30-word code.  A finite search found no
code of size at most 29 within symmetric-difference distance 9 of this
witness.  This last local negative result is only search guidance: no global
size-29 nonexistence claim is made.

Junnila--Laihonen--Lehtila reported the interval `28--32` in 2021.  Targeted
searches through 2026-08-31 found no later construction improving 32, so the
30-word construction is **apparently new to the searched sources**.

The upper bound has only the transparent 128-vertex direct-enumeration trust
boundary.  The lower bound relies on the published proof; the checkers verify
only its arithmetic specialization.  The SAT search is provenance, not part
of the certificate.

## Sources

- I. Honkala, T. Laihonen, and S. Ranto, "On Locating-Dominating Codes in
  Binary Hamming Spaces," *DMTCS* 6(2), 2004, 265--282.
  https://doi.org/10.46298/dmtcs.322
- V. Junnila, T. Laihonen, and T. Lehtila, "Improved Lower Bound for
  Locating-Dominating Codes in Binary Hamming Spaces," *Designs, Codes and
  Cryptography* 90 (2022), 67--85.
  https://doi.org/10.1007/s10623-021-00963-8
