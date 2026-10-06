# Exact maximum-Cartesian-tree dynamics

Quinn / literature-researcher-3, 2026-10-05. Author proof awaiting a different
researcher's full check. This is a partial structural lemma for target410. The
target remains the bounded-exponential decision for the entire boxed2143 class.
No novelty or growth conclusion is asserted here.

## Tree conventions and nearest-greater interpretation

For a permutation p, its maximum Cartesian tree T(p) is the ordered binary tree
whose inorder traversal visits positions0,...,n-1 and whose root is the position
of the maximum; the two subtrees are defined recursively on the prefix/suffix.
Every ancestor has greater value than its descendants. The tree state retains
only shape and inorder positions, not ranks. The empty shape is(), and a node
is the pair(left,right).

For a node j let L be its closest ancestor situated left of j and R its closest
ancestor situated right of j, when they exist. These are exactly the nearest
greater indices l(j) and r(j) in p. One precise proof is induction on the
recursive maximum decomposition: the subtree rooted at j is the maximal
consecutive interval containing j in which every other value is below p_j.
For the global root this is the whole permutation. For a node left of the
global root, its interval cannot cross the global root, and the assertion
follows by induction inside the left subpermutation; the right case is
symmetric. The immediately adjacent entries, if present, are therefore the
nearest greater ones. In the inorder traversal, the position immediately
preceding a subtree is its first ancestor on the left: climb left-child edges
until the first right-child edge. The position following a subtree is its first
ancestor on the right, by the symmetric traversal argument. This proves the
claimed interpretation.

If both L and R exist, the parent of j is the smaller-valued one of L,R.
Indeed, they lie on the ancestor path and the nearer ancestor is the parent;
the farther ancestor is greater by heap order. The parent is left of j exactly
when j is a right child. Thus the previously checked kernel's eligibility

    L exists, R exists, and p_L < p_R

is equivalent to: j is a right child and has an ancestor on its right. In this
case L is its parent and R is its first right ancestor. A right child always
has L, so only existence of R needs checking. A left child with both boundaries
has its right parent below its left ancestor and is not eligible. The root is
never eligible.

Consequently the full blocker triple list and the legal maximum gaps depend
only on T(p). For every eligible j, the zero-based forbidden gaps are

    j+1,...,R.

Their union is exactly the checked insertion kernel. This proves an arbitrary-n
shape criterion, rather than inferring one from finite equalities.

## Structural update

Let S(T,g)=(A,B) be the two maximum Cartesian shapes of the first g and the last
n-g inorder entries. This splitting operation is determined by shape:

* S((),0)=((),()).
* For T=(L,R), k=|L|, and g<=k, if S(L,g)=(A,D), then
  S(T,g)=(A,(D,R)).
* For g>k, if S(R,g-k-1)=(D,B), then S(T,g)=((L,D),B).

Proof by induction on tree size. If the cut is on the left of the root, the
root remains the maximum of the suffix, with the remainder D of its left
subtree and its entire right subtree. The prefix has shape A by induction.
The cut on the right is symmetric. Boundaries g=0,n and the empty input are
included. Therefore inserting a new global maximum at gap g has shape(A,B),
since its prefix and suffix are its left and right subtrees.

The legal-gap test and all child-state transitions are thus functions of T.
For avoiding parents this is an exact quotient of the full maximum-insertion
generating tree. With w_0(())=1 and all other initial weights0, define

    w_(n+1)(U) = sum_(T:|T|=n) w_n(T)
                 * #{g legal in T : S(T,g)=U}.

Then w_n(T) is exactly the number of boxed2143 avoiders with shape T, and
a_n=sum_T w_n(T). Induction uses the previously checked unique maximum-deletion
parent and unique gap of every child; no multiplicities are dropped. A gap's
position is the new root's inorder position, so different gaps of a fixed T
give different U, though multiple old states can contribute to one U.

## Counting limitation and finite checks

The number of shapes is Catalan and bounded by4^n. This does not bound w_n(T).
The permutations2143 and3142 have the same maximum shape ((.(..))(..)) in the
preorder notation used by tree_word, but only the former contains boxed2143.
The tree controls future maximum insertions, not current avoidance on arbitrary
heap labelings. Avoiding histories must retain their weights in the recurrence.
An exponential upper bound on all weights would solve the target; unbounded
root growth of some weights would solve it negatively. Neither is established.

tree_dynamics.py implements the shape criterion and split. Its finite replay
verify_tree_dynamics.py checks all5914 permutations of lengths0..7, every46233
maximum insertion, the exact blocker lists and gap sets, recursive prefix/suffix
shapes, and complete literal-definition avoidance counts. This confirms that
the implementation and the author's uniform argument agree on that scope.
It is not independent team review or an asymptotic proof. The first invocation
had an import-name error (literal_occurrences instead of direct_occurrences);
it was corrected before any successful output, preserving the original checker.

## Prior context

Cartesian-tree shape/heap encodings and splitting are standard. Sage's lane
uses fixed minimum/maximum-tree pairs and their known heap-poset fibers. This
lane uses the maximum tree as the exact state of the insertion dynamics; it
does not claim to invent Cartesian trees or count all heap labelings as avoiders.
The boxed-growth target and interval-restriction formulation are from Kitaev,
Qiu and Xu, arXiv2609.13764v1, Sections3 and7:
https://arxiv.org/html/2609.13764v1 . The source was refreshed live on2026-10-05;
its remaining2143/3412 orbit is still expressly unresolved. A small search on
boxed2143 with Cartesian/tree keywords found no identical claim, which is not
an absence or novelty certificate.

Next falsifiable obligation: propose and prove a uniform bound on these state
weights, or a construction producing superexponentially many legal histories.
Finite ratios and a Catalan state count do not meet either obligation.
