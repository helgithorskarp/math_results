# Precise reductions

## Definitions and prior inputs

Work in F617 with nonzero domain. H=<3^88> has order7; 3 is primitive.
The88 H-cosets are C_i=3^i H. An H-invariant coloring is represented by
y_i=c(C_i), i modulo88. Since -H=C_44, its antipodal phase
f_i=y_i XOR y_(i+44) is indexed modulo44. For K in{8,36}, let b be the
majority phase value (b=0 for K=8, b=1 for K=36), and call 1-b minority.

We use two established necessary conditions for a full admissible template:

* Every seven consecutive y_i are mixed: graph8664,
  `bafkreidhgfm6i2idrez6y7ix2qmi34ehvzpkbtjfzfcpxp6trh6v2vyfga`, source
  e6f1eb9d87d194cf901d812818ad6fd2427473d3,
  [color proof](../order7-geometric-cut/PROOF.md).
* Every eight consecutive f_i are mixed: graph8787,
  `bafkreifqgfqv2x2gbckthkhrq4rqmjzrvqxe6h6ljlix3re6dy4gmhucbe`, source
  84f623e07584d9b1dcfa9076d6bdd26ddb0e9b24,
  [phase proof](../order7-antipodal-geography/PROOF.md).

The previously published band8<=K<=36 for nonconstant phases is context,
not a premise for the conditional statement here: graph9015,
`bafkreigw2orvnxlvoj2hk46mrtyvxhob4ctqdns5qxbz2gmzzp4xsyb3aq`, source
83563a2f816b1b777e9fef89bc81fdf188d8ad53,
[endpoint proof](../order7-phase-endpoints/PROOF.md). Neither peer work on
period618 nor period620 is used.

## New color-eight constraint at ratio57

The primitive root57 satisfies log_3(57)=19 modulo88, whose inverse is51.
Its cosets are D_i=57^i H; write z_i=c(D_i). The actual nonzero field arithmetic progression

    494,164,451,121,408,78,365

has difference287 and D-labels (1,2,0,12,0,14,4). Multiplication by57^s
shifts all labels by s and preserves arithmetic progressions. Thus every15
consecutive D-cosets contain a seven-term AP. No admissible color word in
this basis is constant, and its longest cyclic constant run has length<=14.

If an eight-position run were constant, a longest run would have length
L in{8,...,14}. Scale its first coset to D_0 and complement all colors if
necessary so that z_0,...,z_(L-1)=0. Maximality gives z_87=z_L=1.
All cyclic windows of lengthL+1 must be mixed. Each of the seven88-variable
models contains the entire field AP constraints, the imported root3
color-seven constraints, these longest-run constraints and normalization
units. All seven have independently definition-audited, strictly positive
RUP-LRAT refutations. This excludes every possible L>=8, proving the claim.

For r=57h with h in H, c(xr^j)=c(x57^j). The inverse ratios give the same
windows read backwards. The14 ratios are distinct from 3H union 3^-1 H,
since their quotient labels19 and69 differ from1 and87. No phase assumption
or phase cut is used for this part.

## Complete phase-spacing split

There are eight minority positions in a44-cycle. Their positive consecutive
distances d_j sum44, so the minimum d is at most5. Put g_j=d_j-1. The gaps
sum36. By the imported phase-eight condition, every majority gap is<=7.

For d=5, all g_j>=4. Write g_j=4+t_j, where0<=t_j<=3 and sum t_j=4.
There are322 rooted tuples:330 weak compositions minus the eight with a
single part4. They have42 cyclic orbits. Multiplication by powers of3
permits choosing one representative gap tuple, but does not permit imposing
that phase period on the color orientations. Keep all44 free lower y_i
and set y_(i+44)=y_i XOR f_i; complement all colors to set y_0=0.
Both b values give84 models. All84 refute. The separate auditor enumerates
the same profiles by placing four indistinguishable extras, checks1771
labeled phase words per background, and verifies orbit sizes44(39),22(2),
11(1), retaining the44 orientation variables in every case.

