# Theo's distinct full partial review of Quinn526

Author: literature-researcher-3. Checker: literature-researcher-4.
I accept the uniform external-leaf language and all three contextual
recurrences, the explicit same-size child-multiset collision, and the
uniform four-leaf fixed-perfect-tree obstruction with its conditional
factorial bridge. This is an internal team check, separate from467/498.
It makes no novelty claim or full-target410 conclusion and excludes529.

The frozen four-file manifest is
3104057158e26d7d866005ad06f10a4ba6d50e8271da48c944ca1bb70d37b85c.
BOUNDARY_AUTOMATON_PROBE_V1.md has SHA256
ca88ad5b871895164bb6113bc9b8c556cc78c87e0c71a330e8ef0759c581991f;
PERFECT_LEAF_OBSTRUCTION_V1.md has SHA256
bbe578f20924db61e345a249f1bb9b5eb6126455a17dac49b37301fd55f2dd98.
The three named previously accepted dependencies also match their hashes.

## Uniform reconstruction

Use the previously checked blocker equivalence: a node j blocks insertion
gaps iff it is a right child and has an ancestor on its right. Its first
property says its path ends in R; its second says some earlier edge was L.
The right subtree of j has consecutive inorder gaps j+1 through R_j,
including its external right boundary gap, where R_j is the nearest right
ancestor. Those are exactly the forbidden gaps in the accepted kernel.
Their root-to-external-leaf paths take another R immediately after reaching
j. Conversely an external path containing consecutive RR with an earlier
L identifies such a node j at the first R of that pair. Hence a gap is legal
iff its path has no such RR. Here RR means consecutive letters; the earlier
L can occur anywhere earlier. No empty-tree or outer-boundary exception is
needed.

Before any L has appeared, a left step enters context B and a right step
stays in A. In B the previous letter is L: a left step stays in B and a
right step enters C. In C the previous letter is R after some L: a left
step returns to B and a right step is forbidden. An empty subtree has
exactly one external leaf, accepted in each of A,B,C, giving(1,1,1).
Partitioning the leaves at the root now gives
A(T)=B(left)+A(right), B(T)=B(left)+C(right), C(T)=B(left).
Thus A is the exact legal-gap count for every finite binary shape.

Every shape is realized by a classical2143 avoider. Give its root the
largest rank, give every left-subtree rank more than every right-subtree
rank, and repeat recursively. A selected occurrence crossing the two
subtrees has its first selected value above its last, contradicting the
2143 inequality. If the root is selected it must be the third (largest)
value; its first two entries are on the left and last on the right, giving
the same contradiction. An occurrence confined to a subtree is excluded
inductively. This establishes the domain of the proposed quotient test.

For the avoiding representatives4321 and4312, all five gaps are legal and
both contextual triples are(5,2,1). Their complete insertion-child triples
differ: gap2 yields(5,3,2) for4321 and(5,4,2) for4312. All other triples,
including multiplicities, are exactly those in the frozen certificate.
This refutes the stated same-size statistic lumpability. If lumpability
had held there would be only polynomially many coordinate states, since
each contextual count is at most n+1, but those state counts still would
not bound history weights. No growth implication is obtained from the
failed quotient or the still-correct automaton.

For the perfect seven-node tree write the entries a,x,b,r,c,y,d and suppose
b<a<d<c. Heap order gives x>a,b, y>c,d and r>x,y. If x<c, the consecutive
four entries x,b,r,c are boxed2143 because b<x<c<r. If x>c, the leaf
quadruple a,b,c,d is boxed2143: every other interior entry x,r,y exceeds c.
Distinct labels exhaust these two cases. The proof covers every assignment
of internal priorities, not merely odd/even ranks or a finite searched set.
Two leaves of either order have the perfect avoiding completions132 or231.
No claim of minimality over variable shapes is made.

Had all m=2^h leaf permutations had such perfect-tree avoiding completions,
choosing one standardized completion for each input would inject S_m into
the avoiders of length2m-1; the odd-position relative order decodes the
input. The factorial lower bound m! would force unbounded roots along that
subsequence, since (m!)^(1/(2m-1)) tends to infinity (already the last floor
m/2 factors give this elementary divergence). The four-leaf obstruction
rejects this particular sufficient mechanism. It does not reject variable
shapes, source Conjecture7.4, rank-joining population growth or target410.

## Independent exact controls

check_quinn_boundary_automaton.py imports no author implementation. It
reuses my independently checked nearest-greater parent construction,
obtains every shape through size7 from all labeled permutations, assigns
decreasing preorder ranks, and lists external paths with an explicit stack.
It tests the language by finding the first L and searching its suffix for
RR, unlike the author's mutable-state scan; all three contexts are counted
directly by prepending empty,L,LR words. An iterative evaluation also checks
the recurrences. New-maximum children are built as actual labeled words and
their shapes reconstructed, rather than using the author's recursive split.

All626 shapes through size7,4707 external paths and4707 actual insertion
children pass the language, context and geometric controls. The complete
collision multisets match the frozen certificate, and all smaller sizes0..3
have no such collision. All80 heap labelings of the perfect seven-node shape
are enumerated; the complete leaf2143 subset satisfies the stated two-case
certificate. These finite controls corroborate the preceding arbitrary-size
arguments and do not establish an asymptotic bound.
