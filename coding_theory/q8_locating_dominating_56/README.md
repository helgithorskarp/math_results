# A 56-word locating-dominating code in the binary 8-cube

## Result

The following 56 words form a locating-dominating code in `Q_8`:

```text
00000000 00000011 00001111 00010101 00010110 00011001 00011100
00100110 00101001 00101010 00110000 00111011 00111101 01000110
01001011 01001101 01010000 01011010 01011111 01100010 01100100
01100111 01101001 01110001 01110101 01111000 01111110 10000010
10000101 10001000 10001110 10010001 10010100 10011111 10100011
10100101 10101011 10101100 10110010 10110111 10111000 10111111
11000001 11000101 11000111 11001000 11010011 11011010 11011100
11011101 11100000 11101101 11101110 11110000 11110110 11111011
```

Thus

\[
\gamma^{LD}(Q_8)\le 56.
\]

The Honkala--Laihonen--Ranto lower bound specializes to

\[
\left\lceil
\frac{8^2 2^9}{8^3+2\cdot8^2+3\cdot8-2}
\right\rceil
=\left\lceil\frac{16384}{331}\right\rceil=50.
\]

Consequently the certified interval is

\[
50\le\gamma^{LD}(Q_8)\le56.
\]

This improves the graph's preceding 58-word construction and the published
2021/2022 upper bound of 61.

## Direct certificate

For every one of the 200 non-codewords `v`, both checkers independently form

\[
I_C(v)=C\cap N[v].
\]

They verify that all 200 signatures are nonempty and pairwise distinct.  The
signature-size distribution is

```text
size 1: 48
size 2: 95
size 3: 46
size 4:  9
size 5:  2
```

The unordered codeword-pair distance distribution is

```text
distance 1:  13
distance 2: 156
distance 3: 405
distance 4: 399
distance 5: 321
distance 6: 198
distance 7:  44
distance 8:   4
```

The distance counts sum to `1540 = binom(56,2)`.  As a further exact
cross-check, the 422 code/non-code incidences satisfy

\[
422+56+2\cdot13=9\cdot56=504.
\]

## Reproduce

The Python checker uses only the standard library:

```bash
python3 verify_q8_ld56.py
```

Compile and run the independently implemented C++ checker with:

```bash
g++ -std=c++20 -O2 -Wall -Wextra -pedantic \
  verify_q8_ld56.cpp -o /scratch/verify_q8_ld56
/scratch/verify_q8_ld56
```

The C++ checker builds each signature through direct Hamming-distance tests;
the Python checker intersects the code with explicitly generated XOR
neighborhoods.  The trust boundary is complete enumeration of 256 vertices
using exact Python and C++ integer/set operations.  No SAT result, solver
trace, floating-point computation, or external data file is trusted.

The successful runs used Python 3.11.2 and GCC 12.2.0.  Source SHA-256 hashes
are:

```text
verify_q8_ld56.py   ce5535f7868860b5971daf58d30f637b5217cb1e53af8493107538f36c1a647b
verify_q8_ld56.cpp  4295cd9a05888ab17dcb57badea8b74136de91bc9e4a1c599fb5e40e00823782
```

The code was discovered by adapting the fixed-cardinality hitting-set local
search archived with the earlier `Q_7` work.  Searches for size 55 reached
states with one uncovered constraint but produced no code; these heuristic
timeouts establish no lower bound and are not part of the result.

## Status and sources

Targeted primary-source searches through 2026-08-31 found no later published
binary-Hamming-space bound after the 2021/2022 paper.  The explicit 56-word
construction is therefore apparently new to the searched sources; this is
not a priority claim.

- I. Honkala, T. Laihonen, and S. Ranto, "On Locating-Dominating Codes in
  Binary Hamming Spaces," *Discrete Mathematics & Theoretical Computer
  Science* 6(2), 2004, 265--282.
  https://doi.org/10.46298/dmtcs.322
- V. Junnila, T. Laihonen, and T. Lehtila, "Improved Lower Bound for
  Locating-Dominating Codes in Binary Hamming Spaces," *Designs, Codes and
  Cryptography* 90, 2022, 67--85.
  https://doi.org/10.1007/s10623-021-00963-8
