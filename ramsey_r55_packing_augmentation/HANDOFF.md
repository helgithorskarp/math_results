# Receiver contract

The new rule shrinks the global h3887 carrier by 5.4948%, with exact fractions
in every q8 and q9 task. It covers every good43 by allowing physical
repacking to an existing larger-q task. It is a global coverage change,
not a certificate of UNSAT for any existing task.

For a q8/q9 task, deterministically select 4/2 edges of the fixed core's
lexicographic greedy red matching. For each red block and each pair of
selected edges, emit six clauses forbidding complementary two-position
completions. These have eight negative physical edge literals. The count
is 36r clauses for q8 and 6r for q9, with no auxiliary variables.

`transport.py input.json --clauses` emits the physical clauses. Its input
is a complete graph/packing object with fields `n`, `red_hex`, `blocks`,
`core`, `r`. n=43; `red_hex` has 226 lowercase hex digits and represents 903
edge bits in lexicographic pair order, bit 0 for (0,1), positive meaning red.
The four-vertex blocks partition the complement of `core`; the first r
blocks are red K4s and the rest blue K4s. Input validation checks block
colors, the Ramsey(4,4) core and red maximality. The output clauses use
one-based indices in that same 903-pair order; map them explicitly to any
owner encoding before use.

`transport.py input.json` returns either
`NO_SELECTED_AUGMENTATION_NO_RAMSEY_VERDICT` or a packing transport packet
with status `PACKING_TRANSPORT_NEEDS_CATALOG_AND_ROOT_ORDER`. Save that
packet and run `verify_transport.py input.json packet.json` to independently
check every physical edge, the partition and source binding. The new graph
has the same physical edges under a vertex permutation, one additional red
block and four fewer core vertices. The packet does not supply a catalog
index, enforce the root ordering, or claim full carrier membership or a
Ramsey verdict. Apply the existing catalog/root/block normalization before
using it as a new task. A second q9 violation is transported to q10; no
new constraint is imposed there.

**Do not add these clauses as Ramsey implicates to a fixed old task.**
Their justification requires the complete family, including the destination
tasks. A failed clause means "represent this graph under a larger packing",
not "this graph has a monochromatic five-set". Integration into a partial
solver family requires its owner to establish destination coverage.

team-r55-1 retains all ownership of the 161 q10 children and testing h4021
on that carrier. No such child, physical model, proof, or formula was read
or processed here. This handoff requests neither action nor ownership
transfer. h4001 remains 518 whole q7-r5 exclusions plus 122 UNKNOWN tasks;
the overall whole-task count remains 2,188,660. The separate q10 ledger
remains 99 certified closures and 161 UNKNOWN children.

The accumulated h4009 edge window, h4015 neighborhood theorem, h4021
cross-pair interface and h4029 degree result remain intact. Their properties
hold for any relabeling of a good43. No conditional speedup or additional
q10 pruning is asserted. The exact count and physical interface are the
completed milestone; expanding the exchange patterns or launching a
nearby catalog/solver phase is not part of this handoff.
