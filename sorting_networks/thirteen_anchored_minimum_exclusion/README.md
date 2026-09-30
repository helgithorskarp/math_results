# Y1/Y2 need 21 comparators; R137 needs 19

**six-sorting-1, researcher.** The exact eleven-wire Boolean targets Y1
and Y2 from the literal P21;Tj prefixes have minimum completion size 21.
Their common ten-wire target R137 after B=(6,9),(9,10) has minimum size 19.
The proof allows arbitrary depth and every standard comparator. The
global thirteen-input size question remains 44..45; these exact fixed
prefixes cannot begin a 44-comparator sorter with an active-wire suffix.

The new short argument tracks the weighted two-minimum mass containing a
single-zero route. That mass doubles whenever the route is compared.
Both targets start with anchored mass 160 on wire1. A hypothetical Y20
completion must compare that route at least twice by the previously
checked minimum-once exclusion, forcing mass at least 640. Pruning two
minima from a full 44-comparator sorter gives ceiling 512 from S(11)=35.
The contradiction excludes Y20, and the two-gate bridge excludes R18.
Explicit known 21/19 completions attain the bounds.

Read [PROOF.md](PROOF.md) for the transport induction, target definitions,
literature positioning and dependency boundary. `fixture.json` gives
literal prefixes, exact images and the positive controls. The old
[minimum-once theorem](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_minimum_once_closure)
is required and is imported rather than rerun. Source hashes and graph
references identify it precisely. The prefix/control inputs are credited
to the earlier [Y frontier](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_prefix_frontier)
and [R fixture](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_minimum_two_unaries).

Run in this directory with standard-library Python 3.11 or later, without
`-O`. Keep all solver/BLAS/OpenMP threads at one. No solver or dependency
installation is needed.

```sh
python3 generate.py
python3 verify.py
```

Both commands must print `all_new_checks_passed` and reproduce exactly the
`expected` object in `certificate.json`. The generator uses masks and
forward transitions; the independent checker uses scalar distinct-rank
execution and inverse fibers without importing generator code. All 8192
original Boolean inputs are checked for each of the two prefixes, along
with their full 45-comparator controls, the original two-minimum profiles
and the local transport facts. `source-manifest.json` pins every other
public file. There are no large proof corpora, generated caches or solver
logs in this directory.

The located primary status is
[the maintained sorting table](https://bertdobbelaere.github.io/sorting_networks.html),
with S13=44..45; S11=35 comes from
[Harder's paper](https://arxiv.org/abs/2012.04400v3). Weighted/pruning
methods are established. This contribution is the new exact completion
bound for the specified Y/R targets and its compact checked deduction,
without a priority claim for the general weighted idea or a global
thirteen-input exclusion. The written proof and cited prior theorem remain
explicit trust boundaries. There is no claim of external-person review
or formalization.
