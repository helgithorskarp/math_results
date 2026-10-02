# Actual preparation words have length at most six

Actual author: **six-reviewer-5**, independent mathematical reviewer.
This is a derivative result for the literal P27 and the zero-prior-LOW
branch of committed LEMMA9661, not a result for arbitrary thirteen-input
sorting networks. The defining proof, prefix and counts were visible.
The reconstruction below was completed before target executable or
certificate access. No historical-priority or blinded-review claim.

Let D=(5,6,7,9,10), in increasing physical order. A function f maps every
five-bit input to its complete five-bit output. Bits are indexed0..4.
For a row y define

\[
I(y)=\sum_{0\le i<j<5}[y_i=1,y_j=0],\qquad
\Phi(f)=\sum_{x\in\{0,1\}^5} I(f(x)).
\]

For a standard comparison (a,b), a<b, let T be the set of input rows on
which its operands are1,0. Swapping those two bits decreases I by b-a:
the endpoint pair removes one inversion; each intermediate bit removes
one further inversion, regardless of whether it is0 or1. Therefore

\[
\Phi(f)-\Phi(C_{a,b}\circ f)=|T|(b-a).
\]

Every preparation gate in the stated branch is active on every one of
the ninety tight whole original cubes. In particular T is nonempty.
The identity function has potential80, so the full-function graph is
acyclic; even the unpruned activity graph admits no word longer than80.
This elementary upper bound is a consequence, not a supplied search limit.
It concerns five-port standard comparison functions with the stated
activity condition. It does not bound arbitrary words with identity gates.

The independent complete pruned graph has374 functions,446 edges and193
certified exits. We reconstruct all ten transitions at each retained
function using the target's written cut predicates. A later comparison
with the native certificate is reported separately from this initial seal.
Their obstruction uses original HH(0,1) or HH(8,9), D=9,R=0, and a
conditional free maximum at physical10 on the entire original cube.
Every edge is checked against all nine activity images. Thus prepending
any exit-avoiding actual preparation to P preserves the tight D/R record
of each domain. The first future marked touch or first future touch of10
forces at least45 total comparisons; the specified full-input wrong-rank
witness cannot be repaired. This excludes these exits directly for every
actual preparation word, without first replacing it by a shorter word.
Alternatively, the target's shortest-function replacement proof applies.

Let d(f) be the BFS shortest distance in this pruned graph. Inverting the
strict potential order also permits longest-path dynamic programming.
For every one of374 functions the longest and shortest distances agree.
Independently checking all446 edges gives exactly

\[
d(g)=d(f)+1 \quad\text{for every retained-source edge }f\longrightarrow g.
\]

Consequently **every admissible path that avoids exits has length d(f)**,
not merely a shortest representative of that length. The complete retained
census, by distance, is:

| Distance |0|1|2|3|4|5|6|
|---|---:|---:|---:|---:|---:|---:|---:|
| Retained functions |1|5|16|36|57|51|15|

There are181 retained functions and no retained function at distance7.
All fourteen distance-seven functions are exits. The maximum distance
seven quoted by the original proof is correct for the complete374-state
cover; the original at-most-seven replacement statement is valid but loose.

**Refined theorem.** Every size-at-most44 standard sorting completion of
the literal P27 whose first strict LOW increase is a singleton preceded
by zero LOW binary merges has at most **six actual preparation gates**
before that singleton. The full function of its preparation is one of
the181 retained functions; any other admissible representative avoiding
exits has the same length. No depth bound is assumed as an input.

The bound six is attained in the necessary graph by fifteen functions;
that does not assert any such function extends to a44-comparator sorter.
The first singleton still has fifteen possible heads: one of LOW3/4/8
paired with one of the five dead ports. This refinement does not exclude
those heads or their tails. It leaves the one/two prior LOW-merge cases,
the full HIGH3 target, the H21 target and the global endpoint open.

An additional independent scan permits free-maximum cuts from all72 tight
original domains whose maximum free physical port is10. It produces the
same entire graph and the same193 exits; it gives no smaller necessary cover.
Its failure to find more cuts is not a feasibility assertion.

The proof imports S(11)>=35,S(12)>=39 and the ordinary pruning /
size-preserving standardization interface. The actual-maximum cut induction,
threshold lifting, completeness of the algorithms and their correspondence
to this statement remain ordinary unformalized mathematics. Exact finite
checks corroborate these bridges; they do not make them machine-checked.
