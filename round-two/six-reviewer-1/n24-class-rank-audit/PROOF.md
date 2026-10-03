# Independent order-24 audit and an original spectral stability box

Actual author **six-reviewer-1**, role **independent mathematical reviewer**,
2026-10-03. Target: committed LEMMA10080/0 by six-downset-2/researcher.
The defining rational coordinates are attributed in [WITNESS.json](WITNESS.json).
This is independent verification of a proposed witness, not discovery of it.
All ordinary real-linear-algebra and harmonic bridges below are unformalized.

## 1. Original matrices and the all-real count bound

Let \(\mathcal D=\{A\subseteq[24]:|A|\le22\}\), including the empty vertex.
Put \(N=16777191\), \(s=8388584\), \(h=N-s=8388607\), and \(r=N-2s=23\).
An ordinary H matrix is real symmetric, \(M\mathbf1=\mathbf1\),
\(M_{AB}=0\) whenever \(A\cap B\ne\varnothing\), and
\(L=sI+hM\succeq0\). A cap additionally requires \(L\preceq NI\).
No sign restriction is imposed on supported entries. Noncentral classes are
the ten sizes 2 through 11; size 12 is not counted. Class a is present if
some original complementary pair has \(L_{A,A^c}<s\).

Every nonempty diagonal is s. PSD gives \(L_{A,A^c}\le s\), so an absent
class saturates every pair in it. Since \(L\mathbf1=N\mathbf1\),
\(L-J_N\succeq0\). Saturation therefore kills \(e_A-e_{A^c}\) in L.
For every other nonempty X, at least one of A and its complement intersects X;
the corresponding cross entry is zero, and equality of the two columns
makes the other zero. A saturated pair has only its diagonal, complementary
partner and empty vertex as potentially nonzero couplings. Its row sum
forces \(L_{\varnothing,A}=L_{\varnothing,A^c}=r\).

For q saturated unordered pairs, write \(\lambda=L_{\varnothing,\varnothing}\).
Restrict the lower and upper forms to the empty indicator and their pair
sums. The basis is not normalized; its Gram matrix is diag(1,2,...,2).
The forms are
\[
 \begin{pmatrix}\lambda&2r\mathbf1^T\\2r\mathbf1&4sI_q\end{pmatrix},\qquad
 \begin{pmatrix}N-\lambda&-2r\mathbf1^T\\-2r\mathbf1&2rI_q\end{pmatrix}.
\]
Their Schur complements give \(\lambda\ge qr^2/s\) and
\(N-\lambda\ge2qr\); thus \(q\le s/r\), or \(q\le364721\).
This is the credited9942 argument, reconstructed here rather than a
transported review verdict. The cap is essential in this step.

Four present classes leave at least six absent, hence
\(q\ge\sum_{a=2}^7\binom{24}a=536130>364721\). Five present leave five absent;
the least possible population is
\(q_0=\sum_{a=2}^6\binom{24}a=190026\).
Any other five-element absent set has population at least
\(\sum_{a=2}^5\binom{24}a+\binom{24}7=401534>364721\).
Thus at least five classes are needed, and their absent set must be2..6.
All1024 class subsets are checked as exact arithmetic, not as matrix enumeration.

## 2. Rank and invariant-face completeness

The star indicator \(w_i\) has s entries. Intersection support gives
\(w_i^TLw_i=s^2\); centering gives the zero-energy vector
\(v_i=w_i-(s/N)\mathbf1\), so \(Lv_i=0\) and \(Lw_i=s\mathbf1\).
The 24 centered stars are independent: evaluation at empty first gives
the sum of coefficients zero, then evaluation at singleton i gives its
coefficient zero. All saturated pair differences vanish at empty and
singletons; their supports are disjoint. They are independent of one
another and the stars. Consequently \(\operatorname{rank}L\le N-24-q\).
At five classes this is16587141. Equality forces exactly these190050
kernel dimensions and excludes any additional saturated pair, including middle12.
The same ceiling holds for uncapped ordinary H in the prescribed saturated face.
These necessary mechanisms were already established in10030; the new target
and this audit supply the independent n24 attainment verification.

Permutation averaging preserves both PSD inequalities, all original support
and row equations. Nonnegative deficits show it preserves exactly the
absent/present classes. Saturated classes2..6 have no proper nonempty
couplings. Therefore the complete invariant face has six complement
deficits d7..d12 and thirty proper disjoint coefficients t(a,b), with
7<=a<=b<=17 and a+b<24. All remaining singleton coefficients are forced
by the full original excluding-point equations
\[
 \sum_{b=1}^{22}\binom{23-a}{b-1}B_{ab}=s.
\]
The fresh decoder solves this full22-variable system, without centering or
numerical SDP. The coordinates in [WITNESS.json](WITNESS.json) are the
target's original36 rational inputs. They impose no rationality,
invariance or sign restriction on competitors in the count or rank bounds.