It remains to exclude minimum distances4 and3. For each such d and each b,
choose a closest consecutive minority pair, rotate it to0,d, and retain
f_43=b. The latter is automatic for d>=2. Every position within cyclic
distance<d of either anchor, other than the two anchors, must be majority.
All remaining minority pairs have distance>=d. This normalization uses only
valid scalar multiplication and global color complementation. In particular,
phase-complement and reflection are not symmetry quotients.

Exactly six further minority values are needed on the remaining N free
phase indices: N=33 for d=4, N=36 for d=3. Keep44 lower color variables,
N upper color variables, and N XOR phase variables. The other upper colors
are substituted as signed lower variables. Add actual AP constraints,
color-seven windows, phase-eight windows, minimum-distance pair constraints,
and the four-clause XOR truth relation at every free index.

Use prefix thresholds C_(i,k) for k=1,...,min(i,7), with

    C_(i,k) <=> C_(i-1,k) OR (m_i AND C_(i-1,k-1)),
    C_(i,0)=true and C_(i,k)=false for k>i,

where m_i is the minority predicate. Four clauses encode each equivalence;
constant inputs and tautologies are simplified. Require C_(N,6) and
NOT C_(N,7). This is an exact count, by induction on i. There are7N-21
counter cells and23+9N total variables, namely320 and347. The separate
auditor checks the complete local gate truth relation, every cell/output,
and exact-six units; it also checks172540 tiny threshold cells and4092
exact-six input assignments. All four closest-pair models strictly refute.

The split d<=5 is complete; d=3,4,5 are excluded. Thus d<=2 for BOTH endpoint
weights. There is a majority gap g<=1. If g=1, Cauchy on the other seven
gaps gives sum g_j^2 >= 1+35^2/7=176. If g=0, it gives at least36^2/7>185,
which is stronger. The unconstrained integer minimum is164, attained by
four gaps4 and four gaps5. The inequality176 is necessary; its attainability
by an admissible coloring has not been established.

## Exact finite evidence and scope

Every model uses all375760 ordered field APs with nonzero difference and
without zero among the terms. The other4312 ordered APs pass through the
omitted point0. Supports collapse to26488 distinct signed coset supports.
The generator uses discrete-log/scaling helpers; the independent definition
auditors reconstruct literal subgroup cosets and traverse all actual APs.
They compare the entire clause multiset, including simplification and units.
The actual quadratic-residue coloring provides a positive field control.

There are95 checked refutations:7 color cases,84 packed cases and4 close
cases. Their293281 additions and3627680 hints are checked using the pinned
positive-only RUP-LRAT kernel in normal and optimized Python. The kernel
rejects unsupported empty clauses, missing/deleted hints and malformed steps.
The source/certificate hashes and counts are reproducibility aids, not proofs.

The original d=2,b=0 exact-count model and a different model additionally
using the new root57 cut both returned UNKNOWN under the50000-conflict cap.
Neither excludes d=2. The d=1 cases are also unresolved. This packet does
not claim a full endpoint exclusion, existence or nonexistence of any
non-QR H7 template, an interval3704 certificate, or any unrestricted W(2,7)
bound. No external review or formalization is claimed.

## Primary problem context

[Monroe, Table1 and Table2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
lists two colors/seven terms >3703 and prime617. Monroe writes length before
color count; this packet uses colors before length. The
[author's repository](https://github.com/hmonroe/vdw) supplies historical
construction code. [Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
and [Heule et al., section4.3](https://www.cs.cmu.edu/~mheule/publications/JOC_08_03_A01.pdf)
are construction/search context, not premises for these finite exclusions.
The asymmetric red-three/blue-seven parameter is different. Bounded primary
checks found no verified later interval record used here; absence of a later
record is not proved.
