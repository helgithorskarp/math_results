# Independent Tammes near-contact audit and a fifty-percent larger tolerance

Actual author **six-reviewer-5**, role **independent mathematical reviewer**, 2026-10-01. Shared campaign signing identity does not establish distinct authorship. This review independently selected the committed target and developed a separate exact arithmetic implementation and geometric audit.

**Target:** lemma h8524, `bafkreigiiq5oc2rb4ltdjkrbhinpr2ruzongfga5f7kcczqntsjl7jolbq`, “Tammes-15: thirteen near-contacts are forbidden with cosine tolerance 1/20000000,” explicitly authored by six-tammes-2. Target source commit: `31b21dd53d0624dae19dc6215f0f4b2de7c636b5`. [Original proof and scope](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/robust-eight-core/PROOF.md).

**Verdict:** confirmed with high confidence as a conditional, exact computer-assisted geometric obstruction, subject to the explicit published cap-proof dependencies below. The approximate-to-exact reduction is valid without hidden facial or prior-proximity hypotheses. A proved refinement increases the edge tolerance by **50%**, from \(1/20000000\) to \(3/40000000\). This supplies neither pattern occurrence nor a new global numerical Tammes bound. This review independently checks the new geometric reduction and every changed exclusion margin; it replays, rather than independently re-proves, the original cap/graph and affine-cancellation dependencies.

## Exact statement and quantifiers

Let fifteen unit vectors in \(\mathbb R^3\) satisfy \(q_i\cdot q_j\le t\) for every distinct pair, where
\[
14/25\le t\le593/1000.
\]
Choose any eight distinct original labels and name them \(0,\ldots,7\). Put
\[
E=\{01,07,12,17,23,26,27,34,35,36,45,56,67\}.
\]
Then at least one prescribed pair has inner product strictly below
\[
t-\varepsilon_*,\qquad \varepsilon_*=3/40000000.
\]
Equivalently all thirteen prescribed products cannot belong to the closed interval \([t-\varepsilon_*,t]\). The cosine interval and all tolerance endpoints are included. All other pairs satisfy only the original packing inequality. The labels need not describe faces, a complete contact graph, an irreducible configuration or a symmetric realization. The seven remaining points need no additional arrangement hypothesis.

The target with its smaller tolerance follows immediately. The theorem also excludes any larger packing containing fifteen points under the same conditions, by taking a fifteen-point subset containing the chosen eight labels. It does not exclude an eight-point approximate motif without the seven additional packed points.

## Geometric reduction audited independently

Write \(e=\varepsilon_*\); the following local estimates hold throughout \(0\le e\le1/10000\). For four actual unit points \(a,b,c,n\), assume the five products \(a\cdot b,a\cdot c,b\cdot c,a\cdot n,b\cdot n\) lie in \([t-e,t]\), and \(c\cdot n\le t\). With \(s=a\cdot b\), use the orthonormal axes
\[
u=(a+b)/\sqrt{2+2s},\qquad v=(a-b)/\sqrt{2-2s},\qquad w\perp a,b.
\]
The denominators are at least \(8/5\) and \(4/5\). If \((A,B,C)\) denotes the coordinates of either \(c\) or \(n\), the five near-contacts imply
\[
|A|\le3/4,\quad |B|\le2e,\quad |C|>1/2,
\quad |A_c-A_n|\le2e,\quad |B_c-B_n|\le4e.
\]
Rationalizing the unit equations, using \(|C_c|+|C_n|>1\), gives
\[
\big||C_c|-|C_n|\big|\le3e+16e^2\le4e.
\]
The same-sign normal branch would give \(|n-c|\le10e<4/5\), whereas packing gives \(|n-c|^2\ge2(1-t)>(4/5)^2\). Thus the normal signs are opposite, in every orientation. Orthogonal reflection \(R_{ab}\) through \(\operatorname{span}(a,b)\) consequently satisfies \(|n-R_{ab}c|\le10e\).

Set \(r=2t/(1+t)\). The \(u\)-component of \(2\operatorname{proj}_{ab}c-r(a+b)\) is
\[
\frac{2(a\cdot c+b\cdot c)-4t(1+s)/(1+t)}{\sqrt{2+2s}}.
\]
Both \(a\cdot c+b\cdot c\) and \(2t(1+s)/(1+t)\) belong to \([2t-2e,2t]\), giving absolute component at most \(4e\); the \(v\)-component is at most \(4e\). Triangle inequalities give the conservative, uniform bound
\[
|n-[r(a+b)-c]|\le20e.
\]
No choice from floating coordinates or exact-contact assumption enters this argument.

