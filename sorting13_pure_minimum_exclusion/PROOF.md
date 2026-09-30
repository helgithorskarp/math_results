# Pure-minimum K18 exclusion via a nine-wire completion lower bound

Author and executing agent: **six-sorting-2, researcher**. Comparator(a,b),
a<b, puts min on a. All gate orders and depths are allowed.

**Theorem.** The explicit109-state nine-wire target L has minimum size
**17 or18**. In particular no16-comparator sorter of L exists.
Consequently every18-comparator sorter of the127-state ten-wire target K,
if one exists, has a unary event in its minimum kernel. The binary-only
minimum kernel is excluded completely. K remains18..20, X136 remains21..22,
and the thirteen-input44-versus45 question remains open.

## Target and imported structure

The exact generalized fourteen-gate eleven-wire prefix A, its output
permutation, all rows and controls are in the dependency's
[fixture](../sorting13_maximum_preparation/fixture.json). Append C=(3,10)
and B=(6,9),(9,10). Wire10 holds the global maximum and the lower ten wires
give K. Append the binary minimum word M=(0,5),(0,1). Wire0 is now globally
minimal; wires1..9, renumbered0..8, give L. The full prefix has19 gates.
The known S11=35 implies s(L)>=16, and the checked18-gate control gives
s(L)<=18. The new refutation raises the lower bound to17.

The [binary-front reduction7436](../sorting13_double_pure_obstruction/PROOF.md),
source b10a2bd5584e90135012808e6eef049bd3544fca, shows that any K18 sorter
with a binary-only minimum kernel normalizes to M followed by an L16 sorter.
That reduction uses only disjoint binary commutations. The new nonexistence
therefore excludes the entire pure-minimum K18 branch. The other42 minimum
kernel words, other X kernel classes and arbitrary13-input prefixes remain
outside this theorem.

The [necessary structural theorem7474](../sorting13_maximum_preparation/PROOF.md),
source4ac1823cf27985a6ec871bd4b636e7cd17ccb7a3, applies to every L16 sorter:
the sole0 gate is(0,1); the maximum routes from3,4,5,7,8 have passage counts
4,4,2,4,1; their kernel has exactly five events, four binary and one unary.
The phase/refill conditions force(5,7),(7,8), no earlier5/8 event, no7/8
event between them, no later8 event, and exactly one later7 gate on5/6.
A later(5,7) requires an earlier(6,7). These conditions retain every
admissible interleaving. We do not front-load a unary event.

The earlier7474 refutation concerned zero/one nonkernel preparations.
The present formula imposes **no root-time restriction**. Its full source
includes all36 pairs in each of16 sequential slots and all109 target rows.

## Additional exact ternary witnesses

Give each original eleven-wire input a low/middle/high color. Let m be the
middle count and D the number of prefix gates incident to a nonmiddle
value. Deleting those gates and propagating middle ports leaves a circuit
sorting m middle values if the full35-gate completion exists. Standard
normalization and the established lower bound S(m) imply the remaining
suffix budget35-S(m)-D for such deleted gates.

Let x be the evolving high Boolean threshold and y the nonlow threshold.
A suffix gate is deleted precisely when an endpoint has a1 in x or a0 in y.
Write its union-event count as H(x,y). Each witness thus gives
H(x,y)<=35-S(m)-D. The existing53 witnesses are independently checked in7474.
We add the92 explicit original-input witnesses in additional_witnesses.json;
all have capacity at most8. Their validity does not rely on exhaustive
enumeration of all ternary inputs or on a claim that this selection is optimal.

The independent scalar/rank/middle-port audit checks all92 new witnesses
on10936 Boolean/rank assignments and184 distinct-rank controls. It checks
the actual threshold masks, D, m, capacity and retained middle-port circuit.
The combined145 witnesses constrain actual input executions; an OR of
separate one-hot trajectories is used only for counting kernel events.

## Complete arbitrary-depth refutation

The sequential encoder implements each selected comparator exactly on all
109 Boolean rows and requires every final row to be sorted. It includes
all145 union bounds and the proved7474 necessary structure. No fixed
parallel depth, lexicographic condition, repeated-pair ban, future interval
restriction or selected maximum-root position is used. Any L16 sorter
therefore extends to a satisfying assignment of this formula.

The source-regenerated formula has **34194 variables/726755 clauses**, SHA256
**4fb7cabafebaa7a4287be430eec234ae5d59aa048d92bb99bb5c4a141c3d7875**.
Glucose4 returned UNSAT at23582 conflicts,9.84 solver seconds, within
one thread/30000 conflicts/40 seconds. DRAT-trim verified the native trace
with zero RAT lemmas. Its compact core contains13374 original clauses;
the deletion-free certificate has13084 reverse-unit-propagation additions.

The standalone watched checker verifies every addition, reaches the empty
clause and checks every core clause against the exact regenerated full
formula.4608 truth-table controls and rejection of a premature empty clause
test the checker. Its code is explicitly reused from7474, with original
watched implementation credited to six-sorting-1/source5ad75ecb80164da04c921f1898cf62334668a027
and graph7452. The earlier occurrence-index provenance reaches7306.
This algorithmic check is not an external-person review.

The known L18 word is a separate positive control: its model is checked
against every generated clause, all109 L rows, all2048 original inputs
and all145 marker bounds with capacities shifted by2. This control does
not provide an L17 construction. Native traces, full generated CNFs and
models remain in ignored scratch; only the compact core/RUP certificate,
small witnesses and source are published.

## Scope and trust boundary

The new information is a complete L16 exclusion and the pure-minimum K18
corollary. A private preliminary exact-four formula with only53 cuts
returned UNKNOWN; it was not used as nonexistence evidence. Separate
timing-class refutations led to the stronger witness set; those exploratory
certificates are not needed for this proof or published here.

The primary lower bounds and pruning/standardization come from
[Harder](https://arxiv.org/abs/2012.04400v3),
[Codish et al.](https://arxiv.org/abs/1405.5754v3), and the
[current primary table](https://bertdobbelaere.github.io/sorting_networks.html).
Their original large proof corpora were not rerun. Written pruning, binary
commutation, the7474 structural necessity and encoder correspondence remain
mathematical trust boundaries. No formalization or historical priority for
the general methods is claimed. There is no global44 exclusion or44 witness.
