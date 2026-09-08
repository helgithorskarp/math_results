# Global greedy closure for the good43 packing cover

This contribution strengthens the independently reviewed h3835 complete
43-vertex interface. **Every possible good43 has a labeling in 39 refined
branches**, with explicit forbidden-clique constraints across whole unions
of blocks. A complete covering carrier has fewer than 2^785 codes and is
more than six times smaller than the original rooted family. Each code
specifies all 903 physical edges. Codes may duplicate graphs and may fail
remaining target constraints.

There is no good43 candidate, solved branch, or Ramsey-bound improvement
here. No target solver was called. The contribution is a global normalization,
checked multi-block strengthening, and complete physical handoff.

## Mathematical result

Choose red K4s greedily up to seven, and red triangles greedily up to four
in the remaining tail15. Exhaustion of the preferred color forces:

- No red K4 in a whole 23- or 19-vertex residual when r=5 or6.
- No red triangle in a whole 12-, 9- or 6-vertex residual when s=1,2 or3.
- Branch labels r=5..7, s=1..4, with t=0..2 for s<4 and t=0..3 for s=4.

This gives 39 branches. Among their 106,263 added clauses, 103,941 involve
at least three blocks. Thirty-five retained branches gain clauses; four
with r=7,s=4 remain unchanged. In particular, the earlier all-red UNKNOWN
branch remains undecided.

The triangle-free residual also has no independent five-set. Complete
Ramsey(3,5) catalogs therefore give a coupled carrier across its blocks.
An exact ordered-partition recurrence and a separate vertex-to-bin checker
agree on every catalog entry. No graph automorphism quotient is used.
Combining the residual carrier with all remaining matrix coordinates proves
an upper-bound reduction factor of 6.282136433381775... from the old exact M.
This is a cardinality comparison for a globally complete represented family,
not a measured solver speedup or an isomorphism census.

See [PROOF.md](PROOF.md) for the global coverage theorem, the counting
conventions, catalog trust boundary, and exact inequalities. Exact branch
counts and carrier definitions are in [GLOBAL_COUNTS.json](GLOBAL_COUNTS.json).
The 21 omitted old labels are removed through normalization; their old
formulas are not thereby proved UNSAT.

## Reproduce

Python 3.11.2 and its standard library suffice. The sibling package
[ramsey_r55_global_clique_packing](../ramsey_r55_global_clique_packing/README.md)
is required at its pinned h3835 source. `base.py` checks every parent source
file against its exact manifest before importing anything. The parent is
never modified. From the repository root:

```sh
python3 -B ramsey_r55_global_greedy_closure/reproduce.py
python3 -O -B ramsey_r55_global_greedy_closure/reproduce.py
```

Both return `VERIFIED_GLOBAL_GREEDY_CLOSURE_PUBLIC_REPLAY`. The replay checks
334 catalog graphs, every one of 167,046 ordered partitions, all 39 branch
counts and all added clauses, 2,889 tail-code boundaries, 117 whole43 code
boundaries, 39 greedy-normalization fixtures and the target-decoder rejection
controls. Normalization fixtures are deliberately non-target physical graphs.

To regenerate and independently audit the seven complete target formulas,
use a new directory **outside the repository** (about 441 MB):

```sh
python3 -B ramsey_r55_global_greedy_closure/reproduce.py \
  --generate-cnfs /tmp/r55-greedy-closure-cnf
```

To audit already generated formulas, replace `--generate-cnfs` with `--cnfs`.
The exact expected formula hashes and dimensions are in
[FULL_AUDIT.json](FULL_AUDIT.json). All 9,858,581 clauses were independently
reconstructed literal by literal. Generated CNFs, logs and caches are not
published. [VALIDATION.md](VALIDATION.md) records the actual replays and limits.

## Use the physical interface

[TASKS.json](TASKS.json) specifies 39 stable `gc1-rR-sS-tT` task IDs, their
parent branch labels, complete formula dimensions, residual constraints,
covering intervals and carrier choices. [HANDOFF.md](HANDOFF.md) gives the
immutable handoff convention and exact task semantics.

The least covering count is `gc1-r5-s1-t2`, below 2^752 codes. Its residual
carrier factor decreases by more than 1,207,063,026. This ordering is a count
comparison, not a runtime prediction. Generate its complete formula:

```sh
python3 -B ramsey_r55_global_greedy_closure/strengthen.py \
  --branch 5,1,2 --cnf /tmp/r55-gc1-r5-s1-t2.cnf
```

It has 847 variables (846 physical cross edges plus the true constant),
1,401,670 clauses, and SHA256
`8cbdf4a80e185b68dd9b12221863128e17029cb2936d290c09027ded90d964eb`.
All 962,598 five-subsets are handled by the retained parent layer, with 4,987
additional closure clauses. No single saved residual is fixed as the search.

Decode any covering code into a complete physical state:

```sh
python3 -B ramsey_r55_global_greedy_closure/carrier.py --index 0
```

The CLI reports both any residual-closure obstruction and the independent
physical target check. Code zero fails; a decoded carrier state is not a
candidate certificate. A SAT result is accepted only after complete physical
and refined-branch checks:

```sh
python3 -B ramsey_r55_global_greedy_closure/accept_model.py \
  --branch 5,1,2 --solver-output /tmp/solver.model --output /tmp/good43.json
```

This contribution supplies no SAT model. Every refined formula is still a
full 43-vertex decision problem. UNSAT for one refined task would not by itself
exclude all graphs in the corresponding older, weaker branch.

## Dependencies and scope

The global forcing and CNF coverage use the accepted h3835 theorem and an
elementary R(3,5)<=14 argument. The catalog covering bound additionally imports
completeness from [McKay's Ramsey graph page](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html).
The three small input catalogs and their original hashes are recorded in
[catalog-inputs.json](catalog-inputs.json). The data are attributed to
Brendan D. McKay under the terms on his
[data page](https://users.cecs.anu.edu.au/~bdm/data/).

Parent source: `3f06352ae0735101a04afa1ba7b055736e7300f7`.
Independent parent review source: `daec8e19799d254263f916c9ad4dd9b71464b403`.
This new strengthening awaits external review. Greedy maximality is standard;
no historical novelty is claimed. This is not proof-assistant formalization.
The failed good19 bridge, its saved witness, and the parked fixed-neighborhood
routes are unused. [provenance.json](provenance.json) records the graph context;
[SHA256SUMS](SHA256SUMS) records file integrity.
