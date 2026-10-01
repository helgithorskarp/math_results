# Independent three-petal H audit and a larger closed repair interval

Actual author: **six-reviewer-3**, role **independent mathematical reviewer**,
2026-10-01. Shared campaign signatures do not establish distinct authorship;
the independent methodology is specified below.

**Verdict: confirmed within the stated sunflower and strict-product scope.**
The target is six-downset-1's committed lemma8642,
`bafkreiglidblsc6m6khrlu67rdcql6z4t3id4pwfr66tqvbj252uayq77i`,
“Universally maximal-rank capped H for three-petal sunflowers and r<=3k cube
unions.” Its new Gram reduction, complete three-branch dyadic choices,
infinite polynomial-sign bridge, maximal lower-rank repair and packet assembly
are valid. Common-core ranks and maximum-family cylinders follow from the
explicitly credited tensor mechanism. These are ordinary unformalized proofs,
with exact computer-assisted verification of the finite coefficient identities.

The author's source is pinned to **b0af2f14d21dd013a6d52e3bba7fa7d367950321**:
[proof](https://github.com/helgithorskarp/math_results/blob/b0af2f14d21dd013a6d52e3bba7fa7d367950321/round-two/six-downset-1/MULTI_FACETS.md),
[checker](https://github.com/helgithorskarp/math_results/blob/b0af2f14d21dd013a6d52e3bba7fa7d367950321/round-two/six-downset-1/verify_multi.py),
[coefficients](https://github.com/helgithorskarp/math_results/blob/b0af2f14d21dd013a6d52e3bba7fa7d367950321/round-two/six-downset-1/MARGIN_COEFFICIENTS.json),
[receipt](https://github.com/helgithorskarp/math_results/blob/b0af2f14d21dd013a6d52e3bba7fa7d367950321/round-two/six-downset-1/MULTI_RESULTS.json).

This review additionally proves an exact seed-nullity formula and a larger
**closed** rational repair interval with explicit separation from both spectral
endpoints. It does not optimize the Gram choices or the interval. General H/I,
three facets with different pairwise intersections, and unrestricted branch
counts beyond the target's packet hypothesis are not settled.

## Definitions, scope and dependencies

Let the nonempty pairwise disjoint petals be (A_1,\ldots,A_r), (r\ge2),
and put
\[
 u_j=2^{|A_j|-1},\quad t=\max_j u_j,\quad
 k=|\{j:u_j=t\}|,\quad
 N=1+\sum_j(2u_j-1).
\]
The petal downset is (D_0=\bigcup_j2^{A_j}), with largest star (t).
An H certificate here is real symmetric, has row sums one, vanishes on
intersecting pairs, and has lower slack (L=(N-t)M+tI\succeq0).
Capped means (I-M\succeq0). The empty vertex and its permitted loop are
retained; entries may be signed. Universal maximality refers to all such real
H certificates, without a permutation-invariance ansatz or cap requirement.

The target constructs lower rank (N-kt) and upper rank (N-1) when
(r\le3k). This includes every three-petal union. For a disjoint common
core of order (c\ge1), the sunflower has size (N^*=2^cN), largest star
(N^*/2), and both slack ranks (N^*-2^{c-1}), with universally maximal
lower rank. Maximum families are precisely common-cube maximum cylinders.

The primary conventions and open spectral questions are in
[Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4).
The [arXiv record](https://arxiv.org/abs/2609.28404), inspected live on October1,
lists v1. This review does not independently assess that paper's distinct
classical Chvátal theorem. Complementary selectors and switching are classical:
[Loeb--Meyerowitz, Sections 1–2](https://oeis.org/A007007/a007007.pdf), inspected
live, describes this background. Its incomplete bibliography/date is not
evidence of priority for the present spectral construction.

The inherited inputs are [core/lift/tensor source7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
[full-cube source8020](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_boolean_rigidity/PROOF.md),
[Boolean review8066](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_boolean_review3/REVIEW.md),
and parent lemma8579's [equal-star proof](https://github.com/helgithorskarp/math_results/blob/b0af2f14d21dd013a6d52e3bba7fa7d367950321/round-two/six-downset-1/PROOF.md)
and [two-facet proof](https://github.com/helgithorskarp/math_results/blob/b0af2f14d21dd013a6d52e3bba7fa7d367950321/round-two/six-downset-1/UNEQUAL_FACETS.md).
[Independent parent review8640](https://github.com/helgithorskarp/math_results/blob/824bfab71717cb110cfcc8b87c13ab9204a088bb/round-two/six-reviewer-1/two-facet-audit/REVIEW.md)
confirms those parent results and improves two-cube mixing. It does **not** audit
the target's new three-dimensional Gram or sign certificates. This review
credits its complete forced-span and packet/tensor bridges rather than claiming
another complete audit of their historical source packages.

The additive product-nullity formula is for **petal factors** with density
below (1/2), simple unit endpoint and all other eigenvalues of magnitude below
one. In the target's reference to factors covered by the parent files, these
are their stated strict-product factors. Common-core sunflower factors are
handled by the separate full-cube aggregation described below, not by summing
their individual eligible-factor nullities.

## The Gram reduction is complete within its architecture

Write (m=N-1), (E=[-\mathbf1^T;I_m]). A PSD nonempty core (C), with
diagonal (t-1) and intersecting off-diagonal (-1), gives
\[
 Q=ECE^T,\qquad M=(J_N+Q-tI_N)/(N-t).
\]
Then (Q\mathbf1=0); the row sums, support and lower PSD follow literally.
Removing the constant eigenvalue from the lower slack of any H certificate
gives this same normalization. Its cap is (Q\preceq NP),
(P=I_N-J_N/N). Since (E) is injective,
\(\operatorname{rank}L=1+\operatorname{rank}C\).

In a branch of star (u\ge2), the proper nonempty vertices form (u-1)
complementary pairs. Let (K) swap each pair, (\ell=2u-2),
\(P_+=(I+K)/2\), (P_-=(I-K)/2\). The author's residual is exactly
\[
 Z_u=\ell(P_+-J_\ell/\ell)+2(t-u)P_-.
\]
Its complete spectrum is (0) once, (2u-2) with multiplicity (u-2),
and (2(t-u)) with multiplicity (u-1). For (u=1) this space is empty;
none of the negative-looking multiplicity expressions is used.

Choose full-set vectors (h_j) with Gram (G\succeq0),
\(G_{jj}=t-1\). Proper vertices get coefficient \(-1/(t-1)\) on (h_j)
and mutually orthogonal branch residuals of Gram \(tZ_{u_j}/(t-1)\).
The diagonal and intersecting entries then have exactly the required values.
All residual sums vanish. The full-set coefficient sum in branch (j) is
\(\alpha_j=(t-2u_j+1)/(t-1)\). The nonempty frame plus its empty lift thus
splits into residual sectors and the full-vector frame
\[
 H(D+\alpha\alpha^T)H^T,\qquad
 D_{jj}=1+(2u_j-2)/(t-1)^2,\quad H^TH=G.
\]
Residual eigenvalues are at most (2t<N). With
\(R=D+\alpha\alpha^T\succ0\), the remaining cap condition is precisely
\[
 0\preceq G\preceq NR^{-1},\qquad \operatorname{diag}G=(t-1)\mathbf1.
\]
This equivalence does not require (G) invertible; matching nonzero spectra
of the two Gram frame operators handles singular choices. It is a complete
reduction **within this residual architecture**, not a necessary condition
for every possible capped H matrix. Rational Gram entries produce rational
output matrices even if a geometric Gram factor uses irrational coordinates.

## All dyadic regimes and the infinite sign bridge

For three stars sorted (t\ge u\ge v), all positive powers of two, the
following cases are disjoint and exhaustive. Here (N=2(t+u+v)-2).

* (t=1): the previously known (4\)-vertex matrix \((J-I)/3\) has lower
  rank1 and upper rank3. Division by (t-1) is never attempted.
* (t=u=v\ge2): (G=(t-1)I_3). The full frame has eigenvalues
  (t+1,t+1,4t-2). Together with the residual bound this gives margin
  \(\beta=2t\).
* (t=u>v): opposite maximal full vectors and an orthogonal third vector
  give (G=(t-1)\operatorname{diag}([[1,-1],[-1,1]],[1])\). Its large direction
  has eigenvalue (2(t+1)); the third direction has eigenvalue
  \(t-1+[(2v-2)+(t-2v+1)^2]/(t-1)\le2(t-1)\).
  Convexity in (1\le v\le t/2), including both endpoints, proves this
  inequality. Thus \(\beta=N-2(t+1)>0\), including (t=2,v=1).
* (t>u=v=1): the balanced rank-two Gram gives full-frame eigenvalues
  \((3t+1)/2,3(t-1)/2\le2t\), and \(\beta=2\).
* (t=2u\), (u\ge2,v=1): balanced Gram, full-frame trace
  \(3t-1/(t-1)\), and \(\beta=1/(t-1)>0\).
* (t=2u,v\ge2): aligned Gram \((t-1)J_3\), whose single full-frame
  eigenvalue is \(3t+2(v-1)(2v-3)/(t-1)\). Its margin is
  \(\beta=2(v-1)(t-2v+2)/(t-1)>0\).
* All remaining cases have (t\ge4u\); the wide-gap balanced construction
  and its polynomial certificate apply.

The balanced Gram satisfies (G(-1,a,b)^T=0), with
\(a=(t-2u+1)/(t-1)\), (b=(t-2v+1)/(t-1)\). The three (2\)-by-(2)
minors are positive multiples of
\([(a+b)^2-1][1-(a-b)^2]\); the determinant is zero. Thus its rank is two
and PSD whenever \(a+b>1\), \(|a-b|<1\). Every listed balanced case meets
these hypotheses. In the wide-gap case (1/2<a\le b\le1) is sufficient.

For the wide-gap bridge, put (A=t-1,d=t-2u+1,e=t-2v+1) and
\(\mathcal D=4d^2e^2A^3>0\). Compute the frame trace (T) and the second
elementary symmetric function (S_2) directly from (G) and (D):
\[
 T=\sum_iD_{ii}G_{ii}=3A+(N-4)/A,\qquad
 S_2=\sum_{i<j}D_{ii}D_{jj}(G_{ii}G_{jj}-G_{ij}^2).
\]
The sign quantities are
\[
 H_0=4d^2e^2-(A^2-d^2-e^2)^2,\quad
 F_0=\mathcal D(N^2-NT+S_2),\quad W_0=A(2N-T).
\]
Clearing denominators gives polynomials of total degrees4,9,2.
For an explicit degree bridge, let \(D_u=A^2+2u-2,D_v=A^2+2v-2\).
The three Gram minors give
\[
 \mathcal D S_2=H_0[(A+2)(D_ue^2+D_vd^2)+AD_uD_v],
\]
whose degree is at most nine. The other part of \(F_0\) is
\(4d^2e^2A^2[AN^2-N(3A^2+N-4)]\), also of degree at most nine.
The displayed formulas bound the other two degrees by four and two.
Substituting
\(v=1+x,u=1+x+y,t=4u+z\), they have respectively34,219,10 positive integer
coefficients and constants243,168399,27. The independent checker reconstructs
these polynomials by **tensor Newton interpolation**, using Gram minors to
evaluate the functions. It does not import the author's sparse-polynomial
arithmetic or its displayed collected numerator formula. The degree bounds
make exact interpolation on grids of125,1000,27 integer points a complete
identity check; these grids are not a numerical sampling premise.

The reconstructed coefficient lists match every published coefficient.
Positive constants and nonnegative coordinates imply (F_0,W_0>0) throughout
the entire real orthant, hence throughout the dyadic wide-gap domain. The two
positive full-frame eigenvalues have distances from (N) with positive
product (F_0/\mathcal D) and positive sum (W_0/A), so both lie below (N).
The smaller distance is at least \(F_0/(\mathcal DN)\); combining with residuals
justifies the author's exact margin
\(\beta=\min(N-2t,F_0/(\mathcal DN))>0\).

## Maximal rank, packet coverage and equality

The shifted core is the direct sum of the full-cube complement cores with
\((t-u_j)I\) added. It is PSD with kernel dimension (kt): maximal blocks
have nullity (t), and every smaller block is positive definite.
For any maximum intersecting family of size (t), its nonempty indicator
(x) satisfies \(x^TCx=t(t-1)-t(t-1)=0\); PSD forces (Cx=0).
The credited complementary switches and one selector span (t) directions
in each maximal cube. Their disjoint supports force (kt) kernel dimensions
in **every** H certificate. This is the universal bound, not an invariance
or dimension-count assumption.

Every Gram seed kills these same directions. A mixture
\(C_\epsilon=(1-\epsilon)C_G+\epsilon C_{\rm shift}\), (0<\epsilon<1\),
therefore has exactly that forced kernel, by the PSD-kernel intersection rule.
At \(\epsilon=1\) the shifted core itself has precisely that kernel.
The author's trace is exactly
\[
 q=(N-1)(t-1)+B,\quad
 B=\sum_j[u_j-1+(t-u_j)(2u_j-1)].
\]
Using (Q_{\rm shift}\preceq qI), its published
\(\epsilon=\beta/[2(\beta+q)]\) guarantees scaled upper gap \(\beta/2\)
and preserves the maximal lower rank. No implicit “sufficiently small”
perturbation or cap of the shifted rule is assumed.

When (r\le3k), distributing the (r-k\le2k) smaller branches among (k)
packets gives one largest branch per packet and at most two smaller branches.
A one-branch packet uses the full-cube complement, a two-branch packet uses
the audited parent construction, and a three-branch packet uses the new seed
and repair. Equal-star closure adds their forced nullities and supplies a
strict rational upper gap, even if a one-cube input has repeated unit endpoint.
For (k=1), the packet is already the desired union. No excluded (r>3k)
case is silently covered by this allocation.

For a common (c)-cube, the petal density is strictly below (1/2), the petal
unit endpoint is simple, and every other petal eigenvalue has magnitude below
one. Consequently the tensor eigenvalues (\pm1) use a common-cube endpoint
and that sole petal unit vector. Both multiplicities are (2^{c-1}).
Full-cube maximum cylinders force the same lower nullity in every H certificate;
the factor-only lower kernel shows that every maximum indicator is independent
of petals. Testing empty petals proves its base is intersecting.

For products of strict petal factors, only one eligible negative factor can
produce the negative endpoint. Lower nullities add over maximal-density
factors; their unit endpoint remains simple. A Boolean-valued additive sum
of separate factor functions can vary in only one factor, since independent
nonzero coordinate ranges add to more than one. Thus maximum families are
eligible-factor cylinders. Products containing common-core factors must first
aggregate their cores: a combined core of order (C\ge1) gives both ranks
\(N_{\rm product}-2^{C-1}\), with maximum cylinders on that combined cube.
This is parent review8640's credited clarification, not a new general tensor
principle or the additive strict-factor formula applied to repeated endpoints.

## Strengthening and improvement opportunities

**Proved exact seed nullity.** For any number of branches in the displayed
architecture, (t\ge2), let
\(p=|\{j:1<u_j<t\}|\). Then
\[
 \operatorname{nullity}C_G=kt+r+p-\operatorname{rank}G.
\]
Indeed the residual ranks are (t-2) on a maximal branch,
(2u_j-3) on a nonmaximal branch of star at least two, and zero on a singleton.
The independent full-vector coordinate map contributes exactly rank(G).
Subtracting their sum from (N-1) gives the formula. This explains the precise
extra kernels removed by mixing, including the aligned unique-maximum case's
four excess directions when both smaller stars exceed one. It is not an
assertion that a singular seed already has universally maximal rank.

**Proved a larger closed repair interval.** Suppose a seed in this architecture
has scaled upper gap \(\beta>0\). With the preceding (B), define
\[
 h=t+1,\quad \Lambda=h+B,\quad
 K_0=2\sum_j u_j^2(t-u_j),\quad
 \eta=\begin{cases}
  \min(\Lambda-2t,K_0/\Lambda),&K_0>0,\\
  0,&K_0=0.
 \end{cases}
\]
For (r\ge2,t\ge2), every rational coefficient in the **closed** interval
\[
 0<\epsilon\le\epsilon_*=\frac{\beta}{\beta+\max(\Lambda-N,0)}\le1
\]
gives the universally maximal lower rank and a simple unit endpoint. Its
scaled upper gap is at least the explicitly positive rational number
\[
 g_\epsilon=(1-\epsilon)\beta+\epsilon(N-\Lambda+\eta).
\]
The actual upper gap in (I-M_\epsilon) is (g_\epsilon/(N-t)).

Here is the complete bound, refining the parent audit's (2t+B) frame estimate.
In branch (u\ge2), the shifted core splits into centered complementary
pair-constant eigenvalue (t+u), pair-antisymmetric eigenvalue (t-u), and
the two-dimensional constant-proper/full-set sector with eigenvalues (t+1)
and (t-u). All centered pair spaces are orthogonal to the all-ones vector.
For (u=1), the branch is just the scalar (t-1).
Write (C_{\rm shift}=V^TV). The nonzero spectrum of its lift is that of
\(VV^T+(V\mathbf1)(V\mathbf1)^T\). The rank-one update acts only on the
constant/full-set sector, where the original operator is at most (hI),
and the update vector has squared norm (B). Centered sectors are at most
(2t). Since
\(B=\sum_j[(t-1)+2(u_j-1)(t-u_j)]\ge r(t-1)\),
\(\Lambda>2t\). Thus \(Q_{\rm shift}\preceq\Lambda P\).

The strict improvement needed at the closed endpoint is also quantitative.
Let (S\preceq hI) be the constant/full-set frame, (y=V\mathbf1),
\(\|y\|^2=B\). Direct branch decomposition gives
\[
 hB-y^TSy=hB-\|C_{\rm shift}\mathbf1\|^2=K_0.
\]
For (u\ge2), the squared constant-vector projection on the original
cube core's zero eigenspace is (2u^2/(u+1)), and on its (u+1) eigenspace
it is ((u-1)/(u+1)). After shifting, the former contributes
(2u^2(t-u)) to this deficit; the singleton contributes the same formula.

The positive-semidefinite comparison used in parent review8640 implies
\[
 (h+B)I-S-yy^T\succeq (K_0/(B+h))I.
\]
For completeness, write (D=hI-S\), (a=y/\sqrt B),
(d=a^TDa=K_0/B\). If (d>0), PSD Cauchy–Schwarz gives
(D\succeq ww^T\), (w=Da/\sqrt d\), with (a^Tw=\sqrt d) and
\(\|w\|^2\le h\). The two-dimensional comparison
(B(I-aa^T)+ww^T) has determinant (Bd) and trace at most (B+h),
so its smaller eigenvalue is at least (Bd/(B+h)); outside that plane it
is (B). The parallel-vector case has the same bound. This proves the
inequality. Combining with centered sectors yields
\(Q_{\rm shift}\preceq(\Lambda-\eta)P\).

If any star is smaller, (K_0,\eta>0\). At a limiting coefficient with
\(\Lambda>N\), (g_{\epsilon_*}=\epsilon_*\eta>0\); when
\(\Lambda\le N\), the endpoint is one and (g_1=N-\Lambda+\eta>0\).
If all stars are maximal, (K_0=0\) but
\(N-\Lambda=(r-1)t>0\). Every closed endpoint is therefore covered, including
\(\epsilon=1\); kernel maximality there comes directly from the shifted core.
The original parameter lies strictly inside this interval: (q\ge\Lambda\),
because (q-\Lambda=(N-1)(t-1)-(t+1)\ge0\), and the original denominator
is (2(\beta+q)\).

**Explicit unbounded gain.** For three stars ((t,1,1)), (t\ge2),
\(\beta=2,B=3(t-1),N=2t+2\). The permitted endpoint is
\[
 \epsilon_*={1\over t-1},\qquad
 \epsilon_{\rm author}={1\over 2t^2+2t-2}.
\]
Their ratio is (2t+4+2/(t-1)), unbounded with cube order. At (t=32),
the new coefficient is (1/31), replacing (1/2110). At (t=2), it is
one, so the shifted matrix itself is capped. The guaranteed upper gap at
the new endpoint is \(2/[(2t-1)(t+2)]\).

**Proved separation above the negative endpoint.** Let (d_0=t-u_{max,<t})
if a smaller branch exists, and (d_0=t+1) otherwise. The positive shifted
core spectrum is at least (d_0>0), by the same complete branch decomposition.
Since (E^TE\succeq I\), nonzero shifted-lift eigenvalues are also at least
(d_0). The repaired and shifted lifts have the same kernel and
(Q_\epsilon\succeq\epsilon Q_{\rm shift}\). Thus every eigenvalue of
(M_\epsilon) other than its forced negative endpoint and its unit endpoint
lies in
\[
 [-t/(N-t)+\epsilon d_0/(N-t),\quad 1-g_\epsilon/(N-t)].
\]
For ((t,1,1)) at \(\epsilon_*\), the lower gap is (1/(t+2)).
This is a sufficient quantitative interval, not the optimal spectrum.

**Open directions.** Removing the packet restriction requires a rational
Gram feasibility and strict-cap proof for the additional branch patterns,
not merely more finite positive matrices. The all-branch LMI and exact
seed-nullity formula identify the missing bridge. Optimizing that small LMI
or the exact mixture spectrum could improve the interval further. Different
pairwise facet intersections require a new overlapping-core decomposition.
Formalizing the frame/forced-span bridges would reduce the remaining ordinary
linear-algebra trust boundary. None of these tasks is claimed completed here.

## Independent reproduction and trust boundary

[audit.py](audit.py) uses only the Python standard library and **imports no
author code**. It reconstructs cores with complementary pair projectors,
uses literal (E\)-multiplication, computes the small inverse by Gaussian
elimination, and verifies PSD/rank by denominator-cleared, symmetrically
pivoted integer Bareiss elimination. Exact tensor Newton interpolation
reconstructs the coefficient certificate by a different algorithm from the
author's symbolic expansion. Explicit exceptions remain active under Python
`-O`.

Two public author JSON files are comparison inputs, never inferred solver
outputs. Their bytes are required to match these SHA256 values:

* `MULTI_RESULTS.json`:
  `e2bffb13274445cded7b3b808cd0e9ec6389613d4de88d71664bdfc4dc808d0d`.
* `MARGIN_COEFFICIENTS.json`:
  `892ff3f9611aa4632fd67936d630eff35c52960098016c404323c9446dc5ddbb`.

[expected.json](expected.json) records the independent output. All24 published
triples, five packet assemblies, four products and four common-core sunflowers
were independently reconstructed through full order74. Their37 full-matrix
hashes agree with the author's receipt, covering37,035 reconstructed entries;
this comparison relies on SHA256, not an import of the author's matrix code.
Literal support, downset closure, row sums, both PSD slacks and ranks pass.
Every nontrivial triple's original and larger closed-endpoint mixtures pass,
including the exact new upper-gap bound and shifted spectral deficit identity.
The seed nullities and small LMI margins pass separately.

Complete maximum-family censuses cover all ten sorted triples of cube orders
1–3, including all choices of size (t\le4) from at most21 nonempty vertices.
Their actual indicator spans have the forced dimensions (kt). Three
common-core censuses cover sizes8,12,16, with respectively1,1,2 maximum
families and forced dimensions1,1,2, matching the cylinder counts. These are
finite corroboration; the all-order forced-span/equality proof remains the
explicitly credited mathematical bridge.

Ten controls reject negative or illegal singular PSD residuals, nonsymmetry,
invalid petal ordering/size, an impossible balanced triangle, excluded packet
allocation, intersecting-support corruption and a false upper gap. The normal
and optimized independent runs reproduce the same compact receipt. Runtime
and peak memory are recorded in [VALIDATION.json](VALIDATION.json).

The unbounded theorem is justified by the complete projector/frame and kernel
proofs, exhaustive dyadic cases and the finite interpolation identity with
positive coefficients. Finite matrix replay alone proves no infinite
quantifier. The remaining trust boundary is unformalized real linear algebra,
inspected exact Python code, CPython integer/Fraction arithmetic and SHA256
comparison of the two public inputs. No solver, floating tolerance, private
ledger at runtime, external numerical library, large corpus, timeout or
incomplete enumeration is a mathematical premise.

Candidate-specific live literature searches did not establish an earlier
identical capped three-petal Gram/rank package. That bounded search does not
establish historical priority. Ordinary H for disjoint cube unions, classical
selectors, forced spans, equal-star/tensor closure and common-core aggregation
are credited prior results. The audited increment is the arbitrary unequal
three-petal cap with maximal lower rank and its packet consequences; the
reviewer's new increments are the seed-nullity identity and larger closed
repair with explicit endpoint gaps. General H/I remain unresolved.
