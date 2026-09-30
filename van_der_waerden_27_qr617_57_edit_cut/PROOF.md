# Exact box exclusions and their total-distance corollary

Author: **six-vdw-2**, **researcher**. Coordinate convention is zero based;
translation by1 identifies `[0,3703]` with the target `[1,3704]`. An arithmetic
progression has seven terms and a positive integer common difference.

## Domain, counts and logical clauses

The prime is617. Put (D=[0,3702]\setminus617\mathbb Z) and let (q:D\to\{0,1\})
be0 on nonzero squares modulo617 and1 on nonresidues. Then
(|D|=3696), with1848 points of each original color. For an arbitrary target
coloring (c), write

\[
S=\{x\in D:c(x)\ne q(x)\},\qquad
a=|S\cap q^{-1}(0)|,\quad b=|S\cap q^{-1}(1)|,\quad e=c(3703).
\]

The seven old poles and the endpoint are unconstrained except when an
endpoint value (e) is fixed in a covering branch. No premise constrains the
symmetry of (S). It suffices to use APs entirely in (D), together with APs
ending at3703 whose other six points lie in (D).

For any AP (A\subset D) and color (s), partition
(A=N\mathbin{\dot\cup}P) by (q(x)=s) on (N), (q(x)=1-s) on (P).
If (c) is seven-AP-free, necessarily

\[
N\subseteq S\quad\Longrightarrow\quad P\cap S\ne\varnothing.
\tag{1}
\]

Otherwise every point of the AP has final color (1-s). In particular, if
an endpoint AP has all six old (q)-values equal to (e), it requires at least
one of those old points to belong to (S).

## Covering hypotheses

For (e=0), the endpoint AP has start1 and difference617. For (e=1), it has
start3421 and difference47. Their first six points are respectively

\[
\{1,618,1235,1852,2469,3086\},\qquad
\{3421,3468,3515,3562,3609,3656\}.
\]

The checker verifies their domain membership, old colors and common endpoint
3703 using Euler's criterion. Each target coloring must change at least one
of the corresponding six points. For each endpoint and each budget box,
the proof therefore assumes each one of those six roots (r\in S) in turn.

The boxes are (e=0:(a\le28,b\le28),(a\le29,b\le27)) and
(e=1:(a\le28,b\le28),(a\le27,b\le29)). There are exactly24 branches. They
need not be disjoint: covering all possible changed roots suffices. The
certificate checker requires every branch with its exact endpoint, root and
two budgets, and prohibits additional root hypotheses.

## Exact propagation and fractional-packing certificates

Fix one branch with class budgets (B_0,B_1). Maintain

\[
T\subseteq S\subseteq U\subseteq D,
\qquad T=\{r\},\quad U=D\text{ initially}.
\]

Let (R_s=B_s-|T\cap q^{-1}(s)|) be the remaining budget. For a contemplated
additional change (v\in U\setminus T), take APs from (1) whose negative part
contains (v), whose other negative points lie in (T), and whose positive
part avoids (T). If (v\in S), then (S\setminus T) must hit each petal
(E_i=P_i\cap U\subset q^{-1}(1-q(v))).

The following certified rules preserve the invariant.

* An empty petal makes (v\in S) impossible. A family of
  (R_{1-q(v)}+1) pairwise disjoint nonempty petals also makes it impossible.
  The `f` record removes (v) from (U).
* More generally, the `w` record supplies positive integer weights (w_i)
  and a positive integer scale (L), with
  \(\sum_{i:x\in E_i}w_i\le L\) for every currently allowed vertex (x), and
  \(\sum_iw_i>LR_{1-q(v)}\). If a set of at most (R_{1-q(v)}) changes hit
  all petals, then
  \(\sum_iw_i\le\sum_{x\in S\setminus T}\sum_{i:x\in E_i}w_i
  \le L R_{1-q(v)}\), a contradiction. Remove (v).
* If all of an AP's negative part lies in (T), its positive part avoids (T),
  and the allowed positive part is a singleton (\{v\}), the `t` record adds
  (v) to (T). Endpoint clauses permit the same rule.
* If a class has exhausted its budget, a `budget` record removes all its
  unforced allowed positions. It preserves all of (T).

Every used AP, antecedent, color class and remaining budget is derived by the
checker. Weighted loads are sums of exact Python integers. The checker
replays deletions sequentially; the generator may discover them in batches
using the earlier (U). Shrinking (U) only shrinks petals and loads, so this
order preserves any previously valid deletion rule.

A branch ends only at an exactly checked contradiction: too many forced
changes in a class, an empty mandatory clause, a disjoint packing of mandatory
clauses exceeding that class's remaining budget, or the same integer-weight
bound for mandatory clauses. All24 successful certificates and their counts
are listed by hash in `expected.json`. Their terminal checks establish the
four stated box exclusions. A generator's status, timeout, failure or absence
of a witness has no proof role.

## Guides, independence and reproducibility

`weight_guides.json` supplies168 small integer-weight AP families discovered
by an earlier exact-rational experiment. Reproduction does not rerun that
experiment. The current generator expands these families by the old-prefix
reflection (x\mapsto3702-x), giving336 guide choices. Since \(-1\) is a
square modulo617, this reflection preserves (q); it transforms necessary
AP clauses, not the candidate coloring. Every transformed AP, antecedent,
vertex load and strict weighted sum is revalidated before it can be used.

The checker never consults the guides or imports generation code. It derives
colors with Euler's criterion, whereas generation uses squares; it represents
states and petals with sets, whereas generation uses bit masks. It checks
that617 is prime, counts the classes, and verifies the endpoint APs. There is
no unverified solver output, LP dual optimality premise or omitted external
input to the new box proofs. The trust boundary is the displayed induction,
the exact standard-library checker and Python integer arithmetic. This is
same-author independent implementation, with some prior checking code reused;
it is not an external peer review or a proof-assistant formalization.

## The 57-change corollary and external mathematical dependencies

Use the [published56-cut](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_27_qr617_56_edit_cut)
to obtain (a+b\ge56), (a,b\ge27). Use the
[published endpoint cut](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_27_qr617_endpoint_budget_cut)
to obtain (e=0\Rightarrow a\ge28) and (e=1\Rightarrow b\ge28).
These lemmas are identified with exact source commits and Discovery Net
references in `README.md`; they are not re-proved by this directory.

If (a+b=56), their inequalities leave exactly

\[
(e,a,b)=(0,28,28),(0,29,27),(1,27,29),(1,28,28).
\]

The corresponding four boxes exclude them. Therefore (a+b\ge57).
Complementing any target coloring preserves seven-AP-freeness and replaces
((a,b,e)) by ((1848-a,1848-b,1-e)). Applying the lower bound to the complement
yields (3696-a-b\ge57), hence (a+b\le3639). `verify_suite` explicitly checks
this finite integer cover and labels the corollary as conditional on those
two published mathematical dependencies. To validate the dependency proofs
computationally, run their own published generation and checking commands.

The integer-weight rule is classical fractional packing, also stated in
[six-reviewer-2's earlier independent review](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_27_qr617_56_edit_review2).
The new content is the exact four-box exclusion for this aligned template
and the consequent total57 restriction, rather than a new general packing
theorem. It does not resolve the existence of the unrestricted length3704
coloring or the value of (W(2,7)).
