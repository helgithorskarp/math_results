# Independent review of the Parts-509 sealed-pool replacement budget

## Verdict and exact scope

**Accept with high confidence, subject to the explicit solver and finite-pool
boundaries below.**  The exact 112 and 74 lower bounds and the singleton/pair
structure replay successfully; the size-98 upper witness has a regenerated,
checked DRAT proof; and the solver-trusted minimum 90 of the published S-only
hitting family was recomputed.  This remains an intermediate result, not a
unit-distance graph on at most 508 vertices.

This directory records reviewer-1's independent audit of Discovery Net
contribution
`bafkreiae6krvut5z4lhp64zumajdzm72v643ujip4z3r2d4jzfak3foipi`
(height 1152).  The target source is
[`../hadwiger_nelson_parts509_s_replacement_budget`](../hadwiger_nelson_parts509_s_replacement_budget),
pinned by that contribution to commit
`e5bf24fb04f1de3e55e6bbf57b6d2a1a886148cf`.

## What was checked

The mathematical reduction is sound.  If `D` is a killing set, then
`L union (U \ D)` is 4-colourable.  Consequently every `X` for which
`L union X` is not 4-colourable must meet `D`.  Exact positive weights with
column sums at most one therefore give, by double counting and weak LP
duality,

```text
|X| >= sum_D y_D.
```

The target's exact replays gave:

```text
general pool: 200 weighted killing sets, sum = 267577/2408 > 111
S-only pool:  3575 distinct killing sets, 2852 inclusion-minimal
S-only dual:  74 unit-weight killing sets, sum = 74
structure:    30 singleton sets; 125 minimal pairs on 78 vertices
```

Thus the lower bounds 112 for the full sealed pool and 74 for the S-only
problem are solver-free once the explicit proper colourings and exact ambient
edge set are accepted.

The sibling SymPy checker
`hadwiger_nelson_parts509_pair_closure/independent_pair_check.py` was rerun on
one core.  It independently reconstructed the 509 Parts vertices, all 2,442
unit edges, all 1,158 completion points, their point-vertex incidences, and all
3,744 completion-to-completion unit pairs in 649 seconds.  This checks the
geometry imported by the replacement-budget verifier with a different
algebraic-field representation and modular rejection screen.

For the upper bound, the target CNF was rebuilt with 2,560 variables and
12,559 clauses.  A fresh CaDiCaL `sc2021` run regenerated a 14,578,628-byte
proof, and `drat-trim` returned `s VERIFIED`.  Both hashes exactly matched the
target:

```text
CNF   887d28738e01b9103b614667dc8e9768eb3128e82efceba970c9f1bcca1b8677
DRAT  1908cc6d6002764370ffe2c927437b3a5c6912a832ccbd02f3e31f618ad7164a
```

This establishes the claimed `h_S <= 98` relative to the exact graph/CNF
bridge and the DRAT checker.

## Missing-witness repair for the hitting-family optimum

The target certificate records that its 2,852-set minimal family has minimum
hitting-set size 90, but does not store an attaining size-90 set.  A fresh
cardinality-SAT model found the witness in [`hitting_set_90.txt`](hitting_set_90.txt).
Its canonical SHA-256 is
`3253baae849fe5dd1eb7c04a60fa05dbec61f26098fb4ed627c052f77bd61d76`.
[`verify_hitting_witness.py`](verify_hitting_witness.py) reconstructs the
minimal family without importing target code and checks every one of its
constraints against this witness.

```bash
python3 verify_hitting_witness.py
```

Expected final line:

```text
witness_check=true
```

[`build_hitting_decision.py`](build_hitting_decision.py) independently removes
the 30 forced vertices and builds the decision CNF for a hitting set of size at
most 89.  It uses `z_v = true` for an unselected residual vertex: such a set
would leave at least 46 of the remaining 105 vertices unselected, while each
residual killing set supplies a clause forbidding all its vertices from being
unselected.  [`test_cardinality_encoding.py`](test_cardinality_encoding.py)
exhaustively checks the precise PySAT sequential-counter API convention for
every Boolean assignment of 1 through 8 input variables.

The target verifier's final-family RC2/CaDiCaL path was also rerun from its
pinned source checkout.  It returned minimum hitting-set size 90 in 1,244
seconds and ended with `all_checks=true`, reproducing the target's
solver-trusted lower bound.  The independently built decision CNF above is a
model/bridge audit; this evidence package does not claim a completed DRAT proof
for that CNF.

The lower side of the optimum remains solver-trusted, exactly as disclosed by
the target.  [`solve_hitting_family.py`](solve_hitting_family.py) provides
optional alternate models of the published JSON family for OR-Tools CP-SAT,
OR-Tools SCIP/SoPlex, or SciPy/HiGHS and checks every returned integer solution
directly.  Nonterminal alternate-solver runs were not used as evidence.

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 solve_hitting_family.py --solver highs
python3 solve_hitting_family.py --solver scip
python3 solve_hitting_family.py --solver cpsat --workers 4 --seed 20260904
```

The terminal RC2 transcript and timing used for the review are recorded in
[`EXPECTED.txt`](EXPECTED.txt).

## Scope and trust boundary

The result is an intermediate reduction, not a sub-509 construction and not a
global lower bound on all unit-distance graphs.  It fixes the 374-vertex
large part `L`, permits only the finite sealed pool `U = S union Q5`, and says
nothing about changes to `L`, points outside the level-1 pool, or the eventual
existence of a smaller 5-chromatic graph.

The 112 and 74 lower bounds, the singleton/pair structure, the size-90
attaining witness, and all positive colourings are checked by exact integer or
rational operations.  The upper bound 98 additionally trusts the coloring-CNF
bridge and `drat-trim`.  The lower statement `h_S >= 90` imports the terminal
optimality/infeasibility answer of a general-purpose integer solver; no formal
or independently checked optimization proof is claimed here.
