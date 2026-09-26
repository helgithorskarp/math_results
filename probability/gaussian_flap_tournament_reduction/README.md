# Two ten-point templates for an asymmetric Gaussian counterexample

The [author proof](PROOF.md) reduces **every failed Gaussian hinge** in
the depth-one orthocentric tetrahedron flap family from sixteen source
sites to ten. Opposite directed flaps have a common target. Convexity
therefore moves a negative witness to one of 64 source selectors without
reducing its defect. Exactly 32 selectors have an explicit R5 contracting
motion and satisfy every hinge comparison. The remaining 32 fall into
two types under simultaneous relabelling of geometry and weights.

This is an exact counterexample reduction for an entire asymmetric family,
not a numerical candidate or a solution of the full R3 conjecture.
Neither of the two remaining templates is proved positive or negative.
Independent mathematical review and formalization are pending.

The output is a concrete obligation for existing analytic, geometric and
certification lanes; [HANDOFF.md](HANDOFF.md) gives its exact scope. In
particular a fixed asymmetric tetrahedron requires all 32 labelled
selectors, whereas the two representative families allow relabelled shapes.

Run from this directory with standard-library CPython 3.11 or later:

```sh
python3 verify.py --check
python3 -O verify.py --check
sha256sum -c SHA256SUMS
```

Both verifier modes must reproduce [EXPECTED.json](EXPECTED.json), including
64 classified tournaments, 32 pruned sink selectors, remaining orbit sizes
8 and 24, 120 formal pair identities, three motion polynomial identities,
5760 direct rational distance checks, 128 paired-rank checks, four exact
mixture controls and four rejected corruptions. No Gaussian integral or
floating-point sign is computed. A run takes about one second on the
author’s host; the finite checks support the written proof.

[templates.py](templates.py) produces rational inputs, not sign certificates:

```sh
python3 templates.py --template strong --a 1 --b 2 --d 3
python3 templates.py --template source_cycle --a 3/2 --b 4/3 --d 5/4 --variance 2/3
python3 templates.py --certificate
```

All numerical inputs use integer or fraction syntax. The ten `--units`
are nonnegative and normalized to probability weights; their default is
`1,2,3,4,5,6,7,8,9,10`. The optional `--threshold` is a positive physical
hinge threshold. Coordinates in `input` and `output`, `weights`, and
`variance` are exact fraction strings. The four anchors come first,
followed by one flap for each unordered edge (01,02,03,12,13,23).
Bit one means smaller-to-larger orientation. The masks are 2 for
`source_cycle` and 4 for `strong`.

[CERTIFICATE.json](CERTIFICATE.json) includes a relabelling for each of the
64 masks and two exact asymmetric ten-point fixtures. Regenerating it with
`templates.py --certificate` must reproduce its bytes. The checker imports
no producer code and reconstructs the combinatorics and coordinate geometry
directly. It does not constitute independent mathematical peer review.
The exact certificate SHA256 is

```text
2362bc50ff55fe38d3fc70b9f93f9ef2bc29316b00e1a7cbd0853240e9d8b094
```

All prior source is credited in [SOURCES.md](SOURCES.md). There is no large
artifact, external dataset, third-party package, or hidden numerical input.
