# A period15120 prefix: an integer exclusion and a fractional completion

Actual author **six-covering-2**, role **researcher**, 2026-09-30.
Finite exact certificates and written reductions; no historical-priority,
independent-review or proof-assistant claim.

Let N=15120 and fix these twelve classes:

    A=[(8,0),(9,0),(10,1),(14,1),(12,6),(16,4),(15,2),(18,5),
       (20,16),(21,4),(24,2),(27,2)].

Their moduli are distinct, their minimum is exactly8, and their LCM is15120.
Let R={n:n dividesN,n>=8,n not a modulus inA}. There are61 unused resources.

**Finite claim.** No choice of any subset of R, with one arbitrary phase per
chosen modulus, completes A to a covering of the integers. Yet the ordinary
fractional phase relaxation has a rational feasible completion. Consequently
no ordinary resource-by-resource weighted counting obstruction can exclude
this fixed prefix, for ANY nonnegative N-periodic physical weight.

This excludes a finite conditional family, not all covers of period15120.
It does not change the campaign's global exact-minimum-eight bounds. Neither
the parent prefix without27 nor the other27 phases is assumed excluded here.

## Binary cluster inequality used for the exclusion

Write N=BC with B16,C945, T8 and Q=bC=7560, b8. The full-B resources
are S={16d:d|945}. The ONLY prescribed member is16=4. Its primitive block
has binary coordinates4 and12. For nonnegative N-periodic u vanishing on
every known class and nonnegative Q-periodic v, let

    D(f)=sum_(x modN)f(x), Phi_(n,a)(f)=sum_(x=a modn)f(x),
    C_n(f)=max_(a modn)Phi_(n,a)(f).

The prescribed-top binary-cluster inequality is

    D(u+v)-sum_(known n outsideS)Phi_(n,a)(v)
      <=sum_(n inR outsideS)C_n(u+v)+K_cluster(u,v).      (1)

The known16 footprint is NOT subtracted. To specify K_cluster, in the CRT
coordinates alpha mod16,z mod945, put

    U_d(alpha,r)=sum_(z=r modd)u(alpha,z),
    V_d(t,r)=sum_(z=r modd)v_t(z),
    L_d=max_(alpha !=4 mod8,r modd)[U_d(alpha,r)+V_d(alpha mod8,r)],
    H_d=max_(r modd)[U_d(12,r)+2V_d(4,r)].

Choose P={3,5,7,9}. For G subsetP define

    F_G=max_(r_d modd,d inG)
          [sum_(d inG)U_d(12,r_d)
           +2sum_(z in UNION of these cosets)v_4(z)],
    F_empty=0,
    K_P=max_(G subsetP)[F_G+sum_(d inP outsideG)L_d],
    K_cluster=K_P+sum_(d|945,d>1,d outsideP)max(L_d,H_d).

The union is counted once, with coefficient two. The complete selected
cluster has product_(d inP)(1+d)=1920 phase/subset cases. This is an upper
relaxation of the full top budget; no exact16-resource optimizer is claimed.

Here is a direct proof of (1) in the binary case. At fixed q mod8,z mod945,
the two points have B-coordinates q andq+8. Every proper-B modulus divides
7560, so its class indicator is identical at both points. The weight v is
also identical there. If at most one DISTINCT top point is active, covering
the other point requires a proper class, which covers both and pays the whole
periodic demand. If both top points are active, charge their2v-weight once.
Add ordinary u-counting, using u=0 on all known classes. Combine the outside
u/v footprints at their SAME actual phase before taking C_n.

In the prescribed block q=4, the known16 class already supplies point4 for
all z. A free top class there at point4 has zero u and no further periodic
effect. Moving it to point12 with its same cofactor phase cannot reduce the
objective. Thus the periodic charge in that block is twice the union of
opposite-point cosets. Keep this union for the selected cluster; bound every
other inside coset individually by H_d. Other blocks have no prescribed
top point, and their periodic charge is at most the sum of actual free
periodic footprints, bounded together with u by L_d. Maximizing the cluster's
inside subset and its phases proves (1). Omitted free classes can be adjoined
without decreasing these nonnegative charges. All tail subsets are covered.

This is the binary specialization of six-covering-2's published
[fixed-top point and cluster bound](../distinct_covering_fixed_binary_clusters/proof.md),
source7fdc72707e47e4a230ef50b9c8fef55124599f51, graph7633. That source credits
six-covering-3's primitive-block mechanism7420 and mixed inside/outside
profiles7568, and six-reviewer-5's pair/cluster observation7520. The written
argument here is self-contained. The finite certificates below are the new
application; the general binary lemma is not claimed anew.

## Exact integer exclusion certificate

[input.json](input.json) gives40 positive u-boxes with axes(16,27,5,7) and
18 positive v-boxes with axes(8,27,5,7). A box of value w contributes w at
the physical x when every x modulo the corresponding prime power belongs
to its axis set. The boxes are disjoint; other weights are zero.
This definition needs no CRT constructor or orbit theorem.

The literal checker proves u=0 on ALL known classes and v=0 on every known
proper-B class. The periodic weight on the prescribed16 class is72726;
it is intentionally retained in the prescribed-top budget.

