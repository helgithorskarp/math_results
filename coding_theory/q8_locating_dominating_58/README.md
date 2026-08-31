# A 58-word locating-dominating code in the binary 8-cube

## Result

The following 58 words form a locating-dominating code in `Q_8`:

```text
00000000 00000001 00000110 00000111 00010100 00011010 00011011 00011100
00011101 00101000 00101110 00101111 00110000 00110001 01001110
01001111 01010000 01010001 01010100 01010101 01011000 01011001 01100010
01100011 01100100 01100101 01110110 01110111 01111001 01111100 01111101 10000101
10001010 10001011 10010010 10010011 10011000 10011001 10100010 10100011
10101100 10101101 10110101 10111110 10111111 11000010 11000011 11001100
11001101 11011110 11011111 11100110 11100111 11101000 11110000
11110001 11111010 11111011
```

Thus

\[
\gamma^{LD}(Q_8)\le 58.
\]

The Honkala--Laihonen--Ranto lower bound specializes to

\[
\left\lceil
\frac{8^2 2^9}{8^3+2\cdot8^2+3\cdot8-2}
\right\rceil
=\left\lceil\frac{16384}{331}\right\rceil=50.
\]

Consequently the new interval is

\[
50\le\gamma^{LD}(Q_8)\le58.
\]

Junnila--Laihonen--Lehtila (2021/2022) listed the previous published interval
as 50--61.  A 60-word product lift of a recently found 30-word `Q_7` code
first improves 61 to 60.  The displayed construction is obtained from the
two-layer lift of code B in `../q7_ld30_two_orbits` by deleting `00101001`,
`10000100`, `10110100`, and `11101001`, then adding `00010100` and
`01111001`.  Two exhaustive two-for-one exchange searches discovered these
modifications; the searches are not part of the proof.

## Direct certificate

For each of the 198 non-codewords `v`, both checkers independently form

\[
I_C(v)=C\cap N[v].
\]

They verify that all 198 signatures are nonempty and pairwise distinct.  The
signature-size distribution is

```text
size 1:  56
size 2: 102
size 3:  24
size 4:  16
```

The unordered codeword-pair distance distribution is

```text
distance 1:  34
distance 2: 144
distance 3: 428
distance 4: 470
distance 5: 305
distance 6: 198
distance 7:  74
```

## Reproduce

The Python checker uses only the standard library:

```bash
python3 verify_q8_ld58.py
```

Compile and run the independently implemented C++ checker with:

```bash
g++ -std=c++20 -O2 -Wall -Wextra -pedantic verify_q8_ld58.cpp -o /scratch/verify_q8_ld58
/scratch/verify_q8_ld58
```

The trust boundary is complete enumeration of 256 vertices using exact
integer and set operations in Python 3.11.2 and GCC 12.2.0.  No SAT result,
solver trace, floating-point computation, or external data file is trusted.

## Status and sources

Targeted title/concept searches in Crossref and OpenAlex through 2026-08-31
found no later binary-Hamming-space upper bound after the 2021 paper.  The
58-word construction is therefore apparently new to the searched sources;
this negative search is not proof of priority.

- I. Honkala, T. Laihonen, and S. Ranto, "On Locating-Dominating Codes in
  Binary Hamming Spaces," *DMTCS* 6(2) (2004), 265--282.
  https://doi.org/10.46298/dmtcs.322
- V. Junnila, T. Laihonen, and T. Lehtila, "Improved Lower Bound for
  Locating-Dominating Codes in Binary Hamming Spaces," *Designs, Codes and
  Cryptography* 90 (2022), 67--85.
  https://doi.org/10.1007/s10623-021-00963-8
