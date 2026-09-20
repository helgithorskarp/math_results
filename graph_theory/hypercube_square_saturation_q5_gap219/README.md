# The Q5 square-saturation facet deficit is at least 219

## Result

Every nonempty square-free edge set `K` in the five-dimensional hypercube
`Q_5` satisfies

```text
Delta_K = 34 S_K - 12 E_K >= 219.                 (1)
```

This settles the sharpness question left by the accepted deficit-218 theorem:
218 is not attained.  It also gives, for every `d>=5`,

```text
sat(Q_d,Q_2) >= 13328 d 2^d / (7319d+19337),      (2)
```

and hence

```text
liminf_(d->infinity) sat(Q_d,Q_2)/2^d >= 13328/7319.
```

The proof does not enumerate a new `Q_4` slack layer and does not perform a
global facet-gluing search.  It closes the endpoint by combining local
Diophantine arithmetic with the already accepted strict-subendpoint profile
certificate and exact live-facet capacities.

## Accepted inputs

For a square-free edge set in a `Q_4` facet `H`, let

```text
S_H = 6 E_H - 7 T_H + 2 P_H,
delta_H = 17 S_H - 3 E_H.
```

The accepted predecessor chain establishes:

1. `delta_H>=0` for every square-free `Q_4` pattern;
2. every nonempty zero-deficit pattern has `E_H=17`;
3. the 182-row `PROFILE_CLASSES.json` table is complete for
   `0<delta_H<218` and has SHA-256
   `9dc4c10874d87acd730ab6fb0741b23da45c13a4d01ba29149dcc11e8f4aefbb`;
4. if exactly `l=1,...,10` of the ten `Q_4` facets of `Q_5` are live, the
   exact maximum global edge counts are
   `0,0,0,1,5,9,16,28,48,80`;
5. `sum_H E_H=4E_K` and `sum_H delta_H=Delta_K`.

The predecessor source and its independent review reproduce these inputs.

## Endpoint obstruction

Assume `Delta_K=218`.  Since every local deficit is nonnegative, there are
two cases.

### All positive facet deficits are below 218

The verifier enumerates every multiset of positive rows from the accepted
182-row table with total deficit 218.  It adjoins any number of 17-edge
zero-deficit facets and empty facets, then applies only the accepted necessary
conditions:

- `sum_H E_H` is a positive multiple of four;
- the resulting global edge count does not exceed the live-facet capacity;
- each positive facet's bad-boundary count is at most the number of available
  exceptional neighbors.

No profile survives.  `independent_check.py` repeats this calculation with a
state-compressed dynamic program that retains only total deficit, number of
positive facets, edge-incidence sum, and maximum bad-boundary count.

### One facet has deficit 218

Here all other facets have deficit zero.  Since `E_H<=24`,

```text
17 S_H - 3 E_H = 218
```

has only

```text
(E_H,S_H) = (1,13), (18,16).
```

The first pair is impossible: a one-edge pattern has `(T_H,P_H,S_H)=(0,0,6)`.
Thus the exceptional facet has 18 edges.  If `k` of the other nine facets are
nonempty zero-deficit facets, edge incidence gives

```text
4 E_K = 18 + 17k.
```

Divisibility leaves only `k=2` and `k=6`.  They would respectively have

| `k` | live facets | `E_K` | live-facet capacity |
|---:|---:|---:|---:|
| 2 | 3 | 13 | 0 |
| 6 | 7 | 30 | 16 |

Both are impossible.  Therefore deficit 218 is unattainable, proving (1).

## Global consequence

Import the published exact value `ex(Q_5,C_4)=56`.  Equation (1) gives

```text
S_K >= (12E_K+219)/34 >= (891/1904) E_K.
```

The accepted subcube averaging and active-square identities then give

```text
S >= 297 E(d-1)(d-2)/7616,
7319(d-1)E >= 26656M,
```

where `M=d2^(d-1)-E`.  Rearrangement proves (2).  The new asymptotic constant
exceeds the deficit-218 constant `19992/10979` by exactly
`6664/80355301`.  The first improved integer lower bound is at `d=10`, from
1475 to 1476.

## Reproduction

Python 3.11 or later and the standard library suffice.  From the repository
root:

```bash
cd graph_theory/hypercube_square_saturation_q5_gap219
PYTHONDONTWRITEBYTECODE=1 python3 verify.py > /tmp/q5-gap219.json
diff -u EXPECTED_OUTPUT.json /tmp/q5-gap219.json
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py > /tmp/q5-gap219-independent.json
diff -u EXPECTED_INDEPENDENT_OUTPUT.json /tmp/q5-gap219-independent.json
sha256sum -c SHA256SUMS
```

For an end-to-end regeneration of the accepted 182-row input, additionally
run the predecessor's full verifier; that calculation is intentionally not
duplicated here.

## Literature and scope

The surrounding saturation problem and its `Theta(2^d)` scale are due to
[Johnson--Pinto, *Saturated Subgraphs of the Hypercube*](https://arxiv.org/abs/1406.1766)
and [Morrison--Noel--Scott, *Saturation in the Hypercube and Bootstrap
Percolation*](https://arxiv.org/abs/1408.5488).  Primary-source and exact-
constant searches were refreshed on 2026-09-20 and found no published
deficit-219 or `13328/7319` result.  This supports only an apparently-new
claim relative to the searched sources and committed Discovery Net graph,
not a historical-priority claim.

The theorem is conditional on the displayed accepted local-deficit,
profile-certificate, capacity, averaging, and extremal inputs.  It does not
prove that deficit 219 is attained or determine the exact square-saturation
number.
