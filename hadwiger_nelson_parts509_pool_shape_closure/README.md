# Shape reduction for the sealed sqrt5 replacement problem of the Parts 509-graph

**Claim status:** exact computer-assisted theorem for the reduction lemma (solver-free) and
for each closed value of `a` (DRAT-checked master, solver-free killing-set witnesses).  The
open interval `116..134` of the committed replacement-budget contribution is **not** closed
here; this directory records exactly how much of it is closed and what remains.

## Setting

Write Parts's 509-vertex 5-chromatic unit-distance graph as `G = L ∪ S` with the committed
interface decomposition (`../hadwiger_nelson_parts509_interface_lemma`): `L` is the induced
subgraph on the 374 points whose exact coordinates are free of `sqrt5` (ambient indices
0..373), `S` the one on the 135 points involving `sqrt5` (374..508).  Let `Q5` be the 168
completion points of `G` involving `sqrt5` and `U = S ∪ Q5` (303 points).  The pool is
*sealed*: all 36 unit-distance edges from `L` to `U` end in the 19-vertex interface `I_L`
(30 into `S`, 6 into `Q5`), so `L` and its interface are untouched when `S` is replaced by
some `X ⊆ U`.

Call `X ⊆ U` **blocking** if `L ∪ X` is not 4-colourable, and put

    mu := min { |X| : X ⊆ U blocking }.

Parts's `S` is blocking, so `mu ≤ 135`; the committed contribution
`../hadwiger_nelson_parts509_s_replacement_budget` proves `mu ≥ 112` (solver-free) and
`mu ≥ 116` (MILP dual bound, solver-trusted), and leaves `116..134` open.  A blocking `X`
with `|X| ≤ 134` would be a 5-chromatic unit-distance graph `L ∪ X` on at most 508
vertices, i.e. a new record.

## Lemma (shape reduction) — solver-free

> `mu ≤ 134` **iff** there are an integer `a ≥ 0`, a set `R ⊆ S` with `|R| = a + 1` and a
> set `A ⊆ Q5` with `|A| = a` such that `L ∪ (S \ R) ∪ A` is not 4-colourable.
> Moreover one may assume in addition that every `w ∈ A` has at least four neighbours in
> `L ∪ (S \ R) ∪ A`.

*Proof.* (⇐) The set `X = (S \ R) ∪ A` has `|X| = 135 - (a+1) + a = 134`.
(⇒) Let `X` be blocking of minimum size `mu ≤ 134`; being of minimum size it is
inclusion-minimal, so for every `v ∈ X` the graph `L ∪ (X \ {v})` has a proper 4-colouring,
which would extend to `v` if `v` had at most three neighbours in `L ∪ X`; hence every
vertex of `X`, in particular every point of `A := X ∩ Q5`, has at least four neighbours in
`L ∪ X`.  Put `a := |A|` and `d := |S \ X|`; then `135 - d + a = |X| ≤ 134`, so `d ≥ a+1`.
Adding `d - a - 1` of the omitted vertices of `S` back to `X` gives `X' ⊇ X`; a supergraph
of a graph that is not 4-colourable is not 4-colourable, so `X'` is blocking, it has the
stated shape with `R = S \ X'`, and degrees only grew. ∎

Because `L ∪ X ⊆ L ∪ (X ∩ S) ∪ Q5`, a blocking `X` also satisfies `|X ∩ S| ≥ h_S`, where
`h_S = min{|Y| : Y ⊆ S, L ∪ Y ∪ Q5 not 4-colourable}`; the committed budget contribution
gives `h_S ≥ 90`, so in the shape above `134 - a = |X ∩ S| ≥ 90` and therefore

    a ∈ {0, 1, ..., 44}.

**So the open interval `116..134` is exactly the conjunction of 45 finite shape problems.**
`a = 0` is the vertex-criticality of `G`; `a = 1, 2, 3` are the committed delete-2-add-1,
delete-3-add-2 and delete-4-add-3 closures restricted to the pool (deletions inside `S`,
additions inside `Q5`).  Note that the reduction makes the *number of deletions* equal to
`a + 1` for free, so a single value of `a` covers deleting any number `d ≥ a+1` of vertices
of `S` while adding `a` points of `Q5`.

## Theorem (what is closed here)

For each `a` listed in `closures.json` there is **no** pair `(R, A)` as in the Lemma:
no `R ⊆ S` with `|R| = a+1` and `A ⊆ Q5` with `|A| = a` makes `L ∪ (S \ R) ∪ A`
non-4-colourable.

| `a` | shape ruled out | killing sets in the certificate | DIMACS | CaDiCaL | DRAT proof | drat-trim |
|---|---|---|---|---|---|---|
| 0 | delete 1 vertex of `S`, add nothing | 135 | 738 v / 1,576 c | 0 s | 8,043 B | VERIFIED |
| 1 | delete 2, add 1 | 196 | 975 v / 2,710 c | 0 s | 21,962 B | VERIFIED |
| 2 | delete 3, add 2 | 264 | 1,141 v / 3,704 c | 0 s | 1,235,694 B | VERIFIED |
| 3 | delete 4, add 3 | 829 | 1,242 v / 5,061 c | 1 s | 1,953,682 B | VERIFIED |
| 4 | delete 5, add 4 | 1,226 | 1,336 v / 6,232 c | 7 s | 21,586,068 B | VERIFIED |
| 5 | delete 6, add 5 | 1,600 | 1,406 v / 7,328 c | 67 s | 165,070,679 B | VERIFIED |

