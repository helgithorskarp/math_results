# Two-deletion kappa=1/8 certificate

six-downset-3, researcher. Author-checked, unformalized; independent
review pending. See [PROOF.md](PROOF.md) for the statement, ordinary
bridges, prior credit and limitations.

For every integer q>=7, take the full two-skeleton on a,b,c and q
outside points, and all triples containing at least two core points
except exactly two bcx triples. The new kappa=1/8 table gives a rational
capped H matrix on the whole downset, with greatest lower/upper rank
N-1 and a unique maximum a-star. It closes q=7,8,9 beyond the prior
fixed-kappa sufficient condition. The closed repair interval and
quantitative gap are proved for all q>=7, together with products of
these factors. General Spectral Chvátal H and I remain open.

Use Python3.11+ and standard-library arithmetic. The only external
source inputs are four small files in the sibling `triangle-majority`
directory, pinned before import by [bootstrap.py](bootstrap.py).
The manifest records all source and helper bytes. From a checkout:

```sh
cd round-two/six-downset-3/two-deletion-kappa
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O verify.py
sha256sum -c SHA256SUMS
```

Both replays print PASS and the same records SHA256:

```
914794c18a2af212e272e28f31ab7866e55dce9587400b865d402bbf8d041420
```

Expected coverage:15 unbounded floor determinants,18 upper margins,
2 cap positivity records, full orders76/90/105 with ranks75/89/104,
18 original base action columns,10 secondary characteristic-polynomial
forms,55578 full-entry comparisons and25 rejected damage controls.
[EXPECTED.json](EXPECTED.json) stores compact frozen exact coefficients
and records; the checker regenerates and checks them before comparison.
[RESULTS.json](RESULTS.json) records completed normal/optimized replays
(about18s each, maximum child RSS27200KiB, one job, threads1).

For a single matrix entry at any integer q>=7, no full allocation is
needed. Core masks are a=1,b=2,c=4; deleted triples are14 and22.

```sh
python3 -c 'from entries import entry; print(entry(7,0,0))'
python3 -c 'from entries import entry; print(entry(1000000,1,3))'
```

These print1331/2652 and0. The entry API takes exact rational repair
parameters, defaults to the endpoint, and rejects invalid set masks.
The literal full-matrix checker separately enforces q<=9. A large-
parameter entry test is formula validation, not evidence for unbounded
positivity. The coefficient signs and ordinary completeness/energy
arguments supply that proof. Different exact algorithms here are by
the same author and do not constitute independent peer review.
