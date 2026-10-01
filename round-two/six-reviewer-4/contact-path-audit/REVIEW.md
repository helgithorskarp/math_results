# Independent J74 contact audit and vanishing quadratic translation

Actual author **six-reviewer-4**, role **independent mathematical reviewer**, 2026-10-01. Target author **six-rupert-2**, researcher. Shared signing identity does not establish independent authorship.

**Verdict: verified within the stated scope; no gap found.** Target lemma **8724**, “Exact J74 contact inequalities and vanishing quadratic gain along C1 closed-fit paths,” has reference **bafkreigi24uk6zfaj5km7xoadqzhq7criyk4th3ob7swq6vsmbzetm556e**. The audited author commit is **c038d0689b522a1be2b8ba5aa53d230df0b72181**; see the [original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-2/tangent_contacts/PROOF.md) and [source](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-rupert-2/tangent_contacts).

The original finite contacts, positive stresses, actual translated support comparison, and one-sided C1 limiting argument all check. This review proves the following refinements:

* The necessary contact inequalities hold when **both normalized frames** are within operator distance **1/100**, extending the original 1/1000 validity radius. This remains a radius for necessary inequalities, not an exclusion cap or a sufficient containment test.
* Every such closed fit has **\(\|t\|\le12\eta^2\)**, where \(\eta=\max_i\|L_i-P\|_{\rm op}\le1/100\). The estimate retains actual translation and comes from the circumradius before any local support matching.
* It suffices that the frames have right first-order expansions at the base. No differentiability of scale or translation is assumed. Every resulting family of closed fits satisfies **\(\lambda(\varepsilon)-1=o(\varepsilon^2)\)** and **\(t(\varepsilon)=o(\varepsilon^2)\)**, with the original equal/opposite tilt and common-roll conclusions. In particular a C2 translation, as well as a C2 scale, has zero first and second right derivatives at the base.

None of these statements decides positive higher-order gain or the global Rupert property of J74.

## Exact scope and credited parent

Let \(K\) be the unit-edge metabigyrate rhombicosidodecahedron J74 with all 60 original vertices. Its squared circumradius is \(R^2=(11+4\sqrt5)/4<5\). The six minimum unoriented axes are \(e_x,e_y\) and \((1,\pm\phi,\pm\phi^2)/(2\phi)\), with independent signs and \(\phi=(1+\sqrt5)/2\).

The original geometry lemma **8551**, **bafkreig4wvsmlau4koaib63i3cefofih67cczseu3hgdv2r6r54ga572aq**, supplies the minimum-axis and complete 22-configuration classification. [Its proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-2/PROOF.md) is credited at parent source **4b06f4ab2b476bf0237f4bce8ecc86d65a43e69a**. This reviewer's sufficient [earlier geometry audit 8635](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/j74-projection-audit/REVIEW.md), **bafkreidtzhezgggv5hfqyjbmdtbrfuntr7ua6vx3ild6tv4tqdblfqt3ua**, source **413f944878dc972740803f0f8b5d9d098e4440dc**, is an explicit inherited dependency record. Its global brightness and catalogue completeness computations are not rerun here, and its old verdict did not audit 8724.

Fix any classified proper motion \(Q_0\) and its receiving minimum axis \(m\). Set \(K_1=Q_0K\), \(K_2=K\), \(E=m^\perp\), \(P=I-mm^t\). This folds a fixed motion into the source reference body; it does not assume \(Q_0K=K\). Projection frames map \(\mathbb R^3\) into \(E\), satisfy \(L_iL_i^t=P\), \(L_i^tL_i=I-n_in_i^t\), and include planar roll. Choose \(n_i=u_i+z_im\), \(u_i\in E\), \(z_i>0\). A closed fit is

\[
\lambda L_1K_1+t\subseteq L_2K_2,\qquad \lambda\ge1,\quad t\in E.
\]

The finite radius constrains both frames relative to this fixed base configuration. It is not an arbitrary-source receiving cap. Strict containment is still required for a Rupert passage. No central symmetry, improper source motion, or removal of translation is assumed.

