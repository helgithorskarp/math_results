# Sharp58 for two saturated(2,2,1) rows joined at multiplicity three

Agent: **six-code-3**, role **researcher**, 2026-09-30.
Status: exact computer-assisted restricted maximum, with a separate
same-author replay and explicit attainment. No independent peer review or
proof-assistant formalization is claimed.

Let F be distinct five-subsets of an eighteen-point set, with intersections
at most two. Write r_x for point replication, lambda_xy for pair multiplicity
and t_xy=5-lambda_xy. If r_x=r_y=20, lambda_xy=3, and both positive deficit
rows are(2,2,1), then **|F|<=58**, sharply. Other deficit neighbors may coincide
between the two rows. No condition on their replications, packing automorphism,
incumbent or retained core is imposed.

The source also completely classifies a twenty-block four-subset packing on
seventeen points whose replications are3,3,4,5^14. There are two unmarked
isomorphism types and three types when one replication-three point is marked.
The high-core triangle leave is unrealizable. These are actual block
classifications, extending the necessary leave catalogue; the elementary
degree/leave calculation itself is baseline mathematics.

See [PROOF.md](PROOF.md) for all completeness and normalization bridges,
[witness58.json](witness58.json) for attainment, and [expected.json](expected.json)
for compact deterministic replay information. Coordinate0 is the least
significant bit. In acl69.txt it is the rightmost binary digit.

## Reproduction

Tested with CPython3.12.14 and g++12.2.0, C++17, using only the standard
libraries. Run sequentially from this directory, with one CPU-intensive
job at a time. Generated domains, matrices, binaries and detailed outputs go in
the supplied workspace or temporary directory, outside the source repository.

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 -B generate.py --work-dir /tmp/double221-replay --check expected.json
python3 -B verify.py --work-dir /tmp/double221-replay
python3 -B audit.py --work-dir /tmp/double221-replay --sanitizers
```

The generator rebuilds629 high-block cases, three marked templates,
148 actual second stars in31 symmetry cases, and the exact residual maxima.
The checker regenerates the degree graphs by neighborhood DFS, the first
stars by fixed-pair set enumeration, all58,786,560 label maps by a complete
permutation scan, and every residual graph by triple incidence. Its separate
binary conflict search excludes every residual22-word extension. Both
implementations validate the58-word fixture directly.

Native search and Python enumeration guards are200000 nodes and ten seconds
per mathematical case or triple-anchor fiber. The scan checks exactly5040
full permutations per anchor. All proof cases complete. An incomplete run,
guard failure, resource failure or interrupted output establishes no exclusion.
Runtime summaries and incomplete checkpoints remain in the supplied work
directory. Expected counts/digests are replay metadata, not standalone
exclusion certificates; the source must be rerun.

The production residual maxima on31 representative unions are16/17/18/19/20/21
in4/3/9/5/7/3 cases. The separate checker proves their common upper21 and checks
attainment21 in the supplied fixture. It does not claim a separate audit of
every smaller case maximum. Source generation takes about22 seconds; the
complete independent replay takes about17 seconds on the research CPU.
Detailed measured time/RSS is saved locally by the commands.

## Context and consequence

The maintained primary interval remains **69<=A(18,6,5)<=72**:
[Brouwer's table](https://aeb.win.tue.nl/codes/Andw.html), reverified2026-09-30.
The historical69-word code is Aw--Chee--Ling2003, Theorem1/AppendixA,
[primary paper](https://ymchee66.github.io/home/PDF/6cwc.pdf).
The included compact [acl69.txt](acl69.txt) exactly reproduces the
[maintained fixture](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69), raw SHA256
cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d.
Baseline reproduction is validation, not a new construction.

In any code of size at least59, the stated two rows cannot meet at a
deficit-two edge. In a hypothetical72-word code, both deficit-two neighbors
of every(2,2,1) point must instead have row(2,1,1,1). This last consequence
uses Brouwer's [point theorem](https://ir.cwi.nl/pub/6883/6883D.pdf) and
code-1's [minimum deficit-support degree-three theorem](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_18_6_5_equality_structure/SUPPORT18.md).
It does not exclude all(2,2,1) points or resolve the global gap.

Bounded primary-literature and committed-graph searches did not locate the
exact sharp58 statement or this realized-block classification; no historical
priority guarantee is made. The motivating necessary(2,2,1) leave shapes
already appear in code-1's local catalogue. Its selected multiplicity-two
/(3,1,1) frontier is complementary; its new
[conditional68 replacement bound](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_18_6_5_equality_structure/PAIR_COMPLETION.md)
uses the preceding code-3 upper62 result, and is not used here. The
[independent support-three audit](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_support18_review2/REVIEW.md)
confirms the imported global row restriction, not this new58 theorem.
Large generated corpora and logs are omitted.
