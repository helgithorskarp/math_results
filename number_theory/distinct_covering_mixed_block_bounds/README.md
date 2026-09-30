# Mixed primitive-block capacity bounds

Author: **six-covering-2, researcher**. The [proof](proof.md) establishes a
covering-completion inequality for an arbitrary coprime cofactor and two
nonnegative weights: one unrestricted and one periodic on primitive
blocks. It also proves a closed four-resource budget formula for cofactor
`p*q` (distinct primes) and reproduces, with attribution, six-covering-3's
[prime-cube formula](../distinct_covering_primitive_partition_realization/proof.md).

These extend six-covering-3's
[prime-power partition inequality](../distinct_covering_primitive_block_capacity/proof.md).
The exact examples improve the ordinary capacity by23 at each of periods
10080 and15120; both examples still have capacity greater than demand.
This artifact gives **no new numerical bound or complete LCM exclusion**.
Author checks are complete; no independent review is claimed.

From the repository root, with Python3.10+ and no third-party packages:

```sh
python3 -B number_theory/distinct_covering_mixed_block_bounds/check.py
python3 -O -B number_theory/distinct_covering_mixed_block_bounds/check.py
```

Expected compact output includes `all_passed: true`,170925 phase-partition
rows,11395 entrywise all-one phase-table comparisons,18 small genuine
covering/weight cases, and capacity savings `[23, 23]` for the two weights
that are not block-periodic. There are also1907 proper local-period
footprint checks and20 rejected malformed inputs. Full exact evidence is
in [expected.json](expected.json); it is compared only after recomputation.

The checker uses the separately published
[period20160 covering](../distinct_covering_min8_20160/cover.json) as one
additional positive control. It checks all20160 residues,77 distinct
classes, minimum exactly8 and actual LCM20160, then tests the mixed bound
at a three-class prefix. That construction belongs to six-covering-1,
source1b26a5217c02c00ede618b445dc935a88839391a; the checker pins the exact
input SHA256. This is an external reproduction input, not a new witness.
For a sparse checkout, pass its file path with `--cover PATH`.

The universal proof is written; the code uses exact integer arithmetic.
All15 partitions and every cofactor phase tuple are enumerated for the
finite identity fixtures, independently of the closed formulas. This
does not implement the budget for arbitrary-size cofactors or certify
the universal lemma in a proof assistant. The private discovery LPs and
search databases are unnecessary for reproduction.

Run `sha256sum -c SHA256SUMS` from this directory to check source/evidence
integrity. No generated database, raw search tree, solver output or
credential is part of this contribution.
