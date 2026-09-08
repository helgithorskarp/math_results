# Independent review of the h4009 global Ramsey43 edge window

Verdict: **ACCEPT subject to the declared imported catalog boundaries.** Every
43-vertex graph with neither a clique nor an independent set of order five has
between 390 and 513 edges. This is a universal necessary condition on a
hypothetical `(5,5;43)` graph, not a construction and not a proof that
`R(5,5) >= 44`.

The independent audit uses no module from the reviewed package. It decodes the
complete official 352,366-record `(4,5;24)` graph6 catalog into integer bitsets,
checks every retained Ramsey membership, reconstructs all 24,648 rooted
occurrences and 527 profiles, and retests all 6,669 deficit-two profile pairs.
It also enumerates all 80 graphs on the exceptional positive-excess vertices.
[REVIEW.md](REVIEW.md) gives the proof audit and trust boundaries.

Supply the official catalog with SHA-256
`83ca4028f206b2fa4315ef219b8c2c57c7835209673dd8183d8fb4353bd4fdd0`.
From the repository root, run:

```sh
python3 -B ramsey_r55_global_degree_excess_review1/reproduce.py \
  . /path/to/r45_24.g6 \
  /scratch/research-team-v2/tmp/reviewer-1/review-h4009
```

Expected status: `REPRODUCED_ACCEPT_REVIEW_H4009`. The command extracts the
reviewed source commit, replays its normal and assertion-disabled checks, then
runs the independent checker normally and under `python -O`. It invokes no SAT
solver, canonicalizer, graph-isomorphism library, or floating-point predicate.

Reviewed contribution: Discovery Net h4009,
`bafkreihsjbnqzwlgueho6t6iuphxbvkbdb7f5v6sujtfjnmo5x32oxnilq`.
Reviewed source commit:
`d1c2e7026b09696a72c72e1921b6f09500c21c29`.
