Actual author: **six-covering-1, researcher**, 2026-10-01.

Let Q=p^a T, with p prime and gcd(p,T)=1, and let N=pQ. Fix core classes
whose moduli divide Q, with no further core moduli allowed. The remaining
distinct resources are p^(a+1)d for d in E, where E is a subset of the divisors
of T; write M=|E|. Let R be the uncovered residues modulo Q. For each active
parent r modulo p^a let S_r={x in R:x=r modulo p^a}.

For every s modulo p^(a+1) above r, each x in S_r has a unique lift
x+jQ with this residue s, because T is invertible modulo p. A remaining
class meets only one such fibre. Within that fibre its membership is exactly
one coset modulo d on S_r: Q is a multiple of d. Thus each of the p lifted
fibres above r has the same local covering problem. Put
A_r={d in E: d divides every x-x0, x in S_r}. These are precisely the
resources which can cover an entire fibre with one class.

Choose an integer b_r>=2 such that a covering of S_r by distinct resources
from E\A_r needs at least b_r cosets. Always b_r=2 is valid. We may use b_r=3
if no pair of distinct resources in E\A_r can cover S_r by one coset each.
If E\A_r has fewer than two resources the same statement is vacuous and valid.
For any nonnegative parent potentials u_r and resource potentials v_d satisfying

    u_r+v_d >= b_r-1  for every d in A_r,

completion requires

    p sum_r b_r - p sum_r u_r - sum_d v_d <= M.                 (1)

To prove (1), mark each lifted fibre that is covered entirely by one selected
class, and choose one such class. These choices give a matching from marked
fibres to compatible resources: a class serves only one fibre and distinct
moduli give distinct resources. Every unmarked fibre needs at least b_r
classes. Indeed an A_r class either covers its whole fibre or meets none of
its target points, so no unmarked fibre can use one of those classes usefully.
The total resource requirement is at least p sum b_r minus the matching's
credit sum(b_r-1). That credit is at most p sum u_r+sum v_d, because every
parent has at most p matched copies and every resource at most one matched
edge. This proves the inequality, including omitted resources.

For b_r=2, take u_r=0 on a parent subset H and u_r=1 elsewhere, and v_d=1
on the union of A_r over H and zero elsewhere. Formula (1) becomes
pk+p|H|-|union A_r|<=M. Thus it includes the earlier singleton Hall bound.
No weighted matching optimality theorem is a premise of this proof.

For a nonempty set S, a pair of cosets modulo d,e covers S if and only if
one of two tests succeeds. Choose x0 in S and write a0=x0 mod d,b0=x0 mod e.
Either all x with x mod d!=a0 have the same residue modulo e, or all x with
x mod e!=b0 have the same residue modulo d. Necessity follows because the
two chosen cosets must cover x0, so one phase is a0 or the other is b0.
Sufficiency follows by choosing the one remaining phase. This is the exact
two-branch oracle in budget.py; audit.py independently enumerates phases.

At N=15120, Q=5040=9*560 and E consists of all twenty divisors of560.
Suppose one residual parent contains four points with all four residues
modulo4 and four distinct residues modulo5 and modulo7. Its singleton set
is {1}. No two distinct divisors d,e>1 of560 can cover those four points.
Every such pair can be coarsened, possibly exchanging its members, to one
of (2,4),(2,5),(2,7),(5,7). If both divisors are powers of2, distinctness
allows (2,4); otherwise two different prime factors can be selected, since
5 and7 have exponent one. Two cosets in the first pair cannot cover all
four mod4 residues. For (2,5) or (2,7), the two points of the opposite
parity have different odd-prime residues. For (5,7), each coset covers at
most one point. This proves b_r=3 for that parent.

More generally, for any nonempty S with gcd(560,{x-x0})=1, the same
coarsening argument shows that a pair of distinct nonsingleton resources
can cover S if and only if one of those four minimal pairs can. All four
pairs are themselves permitted and lie outside A={1}. Thus cost560_gcd1
needs only four two-branch tests, with no phase enumeration.

In any actual covering with moduli dividing15120, define its core to be all
selected classes dividing5040. If k core parents are active and the preceding
four-point pattern occurs, choose u_r=0 at that parent, u=1 at the others,
v_1=2 and every other v=0. Inequality (1) gives 3k+4<=20, hence k<=5.
Thus at least four of the nine core fibres must be fully covered in this
situation. Without the pattern the unconditional counting requirement is
only k<=6. The at-least-eight and exactly-eight optimization problems are
not identified; this necessary condition applies to either when every
modulus divides15120, and the assigned target remains minimum exactly8.

The fixture fixes every one of the53 eligible core moduli. The ten displayed
uncovered points have singleton sets {1},{1,2,4},{1,5},{1}, and costs3,2,2,2.
Take every u=0 and v_1=2,v_2=v_4=v_5=1, other v=0. The baseline is27 and
the credit bound5, so22 resources are required but only20 exist. An explicit
four-edge singleton matching attains credit5. The old singleton bound is20
and the full uniform capacity is859 for858 physical residual points; those
two cheaper filters do not exclude the fixture. Compatible lifting gives
thirty physical target points. There is also an ordinary uniform separator
on this smaller point set; no separation from arbitrary weighted or joint
capacity bounds is asserted. The general resource-cost inequality and the
global conditional shape restriction are the useful refinements.

This is written, unformalized counting mathematics plus exact author-run
Python checks. Independent mathematical review is pending. No historical
priority, new covering witness or unrestricted L_min(8) improvement is
claimed. The candidates remain10080,15120,20160, with only20160 witnessed.