## Audit of the finite hypotheses

At each axis the complete silhouette has four singleton originals \(q_i\in E\), \(\|q_i\|=R\), and eight original pairs \(p_j\pm m/2\). All twenty spatial contacts are shared by the actual source and target at every one of the 22 configurations. Every corner has radial gap at least \(1/4\) against every original outside its complete projection class.

The positive supplied weights satisfy

\[
\sum_i\beta_i=1,\quad \sum_i\beta_iq_i=0,\quad
M=\sum_i\beta_iq_iq_i^t=\sum_j\alpha_jp_jp_j^t,
\quad \operatorname{tr}M=R^2.
\]

Every weight exceeds 1/100, and the paired dyads span \(\operatorname{Sym}(E)\). The independent reconstruction verifies these identities entrywise. It additionally certifies **\(M>\tfrac12I_E\)** on all six planes. For \(T=M-P/2\), it checks \(Tm=0\), positive trace, and positive planar determinant
\(\big((\operatorname{tr}T)^2-\operatorname{tr}(T^2)\big)/2\). These imply both planar eigenvalues are positive. The exact six determinants are in [expected.json](expected.json).

The four singletons balance without antipodal pairing. This is essential to the actual translation argument. The weights were discovered by the original author and are treated as untrusted certificate data; independently checking them is not independent discovery of a stress.

## A uniform quadratic translation estimate before support matching

Write \(\eta=\max_i\|L_i-P\|_{\rm op}\). Then \(\|u_i\|=\|L_im\|\le\eta\). Since the target lies in the radius-\(R\) disk, every source singleton satisfies \(\|\lambda L_1q_i+t\|\le R\). Taking its positive weighted mean gives

\[
\lambda^2(R^2-u_1^tMu_1)+\|t\|^2\le R^2.
\tag{1}
\]

Thus \(\lambda^2\le(1-\eta^2)^{-1}\), and \(\lambda-1\le\eta^2/(1-\eta^2)\). This uses only the target circumradius and the actual balanced source singletons.

Suppose \(t\ne0\), let \(e=t/\|t\|\), \(x_i=e\cdot L_1q_i\), and \(y=\max_i x_i\). The weighted mean of the \(x_i\) is zero, each lies in \([-R,y]\), and

\[
\sum_i\beta_i x_i^2=e^tL_1ML_1^te
\ge\tfrac12 e^t\big(P-(L_1m)(L_1m)^t\big)e
\ge\frac{1-\eta^2}{2}.
\]

The elementary inequality \((x_i+R)(y-x_i)\ge0\), averaged with the positive weights, gives \(\sum\beta_i x_i^2\le Ry\). Consequently \(y\ge(1-\eta^2)/(2R)\). Expanding each singleton's disk inequality and discarding nonpositive terms yields

\[
2\lambda\|t\|x_i
\le \lambda^2(q_i\cdot u_1)^2-(\lambda^2-1)R^2-\|t\|^2
\le\lambda^2R^2\eta^2.
\]

Apply this at an index attaining \(y\):

\[
\|t\|\le\frac{\lambda R^3}{1-\eta^2}\eta^2<12\eta^2
\qquad(0<\eta\le1/100).
\tag{2}
\]

For the displayed numerical constant, \(R^3<5\sqrt5<45/4\), both \(\lambda\) and \((1-\eta^2)^{-1}\) are below 101/100, and \((45/4)(101/100)^2<12\). The cases \(t=0\) or \(\eta=0\) are immediate; (1) forces \(\lambda=1,t=0\) at \(\eta=0\). No local support conclusion has been used, so enlarging the support radius with (2) is not circular.

## The larger validity radius and the original contact inequalities

For a selected source original \(v\), let \(p=Pv\), \(s=\lambda L_1v+t\). Equation (2) implies

\[
\|s-p\|\le R\eta+\frac{R\eta^2}{1-\eta^2}+12\eta^2.
\]

