# Exact 7-step domination in four cubic nonabelian Cayley families

## Theorem

Let `G` be one of `A5`, `S5`, `A6`, or `S6`, and let

\[
\Gamma=\operatorname{Cay}(G,X)
\]

be a connected simple undirected cubic Cayley graph.  Thus `X` is an
inverse-closed generating subset of `G`, does not contain the identity, and
has cardinality three.  Then `Gamma` has no exact 7-step dominating set of
cardinality four or six.

This is a finite nonabelian obstruction.  It does not determine Hersh's
`m(7)`, and it makes no claim for other groups, higher Cayley degree, or
non-Cayley graphs.

## Translate reduction

Put

\[
T=\{g\in G:d_\Gamma(1,g)=7\}.
\]

For a center `s`, the vertices at distance seven from it are the left
translate `sT`.  Hence an exact 7-step dominating set `C` is precisely a
partition

\[
G=\bigsqcup_{s\in C}sT.
\]

In particular, `|G|=|C||T|`.  This counting equality eliminates every
connection set except the candidates in the following complete table.

| group | inverse-closed triples | connected | `|C|=4` candidates | `|C|=6` candidates | conjugacy types |
|---|---:|---:|---:|---:|---:|
| `A5` | 785 | 560 | 0 | 60 | 1 |
| `S5` | 3,475 | 1,560 | 0 | 180 | 2 |
| `A6` | 21,255 | 8,640 | 0 | 720 | 1 |
| `S6` | 91,675 | 15,840 | 0 | 0 | 0 |

Conjugacy is allowed by the full symmetric group on the underlying letters.
For `A5` and `A6`, odd conjugators simply give additional automorphisms of
the alternating group.  Thus the 960 surviving labelled connection sets
reduce to four signatures.

## Boundary signatures

Write permutations by their image tuples in `certificates.json`.  In cycle
notation, representatives for the four surviving types are

\[
\begin{array}{c|l}
A_5 & \{(2\,3\,4),(2\,4\,3),(0\,2)(1\,3)\},\\
S_5^{(1)} & \{(3\,4),(1\,2)(3\,4),(0\,3)(2\,4)\},\\
S_5^{(2)} & \{(1\,2)(3\,4),(0\,1)(2\,3\,4),(0\,1)(2\,4\,3)\},\\
A_6 & \{(2\,3)(4\,5),(0\,1\,2\,3\,4),(0\,4\,3\,2\,1)\}.
\end{array}
\]

Set `D=TT^{-1}` and `A=G-D`.  After translating one prospective center to
the identity, every other center must lie in `A`.  Moreover two such shifts
`x,y` give disjoint sphere translates exactly when `x^{-1}y` lies in `A`.
Thus the remaining five shifts required for six centers would form a
5-clique in the compatibility graph on `A`.

| type | `|T|` | diameter | `|D|` | `|A|` | maximum compatibility degree |
|---|---:|---:|---:|---:|---:|
| `A5` | 10 | 10 | 46 | 14 | 2 |
| `S5^(1)` | 20 | 10 | 119 | 1 | 0 |
| `S5^(2)` | 20 | 10 | 109 | 11 | 0 |
| `A6` | 60 | 10 | 360 | 0 | 0 |

A 5-clique has internal degree four, so the displayed degree bounds exclude
all six-center candidates.  Notice that the `A6` signature is especially
rigid: `TT^{-1}=A6`, so no two radius-seven sphere translates are disjoint.

## Completeness of the finite universe

An inverse-closed three-element set has exactly one of two forms:

1. three distinct involutions; or
2. one involution together with one pair `{g,g^{-1}}`, where `g` is not an
   involution.

The verifier enumerates these two families, checks generation by graph BFS,
computes `T`, applies the divisibility equality, and canonicalizes only the
survivors under conjugation.  The independent checker reconstructs the same
universe using sets and frontier expansion, builds the complete conjugacy
orbit of each stored representative rather than taking a canonical minimum,
and verifies that every candidate belongs to exactly one stored orbit.  It
then recomputes the boundary degree certificate.  No SAT, MILP, or opaque
solver certificate is used.

## Reproduction

Only Python 3 and its standard library are required.

```bash
python3 verify.py
python3 independent_check.py
```

The complete run takes seconds on an ordinary workstation.  Compact expected
output is recorded in `EXPECTED_OUTPUT.txt`; the mathematical certificate is
`certificates.json`.

## Literature status and scope

Hersh introduced exact `n`-step domination, proved the general lower bound
`floor(log_2 n)+2`, and posed the associated minimization problem in 1999.
Williams subsequently gave examples for steps four, five, and six with four
centers.  Targeted searches through 2026-09-21 found no primary source
settling `m(7)` or treating the four nonabelian cubic Cayley families above.
The present result should therefore be read as a checked finite obstruction,
not as a solution of the general problem.

- P. Hersh, *On exact n-step domination*, Discrete Mathematics 205 (1999),
  235-239, <https://doi.org/10.1016/S0012-365X(99)00024-2>.
- L. K. Williams, *On exact n-step domination*, Ars Combinatoria 58 (2001),
  13-22, <https://combinatorialpress.com/article/ars/Volume%20058/volume-58-paper-2.pdf>.
