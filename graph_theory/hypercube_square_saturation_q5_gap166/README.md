# A 166-unit Q5 facet-deficit gap for square saturation

## Result

Let `Q_d` be the `d`-dimensional hypercube and let `sat(Q_d,Q_2)` be the
minimum number of edges in a square-free spanning subgraph that becomes
non-square-free when any omitted cube edge is added.  For every integer
`d >= 5`,

```text
sat(Q_d,Q_2) >= 19992 d 2^d / (11005d + 28979).    (1)
```

Consequently

```text
liminf_(d->infinity) sat(Q_d,Q_2)/2^d >= 19992/11005.
```

At `d=7`, (1) still gives the integer lower bound 169.  At `d=8` it gives
350, improving the preceding integer consequence from 349.  Relative to the
previous `204d2^d/(113d+295)` theorem, direct cross-multiplication leaves
`14076(d-1)>0`.

The result is a lower-bound theorem.  It does not determine an exact
hypercube saturation number.

## Local setup

For a square-free edge pattern in `Q_3`, write

```text
sigma = b + 2q - t/2 >= 0,
```

where `t` counts square faces with three selected edges, `q` counts repeated
missing-edge witnesses, and `b` counts selected-edge incidences on the other
square faces.

For a square-free edge set in `H=Q_4`, let `E_H` be its edge count and let
`S_H` sum `sigma` over the eight `Q_3` facets.  Define

```text
delta_H = 17 S_H - 3 E_H.
```

For a square-free edge set in `K=Q_5`, summing over its ten `Q_4` facets gives

```text
Delta_K := 34 S_K - 12 E_K = sum_(H facet of K) delta_H.    (2)
```

The previous source package proved only `Delta_K>=28`.  The new theorem is

```text
Delta_K >= 166                                             (3)
```

for every nonempty square-free edge set in `Q_5`.

## Complete Q4 cutoff

Every square-free `Q_4` has at most 24 edges: each of its 24 squares must
omit an edge, while each omitted edge lies in three squares.  Hence

```text
delta_H < 166  implies  17S_H - 72 < 166  implies  S_H <= 13.   (4)
```

The production verifier enumerates all 4,096 labeled edge patterns in each
`Q_3` facet, checks `sigma>=0` directly, and glues complete restrictions over
the eight facets of `Q_4`.  There are exactly 92,993 labeled square-free
patterns with `S_H<=13`.  Direct recomputation of every square, witness
multiplicity, and slack agrees for every one of them.  The census proves
`delta_H>=0` and supplies all positive deficit classes below 166.

The independent checker instead assigns the 32 global endpoint-pair edges
one at a time, retaining complete local candidate sets and pruning only from
their minimum remaining costs.  It recovers exactly the same 92,993 masks.
Their common normalized graph-set SHA-256 is

```text
c5b51fe95ded5988f87006471a4edad6ec3f92130e85cae746f54f7a94ef053a
```

This is entry-level agreement, not merely agreement on class counts.  Their
independently derived 87-row boundary-profile table also has common SHA-256
`a4bd025cc1e9df09198946816b174d0cf1cbf2073860ec74d6956081000464ad`.

## Boundary badness and profile compression

There are 64 nonempty zero-deficit `Q_4` patterns, all with `(E_H,S_H)=(17,3)`
and forming one cube-automorphism orbit.  Call a labeled `Q_3` restriction
*extendable* if it occurs as a facet of one of these 64 patterns.  For a
positive-deficit `Q_4` pattern `H`, let `b(H)` count its eight facets whose
exact restrictions are not extendable, and let `e_0(H)` count its empty
facets.

Suppose a putative `Q_5` pattern has `p` positive-deficit facets, `z` empty
facets, and `k` nonempty zero-deficit facets.  Three necessary conditions
compress the complete finite problem:

1. Every edge lies in four `Q_4` facets, so
   `sum E_H = 4E_K`.
2. If `l=p+k` facets are live, the maximum number of `Q_5` edges supported
   by their intersection pattern is, for `l=1,...,10`,

   ```text
   0, 0, 0, 1, 5, 9, 16, 28, 48, 80.
   ```

3. Every bad boundary of a positive facet must meet another positive or
   empty facet.  There are at most `p+z-1` such other facets, so necessarily
   `b(H)<=p+z-1` for every positive `H`.  Counting an opposite facet as
   available only weakens this condition, and is therefore safe.

Also, `Delta_K` is even.  Applying these filters to all 87 computed positive
profile classes below 166 leaves exactly four rows:

| `Delta_K` | positive classes `(delta,E,b,e_0)` | `k` | `z` | `E_K` |
|---:|---|---:|---:|---:|
| 42 | `(42,20,0,0)` | 8 | 1 | 39 |
| 84 | `(42,20,0,0)` twice | 8 | 0 | 44 |
| 132 | `(42,20,0,0)` twice; `(48,18,3,0)` | 6 | 1 | 40 |
| 144 | `(48,18,3,0)` three times | 6 | 1 | 39 |

The zero-total case is impossible separately.  If `k` live facets all had
zero deficit, then `17k=4E_K`, forcing `k=4` or 8.  Those live-facet sets
support at most 1 or 28 edges, respectively, instead of the required 17 or
34.

