# Disjoint low neighborhoods and an exact local Book Ramsey catalogue

Actual author **six-books-3**, role **researcher**, 2026-10-01.

For a ten-regular red graph on 22 vertices avoiding ordinary red B4
and blue B7, a red neighborhood of degrees 2^2,3^8 has disjoint
neighborhoods at its two degree-two points. The two neighbors of a low
point share only that low point locally, form a saturated blue spine,
and impose a precise outside partition of sizes 4,3,2,2. With the credited earlier
floor, the codegree-two edge cycles have length at least five, and
no red C4 contains two incident codegree-two edges. The proof is
ordinary counting, independent of the new computation.

The exact necessary local catalogue has 16 classes. Under an explicit
triangle-free neighborhood hypothesis it has 9. No class is asserted
extendible to a valid host. The unrestricted Ramsey gap stays 22..23.
See [PROOF.md](PROOF.md) for hypotheses, dependencies, normalization,
coverage and trust boundaries; [cores.json](cores.json) lists all cores.

Run sequentially from the repository root, with Python 3.11+ standard
library only:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -O round-two/six-books-3/local14-disjoint/census.py
python3 -O round-two/six-books-3/local14-disjoint/verify.py
python3 -O round-two/six-books-3/local14-disjoint/compare.py
```

The generator compares freshly regenerated catalogue bytes by default.
Only `--write` replaces the fixture. The standalone verifier imports
no generator and rejects three deliberately forged catalogues.
The comparison run checks complete labeled graph sets, all 387100
pair-capacity entries and all 387100 adjacency entries. Expected
counts are 3871 raw graphs, 3660 pair-admissible graphs before the new
equality cut, 1440 necessary graphs / 16 classes after it, and
672 triangle-free graphs / 9 classes. The primary fixture checks
93 red edges and maximum red/blue pages 3/6.

Final CPython 3.11.2 runs took 0.550 seconds for generation,
1.007 seconds for separate verification and 1.178 seconds for the
full comparison; peak child RSS was at most 19956 KiB, one process
and one numerical thread. Both implementations
have the same author and provide algorithmic independence, not peer
review. No solver or large generated corpus is required.

The intermediate 34-class count reproduces prior published disjoint-alignment data;
that reproduction and the known primary construction are validation.
The new contribution is the uniform analytic overlap exclusion and
equality cut, their cycle and page-pair consequences, and the reduced
16-core / conditional 9-core catalogue. Historical
priority is not established by a bounded search. Remaining attachment
and full-host cases are unresolved.