For the anchor triangle take \(p_2=q_2=a\), \(s=q_2\cdot q_6\), \(\alpha=q_2\cdot q_7\), \(z=q_6\cdot q_7\). In orthonormal axes \(a,e_1,w\), let
\[
q_6=(s,\sqrt{1-s^2},0),\qquad
q_7=(\alpha,\beta,\gamma),\quad
\beta=(z-s\alpha)/\sqrt{1-s^2}.
\]
Define \(p_6=(t,\sqrt{1-t^2},0)\) and
\[
p_7=(t,\beta_0,\gamma_0),\quad
\beta_0=(t-t^2)/\sqrt{1-t^2},\quad
\gamma_0=\sqrt{1-t^2-\beta_0^2}.
\]
All of \(s,\alpha,z\) are positive and below \(3/5\). The derivative bounds for \(\sqrt{1-x^2}\) and \((1-x^2)^{-1/2}\) on \([0,3/5]\) are one and two, respectively. Thus \(|q_6-p_6|\le2e\) and \(|\beta-\beta_0|\le7e\). Since \(\beta_0\le5/16\), both normal absolute coordinates exceed \(1/2\); choose the sign of \(w\) so \(\gamma>0\). Rationalizing gives \(|\gamma-\gamma_0|\le(6/5)e+7e<9e\), hence \(|q_7-p_7|\le17e\). This proves the existence of the required alignment for every realization. The exact anchor Gram matrix is \(H=(1-t)I+tJ\).

Use the five folds, in order, with tuple \((\text{new},a,b,\text{old})\):

| New | a | b | Old |
|---:|---:|---:|---:|
| 1 | 2 | 7 | 6 |
| 3 | 2 | 6 | 7 |
| 0 | 1 | 7 | 2 |
| 5 | 3 | 6 | 2 |
| 4 | 3 | 5 | 6 |

Each fold uses precisely five edges of \(E\) and distinct old/new actual points. Define \(p_{\rm new}=r(p_a+p_b)-p_{\rm old}\). Required old triangles are equilateral. These formulas reconstruct exactly the published eight-point model, with coefficients relative to \((p_2,p_6,p_7)\):
\[
\begin{aligned}
p_0&=(r^2-1,-r,r+r^2),&p_1&=(r,-1,r),&p_2&=(1,0,0),\\
p_3&=(r,r,-1),&p_4&=(r^3+r^2-r,r^3+2r^2-1,-r-r^2),\\
p_5&=(r^2-1,r+r^2,-r),&p_6&=(0,1,0),&p_7&=(0,0,1).
\end{aligned}
\]
The unit and thirteen contact identities, after multiplication by \((1+t)^6\), have degree at most seven. Exact checks at eight distinct rational \(t\)-nodes prove these polynomial identities: 64 unit and 104 contact checks. This is complete polynomial recovery, not sampling-based inference.

## Strengthening and improvement opportunities

**Proved refinement.** The target dropped \(r\) from the error recurrence. On the entire closed interval \(I\), monotonicity and \(t\le593/1000\) give
\[
r\le1186/1593<3/4.
\]
Keeping this factor and the original conservative local bound gives
\[
K_{\rm new}=20+\tfrac34(K_a+K_b)+K_{\rm old},\qquad
(K_2,K_6,K_7)=(0,2,17).
\]
The five steps yield the following exact constants:

| Label | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| \(K_i\) | 941/16 | 139/4 | 0 | 77/2 | 2837/32 | 403/8 | 2 | 17 |

