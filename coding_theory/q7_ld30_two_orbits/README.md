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

The PySAT discovery program is also preserved, but is not part of the direct
certificate's trust boundary:

```bash
python3 -m venv /scratch/q7-ld-search-venv
/scratch/q7-ld-search-venv/bin/pip install -r requirements.txt
/scratch/q7-ld-search-venv/bin/python search_q7_ld.py 30 \
  --solver cadical195 --zero-degree 0
```

Any generated CNF or solver output should remain under `/scratch`.

For a complete search at bound 29, it is enough to run `--zero-degree` for
the four values `0,1,2,3`.  Indeed, if a dominating code `C` in `Q_n` has
size `K` and `e(C)` induced edges, double-counting closed-neighborhood
incidences gives

\[
2e(C)\le (n+1)K-2^n.
\]

Consequently

\[
\delta(Q_n[C])\le
\left\lfloor n+1-\frac{2^n}{K}\right\rfloor.
\]

At `n=7` and `K<=29` this is at most 3.  Translate a minimum-degree
codeword to zero, then permute coordinates to make its codeword neighbors
the first `r` unit vectors.  The four `--zero-degree r` instances therefore
cover every possible code of size at most 29.  Initial 15-minute CaDiCaL
runs of all four cases timed out; this is search status only, not evidence of
nonexistence.

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
