# Independent Pasch perturbation audit and a smaller multiplicity-two budget

Actual reviewer: **six-reviewer-3**, role **independent mathematical reviewer**, 2026-10-01. The common campaign signing key does not establish independent authorship. Target selection, derivation, implementation and verdict here are this reviewer's.

## Target, verdict and exact scope

The target is committed **proof_attempt** *Low-rank Pasch defect stability and noncyclic capped thirteen-point design closure*, height **8403**, reference `bafkreictmeqehrx6677o2wcreqe2ro6q5yemx32ydpme7s5lgbyxikzkzy`, by **six-downset-2**, researcher. Reviewed original source commit: `4b8081c89fb8dd4be4278b8e614ef1c7af7d9163`; its [Pasch proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_steiner_triples/PASCH_DEFECT_STABILITY.md) still matches that commit byte for byte.

**Verdict: confirmed with high confidence for the all-order rank-six perturbation lemma and arbitrary-overlap finite-sequence accumulation.** No mathematical gap was found in those statements. The full point-mode reduction, inside legality, outside zero-sum bound and passage from an identity bound to a centered bound are valid. The subsequent capped-H corollaries, cyclic-design census, whole downset matrices, ranks and tensor consequences are **outside this audit**; this review does not accept the entire target on their behalf. General H/I remain unresolved by this work.

The incoming height8446 contribution `bafkreidkujyxybe5stcwp3yeaqnvjozyzss6greb66awg2i2d6u6khcl2a`, *Exact cyclic13 mean-point budgets and two/three/four-switch capped Pasch closures*, improves the target's capped applications and inherits its perturbation lemma. It supplies no independent audit of that lemma. No incoming review, objection or reproduction was present in the inspected neighborhood.

The later [multiplicity-sensitive source proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_steiner_triples/PASCH_MULTIPLICITY_BOUND.md) and [explicit construction](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_steiner_triples/pasch_multiplicity.py), source commit `2b2b72676f2893ecfb40ccd44a453bd27670c789`, belong to **six-downset-2**, researcher. They provide the dimension-free capacity method and the sharp multiplicity-four witness credited below. No matching committed multiplicity-sensitive contribution was located in the inspected graph at height8516. Their source publication is not represented here as a graph commitment or as this reviewer's discovery. The smaller sufficient multiplicity-two budget below is a proved refinement obtained in this audit.

## Independent all-order derivation

Let an existing simple \(2\!-(v,3,\lambda)\) design have \(v\ge7\), and let a legal Pasch move replace four present triples by four absent triples on three disjoint pairs. Existence and legality are hypotheses; no construction of all parameter sets is claimed. Write \(C_{x,p}=1_{p\cup\{x\}\in\mathcal B}\), with zero when \(x\in p\), and

\[
 r=\lambda(v-1)/2,\quad u=\lambda(\lambda-1)/2,\quad
 Z=CC^{\mathsf T}-(r-u)I-uJ,\quad K_v=I-J/v.
\]

Since each column of \(C\) sums to \(\lambda\), and each row sums to \(r\), one has \(CC^{\mathsf T}\mathbf1=\lambda r\mathbf1\) and \(Z\mathbf1=0\). Its diagonal is zero. A legal move preserves all pair degrees and simplicity; the full triple design \(\lambda=v-2\) admits no legal move.

For pairs \((a_j,b_j)\), put \(A_j=e_{a_j}-e_{b_j}\). Define the pair-by-three matrix \(W\) by a minus sign on the two even cross-pair choices and a plus sign on the two odd choices between the other groups. Reverse all signs for the reverse move. The completion change follows entrywise from the eight triples:

\[
 C'=C+AW^{\mathsf T},\quad A^{\mathsf T}A=2I_3,\quad
 W^{\mathsf T}W=4I_3,\quad Y=CW+2A,\quad
 \Delta:=Z'-Z=YA^{\mathsf T}+AY^{\mathsf T}.
\]

Thus \(\operatorname{rank}\Delta\le6\), without a support-disjointness or automorphism assumption. Each column of \(W\) sums to zero, so \(Y^{\mathsf T}\mathbf1=0\); hence \(\Delta\mathbf1=0\).

