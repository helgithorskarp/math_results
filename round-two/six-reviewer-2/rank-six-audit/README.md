# Independent rank-six Hoffman-matrix audit

six-reviewer-2, independent mathematical reviewer, 2026-10-01.

[REVIEW.md](REVIEW.md) confirms LEMMA8893 at its mathematical scope and proves
exact cap endpoints for its four fixed boundary seeds. Every rank-six order
n>=8 also admits the construction on the eightfold larger closed interval
0<t<=1/alpha with core/whole cap floor
19906595794607/83326352186591. The infinite branch has an ordinary proof;
checking three stable orders does not establish the infinite quantifier.
General spectral Chvatal H and I are outside this result.

CPython3.11+ standard library only. From this directory:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 audit.py --output /tmp/rank-six-audit.json
python3 -O audit.py --output /tmp/rank-six-audit-optimized.json
cmp /tmp/rank-six-audit.json EXPECTED.json
cmp /tmp/rank-six-audit.json /tmp/rank-six-audit-optimized.json
python3 controls.py --output /tmp/rank-six-controls.json
python3 -O controls.py --output /tmp/rank-six-controls-optimized.json
cmp /tmp/rank-six-controls.json CONTROLS.json
cmp /tmp/rank-six-controls.json /tmp/rank-six-controls-optimized.json
```

Expected:516 rational PSD forms,16342 principal minors,43 complete seed
blocks,11 rejected damages and4 exact negative cap witnesses. Original n=8
audit:246 independent basis columns,121032 action scalars,27834 orthogonality
pairs,174 absent lifts,61009 original entries for each of two parameters.
The input TABLES.json is the author's unaltered small rational table;
PROVENANCE.json identifies and hashes the frozen source. The independent
code imports no author module. EXPECTED.json contains every rational
threshold and inverse witness; the full minor transcript is regenerated
locally and represented by a digest. No large matrix or proof corpus is a
required file.

Our PSD method uses every principal minor, rather than the author's Schur
and Bareiss implementations. The author's optional `--blocks-only` source
replay agrees with its expected record; its full large elimination was not
replayed. Normal/optimized independent runs took about10-13 seconds each,
peak below40MiB, with a fixed90-second guard and sequential jobs.
VALIDATION.json records actual versions and checks. Ordinary harmonic,
infinite-moment, rank and tensor proofs in REVIEW.md remain unformalized.

The four exact cap endpoints classify the fixed seed/trade family only.
At an active endpoint its cap remains PSD but unit multiplicity becomes2,
so that endpoint is excluded from the simple-unit product statement.
Signed matrix entries and the empty loop are part of the normalization.
