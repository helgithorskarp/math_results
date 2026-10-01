# A sharp matched unit-hub barrier for A(18,6,5)

**six-code-2, researcher, 2026-10-01.**

An eighteen-point family of five-subsets has minimum binary distance six
when distinct blocks intersect in at most two points.

**Exact computer-assisted theorem.** Suppose such a family is invariant
under a fixed-point-free involution. At a point occurring in twenty blocks,
suppose the shortened quadruple packing has replication profile
`(4^5,5^12)`, its mate is one of the five replication-four points, and
the pair leave on those five points is `K1,4` centered at that mate.
Then the entire family has **at most 60 blocks**. The bound is attained.
There is no assumption on its other point replications or its total size.

The [proof](PROOF.md) gives the complete normalization, three exact-cover
fibers and two completion graphs. The fiber counts are **48,96,0**.
Their actual permutation orbits cover two classes of compatible
36-block anchors. Each has completion clique number twelve. The two
[60-block witnesses](witnesses.json) meet the hypotheses directly.

This excludes the specified motif from a proposed 70-block construction
with this involution. It does not exclude other involution-invariant
families or arbitrary 70/71-block codes. The maintained primary
[table](https://aeb.win.tue.nl/codes/Andw.html) still records 69--72;
the separately published and reviewed campaign
[upper bound](../../../constant_weight_18_6_5_equality_structure/UPPER71.md)
gives 69--71. Neither interval changes here.

## Reproduce

From the repository root, using Python **3.11.2** and g++ **12.2.0**:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 -B round-two/six-code-2/involution_unit_hub/reproduce.py
```

The standard library and a C++20 compiler are the only dependencies.
The command builds one native job at a time. It completely regenerates
both models, compares every cover and actual group element, verifies both
witnesses, and compares every maximum completion against a different
pivot search. Generated matrices, complete cover/maxima corpora and
binaries go to `scratch/involution-unit-hub`, outside this contribution.
Use `--work-dir PATH` to choose another scratch directory.

Expected: `COMPLETE`, maximum words60, two classes, root counts48/96/0,
completion maxima12/12 and completion counts5274/2, all entrywise checks
true, and eight controls passed. [expected.json](expected.json) pins the
actual model, cover, group, graph and maximum-family hashes.

The following runs also check optimized Python semantics and address/
undefined-behavior sanitizers on all native proof fibers and graphs:

```sh
python3 -B -O round-two/six-code-2/involution_unit_hub/reproduce.py --work-dir scratch/involution-optimized
python3 -B round-two/six-code-2/involution_unit_hub/reproduce.py --sanitizers --work-dir scratch/involution-sanitized
```

No solver, floating-point arithmetic, external mathematical data or large
published certificate is needed. This is an author computer-assisted
proof with explicit source/runtime and ordinary completeness bridges.
It is not a proof-assistant formalization or an independent peer review.
