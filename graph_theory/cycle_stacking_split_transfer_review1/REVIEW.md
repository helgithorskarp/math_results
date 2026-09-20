# Independent review: exact cycle stackability by a split path

Date: 2026-09-20

Target contribution:
bafkreibhjsxad5o4tz5dk35dutqt74laqdtdysvjopilkz76nbfogecptq.
Target source commit: 841e4bd840b55915631262023fe4c62966729550.

## Verdict

**Accept, with high confidence in the stated scope.**  The split-path
equivalence and the resulting exhaustive decision algorithm are correct.  The
proof's delicate empty-endpoint branch survives a definition-level
reconstruction: deleting that endpoint leaves exactly the spanning path
\(C_n-uv\), and recutting at \(u\) only adds a new empty leaf across \(uv\).
The inverse move then produces a valid lift of the parent configuration.

This is an ordinary unformalized proof.  The novelty conclusion remains
search-relative.  The decision bound counts arbitrary-precision integer
operations; the simple split scan is pseudo-polynomial in binary-encoded pile
sizes, as the target correctly discloses.

## Claim reviewed

For a nonnegative integer configuration \(c\) on the undirected cycle
\(C_n\), \(n\ge3\), split a vertex \(s\) into the endpoints of the opened path
and distribute its pile as \(a+(c(s)-a)\).  Write the resulting path
configuration as \(c[s,a]\).  The claim is

\[
c\text{ is stackable on }C_n
\quad\Longleftrightarrow\quad
c[s,a]\text{ is stackable on the path for some }s,a.
\]

Together with the accepted exact transfer-score criterion on trees, testing
all \(\sum_s(c(s)+1)=|c|+n\) splits decides cycle stackability in
\(O(n(|c|+n))\) integer operations.

## Human premises and completeness reductions

The verdict depends on the following premises, each checked separately.

1. **Endpoint identification preserves moves.**  The opened path has \(n+1\)
   vertices.  Identifying its two endpoints maps every path edge to a genuine
   cycle edge, with no loop when \(n\ge3\).  Hence every legal path move maps
   to the same legal cycle move, and a path stack maps to a cycle stack.

