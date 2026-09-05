# Point 613: closure through 507 and a restricted 508-vertex residual

Let V={0,...,508} be the original Parts points, P={509,...,584} its 76
first-level completion points with at least seven neighbours in V, and
A7=UD(V union P). Put q=613=(-5/6,sqrt(11)/6) and H=UD(V union P union {q}).

**Every subgraph of H with at most 507 vertices is four-colourable.**
H has 586 vertices and 3,089 exact unit edges. Its minimum five-chromatic
subgraph order is either 508 or 509. Any non-four-colourable subgraph J on
at most 508 vertices must satisfy all of these necessary conditions:

- J has exactly 508 vertices and contains q and the 451 forced originals F.
- It omits originals 13, 24, 129 and pool point 518.
- It contains 27, 75, 114, 125, 127, 184, 525, 545, 580 in addition to F.
- It uses at least seven points of P, hence at least eight additions to V
  and at least nine original deletions.
- Its 56 free vertices satisfy the published 335-row hitting selector.

**The 508-vertex case remains open.** One bounded Kissat query on the new
6,176-variable, 24,317-clause formula returned UNKNOWN at 300 seconds.
No satisfying assignment or complete negative certificate was obtained.
No record graph is claimed.

## Proof

The [fixed-library certificate](../hadwiger_nelson_parts509_degree6_lift_family/README.md)
supplies proper four-colourings of H minus each member of F and of H minus
D for all 337 inclusion-minimal killing sets except

    A=D245={129,518}, B=D316={13,24}.

Here R=(V union P) minus F has size 134. The
[degree-seven hitting bound](../hadwiger_nelson_parts509_degree_pool_minimum/README.md)
says that every Y subset R meeting all 337 sets and containing at least
four points of P has size at least 58. The old A7 closure and the reviewed
zero-through-three-addition closures are imported facts. The hitting bound
was freshly regenerated and VeriPB-checked in the
[independent point-610 review](../hadwiger_nelson_parts509_degree7_extension610_closure_review1/README.md).
Its OPB hash matches the input regenerated here. That review does not
review this new point-613 argument.

Suppose J is a non-four-colourable subgraph of H of order at most 508.
If q were absent, the old A7 closure would colour J. Every member of F is
present, by the lifted deletion witnesses. Therefore

    X=V(J) minus (F union {q}) subset R, |X|<=56.

X meets every killing set except possibly A and B. The earlier
small-augmentation closures imply |X intersect P|>=3.

If X meets B, add pool point 518. This repairs A too; if 518 was already
present and only three pool points were selected, add any unused pool
point instead. At most one point was added. The result meets all killing
sets, has at least four pool points and has size at most 57, a contradiction.
Thus X omits both 13 and 24.

Five retained killing rows now require selection from these pool groups:

| Row | Group after omitting 13 and 24 |
|---|---|
| 260 | {515,564} |
| 285 | {525} |
| 303 | {522,539,547} |
| 377 | {510,529,543} |
| 394 | {524,555,572} |

They are nonempty and pairwise disjoint, so X has at least five pool points.
If X met A, adding original 13 would repair B with no quota problem, again
contradicting the bound 58. Thus X also omits 129 and 518.

Adding 13 and 518 repairs both missing constraints. If |X|<=55, the result
would have size at most 57 and satisfy the old bound's hypotheses.
Consequently |X|=56 and |J|=508, proving closure through 507.

After the four omissions, rows 126 and 252 additionally require singleton
pool groups {545} and {580}. These are disjoint from each other and the
preceding five groups. Thus X has at least seven pool points. With q this
requires at least eight additions, and order 508 then requires at least
nine original deletions. The nine additional forced vertices in the
theorem are exactly the singleton rows left in the 335 witnessed minimal
constraints after the four omissions.

V lies in H and is five-chromatic, giving the upper bound 509. The verifier
also extends one checked four-colouring of a vertex deletion of H by
assigning a fifth colour to the removed vertex, directly five-colouring H.

A possible 508-vertex obstruction is vertex-critical: deleting any vertex
leaves order 507 and hence a four-colourable graph. In particular it has
minimum degree at least four. These degree conditions are not encoded in
the current selector; no such next formula was generated or queried.

## Encoding and verification

One Boolean selector x_v is assigned to each v in sorted R. For each
minimal killing row other than 245 and 316 require at least one selector.
Fix x_13=x_24=x_129=x_518=0 and require sum(x_v)<=56. The pool requirements
above follow from these clauses. No symmetry restriction is imposed.

The cardinality encoding uses exact prefix thresholds z_(i,j), meaning at
least j of the first i selectors. Their recurrence is

    z_(i,j) iff z_(i-1,j) OR (x_i AND z_(i-1,j-1)).

Each equivalence uses four clauses with Boolean constants simplified; the
final threshold for 57 is false. Existentially quantifying the threshold
variables gives exactly the stated finite hitting selector. A graph
counterexample supplies such an assignment. The reverse implication from
a satisfying selector to non-four-colourability is not claimed.

The standard-library verifier reconstructs exact coordinates and all edges,
replays 451 forced and 335 killing witnesses on H, verifies the disjoint
groups, and rebuilds the canonical formula. It checks 2,410,698 retained
edges in the four-colour witnesses and 3,089 in the full five-colouring.
No new colourings are required: the pinned older witnesses and the prior
42-row extra catalogue suffice.

From this directory in a full checkout, use Python 3.11 or later:

    python3 verify.py
    python3 controls.py
    sha256sum -c SHA256SUMS

Expected output includes closure_through507=true, possible_counterexample_order=508,
minimum_old_pool_points=7 and residual_sha256 equal to
ec62944dd2b05b7b847038ff4f0f7ccd0fb9e470f6d670423c5ac39f0c90a948.
Controls enumerate 2,206 valid repair cases, including 1,422 in which the
designated pool point is already present. A negative control shows why
two disjoint missing rows can need two additions.

To regenerate the bounded pilot in a fresh external directory, use Kissat
4.0.4, source commit 8af8e56f174b778aef3aa45af9f739b2a5f492c2:

    python3 run.py --work /scratch/fresh-point613-pilot --kissat /path/to/kissat

This uses one worker, a 300-second native time limit and a 4 GiB address-space
limit on Linux. The measured run returned UNKNOWN after 300.012 seconds
with 32,336 KiB peak child RSS. Its 275,035,491-byte partial DRAT trace is
not a certificate and remains local. The formula, verbose log and partial
trace are reproducible local outputs. Timing and trace bytes can vary.
No checker is invoked on an incomplete trace.

The imported hitting theorem, small-augmentation closures and original
Parts five-chromaticity remain explicit premises. New verification uses
integer arithmetic in Q(sqrt(3),sqrt(5),sqrt(11)), denominator 288, ordinary
Python code and the proof above. This is not a proof-assistant
formalization or a new external review.

The bounded pilot is complete. Extending this unchanged SAT configuration
is not the recommended continuation. A new structural inequality, such as
a useful consequence of vertex-criticality, would be needed to justify
another formula. The teammate's newest dense506 one-arbitrary-point/two-
completion-point theorem concerns a different support and does not resolve
this residual.
