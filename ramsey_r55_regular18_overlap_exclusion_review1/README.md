# Independent review of the h3959 regular18/24 exclusion

Verdict: **ACCEPT subject to the declared imported catalog boundaries.** There
is no 18-regular or 24-regular good graph on 43 vertices. Consequently any
regular good43 would have degree 20 or 22. This is an intermediate complete
degree-class exclusion, not a good43 construction or a proof of
`R(5,5) >= 44`.

The independent audit downloads no data itself. Supply the complete official
352,366-record `(4,5;24)` graph6 catalog with SHA-256
`83ca4028f206b2fa4315ef219b8c2c57c7835209673dd8183d8fb4353bd4fdd0`.
The audit decodes the full catalog using fresh bit-row code, verifies every
retained Ramsey graph, reconstructs all 24,648 rooted profiles and all 6,669
profile-pair decisions, and probes the physical interface on fresh regular
graphs. [REVIEW.md](REVIEW.md) gives the proof audit and trust boundary.

From the repository root, using CPython 3.11 or later and fresh scratch paths:

```sh
curl -fL https://users.cecs.anu.edu.au/~bdm/data/r45_24.g6 \
  -o /scratch/research-team-v2/tmp/reviewer-1/catalogs/r45_24.g6
python3 -B ramsey_r55_regular18_overlap_exclusion_review1/reproduce.py \
  . /scratch/research-team-v2/tmp/reviewer-1/catalogs/r45_24.g6 \
  /scratch/research-team-v2/tmp/reviewer-1/review-h3959
```

Expected status: `REPRODUCED_ACCEPT_REVIEW_H3959`. The reproduction extracts
the reviewed source commit, replays its normal/assertion-disabled checks, and
runs the independent checker in both modes. It uses Git and the Python
standard library, invokes no solver, and keeps generated evidence outside the
repository.
