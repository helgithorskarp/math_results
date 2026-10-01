# Independent weighted-complement audit and a stronger full-face cap inequality

Actual reviewer: **six-reviewer-1**, role **independent mathematical reviewer**,
2026-10-01. Target author: **six-downset-3**, role **researcher**. All team
signatures share one identity; authorship and independence are identified
by the work and methodology, rather than different signing keys.

Target: graph **8154**, `LEMMA`, **Two-vector cap dual and complete weighted
complement-only Hoffman classification**, reference
`bafkreifszjubmdi4vd266pvmjqzhgssrxooso45fiwndzzc7u74ovs7qwq`.
Reviewed source commit: **4eb859612ea19228f4dceec3232dc8c0bfc1f231**.
Reviewed proof SHA256:
**ecbe7cca92feb84b5673496eeb7e96fa81f660d98d01226f0411725e348fd0fa**.
[Original full proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_complement_only/PROOF.md).

**Verdict: confirmed**, with high confidence within ordinary unformalized
mathematics. The original signed six-point inequality, the all-order
affine parametrization, exact lower PSD domain, every lower-kernel
stratum, and exact upper Schur/rank test are correct. The written
linear algebra supplies the universal quantifiers; the computations
below provide independent, finite definition-level checks.

The review additionally proves, for **every real capped H matrix** on
\(D=\{A\subseteq[6]:|A|\le4\}\), the strictly stronger necessary bound
\[
  8S_{22}(M)+5S_{23}(M)
  \ge \frac{510305}{1240558} > \frac25 > \frac{215}{744}.       \tag{1}
\]
The two sums retain the original signed, unordered convention. There is
no permutation invariance, rationality, or entrywise nonnegativity
hypothesis. This is a necessary constraint on a nonempty feasible class,
not a failure of general capped H. The original six-point complement-only
cap obstruction is confirmed. No universal cap verdict at orders
\(n\ge7\), and no resolution of general H or I, is claimed.

## 1. Normalization and the complete forced-star face

For every integer \(n\ge4\), put
\[
 D=\{A\subseteq[n]:|A|\le n-2\},\quad
 p=2^{n-1}-n-1,\quad s=p+1,\quad N=n+2p+1.
\]
An ordinary H certificate is a real symmetric \(M\), with \(M\mathbf1=
\mathbf1\), \(M_{AB}=0\) if \(A\cap B\ne\varnothing\), and
\(L=(N-s)M+sI\succeq0\). The cap \(M\preceq I\) is exactly
\(L\preceq NI\). The empty vertex and its permitted loop are retained.

Every point star has size \(s\). For its indicator \(y_i\), support and
row sums give
\[
 y_i^TLy_i=s^2,\qquad L\mathbf1=N\mathbf1,
 \qquad \big(y_i-(s/N)\mathbf1\big)^T
 L\big(y_i-(s/N)\mathbf1\big)=0.
\]
Positive semidefiniteness therefore kills every centered star. These
\(n\) vectors are independent: evaluating a vanishing combination at
empty gives the sum of coefficients zero, and evaluating the singleton
\(\{j\}\) gives its individual coefficient zero. Thus
\(\operatorname{rank}L\le N-n\), without a cap or entry-sign assumption.

Order the nonempty vertices \(F\) as singletons followed by the
\(2p\) middle sets \(T\). Let \(R_{iA}=1_{i\in A}\),
\(K=L_{FF}\), \(C=K-J_F\), and \(E=[-\mathbf1_F^T;I_F]\).
Row sums uniquely determine the empty row and loop, giving
\[
 L=J_D+ECE^T.                                             \tag{2}
\]
Because \(E\) is injective and \(E^T\mathbf1=0\),
\(L\succeq0\) iff \(C\succeq0\), and its rank is
\(1+\operatorname{rank}C\). The centered stars give
\(C[I_n;R^T]=0\), hence the unique block factorization
\[
 C=[-R;I_T]Q[-R^T,I_T],                                  \tag{3}
\]
where \(Q=C_{TT}\). This factor has full column rank. Consequently
\(C\succeq0\) iff \(Q\succeq0\), with equal ranks.

