# Two-round localization and slowdown under edge addition

Adding an asymptotically negligible fraction of edges can make one-cop
full-feedback localization take arbitrarily many more rounds in sparse
random graphs. Both the original and enlarged graphs still admit a
winning one-cop strategy with probability tending to one.

Here a probe returns **all** neighbors on shortest paths to an invisible
robber. After an unresolved round the robber may stay or move one edge.
Write `T(G)` for the optimal worst-case number of rounds with one cop.

The new theorem is

```
np^2/log n -> c,  15/32 < c < 1/2  =>  T(G(n,p))=2 with high probability.
```

One fixed first probe and a fixed finite list of alternative second probes
suffice; the cop chooses the second probe after the first response. For
example, at `c=31/64`, a list of 23 alternatives works. The endpoint
`15/32` is sufficient for this proof and is not claimed sharp.

Combining this theorem with the explicitly cited
[prior capture-time hierarchy](https://github.com/helgithorskarp/math_results/tree/main/probabilistic_combinatorics/full_feedback_capture_rounds)
gives two consequences:

- For any fixed integer `M>=3`, independent edge addition couples random
  graphs with `T(G_-)=2` and `T(G_+)=M` simultaneously with high probability.
  One may take `np_-^2/log n=31/64` and
  `np_+^2/log n=1/2+1/(2M-1)`.
- There are deterministic sequences with `p_+/p_- -> 1` and both
  `np_+^2/log n` and `np_-^2/log n` tending to `1/2`, such that
  `T(G_-)=2` with high probability, `T(G_+)` diverges in probability,
  and `T(G_+)` remains finite with high probability. The number of added
  edges divided by the original number tends to zero in probability.

The second consequence uses an existential diagonal argument. It gives
no explicit divergence rate and makes no uniform claim for a prescribed
growing number of rounds. Both consequences depend on the prior written
hierarchy proof, which awaits independent review. The new two-round
theorem is self-contained in [PROOF.md](PROOF.md).

The proof first shows that distance-three responses distinguish all
zero-common-neighbor targets below `c=1/2`. It then counts simultaneous
failures of all candidate second probes. A spanning-tree argument controls
overlapping witnesses, including repeated centers and cycle-free
degeneracies. This proves that every possible unresolved first reply has
a successful second probe.

Nonmonotonicity itself was already visible by closing a path into a cycle,
which can raise the required number of cops from one to two. The claims
here keep that number at one and concern random graphs and relative edge
addition. They do not answer whether any graph needs more than two cops.
[LITERATURE.md](LITERATURE.md) records the primary source, graph context,
and the limited novelty search.

## Reproduction

Python 3.11+ and its standard library suffice; CPython 3.11.2 was used.
No solver, floating-point calculation, external dataset, or omitted large
certificate is required. From this directory:

```sh
python3 verify.py > /tmp/edge-addition-slowdown.json
cmp EXPECTED.json /tmp/edge-addition-slowdown.json
python3 -O verify.py > /tmp/edge-addition-slowdown-optimized.json
cmp EXPECTED.json /tmp/edge-addition-slowdown-optimized.json
sha256sum -c SHA256SUMS
```

Expected status: `VERIFIED`. The exact checks comprise:

- All 934,089 star identification partitions and 77,897 pair partitions
  with predecessor choices for one or two alternatives: 11,924 valid star
  templates and 3,612 valid pair templates. Each constructed forest,
  edge charge, and counting exponent is checked with exact arithmetic.
  Controls cover a reused center, a cycle-free degenerate witness, and
  four charges on one edge. Four malformed templates are rejected.
- All 1,099 labelled graphs through five vertices, including 772 connected
  graphs and 18,849 response entries. Independent shortest-path response
  implementations agree. There are 3,003 successful full-menu two-round
  policies and 12,624 successful two-alternative menus. Literal robber
  moves reproduce 9,242 and 31,146 response histories, respectively.
  Full-menu success agrees with the exact adaptive information-set fixed
  point. Seven malformed inputs or corrupted policies are rejected.
- Exact rational checks of 18 one-direction and 18 two-direction
  separation identities, five nonneighbor code-equality identities,
  165 edge-addition marginal identities, and 98 slowdown coefficients.

The finite template-record SHA-256 is
`bd4b2bce1686fb51e489819546f63b2cd31e3425bad67b8b8c8c08187f1330b8`.
The finite graph-record SHA-256 is
`27bcf997ed3ffb7b567ab13ec56130c0c5dd2b1e9c23ed239dc0ce58919f93b6`.
`EXPECTED.json` contains the complete compact summary; `SHA256SUMS`
covers all other published files in this directory.

These computations check finite bookkeeping and the game semantics.
They do not prove the asymptotic quantifiers. The universal spanning-tree
lemma, independence arguments, probability estimates, and diagonal
construction are supplied by the written proof. No independent acceptance
or formal verification is claimed.