| Physical quantity | Exact value |
| --- | ---: |
| Effective demand D(u+v), known-outside cost0 | 999672 |
| Outside capacity, all46 resources and28594 actual phases | 829414 |
| Cluster top upper budget, all1920 cases | 170139 |
| Total capacity | 999553 |
| Strict gap | 119 |
| Capacity with no cluster, individual max(L_d,H_d) only | 1027770 |
| Ordinary residual demand for this weight, masked off known classes | 926946 |
| Ordinary residual capacity for this masked weight | 947842 |

Thus (1) fails by119, which excludes every completion in the stated family.
The selected cluster saves28217 compared with the individual fixed-binary
budget and is necessary for strictness of THIS vector. No assertion about
the optimized no-cluster bound is made.

## Exact fractional completion and ordinary-weight impossibility

Let y_(n,a)>=0 denote the tail phase variables. The ordinary relaxation is

    sum_(a modn)y_(n,a)<=1                     for every n inR,
    sum_(n inR)y_(n,x modn)>=1                for every uncovered x.

Known classes have their prescribed phase with weight1. A mass below1 can
be topped up at any phase if divisor completion uses equality rather than
the optional-resource inequality. This preserves coverage.

[fractional.json](fractional.json) represents105 phase groups for all61
unused resources. Its common denominator is1000000. A group with numerator h
and g actual phases assigns h/(1000000*g) to EACH phase. A phase belongs
when its residues modulo the prime-power factors of its modulus lie in the
listed phase axes; the decoder checks g by literal enumeration.

For every resource the group numerators sum to at most1000000. Taking720 as
the LCM of the actual group sizes gives a common coverage unit720000000.
All5392 residues left uncovered by A have scaled tail coverage at least
726304320. Therefore their coverage is at least

    726304320/720000000 = 252189/250000 > 1.

These are exact rational feasibility checks on every physical residue, not
a floating LP optimum or an inferred dual certificate. The certificate is
verified without the LP, symmetry reduction, rounding or discovery generator.
It is fractional and does not give a congruence-covering witness.

For any nonnegative physical weight w, multiply the pointwise completion
inequality by w and sum. Resource masses at most1 give

    D(w) <= sum_(known n,a)Phi_(n,a)(w)
            +sum_(n inR,a)y_(n,a)Phi_(n,a)(w)
         <= sum_(known n,a)Phi_(n,a)(w)+sum_(n inR)C_n(w). (2)

Consequently the ordinary weighted counting test cannot be strict at this
prefix, even with arbitrary full-period weights and actual known-footprint
subtraction. Supported residual weights are included as a special case.
This statement concerns individual resource capacities; it does not rule
out joint union capacities or other structural inequalities. The integer
exclusion and rational completion establish the claimed finite separation.

## Reproduction, controls and trust boundary

Run [check.py](check.py) from repository root, with Python3.10+ and the
standard library only:

    python3 -B number_theory/distinct_covering_15120_cluster_fractional_separation/check.py
    python3 -B -O number_theory/distinct_covering_15120_cluster_fractional_separation/check.py

Both must reproduce [expected.json](expected.json), including both input
hashes. The integer checker decodes literal residue predicates, examines
all actual outside phases, and forms actual progression unions in the
opposite binary point. The fractional checker traverses every represented
phase and every physical residue. Eight integer and seven fractional
malformed cases are rejected. A genuine36-period cover with minimum2
supplies a positive fractional control; it is not a target witness.

Discovery used bounded, single-thread SciPy/HiGHS LPs with2-second solver
limits, integer rounding, and an elementary periodic-weight erasure when
known proper moduli divideQ. None of these is a proof input. No solver output,
private proof forest, omitted numerical optimality certificate or independent
review is required or claimed. Trust rests on the written binary/union and
weighted-summation arguments, literal compact input, ordinary Python
arbitrary-precision integer arithmetic, and the unformalized decoder.

Source context: [weighted resource framework](../distinct_covering_residual_weight_duals/proof.md)
by six-covering-2, sourceb9d39eb740a866e07237be1c78b834d1ab6ea718, graph7174;
[coupled coarsest profiles](../distinct_covering_coupled_coarsest_budget/proof.md)
by six-covering-3, sourcee31259c8420004b5521b823e03050ddd58a8dbdf, graph7568;
and six-reviewer-5's [coarsest pair review](../distinct_covering_coarsest_block_review5/REVIEW.md),
source16fffdf8660ac980b5a11c5efa0ba9e7f5868a00, graph7520. That review
does not review this certificate. Covering-3's complementary
[eight-class43200 application](../distinct_covering_43200_binary_union_prefix/proof.md),
source d0c2b6b515594067537e5035a7f42d13a4dc9690, graph7685, uses the same
distinct-point mechanism in a different conditional family. It establishes
same-vector improvements; no rational ordinary-weight barrier is imported
from it. Neither certificate is a complete period exclusion.
Primary context retrieved live2026-09-30:
[Zhang--Zhang](https://arxiv.org/html/2607.19029) concerns minimum7, and
[HKLT Problem3](https://arxiv.org/html/2605.18644) concerns the separate pure235
frontier. Neither is a proof premise or a solution of the unrestricted
minimum-exactly-eight problem. No general LP or cluster method priority is claimed.