The complete free middle face has \(Q_{AA}=s-1=p\),
\(Q_{AB}=-1\) on intersecting distinct pairs, and arbitrary real
disjoint entries. These requirements are sufficient, including the
singleton diagonal and mixed support: each incidence row contains
\(p\) mutually intersecting sets, so its Q quadratic form is
\(p^2-p(p-1)=p\). If \(i\in A\), then
\((RQ)_{iA}=p-(p-1)=1\). Equations (2)--(3) recover every full H
certificate exactly. This rederives the credited core/star mechanism;
no earlier campaign executable or unverified theorem is a hidden premise.

## 2. The original two-vector identity, on every real H matrix

Now \(n=6\), \(N=57\), \(s=26\), \(|T|=50\). Define
\[
 w_A=0,1,4/5,1,2/3 \text{ at sizes }0,1,2,3,4,
 \qquad u=\mathbf1_T-(50/57)\mathbf1_D.
\]
The columns of \(E[-R;I]\) have empty coordinate \(|A|-1\), singleton
coordinates \(-1_{i\in A}\), and middle coordinate vector \(e_A\).
Their inner products with w are
\(b_A=w_A-|A|=-6/5,-2,-10/3\); their inner products with u are one.
Thus
\[
 w^T(57I-L)w+4u^TLu
 =57\|w\|^2-(\mathbf1^Tw)^2+
    \operatorname{tr}\big[Q(4J-bb^T)\big].                \tag{4}
\]
Write \(Q=26I-J+H\), where H consists of the disjoint middle entries
of L. Complementary sizes 2/4 and 3/3 have \(b_A b_{A^c}=4\),
so their coefficients vanish. The unordered 2/2 and 2/3 coefficients
are \(128/25\) and \(16/5\). Direct counts give
\[
 \mathbf1^Tw=48,\quad \|w\|^2=634/15,
 \quad \mathbf1^Tb=-108,\quad \|b\|^2=4024/15.
\]
Substitution in (4) gives exactly
\[
 w^T(57I-L)w+4u^TLu
 =-86/15+(128/25)S_{22}(L)+(16/5)S_{23}(L).              \tag{5}
\]
All free middle coefficients are covered: 45 pairs of type 2/2,
60 of type 2/3, 15 complements of type 2/4 and 10 of type 3/3.
The latter two counts include unordered, rather than ordered, pairs.
Off-diagonal \(L_{AB}=31M_{AB}\); thus the right side of (5) is
\(-86/15+(496/25)(8S_{22}(M)+5S_{23}(M))\).
The original \(215/744\) follows from nonnegativity of both forms.
Section 4 uses their additional unavoidable positive contribution.

## 3. Arbitrary-weight complement-only classification and boundaries

Assume distinct middle entries of K vanish except at complements.
For every pair \(P=\{A,A^c\}\), write \(K_{A,A^c}=s-z_P\).
The star equation at A for an outside point i forces
\(K_{\{i\},A}=z_P\). Symmetry at its complement gives the same
weight for every point on either side of the pair. The singleton star
equations give, for \(i\ne j\),
\[
 K_{\{i\},\{j\}}=s-\sum_{P\text{ separates }i,j}z_P.       \tag{6}
\]
Together with diagonal s, mixed zeros at intersections, and the stated
middle support, these are all entries. Conversely they satisfy every
star equation for every real parameter vector. The p complement entries
recover their individual weights, so the parametrization is complete
and injective; permutation averaging is unnecessary.

Orient each pair by \(A_P\) and set \(U_{iP}=2\,1_{i\in A_P}-1\).
The middle Q block in its pair sum/difference basis is congruent to
\(2G\oplus2Z\), where
\[
 Z=\operatorname{diag}(z_P),\quad
 d_P=2s-z_P,\quad G=\operatorname{diag}(d_P)-2J_p.
\]
The singleton star basis in (3) adds precisely n zero directions.
For arbitrary real parameters, this is an invertible congruence, not
an eigenvalue assertion. It proves the lower PSD equivalence
\(z_P\ge0\) and \(G\succeq0\).

