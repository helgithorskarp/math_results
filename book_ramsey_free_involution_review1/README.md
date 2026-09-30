# Independent Book Ramsey free-involution review

**six-reviewer-1**, independent mathematical reviewer, 2026-09-30.
[REVIEW.md](REVIEW.md) independently confirms the two-red/seven-total
uniform-pair theorem for every fixed-point-free color-preserving involution
of an ordinary red-B4/blue-B7-free coloring on 22 vertices.

It proves **four blue uniform pairs**, restricting seven-pair color counts
to **two red/five blue** or **three red/four blue**. Two short Gram-action
certificates eliminate the six-pair shapes, with sharp squared residual
minima16 and16/5 in the stated abstract operator relaxations. These are
unformalized ordinary proofs, not an unrestricted Ramsey resolution.
The located R(B4,B7) interval remains22..23.

[audit.py](audit.py) imports no author executable. It checks all66048
three/four-orbit lifted graphs, a reduced complete696150-pattern census,
56 surviving necessary unsigned patterns and all3584 inside assignments,
16 no-red clique partitions,720 A-row and2160 B-row cases, and the new
four-blue and exact Gram/residual certificates. Expected output is compact
and reconstructs every surviving flag assignment. These finite checks
validate the written proof; they do not enumerate every22-vertex graph or
every matching signing.

From the repository root, CPython3.11+ and the standard library suffice:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -B -O book_ramsey_free_involution_review1/audit.py \
  --check book_ramsey_free_involution_review1/expected.json
```

Canonical output SHA256:
`8806f5573cd8f4962ade71c10b3e8d1b735205906c5d64990ae8d75bb12edef6`.
Normal and optimized outputs agree. Optimized runtime8.065s/21216KiB;
normal full check with optional author comparison7.994s/18372KiB.
All guards are explicit. Four altered records must reject under both modes.

An optional entrywise comparison reproduces the author's separate C++
census and checks all56 surviving patterns and3584 flag entries:

```sh
mkdir -p /tmp/book-involution-review-comparison
g++ -std=c++17 -O2 -Wall -Wextra -Wpedantic \
  book_ramsey_b4_b7_free_involution/census.cpp \
  -o /tmp/book-involution-review-comparison/census
/tmp/book-involution-review-comparison/census 6 \
  /tmp/book-involution-review-comparison/survivors.jsonl
python3 -B book_ramsey_free_involution_review1/audit.py \
  --check book_ramsey_free_involution_review1/expected.json \
  --compare-author-records /tmp/book-involution-review-comparison/survivors.jsonl
```

The comparison is optional; the independent check regenerates every
mathematical datum. GNU C++12.2.0 produced the author's full published
3858660-pattern summary exactly. A five-pair diagnostic passed ASan/UBSan.
Only this optional comparison trusts the compiler. The author's larger
formula-control suite was not rerun. Builds, raw survivor lists and logs
stay in scratch; none is required by the independent proof or publication.

[provenance.json](provenance.json) pins the reviewed source and records
methods/resources; [SHA256SUMS](SHA256SUMS) covers every other contributed
file. The source contains no large corpus or third-party dependency.
