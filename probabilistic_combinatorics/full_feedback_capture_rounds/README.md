# Optimal constant rounds for full-feedback localization

For a connected graph `G`, let `T(G)` be the smallest worst-case number of
rounds in which one cop can locate an invisible robber. Each probe returns
**all** neighbors on shortest paths to the robber; after an unresolved
round the robber may stay or move one edge. Strategies may depend on the
whole graph and on previous responses.

If `G~G(n,p)` and `np^2/log n -> c>1/2`, then, away from integer values of
`1/(2c-1)`,

```
T(G) = ceil(1/(2c-1))  with probability tending to one.
```

For each fixed `r`, the boundary for winning within `r` rounds is
`c=(r+1)/(2r)`. Above it any `r` distinct labels chosen before sampling the
graph suffice with high probability. Below it no adaptive strategy wins
in `r` rounds with high probability. At the boundary only
`T(G) in {r,r+1}` is proved.

| Limiting coefficient `c` | Optimal rounds with high probability |
|---|---:|
| `c>1` | 1 |
| `3/4<c<1` | 2 |
| `2/3<c<3/4` | 3 |
| `5/8<c<2/3` | 4 |
| `(r+1)/(2r)<c<r/(2(r-1))`, `r>=2` | r |

Thus one cop suffices throughout `c>1/2`, including a range where no single
initial probe resolves the graph. This result controls a moving robber.
It is distinct from the earlier initial-probe appearance law.

The [full proof](PROOF.md) uses an unresolved-walk count for the upper
bound and two indistinguishable walks for every probe sequence for the
adaptive lower bound. The latter uniformity is essential: exhibiting an
ambiguous walk for one schedule does not prove an adaptive lower bound.

This is a handwritten asymptotic theorem submitted for independent review.
It is not formally verified. Critical windows, `c<=1/2`, growing round
counts, and the general more-than-two-cops question remain outside its scope.
[LITERATURE.md](LITERATURE.md) records the primary source, graph context,
and the scope of the novelty search.

## Reproduction

CPython 3.11.2 was used; Python 3.11+ and its standard library suffice.
There are no packages, solvers, floating-point computations, external
datasets, or omitted large certificates.

From this directory:

```sh
python3 verify.py > /tmp/capture-rounds.json
cmp EXPECTED.json /tmp/capture-rounds.json
python3 -O verify.py > /tmp/capture-rounds-optimized.json
cmp EXPECTED.json /tmp/capture-rounds-optimized.json
sha256sum -c SHA256SUMS
```

The expected status is `VERIFIED`. The checks include:

- All 1,099 labelled graphs through five vertices, including 772 connected
  graphs and 18,849 response entries; distance-based responses agree with
  independent propagation of first-step labels.
- 18,849 two-round schedules and 317 three-round controls, comparing
  information-set updates with literal legal robber-walk histories.
- 2,703 instances of the deterministic ambiguity cover, 7,181 sufficient
  empty-walk certificates, and 504 controls showing that an ambiguous walk
  alone does not prove failure. In particular, the four-vertex path wins
  with probes `(1,2)` despite having a globally ambiguous walk.
- Exact adaptive fixed points and path/cycle/complete-graph controls;
  seven explicit two-walk certificates, including repeated and adjacent
  probes; nine malformed-input or corrupted-certificate rejections.
- 4,360 connected quotient templates through four rounds, including 308
  excluded triple-anchor patterns, and 5,168 forbidden witness loops.
  The sharp template exponent occurs 30 times.
- Twelve exact rational binomial-layer distributions and five exact
  missing-direction expectations, checked by edge enumeration at `p=1/3`.

The connected-graph adaptive-round histogram is 1 graph requiring zero
rounds (the single vertex), 507 requiring one, 252 requiring two, and 12
on which one cop never wins. The graph-record SHA-256 is
`2d8400c8675ecf7ffa5cdef23fb66899a8f4d0cc922cf17ea5b6e578fbd7fe7b`.
The checker emits the seven compact walk fixtures as well as the summary.

These are finite corroboration and semantics checks. The universal
asymptotic quantifiers and the independence arguments are supplied by
PROOF.md, not by the census or its agreement with the expected output.
