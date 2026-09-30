# A binary-union certificate for one period-43200 prefix

Actual author: **six-covering-3**, role **researcher**, 2026-09-30.
Written proof and exact author checks; no independent review or historical-priority claim.

No finite distinct covering by moduli at least8 dividing43200 contains
the eight prescribed congruences

    [(8,0),(9,0),(10,5),(12,1),(15,11),(16,4),(18,3),(20,16)].

The ordered pairs are (modulus,residue). The actual LCM of a proposed
completion need not equal43200. The prescribed8-class would make its
minimum exactly8. This excludes one fixed prefix, not all assignments
at43200 and not either global candidate10080 or15120.

The mechanism applies six-covering-2's
[fixed-binary distinct-point and cluster proof](../distinct_covering_fixed_binary_clusters/proof.md),
source7fdc72707e47e4a230ef50b9c8fef55124599f51, after conditioning on the
unplaced coarsest class. Here the unrestricted component is zero. Its
distinct-point/union mechanism is attributed to that author; the earlier
[single-pair overlap correction](../distinct_covering_coarsest_block_review5/REVIEW.md),
source16fffdf8660ac980b5a11c5efa0ba9e7f5868a00, is six-reviewer-5's result.
The new content is the compact certificate for this previously open prefix.
No assertion that every completion of the prefix requires this method.

## Binary blocks and the upper bound

Let N=BC with B a power of two, C odd, T=B/2, and b|T. Suppose
all top resources S={Bd:d|C} are eligible and unplaced. Known classes
have proper B-part. Let w>=0 be bC-periodic and vanish on every known
class. Its CRT values are W_z(t), t modb,z modC. A primitive block
q+Tj, j=0,1, at fixed z has two physical B-coordinate points and a
common weight W_z(q modb).

Every outside congruence has proper B-part dividing T; at fixed z its
indicator is identical at both points. If the top classes cover at most
one distinct point, covering the other forces outside classes to cover
both points. If they cover both points, charge the periodic mass twice
to those two distinct points. Thus outside footprints plus

    2*sum_(q,z with both top points active) W_z(q modb)

meet the full demand. This counts distinct points, not resource
multiplicity. Known outside classes cost zero by support. Ordinary
unused outside capacities can replace their actual footprints.

Adjoin an arbitrary phase of every omitted available top modulus.
This preserves a cover and cannot decrease the distinct-point charge.
Fix the B-class at alpha0 modB and put q0=alpha0 modT, t0=q0 modb.
At q0 its point is active for every z. A Bd class in that block sharing
alpha0 is redundant with the B-class. It can be moved to the opposite
point alpha0+T, with the same cofactor phase, without uncovering any
integer. Explicitly its full phase can be shifted by Td modulo Bd,
since d is odd. Distinct moduli and their LCM do not change. Hence the
charge at q0 is at most twice the weighted union of the other inside
cofactor cosets. In every other block, distinct-point charge is at most
the sum of the actual individual top footprints.

For d|C,d>1 define

    H_d(t)=max_(a modd) sum_(z=a modd) W_z(t),
    M_d=max_t H_d(t).

Choose a cluster P of distinct divisors d>1. For each inside subset I
of P retain the actual union of its cofactor cosets. Set

    F_P(t)=max_(I subsetP, a_d modd for d inI)
           [2*sum_(z in UNION_(d inI){z=a_d modd}) W_z(t)
            +sum_(d inP outsideI) M_d],
    G_P=max_t [F_P(t)+sum_(d|C,d>1,d outsideP) max(M_d,2H_d(t))].

This is an upper relaxation. Inside noncluster resources contribute
at most2H_d(t0); outside resources contribute at most M_d. The entire
inside cluster union is charged once with coefficient two. Enumerating
every inside/outside placement proves, for actual unused resources R,

    sum_(x modN) w(x) <= sum_(n inR outsideS) C_n(w)+G_P,
    C_n(w)=max_(a modn) sum_(x=a modn) w(x).

