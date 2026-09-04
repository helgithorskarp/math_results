# Independent review of the Parts 108/789 union minimum

This directory records reviewer-1's clean-room check of the committed claim
`bafkreihi75b6dzd7ec7u5ibba5eziuthvz5n6rz3yx4fb6tvzh6kgja5yq`:
within the explicitly defined strict unit-distance union of exceptional Parts
placements 108 and 789, every non-4-colourable induced subgraph has at least
509 vertices, and the bound is attained by the identity Parts placement.

This is an intermediate negative result about one 525-vertex coordinate pool.
It is not a sub-509 five-chromatic unit-distance construction and does not
exclude other pools, coordinate changes, or delete-and-repair constructions.

## Independent argument and computation

The submitted certificate has SHA-256
`85ea2050dbc6ff05b2766f899e86ba3b9157e4aa59cc6ef21f54f7531941c728`.
The submitted standard-library verifier was first run unchanged and returned
its documented summary, including 525 vertices, 2,551 edges, 489 forced
vertices, 133 deletion sets, and transversal number 20.

`independent_check.py` does not import the submitted verifier.  It instead:

1. reconstructs the union over `Q(sqrt(3),sqrt(5),sqrt(11))` using a generic
   squarefree-monomial product and exact integer numerators at denominator 192;
2. enumerates every exact unit pair and recovers 2,551 edges with SHA-256
   `4f7a2472d60aa0835a256b51dc9d1e3eb050b3e575bb41fa814961ce48496a47`;
3. directly checks all 489 colourings of `U-v` and all 133 colourings of
   `U-D`, totaling 1,577,939 retained-edge checks;
4. proves that the 133-set hypergraph has no hitting set of size at most 19
   using a separately written binary include/exclude DPLL search (2,338
   states), not the submitted verifier's disjoint pivot branching; and
5. checks directly that the 20 optional identity-placement vertices hit all
   133 sets.

The mathematical implication is short.  A colouring of `U-v` means any
non-4-colourable induced subgraph must contain `v`; hence it contains all 489
forced vertices.  A colouring of `U-D` means its remaining optional vertices
must meet `D`.  They therefore form a transversal of the certified family,
whose minimum size is 20.  The order is at least `489+20=509`.

Run with CPython 3.11 or newer from this directory:

```bash
python3 independent_check.py
```

The deterministic output is in `expected_output.txt`.  The checker uses only
the Python standard library, exact unbounded integers, and one CPU core.

## Sharpness and trust boundary

The independent checker verifies the identity placement's exact 2,442-edge
digest and its explicit proper 5-colouring.  Non-4-colourability of that
placement is imported from the sibling Parts criticality artifact, whose
certificate is pinned at SHA-256
`d354f9629c41639168b80fc1aa6feb6e4187dd37dee7efcb83b4ef6ebe68d16c`.
The criticality artifact bridges non-4-colourability to an external DRAT proof;
the separate replay details and hashes are recorded in `drat_audit.txt`.

The clean-room lower bound trusts CPython integer arithmetic, this checker's
small multiquadratic implementation, the pinned point and certificate bytes,
and the reviewer's exhaustive DPLL code.  It trusts no SAT solver.  Sharpness
additionally trusts the audited CNF bridge, the externally mirrored DRAT bytes,
and `drat-trim`.

The submitted source was inspected at repository commit
`163022bba6666fddcf6e770e27c92a2ca2043a62`; the target directory was unchanged
on `main` at the time of review.
