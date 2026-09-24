# Linear full-LP triangle rounding for bounded neighborhood diversity

For every fixed number `t` of mixed vertex classes, the
[author proof](PROOF.md) establishes a finite constant `K_t` such that

```text
0 <= nu*(G) - nu(G) <= K_t |V(G)|.
```

Each class is a clique or an independent set, and each cross pair is
complete or empty. **Class sizes are arbitrary.** Several classes may
vanish relative to the others at unrelated rates. The result concerns the
full fractional triangle packing, including every repeated-type triangle.
The linear error order is necessary already for even complete graphs.

The proof is complete at the author level and awaits independent review.
`K_t` and the design thresholds remain existential. The result does not
settle Tuza's exact packing-covering conjecture or supply a practical
universal construction.

The stronger theorem rounds full profiles of triangles and finitely many
labeled single-edge patterns with linear total component loss, while
bounding every individual pattern's vertex-role discrepancy by a constant.
This invariant permits induction on the number of classes, even though
the number of auxiliary edge labels grows.

The two main bridges are:

- [Private pendant tags](ROLE_COMPLETION.md), which force actual roles at
  each vertex in a generalized design, beyond the earlier global-count tags.
- Same-type color swaps preserving every type/color count. A per-class
  incidence estimate makes this work without comparable small-class sizes.

These combine with row-normalized integral flow, globally ordered Hall
matchings and the accepted sparse-switch/degree-realization lemmas.
[SOURCES.md](SOURCES.md) identifies dependencies and novelty limits.

## Reproduce

Python 3.11.2 and the standard library suffice. From this directory:

```sh
python3 check.py > /tmp/bounded-type-audit.json
cmp /tmp/bounded-type-audit.json AUDIT.json
sha256sum -c SHA256SUMS
```

Expected output is [AUDIT.json](AUDIT.json), with SHA-256
`3524a0deed1930285cc68ab6953d912034bc7aa85170b7a7be437dd3e4f027fd`.
Normal execution took about 33 seconds and 345 MiB maximum resident memory
on the research host. Exact measurements and the optimized-mode repeat
are in [RUN.json](RUN.json). The output is deterministic and is checked
byte-for-byte under `PYTHONHASHSEED=123 python3 -O check.py`.

[constructions.py](constructions.py) generates finite tag, coloring and
exterior witnesses; [flow.py](flow.py) reuses the earlier exact flow/matching
routines. [check.py](check.py) separately checks definitions, replays all
swaps, verifies each flow column bound and checks every literal edge.
This is same-author validation, not independent peer review.

The audit covers:

- 4,608 pendant degree prescriptions; all 8,480 labeled embeddings in six
  repeated/distinct-type fixtures; and a complete 42-edge augmented Fano
  decomposition with exact local-role decoding.
- All 1,099 graphs through five vertices for coloring input/decoding
  checks, 60 seeded nontrivial repair cases, and two literal fixtures
  meeting all universal coloring hypotheses: 73,536 edges on 384 vertices
  and 192,000 edges with unequal parts of sizes 192 and 1,000. It replays
  8,624 repairs in those nontrivial cases.
- 148 compressed profiles on all 74 mixed templates with up to three
  classes, checking 2,176 exact role intervals through order
  6,000,000,000,000; 192 parameter tuples; 4,783 illustrative size-hierarchy
  cases; and 210 small-class deletions with exact released-capacity labels.
- A graph with three interacting exceptional classes of sizes 9,9,9,
  respectively clique, independent, clique, and different neighborhoods
  in a 37,000-vertex core. All 274,587 exterior triangles and 89,694 labeled
  spoke edges are checked, along with 45 matching conditions, 13 matching
  repairs, ten color swaps and a nonzero residual HHH capacity profile.
- Nine malformed inputs or certificates, all rejected.

The exhaustive five-vertex graphs start with distinct edge colors; they
test the input/decoding contract, not the hard repair mechanism. The latter
is exercised by the seeded cases and the two sufficient-hypothesis fixtures.
The integrated interior is an explicitly supplied affine witness, below
the universal color lemma's absolute minimum; its successful coloring is
checked directly. The integrated flows do meet the stated cutoff and
elementary size conditions. Neither its interior nor its core is claimed
to exceed an unknown design threshold. Core-only triangles are not
materialized; their residual capacity identities are checked exactly.

The large profiles are integer/rational identities, not giant packings.
The size-hierarchy tolerances are illustrative rational values, not
computed Keevash constants. Additional complete-bipartite color profiles
reach a part size of `10^24` without materialization.

All literal witnesses and traces are regenerated in memory. No solver,
floating point, external input, private data, omitted bulk certificate or
unpublished enumeration is required. The finite checks do not prove the
imported universal design theorem, formally verify the induction, compute
`K_t`, or establish historical priority.