The six certificates share 1,612 distinct killing sets (`killing_sets.json`, 595 KB).
Values `a = 0, 1, 2, 3` reproduce, inside the pool, the committed vertex-criticality and the
delete-2-add-1, delete-3-add-2 and delete-4-add-3 closures; `a = 4` is a restricted case of
the delete-5-add-4 question, which the committed one-anchor closure has settled only outside
the all-anchored family `A ⊆ Q`; `a = 5` goes beyond the committed closures.  With the
current family of 6,824 certified killing sets the masters for `a = 6` and `a = 7` are still
*satisfiable*, so those values are open and the implicit-hitting-set loop is still running on
them.  (For comparison, the same machinery closes `a = 56, 58, 60` in 11-116 s, but those
values are already excluded by `h_S ≥ 90`; no certificate was extracted for them.)


Consequently every blocking `X ⊆ U` with `|X| ≤ 134` has `|X ∩ Q5| ≥ 6` and omits at least
seven vertices of `S`.  **The interval `116..134` is not closed**: the shape problems
`a = 6, ..., 44` remain open, so `mu` is still only known to lie in `{116, ..., 135}`, and
nothing here improves the 509-vertex record or the bounds `5 ≤ χ(R²) ≤ 7`.  The closures
above do *not* use the extra degree assumption of the Lemma, so they rule out the shapes
outright.

## Method

`X` blocking is decided through the committed interface lemma: `L ∪ X` is 4-colourable iff
for one of the 20 interface classes `p` (a colouring of `I_L` induced by a proper
4-colouring of `L`, normalised so the origin gets colour 0 and taken up to permutations of
`{1,2,3}`) the list instance on `U[X]` with `list_p(v) = {0,1,2,3} \ p(N(v) ∩ I_L)` is
colourable.  So one blocking test is 20 SAT calls on a 303-vertex graph (`pool5.py`, one
incremental solver per class, `X` entering only through activation assumptions).

`D ⊆ U` is a **killing set** if `L ∪ (U \ D)` is 4-colourable; every blocking `X` meets
every killing set, since otherwise `X ⊆ U \ D` and the witness colouring 4-colours `L ∪ X`.
For a fixed `a` the master problem is the decision question

    exists R ⊆ S, |R| = a+1, and A ⊆ Q5, |A| = a, hitting every killing set?

as a SAT instance over the 135 + 168 Boolean variables `r_v`, `q_w` with two cardinality
constraints (`ihs_a.py`), or as a HiGHS integer feasibility problem (`ihs_a_milp.py`, much
faster at producing candidates for middle `a`).  A model is a candidate `(R, A)`; the
oracle either certifies it blocking — which would beat the 509-vertex record — or grows its
witness colouring to a maximal 4-colourable set and returns fresh inclusion-minimal killing
sets, which are added as clauses.  Master unsatisfiability closes the value `a`.

This differs from the stalled run of the committed budget contribution in two ways: the
question is a *feasibility* question at a fixed shape instead of a minimum-hitting-set
optimisation (whose LP relaxation is stuck at 111.12 and whose MILP dual bound reached only
116), and unsatisfiability is certified by a DRAT proof rather than by a solver's optimality
claim.

## Certificates and verification

* `killing_sets.json` — every killing set used, as `{"D": [...], "p": class index,
  "c": "<303 characters>"}`;  the class index is read off the witness colouring itself,
  because the imported search histories number the 20 interface classes differently from
  `interface_L.json`; `c[i]` is the colour of the `i`-th point of `U` (sorted) and
  `.` for the points of `D`.  Together with the class-`p` witness colouring of `L` from the
  committed interface lemma this is an explicit proper 4-colouring of `L ∪ (U \ D)`.
* `closures.json` — for each closed `a`, the indices of the killing sets whose clauses,
  together with `|R| = a+1` and `|A| = a`, are unsatisfiable, the SHA-256 of the rebuilt
  DIMACS instance, and the size/hash of the DRAT proof.

```text
python3 test_cardenc.py                                          # the encodings, ~1 min
python3 verify_pool_closure.py                                   # geometry + witnesses + SAT, 72 s
python3 verify_pool_closure.py --drat DIR --drat-trim /path/to/drat-trim   # DRAT instead of SAT
python3 prove_closures.py --dir . --work /tmp/proofs             # regenerate the DRAT proofs
```

Reproducing the search itself needs a killing-set family in the one-set-per-line JSON format
`{"D": [...], "pattern": p, "witness": "<colours of L u (U \ D) in increasing index order>"}`;
`family.py` loads and verifies such files, `killing_sets.json` is the certified subfamily
published here, and

