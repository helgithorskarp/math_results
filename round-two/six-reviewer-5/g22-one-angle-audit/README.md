# G22 independent facial audit

six-reviewer-5, independent mathematical reviewer. Confirms9562 and proves
injectivity on closed c=[1/2,3/5] with only the pentagon angle at name7<=pi;
the remaining four angles are unrestricted. Actual faciality and the specified
pattern remain hypotheses. [REVIEW.md](REVIEW.md) is the complete ordinary
proof and [RESULT.json](RESULT.json) is the compact full mathematical record.
The conditional fifteen-point corollary retains9515 on its original domain.

Use Python3.11+ standard library; actual environment CPython3.12.14. From this
contribution directory run serially, one native thread and fixed45s per job:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
timeout 45s python3 reproduce.py
timeout 45s python3 -O reproduce.py
```

Both regenerate and compare the entire record with canonical hash
`0f41081e55dc16664b03cead1b5d920815f37b563f777d2dc6b4b0cb7b337c72`.
The independent core imports no author code or certificate. It enumerates the
whole8^6 cube, filters all37633 partial injections, uses rotation subset DP,
and expands literal integer-coefficient Sylvester determinants. It regenerates
all original/wider closed-band sign certificates and controls.

To independently write a fresh record, use an existing local scratch directory:

```bash
mkdir -p out
timeout 45s python3 reproduce.py --write out/fresh.json
```

Optional late entry-level comparison requires the original pinned source
commitb0b8df3d6be363bb8f1bf4e1448c78bafe578aa6. In a checkout containing its
original directory, the default is inferred correctly. Otherwise provide that
directory explicitly (the downloaded code must be that exact public source):

```bash
timeout 45s python3 compare_author.py /path/to/pinned/g22-facial-injectivity
```

This comparison imports the original producer, so it is corroboration only.
All original source pins, chronology, actual guarded runs and primary hashes
are in [SOURCE-CREDITS.json](SOURCE-CREDITS.json) and [VALIDATION.json](VALIDATION.json).
No private ledger, key, large proof corpus or solver is needed. No global
Tammes15 occurrence/optimality/equality theorem is asserted.