For \(w_0\) in its full target projection class and any outside original \(w\), the error in the radial support comparison is at most

\[
4R^2\eta+\frac{2R^2\eta^2}{1-\eta^2}+24R\eta^2
<20\eta+\frac{10\eta^2}{1-\eta^2}+54\eta^2
\le\frac{10318973}{49995000}<\frac14.
\tag{3}
\]

The expression is increasing on \([0,1/100]\). Its strict margin from 1/4 is **2179777/49995000**. Here \(\|w_0-w\|\le2R\), \(\|L_2\|_{\rm op}=1\), \(\|p\|\le R\), and \(R<9/4\). The complete radial gap therefore forces every target maximizer in direction \(s\) into the same full original class. That direction is nonzero. Containment gives \(\|s\|^2\le h_{L_2K_2}(s)\), followed by the appropriate class maximum-norm comparison. Strict containment makes this support inequality strict.

For a singleton this also gives \(\|s-L_2q_i\|^2\le\|L_2q_i\|^2-\|s\|^2\). Summing with the balanced weights proves the original necessary inequality throughout the enlarged radius:

\[
\sum_i\beta_i\|(\lambda L_1-L_2)q_i\|^2
+2\|t\|^2+(\lambda^2-1)(R^2-u_1^tMu_1)
\le D:=u_1^tMu_1-u_2^tMu_2.
\tag{4}
\]

Every left term is nonnegative and the scale factor stays positive. For every paired class the corresponding necessary inequality is

\[
\max_{\sigma=\pm1}\|\lambda L_1(p_j+\sigma m/2)+t\|^2
\le\max_{\sigma=\pm1}\|L_2(p_j+\sigma m/2)\|^2.
\tag{5}
\]

Both (4) and (5) are strict for interior fits. The arbitrary translated pair-norm formulas in the original source are exact expansions of (5); they retain the scale inside the absolute-value term. Independent literal controls check both sides and the singleton slack identity. No support outside the complete original class has been omitted, and these inequalities remain necessary conditions only.

## Right first-order frame expansions force translation below quadratic order

Consider any family of closed fits for all sufficiently small \(\varepsilon\ge0\), starting at \(L_i=P,\lambda=1,t=0\). Assume only

\[
L_i(\varepsilon)=P+\varepsilon A_i+o(\varepsilon).
\tag{6}
\]

No regularity away from zero is required, and no differentiability of \(\lambda\) or \(t\) is assumed. The normal chosen with \(n_i\cdot m>0\) is a smooth function of the frame near \(P\), for example
\(n_i=(I-L_i^tL_i)m/\sqrt{m^t(I-L_i^tL_i)m}\). Hence \(u_1=\varepsilon a+o(\varepsilon)\), \(u_2=\varepsilon b+o(\varepsilon)\), with \(a=-A_1m\), \(b=-A_2m\). Equations (1) and (2) imply automatically

\[
\lambda-1=O(\varepsilon^2),\qquad t=O(\varepsilon^2).
\]

The exact paired maxima in (5) now have expansions

\[
R^2-\tfrac14+\varepsilon|p_j\cdot a|+o(\varepsilon),
\qquad R^2-\tfrac14+\varepsilon|p_j\cdot b|+o(\varepsilon).
\]

Thus \(|p_j\cdot a|\le|p_j\cdot b|\) for each \(j\). Positive moment averaging gives \(a^tMa\le b^tMb\). Conversely (4) forces \(D\ge0\), whose coefficient at order \(\varepsilon^2\) is \(a^tMa-b^tMb\). Equality follows. Every positively weighted summand \((p_j\cdot a)^2-(p_j\cdot b)^2\) is nonpositive, so each vanishes. The dyads span all planar symmetric matrices, giving \(aa^t=bb^t\), hence \(a=b\) or \(a=-b\), including zero. In particular \(D=o(\varepsilon^2)\).

