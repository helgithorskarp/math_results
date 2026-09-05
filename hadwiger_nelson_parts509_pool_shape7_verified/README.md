# Parts sealed-pool shape a=7 is closed

**Exact computer-assisted theorem.** Let `L={0,...,373}` and
`S={374,...,508}` be the committed Parts decomposition, and let `Q5` be the
specified 168-point set in
[pool_S.json](../hadwiger_nelson_parts509_s_replacement_budget/pool_S.json).
For every `R subset S` with `|R|=8` and `A subset Q5` with `|A|=7`, the strict
unit-distance graph

```text
H = L union (S minus R) union A
```

is four-colourable. Each such graph has 508 vertices. Further deletions
inside S follow by restriction.

Together with the earlier unconditional `a=0,...,6` closures, this means
that any `X subset S union Q5` with `|X|<=134` for which `L union X` is not
four-colourable must use **at least eight Q5 points**, and omit at least
nine S points. This closes one finite stratum. It does not close the whole
sealed pool or establish an at-most-508 five-chromatic graph.

## Reduction and certificate

Write `U=S union Q5` in sorted global-label order. A killing set `D subset U`
has a proper four-colouring of `L union (U minus D)`. A non-four-colourable
selected set `X` must meet every such D, since otherwise that colouring
restricts to `L union X`.

The [canonical positive instance](killing_clauses.cnf) supplies 12,824
killing sets. Variable `i+1` selects `U[i]`. Each positive clause lists one
D, and [interface_hints.json](interface_hints.json) supplies an index into
the explicit proper L-colourings in
[interface_L.json](../hadwiger_nelson_parts509_interface_lemma/interface_L.json).
These are search hints: the public verifier regenerates a full colouring
for every row, and checks all surviving edges directly. It checks the
L-colourings themselves as well. Neither positive SAT verdicts nor
completeness of the interface classes is a proof assumption.

The master has exactly eight absent S points and exactly seven selected
Q5 points. In addition to the killing clauses, each selected `w in Q5`
must satisfy

```text
sum(x_v for v in N(w) intersect U) >= 4 - |N(w) intersect L|.
```

All pairs of the 677 distinct points are tested exactly in
`Q(sqrt(3),sqrt(5),sqrt(11))`, obtaining 3,400 strict unit edges. No
approximate distance decision is used.

The [committed totalizer encoder](../hadwiger_nelson_parts509_pool_shape_closure/cardenc.py)
represents threshold counts in a binary tree. For every input assignment,
assigning each auxiliary its actual truncated threshold value satisfies
the merge clauses. Conversely the forward and reverse merge clauses force
those values, inductively from the leaves. Asserting threshold 8 and
forbidding 9 therefore imposes exactly eight absent S points; thresholds
7 and 8 impose seven selected Q5 points. The degree constraints are
at-most counters on absent neighbours, each with private auxiliary
variables and clauses guarded by `not x_w`. If `x_w=0` all these clauses
are inactive; if `x_w=1` they impose precisely the displayed demand.

Kissat produces an UNSAT trace and drat-trim checks it. Every selection
obeying the counts and degrees extends to a counter assignment, so UNSAT
says it misses at least one killing set. The checked complement colouring
then supplies a proper colouring of H. This proves the theorem when all
added points have degree at least four.

To remove that degree condition, take an added point v of degree at most
three. Delete v and restore any one omitted S point. The resulting
delete-seven/add-six graph is four-colourable by the
[unconditional a=6 closure](../hadwiger_nelson_parts509_pool_shape6_verified),
which has an [independent accepted review](../hadwiger_nelson_parts509_pool_shape6_review1).
Remove the restored point and reinsert v using a colour absent from its
at most three neighbours. This proves the unconditional theorem stated
above. For a smaller selected set, add omitted S points to the matching
closed shape and restrict its colouring.

## Reproduce

From the repository root, with Python 3.11, Kissat 4.0.4 and drat-trim:

```sh
python3 -m pip install -r hadwiger_nelson_parts509_pool_shape7_verified/requirements.txt
python3 hadwiger_nelson_parts509_pool_shape7_verified/verify.py \
  --work /tmp/parts-shape7 \
  --kissat /path/to/kissat --drat-trim /path/to/drat-trim
python3 hadwiger_nelson_parts509_pool_shape7_verified/audit.py \
  --work /tmp/parts-shape7
```

Run without Python optimization flags. The per-colouring conflict budget
is 200,000 by default; increase `--conflicts` if a positive search is
unresolved. The checked cache permits resuming witness reconstruction.
The master solver has a configurable 900-second bound by default. A
completed UNSAT trace is checked to completion. A failed or unresolved
search cannot produce a successful new result.

Expected success is `a=7 COLOURING COVER AND DRAT VERIFIED`.
[expected.json](expected.json) pins the two compact input hashes and the
master: 4,641 variables, 33,387 clauses, SHA-256
`ed3ae96f4a4d2664c69914520ae40c469440481c2c035b6551d0ecd2d3d4ece6`.
The positive instance is 818,834 bytes. Complete colouring caches, full
CNFs and proof traces are generated in `--work`; none is an unavailable
input dependency. [proof_manifest.json](proof_manifest.json) records the
completed fresh run and trace hash; [toolchain.json](toolchain.json)
records tool versions and exact input hashes.

`audit.py` imports neither the main verifier nor its exact geometry
module. It uses the independently reviewed integer-table geometry from
the [two-triple review](../hadwiger_nelson_parts509_two_triple_budgets_review3),
rebuilds the graph at denominator 288, checks every positive witness with
bitsets, and matches each killing clause to the master. This is a second
implementation check run by the author, not external peer review of the
present a=7 theorem.

## Provenance and trust boundary

The research master reused 34,551 extended minimal killing witnesses from
the a=6 campaign and rechecked all 3,575 published S-only witnesses. All
38,126 records were directly checked. Removing duplicate sets, clauses
with more than eight S points, and exact subset redundancies left 34,791
clauses. In particular, 240 eight-S-point clauses become useful in this
shape after having been safely omitted at a=6. The initial 4,641-variable,
55,354-clause master was UNSAT with a checked proof. Proof-core extraction
produced the smaller canonical instance here.

The public reproduction regenerates its own witnesses and proof; it does
not require the exploratory witness streams, old shortcut verdicts, or
proof-core extraction. An additional local audit used independently
implemented integer geometry and directly checked all 34,791 initial
witnesses. It generated an alternative master with one-hot counting
automata and elementary subset degree clauses, but that alternative was
not solved and is not cited as an UNSAT certificate.

The trust boundary is the exact coordinate sources/parsers and arithmetic,
the explicit cover and counter arguments, ordinary software/hardware, and
the DRAT checker. The source verifier builds on the reviewed a=6 verifier;
this is an extension to a new stratum, not a claim of a new solving method.
No proof-assistant formalization is supplied. The unconditional corollary
imports the a=6 theorem. Eight or more additions and other geometric
construction families remain outside this certificate.