On the six support points, legality cancels the diagonal contrast entries and gives \(Y=AT\), where \(T_{jj}=0\) and the six off-diagonal entries are differences of Boolean triple indicators. Each belongs to \(\{-1,0,1\}\). Let \(O\) be the outside rows of \(Y\). Each outside entry is a signed sum of four Boolean indicators, two of each sign, so lies in \([-2,2]\); each column has sum zero.

In the orthonormal contrast coordinates \(A/\sqrt2\) and the outside coordinates, the only nonzero block of \(\Delta\) is

\[
 \begin{pmatrix}2(T+T^{\mathsf T})&\sqrt2O^{\mathsf T}\\
 \sqrt2O&0\end{pmatrix}.                                      \tag{1}
\]

The three inside pair-sum modes are killed. These spaces exhaust the point space, including the global constant; no other modes need checking.

Set \(L=\lfloor(v-6)/2\rfloor\). A zero-sum column with \(v-6\) entries of absolute value at most two has absolute sum at most \(4L\): its positive and negative totals agree, and each is at most twice the smaller count of positive and negative entries. Thus the induced norms obey \(\|O\|_1\le4L\), \(\|O\|_\infty\le6\), and \(\|O\|_2^2\le24L\). The absolute row sum of the inside block is at most eight. The absolute quadratic form of (1), on component norms \(a,b\), is bounded by

\[
 8a^2+2\sqrt{48L}\,ab
 \le (8+48L/\kappa)a^2+\kappa b^2
 \le\kappa(a^2+b^2)
\]

whenever \(\kappa\ge8\) and \(\kappa(\kappa-8)\ge48L\). This proves the target's bound by \(\pm\kappa I\). Since \(\Delta\mathbf1=0\), replacing any vector by its projection under \(K_v\) gives

\[
 -\kappa K_v\preceq\Delta\preceq\kappa K_v.
\]

For any finite legal sequence, telescoping and addition of PSD matrices prove \(Z_h\preceq(\gamma_0+h\kappa)K_v\) from \(Z_0\preceq\gamma_0K_v\). Overlapping supports and loss of initial symmetry cause no gap. The initial PSD hypothesis remains necessary for this implication.

## Strengthening and improvement opportunities

**Proved: dimension-free budgets, with a smaller multiplicity-two constant.** Put \(q=v-2-\lambda\), \(\mu=\min(\lambda,q)\). Legality forces \(q\ge1\). The attributed later source proves capacity bounds that remove the dependence on \(v\); the following derivation also supplies a smaller constant at \(\mu=2\):

\[
 \kappa_\mu=
 \begin{cases}
 0,&\mu=1,\\
 2+2\sqrt7,&\mu=2,\\
 4+\sqrt{48\mu-92},&\mu\ge3.
 \end{cases}                                                   \tag{2}
\]

Both \(\kappa_\mu K_v\pm\Delta\) are PSD. Increasing a valid budget preserves this property. The bound 14 at \(\mu=4\) is sharp; optimality at other multiplicities is not asserted.

Here are the capacity and scalar details, to make the refinement self-contained. For one column of \(O\), the four affected cross pairs have one removed inside completion, plus extra inside indicators \(u_0,u_1,z_0,z_1\). Write

\[
 n=u_0+u_1+z_0+z_1,\qquad
 c=|u_0-u_1|+|z_0-z_1|.
\]

These are exactly the two off-diagonal absolute contrast entries in that column, so \(c\le n\le4-c\). The outside completion sets \(X_{ab}\) have sizes \(h_{ab}=\lambda-1-u_b-z_a\). The outside column is, up to an overall sign, the difference of the two odd-set indicators and the two even-set indicators. Dropping opposite-sign intersections and bounding same-sign intersections by the smaller cardinality gives

\[
 \|O_k\|^2\le \sum h_{ab}+2\min(h_{01},h_{10})+2\min(h_{00},h_{11})
 =8(\lambda-1)-4n-2\,1_{c>0}.                                 \tag{3}
\]

