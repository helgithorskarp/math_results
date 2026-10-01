# Complete four-nine certificate and ordinary 108-edge rootlessness

Actual author **six-books-3**, role **researcher**, 2026-10-01.

The new exact core excludes a full Petersen root in an ordinary valid
22-point graph with108 red edges, maximum degree ten and degree multiset
`9^4,10^18`. With credited8828 and the rooted finite parts of8941/8979/9041,
**every maximum-ten108-edge graph is rootless**. The upper-degree part of8012
removes the explicit maximum-ten hypothesis. Rootless means no degree-ten
point whose ten red neighbors are all degree ten. The rootless108 sectors
and Ramsey interval22..23 remain open. [PROOF.md](PROOF.md) gives the full
ordinary/finite arguments and exact import boundaries. New peer review and
formalization are pending.

From the repository root, run **sequentially** with all native threads one:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
timeout 45s python3 round-two/six-books-3/four-nine108/produce.py
timeout 45s python3 round-two/six-books-3/four-nine108/verify.py
timeout 45s python3 round-two/six-books-3/four-nine108/controls.py
timeout 45s python3 round-two/six-books-3/four-nine108/controls.py --summary-only
timeout 45s python3 -O round-two/six-books-3/four-nine108/produce.py
timeout 45s python3 -O round-two/six-books-3/four-nine108/verify.py
timeout 45s python3 -O round-two/six-books-3/four-nine108/controls.py
timeout 45s python3 -O round-two/six-books-3/four-nine108/controls.py --summary-only
```

CPython3.11.2 standard library only, no solver or private data. Each job
completed within the fixed45-second guard and unchanged1CPU/2GiB scope.
Never interpret timeout or incomplete enumeration as exclusion. Default modes
compare full [expected.json](expected.json) records; all mathematical/schema
guards remain active under -O. Both integrity modes are required. Normal runs
write only optional Python caches and temporary control files under /tmp.
`produce.py --derive --output PATH` explicitly regenerates the certificate;
`--derive` omits only frozen-summary comparison. The checker accepts
`--certificate PATH --expected PATH` while retaining mathematical checks.

The producer uses full-column/base-eight low-pair joins. The independent
checker uses literal P, eleven canonical full-large tuples, different
low-pair quotient joins and unique star-multiplicity recovery, then expands
every local relabeling. Their complete sets match **55,080 keys entrywise**.
The checker independently verifies all478 supplied templates and their
complete raw union, and literal22-point sets rebuild every outside star.
448 templates are initially empty;30 have complete static pair-support
covers. Weighted coverage is51,710+3,370;50 groups cover216 target stars.
No propagation, branching, all-other-rootP or host symmetry is used.

The complete low pool retains all582 words of sizes5/6/7. Four equal
one-tag words are sorted numerically with repetitions considered, rather
than by size. The primary21 positive control accepts ten actual stars and
the actual completion;196 asymmetric changes reject.27 damaged certificates
and one forged narrowed summary reject. Separate author algorithms are not
independent peer review. [provenance.json](provenance.json) records exact
premise roles; [manifest.json](manifest.json) hashes every other source file.

Canonical incidence digest:
`7e6367f5996a84527e2fcd43927def7806a136c1cb7c22185a1f17fdee377569`.
Canonical certificate digest:
`5bdeb920b929a0104cddca836292358ee3fcee3088c666566cbc6fe5ef7b4e77`.
The compact [certificate.json](certificate.json) contains only local
representatives, exact domain sizes/hashes and static obstruction lists.
Every omitted raw incidence/star corpus is regenerated from the source.
The exhaustive algorithms and ordinary coverage arguments establish the
claim; hashes record agreement.
