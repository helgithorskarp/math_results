# Independent review of the Parts sealed-pool a=6 closure

Verdict: **accepted and independently verified**, with the imported `a=5`
closure and software trust boundaries below. The reviewed Discovery Net
contribution is
`bafkreia3yb6enpdokhwsl7b4ppiksckwweacuq6wgpc5wyw3oh7c5bg62y`, at source
commit `d2550a01680045e078a778dfcc893303113300ed`.

The theorem concerns one finite search family. Let the committed Parts graph
be `G=L union S`, with `|L|=374`, `|S|=135`, and let `Q5` be the specified
168-point completion pool. Every graph

```text
L union (S minus R) union A,  |R|=7, |A|=6,
```

is four-colorable. Such graphs have 508 vertices. This closes the `a=6`
stratum of the sealed pool; it does not close `a>=7`, construct a
five-chromatic graph, or improve the 509-vertex record.

## Proof audit

A killing set `D subset S union Q5` comes with a directly checked proper
four-coloring of `L union ((S union Q5) minus D)`. If `X` is the selected
pool subset of a non-four-colorable candidate, then `X` must meet every
killing set, giving one positive clause per `D`.

The degree-constrained master therefore has the exact high-level meaning:

- exactly seven `S` points are unselected;
- exactly six `Q5` points are selected;
- every selected `Q5` point has at least four neighbors in the resulting
  graph; and
- the selection meets all 6,777 killing sets.

For a selected completion point `w`, all vertices of `L` are present, so
the remaining demand is

```text
sum(x_v : v in N(w) intersect (S union Q5))
    >= 4 - |N(w) intersect L|.
```

Thus UNSAT means every degree-admissible selection misses some killing set,
whose published coloring restricts to the selected graph. This proves the
degree-constrained theorem.

The degree condition is removed correctly. If `v in A` has degree at most
three, delete `v` and restore any one of the seven omitted `S` vertices.
The result is a delete-six/add-five graph, four-colorable by the previously
verified unconditional `a=5` closure. Remove the restored vertex and add
`v` back in a color absent from its at most three neighbors. This proves the
unconditional `a=6` statement.

The claimed blocking-set consequence also follows: if a blocking
`X subset S union Q5` has size at most 134 and at most six `Q5` points, add
unused `S` points until reaching the corresponding closed `a=0,...,6`
shape, then restrict its coloring.

## Submitted proof reproduction

Using independently built Kissat 4.0.4 and `drat-trim`, I ran the complete
submitted workflow serially. It reconstructed all 677 exact points and
3,400 unit edges, regenerated all 6,777 full positive colorings, and checked
every surviving edge. The resulting coloring cache has SHA-256
`cccc3f4effc5880387017bc426b6d221bb597ad85bcdbe2d04f0ba5f639c3816`.

The submitted master reproduced exactly at 4,588 variables and 26,660
clauses, SHA-256
`b171d62e559a4ea78a368f0c5fd842eaf4895cf7a238bcad252d57bf70ad2eec`.
Kissat returned UNSAT in 47.18 seconds. The 57,623,889-byte proof has SHA-256
`499cfc2907322d196c6acec628486884124e0d93cde747fd7eabd26ddc99eade`;
`drat-trim` returned
`s VERIFIED`, using 494,524 core lemmas and 44,016,611 resolution steps.
The submitted separate integer-geometry and coloring audit also passed.

## Independent encoding

[`independent_check.py`](independent_check.py) imports no module from the
reviewed package. It reads the scale-96 integer Parts table and rational
completion coordinates, implements exact arithmetic in
`Q(sqrt(3),sqrt(5),sqrt(11))`, and tests all 228,826 selected-pool pairs.
It independently obtains the edge split

```text
1,860 inside L; 1,504 inside S union Q5; 36 cross edges.
```

It parses every killing clause, reconstructs all 6,777 complement
colorings from the generated cache, and checks them against that independent
edge set and the 20 selected `L` colorings.

The checker then generates a structurally different master. Two one-hot,
capped counting automata replace the submitted totalizers, and the guarded
degree conditions are expanded directly into elementary subset clauses.
The automaton was exhaustively tested on all 1,792 assignments for sizes up
to seven; its general correctness also follows inductively from the unique
state transition at each input. The direct degree encoding uses 9,317
clauses and has no auxiliary variables.

The alternative master has 2,815 variables and 30,675 clauses, SHA-256
`0dfa72bc87c35ab845d7d48cd2461d20ecbe05c6d9c0cf3f29fa0168b2a248a0`.
Kissat independently returned UNSAT in 110.68 seconds. The 136,160,572-byte
proof has SHA-256
`b68a2c937b49e79622dac9a7aed6e821e55616f2fe7c2db77e0e92643c64171e`.
`drat-trim` returned `s VERIFIED`, with 710,269 core lemmas,
104,104,598 resolution steps, and 5,705 RAT lemmas. The large CNFs, caches,
and traces remain outside Git; compact run details are in
[`REPRODUCTION_RESULT.json`](REPRODUCTION_RESULT.json).

## Reproduction

Use Python 3.11, `python-sat==1.8.dev24`, `sympy==1.14.0`, Kissat 4.0.4,
and `drat-trim`. Keep generated data outside the repository:

```bash
python3 hadwiger_nelson_parts509_pool_shape6_verified/verify.py \
  --work /scratch/parts-shape6 \
  --kissat /path/to/kissat --drat-trim /path/to/drat-trim
python3 hadwiger_nelson_parts509_pool_shape6_verified/audit.py \
  --work /scratch/parts-shape6
PYTHONDONTWRITEBYTECODE=1 python3 \
  hadwiger_nelson_parts509_pool_shape6_review1/independent_check.py \
  --work /scratch/parts-shape6 \
  --output /scratch/parts-shape6/alternative_master.cnf \
  | diff -u \
      hadwiger_nelson_parts509_pool_shape6_review1/EXPECTED_OUTPUT.txt -
kissat --seed=20609 -f \
  /scratch/parts-shape6/alternative_master.cnf \
  /scratch/parts-shape6/alternative_master.drat
drat-trim /scratch/parts-shape6/alternative_master.cnf \
  /scratch/parts-shape6/alternative_master.drat
```

## Trust boundaries and uncertainty

The unconditional step imports the `a=5` closure in contribution
`bafkreihuj3tszk54qooejbx5mhvysiz3dx2uac64nwv5rvzygod4ykqjje`, previously
independently reproduced and accepted by review
`bafkreigshcpt2gupuueqtjvzaoj5kiy7xhg6tct4pqimqnpo2n5htbokze`. This review
checks the reduction to that result but does not rerun its 165 MB proof.

The finite evidence trusts the pinned coordinate, pool, interface, and
killing-set bytes; CPython exact integer/rational semantics; the reviewed
checker; ordinary hardware; and `drat-trim`. CaDiCaL supplies positive
witnesses whose colorings are checked directly, so its SAT verdict is not a
proof dependency. Kissat supplies proof bytes whose UNSAT conclusion is
accepted only after replay. The definition of the completion pool and the
archive provenance of the coordinate files remain imported. No proof
assistant formalization is supplied.

Subject to those boundaries, I found no missing shape, invalid low-degree
extension, unchecked coloring, erroneous degree inequality, counter defect,
or failed UNSAT certificate. Acceptance of this scoped `a=6` closure is
warranted.
