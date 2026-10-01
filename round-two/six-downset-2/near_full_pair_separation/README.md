# A cap separation on D(16,14)

**six-downset-2, researcher.** An exact finite certificate excludes every real
centered capped H matrix on the sets of size at most 14 in [16] when all
noncomplementary disjoint weights between sizes at least 3 are zero. A broader
rational centered seed exists; a closed affine repair interval attains the
universally greatest lower rank 65503 and a simple unit eigenvalue.

The domain includes the empty vertex and its allowed loop. The cap is the
additional inequality M <= I, not Conjecture I. Centering is an extra hypothesis
on the obstruction. General H/I and an unbounded version of this separation are
unclaimed. Ordinary near-cube H and its maximal rank are already prior results;
the new content is the stated centered support separation and the explicit
capped witness. [PROOF.md](PROOF.md) gives definitions, complete hypotheses,
bridges and precise prior-art citations.

## Replay

Only Python's standard library is needed; checked with **CPython 3.12.14**.
Run these commands from this directory. All mathematical jobs were serial,
with solver/BLAS/OpenMP threads set to one. No solver is used by the checker.

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B verify.py --check expected.json --output /tmp/near-full-normal.json
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B -O verify.py --check expected.json --output /tmp/near-full-optimized.json
cmp expected.json /tmp/near-full-normal.json
cmp /tmp/near-full-normal.json /tmp/near-full-optimized.json
sha256sum -c SHA256SUMS
```

Expected compact stdout in each mode:

```json
{"ok": true, "result_sha256": "400396a7fec325eefe383cdc0f0462d85db2628297124ec49ea221010b4daf5d", "complete_n16_blocks": 27, "dual_blocks": 2, "literal_order": 57, "controls": 8}
```

Each run compares its full output with the **pre-existing** frozen
[expected.json](expected.json), not just this displayed summary. File hashes
are in [SHA256SUMS](SHA256SUMS); runtime metadata and pinned prior sources are
in [provenance.json](provenance.json). Expected results are regenerated from the
actual certificate data, not trusted as an input proof.

## What is checked

- Two 14-by-14 rational positive duals cancel all six arbitrary real complement
  parameters and give a strictly negative constant, excluding the entire
  restricted affine face. The negative proof only needs two necessary upper
  forms; it does not require higher-harmonic completeness.
- The seed's 36 rational coordinates are recovered by both elimination and a
  separate direct completion. All nine complete sectors at the seed, midpoint
  and closed repair endpoint pass integer Bareiss and rational Schur PSD/rank
  checks. The ordinary completeness and convexity bridges prove full matrices
  and every real repair parameter, rather than extrapolating from samples.
- The credited published D(6,4) baseline is checked on literal order-57 matrices,
  including original support, rows, stars, empty loop, ranks and 16 layer-action
  columns. Each PSD algorithm separately agrees with the all-principal-minor
  criterion on all 729 symmetric ternary matrices of order 3. Eight deliberate
  damage or resource-guard controls reject in normal and optimized modes.

## Files and trust boundary

| File | Purpose |
|---|---|
| [PROOF.md](PROOF.md) | Ordinary proof, scope and credited prior results |
| [seed.json](seed.json) | Compact exact positive seed and repair endpoint |
| [dual.json](dual.json) | Compact exact two-block exclusion certificate |
| [model.py](model.py) | Affine equations, complete sectors and small literal lift |
| [exact.py](exact.py) | Integer Bareiss and separate rational Schur arithmetic |
| [verify.py](verify.py) | Decoder agreement, certificates, baseline and controls |
| [expected.json](expected.json) | Frozen full deterministic evidence |
| [provenance.json](provenance.json) | Author, scope, versions and source pins |
| [SHA256SUMS](SHA256SUMS) | Hashes of the compact source and evidence |

The 65519-by-65519 matrices are defined by their entry formulas and complete
sector decomposition; they are never allocated. The ordinary bridges are
unformalized. Two arithmetic implementations and the independent affine
decoder are same-author checks, not an external peer verdict. Floating searches
only proposed fixtures and are outside the proof boundary. No solver failure,
infeasibility status, timeout, extrapolation, private ledger or omitted large
corpus is a premise. Only this compact source and evidence are published.
