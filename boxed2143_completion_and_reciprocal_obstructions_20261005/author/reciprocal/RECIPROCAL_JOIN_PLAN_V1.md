# A falsifiable reciprocal join mechanism for the full target

Quinn, workday3, 2026-10-05. This is a research hypothesis, not a theorem.
The agreed bounded-exponential decision410 remains the target.

Use the exact perfect-tree fibers F_h and join count N(alpha,beta) defined
in the separately checked REVERSE_MERGE_AND_JOIN_BOUND.md. The proposed
reciprocal hypothesis R is, for EVERY h>=1 and EVERY alpha,beta in F_h,

    N(alpha,beta) * N(beta,alpha) >= 2^(m_h-1),  m_h=2^h-1.

The kernel is asymmetric in the left/right priorities (LL after R is the
forbidden spine word). R asks whether the opposite ordering compensates for
a poor ordered pair. It does not assert the already refuted pointwise H,
and is not justified by that informal compensation idea.

R would solve the FULL negative target. Both factors are nonnegative counts.
AM-GM gives N(alpha,beta)+N(beta,alpha)>=2*2^((m_h-1)/2).
Summing over the ordered pair population, the two sums on the left coincide
by swapping alpha,beta. The exact join identity would then give

    |F_(h+1)| >= 2^((m_h-1)/2) * |F_h|^2.

Consequently the same checked recurrence bridge b_h>=2^(h-2)(h-3)+1
would imply infinite limsup of a_n^(1/n). Only the R-to-growth implication
is elementary; its universal hypothesis is wholly unproved here.

First decisive tests: compare R entrywise in the existing COMPLETE literal
m7 table (no repeated native enumeration), then compute N(Q_h,P_h) for the
explicit domain-safe P_h,Q_h family already responsible for H's failure.
Reuse the checked N(P_h,Q_h) certificate. Every new transposed count must
check input avoidance and perfect shape and record the complete weighted
level streams. A fixed state cap means incomplete, never a truncated count.
Stop the family at the first R failure or incomplete run. Favorable tests
would not establish R or justify a census expansion; next would be a
uniform injection/entropy argument or a concrete obstruction to it.

An earlier workday3 construction was rejected before any large job: recover
arbitrary leaf permutations in a prescribed perfect maximum tree, using
adaptive internal labels. Already four leaves in relative order2143 have
no such completion at length7. Write the inorder layout a,x,b,r,c,y,d with
b<a<d<c, x>a,b, y>c,d, and r>x,y. If x<c, (x,b,r,c) at consecutive positions
2,3,4,5 is boxed2143. If x>c, (a,b,c,d) is boxed2143, since all other interior
values x,r,y exceed c. Distinctness exhausts the cases. This rejects even
arbitrary internal priorities in that fixed perfect shape, not just the
suggested max-descendant priority rule. It does not reject variable-shape
completions, the source's strict interleaving conjecture, or factorial growth.
The full size7 fiber has43 avoiders but only19 of24 leaf patterns; direct
definition reproduction is retained separately. This new obstruction has
not yet received a different-researcher check and is not in the public packet.
