# Independent local-fourteen audit

Actual author **six-reviewer-4**, independent mathematical reviewer. The original claim and copied integer cuts are by **six-books-3**, researcher. Shared graph signatures do not distinguish these authors.

[REVIEW.md](REVIEW.md) verifies committed lemma 8638, reference `bafkreidkxsdjhx2pheg3xcq5ujblspc2l4gi5fftsj623vb7pmb2g47we4`, at author commit `0efb5185b1880be9a29f76ae05f206a8baf60368`. A valid ten-regular ordinary red-B4/blue-B7-free graph on 22 points cannot have a neighborhood of degree sequence 2²,3⁸. The global red-codegree-three conclusion uses explicitly credited older premises; no full regular-host exclusion or unrestricted Ramsey endpoint is established here.

The independent checker regenerates all 672 normalized triangle-free local cores, verifies generic graph-isomorphism coverage by nine representatives, checks all integer cuts on complete row domains, and reconstructs all 130 residual incidence matrices by integer multicover. Its 130 two/three-column inequalities then exclude every outside-star possibility without enumerating stars. No author program is imported.

CPython 3.11+ standard library is sufficient; validated version 3.11.2. From the repository root, run sequentially:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B round-two/six-reviewer-4/local-fourteen-audit/audit.py
python3 -B -O round-two/six-reviewer-4/local-fourteen-audit/audit.py
```

Both commands print `status: PASS`, 672 aligned triangle-free cores, 130 incidence matrices, and 130 compressed obstructions (128 of size two, two of size three; margins one:124, two:6). The optional author comparison is null without external author data. Normal and optimized complete comparisons took about 25/22 seconds and less than 30 MiB of measured child RSS. Run one job at a time.

`expected.json` is a checked complete result record, not a trusted enumeration input. `cover-cuts.json` supplies `[outside-row-index, subset-bit-word]` certificates in the regenerated sorted matrix order. Every strict inequality is checked from literal page identities. `cuts.json` is an exact credited copy of the original author's nine certificates; every sign, coefficient, row score, and right-hand side is verified. `SHA256SUMS` covers the other compact files.

To regenerate compact output into local scratch:

```bash
python3 -B round-two/six-reviewer-4/local-fourteen-audit/audit.py --emit > /tmp/local14-expected.json
python3 -B round-two/six-reviewer-4/local-fourteen-audit/audit.py --emit-cover-cuts > /tmp/local14-cover-cuts.json
```

Optional complete entrywise comparison reads only the author's JSON fixtures. Obtain `incidences.json` and `expected.json` from the exact author commit above, preserving their filenames in a local directory, then run:

```bash
python3 -B -O round-two/six-reviewer-4/local-fourteen-audit/audit.py --author-source /tmp/pinned-local14-author
```

The pinned author `incidences.json` file SHA256 is `cf4c9381d29cbf6937ae663e879a00da514118d0377093c1bdecbf5500f79d35`; its `expected.json` file SHA256 is `6bd1402047091c395dadd74eda239c622d90d5e42b2a2c3fccba05aad3746a7b`. Their [reader-facing directory](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-books-3/local14-exclusion) can change as main advances; the exact recorded commit identifies the audited snapshot. A comparison checks all 130 matrices/14,300 binary entries, nine core profiles, and all capped high-multiset counts.

`VALIDATION.json` records normal/optimized runs, three damaged-input rejections under optimized Python, native author replays, pinned author hashes, and exact finite output. The matrix-stream digest is `7e9c728b3c4e2fb0ad768e43f5a2aaffb543a4036b2e727f3ec14e652cfdb194`; the 672-core stream digest is `a79ef5d8047a18c433f415b48bf75f4ceadda24bf9bc622ea7e99c6e71e782f7`. Stream digests use compact JSON values followed by a newline. File digests also depend on formatting.

The proof's trust boundary is exact Python execution and the written reduction/completeness arguments, not a proof assistant. No solver, approximate infeasibility, external graph catalogue, timeout, omitted large proof corpus, or incomplete search supplies an exclusion. The older credited global premises are not rerun by this checker.
