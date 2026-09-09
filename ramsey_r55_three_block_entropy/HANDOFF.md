# Three-block carrier bound and physical witness interface

**Certified effect:** at least 74.45253502733943% removed from the entire h4059 bare carrier, and at least 32.10443932984054% from every task carrier. All 18 classes and all 2,189,178 original task IDs are covered. These are lower bounds on removal; the refined global cardinality is not counted exactly, and zero new task verdicts are assigned.

The three exact local probabilities and per-class rational upper bounds are in `EXPECTED.json`. The projection inequality uses each non-root matrix coordinate exactly `3(q-3)` times. It preserves root multiset ties and every labelled matrix assignment. The new matrix restrictions are independent of the fixed core and allowed root/contact coordinates. No degree-bound multiplier is used.

For a complete physical coloring, save

```json
{"task":"bo1-q9-r5-c000000","graph":{"n":43,"red_hex":"226 lowercase hexadecimal digits"}}
```

and run:

```sh
python3 -B ramsey_r55_three_block_entropy/physical.py /tmp/r55-complete-input.json
```

The word uses the original 903 lexicographic edges, bit zero=(0,1), red=1. The interface validates the graph representation and fixed block colors. Original carrier membership is a caller precondition for applying its carrier measure; this predicate does not certify the core, root order, contacts, or maximality.

- `THREE_BLOCK_RAMSEY_REJECT` includes a literal monochromatic five-set, its centre block, and the two other non-root blocks. `verify_witness` checks all ten physical pairs and the 3+1+1 split.
- `NO_THREE_BLOCK_WITNESS_NOT_TARGET` means only that this particular filter found no obstruction. It is not a target verdict or a new carrier rank.

These clauses already occur in the complete original Ramsey CNF. The certified effect is on the size of the explicit physical carrier, not demonstrated SAT speedup. Do not apply its percentage to a carrier conditioned on arbitrary ordinary-matrix entries or to the 161 q10 child prefixes without a separate argument.

This pass consumes no team-r55-1 child input and requests no ownership transfer. h3987 stays 99 certified closures/161 UNKNOWN. The separate h4063 queue keeps 67 active children and redirects 94; redirects are not UNSAT. This percentage uses the un-oriented h4059 carrier and is not composed with color orientation or applied to that queue; h4001 separately stays 518 exclusions/122 UNKNOWN. The reviewed h4045 bridge and h4059 contact package remain unchanged.

The one predeclared milestone ends here. There is no automatic root-triple, 2+2+1, larger-tuple, matching, degree, or alternate-cover tail.