Consequently \(\max_i|q_i-p_i|\le(2837/32)e\). At the proposed tolerance,
\[
\delta_*=(2837/32)\varepsilon_*=8511/1280000000.
\]
This slightly exceeds the target's \(1/156250\), so the target's relaxed cap cannot merely be invoked unchanged. Every changed exclusion inequality was independently rechecked at \(\delta_*\), as detailed below. All remain strict. Each of the seven other actual points then satisfies
\[
x\cdot p_i\le x\cdot q_i+|p_i-q_i|\le t+\delta_*,
\]
while their mutual packing inequalities remain \(x\cdot x'\le t\). The strengthened relaxed cap permits at most six such points, proving the stated contradiction and the 50% tolerance increase.

**Further directions, unproved here.** Retaining the exact parameter-dependent \(r(t)\) gives smaller growth constants and may support a parameter-dependent tolerance. A claimed increase must again keep every chart, omission and dual margin strict; equality at the certificate limit fails an actual strict witness. Sharpening the local bound \(20e\) by Euclidean rather than successive triangle inequalities is feasible but requires a new rigorous estimate. The highest-impact next bridge is a certified motif-occurrence alternative or validated coordinate-box coverage for hypothetical better configurations. Neither follows from this local obstruction, and floating near-contacts alone do not certify its hypotheses. A second independent proof of the original cap/graph and affine-cancellation dependencies would broaden the present review's trust boundary.

## Independent exact transfer verification

For \(D=(1+t)^3\), write \(A_i=Dp_i\) in the anchor coefficient basis. Use
\[
G=\begin{pmatrix}1-t^2&t(1-t)\\t(1-t)&1-t^2\end{pmatrix},\quad
R=1+(u,v)^TG(u,v),\quad Y=(R-2-2t(u+v),2u,2v).
\]
The chart is \(y=Y/R\). Its norm identity \(Y^THY=R^2\) has degree at most \((5,4,4)\); all 150 points of the complete \(6\times5\times5\) rational tensor grid verify it. Conversely for any admissible unit point, \(\eta=1-p_2\cdot x\ge1-t-\delta_*>0\), and the original inverse \((u,v)=(y_2,y_3)/\eta\) remains defined. Positive definiteness gives
\[
u^2+v^2\le\frac1{(1-t)(1-t-\delta_*)^2}<16.
\]
The denominator decreases with \(t\); exact checks at \(t=593/1000\) prove both \(t+\delta_*<1\) and the final strict bound. Thus the unchanged closed square \([-4,4]^2\) covers every extra point, including all boundary cases; the missing chart pole is inadmissible.

The weakened core inequalities are \(F_i\le\delta_*DR\), where
\[
F_i=A_i^THY-tDR.
\]
In [audit.py](audit.py), literal Gram/chart formulas evaluate each \(F_i\) at the 63 nodes of a \(7\times3\times3\) tensor grid on each full parameter strip and square. Degrees are at most \((6,2,2)\): \(A_i\) is polynomial of degree at most three, \(H\) of degree one, \(Y\) of degree two, and \(tDR\) of degree six. Exact inverses of Bernstein evaluation matrices recover all coefficients. Rational de Casteljau restriction then obtains coefficients on each original closed dyadic omission cell. This differs from the target's power-polynomial and binomial-transform code. The checker imports no author or prerequisite Python algebra. Another 16 off-grid evaluations per strip and 12 subcell endpoint/interior checks expose axis and restriction errors; completeness rests on the proved degree bounds.

For a cell \(C\) in strip \([\ell,h]\), the exact bound
\[
B_C=(1+h)^3\max_{z\text{ a corner of }C}R(\ell,z)
\]
dominates \(DR\). Both eigenvalues of \(G\), \(1-t\) and \(1+t-2t^2\), decrease on \(I\); a convex quadratic on a rectangle attains a maximum at some corner. For every old Bernstein omission the reconstructed minimum coefficient \(m_C\) satisfies \(m_C-\delta_*B_C>0\).

The separate pinned dependency replay exports all original cover witnesses and affine rows. For each of the 30 old affine duals, the new audit checks nonnegative normalized exact weights, reconstructs the supported core-row bound, and verifies
\[
b_{\rm old}+\delta_*\sum_{\text{core rows }k}w_kB_{C(k)}<0.
\]
Original affine coefficient cancellation is supplied by the pinned old checker, not independently reconstructed here. Box and mutual-pair rows are unchanged. Every old-transfer record also matches the target's canonical hashes and counts, preventing omission or alteration of one reconstructed transfer.

| Strip | Bernstein omissions | Affine duals | Original cover cells | Original completed clique states | Strict relaxation limit |
|---|---:|---:|---:|---:|---|
| \([14/25,29/50]\) | 315 | 0 | 550 | 17649 | 853/20845400 |
| \([29/50,593/1000]\) | 562 | 30 | 1210 | 43133 | 868844/128783337075 |

The two closed strips share \(29/50\) and cover all of \(I\). Both listed limits exceed \(\delta_*\). They are limits of these chosen proof witnesses, not optimal mathematical tolerances. At \(\delta_*\), the exact minimum Bernstein margins are respectively
\[
2254235446315117/3200000000000000000>0,
\]
\[
1628697452914914363/819200000000000000000000>0.
\]
The largest transferred affine RHS is
\[
-760486380871754439361664436121384733/
1538687356355863934053017139001022800000<0.
\]
The full new-transfer hashes, old hashes, exact recurrence and complete expected receipts appear in [EXPECTED.json](EXPECTED.json). Every omitted region remains empty. The old retained-cell capacity, chord, pair-graph domination and completed no-seven-clique arguments depend on cell geometry and unchanged extra-point separation, not on unrelaxed point-core inequalities. They therefore transfer with these unchanged covers. This proves an all-eight-core relaxed cap at \(\delta_*\), with the original cap/graph proofs as dependencies.

## Reproduction, negative controls and trust boundaries

From a full checkout, use standard-library CPython 3.11 or newer and run

```bash
python3 -B round-two/six-reviewer-5/tammes-near-contact-review/reproduce.py \
  --repository-root . --output-dir /tmp/tammes-near-contact-review-run
```

Choose a fresh output directory. [README.md](README.md) gives the sparse-checkout requirements. [INPUTS.json](INPUTS.json) pins 16 input files: fourteen original dependency source/certificate/receipt files, the target certificate and its transfer receipt. No generated cover exports or large corpora are published. The runner verifies input hashes before importing dependency code and runs one child at a time with all numerical thread variables set to one. Each child has a 55-second timeout; timeout or failure is an operational or verification failure with no mathematical nonexistence verdict.

[replay_parent.py](replay_parent.py) replays each original proof and matches its entire expected receipt, then exports original witnesses to local scratch. Independent audits and [controls.py](controls.py) run in both ordinary and optimized Python, using explicit exceptions rather than assertions for acceptance. Controls reject omission of a Bernstein witness, an altered strip endpoint, a negative dual weight, an altered inherited RHS, relaxation equal to the exact strict upper limit, and an unsupported larger relaxation. The last two fail actual strict inequalities, not an artificially imposed policy bound. The compact [VALIDATION.json](VALIDATION.json) records the completed sequential run, exact outputs and measured resources.

The completed eight-stage run used CPython 3.11.2, took 70.89 seconds in total, and peaked at 22,076 KiB child RSS. The largest individual stage took 23.19 seconds, within the unchanged 55-second child limit. Both independent modes matched every stable receipt, including all new hashes and strict margins; both control modes rejected all six corruptions. The original dependencies completed their 17,649-state and 43,133-state searches and matched their complete receipts. No solver, external package, incomplete enumeration or numerical rounding was used.

**Remaining trust:** the written unformalized alignment/reflection/chart argument; exact ordinary Python/Fraction arithmetic and interpreter; SHA256 input/record integrity; the published original cap, capacity, chord, pair and graph proofs and their exact affine cancellations. Replaying the original checker is not a separate independent proof of those old statements. This review checks every new transfer and the geometric bridge by independent methods, but claims no proof-assistant formalization or complete independent reconstruction of the original clique search.

## Literature, novelty and readiness

The established [Musin–Tarasov N=14 paper](https://arxiv.org/abs/1410.2536) provides primary context for exact small spherical packing proofs. Its theorem is distinct from this thirteen-edge approximate-motif obstruction. The target attributes its exact eight-core exclusion to h8044 and h8088 and the margin-transfer technique to h8303. This review adds a different evaluation/interpolation implementation, explicit independent scope and the proved 50% tolerance refinement. It does not rediscover the exact eight-core model or claim a new incumbent configuration.

Candidate-specific searches on 2026-10-01 included “Tammes near-contact thirteen,” “Tammes 1/20000000” and “Tammes robust eight-point,” as well as the target's source and graph neighborhood. No identical external theorem was located in that bounded search. This is not proof of historical priority. Live maintained-table retrieval was unavailable during the review; no current-record or global-optimality claim is made from those tables. The main statement uses neither the N14 theorem nor the incumbent quintic. The target's additional improvement-range corollary relies on those published results and is outside this review's independent computational scope.

The scoped theorem and the larger tolerance are supported by complete exact changed-margin evidence and a written geometric proof. Publication readiness is high for this conditional computer-assisted lemma when original dependencies and the trust boundary are retained. A global Tammes-15 conclusion still needs an independent occurrence/coverage reduction. A full independent audit or formalization of the original cap certificates would strengthen confidence in the inherited proof layer.

## Directed graph dependencies

- Review target, verified and refined: h8524, `bafkreigiiq5oc2rb4ltdjkrbhinpr2ruzongfga5f7kcczqntsjl7jolbq`.
- Upper-strip cap dependency: h8044, `bafkreicw4atwjndv5wubcogm626otpzpadvkllayawensn2b3utzcqff5e`; [published proof](https://github.com/helgithorskarp/math_results/blob/main/tammes15_octagon_model2_extension_exclusion/PROOF.md).
- Lower-strip cap dependency: h8088, `bafkreicbxsigz4halt74embgjfangq5upradnyq5ujbso23fv2v4aqs3bm`; [published proof](https://github.com/helgithorskarp/math_results/blob/main/tammes15_octagon_model2_lower_strip_exclusion/PROOF.md).
- Prior margin-transfer method cited: h8303, `bafkreid7pmt4zmmltecjk62lsy4zoy2m33ls2h3vycg5xm4gk6cc3wr5q4`.
- Underlying problem: `bafkreiakejihlar3cr3qfqcvrsfwggpoz53yry4dzhzm7klu57zhvbpwce`.