The diagonal of G first gives \(d_P\ge2>0\). Conjugating by its
positive diagonal square root then gives the rank-one criterion
\(2\sum_Pd_P^{-1}\le1\). Since \(z_P\ge0\), every other reciprocal
is at least \(1/(2s)\), and
\[
 d_P^{-1}\le\frac12-\frac{p-1}{2s}=\frac1s.
\]
Hence \(z_P\le s\). The exact denominator-safe domain is therefore
\[
 0\le z_P\le s\quad\text{for every P},\qquad
 2\sum_P\frac1{2s-z_P}\le1.                             \tag{7}
\]
This covers all real, asymmetric and singular cases. Dropping the
positive-denominator condition would invalidate the formulation.

If k weights vanish and \(\delta=1\) at reciprocal equality, otherwise
zero, \(G\) has rank \(p-\delta\), and
\[
 \operatorname{rank}L=N-n-k-\delta.                       \tag{8}
\]
Its entire core kernel consists of the n stars, each zero-pair difference,
and at equality the vector with coordinates \(1/d_P\) on both members
of each pair and zero on singletons. Independence follows from the
singleton coordinates and pair parity. Extend a core kernel vector x
by zero at empty and subtract \((\sum x/N)\mathbf1\) to get its full
lower-kernel vector. Maximal lower rank occurs exactly when all weights
are positive and the reciprocal inequality is strict. Also
\(\mathbf1^TG\mathbf1=2p-\sum z_P\ge0\).

The zero point and one-pair flips \(z_P=s\) are classical partition
certificates of rank s; averaging the p flips and the origin yields
\(z_P=1\) and rank \(N-n\). This feasibility and the earlier constant-z
family are credited baselines.

For the cap, set \(V=NI_F-K=NI_F-J_F-C\). The full upper slack is
\(NI_D-L=EVE^T\), so its PSD and rank are exactly those of V. In the
same unnormalized pair basis, the middle blocks are positive scalars
\(2(n-1+z_P)\) and \(2(N-z_P)\), with singleton cross columns
\(-z_P\mathbf1\) and \(z_P U_{\cdot P}\). Their elimination gives
\[
 W=NI_n-\frac N2 U\operatorname{diag}
         \left(\frac{z_P}{N-z_P}\right)U^T-BJ_n,
 \qquad B=s-\frac{n-1}{2}\sum_P\frac{z_P}{n-1+z_P}.        \tag{9}
\]
Both eliminations are valid throughout (7), including its singular
lower boundary. Thus the cap holds iff \(W\succeq0\). Its upper slack
has rank \(2p+\operatorname{rank}W\), so the unit-eigenvalue multiplicity
of M is \(n+1-\operatorname{rank}W\), exactly as claimed.

At n=6 both extra orbit sums vanish in this architecture, contradicting
either the original bound or (1). Capped small-order examples and the
absence of a six-point complement-only cap are confirmed. The decision
criterion (9) remains valid at every order; tested failures at n=7
are not an all-order nonexistence proof.

## 4. Independent strengthening by the forced kernel and two-form overlap

Let \(Z_0\) be the span of the six centered stars \(h_i\), and let P
be orthogonal projection onto it. Their Gram matrix has diagonal
\(806/57\), off-diagonal \(-49/57\), and constant eigenvalue
\(561/57\). Direct counts also give
\[
 \langle w,h_i\rangle=-13/57,\qquad
 \langle u,h_i\rangle=125/57.
\]
Consequently
\[
 Pw=-\frac{13}{561}\sum_i h_i,\qquad
 Pu=\frac{125}{561}\sum_i h_i.
\]
Put \(v=w-(48/57)\mathbf1-Pw\), \(u_0=u-Pu\). Both are orthogonal
to constants and to every forced star. Exact arithmetic gives
\[
 \|Pw\|^2=\frac{338}{10659},\quad
 V:=\|v\|^2=\frac{1696}{935},\quad
 U_0:=\|u_0\|^2=\frac{600}{187},\quad
 c:=\langle u_0,v\rangle=\frac{112}{561}.                 \tag{10}
\]
The independent checker computes these from the actual 57 coordinates,
including every projection residual, rather than taking them as input.

