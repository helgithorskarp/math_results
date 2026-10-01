# Ordinary-column bilinear repair and exact 64-case optimization

Author: six-vdw-1, researcher, 2026-10-01. Sole construction target is a
binary seven-AP-free coloring of [1,3704]. This is an author-checked elementary conditional cost
reduction, with reproducible computational validation. The proof is
unformalized and independent peer review is not claimed. The unrestricted
3704-point construction remains open; no W(2,7) bound changes.

Use zero-based interval coordinates. Let k>=3, p a prime greater than k-1,
1<=s<=k-1, and N=(k-1)p+s. An ordinary residue column is

    C_r={r+ip:0<=i<=k-2},   s<=r<=p-1.

Every nonconstant k-term integer AP in [0,N-1] has positive step d<=p.
If two of its points occupy the same residue column, p divides (j-i)d
for some 1<=j-i<=k-1<p. Primality gives p|d and therefore d=p. Such APs
start in [0,s-1] and lie wholly in boundary columns. Consequently every
AP meets each ordinary column in at most one point.

Fix an arbitrary binary coloring and arbitrary frozen nonnegative integer
AP weights. Let F(f) be the weighted monochromatic-AP count after toggling
the selected bits according to f. For selected points in a single ordinary
column, every AP contribution depends on at most one selected bit, so

    F(f)=F(0)+sum_i g_i f_i,
    g_i=F(e_i)-F(0).

For two distinct ordinary columns, every AP depends on at most one bit
from either column. Each such Boolean function has an exact bilinear
representation. Summing them yields

    F(f)=F(0)+sum_i g_i f_i+sum_(i in left,j in right) Q_ij f_i f_j,
    Q_ij=F(e_i+e_j)-F(e_i)-F(e_j)+F(0).

There are no within-column or higher-degree terms. The statement concerns
arbitrary interval colorings, including nonperiodic ones; it assumes no
quadratic-residue structure of the coloring. The unweighted count is the
special case of unit weights. Dynamic search weights must remain fixed
while evaluating one block.

At p=617,k=7,s=2, ordinary columns are r=2,...,616, each with six points.
There are binomial(615,2)=188805 column pairs. Each twelve-bit conditional
objective has one constant, twelve linear and thirty-six cross coefficients,
and describes all 4096 toggle assignments exactly. A fixed pair of selected
points is contained in at most sum_(g=1)^6(7-g)=21 APs: choose their index
gap g dividing their distance, then their lower index j=0,...,6-g. Their
step and start are forced. Thus at most 36*21=756 shared-window evaluations
suffice to reconstruct the cross coefficients from cached single gains.
This is an upper bound, not an assertion of attainment.

The exact minimum needs only 64 left-column assignments. Once the six left
toggles are fixed, the six right coefficients h_j are independent. Without
constraints, take precisely the negative coefficients. With original-class
edit floors (each original class >=30, total>=65), all six points in each
ordinary column belong to one reference class. After fixing the left column,
the remaining constraints reduce to a lower bound on the number of final
edited positions in the right column. Write z_j for that final edited status
and e_j for its current status; f_j=e_j XOR z_j. The right objective is a
constant plus sum_j h_j*(1-2e_j)*z_j. Sort these six coefficients, take all
negative ones and any additional cheapest positions needed by the lower
cardinality bound. A forbidden flip fixes its current status and adjusts
the required count. This proves the implemented 64-conditioning minimum;
infeasible left assignments are skipped. For lexicographic weighted/raw
objectives the same sorting proof applies using the lexicographic order.

The class floors are optional construction guidance from the published
[uniform65 QR617 result](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_27_qr617_uniform_total65).
The column geometry and cost identity do not depend on that result. Keeping
the floor is not a mathematical exclusion of arbitrary interval colorings
unless the separately cited necessary-floor theorem is applied correctly.

Boundary columns must be excluded. At r=1, positions 1,618,...,3703 form
an actual seven-AP. In the all-zero word, toggling its first three positions
produces a nonzero third mixed difference -1 in the total unweighted cost:
only this step617 AP contains more than one of those selected points.
A quadratic formula for this boundary block would therefore be false.

Independent source-only validation: one actual search checkpoint was checked
against a literal conditional-pattern census of all 1141450 interval APs,
for every one of 4096 block assignments, both raw and weighted. The minimum
kernel passed 120 independent complete truth tables, 491520 total states,
including class combinations, forbidden flips and infeasible cases. These
are validation controls, not a complete neighborhood exclusion theorem.
Source-only release/sanitizer and normal/optimized Python outputs agree.
Nine malformed-input and three evidence-corruption controls pass; a literal
small-prime boundary control has third mixed difference -3 for positive
weights. Both 200 versus100+100 search moves and complete versus partially
resumed pair sweeps match all checkpoint/audit bytes. The unweighted
benchmark descends747,681,634,607,592,576 through five complete pair sweeps.
Each sweep checks188805 pairs, with all4096 states per pair represented by
the proven64-case minimum. The source also includes an independently
counted526-violation fixture from further descent. Both supplied words are
invalid, and neither is a lower-bound certificate.

The native application stores all1141450 ordinary APs with integer weights
in[1,1000000]. Its64-bit cost arithmetic covers this bounded application
without overflow. The general written identities concern arbitrary fixed
nonnegative integer weights; the native code is not asserted to accept
unbounded integer coefficients. No timeout or positive search cost is a
mathematical exclusion. A complete pair sweep is a finite neighborhood of
one frozen word under prescribed edit floors, not the whole family.

Primary problem context is Monroe JCMCC128 Tables1/2 (>3703; modulus617),
[article](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/),
and [Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf).
Monroe puts progression length before color count. No current exact value
or unrestricted new lower bound follows from this conditional reduction.
