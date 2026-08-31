# Eight inequivalent 30-word locating-dominating codes in the binary 7-cube

## Result

Let `Q_7` have vertex set `F_2^7`, and for a code `C` write

\[
I_C(v)=C\cap\bigl(\{v\}\cup\{v+e_i:1\le i\le7\}\bigr).
\]

The eight sets hard-coded in `verify_q7_ld30_eight_orbits.py` are
locating-dominating codes of cardinality 30.  They lie in eight different
orbits under

\[
\operatorname{Aut}(Q_7)=\mathbb F_2^7\rtimes S_7.
\]

Their non-codeword signature-size distributions are pairwise distinct, so
inequivalence follows without a group search:

| code | signature-size distribution | pair distances 1 through 7 | stabilizer | orbit |
|---:|:---|:---|---:|---:|
| 1 | `1:20 2:54 3:18 4:6` | `2 72 158 100 64 39 0` | 2 | 322,560 |
| 2 | `1:20 2:55 3:16 4:7` | `2 73 156 100 66 38 0` | 2 | 322,560 |
| 3 | `1:21 2:49 3:21 4:7` | `0 77 154 98 70 35 1` | 14 | 46,080 |
| 4 | `1:22 2:54 3:15 4:6 5:1` | `3 73 156 98 66 39 0` | 1 | 645,120 |
| 5 | `1:24 2:54 3:12 4:6 5:2` | `4 74 154 97 66 40 0` | 4 | 161,280 |
| 6 | `1:25 2:52 3:12 4:8 5:1` | `4 74 152 98 69 38 0` | 2 | 322,560 |
| 7 | `1:26 2:52 3:8 4:12` | `4 75 148 100 72 36 0` | 4 | 161,280 |
| 8 | `1:28 2:36 3:32 4:2` | `3 72 153 104 67 34 2` | 2 | 322,560 |

Since the eight orbits are disjoint, this also certifies at least

\[
2{,}304{,}000
\]

labelled 30-word locating-dominating codes in `Q_7`.

Codes 2 and 4 belong to the two previously exhibited orbits; the checker
includes explicit cube automorphisms carrying them to those earlier
representatives.  Thus this result raises the known orbit lower bound from
two to eight rather than recounting the earlier two.

## A one-defect bridge

The checker also contains an explicit 29-word set `S` for which the 99
signatures of non-codewords are pairwise distinct, but exactly one signature
is empty, at `0000100`.  Adding any word of the closed ball around `0000100`
therefore gives a 30-word locating-dominating code.  Adding the center gives
signature profile 3 in the table; adding any of its seven neighbors gives
profile 2.  The profile-3 completion is independent as an induced subgraph
and contains one antipodal pair, explaining the zero and one in its
distance-1 and distance-7 entries.

This is a structural construction, not a size-29 locating-dominating code:
the missing domination constraint is essential.

## Exact certificate

Run the standard-library checker:

```bash
python3 verify_q7_ld30_eight_orbits.py
```

For every displayed set, it checks directly that all 98 non-codeword
signatures are nonempty and different.  It recomputes both invariant
distributions and the incidence identity

\[
\sum_{v\notin C}|I_C(v)|+|C|+2e(C)=8|C|.
\]

It then exhausts all `7!` coordinate permutations and the only 30 possible
translations for a stabilizer of a code containing zero.  Orbit sizes follow
from orbit-stabilizer and `|Aut(Q_7)|=128*7!=645120`.  Finally it checks the
one-defect bridge and the two explicit maps to the previous representatives.

The discovery program treats location-domination as an 8,256-clause
fixed-cardinality hitting-set problem.  It is heuristic and is not part of
the certificate:

```bash
g++ -std=c++20 -O3 -Wall -Wextra -pedantic \
  discover_q7_hitting_sets.cpp -o /scratch/discover_q7
/scratch/discover_q7 30 100000 1
```

A deterministic run of seeds 1 through 2,000 found explicit solutions in
all 2,000 cases and yielded the eight invariant profiles above, with no ninth
profile.  This is heuristic evidence only; **no claim is made that there are
exactly eight orbits**.  Codes within one profile could also split into
further orbits.

`explore_q7_ld29_mip.py` preserves the independent exact 0-1 formulation used
to search for a size-29 code.  It requires the pinned exploratory dependency
in `requirements-exploration.txt`; a time-limited run without a solution is
not a nonexistence proof.  No size-29 conclusion is claimed.

## Status and trust boundary

The theorem is a transparent finite result over 128 vertices.  Its trust
boundary is the displayed data, the standard-library Python implementation,
and exhaustive integer/set operations.  Neither the local search, MIP
solver, nor any SAT solver is used to certify correctness or inequivalence.

The certificate was run with Python 3.11.2.  The discovery program was
compiled with GCC 12.2.0.  Source SHA-256 hashes are:

```text
verify_q7_ld30_eight_orbits.py  02f4179224b21c395de3209abccba1a06e73691a28b16e4e30d65c27d6667ff4
discover_q7_hitting_sets.cpp    39ddf40e277ef8bf7a54aadebeefe534bd5ec19c8c894fbb7766dab8548d3c69
explore_q7_ld29_mip.py          3a93b7367dde76958a50c7edc6dfb32c1cf19a8593df2166cf369f9b230bd044
requirements-exploration.txt   ebb8e5f98cc8645b1b56264be490a29f4e36905b32fbb6e1d56f42fdfca1ed8a
```

The result is an apparently new refinement of the newly obtained 30-word
upper bound and the preceding two-orbit result.  It is a lower bound on the
number of orbits, not a classification, and it does not decide whether a code
of size 28 or 29 exists.

Primary background:

- I. Honkala, T. Laihonen, and S. Ranto, "On Locating-Dominating Codes in
  Binary Hamming Spaces," *Discrete Mathematics & Theoretical Computer
  Science* 6(2), 2004, 265--282.
  https://doi.org/10.46298/dmtcs.322
- V. Junnila, T. Laihonen, and T. Lehtila, "Improved Lower Bound for
  Locating-Dominating Codes in Binary Hamming Spaces," *Designs, Codes and
  Cryptography* 90, 2022, 67--85.
  https://doi.org/10.1007/s10623-021-00963-8