## 3. Actual empty completion and all physical degrees

For nonempty A,B set
\(C_{AB}=s\mathbf1_{A=B}-1+B_{|A|,|B|}\mathbf1_{A\cap B=\varnothing}\).
With \(E=[-\mathbf1^T;I]\), set \(L=J_N+ECE^T\).
The actual empty row is also reconstructed independently from the original
row sums:
\[
 L_{\varnothing,A}=N-s-\sum_b\binom{24-|A|}bB_{|A|,b},\qquad
 L_{\varnothing,\varnothing}=N-\sum_a\binom{24}aL_{\varnothing,a}.
\]
Every size row, every excluding-point star equation and the actual empty
star are checked. The loop is2238275691119621/4468750000; its 22 cross
entries are regenerated, not accepted from the native expected record.
E has full column rank and range1-perp. Consequently lower PSD and rank
are equivalent to those of C, with rankL=1+rankC. The identity
\(NI-L=E(NI_F-J_F-C)E^T\) retains the empty row and loop.

For completeness we reconstruct the classical harmonic bridge credited to9639.
Let R add a point by summation, and let D be its adjoint. Direct counting gives
\(DR-RD=(24-2a)I\) on layer a. Thus R is injective below the middle, and
the degree-j harmonic kernel has dimension
\(m_j=\binom{24}j-\binom{24}{j-1}\). For a harmonic f on j-subsets,
\(f_a(A)=\sum_{S\subseteq A,|S|=j}f(S)\). The commutator induction gives
\(DR^tf=t(24-2j-t+1)R^{t-1}f\), whence
\(\|f_a\|^2=\binom{24-2j}{a-j}\|f\|^2\).
Lowering proves different degrees orthogonal; the dimension telescope
\(\sum_{j\le\min(a,24-a)}m_j=\binom{24}a\) exhausts every retained layer.
Disjoint action is
\[
 \sum_{B\cap A=\varnothing,|B|=b} f_b(B)
 =(-1)^j\binom{24-a-j}{b-j}f_a(A).
\]
Expand exclusion over j points; every lower-degree term vanishes by repeated
harmonic lowering. Therefore on
\(I_j=\{\max(1,j),...,\min(22,24-j)\}\), j=0..12,
\[
 K_j[a,b]=s\mathbf1_{a=b}-\mathbf1_{j=0}\binom{24}b
            +(-1)^j B_{ab}\binom{24-a-j}{b-j},\quad
 G_j=\operatorname{diag}\binom{24-2j}{a-j},\quad H_j=G_jK_j.
\]
Every H_j is checked symmetric. Multiplicities exhaust N-1; no degree,
mean direction or highest middle parity is dropped.

The fresh representation uses inverse empty-coordinate congruence.
For j=0 write b_a=binom(24,a) and P=I+1b^T. An original mean vector
with layer values z has empty coefficient -b^Tz, metric diag(b)+bb^T,
and E^T image y=Pz. Since \(P^{-1}=I-\mathbf1b^T/N\), its TRUE original
Euclidean metric in y coordinates is
\[
 R_0=(P^{-1})^T(\operatorname{diag}b+bb^T)P^{-1}
     =\operatorname{diag}b-bb^T/N.
\]
For j>0 use R_j=G_j. The original upper forms in these coordinates are
\(V_j=NR_j-H_j\). This avoids treating a physical degree-zero norm as
the original norm. [literal.py](literal.py) separately builds all247
original n8 vertices, all61009 lifted upper entries and all1976 original
point-star rows; actual centered layer indicators check the mean metric
including their empty coordinates. Definition-level pair-difference
harmonics check every entry of all five n8 physical energy blocks. This is
a convention control, not an n8 feasibility theorem or vertex enumeration at n24.

## 4. Exact certificate and a proved two-endpoint spectral gap

Known physical lower kernels are (a)_a at j=0, (1)_a at j=1, and
\(e_a-(-1)^je_{24-a}\) for each saturated class2..6 in I_j.
Their independent counts are(6,6,5,4,3,2,1,0,0,0,0,0,0).
The checker verifies every complete H_j kernel identity and exact
independence; it finds complementary coordinate planes by elimination
on the kernel vectors. Exact diagonal-pivot completion of squares
checks all full lower and upper forms and their ranks. This is a fresh
implementation and representation; completion of squares is not claimed
a new mathematical PSD algorithm.

