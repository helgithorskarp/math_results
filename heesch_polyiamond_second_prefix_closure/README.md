# T214: all sixth continuations of an alternative second prefix are excluded

**six-heesch-2, researcher, 2026-09-30.** Under arbitrary real translations,
rotations, reflections and topology, the specified **18-copy second prefix**
cannot have four further strict surrounds. Thus no sixth corona starts
with it, regardless of third, fourth or fifth choices. Its known four
disc coronas are rechecked; a fifth remains undecided. See [proof.md](proof.md).

Two exact intermediate results make this earlier branch closure possible:

- With two future surrounds, this second prefix forces all **30 specified
  third-layer copies**. A 371-clause, 371-unit certificate forces 28 copies;
  two newly exposed small gaps at OLD second-prefix vertices force the
  remaining two. Unlisted real-motion copies stay free. Full halo coverage
  implies that a third prefix with the usual contact condition is exactly
  the 48-copy prefix. [rigidity.json](rigidity.json) specifies the data.
- A transportable **18-copy local pattern** has no three further surrounds.
  Its independent check has 13 complete covers, 144 relevant providers,
  157 geometric clauses and five RUP implications. This localizes the
  earlier fixed 48-copy third-prefix obstruction. [local-pattern.json](local-pattern.json)
  specifies the smaller premise. Minimum support is not claimed.

The different original **17-copy** second-prefix rigidity was already
published and is credited. The present prefix has 18 copies and is the
alternative branch in the published escape-both witness; no old construction
is presented as new. The elementary halo/contact principle is also credited.

From repository root, CPython 3.11.2 standard library:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B heesch_polyiamond_second_prefix_closure/check.py --controls --expected heesch_polyiamond_second_prefix_closure/expected.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B -O heesch_polyiamond_second_prefix_closure/check.py --controls --expected heesch_polyiamond_second_prefix_closure/expected.json
```

Both commands reproduce [expected.json](expected.json). The reader uses
centroid-face joins instead of discovery's vertex anchors and bit-mask unit
logic instead of the discovery dictionary trace. It verifies all retained
clauses and the complete terminal lists, replays the local contradiction,
checks whole meshes/full halos, and matches the transported local pattern.
Nine malformed controls reject, including incorrect future stages and a
terminal point belonging only to a selected third copy. Dense formulas,
the discovery inventory, extractors, SAT solvers and DRAT traces are not inputs.

Byte-pinned older geometry and pattern routines are disclosed reuse. The
38 imported interior-pair lemmas and written small-gap/halo bridges remain
explicit mathematical trust boundaries. No independent peer review or
proof-assistant formalization is claimed. Global bounds stay
`5 <= Hc(T214) <= Hh(T214) <= 385`; no finite-six construction, global exact
height, new record or size optimum follows. Other earlier prefixes remain open.
