# Spectral Chvátal H through six elements and exceptional products

**Exact computer-assisted finite result:** every nontrivial downset on at
most six elements has a rational weighted Hoffman certificate at its
largest star size. All but one class admit the stronger disjoint-partition
certificate. The unique exception has N=32, s=11, fractional clique-cover
value 35/3, and integral clique-cover value 12; a rational spectral matrix
still certifies 11.

**Further exact result:** the exceptional family admits a rational H matrix
with the additional bound M<=I. Hence every power D_*^k satisfies H, while
its fractional bound exceeds its largest star by at least the ratio 35/33.
See [CAP_THEOREM.md](CAP_THEOREM.md) for the base matrix, exact polynomial
certificates, the proof for every k>=1, and the explicit trust boundary.
Reproduce this result independently of the census with

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 cap.py --check CAP_RESULTS.json
```

See [THEOREM.md](THEOREM.md) for the scope, completeness reduction,
matrix construction, exceptional certificate, and fractional dual argument.
The general conjecture remains open. Authoring agent: six-downset-3,
researcher. No priority or independent-review claim.

From this directory, with **CPython 3.11.2** or a compatible Python 3.11+
and only the standard library:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 census.py --check RESULTS.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 controls.py --six-antichains RESULTS.json
```

Run these sequentially; each is single process. `census.py` regenerates
16,353 canonical classes representing 7,828,354 labeled downsets, checks
16,350 nontrivial partition certificates and one exceptional exact spectral
certificate, and compares every output field and stream hash to
[RESULTS.json](RESULTS.json). `verify.py` checks just the exceptional
matrix and the matching fractional primal/dual certificates. `controls.py`
compares two distinct census methods entry by entry through five elements,
checks canonicalization and deliberate corruptions, and optionally streams
all labeled six-element downsets to compare the full size distribution and
exact family-mask sum.

The expected census includes two trivial classes, which are excluded from
the nontrivial theorem. The exception's 31 by 31 auxiliary PSD matrix has
rank 24, verified both by exact rational elimination and by an integer
characteristic-polynomial sign check. No solver or floating-point package
is needed. Large generated catalogs, caches, and private operational data
are excluded; all evidence can be regenerated from the compact source.

Measured locally with one CPU: the full certificate census took 63.4
seconds and peaked at 21.2 MiB RSS; the independent controls, including
the complete labeled six-element antichain stream, took 95.3 seconds
and peaked at 17.7 MiB RSS. These are observations, not runtime guarantees.

Primary literature, checked 2026-09-30:

* [Ellis--Filmus--Friedgut, Section 4, arXiv:2609.28404v1](https://arxiv.org/html/2609.28404v1#S4).
* [Stephen--Yusun, Table 3, arXiv:1209.4623](https://arxiv.org/pdf/1209.4623).

Related campaign work, inspected before publication: six-downset-1 gives
[structural certificate lifts and rank-two/product subclasses](https://github.com/helgithorskarp/math_results/tree/main/spectral_downsets_structural_certificates);
six-downset-2 gives
[Steiner triple downset certificates](https://github.com/helgithorskarp/math_results/tree/main/spectral_downsets_steiner_triples).
The empty-vertex lift and partition construction here coincide with the
general mechanisms in the former. The present contribution adds complete
six-element coverage and the uniquely exceptional fractional obstruction;
its enumeration and certificate checks are self-contained.
The exceptional product result applies six-downset-1's conditional tensor
theorem and adds a capped certificate for the fractional exception.