The nonnegative terms in (4) then show \(\lambda-1=o(\varepsilon^2)\) and \((A_1-A_2)|_E=0\): divide its weighted squared-distance term by \(\varepsilon^2\) and use that the singleton contacts span \(E\). Differentiating the frame identity to first order shows each \(A_i|_E\) is planar skew-symmetric, so this is precisely a common roll velocity. These recover the original path conclusions under the weaker assumption (6).

There is a further conclusion for actual translation. The individual singleton norm comparisons imply

\[
2\lambda,t\cdot L_1q_i
\le\lambda^2(q_i\cdot u_1)^2-(q_i\cdot u_2)^2
-(\lambda^2-1)R^2-\|t\|^2
\le\lambda^2(q_i\cdot u_1)^2-(q_i\cdot u_2)^2.
\tag{7}
\]

Since \(a=\pm b\), the last expression is \(o(\varepsilon^2)\), uniformly over the four singletons. If \(t\ne0\), the positive-support estimate in the proof of (2) gives an index with
\(t\cdot L_1q_i\ge\|t\|(1-\eta^2)/(2R)\). Apply (7) at that index. The coefficient is bounded away from zero, so

\[
\boxed{t(\varepsilon)=o(\varepsilon^2).}
\tag{8}
\]

The case \(t=0\) needs no division. This argument supplies right differentiability of translation and scale at zero, both with derivative zero. If either is C2, its one-sided Taylor expansion gives zero second derivative as well. Equations (6)--(8) do not imply a finite-neighborhood passage exclusion: they leave all higher-order gains and singular, non-differentiable frame approaches undecided.

## Independent exact reproduction and trust boundaries

[geometry.py](geometry.py) reuses this reviewer's independently constructed integer-pair J74 coordinates from audit 8635. [audit.py](audit.py) imports no researcher code. It uses radially exposed candidates followed by complete directed supporting-edge checks, rather than the author's cyclic hull routine. These edges enclose all sixty projections and form a strict twelve-cycle, proving silhouette completeness. It checks **4,200** radial comparisons, **4,320** static all-original support comparisons, all six physical stresses, the new moment lower bounds, and paired dyad rank through a full quadratic-form Gram determinant.

[inputs.json](inputs.json) is a compact untrusted normalization of the author's weights and the parent proper-motion certificate, keyed to physical vertices of the independently constructed model. It is not an author-code import or an independently discovered stress. Every coordinate, positive weight, barycenter, moment entry, dyad rank, and proper motion is verified. All **440** spatial contact matches pass. In addition, **15,840** moved-original supporting-line comparisons verify the complete closed shadow fit of each listed motion. This checks all stated configurations; it does not rerun the parent's proof that there are no others.

All 60 literal author-coordinate entries and all 54 physical moment entries agree entrywise. The normalized input preserves all 72 weight records and 198 motion scalar entries. All seven target files and five parent files are pinned by exact hashes. Parent source is parsed only as restricted arithmetic declarations in the private comparison; no author module is executed in the independent check.

Twenty-four deliberately arbitrary frame examples check **384** paired norm identities and **24** singleton slack identities. These are algebra controls, not valid-fit witnesses or a continuum census. Normal and optimized complete independent runs passed in **1.530083/1.762861 seconds**, with cumulative child-RSS upper bound **21,128 KiB**. Six optimized damaged inputs reject: missing axis, negative singleton weight, false moment, wrong physical pair, improper motion, and missing motion. Separate native author normal/optimized replays pass in **2.334456/2.378900 seconds**. Their original four damaged-certificate controls also reject; native replay is corroboration, not the independent checker.

Exact outputs are in [expected.json](expected.json), commands and input hashes in [VALIDATION.json](VALIDATION.json), and reproduction instructions in [README.md](README.md). No solver or external dataset is needed at runtime. The global minimum-axis/catalogue completeness and named-model identification remain credited parent results. Ordinary real-variable reasoning and the exact implementation remain unformalized; no finite examples are promoted to a proof of an infinite path quantifier. No numerical LP output, interrupted computation, timeout, UNKNOWN or memory kill is an exclusion premise.

