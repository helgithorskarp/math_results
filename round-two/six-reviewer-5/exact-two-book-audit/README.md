# Independent exact-two Book audit

Actual contributor: **six-reviewer-5, independent mathematical reviewer**.
See [REVIEW.md](REVIEW.md) for the theorem, dependency boundary and proved
removal of high-high blue caps from the two-triple sector. This does not
settle the Ramsey endpoint or assert a realizable host.

CPython 3.12.14, standard library only. Set all native numerical thread
variables to 1 and run one mathematical child at a time. Each command uses
a fixed 45-second external guard; internal certificate/AC guards are also
45 seconds per case and 20 million support tests. Failure to complete is
an operational limit, never an exclusion.

```bash
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1
timeout 45 python3 check.py --check expected.json
timeout 45 python3 -O check.py --check expected.json
timeout 45 python3 first_census.py
```

The entire 1,663-byte main record has SHA256
`562fee0f83a123eaadae98a08884ba2a99fe5b3fe50991680e1ca18b901a742d`.
The first census must return all82_closed=true and whole record SHA256
`c4dba71ea2a195a23e0b8b56d019d38ffe00140ee7889f1322aca49df20d2261`.
Checks use explicit exceptions, never optimized-away assertions.

[domains.py](domains.py) reconstructs all incidence profiles, every actual
exception assignment and every high star by an 8/9 meet-in-the-middle
subset split. [propagate.py](propagate.py) is a fresh cached-support AC3
engine, written and run before reading the author code or certificate.
[first-seal.json](first-seal.json) binds those original modules and
[first-record.json](first-record.json). The later adapter
[first_census.py](first_census.py) reconstructs that whole initial record.

[replay.py](replay.py) independently replays complete unsupported sets,
starting from regenerated entire initial domains. It imports only our
modules. [credited-certificate.json](credited-certificate.json) and
[credited-expected.json](credited-expected.json) are exact credited inputs
from six-books-3's [original packet](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-books-3/exact-two108),
source commit `c3615599d76ef1b79e0302b8f7412f8b15ea65cb`. The serializer/schema
was inspected only after our independent first seal. No author executable
supplies the independent calculations. Separate late original-executable
replays are reported honestly in [provenance.json](provenance.json).

[no-high-blue-certificate.json](no-high-blue-certificate.json) is our fresh
complete certificate: 24 initial contradictions, 58 arc contradictions,
3,073 batches and 104,504 deleted stars, with **no high-high blue cap**.
Its canonical mathematical SHA256 is
`5e1201e36074c20b30a0a75c97b36b9682aaf006e2230efc152e30389ee5f047`.
It concerns the independent-low two-triple sector. The separate quadruple
sector retains a blue obstruction as explained in the review.

[controls.py](controls.py) compares all 1,476 entire initial domains to
an additional full-subset census (2,567,136 subsets), checks 291,364
literal set/bit page predicates and 19 damaged certificates, and validates
the credited [primary21.txt](primary21.txt) prior construction. Raw/full
star and deletion records (2.6/3.1 MB) stay private and regenerate in memory;
only source, compact certificates, summaries and provenance are published.

The ordinary reductions, finite completeness bridge and Python execution
remain unformalized. The universal 108-edge conclusion imports earlier
maximum-ten and rootlessness results with their exact retained premises.
