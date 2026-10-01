# Independent all-unit high-core review

**six-reviewer-2, independent mathematical reviewer**, 2026-10-01.

This package independently confirms that a twenty-quadruple pair packing on
17 points with replication multiset \((4^5,5^{12})\) has at most six leave
edges among its replication-four points. It also closes the unreviewed
eight-edge exclusion needed for the preceding bound of seven.
[REVIEW.md](REVIEW.md) gives exact hypotheses, complete reductions and boundaries.

The package separately supplies 256 affine-derived positive packings with
four high-core edges and three provably different intrinsic profiles.
The local extremal value lies in 4--6; sharpness at six is unresolved.
The unrestricted coding interval remains \(69\le A(18,6,5)\le72\).

CPython 3.11.2, g++ 12.2.0; standard libraries only. From the repository root,
run these **sequentially**, with OMP_NUM_THREADS, OPENBLAS_NUM_THREADS,
MKL_NUM_THREADS and NUMEXPR_NUM_THREADS all set to one:

```sh
python3 -B constant_weight_unit_core_review2/audit.py --work /tmp/unit-core-normal
python3 -B constant_weight_unit_core_review2/check_fixtures.py
python3 -B -O constant_weight_unit_core_review2/audit.py --work /tmp/unit-core-optimized
python3 -B -O constant_weight_unit_core_review2/check_fixtures.py
```

Both audit commands rebuild every carrier and all 3,695 matrices, check all
12,745 certificate nodes literally, and independently search every matrix
with the reviewer-owned point-partition kernel. They compare the complete
stable record against [expected.json](expected.json); timings/RSS are separate.
The fixture command rebuilds all 256 packings and compares the three explicit
fixtures and exact profile counts with [fixtures.json](fixtures.json).

Four external runtime JSON files are consumed from the default sibling
`constant_weight_18_6_5_equality_structure`. They are small expected summaries
and the already published rejection trees. [INPUT.json](INPUT.json) records
their exact historical commit and byte hashes, plus previous reviewer reuse.
If main later changes those inputs, use `--target PATH` with the pinned copies.
No target-author executable module is imported, compiled or run.

The zero-block incidence assignment differs from both published generators.
The actual leave groups and two-stage orbit strategy share the mathematical
reduction, with independently written enumeration and full literal checks.
The native kernel is an explicit 17-point/136-pair layout extension of this
reviewer's previous kernel; the search algorithm and guards are unchanged.
Address/undefined-behavior sanitizers check the highest pair bit on a genuine
positive instance and an actual negative proof matrix.

Every claimed search completes below the unchanged 200,000-state/ten-second
local guards. A guard failure reports INCOMPLETE and yields no exclusion.
`--record` explicitly writes a new expected baseline and is not a comparison.
The normal baseline took 42.03 seconds and the optimized comparison 68.37
seconds in this campaign; costs vary by host. All work data and binaries stay
under the requested scratch directory. See [VALIDATION.md](VALIDATION.md).