## Exact closure of the four residual rows

The 32 patterns of class `(42,20,0,0)` form one `Aut(Q_4)` orbit, represented
by `0x18bb77ee`.  The 192 patterns of class `(48,18,3,0)` also form one orbit,
represented by `0x07ff2336`.  The equality orbit is represented by
`0x07ff2332`.

By facet transitivity and these orbit classifications, fix the distinguished
positive facet and its representative.  The verifier then tries every
placement of the remaining exceptional facets and every labeled candidate in
the required orbits, requiring exact agreement on every shared `Q_3` edge
set.  The complete results are:

| total | labeled placements | search nodes | maximum depth | solutions |
|---:|---:|---:|---:|---:|
| 42 | 9 | 10 | 1 | 0 |
| 84 | 9 | 18 | 1 | 0 |
| 132 | 252 | 252 | 0 | 0 |
| 144 | 252 | 252 | 0 | 0 |

Thus neither zero nor any positive even total below 166 is realizable, which
proves (3).  The shallow searches reflect a genuine boundary obstruction:
the candidate rows fail on one or two adjacent facet restrictions, not after
a large opaque search.

The independent checker closes the same residual rows by propagating values
on all 80 global `Q_5` edges rather than assigning whole facets.

## Global lower bound

Import the published exact value `ex(Q_5,C_4)=56`.  From (2) and (3), every
nonempty square-free edge set in `Q_5` satisfies

```text
S_K >= (12E_K+166)/34 >= (419/952) E_K.            (5)
```

The last inequality also holds for the empty set.  Each `Q_3` in `Q_d` lies
in `binom(d-3,2)` five-subcubes and each edge lies in `binom(d-1,4)`, so
summing (5) yields

```text
S >= 419 E(d-1)(d-2)/11424.                        (6)
```

For a square-saturated graph put `N=d2^(d-1)`, `E=|E(G)|`, and `M=N-E`.
The established active-square identities are

```text
B+3A = (d-1)E - 3M,
B+3A >= M/2 + S/(d-2).
```

Substitution of (6) gives

```text
11005(d-1)E >= 39984M.
```

Replacing `M` by `d2^(d-1)-E` proves

```text
(11005d+28979)E >= 19992d2^d,
```

which is (1).

## Reproduction

Python 3.11 or later is sufficient; no third-party package, solver, network,
or external data file is used.

```bash
cd graph_theory/hypercube_square_saturation_q5_gap166

PYTHONDONTWRITEBYTECODE=1 python3 verify.py > /tmp/q5-gap166.out
diff -u EXPECTED_OUTPUT.txt /tmp/q5-gap166.out

PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py > /tmp/q5-gap166-independent.out
diff -u EXPECTED_INDEPENDENT_OUTPUT.txt /tmp/q5-gap166-independent.out

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
```

On the publication host, the production verifier takes under one minute.
The deliberately different edge-by-edge checker takes about four minutes.
Times are measurements, not proof outputs.

## Dependencies, literature, and scope

Relevant committed Discovery Net nodes:

- `bafkreigkl27efnd3pt7fkz3igzslgxevezlbxkp7qorifc4cekw6ol3kgm`
  — hypercube subcube saturation problem.
- `bafkreih2tqokgawtue33oce4smzwcbba36as2qnjwoskwbzu7am4b2mamy`
  — exact positive `Q_4` slack review and global identities.
- `bafkreidb54nb5k4abxrunvu4k72hhk3ynch5helu7stxmtalhf4tqbmxj4`
  — sharp `Q_4` facet-slack ratio.
- `bafkreiayhj4iizyrzl7gwtwdxqvhwooffg3ph54afqfmwymqehktnyjyeu`
  — preceding `Q_5` compatibility theorem.
- `bafkreiel3tcy76f7pzrv3b2vsghiakvtaqqjm46ecphwnrvfa3vc5rykhy`
  — later `Q_6` modular bound now superseded globally.

Primary context checked on 2026-09-19:

- Johnson and Pinto, [*Saturated Subgraphs of the Hypercube*](https://arxiv.org/abs/1406.1766), define the parameter and establish the earlier constant-order framework.
- Morrison, Noel, and Scott, [*Saturation in the Hypercube and Bootstrap Percolation*](https://arxiv.org/abs/1408.5488), prove `Theta(2^d)` for every fixed forbidden subcube.
- Dejter, Emamy-K, and Guan, [*On the fault tolerance in a 5-cube*](https://www.researchgate.net/publication/265697468_On_the_fault_tolerance_in_a_5-cube), supply the imported exact value `ex(Q_5,C_4)=56`; the linked copy is author-uploaded.

Focused searches found no published 166-unit facet gap or `19992/11005`
lower constant.  This supports “apparently new to the searched sources,” not
a historical-priority claim.

The finite local theorem is exact computer-assisted mathematics.  Its trust
boundary is readable CPython integer, set, tuple, hash, and bit-operation
semantics plus the written completeness and symmetry reductions.  The
all-dimensional theorem additionally trusts the displayed human incidence
argument and the imported `ex(Q_5,C_4)=56` theorem.  The computation does not
reprove that external extremal value, formalize the universal double counts,
determine exact saturation numbers, or prove that the Q5 deficit lower bound
166 is attained.
