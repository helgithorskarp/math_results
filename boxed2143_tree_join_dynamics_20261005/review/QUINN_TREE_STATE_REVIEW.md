# Internal check of Quinn's exact maximum-tree insertion state

Author: Quinn, literature-researcher-3. Checker: Theo, literature-researcher-4.
Date: 2026-10-05. Verdict: accept the full stated partial scope of
`TREE_STATE_LEMMA.md`, SHA256
`89dea3f1620f3f9d488eaa0f0cb55fc59d9400b1fb9dbe7d4dc305b1e6fd558b`.
The six-file frozen manifest has SHA256
`5453f312b07df2c304816db33ac279a49af856bb41371832077158b70decb73f`.
Every recorded source/evidence byte and the previously reviewed kernel
dependency matched before and after the independent replay. This is a new
review of this tree packet, separate from kernel444 and extremal-site454.
It is internal team checking, not external peer review or a novelty judgment.
Decision410 remains unsolved.

## Uniform mathematical scope

For a permutation with distinct labels, nearest-greater neighbors and the
maximum Cartesian tree determine one another. Here is a direct interval
argument for the particular identification used by the author. For a node j,
stop on each side at the first label exceeding p_j. Between the two stops
every label other than p_j is smaller. The corresponding interval is precisely
the subtree rooted at j: recursively descending from the global maximum,
larger split points truncate the interval on their side, and the first split
equal to p_j is its root. Conversely a subtree is a consecutive inorder
interval, all its strict descendants are smaller, and any immediately adjacent
point outside it is an ancestor, hence larger. Thus its adjacent boundaries
are exactly the nearest-greater entries.

Inorder traversal identifies the left boundary with the closest ancestor to
the left, and the right boundary with the closest ancestor to the right.
If both exist, they lie on a single ancestor path and are comparable by
ancestry. One is the parent; the farther ancestor exceeds that parent by heap
order. Therefore the smaller-valued boundary is the parent. The kernel's
condition p_L<p_R says exactly that the left boundary is the parent: j is a
right child with some ancestor to the right. A right child already has its
left boundary; a root has neither parent; a left child with both boundaries
has the opposite comparison. These cases are exhaustive. All blockers and
their intervals j+1 through R consequently depend only on tree shape and
inorder indices, even for a parent which currently contains the pattern.

The splitting formulas are correct at all cuts. If the cut is before or
inside the left subtree, the old root remains the suffix maximum and keeps
the remainder of its left subtree plus its full right subtree. If the cut is
after the root, the symmetric statement holds for the prefix. Recursive
splitting exhausts those two cases, including cuts0,n and the empty input.
Adding a new global maximum makes precisely these prefix and suffix shapes
its two children. No label information beyond the shape is needed for the
update.

The weighted recurrence is an exact quotient of *avoiding histories*. Its
inductive base is the empty permutation with weight1. In the induction step,
the accepted kernel says that each legal gap creates an avoiding child from
an avoiding parent. Conversely deleting a global maximum from an avoiding
child preserves avoidance, because it cannot have blocked a rectangle whose
selected values are all smaller. That deletion and the deleted position
recover a unique parent and gap. The state transition and legality are shape
functions, so summing each parent's weight at each legal gap counts every
child once. Different gaps of a fixed parent shape give different root
inorder positions, although different parent shapes can reach the same child
shape. The recurrence retains those latter multiplicities correctly.

The qualifications in the author statement matter. Equality of maximum-tree
shapes does not decide current avoidance for arbitrary heap labelings:
2143 and3142 share a shape and have opposite avoidance status. The recurrence
counts the legal histories starting from the empty state, rather than treating
all heap labelings as avoiders. Catalan many states supplies no bound on their
weights. If every weight has a uniform exponential bound, summing over at
most4^n shapes would prove an upper bound for a_n. If some weights have
unbounded nth roots, they would prove the negative answer. Neither implication
has its missing hypothesis established by this packet.

## Code and independent replay

The author traversal correctly retains the closest right ancestor: going left
sets that boundary to the current root, and going right keeps the preceding
boundary. Its parent and direction identify exactly the eligible right child.
The difference-array union and recursive cut arithmetic implement the
checked formulas. Invalid cut values, including bool and noninteger values,
are explicitly rejected. Internal tree states are generated as well-formed
binary tuples; acceptance does not assume that these routines validate every
arbitrary externally supplied object as a tree.

My `check_quinn_tree_state.py` uses naive greater-neighbor scans, chooses the
smaller neighbor as parent, and constructs shapes with an iterative postorder.
This differs from the author's recursive maximum decomposition and structural
split. The finite replay checks every blocker triple, legal-gap set and child
shape on all5914 permutations through7 and all46233 insertions. For avoiding
parents, the child-avoidance equivalence is independently checked with my
canonical value-rectangle checker; no author verifier is imported.

A separate weighted implementation assigns postorder ranks to a representative
of each heap shape, obtains gaps from value-neighbor scans, and reconstructs
each child from its actual labels. It reproduces every complete avoiding
shape fiber through7 and the author's entire state-weight stream through10.
The resulting finite values a_9=164363 and a_10=1294305 and maximum fibers
43,120,368,1200 at n7..10 agree. They are exact finite calculations, not
asymptotic evidence or a full-target answer. The replay also verifies the
2143/3142 collision directly and rejects four malformed cuts.

Reproduce from this directory:

```sh
python3 -B check_quinn_tree_state.py --output quinn-tree-state-reproduction.json
```

Use `--author-dir` for an unchanged transferred snapshot. Every author file is
checked against the frozen manifest before replay. Deterministic parent-state
stream SHA256:
`27edd2313a64daae1afad84a96ecc7a5145e910d2bfc7c30fa1d9992bf305149`.
The independent run used CPython3.11.2 and the standard library, took about
10.48seconds and peaked at34600KiB Linux RSS, with one process and no solver or
native parallel job. Source hashes and stream hashes, rather than timings,
identify the reproduced evidence.

The written arbitrary-size arguments and inspected Python/stdlib remain the
trust base. No uniform bound on history weights or persistent superexponential
family has been proved. This review accepts that exact structural bottleneck;
it does not preapprove a future entropy argument, a full-growth completion
request, or an external novelty claim.
