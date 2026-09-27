# Prior-art boundary for the accepted cap theorem

Targeted comparison, 27 September 2026. The positive theorem and its
certificates are preserved; no cap or flap variant is added. This note
compares precise sufficient mechanisms. A bounded literature search cannot
establish historical priority or exclude an unexamined proof.

## The result being positioned

For pairwise disjoint open caps C_i={x in K:n_i.x>b_i} of a compact convex
K in R3, reflect each cap in its plane and fix the core. The
[accepted theorem](../gaussian_cap_auxiliary_certificates/PROOF.md) constructs
an analytic contracting motion in R5 when the normals lie in one closed
hemisphere, with arbitrarily many caps, or when there are at most four caps.
It gives all-law/all-variance Gaussian majorisation and both union and
intersection inequalities for arbitrary individual ball radii.

Its [independent review](../gaussian_cap_auxiliary_review2/REVIEW.md), graph
6232, accepts these statements and the stated auxiliary-certificate
obstruction. It explicitly leaves historical priority and the inherited
strong-chain comparison outside its acceptance. The historical pending
headers in the original source are not the current correctness status.

## Primary-source comparisons

The entries below are paraphrases; references identify exact theorem
locations. Statements in the right column are this note's deductions.

| Primary result | What it provides | Exact relation to the cap theorem |
| --- | --- | --- |
| Aishwarya--Li, arXiv:2609.07041v2, Theorem 1.4(i)(a) and the paragraph after Theorem 1.5 | Density-value comparison along continuous contractions; at most two auxiliary coordinates suffice for full Gaussian majorisation | This is the cap theorem's Gaussian transfer premise. The new geometric task is constructing the R5 motion, not a new Gaussian cancellation or transfer theorem. |
| Bezdek--Connelly, arXiv:math/0108098v1, Theorem 1 | Both individual-radius ball inequalities from a piecewise smooth motion in dimension n+2 | The cap consequence is a new sufficient map criterion within this established motion theorem. It is not a strengthening of the transfer theorem. |
| The same paper, Lemma 1, Remark 1, Corollaries 3 and 4 | The canonical leapfrog motion, its affine-span version, a two-dimensional displacement condition, and the automatic N<=n+3 case | The preserved seven-site fixture has seven distinct centers and full paired affine rank six. Its canonical leapfrog has rank six at every interior time, and no independent rigid endpoint frames reduce its displacement span to two. Its separate cap motion is therefore essential to the stated application. |
| Bezdek--Naszodi, arXiv:1701.05074v4, Sections 1.1--1.2 and Theorem 1.3 | Uniform-distance contractions, coordinatewise strong contractions, and union/intersection comparison for unconditional bodies; one-sided folds are strong examples | The fixture is not uniform: a source core distance squared is 2 while a target distance squared is 30. The new closure proof excludes even limits of finite strong chains with freely changing frames. This strengthens the earlier exact-chain separation. |
| Bezdek--Connelly, *On the weighted Kneser--Poulsen conjecture*, author manuscript dated 5 February 2008, Sections 3--6 | Compatible max/min radial weight formulas and their relation to ball flowers; continuously monotone repositionings give the weighted comparison | These functionals are not the hinge of a sum of Gaussian translates. Mixed Boolean flowers require their own pair-sign pattern; the cap theorem's two volume inequalities do not silently prove every mixed flower statement. |

Sources: [Aishwarya--Li](https://arxiv.org/html/2609.07041v2),
[Bezdek--Connelly 2001 manuscript](https://arxiv.org/pdf/math/0108098v1),
[Bezdek--Naszodi](https://arxiv.org/html/1701.05074v4),
[weighted manuscript](https://pi.math.cornell.edu/~connelly/Slepian-2.pdf).

The selected-dilation criterion in Bezdek--Connelly Corollary 5 and all
possible compositions with other known positive classes are **not classified
here**. Neither is the closure of the full R5-motion class: the fixture
already belongs to that class. No separation from every earlier theorem is
claimed.

## Why the rank and closure comparisons are genuine

For the old seven-site coordinates, subtract the row of c0 from each of the
six other paired rows (p_i,q_i). The resulting 6 by 6 determinant is 4096/27.
Independent endpoint isometries preserve its nonvanishing. A displacement
span of dimension at most two would give a nonzero scalar linear relation
between those paired rows, a contradiction.

At an interior time the canonical leapfrog sends a paired row (p,q) to

    ((p+q+cos(theta)(p-q))/2, sin(theta)(p-q)/2).

Its 6 by 6 linear transformation is invertible when sin(theta) is nonzero.
Thus the affine span remains six, including after independent endpoint
frames or an isometric repositioning of a time slice. This rules out the
canonical low-span shortcut, **not** an alternative R5 motion.

The [new closure theorem](STRONG_CLOSURE.md) supplies the missing approximation
quantifier in the strong-chain comparison. Its proof uses the two-state
distance interval and closedness of the elementary relation. It permits
unbounded factor count, moving frames, changing endpoints, and arbitrary
auxiliary labels restricted back to the original sites. Consequently the
cap theorem adds positive inputs beyond the closure of that particular
classical construction mechanism. This is a precise relative extension,
with the new closure proof still awaiting independent review.

The same two-state interval rules out a continuous contracting path in R3:
the continuous distance vector would have to connect two distinct elements
of a finite set. Hence a result that assumes a motion in the original
dimension cannot be applied to this fixture without a new argument.

## Novelty that is and is not supported

The identifiable mathematical contribution is the convex-cap separation
margin and the two-dimensional auxiliary-normal certificate that constructs
the motion. Hemispherical projection and the four-normal certificate are
the accepted automatic cases. The Gaussian and ball-volume transfer
theorems, ordinary one-sided folds, and general piecewise-isometric extension
are established tools, not claimed discoveries of this campaign.

The new supplement adds stability of finite-interval obstructions under
approximation. It also shows that the existing strict rational finite
frontier contains inputs outside strong-chain closure. The control itself
and all of its positive Gaussian/Kneser--Poulsen conclusions are inherited.

Searches on 27 September 2026 used combinations of Kneser--Poulsen with
disjoint caps, cap reflections, hemispherical normals, piecewise isometries,
strong contractions, compositions, and approximation. The substantive
comparison used the primary texts above, not search summaries. It did not
locate the exact automatic cap criterion in these sources. This supports
"new to the compared mechanisms," not an exhaustive priority finding.

No unrestricted dimension-three theorem, negative hinge, new positive map
class, or independently reviewed closure theorem is announced. The former
orthocentric templates and depth-one family remain closed, with their
[theorem and review package](../gaussian_flap_selector_motion/REVIEW_STATUS.md)
preserved. The separate axial class has its own comparison and is not
subsumed by this note.
