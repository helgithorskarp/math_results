# Parts sealed-pool shape a=6 is closed

**Exact computer-assisted theorem.** Let `L={0,...,373}` and
`S={374,...,508}` be the committed Parts decomposition, and let `Q5` be the
specified 168-point completion set in
[pool_S.json](../hadwiger_nelson_parts509_s_replacement_budget/pool_S.json).
For every `R subset S` with `|R|=7` and `A subset Q5` with `|A|=6`, if every
added point has degree at least four in the induced unit-distance graph

```text
H = L union (S minus R) union A,
```

then `H` is four-colourable. Every such graph has 508 vertices.

Together with the earlier unconditional
[a=5 closure](../hadwiger_nelson_parts509_pool_shape_closure), the degree
condition can be removed: if an added point has degree at most three,
delete it, restore one omitted S vertex, and use that earlier
delete-six/add-five theorem. Restrict the resulting colouring and put the
deleted added point back using a colour absent from its at most three
neighbours. Thus **every delete-seven/add-six graph in this sealed family
is four-colourable**. Further S deletions are covered by restriction.

The earlier `a=0,...,5` closures and this result imply that any blocking
`X subset S union Q5` with `|X|<=134` must contain at least **seven** Q5
points. This does not exclude larger addition sets, close the entire
sealed-pool problem, or improve the 509-vertex record.

## Positive colouring cover

Write `U=S union Q5`, in the sorted order used by the pool file. A killing
set `D subset U` has a proper four-colouring of `L union (U minus D)`.
A blocking selected set `X` must meet every killing set: otherwise that
colouring restricts to `L union X`.

[killing_clauses.cnf](killing_clauses.cnf) gives 6,777 such sets as a
canonical positive-clause instance. Variable `i+1` represents the selected
point `U[i]`; each clause lists the points of one killing set. All clauses
are nonempty, distinct and contain only positive variables in `1..303`.
The file is 399,219 bytes. [interface_hints.json](interface_hints.json) gives
one index per row into the explicit L-colourings in
[interface_L.json](../hadwiger_nelson_parts509_interface_lemma/interface_L.json).

The verifier reconstructs a complete positive colouring for every row by
incremental two-bit SAT, guided by the hint. Each returned colouring is
checked directly against every surviving exact unit edge, including all
edges inside L. A bad hint, unresolved search, or invalid colouring fails
verification. The SAT solver is a witness finder; its verdict is not trusted
as proof of positive colourability. **Completeness of the stored interface
classes is not needed.** The actual full colourings are generated locally.

## Master formula and proof

The master selects exactly 128 of the 135 S points and exactly six Q5 points.
It contains the 6,777 positive killing clauses, two exact cardinality
constraints, and the following conditional degree constraint for each Q5
point `w`:

```text
x_w = 1 implies sum(x_v for v in N(w) intersect U)
                  >= 4 - |N(w) intersect L|.
```

All neighbours are recomputed by exact arithmetic in
`Q(sqrt(3),sqrt(5),sqrt(11))`; the 677 distinct points have exactly 3,400 unit
edges. The deterministic totalizer counters come from the committed
[cardinality source](../hadwiger_nelson_parts509_pool_shape_closure/cardenc.py).
Each counter records threshold counts in a binary tree. The forward merge
clauses force every attained threshold; the reverse clauses permit a parent
threshold only if the children attain a compatible split. Assigning actual
truncated counts extends every input assignment, so asserting the seventh
threshold and forbidding the eighth gives exactly seven absent S points,
and likewise for six selected Q5 points. The conditional degree counters
have private auxiliaries and are guarded by `not x_w`.

Kissat generates an UNSAT trace and drat-trim checks it. For any selection
obeying the cardinalities and degrees, a counter assignment exists. UNSAT
therefore says that this selection misses at least one killing set, whose
checked colouring supplies the desired colouring of H. This proves the
degree-constrained theorem directly.

The new proof uses **no unverified beta, pair or higher-order shortcut**.
It supersedes the unfinished older a=6 certificate as a route to this
closure; that earlier certificate's 768 unproved higher-order rows and
four unfinished frontier cubes are not dependencies.

## Reproduce

From the repository root, with Python 3.11, Kissat 4.0.4 and drat-trim:

```sh
python3 -m pip install -r hadwiger_nelson_parts509_pool_shape6_verified/requirements.txt
python3 hadwiger_nelson_parts509_pool_shape6_verified/verify.py \
  --work /tmp/parts-shape6 \
  --kissat /path/to/kissat --drat-trim /path/to/drat-trim
python3 hadwiger_nelson_parts509_pool_shape6_verified/audit.py \
  --work /tmp/parts-shape6
```

Run without Python optimization flags. The colouring cache is checked on
every invocation and permits resuming an interrupted reconstruction. The
default per-colouring conflict budget is 200,000; increase `--conflicts`
if a positive case is unresolved. `--solver-seconds` bounds the master solver
(default 900); a completed UNSAT trace is checked to completion.
No failed or partial run reports the theorem as verified.

[expected.json](expected.json) pins the master and compact input hashes.
Expected master dimensions are 4,588 variables and 26,660 clauses. Its
SHA-256 is
`b171d62e559a4ea78a368f0c5fd842eaf4895cf7a238bcad252d57bf70ad2eec`.
Success is reported as `a=6 COLOURING COVER AND DRAT VERIFIED`.
Tool versions and trace provenance are in [toolchain.json](toolchain.json)
and [proof_manifest.json](proof_manifest.json).

`audit.py` uses a separate exact-geometry implementation from the committed
[independent two-triple review](../hadwiger_nelson_parts509_two_triple_budgets_review3).
It parses the integer scale-96 Parts table, rebuilds the geometry at scale
288, checks all generated colourings with bitsets, and checks their alignment
with the master clauses. It imports neither this verifier nor its geometry
module. General totalizer correctness remains the explicit mathematical
argument above; 15,364 small signed-cardinality and conditional-degree
projections were exhaustively checked during validation.

## Provenance and scope

The initial master used only directly checked positive colourings from
published S-only/mixed families and saved research witnesses. It checked
104,730 distinct witnesses, retained 102,687 after safe pruning, and produced
a DRAT-verified contradiction. Greedy extension of the colourings, exact
subsumption and two proof-core extractions produced the smaller family here.
The public reproduction needs none of those exploratory streams or their
solver claims: it regenerates and checks its own colourings and master proof
from the two small instance files and committed coordinate data.

The generated colouring cache, full CNF and DRAT traces stay in `--work`.
They are reproducible outputs, not unavailable input dependencies. The trust
boundary is the committed exact coordinate parsers/arithmetic, the explicit
cover/counter argument, ordinary computation and the DRAT checker. The result
is not a proof-assistant formalization. The unconditional corollary additionally
uses the earlier a=5 theorem; the checked master itself proves the stated
degree-constrained a=6 theorem independently of the earlier closures.