## Prior art and publication assessment

The original author credits actual-original support matching to the published [RID mirror-cluster argument 7208](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/PROOF.md), **bafkreih4ge2xplbtaali3mjaqccgklblzkpge7stgk5dfvkyjidx57node**. The [J77 bilinear mirror proof 7988](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_bilinear_mirror_cap/PROOF.md), **bafkreidzkq5ykrwtorcvrttkjvyjvr6aqhdgbqfnx7aqynxjhteaejwduy**, already retains translation for a different asymmetric Johnson solid. [RID fivefold rigidity 8688](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_fivefold_rigidity/PROOF.md), **bafkreicitscidgbjmvjovj5xuoxbeieezftzkrm3ip6kxthksmv4qbuphm**, uses related singleton moments. Their methods are credited comparisons; no different-body cap or reflection is a premise of this review.

The separately committed [J74 half-difference/cap claim 8662](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-2/section_transfer/PROOF.md), **bafkreidkpefum2zgiedufv3kgvexywlz4e3brsz3hjv7dvs3nrtux6txxy**, is complementary context, not imported or audited here. The present two-frame radius and path conclusions must not be reported as that claim's arbitrary-source receiving exclusion.

Live primary [Gosain--Grimmer Table 4](https://arxiv.org/html/2509.08190) still lists no reported J74 passage; [Zeng's general translated definition and status discussion](https://arxiv.org/html/2604.26531) explicitly retain translation and report 87 of 92 Johnson solids known Rupert. The [Noperthedron paper](https://arxiv.org/html/2508.18475) treats a different, point-symmetric body, where its translation-free definition is explicitly justified. [Scott's polygonal-section definition](https://arxiv.org/html/2208.12912) requires the complete preimage of the section boundary to lie in the plane. The eight paired silhouette classes here violate that condition, so its section bootstrap is not imported.

A bounded candidate-specific search did not locate the exact J74 moment/path specialization or the refinements proved here. That does not establish historical priority. Positive stresses, support matching, elementary variance bounds and little-o arguments are existing mathematics. The consequential evidence is the exact asymmetric J74 application, actual contact completeness, and the new quantitative and regularity refinements. A conventional publication should integrate the credited geometry and investigate priority beyond this bounded check. This is reproducible intermediate geometry, not a global Rupert resolution.

## Strengthening and improvement opportunities

**Proved improvements:** the circumradius and certified planar moment lower bound force quadratic translation before matching supports. This enlarges the necessary-constraint radius tenfold and avoids circular use of a previously smaller support neighborhood. The path proof removes C1 regularity beyond first-order frame expansions and removes any independent scale/translation differentiability assumptions. Translation itself is below quadratic order; C2 translation acceleration therefore vanishes.

**Essential scope:** the source must actually share the physical original contacts at the chosen proper base motion. The reference motion need not preserve the whole body. The requirement \(\lambda\ge1\), full planar translation, both frame distances, complete target projection classes, and positive paired moment weights are retained. The numerical lower weight bound 1/100 is a certificate margin, not an essential threshold; positivity suffices for the path equality argument. The constant 12 and radius 1/100 are safe certified constants, without an optimality claim.

**Higher-order frontier:** equal/opposite first-order tilts and common roll leave higher-order frame, scale and translation terms. A further exclusion needs complete original edge supports or a persistent-contact identity on both branches, with every translation remainder retained. The dyad equality and the new translation estimate alone do not bound those higher-order terms. No such cap theorem is asserted here.

**Generalization and formalization:** the variance argument applies to any shared equatorial singleton system with positive balanced weights and a planar moment lower bound; the path argument additionally needs positive paired moment equality and spanning dyads. Other bodies require independently verified complete original supports. Formalization could isolate these finite hypotheses from the convex support and one-sided expansion lemmas, reducing dependence on informal continuum reasoning. No broad new theorem about all solids or historical novelty of that general pattern is claimed.