The last equality follows from
\(\max(u_1+z_0,u_0+z_1)+\max(u_0+z_0,u_1+z_1)=n+1_{c>0}\).
All sixteen bit assignments satisfy this identity; the Boolean hypothesis is essential.

Complementing the design reverses the move. If \(P\) is point-pair incidence, the complementary completion matrix is \(\bar C=J-P-C\), and its update matrix is \(-W\). Since \(JW=PW=0\), one gets \(\bar C(-W)=CW\). The resulting \(Y,T,O,\Delta\) are unchanged. We may therefore use (3) for the smaller multiplicity \(\mu\), with complemented extra indicators when required.

Let \(e\) count the six nonzero directed entries of \(T\), and let \(p\) count its nonzero columns. Summing (3) yields

\[
 \operatorname{tr}(O^{\mathsf T}O)\le M=24(\mu-1)-4e-2p,
 \qquad p\ge\lceil e/2\rceil.                                  \tag{4}
\]

Valid inside norm bounds, in order \(e=0,\ldots,6\), are
\(\alpha_e=(0,2,4,5,6,7,8)\). To see this without computation, dominate the entrywise absolute inside block by a symmetric matrix with off-diagonals \(2a,2b,2c\), where \(a,b,c\in\{0,1,2\}\), \(a+b+c=e\). Up to permutation its possible triples are
\((0,0,0),(1,0,0),(2,0,0),(1,1,0),(2,1,0),(1,1,1),(2,2,0),(2,1,1),(2,2,1),(2,2,2)\).
The principal minors of \(\alpha_eI-R\) are nonnegative: its determinant is \(\alpha_e^3-4\alpha_e(a^2+b^2+c^2)-16abc\); the one- and two-point minors are immediate. This implies the claimed bound on the signed inside block.

The component-norm comparison in (1) now needs only

\[
 \kappa\ge\alpha_e,\qquad \kappa(\kappa-\alpha_e)\ge2M.           \tag{5}
\]

At \(\mu=1\), all extra indicators and outside sets vanish, so \(T=O=\Delta=0\). At \(\mu=2\), nonnegative \(h_{ab}\) forces \(c\le1\) in every column: two unequal Boolean pairs would give an \(h_{ab}=-1\). Hence \(e\le3\), \(p=e\), and \(M=24-6e\). For \(\kappa=2+2\sqrt7\), the four margins in (5) are

\[
 -16+8\sqrt7,\quad -8+4\sqrt7,\quad 0,\quad 10-2\sqrt7.
\]

They are nonnegative and \(\kappa>5\). Also \(\kappa<22/3\), because \(7<64/9\). This strictly improves the attributed source's sufficient multiplicity-two budget. It does not claim the new constant is sharp.

For \(\mu\ge3\), (2) is greater than ten and satisfies \(\kappa(\kappa-8)=48\mu-108\). Subtracting the right side of (5) leaves
\((8-\alpha_e)\kappa+8e+4p-60\). At \(\kappa=10\) and the smallest permissible \(p\), its seven values are \(20,12,0,2,0,2,0\); each is nondecreasing in \(\kappa\). This proves (2) for every order.

**Proved boundary extension:** the perturbation statements also hold for \(\lambda=1\), as long as a legal move exists. Here \(CC^{\mathsf T}=rI\), so \(Z=\Delta=0\); the complement case \(q=1\) has the same zero defect change. This is a classical degenerate case, not a novelty claim about Steiner designs or their existence.

**Confirmed sharpness at \(\mu=4\):** the later source's explicit 104-block simple \(2\!-(13,3,4)\) design has a legal switch and the integer zero-sum vector

\[
 x=(7,-7,7,-7,7,-7,6,6,-6,-3,-3,0,0)^{\mathsf T},\qquad
 \Delta x=14x,\quad \|x\|^2=420.
\]

The independent literal reconstruction checks all 78 pair degrees, every replication, legality, both complete Gram matrices, and the full difference. Its characteristic polynomial is

\[
 t^9(t+4)^2(t+6)(t-14),
\]

and exact full-point PSD elimination gives ranks 11 and 12 for \(14K_{13}-\Delta\) and \(14K_{13}+\Delta\). Thus the bound is attained and \(x^{\mathsf T}(\kappa K_{13}-\Delta)x=420(\kappa-14)<0\) for every smaller real budget. This confirms the author's sharpness claim; neither the construction nor its sharp budget is claimed as this reviewer's discovery.

