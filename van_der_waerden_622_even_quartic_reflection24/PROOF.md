# Reflection-paired quartic obstruction: 24 field edits and264 template coordinates

Author: **six-vdw-1**, role **researcher**. Exact computer-assisted lemma,
with separate same-author verification; no external review or formalization.

Let F=F311. For a polynomial P of the form

    P(x)=alpha*((x-v)^4+A*(x-v)^2+B),
    alpha in F*, v,A,B in F,

let phi:F->{0,1} be1 where P is a nonzero square and0 where P is a nonsquare.
Each root value of phi is arbitrary, independently of every other root.
Define c_phi(t+1)=(t mod2) XOR phi(t mod311). This has period622 and
c_phi(t+312)=1-c_phi(t+1). Alpha is nonzero, so P is a nonzero quartic.

**Lemma.** Every such c_phi has24 monochromatic nonconstant seven-term
integer APs in[1,2171] with pairwise disjoint field-residue supports and no
root of P in any support. Thus:

1. Recoloring roots alone cannot make the seed AP-free.
2. If an arbitrary psi:F->{0,1} has c_psi AP-free on[1,2171], then psi differs
   from phi at at least24 nonroot residues.
3. If c_psi is AP-free on[1,3704], it differs from c_phi at at least264
   binary coordinates in nonroot columns of that interval.
4. An arbitrary AP-free binary coloring of[1,2171], with no template
   restriction, differs from c_phi at at least24 nonroot coordinates.

These are lower bounds, without optimality or attainment claims. The264
statement requires the period622/anti-period311 lift. This lemma gives no
new W(2,7) bound and does not exclude arbitrary3704-point colorings, arbitrary
quartics, or arbitrary311-bit template words.

## 1. The exact polynomial family

For a general quartic alpha*x^4+beta*x^3+gamma*x^2+delta*x+epsilon, alpha!=0,
the unique translation canceling its cubic coefficient is v=-beta/(4*alpha).
The coefficient of y in P(y+v) is

    L=4*alpha*v^3+3*beta*v^2+2*gamma*v+delta.

The family of this lemma is precisely L=0. Expanding then gives

    P(y+v)=alpha*(y^4+A*y^2+B),
    A=(6*alpha*v^2+3*beta*v+gamma)/alpha, B=P(v)/alpha.

No assertion is made when L!=0. Multiplicities and splitting patterns of the
included quartics are unrestricted. The proof does not enumerate all raw
polynomial coefficients or all root-bit assignments.

## 2. All included quartics reduce to625 sufficient cases

Multiplying a polynomial by a nonzero field scalar preserves or complements
all character bits away from its roots. Field substitution y=u*z gives

    y^4+A*y^2+B = u^4*(z^4+(A/u^2)*z^2+B/u^4).

The square map on F* has image size155, and11 is a nonsquare. The fourth-power
map has the same image: in the cyclic group of order310, gcd(4,310)=2, so its
image is precisely the nonzero squares.

If A!=0, choose u with A/u^2 equal to1 or11 according to the square class of A.
The transformed constant can be any field element. This yields622 cases:

    Q(z)=z^4+z^2+b, b=0,...,310;
    Q(z)=z^4+11*z^2+b, b=0,...,310.

If A=0 and B!=0, choose u with B/u^4 equal to1 or11, again according to its
square class. If A=B=0 use u=1. These yield three more cases:

    Q(z)=z^4, z^4+1, z^4+11.

The total is3+622=625. They are sufficient coefficient cases, not distinct
or minimal affine orbits. The scalar alpha*u^4 is harmless up to one global
complement. Roots transport bijectively under x=u*z+v. Since all certificate
APs avoid roots, every independent root assignment is covered at once.

The order in packings.json is the three pure quartics, then the311 quadratic-
coefficient1 cases, then the311 coefficient11 cases. Each polynomial is stored
in ascending coefficient order. The checker derives this whole mandatory
cohort independently and rejects omitted, duplicated, substituted or extra
cases and added hypotheses.

## 3. Affine field transport gives actual short integer APs

For any u!=0 and v in F, choose the unique odd residue M modulo622 with M=u
modulo311 and the unique even residue V with V=v modulo311. M is a unit.
If phi(u*z+v)=theta(z) XOR e on the used nonroots, then

    c_phi(M*t+V+1)=c_theta(t+1) XOR e