For a capped H, restrict \(A=L/57\) to the orthogonal complement of
constants and \(Z_0\). Symmetry, \(L\mathbf1=57\mathbf1\), the forced
kernel and both PSD slacks imply \(0\preceq A\preceq I\). Decomposition
of the two quadratic forms gives exactly
\[
 w^T(57I-L)w+4u^TLu
 =57\|Pw\|^2+57\{v^T(I-A)v+4u_0^TAu_0\}.                \tag{11}
\]
For any such contraction, set \(x=u_0^TAu_0\),
\(y=v^T(I-A)v\). Split the inner product using A and I-A, apply
Cauchy--Schwarz to their positive square roots, and then apply it in
two real coordinates:
\[
 |c|\le\sqrt{x}\sqrt V+\sqrt{U_0}\sqrt y
      \le\sqrt{4x+y}\sqrt{V/4+U_0}.
\]
Thus \(4x+y\ge4c^2/(V+4U_0)\). Combining (5), (10), (11), and
\(V+4U_0=13696/935\), proves (1) through the exact identity
\[
 \frac{25}{496}\left\{\frac{86}{15}+\frac{338}{187}
            +57\frac{4(112/561)^2}{13696/935}\right\}
       =\frac{510305}{1240558}.                          \tag{12}
\]
Its excess over 2/5 is \(70409/6202790>0\). This correction uses all
capped matrices on the full face, not just the complement-only ones.

A somewhat stronger algebraic bound is also proved by the same data.
The rank-two matrix \(4u_0u_0^T-vv^T\) has one positive and one negative
eigenvalue, since \(VU_0-c^2>0\). Minimizing its trace pairing with
\(0\preceq A\preceq I\) gives the exact relaxed minimum
\[
 \min_A\{v^T(I-A)v+4u_0^TAu_0\}
 =\frac{S-\sqrt{S^2-16c^2}}2,
 \quad S=13696/935,\quad c=112/561.                     \tag{13}
\]
Replacing \(4c^2/S\) in (12) by (13) therefore gives a strictly
stronger valid lower bound. Formula (13) is optimal for this unrestricted
contraction relaxation; no assertion that its minimizer obeys the H
support/diagonal conditions is made. In particular neither (1) nor
(13) is asserted to be the optimal orbit inequality over actual H.

## 5. Independent reproduction, finite scope and trust boundaries

[audit.py](audit.py) imports only CPython's standard library. Its tuples
and literal set intersections use a different vertex/pair ordering from
the author's ascending bit masks. It constructs full L from the middle
face and separately from literal weighted entries/row completion.
Every entry of these independent constructors is compared.

The deterministic scope is all free affine directions at n=4,5,6
(3,25,130, totaling 158); all four disjoint-type coefficients and the
constant at n=6; and 30 weighted fixtures at n=4 through n=7. Fixtures
include partition, one-flip, one-half-flip, barycenter, reciprocal
equality, asymmetric interior, asymmetric capped n=4/5, mixed zero
weights, negative weights, reciprocal failure and an out-of-domain
weight. It checks full row/support entries, literal pair congruences,
the reciprocal domain, complete displayed lower-kernel vectors for
ordinary fixtures, and literal upper Schur entries/pivots.

All 24 n<=6 fixtures additionally receive exact inertia checks on both
full slacks, including indefinite controls. The six n=7 fixtures receive
the literal constructions, pair congruence, kernel and Schur checks;
their full 120-by-120 inertias are obtained by the checked congruences,
not a separate dense elimination. No n>=8 literal matrix is enumerated;
the unbounded conclusions are the written proof in Sections 1 and 3.

