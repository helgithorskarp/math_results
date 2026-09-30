# Spectral Chvátal H: finite classifications and capped certificate ranks

**Sparse rank trades:** rational perturbations on disjoint
singletons and pairs raise a centered H certificate to the largest
possible rank, under the exact kernel and strict-cap hypotheses in
[KERNEL_TRADE_PROOF.md](KERNEL_TRADE_PROOF.md). It gives maximal-rank
capped certificates for every uniform rank-two downset on n>=4 points.
The two-singleton template also gives maximal-rank caps for every
friendship downset with at least two triangles and every two-center
downset with at least two independent leaves.
The two-center maximal-rank conclusion was also established in an
already committed independent review, using a stronger nonnegative
off-diagonal construction; it is credited in the proof.
The proof also classifies equality from a star/empty kernel, with the
three-point triangle downset as its sole exception, and gives a cylinder
classification for all strict capped products with simple unit endpoints.
The trade's all-orders Steiner application is an alternative to the
already published, credited convex-mixture rank repair.

Reproduce its 19 exact base audits and 18 perturbed matrices from the full
repository root, using Python 3.11+ and the standard library:

~~~bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -O spectral_downset_six_exact/kernel_trade.py --check spectral_downset_six_exact/KERNEL_TRADE_RESULTS.json
~~~

The verifier reads the small public two-STS9 fixture in the sibling
contribution. For an isolated export, pass its local path with --two-sts9.
All other new checks use generated matrices and explicit exceptions.
The final run took 81.84 seconds and 34,852 KiB RSS, with one CPU.
The infinite construction and equality theorems are written proofs;
the finite audits are implementation validation.
The separate --boundaries-only mode checks two attributed nine-point
examples: it sharpens their centered rank bounds to 71 and 74 and proves
that the full trade fails at every nonzero parameter. It constructs no H
matrix for those examples; see
[KERNEL_BOUNDARY_RESULTS.json](KERNEL_BOUNDARY_RESULTS.json).

**Regular triple classification:** every nonempty regular triple collection
on six points, with the full two-skeleton included, has a rational H
certificate also satisfying M<=I and having maximal possible rank.
The complete cohort consists of 34 permutation classes representing
3,435 labeled collections. Its maximum intersecting families are precisely
the six coordinate stars. These capped certificates also cover all finite
mixed products, with their complete maximum-family classification.
An [independent review](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_regular_six_review5/REVIEW.md)
confirms this result. It also credits the previously known classical
base equality classification; capped spectral certificates and their
ranks are the separate claims here.
See [REGULAR_SIX_PROOF.md](REGULAR_SIX_PROOF.md) for the scope, kernel
lemma, exact separation from convex partition templates, and mixed fractional
obstructions. Reproduce the new finite classification with

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 regular_six.py --check REGULAR_SIX_RESULTS.json
```

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
The regular triple result adds 34 exact maximal-rank capped bases, a kernel
lemma classifying their extremizers and mixed products, and a linear
obstruction to every convex mixture of partition lifts for eight classes.
The disjoint-pair trade now supplies a conditional rank-lifting mechanism
and all-orders uniform rank-two, friendship and two-center maximal certificates. Prior source
dependencies and concurrent Steiner/two-center overlap are credited
explicitly in its proof.
