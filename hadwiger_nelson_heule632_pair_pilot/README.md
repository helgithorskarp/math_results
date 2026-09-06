# A five-chromatic 630-point Heule completion seed

The full unit-distance graph on `H632 - {399,462}` has **630 distinct
vertices, 3,098 edges and chromatic number exactly five**. Labels 399 and 462
refer to the old H510 order defined below. A DRAT-checked refutation excludes
four colours; the compact certificate supplies a proper five-colouring.

This is a larger seed for a subsequent bounded minimization experiment.
It does **not** improve the 509-vertex record, establish a graph on at most
508 vertices, or assert minimality or vertex criticality. No minimization
was performed in this milestone.

## Exact support and proof

Let `H632` contain the archived 510 Heule points and all 122 archived fresh
completion centres. Both coordinate sources are already in this repository:

- [`certificate_H510.json`](../hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json):
  take the increasing union labels whose provenance contains `"510"`,
  assigning them old labels 0 through 509.
- [`fresh_candidates.json`](../hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json):
  append every row, in its increasing `centre_index` order, assigning labels
  510 through 631. These labels differ from the sparse archived centre indices.

Each coordinate is an eight-entry rational coefficient vector in the ordered
basis `(1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165))`.
Multiplication by 96 makes every coefficient integral. Both implementations
check all 199,396 unordered pairs by exact integer arithmetic, recovering
632 distinct points and 3,112 unit edges. Delete old labels 399 and 462
(union labels 436 and 505). The remaining induced unit-distance graph has
630 vertices and 3,098 edges. See [PROOF.md](PROOF.md) for the encoding and
mathematical argument.

The four-colour CNF has 2,520 variables and 16,805 clauses. Its SHA-256 is
`8c123d547fc4c2ff24338880b8a9d61e6edb798b844900c172de6e6a6e3c7e4f`.
The original binary DRAT certificate contains 3,231,081 bytes, with SHA-256
`888d261774d76c2ae5667931a96a27abd54d2cb872dfbda183f2b3372b51f620`.
It passed the checker during the run and again against a separately rebuilt
CNF. Standalone regeneration produced the same proof and passed a third check.

[`certificate.json`](certificate.json) contains the 632-character
five-colouring, with dots at the two omitted positions, and five positive
four-colourings from the pilot prefix. Its SHA-256 is
`fffa224298854425f7c40726a9dd96196b1c5e82b75ffa4d8c6c19fefbc8274f`.
Every retained unit edge is checked against each applicable colouring.

## Frozen experiment and completed boundary

The preceding [transport result](../hadwiger_nelson_heule632_transport/README.md)
provides 22 valid singleton-deletion four-colourings. Any pair touching one
of those old labels is already four-colourable by restriction, leaving
`C(488,2) = 118828` potentially useful old omission pairs. The [independent
transport review](../hadwiger_nelson_heule632_transport_review1/README.md)
accepts those cuts and the exact scope of the fixed-library classification.

The pilot froze 24 pairs before any query: eight each from LL, LS and SS,
where the old large block L consists of the 375 points whose two coordinates
have no coefficients involving `sqrt(5)`. Within each stratum, pairs are
ranked by `(edges lost, u, v)`, and eight vertex-disjoint pairs are greedily
selected. The three lists are interleaved. This is a density heuristic,
not a symmetry reduction or exhaustive decision of the pair family.

The prescribed stopping rule was the first verified four-colour refutation,
followed by at most one five-colour query on that same support.

| Index | Stratum | Omitted old labels | Unit edges | Four colours |
| --- | --- | --- | --- | --- |
| 0 | LL | 102, 293 | 3104 | SAT, checked colouring |
| 1 | LS | 102, 384 | 3102 | SAT, checked colouring |
| 2 | SS | 384, 444 | 3100 | SAT, checked colouring |
| 3 | LL | 302, 305 | 3104 | SAT, checked colouring |
| 4 | LS | 293, 399 | 3101 | SAT, checked colouring |
| 5 | SS | 399, 462 | 3098 | UNSAT, checked DRAT |