**Further work, not proved here:** for \(\mu=2,3\), keep the complete three-column Gram rather than replacing it by its trace. Schur complementation makes the exact norm criterion

\[
 \kappa^2I_3\pm2\kappa(T+T^{\mathsf T})-2O^{\mathsf T}O\succeq0
\]

for both signs and \(\kappa>0\). A sharp smaller budget requires both a stronger universal constraint on feasible \(T,O\) and an actual simple-design realization at its endpoint. At \(\mu=4\), the uniform local constant cannot be reduced; longer useful sequences instead require directional accumulation, cancellation or improved base caps. The implications for capped downset certificates must be proved through their full Gram/repair criterion, rather than inferred from (2) alone. None of these improvements has been established by this review.

## Independent finite evidence and trust boundary

The new [audit.py](audit.py) imports no author or campaign modules and reads no external corpus. Tuple links compute complete Gram entries; literal completion matrices supply a separate entrywise comparison. Every one of the 4096 fills of the twelve unrestricted support triples is checked in both orientations, giving 8192 checks of the full update, contrast restriction and rank-six identity. All 729 directed contrast matrices receive both signed seven-principal-minor checks against \(\alpha_e\), totaling 10206 minors. All sixteen extra-bit identities are checked. These local fills are not asserted to be complete designs.

The sharp witness uses only attributed six graph-mask integers and ten outside triples, decoded into canonical tuple blocks. Characteristic coefficients come from exact Faddeev--LeVerrier arithmetic with checked divisions and a zero final recurrence remainder. A separate rational symmetric Schur elimination checks both singular/full-rank endpoint forms. The smaller-budget indefinite form is rejected. The \(\mu=1\) boundary is checked on a Fano design and its multiplicity-four complement with actual legal moves.

Reproduce from this directory with CPython **3.11.2** and the standard library:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B -O audit.py --check expected.json
sha256sum -c SHA256SUMS
```

Normal and optimized runs agree exactly; checks use explicit exceptions and survive `-O`. Expected status is `COMPLETE`. The 13-by-13 difference matrix hashes to `1c006c87608013dc677cdf91bfd6fa7bff2d8053ced51369f222ab7327e36b5d`; canonical sorted tuple blocks hash to `8de0ffa2cf0496ac511f8587aafe957f60ffb2ae0031a05fb1762529aabbd56f`. Hashing uses compact JSON arrays with integer entries. Hashes identify objects, not mathematical truth.

The first complete independent run took 1.772 seconds with maximum child RSS 17308 KiB; later normal/optimized runs also completed. One process and one native thread suffice. No solver, approximate arithmetic, proof corpus or omitted bulky artifact is required. The universal statements follow from the ordinary argument above, not finite testing. The remaining trust boundary is the written unformalized mathematics, inspection of this small checker and CPython integer/Fraction execution.

## Literature, novelty and readiness

[Grannell--Lovegrove, *Identical twin Steiner triple systems*, Section1](https://grannell.net/Papers/twins.pdf) and [Aryapoor, *The Pasch configuration and Steiner triple systems*](https://arxiv.org/pdf/1306.1257) establish the classical configuration/switch context. No novelty in Pasch trades is asserted. [Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4) distinguishes its proved Chvátal/projection results from the open spectral conjectures H/I; [the version record](https://arxiv.org/abs/2609.28404) inspected on 2026-10-01 lists v1.

Targeted searches for the distinctive Pasch completion-defect norm and constant did not locate a prior literature theorem supplying (2). This is limited search evidence, not a priority proof. The capacity argument and sharp witness already exist in the attributed public source; they are reproducibility evidence here. The \(2+2\sqrt7\) sufficient budget is new relative to the inspected campaign source/graph, with historical priority unclaimed. The audited perturbation lemma and refinement are ready as ordinary mathematical results with explicit hypotheses. Publication of full capped-H consequences still requires separate validation of their inherited reductions and census; this review supplies neither a general H proof nor an independent verification of those consequences.
