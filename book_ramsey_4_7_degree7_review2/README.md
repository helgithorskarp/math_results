# Independent Book Ramsey degree-seven audit

Reviewer: **six-reviewer-2**, independent mathematical reviewer. The campaign shares a signing identity; actual authorship and independent methods are explicit.

Confirmed: every22-vertex ordinary red-B4/blue-B7 avoiding graph has at most one red degree-seven vertex; if present, it forces105–115 edges. This confirms two committed researcher theorems. The global Ramsey interval remains22–23; no endpoint realization or general graph enumeration is asserted.

Read [the complete review](REVIEW.md) for the universal mathematical bridges, credited dependencies and strengthening opportunities. [INPUT.json](INPUT.json) pins both source versions. [VALIDATION.json](VALIDATION.json) records independent and author replay checks. The checker uses standard-library Python3.11+ and no target imports, external catalog, solver or numerical eigensolver.

From the repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 book_ramsey_4_7_degree7_review2/audit.py \
  --expected book_ramsey_4_7_degree7_review2/expected.json
```

The identical check also passes under `python3 -O`. It independently generates all553normalized cubic-eight graphs and552negative-principal-minor certificates, proves exact spectra for seven normalized cubic-six graphs, validates the rank and moment controls, and audits the stronger edge theorem through a separate analytic-proof control module. All30Fano systems and465unions are generated as arithmetic fixtures; this is expressly not a classification of every twofold triple system. Written analytic reasoning provides the universal coverage for the stronger edge bound.

Deterministic expected-output SHA256: `5e74bf13ab286c0c2407744466728997646c2703f28b1b38daf72114f800a7bf`. Independent normal runtime3.465s, optimized3.636s. The cumulative child RSS upper bound is22,148KiB. All12malformed controls remain active under optimization. No large inputs or generated corpus are published. The standalone output is compact and deterministic.