The conditional five-colour query was SAT. The pilot therefore ended after
six of 24 prepared cases, leaving 18 unattempted and no UNKNOWN outcomes.
The full pair family remains open. The complete pilot took 10.63 seconds;
the winning solve and its first proof check took 2.73 and 1.72 seconds.
Timings are observations from this environment, not performance guarantees.

## Reproduction

Use Python 3.11 or newer on a Unix system, Kissat 4.0.4 and `drat-trim`.
Python modules use only the standard library. The executed Kissat source ID
was `8af8e56f174b778aef3aa45af9f739b2a5f492c2`. Exact executable hashes,
input hashes, solver options and resource limits are in [plan.json](plan.json).

From the repository root, choose an output directory outside the repository:

```sh
python3 -B hadwiger_nelson_heule632_pair_pilot/verify.py \
  --out /tmp/hn630-verification \
  --regenerate-with /path/to/kissat \
  --drat-trim /path/to/drat-trim
```

This rebuilds all geometry and 24 frozen formulas, verifies the six positive
colourings, regenerates the four-colour proof, and checks it against the
independent CNF. Expected output includes
`EXACT630-VERTEX FIVE-CHROMATIC UNIT-DISTANCE GRAPH VERIFIED`, 630 vertices,
3,098 edges, and `proof_regenerated: true`. It took 7.39 seconds here.
A different valid DRAT proof is acceptable. To check a supplied proof, replace
`--regenerate-with /path/to/kissat` with `--proof /path/to/proof.drat`.
Neither mode accepts a stored UNSAT verdict without checking a real proof.

The original controls and bounded pilot can also be rerun:

```sh
python3 -B hadwiger_nelson_heule632_pair_pilot/controls.py \
  --out /tmp/hn630-controls --kissat /path/to/kissat \
  --drat-trim /path/to/drat-trim
python3 -B hadwiger_nelson_heule632_pair_pilot/run.py \
  --out /tmp/hn630-pilot --kissat /path/to/kissat \
  --drat-trim /path/to/drat-trim \
  --controls /tmp/hn630-controls/controls.json
python3 -B hadwiger_nelson_heule632_pair_pilot/verify.py \
  --out /tmp/hn630-audit --archive /tmp/hn630-pilot \
  --drat-trim /path/to/drat-trim
```

The pilot runner requires the original executable hashes to preserve the
frozen experiment. Standalone theorem verification permits another solver
binary and still requires a checked proof. A bounded rerun that times out is
inconclusive; it does not invalidate the archived certificate.

## Validation and trust boundary

[`independent.py`](independent.py) and [`verify.py`](verify.py) import no
producing graph, CNF or runner module. The producer uses ordered XOR
convolution; the verifier uses sparse squarefree radicands, diagonal terms,
and unordered cross terms reduced by gcd. They independently rebuild pair
selection and every prepared CNF. This is implementation independence within
one researcher, not an independent-author review of this new seed.

Controls compare all 32,768 Boolean assignments over all eight graphs on
three labelled vertices with the definition of a pinned proper colouring.
Native controls establish K4/4 SAT, K5/4 UNSAT with checked DRAT, and K5/5
SAT. The archive audit checks 106,532 native-model clauses, 15,511 retained
edges across the five positive prefix cases, and 3,098 five-colouring edges.
Three malformed positive certificates are rejected. See
[validation.json](validation.json) for the executed reports.

The proof relies on exact rational/integer execution, independence of the
radical basis, the CNF equivalence proved below, and the correctness of the
DRAT checker. It does not trust Kissat's UNSAT exit code alone. Neither a
proof-assistant formalization nor a second proof-checker implementation is
claimed. All imported files are hash-pinned; no completeness property of the
fresh-centre search or old colouring library is assumed for this graph.

Public files contain source, frozen decisions and a compact positive
certificate. Raw CNFs, the 3.23 MB proof and verbose logs stay in local run
storage; the proof is reproducible with the standalone command above.
The next proposed phase is a bounded minimization of this verified seed,
preserving the two old omissions. It has not started.
