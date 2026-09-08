# Direct retention of the checked proof base cannot reach 508

The checked LRAT certificate's initial deletion record retains original vertex
clauses for **26,885 distinct VND source vertices**. Consequently any source
subgraph whose original-label colouring formula contains every original clause
retained by that record has at least 26,885 vertices. Directly carrying this
retained base into a graph cannot meet the 508-vertex target. The bound need
not be sharp: retained edge clauses may require additional vertices.

This is an obstruction to one fixed certificate-retention operation. It is
**not** a lower bound for arbitrary subgraphs of the VND source, all possible
refutations, rewritten proofs, or coordinate identifications. No physical core
was extracted and no further SAT call was made.

## Precise certificate and argument

The input formula, whose byte hash is fixed in `EXPECTED.json`, has 64,513
vertices and 2,234,404 clauses. Its first 64,513 clauses are, in source order,

    A_v = X(v,0) or X(v,1) or X(v,2) or X(v,3),  v=0,...,64512,

where the variable number of X(v,c) is 4v+c+1. These rows have one-based clause
labels v+1. The formula then lists four binary colour constraints for each
edge and three palette pins. The already verified source has distinct physical
points for all source vertex labels.

The first LRAT line deletes exactly 1,768,793 original clause labels, leaving:

| Original clause type | Retained count |
|---|---:|
| Vertex at-least-one clauses | 26,885 |
| Edge clauses | 438,723 |
| Palette pins | 3 |
| Total | 465,611 |

A formula formed on a source subset S can contain A_v as an original vertex
clause only when v belongs to S. Hence retaining all these vertex clauses
forces |S| >= 26885. An injective renumbering changes no cardinality. Selecting
a subset of the premises or using a different refutation is a different
operation and is outside this bound.

The compact `SUPPORT_GATE.json` includes 509 distinct retained vertex-clause
labels. They alone witness failure of the 508 budget. The complete retained
vertex-label set is counted and hashed rather than stored in Git. The verifier
also binds the entire CNF and LRAT by SHA256 and checks every original vertex
row directly against its expected four variables. It validates the initial
LRAT deletion syntax, range and uniqueness, then counts its complement using a
byte array. The certificate producer used a set complement. Four controls
substitute a deleted vertex clause, duplicate a witness label, change the
claimed count, or broaden the scope to arbitrary subgraphs; all are rejected.

Run against the previously generated and checked files without invoking a SAT
solver:

```sh
python3 verify_support_gate.py --work /path/to/vnd-case10-work
```

Expected status: `VERIFIED_VND_FIXED_RETAINED_BASE_ORDER_GATE`.

The trust boundary is the elementary source-label argument, the pinned formula
and LRAT bytes, Python integer/byte-array operations and SHA256, plus the source
point distinctness established in the parent package. This check does not need
to rerun proof verification: its order bound concerns the explicitly retained
original base, independently of whether that base is satisfiable. The parent
package supplies the separate non-four-colourability certificate. This finding
closes direct retention of that base as a target-scale route; it leaves the
large positive source intact and establishes no record improvement.
