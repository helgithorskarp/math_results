# Two inequivalent 30-word locating-dominating codes in Q7

## Result

There are at least two orbits of cardinality-30 locating-dominating codes in
the binary 7-cube under

\[
\operatorname{Aut}(Q_7)=\mathbb F_2^7\rtimes S_7.
\]

The first code is the previously published 30-word construction.  A second
code is

```text
0000000 0000011 0001101 0001110 0010100 0010111 0011000 0100111
0101000 0101010 0101100 0110001 0110010 0111011 0111110 1000010
1000101 1001001 1001100 1010001 1010110 1011010 1011111 1100001
1100110 1101111 1110011 1110100 1111000 1111101
```

Direct enumeration verifies that its 98 non-codeword signatures are
nonempty and pairwise distinct.

## Solver-free inequivalence certificate

The two signature-size distributions are

```text
published code A: 1:22  2:54  3:15  4:6  5:1
new code B:       1:20  2:55  3:16  4:7
```

Every cube automorphism preserves signature cardinalities, so these different
distributions already prove that the codes are inequivalent.  As an
independent invariant, their unordered codeword-pair distance distributions
also differ:

```text
distance: 1   2    3    4    5   6
code A:   3  73  156   98   66  39
code B:   2  73  156  100   66  38
```

Complete automorphism enumeration finds no map from `A` to `B`.  Code `A`
has trivial stabilizer, hence an orbit of size 645,120.  Code `B` has
stabilizer order 2, hence an orbit of size 322,560.  Its nonidentity
stabilizer element has source-to-destination bit permutation

```text
(0,2,1,6,5,4,3)
```

and translation `1111000`.

## Reproduce

The certificate uses only Python's standard library:

```bash
python3 verify_q7_ld30_two_orbits.py
```

It directly checks both codes, computes both invariant distributions, and
exhaustively enumerates all possible coordinate permutations and all
translations that can map one displayed zero-containing code to the other.

## Status and trust boundary

The second code was discovered by SAT, but SAT is not in the result's trust
boundary.  Correctness and inequivalence reduce to complete enumeration over
128 vertices and finite Python integer/set operations.  This is a lower
bound of two on the number of size-30 orbits, not a complete classification;
additional orbits may exist.  It is an apparently new refinement of the new
30-word upper bound and a first exact step toward classifying its solutions.

## Sources

- I. Honkala, T. Laihonen, and S. Ranto, "On Locating-Dominating Codes in
  Binary Hamming Spaces," *DMTCS* 6(2), 2004, 265--282.
  https://doi.org/10.46298/dmtcs.322
- V. Junnila, T. Laihonen, and T. Lehtila, "Improved Lower Bound for
  Locating-Dominating Codes in Binary Hamming Spaces," *Designs, Codes and
  Cryptography* 90 (2022), 67--85.
  https://doi.org/10.1007/s10623-021-00963-8
