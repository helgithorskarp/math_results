# Conditional minimum-lock certificate

**six-sorting-1, researcher**, 2026-10-02. The literal 26-comparator
`B23;(1,3);(2,4);(1,2)` has no standard sorting completion of total size
at most 44, with no suffix depth restriction. [PROOF.md](PROOF.md) proves
the invariant and its scoped application. The full thirteen-input gap is
still 44..45. No exact minimum 45 for this prefix is claimed.

CPython **3.11.2**, standard library only; tested with one process and
one native thread. From the repository root:

```sh
python3 -B round-two/six-sorting-1/conditional_minimum_lock/generate.py
python3 -B round-two/six-sorting-1/conditional_minimum_lock/verify.py
python3 -B -O round-two/six-sorting-1/conditional_minimum_lock/generate.py --output /tmp/minimum-lock-certificate.json
python3 -B -O round-two/six-sorting-1/conditional_minimum_lock/verify.py --certificate /tmp/minimum-lock-certificate.json
```

Each stage was run serially with a 55-second process timeout and
`OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=NUMEXPR_NUM_THREADS=VECLIB_MAXIMUM_THREADS=1`.
No stage approached that guard; both verifier modes took about 0.53s.
There is no SAT solver or search-depth parameter. Keep native library
threads at one if reproducing inside the campaign resource scope.

The verifier prints `CONDITIONAL_MINIMUM_LOCK_PREMISES_VERIFIED`, lower
bound 45, physical locked port 2, exact eleven-variable final minimum DNF
`[2047]`, 2048 original free assignments, twelve incident controls and
fourteen rejected damages. Excluding `seconds` and `maximum_rss_kib`,
its output equals [expected.json](expected.json). Normal/optimized
producers regenerate byte-identical certificate SHA256
`afc2d7cab06f8574f78a5c4aedc5c28b3978847ad8a0ed942ea7c8b1e38137d2`.
The certificate is 3637 bytes and the fixture is hash-pinned in both
programs. The standalone checker imports no producer, sibling or graph
module; its numeric rank and DNF algorithms separately derive every
finite premise. A checksum alone is never accepted as a mathematical
route, minimum or sorting check.

The eleven-input lower bound 35 is imported from Harder's primary paper;
the historical large proof corpus is omitted and not rerun. Positive
checks test a 35-gate eleven-input sorter on all 2048 inputs and a
71-gate completion of this prefix on all 8192 inputs. The ordinary
minimum-lock argument covers all future preparations. Same-author
algorithmic independence, no external-person review and no formalization
are claimed. Exact source ancestry is in [SOURCE-CREDITS.md](SOURCE-CREDITS.md).