This does not assume simultaneous attainment of the individual maxima.
Taking extra hypothetical outside phases in M_d is harmless for an
upper bound, even if a block label is available only inside. Zero
weights, omitted resources and smaller actual LCMs are permitted.
For P={p,r}, the both-inside term is2U_p+2U_r-2I_pr. This stronger
binary coefficient is justified by the two distinct points; it must
not be imported into the arbitrary-B multiplicity bound. Whole unions
also avoid unsafe independent subtraction of many pair intersections.

## Exact input and complete finite evaluation

For the stated prefix take B64,C675,b16,Q720 and P={3,5}.
Q divides bC=10800. The26 disjoint boxes in [input.json](input.json)
have axes(16,9,5); each box is (three coordinate masks,positive integer
weight). A physical integer x receives its box's weight exactly when
each mask contains x modulo its corresponding axis. All other x have
weight zero. No orbit declaration, LP status or private search is a
proof input.

All eight prescribed classes have zero weight. Exactly70 eligible
moduli remain unused;12 are top and58 outside. All are counted,
including every unplaced top resource even if a completion would omit
it. Literal integer calculations give:

| Quantity | Physical value |
| --- | ---: |
| Demand | 55920 |
| Outside capacity,58 resources | 53296 |
| Binary-union top upper budget | 2622 |
| Total / strict deficit | 55918 / 2 |
| Ordinary capacity,same vector | 56182 |
| Older fibre capacity,same vector | 56140 |
| Older coarsest G capacity,same vector | 56188 |
| Reviewer single-pair capacity,same vector | 56053 |

The first inequality is therefore impossible. The comparisons establish
only a same-vector improvement, not optimized dominance or necessity
of this mechanism for the prefix. The
[older coarsest proof](../distinct_covering_coarsest_block_budget/proof.md),
source959893f7358905bc46ddb01fdcaaffa8086ffe3f, is six-covering-3's result;
the older fibre framework and weighted residual resource method are
attributed in those campaign sources. No new general counting principle
is claimed.

[check.py](check.py) evaluates every one of157351 actual unused
resource phases over all43200 residues. It evaluates all384 selected
cluster cases:16 labels times(1+3)(1+5) cofactor placements. The
cofactor phases are checked by ordinary progressions at the opposite
B-coordinate, with literal unions and no CRT inversion. It pins every
phase-value digest and every cluster-case digest, the exact integer
weight vector and the input bytes. The small positive control genuinely
covers period12 with minimum2; it is not a minimum8 construction.
Eleven malformed or unsupported variants are explicitly rejected even
under Python optimization.

Reproduce with Python3.10+ and the standard library, from repository root:

    python3 -B number_theory/distinct_covering_43200_binary_union_prefix/check.py
    python3 -B -O number_theory/distinct_covering_43200_binary_union_prefix/check.py

Both outputs must match [expected.json](expected.json). [SHA256SUMS](SHA256SUMS)
pins the six proof/source/evidence files. Floating optimization was used
only to discover the integer vector. Trust boundaries are ordinary Python
arbitrary-precision arithmetic, the compact literal input and the written
binary two-point argument. No solver, proof assistant, enumeration of
all prefixes or omitted private forest is assumed. These are author
checks independently of the LP/profile implementation, not peer review.

## Primary and campaign context

[Zhang--Zhang](https://arxiv.org/html/2607.19029) supplies the
minimum-seven filtering context, and [HKLT Problem3](https://arxiv.org/html/2605.18644)
is the separate pure235 minimum-eight target. Both were retrieved live
2026-09-30. Neither is a premise of this finite conditional certificate.
The elementary binary argument is the two-point instance of the
earlier [primitive-block framework](../distinct_covering_primitive_block_capacity/proof.md),
source234569d6f32f1ad96958ed3300050d9ce7acef1e, authored by six-covering-3.
The fixed-binary cluster source and the independent reviewer pair source
are explicitly credited above; neither review is asserted to review this
new certificate. Global exactly-eight candidates remain10080,15120,20160;
no numerical global or pure235 bound changes here.
