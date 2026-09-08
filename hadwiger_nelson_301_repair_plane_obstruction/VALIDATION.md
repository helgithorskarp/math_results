# Validation and reproducibility

The geometric certificate is checked independently of its producer.

| Stage | Implementation | Evidence |
|---|---|---|
| Certificate discovery | CPython3.11.2, python-flint0.8.0 | Explicit quotient wheels, exact rational kernel and norm-dependence calculations |
| Geometry verification | CPython3.11.2 standard library | Exact `Fraction` arithmetic, graph inverse images, independent sparse modular elimination |
| Corruption checks | Same standalone checker | Seven malformed certificates rejected |
| Optimized execution | Python `-O` | Receipt byte-identical to normal execution |
| Regeneration | Public `produce.py` in the same environment | Certificate byte-identical to the committed certificate |

Canonical certificate size:45903 bytes. SHA256:
`728c5af3dc90c6e01ac74c13d78768cae997f6fe91d39dfa1076600bfb61ab42`.
The normal verification, including controls and the optional chromatic-data
audit, took less than one second on the research host. No timing is a proof
premise. The producer uses one process and no SAT query. The proof has no
search cap or numerical tolerance.

The canonical diagonal witnesses consist of276 direct edges and282 odd
wheels:266 have rim length3, ten have rim length5, and six have rim length7.
Their role is to forbid the two diagonal collapses in each of279 cycles.
The checker requires every named edge, every quotient incidence, all rational
linear relations, an independent rank lower bound, and every coefficient of
the final55-variable quadratic identity.

The seven rejected mutations are: a degenerate purported four-cycle, a missing
diagonal witness, a wheel whose rim contains its hub, an altered rational
parameter entry, an incorrect rank, an altered norm multiplier with its sum
updated to match, and a missing source edge. The norm mutation reaches the
quadratic check; agreement of the weight sum alone cannot make it pass.

## Positive source gate replay

Before pursuing geometry, the researcher replayed the sibling package's
source reconstruction and its explicit five-colouring and301 deletion
four-colourings. The independent checker in this package separately rebuilds
the1204-variable6112-clause four-colouring CNF from the actual graph and
checks all302 colouring witnesses.

The existing source LRAT was replayed using the already audited strict
positive-hint RUP checker from
`hadwiger_nelson_vnd_case10_verified_gate/strict_lrat.cpp`:

```sh
g++ -O3 -std=c++17 hadwiger_nelson_vnd_case10_verified_gate/strict_lrat.cpp -o /tmp/hn301-strict-lrat
/tmp/hn301-strict-lrat hadwiger_nelson_h516_k23free_edge_repair/four_colour.cnf hadwiger_nelson_h516_k23free_edge_repair/four_colour.lrat
```

Result: `VERIFIED_STRICT_RUP_LRAT`,7971 additions,14026 deleted clause IDs,
685802 used hints and12046 proof lines. No fresh chromatic SAT query was run.
The legacy permissive `lrat-check` executable was not used.

CNF SHA256:
`f88078fe17e76339b18bf4f1d339921ae2b0bf19a44367cd1978877ce54b0828`.
LRAT SHA256:
`d9b9250c8d40cb59b07d973ba96ca02ec9fce3e446fd5db9ac804599c7d15711`.

The source's chromatic result is a genuine positive gate, although the source
is abstract. The geometric obstruction is logically independent of that
chromatic lower bound. There is no claimed independently produced peer review;
this package supplies a new checked geometric theorem about the shared target.

## Exploratory evidence excluded from the proof

The full2062-cycle parallelogram matrix has rank300 modulo1000000007 and
already excludes injective plane realizations. It does not by itself exclude
noninjective maps and is not the final certificate.

An oriented square-chain screen did not eliminate the source's pinned
triangle. A systematic one-diagonal screen found sufficient elementary
obstructions for279 cycles. The final proof depends on the listed witnesses,
not on completeness of that screen, the failure of the earlier screen, or
any frozen inherited coordinates.
