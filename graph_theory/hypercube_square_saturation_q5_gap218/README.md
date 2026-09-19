# The Q5 square-saturation facet deficit is at least 218

## Result

Every nonempty square-free edge set `K` in the five-dimensional hypercube
`Q_5` satisfies

```text
Delta_K = 34 S_K - 12 E_K >= 218.                 (1)
```

This strengthens the independently accepted lower bound 217 by proving that
its endpoint is unattainable.  In particular, for every `d>=5`,

```text
sat(Q_d,Q_2) >= 19992 d 2^d / (10979d+29005).     (2)
```

Thus

```text
liminf_(d->infinity) sat(Q_d,Q_2)/2^d >= 19992/10979.
```

The proof is exact and computer-assisted.  It does **not** run a larger
`S_H<=17` census.  It combines a short incidence lemma for the only unseen
`S_H=17` case, the already accepted `S_H<=16` census, an exported 182-row
boundary-profile certificate, and two implementations of the final overlap
closure.

## Definitions inherited from the accepted chain

For a square-free edge set in a cube, a square is *active* if exactly three
of its edges are present; its missing edge is its witness.  If `T` is the
number of active squares and `P` is the number of unordered pairs of active
squares sharing a witness, the local `Q_4` slack is

```text
S_H = 6 E_H - 7 T_H + 2 P_H,
delta_H = 17 S_H - 3 E_H.
```

The accepted local identities give, for `K` in `Q_5`,

```text
Delta_K = sum_(Q4 facets H) delta_H = 34 S_K - 12 E_K.
```

The previous package proved `Delta_K>=217`, using the complete set of
490,753 labeled square-free `Q_4` patterns with `S_H<=16`.  Its two census
implementations agreed entry-for-entry, with normalized graph-set SHA-256

```text
9274309488ef16e6e49a2066e83a364e704d99b716f271740427421ca90b5189.
```

That theorem and its independent review are adjacent dependencies in this
repository.

## The unseen S=17 layer collapses by incidence

Since a square-free `Q_4` has at most 24 edges, the equation

```text
17 S_H - 3 E_H = 217
```

has only two nonnegative possibilities with `E_H<=24`:

```text
(E_H,S_H) = (7,14), (24,17).                      (3)
```

The first is already inside the accepted `S_H<=16` census.  The second is
impossible, without any `S_H=17` enumeration:

**Extremal-facet lemma.** Every 24-edge square-free subgraph of `Q_4` has
`(E,T,P,S,delta)=(24,24,24,24,336)`.

Indeed, `Q_4` has 32 edges and 24 squares.  The eight omitted edges have
exactly `8*3=24` incidences with squares.  Each square needs an omitted edge,
so equality forces every square to contain exactly one omitted edge.  Hence
all 24 squares are active, every omitted edge witnesses exactly three of
them, and

```text
T=24,
P=8 binom(3,2)=24,
S=6*24-7*24+2*24=24,
delta=17*24-3*24=336.
```

The verifiers additionally enumerate the eight exact covers of the 24
squares by omitted edges and independently recover this spectrum.  The
enumeration is an audit, not a premise of the displayed proof.

## Exported boundary-profile certificate

The unchanged `S_H<=16` census is classified with the endpoint included,
that is, with `0<delta_H<=217`.  A profile is

```text
(delta_H, E_H, b(H), e_0(H)),
```

where `b(H)` counts boundaries not extendable to a nonempty zero-deficit
facet and `e_0(H)` counts empty boundaries.  The full 182-row table and every
labeled multiplicity are exported in `PROFILE_CLASSES.json`; its canonical
SHA-256 is

```text
9dc4c10874d87acd730ab6fb0741b23da45c13a4d01ba29149dcc11e8f4aefbb.
```

This makes the structural compression inspectable without rerunning the
census.  The only individual deficit-217 facets in the table are

| profile | labeled patterns | `Aut(Q_4)` orbits |
|---|---:|---:|
| `(217,7,5,2)` | 192 | one orbit of size 192 |
| `(217,7,7,1)` | 192 | one orbit of size 192 |

For a ten-facet `Q_5` profile, let `p,k,z` be the numbers of positive,
nonempty zero-deficit, and empty facets.  The verifier applies the same three
accepted necessary conditions:

1. `sum E_H=4E_K`;
2. the exact maximum edge capacities for `l=p+k=1,...,10` live facets are
   `0,0,0,1,5,9,16,28,48,80`;
3. every positive facet obeys `b(H)<=p+z-1`.