modulo the period. Thus a cyclic AP(a,d) maps to(M*a+V,M*d), and its field
support maps bijectively by z->u*z+v. Monochromaticity, disjointness and
absence of polynomial roots are preserved.

The difference is nonzero modulo311. Take its positive representative
D in{1,...,621}, excluding311. If D>311, reverse the seven terms and use
622-D instead, giving a difference in{1,...,310}. Reduce the start modulo622.
If it is at least311, subtract311. This complements every color while
preserving all field residues. The result is therefore an actual integer AP

    a+1, a+1+D, ..., a+1+6D,
    0<=a<=310, 1<=D<=310,

whose last position is at most2171. This process preserves each field support.
Consequently24 canonical field-disjoint root-free obstructions yield24 such
obstructions for every original included quartic and every root assignment.

## 4. Reflection pairs and a seven-uniform matching problem

For each canonical even Q, its character satisfies phi(-x)=phi(x) at every
nonroot. On zero-based coordinates, parity is also unchanged by t->-t
modulo622. Hence c_Q(-t+1)=c_Q(t+1) at those coordinates.

A root-free monochromatic AP with zero-based start a and positive difference d
has a reflected and reversed AP with the same d and start

    a_ref = -(a+6*d) modulo622.

If this start is at least311, subtract311. The subtraction complements all
seven colors and preserves its field support, so monochromaticity remains.
Its support is exactly -R, where R is the original field support. If R avoids0
and R intersects -R trivially, these two APs have14 different field residues.

The310 nonzero field residues form155 orbits {x,-x}. An eligible AP pair uses
seven different orbits. Two such pairs have disjoint field supports exactly
when their seven-orbit sets are disjoint. Thus12 disjoint edges in this
seven-uniform hypergraph supply24 disjoint actual APs. Reflection is a proposal
mechanism; the independent checker evaluates both explicit APs rather than
assuming this identity.

The builder scans every canonical zero-based start a=0,...,310 and difference
d=1,...,310 (96,410 choices) for the selected Q. It rejects roots, zero,
non-monochromaticity, and repeated or negative-colliding field residues.
It retains one explicit representative of each eligible seven-orbit edge.
Duplicate edges are interchangeable for this particular matching question.
This enumerates the stated reflection-paired class, not all possible unpaired
AP packings or all binary colorings.

A greedy proposer is tried first. If it finds fewer than12 pairs, one capped
SAT query seeks12 disjoint edges. There is one selection variable per edge.
At-most-one per orbit uses Sinz-style sequential prefix clauses. A truncated
prefix threshold encodes at least12 selections. For its prefix variable z(i,j),
with p=z(i-1,j), q=z(i-1,j-1) and x the current edge variable, the exact recurrence

    z(i,j) <=> p OR (x AND q)

uses clauses (-p OR z), (-x OR -q OR z), (-z OR p OR x),
and (-z OR p OR q), with constant boundary values simplified. The final
threshold12 is required. The returned assignment is checked against every
CNF clause and the decoded edges are checked for disjointness before producing
explicit AP proposals. Unchecked UNSAT, UNKNOWN, timeout, an over-cap encoding
or a missing greedy packing stops the run and proves no mathematical exclusion.
The proof below uses only the successful exact AP certificates, so it does
not rely on solver correctness or completeness of this search encoding.

## 5. Compact certificates and independent checks

packings.json contains625 mandatory cases, each with12 pairs of two explicitly
stored [one-based start,positive difference] APs. It is179,102 bytes. Its SHA256 is

    74c7fc5307762c76b5f11001cdd1d876edb1b68ae47bac6a30ac8f44a83cce88

The standard-library checker derives the exact canonical coefficients and
ordered625-case coverage independently. For every actual integer term it
uses Horner evaluation modulo311, rejects roots, evaluates the character by
Euler's criterion, and computes its parity-XOR color. It checks seven distinct
residues and monochromaticity in each AP, disjointness across all24 APs, and
that the two APs of each pair have equal differences and opposite field
supports. It imports no proposer, reflection formula, solver, or numeric
library. All substantive checks use explicit exceptions and survive -O.

Each full check verifies15,000 actual APs and105,000 term colors, using168
nonroot residues per case. The largest supplied canonical position is2167;
the general affine transport in section3 gives the bound2171. Every arbitrary
root-bit assignment is covered simultaneously because all used residues are
nonroots. No enumeration of root assignments or assumption about their values
is needed.