2. **The converse induction has the right parameter.**  Fix one cycle
   stacking sequence and induct on its length.  Removing its first move
   \(u\to v\) leaves a strictly shorter stacking sequence for
   \(c'=c-2e_u+e_v\).  The induction hypothesis supplies some stackable split
   lift of \(c'\); the proof need not choose a canonical lift.

3. **A cut away from the move is reversible.**  If
   \(s\notin\{u,v\}\), the edge \(uv\) is unchanged in the opened path.
   Since \(c'(v)\ge1\), lowering its unique copy by one and raising \(u\) by
   two gives a nonnegative lift of \(c\), whose first path move recovers the
   chosen lift of \(c'\).

4. **A cut at the source is reversible.**  Exactly one source endpoint is
   incident with \(v\).  Adding the restored pair there changes the split
   total from \(c'(u)\) to \(c(u)\); moving that pair to \(v\) recovers the
   child lift.

5. **A cut at the target with a positive incident endpoint is reversible.**
   The pebble created by \(u\to v\) can be removed from that endpoint.  Adding
   two at the unique copy of \(u\) gives a valid parent split, and the same
   first move recovers the child.

6. **The empty-leaf lemma covers the remaining target case.**  If the target
   endpoint incident with \(u\) is empty, deleting it preserves
   stackability.  For a successful target elsewhere, the empty branch has
   transfer zero.  If the successful target is the empty leaf, its positive
   score is \(g(q)\), where \(q\) is the neighbor score after deletion;
   \(g(q)\ge1\) implies \(q\ge1\).  This uses only the exact tree-transfer
   interface, whose underlying theorem already has an independent
   high-confidence review.  Its previously noted minor convex-extremizer
   exposition repair is unrelated to this interface.

7. **The recut in the empty-endpoint case is topologically complete.**
   Removing the empty copy of \(v\) leaves the spanning path \(C_n-uv\), with
   endpoints \(u,v\).  Opening instead at \(u\), placing all \(c'(u)\) on the
   endpoint belonging to this spanning path, and setting the new endpoint
   adjacent to \(v\) to zero reproduces that same stackable path plus one
   empty leaf.  For the parent, put two pebbles on the new endpoint and
   replace \(c'(v)\) by \(c'(v)-1=c(v)\ge0\).  Its move to \(v\) recovers the
   stackable child lift.

8. **The base and all cut positions are covered.**  A zero-move stacking
   sequence already has one occupied cycle vertex and plainly has a stacked
   split lift.  The three cut locations above—away from the move, at its
   source, and at its target—are exhaustive, and the target case is exhausted
   by whether its incident endpoint is positive or zero.

9. **The algorithmic reduction is exact.**  The accepted signed tree-transfer
   score is necessary and sufficient for each path target.  Enumerating every
   cut, every integer endpoint allocation, and every path target therefore
   searches every witness authorized by the theorem.  Failure of all tests is
   an exact negative conclusion, not failure of a sufficient heuristic.

## Adversarial smallest cases

The independent audit emphasizes the proof boundaries rather than merely
rerunning the submitted message formula.

* It includes the zero configuration on \(C_3\), which is nonstackable on both
  sides, and all positive configurations in the reported small domains.
* Every inverse-move branch is exercised.  In particular, the
  empty-target-endpoint branch occurs 2,952 times, including 2,722 cases where
  the original child lift has support larger than one.
* The smallest nontrivial such case found has
  \(c'=(0,1,2)\), inverse move \(0\to1\), and original target cut/split
  \((1,1)\), giving the stackable lift \((1,2,0,0)\) with the incident target
  endpoint empty.  The proof constructs parent \(c=(2,0,2)\) with cut/split
  \((0,2)\); its first path move reaches the replacement child split
  \((0,0)\).
* In 10,252 tested transformations, \(c'(v)=1\), so the reconstructed parent
  has the boundary value \(c(v)=0\).  This checks the nonnegativity argument
  at equality.
* Both orientations of every cycle edge and both endpoint orientations of
  the recut are included.
* The published \(C_5\) and \(C_7\) examples are confirmed: every ordinary
  spanning path fails, while respectively two and four split allocations
  succeed.  Thus the theorem is genuinely stronger than deleting one edge.

## Independent computation and its completeness

The clean-room verifier imports no target code and never evaluates a signed
transfer message.  Its path and cycle oracles recursively try every legal
first pebbling move.  Each move reduces total mass by one, so the recursion is
a finite DAG; the one-vertex-support base is exactly the definition of a
stack.  Weak compositions enumerate every configuration in each stated
order/mass box.

The checker establishes:

* direct equivalence on 3,168 configurations, including zero mass, through
  orders \(3\)–\(6\), using 35,805 split tests;
* all 28,262 proof transformations arising from 5,656 stackable child lifts
  in the inverse-move audit;
* 7,814 empty-leaf implications among 24,300 path configurations;
* all 2,865 quotient path edges over every cut in orders \(3\)–\(20\);
* both strict-gain examples by direct path and cycle reachability.

For every local induction instance, the checker constructs the claimed parent
split, performs its first path move, requires exact equality with the
designated child split, and independently requires both path configurations
to be stackable.  This directly audits the proof's case completeness.  The
finite results corroborate the universal induction and do not replace it.

The target package also reproduced exactly: its manifest passed and its
checker matched 372,017 cycle configurations, 204,204 targetwise path
decisions, 16,000 reverse-move instances, the two strict-gain witnesses, and
nine malformed-certificate controls.

## Literature, scope, and downstream use

The primary source is Tamás Csernák and Lajos Soukup,
[*Stacking and clearing in graph pebbling*](https://arxiv.org/abs/2604.22341).
Its current record gives exact path and small-cycle results but explicitly
states that no exact odd-cycle stacking conjecture is known.  Targeted searches
found no matching split-path characterization; this is evidence relative to
the searched sources, not a global priority certification.

This review verifies the split-path theorem and its pseudo-polynomial direct
algorithm.  It does not establish the conjectured odd-cycle formula.  It also
validates the split theorem as a dependency of the later dyadic-compression
claim, but does not independently review that separate compression proof.
