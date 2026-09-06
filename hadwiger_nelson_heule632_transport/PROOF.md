# Exact extension and the fixed-library decision

Let H be the archived 510-point Heule support and F the fixed 122 completion
centres of `../hadwiger_nelson_heule_fresh122_incidence`. Write H632 for the
strict unit-distance graph on H union F. It has 632 distinct points and
3,112 edges: 2,504 inside H, 551 between H and F, and 57 inside F.

The inherited exact incidence certificate shows that F has 65 tree
components and one 37-vertex component with unique cycle
`1239,1370,1522,1371` in cyclic order. Labels here are archived
`centre_index` values. The new verifier rechecks every coordinate pair
of H632, using exact integer arithmetic at denominator 96, and checks
the inherited structure. No completeness claim about other possible
completion centres is needed.

## Exact list extension for arbitrary deletions

Choose arbitrary retained subsets O of H and Q of F, and fix a proper
four-colouring c of O. For each v in Q define

```
A(v) = {0,1,2,3} minus {c(u): u in N_H(v) intersect O}.
```

An extension of c to O union Q is equivalent to a list colouring of Q
from these sets: the lists enforce precisely the old-to-fresh edges,
and the fresh graph enforces precisely the remaining new edges. The
old edges already hold. A missing vertex and an empty list are different:
the former is absent from the graph; the latter makes a retained vertex
impossible to colour.

For a rooted tree, process children before parents. Let S(v) be the
colours feasible at v in its descendant subtree. Inductively,

```
S(v) = {a in A(v): every child w has some b in S(w) with b != a}.
```

The induction is exact because the child subtrees are disjoint with no
edges between them. A tree is list-colourable if and only if its root
set is nonempty. A witness is recovered from parent to children by
choosing a supported colour different from the parent colour.

If any vertex of the unique four-cycle is omitted, Q is a forest.
Otherwise fix the minimum-labelled cycle vertex z, try each a in A(z),
remove z, and remove a from each retained neighbour's list. What remains
is a forest. A trial succeeds if and only if a full extension with
c(z)=a exists. The disjunction of at most four forest tests is therefore
exact, including empty and singleton lists. Distinct components factor
once the old colouring is fixed. `oracle.py` implements this procedure.
It needs linear time in the input graph for a fixed palette of four
colours; it does not invoke SAT or enumerate old colourings.

The optional-vertex interface uses a dictionary of selected labels and
four-bit masks. An omitted key means a deleted vertex; mask zero means a
retained vertex with no available colour. The precondition is the supplied
certified forest/unicyclic structure and its correct cycle labels. The
code checks that the graph on which it performs forest propagation is
acyclic; it is not a general recognition algorithm for arbitrary graphs.

## Independent algorithm

`independent.py` imports no producer. It enforces arc consistency on
every directed retained edge: delete colour a from the list at u if
the list at v has no colour different from a. Every deletion preserves
all valid list colourings, and the finite process terminates.

On a forest, nonempty arc-consistent lists guarantee a colouring:
choose any root colour and extend outward, using the support property
at each directed edge. On the unicyclic component, enumerate all tuples
on the four remaining cycle lists and keep one satisfying the cycle
edges. Every original colouring gives such a tuple, because arc
consistency never deletes a colour belonging to a valid colouring.
Conversely, any retained proper cycle tuple extends outward into its
attached trees by the same support argument. Other components are trees.
Thus failure of this test is also an exact failure to extend the fixed
old colouring, not just failure of a greedy heuristic.

The independent implementation drains the cycle reconstruction queue
before choosing roots of other retained components. The six-vertex
control fixture labels its attached branch below the cycle vertices;
vertex deletions can isolate that branch while keeping the cycle. This
tests the distinction between disconnected selected components and a
single connected component in the original graph.

The two algorithms and direct assignment enumeration agree on all
182,667 frozen control cases:

* All 17^4 assignments on a four-vertex path: one deleted state or any
  of 16 four-colour lists independently at each vertex.
* The same 17^4 assignments on a four-cycle.
* All 5^6 assignments on a four-cycle with a two-edge attached branch:
  a deleted state or any subset of two colours.

Both algorithms' positive witnesses are checked directly. An odd-cycle
control fails with identical two-element lists, and malformed lists,
unknown labels and a K4 supplied as a pseudoforest are rejected. These
finite controls check implementation details; the induction and cycle
reduction above establish the general quantified correctness statement.

## The frozen 544-colouring experiment

The positive H514 library contains 516 interface rows, 15 profile rows
and 13 final rows. Its independent acceptance and raw-recipe decoder
were published before this run. Here each string is restricted to its
first 510 characters, dropping the four original fresh-point colours.
The oracle may recolour all 122 fresh points. No old colour is changed
and every one of the 122 fresh points is retained in this experiment.

The row order and all input hashes were frozen in `plan.json` before
testing extensions. The restricted library has 532 rows omitting one
old vertex, 10 omitting two, and two omitting three; it includes a
singleton omission for every one of the 510 old vertices. All 544 rows
are tested against all 66 fresh components, for 35,904 exact decisions.
No adaptive new colouring, graph shrink or native solver call is allowed.

Exactly 22 rows extend to the full retained H632 support. Each omits
one distinct old vertex, giving the following valid singleton cuts:

```
11,39,48,51,81,105,142,145,168,179,199,200,
212,220,225,226,241,300,328,366,473,504.
```

Every subgraph of H632 omitting one of these vertices is four-colourable,
by restriction of the corresponding checked positive witness. All
68,225 retained edge inequalities of these 22 witnesses are checked.
The certificate stores only the new 122-character tails and their
canonical source-row references; the old colours are decoded and
verified from pinned public data.

Of the 522 failing old colourings, 505 give at least one fresh vertex
an empty list. The other 17 have nonempty lists everywhere but fail a
coupled fresh component. At the component level there are 1,418 failed
tests: 1,239 with an empty list and 179 with nonempty lists. The
37-vertex component accepts 77 of the 544 old colourings; every other
component accepts at least 452. This is a statement about this fixed
library, not all possible old colourings.

For a concrete coupled failure, row `interface:462` omits old vertex
486. Every fresh list is nonempty, but centres 809 and 1041 are adjacent
and both have the singleton list `{1}`. Their old neighbour colours are

```
809:  396->2, 405->2, 427->0, 433->3;
1041: 379->3, 396->2, 407->0, 450->2.
```

This verifies that checking only for empty fresh lists would be
insufficient. It does not prove that H632 minus vertex 486 is
non-four-colourable: another old colouring could extend.

## Decision and scope

If at least 509 distinct old singleton deletions had extended, every
subgraph on at most 508 vertices would omit one of those 509 vertices
and hence be four-colourable. The actual 22 cuts do not meet this
criterion. Therefore the fixed-library assessment is complete but
the H632 family remains open. Global permutations of the four colour
names preserve each row's extension verdict, but arbitrary recolouring
of old vertices was not tested.

No at-most-508 five-chromatic graph, non-four-colourability result for
any of the 522 failed rows' supports, or complete H632 subgraph closure
is claimed. The earlier H514, H517 and H574 closures remain restricted
to their own supports. The current work supplies a verified exact
extension procedure and a complete finite transport decision, and
stops before another library-refinement or candidate-search phase.
