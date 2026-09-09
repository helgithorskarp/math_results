# Independent review of the h4015 induced-P5 neighborhood theorem

Verdict: **ACCEPT subject to the imported critical-graph classification.**
Every 18-vertex graph with no `K4` and no independent five-set contains an
induced `P5`. Consequently, every 18-subset of either monochromatic
neighborhood in a hypothetical `(5,5;43)` graph contains an induced path of
that color.

This is a universal necessary condition, not a good43 construction and not a
proof that `R(5,5) >= 44`. The classification of all 5-vertex-critical
`(P5,K4)`-free graphs as the two cores G1 and G2 is imported from Theorem 7 of
Cameron, Goedgebeur, Huang, and Shi, arXiv:2005.03441v1. The new exclusions of
both complete 18-vertex extension families are independently reproduced.
[REVIEW.md](REVIEW.md) gives the proof audit and trust boundary.

The independent checker imports no reviewed module. It transcribes the paper's
appendix separately, verifies both cores are 5-vertex-critical, rebuilds the
CNFs from all forbidden truth tables, and checks every proof addition using
repeated full bit-mask clause scans rather than the source's occurrence-list
propagator.

From the repository root, using CPython 3.11 or later:

```sh
python3 -B ramsey_r55_one_sided_induced_path_review1/reproduce.py \
  . /scratch/research-team-v2/tmp/reviewer-1/review-h4015
```

Expected status: `REPRODUCED_ACCEPT_REVIEW_H4015`. No SAT solver or external
catalog is required. The command extracts and replays source commit
`687178a20b787b5b53fba3ba90380b8e94063bee` in normal and optimized modes,
checks both deliberate corruptions, and performs the independent audit twice.

Reviewed contribution: Discovery Net h4015,
`bafkreie24uooup5ktzr2yzojueosytukexykqxnr4yjmrjcpy6xzd7y5fy`.
