# Internal check: Atlas conditional induction, version 1

Checker: Nova, studio-researcher-3, researcher. Date: 2026-10-05.
Author: Atlas, studio-researcher-1. Scope: sections 1,2,4 of PROOF.md.
Exact SHA256: 208096e0a2ba2021dbb713d7ef0741bd4d9b74e6c61bfeb17623d0fd4cd91ee4.
Source: /scratch/research-team-colloquium-sol61-20261005/workspaces/studio-researcher-1/group_theory/nonsolvable_cyclic_gap_induction/PROOF.md.

Outcome: accepted as a CONDITIONAL induction from B6, E, C and the stated
Hall-branch proposition. This is an internal mathematical check, not
external review, and does not certify those separate inputs.

I independently reconstructed the quotient argument: cyclic image
surjectivity gives c(G)>=c(Q) for a persistent kernel prime. For a new
prime, the elementary cocycle averaging gives a split extension and the
nonnegative coset defect gives c(G)>=2c(Q). The respective prime counts
are equal or differ by one, so eta(Q)<=eta(G) in both cases. This does
not use an induction hypothesis or the target's truth. The cocycle sign
is correct: replacing the section by minus B cancels its coboundary.

Inside a nontrivial solvable radical, a minimal nontrivial G-normal
subgroup is elementary abelian. Its quotient remains nonsolvable, and
has smaller order. These facts permit precisely the stated induction
hypothesis. The new-prime Hall branch preserves every permitted exponent
profile once it forces rank one and trivial action. Proposition H is
Iris's separate checking scope; this report uses its exact statement.

For persistent p=2,3,5, I recomputed the A5 weights 17/15,22/10,26/6.
Their normalized lower values are 49/8,27/4,29/4 multiplied by delta(m),
all >6. For p>5, write m=p^a r. The denominator is 2^(4+omega(r)),
and the resulting bound is 2 delta(r)[c(V)+a p^(d-1)]. Rank>=2,
a=2, or a squared prime in r all give >6. The sole remaining profile
has rank one, a=1 and squarefree r, and eta(G)<=6 forces equality at 6.
The odd-p equality condition makes A5 and C_r act trivially, and the
cyclic p-part has trivial image in Aut(C_p) of order p-1. Thus centrality
follows without global splitting, and precisely input C applies.

The coprime product converse is exact, with the trivial group convention
giving m=1. No threshold-four strictness is used to infer a six-margin.

Interface comparison: Rowan's fixed proof SHA256 813c8449357199d7db6ff9ac3f13725b6239dbb44f2bb721a78f748a90adc7de
implies E as stated, including its quotient-family specialization. Iris's
fixed proof SHA256 ea938c7b0313e008db5e7632a144d06c4a8038576f24714a99fdec294a59a769
states a broader central-extension conclusion that includes exactly C.
I checked this interface containment; Rowan is the designated checker
of Iris's actual proof and computational controls. B6 remains a separate
base draft pending Atlas's internal check. This acceptance closes the
conditional-induction checking task, not the campaign classification.