Put \(\epsilon=10^{-8}\). On each chosen complementary lower plane
the checker proves \(H_j\succ\epsilon R_j\); on the COMPLETE upper
space it proves \(V_j\succ\epsilon R_j\). The prescribed lower nullity
is190050, hence original rank16587141 and upper rankN-1=16777190.
All six active deficits are positive, proving the target's count/rank attainment.

Here is the additional ordinary bridge needed for an ORIGINAL lower gap.
For a vector x orthogonal to the full prescribed kernel, write x=k+u,
where k is in the kernel and u is the representative on the retained plane.
Then \(x^TLx=u^TLu\ge\epsilon\|u\|^2\ge\epsilon\|x\|^2\), because
\(\|u\|^2=\|x\|^2+\|k\|^2\). The argument uses the actual metric R_j,
not an arbitrary core norm. It applies to each orthogonal harmonic copy,
and the remaining constant direction has eigenvalue N. Thus
\[
 \operatorname{spec}(L)\subseteq\{0,N\}\cup[\epsilon,N-\epsilon].
\]
Zero has multiplicity190050, N has multiplicity1, and the16587140 other
eigenvalues occupy the displayed interval. Equivalently all nonendpoint
eigenvalues of M lie in
\([-s/h+1/838860700000000,\,1-1/838860700000000]\).
The extremal eigenvalue -s/h has exactly190050 copies. The original
Hoffman value is s and the unit eigenvalue is simple. No gap optimality
is asserted. A retained-plane floor alone is not advertised as a full
orthogonal spectral floor; this explicit representative argument supplies
the missing implication.

## 5. A quantified closed36-dimensional stability box

Independently perturb each of the36 defining real coordinates by at most
\[
 \delta=\epsilon/2^{93}=1/990352031428304219919299379200000000.
\]
Keep all zeros and saturated complement entries fixed and decode the
singleton/empty entries by the same original equations. The face is
affine and injective in these36 coordinates.

Every nonsingleton coefficient changes by at most delta. The excluding-point
equation at a>=2 gives singleton change at most \(2^{21}\delta\);
the equation at a=1 gives B11 change at most \(2^{43}\delta\).
For any nonempty size a, the row-sum decoder therefore bounds the empty
cross change by \(2^{66}\delta\). The empty loop changes by at most
\(2^{90}\delta\). The entire empty absolute row sum is at most
\(2^{91}\delta\); every nonempty absolute row sum is at most
\(2^{67}\delta\). Symmetry gives
\(\|\Delta L\|_2\le\|\Delta L\|_\infty\le2^{91}\delta=\epsilon/4\).
These are sums over ALL original vertices, using binomial population bounds,
not a sampled support or numerical estimate.

The 24 centered stars and190026 pair differences remain killed exactly,
and the constant direction remains eigenvalue N. On their fixed orthogonal
complement the spectral bounds of Section4 and the norm inequality give
\[
 (3\epsilon/4)I\preceq L\preceq(N-3\epsilon/4)I.
\]
Every active deficit stays positive (the smallest baseline exceeds1/2,
whereas delta<1/2). Thus EVERY point of this closed independent-coordinate
box, including every boundary choice, is an original capped H with exactly
five present noncentral classes, sharp rank16587141 and a simple unit
eigenvalue. Its nonendpoint M eigenvalues remain at least
3/(3355442800000000) from BOTH extremal endpoints. This is a quantified
new-order family, not a classification of all five-class caps, optimized
radius, all-order attainment or settlement of H/I.

## 6. Trust and prior-art boundary

The count, star/saturated-kernel and harmonic/lift mechanisms retain
9942,10030,9639,9365 and7578 credit. Existing10008/10030 n12/16 certificates
do not supply n24 feasibility. Existing9556 already proves unrestricted
n24 cap existence/rank; that is not the novelty here. The new finite
attainment, fresh original-metric reconstruction, full two-endpoint gap
and explicit36-coordinate box are the scoped conclusions.

Written target and prior proofs and the mathematical certificate inputs
were exposed before coding: NOTBLIND. Author executable/expected records
are not used in this primary calculation; source seals precede any native
corroboration. Exact CPython/Fraction implementation and all ordinary
linear-algebra, real harmonic, rank, support and continuity arguments
remain unformalized trust boundaries. Generated complete records remain
in explicitly requested scratch directories, with compact source/expected
hashes sufficient for cold regeneration.

The primary problem is proposed spectral Conjecture H in
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
The [version history](https://arxiv.org/abs/2609.28404) was rechecked2026-10-03.
This fixed-order capped result does not prove either spectral conjecture;
the paper's classical Chvatal theorem supplies no matrix used here.
Candidate-specific searches establish no historical priority claim.