Reproduce.py starts without private seeds. It constructs a mandatory12-case
pilot, checks it in normal and optimized Python and rejects22 distinct
corruptions per mode. It then regenerates every remaining case, reusing only
that completed identical-source pilot. The resulting625-case certificate
must have exactly the supplied bytes. It is checked in both modes, again with
22 corruptions per mode. The supplied certificate also gets a separate
positive check in both modes. Fresh construction uses519 greedy successes and
106 capped SAT matching successes; every matching witness is independently
checked on its actual terms before whole-cohort checking.

Corruptions cover omitted and duplicate cases, wrong coefficients or field,
Boolean indices/coordinates, roots, bichromatic APs, overlap within and between
pairs, an incorrect reflection, missing pair members, invalid starts or
steps, extra root hypotheses and unsupported stronger bounds. Each rejection
must identify its intended mathematical defect, not hit an operational limit.

Audit_reduction.py is copied unchanged from the previous20-AP source. It checks
character multiplicativity and every odd/even CRT parameter pair, all leading/
cubic cancellation pairs, and normalization/restoration for all96,721(A,B)
pairs in five adjacent A-domain slices. These arithmetic checks support the
written reduction; the previous numerical packing certificate is not a
premise. Every actual compute child has a30-second external guard and at most
200,000 declared cases. All threads and the simultaneous compute-job count
are one. SAT is requested at9,500 conflicts with a10,000 reported hard bound.

## 6. Repair conclusions

If an AP remains unchanged at every field residue in its support, it remains
monochromatic. Each of the24 disjoint supports contains only nonroots, so an
AP-free c_psi must change at least one nonroot bit in each support. Disjointness
requires at least24 distinct field-bit changes, even if every root is also
changed. Root recoloring alone cannot succeed.

Every residue modulo311 occurs at least floor(3704/311)=11 times among
zero-based positions0,...,3703. Changing a template bit changes all positions
of that residue. Thus an AP-free repair within this template changes at least
24*11=264 nonroot coordinates on[1,3704]. Without the template restriction,
disjoint field supports still imply disjoint actual position sets, so any
AP-free word on[1,2171] or[1,3704] differs from this seed at at least24 nonroot
positions. The264 consequence requires the template.

## 7. Prior work and scope

This strengthens the same-family [20-AP even-quartic lemma](../van_der_waerden_622_even_quartic_character_repair)
from20 field edits/220 template coordinates to24/264. That source's arithmetic
audit is reused; its packing certificate is not used to prove the new bound.
The [degree-at-most-three lemma](../van_der_waerden_622_degree3_character_repair)
concerns a different polynomial family. No containment of all its character
words is asserted. No optimality or distinct-orbit claim is made here.

The [aligned QR617 balanced33 profile](../van_der_waerden_27_qr617_balanced33_profile)
and [QR617 reflection-phase individual198 result](../van_der_waerden_617_single198_implications)
have different seeds and edit domains. Their numerical constants and proof
corpora are not used in this argument. We claim no novelty for reflection,
affine normalization, character multiplicativity, greedy matching, cardinality
encodings or the classical cyclic zipper of
[Herwig, Heule, van Lambalgen and van Maaren](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v14i1r6).
The contribution is the completely checked stronger scoped quartic repair
bound, new to the bounded inspected graph/source context. No exhaustive
literature priority claim is made.

[Monroe Table1/Table2](https://arxiv.org/html/1603.03301v7), rechecked2026-10-01,
records the historical two-color/seven-term seed>3703 and prime617, using
W(length,colors) notation. The campaign uses W(2,7) for colors first. A binary
AP-free word on[1,3704] would establish W(2,7)>=3705; none is supplied here.
The asymmetric w(3,k) problem is different. This lemma does not exclude all
quartics, all311-bit template words or arbitrary3704-point colorings, and
gives no new W(2,7) bound.

Trust boundary: the written finite-field reduction and exact stdlib checker,
implemented separately by the same named researcher. No external independent
review or proof-assistant formalization is claimed. PySAT is a proposal tool,
not a mathematical proof premise. Its pinned software release is
[python-sat1.8.dev24](https://pypi.org/project/python-sat/1.8.dev24/).
