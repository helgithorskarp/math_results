# Identity-offset-four E2 exclusion for literal polyhex strips

Actual author **six-heesch-2**, role **researcher**. An exact author-checked
intermediate lemma, independently unreviewed and unformalized.

For every integer k>=6 and integer b, the registered local contact(I;4,b)
is outsideE2. Its inverse side is excluded by swapping centers. The b=3
contact is already outsideE1. [proof.md](proof.md) specifies the literal
area4k+3 polyhex, reflections, pair-halo filters and all quantifiers.
No Heesch number, plane tiling, complete E2-subset-A2 or finite-five
construction is asserted.

The raw domain is3<=b<=k+2. Five occupied cells common to the moving
copy restrict the first original demand to four affine poses. Exact
packing intervals leave no supplier at b=3, Z at b=4, and A/Z afterwards.
A prior E1 exclusion of Z forces A. A second original demand, with thirteen
common occupied cells, has four suppliers, all excluded by packing or
two earlier E1 contact rules. The computation uses no SAT/SMT solver,
cover search or finite-sample extrapolation.

From a repository checkout, standard-library Python3.11+:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 round-two/six-heesch-2/strip-e2-side4-exclusion/verify.py
```

The verifier checks byte-pinned source/dependencies and runs four serial
producer/reader jobs in normal and optimized Python. Each retains43s
work/45s signal/47s parent and100000-operation guards. All solver/BLAS/
OpenMP threads are one. Guards and incomplete jobs prove no exclusion.
Generated evidence is ignored and is not an external required certificate.

Producer mathematical SHA256:
`113975a596fe6c3a7523d76566817652a443ceaec81eb15d81c6f8ee844c976f`.
Reader mathematical SHA256:
`971d96aace7f2d6d669ae4e6a6f28be010f79fda2ad7c4aa02cf3a372f2dbabd`.
Three false wedge controls and seven damaged reader certificates reject in
both modes. Axial audits use k=6,7,8,9,12,40 and all raw b at each audited k.
Exact endpoint partitions establish the full unbounded range.

[point_blocks.py](point_blocks.py) derives the new occupied-cell source-height
constraints. [check.py](check.py) reconstructs them through axial coordinates
and a separate interval event sweep, without importing the new producer or
point-block kernel. Shared prior affine and whole-copy overlap code,
ordinary completeness/wedge arguments and cited E1 results remain trust
boundaries. Same-author replays do not constitute independent review.

Prior source is reused without alteration. Only9542/E02,9578/B05 and the
9404 identity-U6 E1 restriction are mathematical exclusion premises;
9321 supplies the unconditional literal/column model. See the precise
links in the proof. The earlier U5 lemma is context, not a premise.
