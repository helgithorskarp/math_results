# A 28-unit Q5 facet-deficit gap for square saturation

## Result

Let `Q_d` be the `d`-dimensional hypercube and let
`sat(Q_d,Q_2)` be the minimum number of edges in a square-free spanning
subgraph that becomes non-square-free whenever any omitted cube edge is
added.  For every integer `d >= 5`,

```text
sat(Q_d,Q_2) >= 204 d 2^d / (113d + 295).          (1)
```

Consequently

```text
liminf_(d->infinity) sat(Q_d,Q_2)/2^d >= 204/113.
```

At `d=7`, (1) is `30464/181`, so the integer lower bound is **169**.
The theorem improves the committed `5183640/2874791` asymptotic constant and
its finite formula; direct cross-multiplication leaves
`706044(d-1) > 0` for `d >= 5`.

This is a lower-bound theorem.  It does not determine an exact unrestricted
hypercube saturation number.

## Low-slack Q4 theorem

For a square-free edge set in `Q_3`, write

```text
sigma = b + 2q - t/2,
```

where `t` is the number of square faces with three selected edges, `q` counts
repeated missing-edge witnesses, and `b` counts selected-edge incidences on
the other square faces.  The committed local theorem gives `sigma >= 0`.

For a square-free edge set `F` in `H=Q_4`, let `E_H=|F|` and let `S_H` be the
sum of `sigma` over the eight `Q_3` facets.  Define

```text
delta_H = 17 S_H - 3 E_H.
```

The sharp committed `Q_4` inequality gives `delta_H >= 0`.  The new exact
finite lemma is the strict gap

```text
delta_H = 0  or  delta_H >= 28.                   (2)
```

The value 28 is attained.  The complete low-slack spectrum through `S_H=5`
is

| `E_H` | `S_H` | labeled patterns |
|---:|---:|---:|
| 0 | 0 | 1 |
| 17 | 3 | 64 |
| 19 | 5 | 192 |

There are no patterns with `S_H` equal to 1, 2, or 4.  The 192 patterns in
the last row have deficit 28 and form one orbit under the 384 translations
and coordinate permutations of `Q_4`; their stabilizer has order two.  In the
canonical `(vertex,direction)` edge order used by `verify.py`, one
representative is `0x0fff163c`.

Why the finite cutoff proves (2): every square-free `Q_4` has at most 24
edges, by counting selected-edge incidences over its 24 squares.  Therefore,
if `S_H >= 6`, then

```text
delta_H >= 17*6 - 3*24 = 30.
```

Every possible smaller positive deficit is therefore covered by the complete
`S_H <= 5` census above.  Its only nonempty rows have deficits 0 and 28.

## Lifting the gap to Q5

Let `K=Q_5`, and let `E_K` and `S_K` have the analogous meanings.  Summing
`delta_H` over the ten `Q_4` facets of `K` counts every edge four times and
every `Q_3` twice, so

```text
Delta_K := 34 S_K - 12 E_K = sum_(H facet of K) delta_H.   (3)
```

For nonempty `F`, the sum cannot vanish.  Indeed, a zero-deficit live `Q_4`
facet has `(E_H,S_H)=(17,3)`.  If `k` facets were live, then
`17k=4E_K`, forcing `k=4` or `k=8`.  Four live facets support at most one
`Q_5` edge, not the required 17; eight support at most 28, not the required
34.  The exact support distributions are checked as

```text
k=4: {capacity 0: 130 sets, capacity 1: 80 sets}
k=8: {capacity 16: 5 sets, capacity 28: 40 sets}.
```

Thus at least one summand in (3) is positive.  By (2),

```text
Delta_K >= 28.                                    (4)
```

The previous graph result had only `Delta_K >= 1`.  In particular, (4)
rules out the twelve deficit-one facets required by the sole arithmetic
equality profile in the later `Q_6` modular-gap result.

## Global bound

Import the published exact value `ex(Q_5,C_4)=56`.  From (4), for every
nonempty square-free edge set in `Q_5`,

```text
S_K >= (12E_K+28)/34 >= (25/68) E_K.              (5)
```

The last inequality also holds for the empty set.  Every `Q_3` in `Q_d` lies
in `binom(d-3,2)` five-subcubes and every edge lies in `binom(d-1,4)`, so
summing (5) gives

```text
S >= 25 E (d-1)(d-2) / 816.                       (6)
```