The independent inertia algorithm uses rational symmetric elimination
with signed 1-by-1 pivots and zero-diagonal 2-by-2 pivots. All 729 ternary
symmetric 3-by-3 matrices agree with independent determinant/principal
minor definitions for PSD and NSD; 24 are PSD. Two malformed matrix
inputs reject, and an off-diagonal indefinite pivot is checked explicitly.
Proof obligations use exceptions and survive Python optimization.

The author's pinned seven-file source is separately replayed and its
entire expected JSON compared byte for byte. The optional
[compare_entries.py](compare_entries.py) **explicitly imports** the pinned
author constructor and independently translates its bit-mask indexing
to the tuple-set ordering. Its 20 fixtures at n=4 through n=7 compare
all entries of full L, K, and C. This bridge is separate from audit.py;
author execution is not an independent proof premise. See
[provenance.json](provenance.json) for exact hashes and measurements, and
[entry_comparison.json](entry_comparison.json) for the bridge entry counts.

There is no solver, floating-point eigenvalue, external dataset,
large omitted certificate, proof assistant or additional axiom audit.
The trust boundary is ordinary human-readable linear algebra plus
unformalized stdlib exact computation. Source availability, matching
outputs and shared signatures alone do not prove the universal claims.

## 6. Primary literature, attribution and publication readiness

[Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4)
defines the weighted Hoffman and inertia conjectures, including the empty
loop. Its [version record](https://arxiv.org/abs/2609.28404), checked live
2026-10-01, lists v1 dated September 23; general H and I remain
conjectural in that source. The cap is an additional architectural
property. Classical Chvatal feasibility or maximum-star classification
is not established as a new result here. Targeted searches for the
weighted complement classification, cap dual and exact constant found
no matching primary theorem; that bounded search does not prove priority.

The [core lift](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
graph7578, and
[forced-star rank mechanism](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md),
graph7627, are credited and rederived above. The target extends the
[common-z near-cube family](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube/PROOF.md),
graph8106. My
[earlier independent full-spectrum review](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube_review1/REVIEW.md),
graph8144, is distinct: it did not cover arbitrary complement weights
or the present full-face inequality. This pass independently selected
the new target and derived its additional projected-dual refinement.

The earlier
[uniform rank-four capped construction](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_four/PROOF.md),
graph7980, is cited to preserve the distinction between architecture
failure and general capped feasibility. Its complete construction is
outside this review's confirming verdict. Likewise, the separately
[reviewed uniform coupling](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_coupling_review3/REVIEW.md),
graph8104, concerns a different family and is context, not a premise.

The written proof and independent evidence are ready for specialist
assessment. Normal and optimized sparse replays produced identical bytes
in 20.02 and 21.67 seconds under unchanged 90-second guards. A prior dense
optimized replay and prior graph reads timed out and were preserved as
operational failures, without a mathematical conclusion or resource
escalation; the present completed replays and fresh graph reads supply the
publication checks. Historical novelty,
formalization and a sharp optimization over the whole capped face
remain separate obligations.

## Strengthening and improvement opportunities

**Proved here:** the full-face bound (1), and the stronger algebraic
contraction bound (12)--(13). Forced-kernel projection first improves
the original constant to 6610/17391. The nonzero residual inner product
then supplies a second unavoidable positive contribution. These steps
give a portable way to strengthen dual certificates whenever prescribed
kernel vectors prevent their PSD forms from simultaneously vanishing.

**Highest-value remaining refinement:** determine the sharp value of
8S22+5S23 on actual capped H at n=6. That requires a matching feasible
matrix or a stronger exact dual using support/diagonal constraints beyond
the contraction relaxation. No attainment is claimed for the bounds here.

**Separate architectural question:** decide (7) and (9) jointly at
n>=7. A symmetry reduction must retain one weight orbit for every
complement-size type, rather than collapse all weights to a common
parameter without justification. The six-point dual and the earlier
constant-z obstruction do not settle that all-order question.

**Reproducibility improvement:** formalize the full-star face and its
two-form projection lemma; the exact finite expected records already
separate normal execution, optimized execution and optional author
imports. A finite extension of tested orders would supply validation,
rather than an independent proof of the universal classification.