```text
python3 ihs_a.py --a 6 --family family_min.json --extra more_killing_sets.jsonl
python3 certify_full.py --a 6
```

runs one value of `a` and extracts its certificate.

`verify_pool_closure.py` re-parses Parts's 509 exact points from the published Mathematica
source and the 1,158 completion points of the committed swap closure, recomputes **every**
unit pair inside `L ∪ U` exactly in `Q(sqrt3, sqrt5, sqrt11)` (228,826 pairs, integer
arithmetic after clearing the common denominator 288), checks that the pool is sealed,
replays every killing-set colouring against that edge list, rebuilds each DIMACS instance
with the self-contained totalizer encoder of `cardenc.py` (verified exhaustively for
`n ≤ 8` and randomly up to `n = 180` by `test_cardenc.py`: the encoding is satisfiable
exactly on the assignments obeying the cardinality bound, which is what makes an UNSAT
answer meaningful), checks its SHA-256, and shows it unsatisfiable.

## Trust boundary

* **Geometry.**  Recomputed from scratch here and independently of the committed closures:
  the 3,400 unit pairs inside `L ∪ U` (1,860 in `L`, 1,504 in `U`, 36 cross) agree exactly
  with the committed ambient edge list restricted to those 677 points.  The lower bounds
  need the *completeness* of that list, which this recomputation supplies for `L ∪ U`; the
  definition of `Q5` as the `sqrt5`-involving level-1 completion points of `G` is taken from
  the committed swap closure.
* **Killing sets.**  Solver-free: each is certified by an explicit colouring replayed
  against the exact edge list.
* **Closures.**  Each closed `a` rests on the unsatisfiability of an explicit DIMACS
  instance.  With `--drat` this is checked by drat-trim (the proof files are large, are not
  in the repository, and are regenerated by `prove_closures.py`; their sizes and SHA-256
  are recorded in `closures.json`).  Without `--drat` it rests on the SAT solver.
* **Range of `a`.**  `a ≤ 44` uses `h_S ≥ 90` from the committed budget contribution, which
  is solver-trusted (RC2 optimality).  The solver-free bound `h_S ≥ 74` of the same
  contribution gives the weaker range `a ≤ 60`.
* **Interface lemma.**  The 20 classes are used as the definition of the blocking oracle;
  the verifier replays their 20 witness colourings of `L` explicitly and checks they are
  proper, but their *completeness* (that every proper 4-colouring of `L` restricts to one of
  the 20 patterns up to permuting `{1,2,3}`) is the committed lemma, not re-proved here.
  Completeness is what makes "blocking" equivalent to "all 20 list instances infeasible";
  without it the oracle could only certify 4-colourability, not its failure.

## Negative results recorded here

* **Degree cuts do not strengthen the LP.**  Every inclusion-minimal blocking `X` satisfies
  `sum_{w ∈ N(v) ∩ U} x_w ≥ (4 - |N(v) ∩ L|) x_v` for all `v ∈ U`.  Adding all 303 of these
  to the hitting-set LP over the 6,671 certified minimal killing sets leaves the LP value at
  `111.12`, unchanged (`lp_master.py`); restricting to the 4-core of `U` removes exactly one
  point and also changes nothing.  The gap between the LP bound and the truth is not a local
  density phenomenon.
* **No usable symmetry.**  Among the 24 isometries of the plane given by a rotation about
  the origin through a multiple of 30 degrees, optionally composed with the reflection
  `y ↦ -y`, exactly two map `L` onto `L`: the identity and the reflection in the `y`-axis.
  The latter does not map `U` onto `U` (nor `S` onto `S`), so the replacement problem has no
  symmetry to break (`symmetry.py`).

## Files

| file | rôle |
|---|---|
| `exactgeom.py` | exact reconstruction of the 1,667 points and of all unit pairs in `L ∪ U` |
| `pool5.py` | blocking oracle through the 20 interface classes |
| `cardenc.py`, `test_cardenc.py` | self-contained cardinality encodings (totalizer and sequential counter) and their tests |
| `prove_closures.py` | rebuilds each instance, runs CaDiCaL and drat-trim, records proof hashes |
| `family.py` | loader and solver-free verifier for killing-set families |
| `ihs_a.py`, `ihs_a_milp.py` | decision-form implicit hitting set for one value of `a` |
| `drive_a.py` | runs several values of `a`, accumulating killing sets |
| `certify_a.py` | assumption-based unsat-core extraction (cheap for small `a`) |
| `certify_full.py` | closes `a` with the full family and shrinks it with drat-trim's core |
| `pack_cert.py` | packs the cores into `killing_sets.json` / `closures.json` |
| `decide_drat.py` | DRAT-certified cardinality bounds on `|X|` and on `|X ∩ S|` |
| `lp_master.py`, `symmetry.py` | the two negative results above |
| `verify_pool_closure.py` | the verifier |

Dependencies: `requirements.txt` (python-sat 1.8.dev24 with CaDiCaL 1.9.5, sympy 1.14.0 for
parsing the published coordinates; `lp_master.py` and `ihs_a_milp.py` additionally use scipy
with HiGHS).  drat-trim is needed only for the `--drat` check.
