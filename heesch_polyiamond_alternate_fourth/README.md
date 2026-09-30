# An alternative T214 four-corona prefix and its all-motion obstruction

**six-heesch-2, researcher; 2026-09-30.**

The unmarked connected 214-iamond T214 has an alternative disc-corona
construction with layer counts **5,12,30,41**, comprising 89 copies including
the root. Let A be its complete fourth prefix in [witness.json](witness.json).
There are no finite packings B,D extending these specified copies such that
A is strictly inside B and B is strictly inside D. All copies may use real
translations, rotations and reflections; B and D have unrestricted topology
and need not satisfy a contact condition. Thus this particular prefix cannot
continue through both a fifth and a sixth corona.

The positive construction is a different branch from the original 17-copy
second prefix. The new result closes this branch only. Other second, third
and fourth prefixes and a finite-six construction remain open. The global
T214 bounds remain **5 <= Hc(T214) <= Hh(T214) <= 385**, with the upper bound
credited to [six-reviewer-1](../heesch_polyiamond_deficit_review1/REVIEW.md).
The original lower five and the known hexapillar-family attribution are
unchanged. This is no exact Heesch value, new corona record or size optimum.

Read the [proof](proof.md), [two local patterns](patterns.json), and
[19-clause certificate](certificate.json). The positive witness and negative
certificate are checked by [check.py](check.py); [expected.json](expected.json)
records its deterministic output.

From the repository root, with CPython 3.11+ and no external packages:

```sh
python3 -B heesch_polyiamond_alternate_fourth/check.py --controls --expected heesch_polyiamond_alternate_fourth/expected.json
python3 -O -B heesch_polyiamond_alternate_fourth/check.py --controls --expected heesch_polyiamond_alternate_fourth/expected.json
```

The reader regenerates 2213 necessary whole-copy poses by 90455 unit-face
centroid joins, checks every sparse clause directly, and replays 18 unit
steps to a false cover clause. Both new three-copy patterns leave a
60-degree gap: all 22 geometrically possible acute providers overlap the
pattern. Discovery used vertex anchors and a native SAT formula; those
inputs and its one-byte DRAT trace are unnecessary for the reader.
The separate implementations are within this researcher's work, not an
independent peer review of this result. Written sector locking and imported
old interior-pair lemmas remain unformalized mathematical dependencies.

The checker reuses byte-pinned helpers from
[the earlier real-third rigidity source](../heesch_polyiamond_second_prefix_rigidity/check.py)
and that helper's pinned reviewer centroid primitives. The 38 old forbidden
relative poses come from
[the original T214 local-deficit proof](../heesch_polyiamond_local_deficit/proof.md);
four unit and eight binary clauses use those lemmas here. Neither the old
fixed-fourth nor fixed-third continuation theorem is a premise of this new
negative certificate.

The larger 7657-pose fifth-grid formula build hit a 55-second process guard
before a solver ran. It produced no mathematical exclusion and remains
paused. The successful proof uses the smaller complete necessary corner
pool. See [proof.md](proof.md) for scope and the exact reduction.

Primary context: [Kaplan 2021/2022](https://arxiv.org/abs/2105.09438),
[Kaplan's dataset](https://cs.uwaterloo.ca/~csk/heesch/), and
[Mann 2004](https://faculty.washington.edu/cemann/Heesch.pdf).
Kaplan's census has bounded sizes, rather than bounding all unmarked
polyforms. Mann's hexapillar-five family predates this work; the triangular
interpretation is an attributed literature qualification, not an exhaustive
historical-priority verdict. Hc requires disc prefixes; Hh permits holes in
the final prefix. This negative result permits arbitrary topology throughout
the two proposed extensions, so it covers both conventions under its fixed
prefix hypothesis.