For a square-saturated `G` put `N=d2^(d-1)`, `E=|E(G)|`, and `M=N-E`.
The established active-square identities are

```text
B+3A = (d-1)E - 3M,
B+3A >= M/2 + S/(d-2).
```

Using (6) yields

```text
791(d-1)E >= 2856M.
```

Substitute `M=N-E` and divide by seven to obtain

```text
(113d+295)E >= 204d2^d,
```

which is (1).

## Reproduction

Python 3.11 or later is sufficient; no third-party package, solver, network,
or external data file is used.

```bash
cd graph_theory/hypercube_square_saturation_q5_deficit_gap
PYTHONDONTWRITEBYTECODE=1 python3 verify.py > /tmp/q5-gap.out
diff -u EXPECTED_OUTPUT.txt /tmp/q5-gap.out

PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py > /tmp/q5-gap-independent.out
diff -u EXPECTED_INDEPENDENT_OUTPUT.txt /tmp/q5-gap-independent.out

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
```

On CPython 3.11.2, `verify.py` takes about 1.1 seconds and
`independent_check.py` about 9.6 seconds on the publication host.  Times are
measurements, not proof outputs.

The production verifier exhausts all 4,096 labeled edge subsets in each
`Q_3` facet, retains the 1,273 with `2 sigma <= 10`, and glues compatible
complete facet restrictions.  Nonnegative local slack proves completeness:
every global pattern with `S_H <= 5` has every facet in those retained lists.
It visits 1,033,852 gluing states and then directly recomputes every square,
witness multiplicity, and slack value for all 257 resulting graphs.

The independent checker uses unordered endpoint-pair labels and assigns the
32 global edges one at a time, pruning only when the sum of the eight local
minimum costs exceeds ten.  It visits 88,446 states.  Both implementations
produce exactly the same normalized graph-set SHA-256:

```text
e9e897e7ac97b4fce847acbb395615d3cc1e409dea2ef57148273fd1a1bd1c72
```

This is entry-level agreement on the complete 257-graph set, not merely
agreement on aggregate counts.

## Dependencies, literature, and scope

Graph dependencies and the opportunity being closed:

- `bafkreigkl27efnd3pt7fkz3igzslgxevezlbxkp7qorifc4cekw6ol3kgm`
  — hypercube subcube saturation problem.
- `bafkreih2tqokgawtue33oce4smzwcbba36as2qnjwoskwbzu7am4b2mamy`
  — independently checked exact positive `Q_4` slack of three.
- `bafkreidb54nb5k4abxrunvu4k72hhk3ynch5helu7stxmtalhf4tqbmxj4`
  — sharp `Q_4` facet-slack ratio.
- `bafkreiayhj4iizyrzl7gwtwdxqvhwooffg3ph54afqfmwymqehktnyjyeu`
  — preceding `Q_5` compatibility theorem with deficit lower bound one.
- `bafkreiel3tcy76f7pzrv3b2vsghiakvtaqqjm46ecphwnrvfa3vc5rykhy`
  — later `Q_6` modular bound whose arithmetic equality profile is now
  impossible and whose global bound is superseded.

Primary context checked on 2026-09-19:

- Johnson and Pinto, [*Saturated Subgraphs of the Hypercube*](https://arxiv.org/abs/1406.1766), define the parameter and establish the earlier constant-order framework.
- Morrison, Noel, and Scott, [*Saturation in the Hypercube and Bootstrap Percolation*](https://arxiv.org/abs/1408.5488), prove `Theta(2^d)` for every fixed forbidden subcube.
- Dejter, Emamy-K, and Guan, [*On the fault tolerance in a 5-cube*](https://www.researchgate.net/publication/265697468_On_the_fault_tolerance_in_a_5-cube), supply the imported exact value `ex(Q_5,C_4)=56`; the linked copy is author-uploaded.

Focused searches found no published 28-unit facet gap or `204/113` lower
constant.  This supports “apparently new to the searched sources,” not a
historical-priority claim.  The finite lemma is exact computer-assisted
mathematics.  The all-dimensional theorem additionally trusts the displayed
human incidence reductions and the imported `ex(Q_5,C_4)=56` theorem.  The
computation does not reprove that external extremal value, formalize the
universal double counts, determine exact saturation numbers, or prove that
the Q5 deficit lower bound 28 is itself attained.