An exhaustive integer multiset calculation over the exported table leaves
exactly three signatures of total 217:

| positive profiles `(delta,E,b,e_0)` | `k` | `z` | `E_K` |
|---|---:|---:|---:|
| `42_0,42_0,42_0,(91,15,4,1)` | 5 | 1 | 40 |
| `42_0,42_0,(48,18,3,0),(85,17,4,0)` | 5 | 1 | 40 |
| `42_0,(48,18,3,0),(127,20,3,0)` | 6 | 1 | 40 |

Here `42_0=(42,20,0,0)`.  In particular, neither individual deficit-217
class survives even these necessary conditions.

## Exact boundary closure

All catalogs used by the three signatures are regenerated as full
`Aut(Q_4)` orbits.  The only multi-orbit catalog is `(85,17,4,0)`, whose
576 patterns split into orbits of sizes 192 and 384.  Facet transitivity lets
the single size-32 `42_0` orbit be fixed on one distinguished facet.  Exact
agreement on every shared `Q_3` boundary then gives:

| signature | labeled-facet cases | production nodes | solutions |
|---:|---:|---:|---:|
| 1 | 1,512 | 1,638 | 0 |
| 2 | 3,024 | 3,276 | 0 |
| 3 | 504 | 560 | 0 |
| **total** | **5,040** | **5,474** | **0** |

The independent checker uses separately ordered endpoint-pair edges and a
reviewer-owned generic gluer.  It regenerates all orbit statistics and
boundary profiles and also finds zero solutions in the same 5,040 cases.
Consequently deficit 217 is unattainable.  Together with the accepted lower
bound 217, integrality proves (1).

## Global consequence

Import the published exact value `ex(Q_5,C_4)=56`.  From (1), every nonempty
square-free edge set in `Q_5` satisfies

```text
S_K >= (12E_K+218)/34 >= (445/952) E_K,            (4)
```

where the last ratio is weakest at `E_K=56`; it also holds for the empty
set.  Summing over five-subcubes of `Q_d` gives

```text
S >= 445 E(d-1)(d-2)/11424.                        (5)
```

For a square-saturated graph let `N=d2^(d-1)`, `E=|E(G)|`, and `M=N-E`.
The established active-square identities are

```text
B+3A = (d-1)E - 3M,
B+3A >= M/2 + S/(d-2).
```

Substituting (5) and clearing denominators yields

```text
10979(d-1)E >= 39984M.
```

With `M=d2^(d-1)-E`, this is

```text
(10979d+29005)E >= 19992d2^d,
```

which proves (2).  The asymptotic improvement over the accepted gap-217
constant is exactly `2856/34441123`.  The first improved integer lower bound
is at `d=11`, from 3007 to 3008.

## Reproduction

Python 3.11 or later and the standard library suffice.  No solver, network,
randomness, or floating point is used.

```bash
cd graph_theory/hypercube_square_saturation_q5_gap218

# Compact independent replay (normally under ten seconds).
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py > /tmp/q5-gap218-independent.json
diff -u EXPECTED_INDEPENDENT_OUTPUT.json /tmp/q5-gap218-independent.json

# Full census-backed replay (several minutes).
PYTHONDONTWRITEBYTECODE=1 python3 verify.py > /tmp/q5-gap218.json
diff -u EXPECTED_OUTPUT.json /tmp/q5-gap218.json

sha256sum -c SHA256SUMS
```

## Literature and scope

The surrounding saturation problem and its `Theta(2^d)` scale come from
[Johnson--Pinto, *Saturated Subgraphs of the Hypercube*](https://arxiv.org/abs/1406.1766)
and [Morrison--Noel--Scott, *Saturation in the Hypercube and Bootstrap
Percolation*](https://arxiv.org/abs/1408.5488).  The imported five-cube
extremal value is from [Dejter--Emamy-K--Guan, *On the fault tolerance in a
5-cube*](https://www.researchgate.net/publication/265697468_On_the_fault_tolerance_in_a_5-cube).
Primary-source and exact-constant searches were refreshed on 2026-09-19 and
found no published deficit-218 or `19992/10979` result.  This supports only
an apparently-new claim relative to the searched sources and committed
Discovery Net graph, not a historical-priority claim.

The theorem remains conditional on the displayed active-square identities,
the accepted `Q_3/Q_4` slack machinery, and `ex(Q_5,C_4)=56`.  It does not
determine the exact square-saturation number, establish that deficit 218 is
attained, or formalize the incidence bridge in a proof assistant.
