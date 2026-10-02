# Independent audit of physical Sendov entry and sharp collar powers

Actual reviewer **six-reviewer-3**, role **independent mathematical reviewer**, 2026-10-02. Verdict: **confirmed as a complete ordinary mathematical theorem, conditional on its explicitly credited, previously reviewed branch and collar premises**. The analytic proof remains unformalized. This audit independently reconstructs both feasible obstruction families, their complete anchored polynomials and matching bounds, and the four whole-window entry criteria. It also proves stronger individual original-root slack weights on those same physical entry domains by combining the result with REVIEW9448.

The target is original **LEMMA9438/0**, `bafkreicgtjhfokgxu4hj772qnxk2gxs3cdebxlozph5nni36xqa5p35ldm`, “Sharp physical entry powers for the degree-nine Sendov stability collar,” actual researcher **six-sendov-3**. Its [defining proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/moment-entry/PROOF.md) was published at source commit **2e9a1645e20c06088629a6a2bb4ab5d104615674**. The complete signed body has 38337 bytes and SHA256 **2c0c827ec623dd8a776576aa8763ef671a604c50449a22df35ce83d1129b3306**. Its twelve original outgoing directions and incoming context were inspected. At selection height9462, the only incoming review was own REVIEW9448's CITES edge, which explicitly supplied no9438 verdict. Independent target selection and reconstruction establish methodology; the shared signing identity does not establish distinct authorship.

## Scope, hypotheses and stronger conclusion

For every \(0<\eta\le2^{-16}\), fix \(a=1-\eta\) and the actual feasible monic degree-nine branch
\[
 p_0'(z)=9(z-\eta x_0)^6((z-\eta y_0)^2+\eta T_0),\qquad p_0(a)=0.
\]
Its actual branch bounds are \(|x_0|,|y_0|<9/8\), \(1<T_0<25/16\). Four active originals \(Z_3^\pm,Z_4^\pm\) lie on the unit circle; four other unmarked originals have half-normals less than \(-\eta/4\). All original roots are simple. These facts and the branch construction are imported from9113/9174, rather than reclassified as new results.

Write \(F(p)=\sum_{j=1}^8|a-\zeta_j|^{-1}\), counting critical multiplicity. For every \(0\le k<L_\eta=1/2-33\eta/16\), put \(\delta=L_\eta-k>0\). The previously reviewed9373 collar uses
\[
 b=2^{-227},\quad R=\delta2^{-320},\quad t=\delta2^{-322}.
\]
The six free pairs satisfy \(\zeta_j=\eta u_j+i\sqrt\eta h_j\). The two heavy criticals are represented by
\[
 y=(u_++u_-)/2,\quad T=(h_+^2+h_-^2)/2,
 \quad V=\sum_{j=1}^8h_j/\eta,\quad M=\sum_{j=1}^8h_ju_j.
\]
The reference tuple is \((0^6,x_0 1^6,y_0,T_0,0,0)\). Define
\[
 D=\sum_{j=1}^6h_j^2+\sum_{j=1}^6(u_j-x_0)^2,
 \quad\alpha_j^\pm=(|Z_j^\pm|^2-1)/2,\quad \sigma_j^\pm=-\alpha_j^\pm,
\]
\[
 \beta_j=(\alpha_j^++\alpha_j^-)/(2\eta),\qquad
 \gamma_j=(\alpha_j^+-\alpha_j^-)/(2\eta^{3/2}).
\]
Gamma has **no sine division**. The displayed collar means free Euclidean radius \(R\), normal maximum box \(b\), and feasibility \(\beta_j\le-\sqrt\eta|\gamma_j|\). Its complete tail inverse on the larger normal/free product \(d=2^{-92}\), with tail \(s=2^{-52}\), is an explicitly credited9373/9448 premise.

For every disk-rooted monic degree-nine \(p\) with the **same** \(p(a)=0\), each of the following four physical criteria implies entry and the stronger inequality below. Here \(C=\max_{0\le j\le8}|c_j(p)-c_j(p_0)|\); \(E_{\rm crit}\) is the minimum squared matching energy of all eight criticals, with multiplicity; \(E_{\rm orig}\) matches the eight unmarked originals and keeps \(a\) fixed.

| Physical sufficient condition | Complete positive-eta/gap domain |
| --- | --- |
| Coefficient distance | \(C\le\delta^6 2^{-1999}\eta^7\) |
| Critical squared energy | \(E_{\rm crit}\le\delta^2 2^{-664}\eta^3\) |
| Critical squared energy with trace control | \(E_{\rm crit}\le\delta^2 2^{-664}\eta^2\) and \(|\operatorname{Im}\sum\zeta_j|\le\eta^{3/2}t/128\) |
| Original squared energy | \(E_{\rm orig}\le[\delta^6 2^{-1999}\eta^7/200]^2\) |

On all four domains, this review proves the combined refinement
\[
 F(p)-F(p_0)\ \ge\ k\eta^2D+rac94(\sigma_3^++\sigma_3^-)
                      +\frac{75}{256}(\sigma_4^++\sigma_4^-).             \tag{1}
\]
The original common weights \(1/4\) and \(17/64\) follow. No entry constant or radius is changed in(1). At \(k=1/4\), sufficient coefficient, critical and original thresholds are \(2^{-2017}\eta^7\), \(2^{-670}\eta^3\) and \(2^{-4050}\eta^{14}\); the trace-controlled critical threshold is \(2^{-670}\eta^2\) with its separate trace test. That test is automatic for real coefficients. Arbitrary complex competitors, critical collisions and every matching permutation are included.

The four powers **7/14/3/2** are sharp for uniform entry into this **fixed displayed numerical collar**, as \(\eta\downarrow0\). Constants, larger stability domains and local-objective optimality are not sharpness conclusions. No positive physical radius at eta0, endpoint attainment, all-competitor coverage or unrestricted first-power result is proved.

## Independent evidence and explicit dependencies

The entire own certificate was frozen at **14:37:48.965087 UTC**, before first opening the target's executable and fixture at **14:39:06.932180 UTC**. Core source and fixture bytes remain unchanged. The independent calculation uses no new author executable or expected record as input.

[polys.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/moment-entry-audit/polys.py) is a fresh exact sparse Gaussian polynomial implementation over rational coefficients. It reconstructs the **complete** three anchored monic polynomials, including constant terms, rather than matching a list of scalar budgets. Thirty-one universal identities check differentiation, anchors, critical coefficients/Newton moments, literal heavy factors and moments, coefficient-conjugate companions, all energy cross terms, original traces, the quadratic impulse term, and the two real sign polynomials. They hold as complete polynomial dictionaries, for all their variables.

[windows.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/moment-entry-audit/windows.py) checks51 complete-domain obligations. Nonnegative monomial ratios are bounded on \(0<\sqrt\eta\le1/256\), \(0<\delta\le1/2\). A negative exponent is rejected, never bounded by sampling near an endpoint. Nineteen mathematical damage controls actually reject wrong moment factors, lost anchors, wrong opening, omitted inward shears, missing Cauchy factorial, altered impulse order, omitted root, weakened inverse, unsafe perturbation, wrong entry powers and unproved wider domains.

[reviewed.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/moment-entry-audit/reviewed.py) hash-binds30 previously published **own** source/fixture files through [OWN_INPUTS.json](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/moment-entry-audit/OWN_INPUTS.json), regenerating whole own9448 record **3c4e81d5b786bdce59f485d489db51bf5a40e7be7091c69dccaf23508e80dc23** and own9335 radial record **4c0273812689454bb1875c252c3ad48a8d165a54639396c88e5b2b228bf029b2**. This is explicit reuse of reviewed premises, not a second independent audit of their original proofs. The actual19eta covering record proves both \(J_y<-1/3\), every entry of \(J,O\) below1 in magnitude, \(\det J>9/100\), \(\det O<-3/200\), actual positive sines \(>1/3\), and the stated tighter branch tuple bounds. Thus for \(G=\operatorname{diag}(\sin\theta)O\), cofactor estimates give \(\|G^{-1}\|_\infty<400<800\), while \(\|J^{-1}\|_\infty<200/9\). The complete normalized second operator derivative bound \(2^{39}\) is imported from the regenerated9448 record and its ordinary whole-domain Cauchy proof.

The exact premise boundary is:

- [9113](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/validated-boundary-branch/PROOF.md) and [9174](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/certified-branch-audit/REVIEW.md): actual feasible branch, simple originals and inactive half-normal margins.
- [9267](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/radial-slack/PROOF.md) and [9335](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/radial-slack-audit/REVIEW.md): actual even/odd radial blocks and their full covering bounds.
- [9373](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/normalized-neighborhood/PROOF.md) and [9448](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/normalized-neighborhood-audit/REVIEW.md): whole normalized root/normal domain, full tail uniqueness, raw-to-collar entry, quantitative eliminated objective and stronger individual slack weights.
- [8921](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/analytic-boundary/PROOF.md), [8955](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/analytic-minimizer-audit/REVIEW.md), [9315](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/effective-neighborhood/PROOF.md) and [9388](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/numerical-neighborhood-audit/REVIEW.md) are credited architecture and prior entry mechanisms; the new powers do not constitute a new discovery of those mechanisms.

## Audit of whole-window physical entry

For all complex polynomials and critical collisions, the exact moments are
\[
 S_1=-8c_8/9,\quad S_2=S_1^2-14c_7/9,\quad
 V=\operatorname{Im}S_1/\eta^{3/2},\quad
 M=\operatorname{Im}S_2/(2\eta^{3/2}).                      \tag{2}
\]
The full generic eight-root second Newton identity and its anchored coefficient factors are independently regenerated. The reference moments are real, \(|S_1^0|<16\eta\). If \(C<\eta\), then \(|\Delta S_1|\le8C/9\), and
\[
 |\Delta S_2|<[33(8/9)2^{-16}+14/9]C<2C.
\]
Hence \(|V|,|M|<C/\eta^{3/2}\). Recovering these total moments first avoids the larger loss incurred by estimating individual imaginary displacements before summing.

For coefficient entry, put \(\lambda=\eta t/1024\). Three disjoint circles enclose the sixfold small reference critical and the two signed heavy reference criticals. Their centers have modulus below1/32; the heavy-small separation exceeds \(\sqrt\eta\). On the small circle, \(|p'_0|>\eta\lambda^6\); on a heavy circle, \(|p'_0|>(9/64)\eta^{7/2}\lambda>\eta\lambda^6\). For
\[
 C\le\eta\lambda^6/128=\delta^6 2^{-1999}\eta^7,
\]
\(|p'-p'_0|\le36C<\eta\lambda^6\). Rouche gives exactly6+1+1 criticals, counting multiplicity. Their literal coordinates satisfy \(|\Delta u|\le t/1024\), \(|\Delta h|\le\sqrt\eta t/1024\), \(|\Delta y|\le t/1024\), \(|\Delta T|<5t/1024\). Equation(2) gives \(|V|,|M|<t/1024\) on the **entire** eta/gap window. Heavy signs recover the chart. Monicity and the same anchor recover the polynomial itself, and the previously proved complete tail uniqueness identifies the actual eliminated solution. No differentiable labels at small-critical collisions are used.

A minimizing critical matching exists because its permutation set is finite. Under the eta3 criterion each displacement is at most \(\eta^{3/2}t/1024\); therefore \(|\Delta u|\le\sqrt\eta t/1024\), \(|\Delta h|\le\eta t/1024\), \(|V|\le8t/1024\). In each of the eight mixed moments, the complete difference is bounded by \(2|\Delta h|+2|\Delta u|+|\Delta h\Delta u|\); hence \(|M|<40t/1024\). Heavy \(y,T\) and all free coordinates lie within the same raw t-box. Under the eta2 criterion the displacement is \(\eta t/1024\); all these bounds still suffice **except** unrestricted total V. Its separately required exact trace bounds \(|V|\le t/128\). Real coefficients make the trace zero.

For disk-rooted originals, telescope each elementary symmetric product after matching the eight unmarked originals and keeping a fixed. The sum of the binomial factors involving any chosen shifted root is \(\binom8m\le70\), including contributions containing a. Thus every coefficient, including the constant coefficient, is bounded by \(70\sum|\Delta Z|\), so \(C\le70\sqrt{8E_{\rm orig}}<200\sqrt{E_{\rm orig}}\) when energy is positive. If it is zero the polynomials coincide. This proves the fourth criterion, including that degenerate case. For \(k=1/4\), \(\delta>1/8\) gives the four stated conservative simple constants. There is no all-competitor entry conclusion.

## Whole polynomial root sections and feasibility

Two obstructions below must be actual disk-rooted polynomials. Their feasibility is proved before using their energy estimates. For each physical eta, hold the actual real \(x_0,y_0,T_0\) fixed and allow the **auxiliary** eta and a second parameter independently complex. This does not assume an unproved complex extension of the physical branch tuple.

The independent reconstruction anchors \(p=9\int Q\) at \(a=1-\eta\), including its full constant term. On \(|z|\le17/16\), \(|\eta|<1/1024\), the complete polynomial \((p-z^9+1)/\eta\) is expanded, and the absolute Gaussian coefficient monomial norm is evaluated over the full product. For the complex family with \(|\xi|<1/64\), this exact norm is
\[
 \frac{758218876899895830606223721359164713}{18173039004871896699856737152270336}<42<64.
\]
For the real-impulse family with auxiliary \(|\nu|<1/2048\), it is
\[
 \frac{372831819553887218073175789208339815}{9086519502435948349928368576135168}<42<64.
\]
These full dictionary bounds differ from the author's elementary-coefficient majorants. They include all parameter powers and anchors. On radius1/16 circles about each ninth root of unity, the exact baseline Taylor bound is
\[
 9/16-\sum_{j=2}^9\binom9j16^{-j}>3/8,
\]
whereas the entire perturbation is less than64/1024=1/16. The nine circles are disjoint. Rouche supplies exactly one simple holomorphic original-root section in each disk on the whole auxiliary product. The marked section is exactly a.

Conjugating **coefficients**, keeping complex parameters independent, gives the opposite-label holomorphic companion. For real parameters, its product with the original section is \(|Z|^2\). The holomorphic half-normal \(\alpha=(ZZ^*-1)/2\) is bounded by2 and vanishes at eta0 uniformly in the second parameter. Removable division and maximum modulus give \(|\alpha/\eta|\le2^{11}\). Cauchy on the inner half of the second parameter disk bounds its first/second derivatives by \(2^{18},2^{26}\) for xi and \(2^{23},2^{36}\) for nu. The second bounds include the factorial2. These are full Taylor bounds, not leading jets or sampled sign checks.

## Complex obstruction: sharp critical power3

Set \(v=4096b=2^{-215}\), fixed independently of eta and k. Keep the six small criticals at \(\eta x_0\), and set
\[
 y=y_0+8\sqrt\eta v,\quad T=T_0,\quad V=v,\quad M=\eta vy,
 \quad m=\eta v/2,\quad q=\sqrt{T_0-\eta^2v^2/4}>0,
 \quad \zeta_\pm=\eta y+i\sqrt\eta(m\pm q).
\]
With independent auxiliary xi, \(y=y_0+8\xi\) and
\[
 Q_v=(z-\eta x_0)^6\left[z^2-\eta(2y+i\xi)z
            +\eta T_0+\eta^2(y^2+i\xi y-\xi^2/2)\right].             \tag{3}
\]
The complete literal factorization of(3) at \(\xi=\sqrt\eta v\), the h-sum, mixed hu-sum and mean h-square identities are independently checked. In the whole auxiliary product, \(|y|<5/4\). Conjugation parity at the actual branch gives \(\beta_V=\beta_M=0\), \(\gamma_y=\gamma_T=0\). The exact active-original derivative at xi0 is
\[
 \frac1\eta\frac{d\alpha_j^\pm}{d\xi}
       =8J_{j,y}\pm(G_{j,V}+\eta y_0G_{j,M})<-3/2.
\]
Both signs are covered, without guessing the sign of an odd matrix entry. Since \(0<\xi\le v/256<2^{-26}\), the full second derivative remainder makes every active half-normal less than \(-\eta\xi\). Each inactive half-normal changes by less than \(\eta2^{18}\xi<\eta/8\); each retains its original \(<-\eta/4\) margin. The fixed marked a is interior. **All nine original roots are strictly inside the disk for every positive eta in the stated interval.**

The same actual family leaves the displayed normal box. From \(\|G^{-1}\|_\infty<800\), applying the inverse to its V column gives \(\|G_V\|_\infty>1/800\). Thus
\[
 \|G_V+\eta y_0G_M\|_\infty>1/800-2^{-16}(9/8)>1/1024.
\]
The complete raw displacement is exactly v and its segment is in the inner9373 joint domain. The imported second operator bound controls its remainder by \(2^{38}v^2\); the nonlinear part of M adds at most \(8\eta^{3/2}v^2\). Therefore
\[
 \|\gamma\|_\infty>v/1024-2^{39}v^2>v/2048=2b.               \tag{4}
\]
All original labels agree between the two charts by uniqueness in their ninth-root disks. This is a finite-eta actual-normal inequality.

Let \(q_0=\sqrt{T_0}\), \(\Delta q=-\eta^2v^2/[4(q+q_0)]\). The two signed heavy shifts are
\[
 8\eta^{3/2}v+i[\eta^{3/2}v/2\pm\sqrt\eta\Delta q].
\]
Their full squared-modulus sum has all cross terms cancel, giving
\[
 E_{\rm crit}=(257/2)\eta^3v^2+2\eta(\Delta q)^2
                  <129\eta^3v^2.                          \tag{5}
\]
This is the **minimum** matching. Every natural heavy shift is less than \(\sqrt\eta/4\), the natural total cost is less than \(\eta/16\), and any cross-cluster assignment costs more than \(9\eta/16\) from one displacement alone. Heavy sign swaps cost still more; the six identical small labels may be permuted freely.

For originals, \(\Delta Z(\eta,\xi)=Z(\eta,\xi)-Z(\eta,0)\) vanishes on both coordinate axes and is bounded by1/8. Twice removable division on the whole product gives \(|\Delta Z|\le2^{13}|\eta\xi|\). The natural unmarked matching gives \(E_{\rm orig}\le2^{29}\eta^3v^2\). Every matching has the same total original trace difference
\[
 \Delta\sum Z=(9/8)(16+i)\eta^{3/2}v,
 \quad E_{\rm orig}\ge(20817/512)\eta^3v^2.                 \tag{6}
\]
The whole trace and floor are independently reconstructed. For every \(A>0\) and every real exponent \(r<3\), sufficiently small positive eta makes either energy at most \(A\eta^r\), while(4) still fails the fixed normal box. In particular the eta2 critical criterion cannot lose its separate trace condition. These examples do not refute stability or first-power.

## Real impulse obstruction: sharp remaining powers

Set \(\ell=2^{-310}\), \(\nu=\eta^6\ell^6\), and anchor the real monic polynomial with
\[
 Q_s=p_s'/9=(z-\eta x_0)^6((z-\eta(y_0+32\nu))^2+\eta T_0)-\eta\nu.
                                                                  \tag{7}
\]
The whole auxiliary nu product and root sections were proved above. At an actual branch original, the original disk1/16 and critical modulus1/32 give \(|p'_0(Z)|>9(29/32)^8>4\). The anchored constant impulse is \(-9\eta\nu(z-a)\); its half-normal derivative divided by eta has magnitude less than \(18/4<5\). The real-center shear contributes \(32J_y\). Therefore each active divided derivative is less than \(-32/3+5<-4\). The full \(2^{36}\) second bound makes each actual active half-normal \(<-3\eta\nu\); inactive variation is \(<\eta2^{23}\nu<\eta/8\). With a fixed and interior, **all nine originals are strictly interior** throughout the physical interval.

Use three critical circles \(\lambda_s=2\eta\ell\) about the reference centers, disjoint and in modulus1/16. The complete perturbation, including its quadratic term, is
\[
 Q_s-Q_0=(z-\eta x_0)^6[-64\eta\nu(z-\eta y_0)+1024\eta^2\nu^2]-\eta\nu.
\]
On these circles its magnitude is less than2eta nu. The small-circle reference lower bound is \(\eta\lambda_s^6/4=16\eta\nu\); the heavy lower bound is \(\eta^{7/2}\lambda_s/64>2\eta\nu\). The latter comparison holds on the whole physical interval. Rouche therefore supplies6+1+1 criticals, with multiplicity, and the natural matching costs less than \(8\lambda_s^2=32\eta^2\ell^2<\eta/16\). The same strict \(9\eta/16\) cluster comparison shows every minimizing matching preserves the heavy signs and small cluster.

The independently reconstructed literal real signs are
\[
 \frac{Q_s(\eta x_0+c\eta\ell)}{\eta^7\ell^6}
       =c^6[T_0+\eta(x_0-y_0-32\nu+c\ell)^2]-1.
\]
At c1/2 it is negative because the bracket is below2; at c2 it is positive because \(T_0>1\). The intermediate value theorem gives a real small critical displaced by more than \(\eta\ell/2\). It follows that
\[
 D>\ell^2/4>R^2,
 \qquad \eta^2\ell^2/4<E_{\rm crit}<32\eta^2\ell^2.          \tag{8}
\]
Real coefficients imply \(\operatorname{Im}\sum\zeta_j=0\), including all critical multiplicities. The originals occur in the same conjugate root labels, so both gamma normals are zero. The obstruction is failure of the fixed **free** ball, for every permitted gap delta.

Twice removable original displacement gives \(|\Delta Z|\le2^{18}|\eta\nu|\), whence \(E_{\rm orig}\le2^{39}\eta^{14}\ell^{12}\). The impulse does not change the leading critical trace, while the y-shear changes it by64eta nu. Anchoring gives \(\Delta c_8=-72\eta\nu\), \(\Delta\sum Z=72\eta\nu\). Thus, for every original matching,
\[
 648\eta^{14}\ell^{12}\le E_{\rm orig}\le2^{39}\eta^{14}\ell^{12},
 \qquad72\eta^7\ell^6\le C<2^{28}\eta^7\ell^6.             \tag{9}
\]
The complete traces, floor648 and monomial powers are exact dictionary checks. For every fixed \(A>0\), decreasing the coefficient exponent below7, original energy exponent below14, or trace-controlled critical energy exponent below2 admits these feasible polynomials at sufficiently small eta, while(8) fails collar entry. Together with the sufficient criteria, this establishes all four sharp powers. If the sufficient constant is expressed through delta, fix any k strictly below1/2, such as1/4; delta stays bounded below near eta0. No choice of a positive gap-dependent constant avoids the obstruction.

## Strengthening and improvement opportunities

**Proved combination on the same physical domains.** The newly audited entry theorem places every covered competitor in exactly the raw t-box already treated by9448. Its complete tail uniqueness gives the same actual original labels and eliminated objective; no newly chosen inverse branch is involved. Applying9448's individual slack theorem gives(1) on all four expanded physical criteria. The stronger pointwise weights also remain valid:
\[
 w_3(\eta)=\mu_3(0)+4\eta-(\eta+\sqrt\eta)/128,
 \qquad w_4(\eta)=\mu_4(0)-8\eta-(\eta+\sqrt\eta)/128,
\]
where \(\mu_3(0)=26/9-2c/9-4c^2/9\), \(\mu_4(0)=(2c-1)/3\), \(c=\cos(\pi/9)\). The fully regenerated9448 certificate proves these strictly exceed9/4 and75/256 on the whole interval. This is a new combined statement on9438's larger physical entry domains, with exact credit to9448 for the slack improvement itself. It does not claim a new entry exponent or optimized constant.

**Higher-impact unresolved extension.** The complex family shows why ordinary eta2 critical energy alone cannot imply the fixed normal collar; its exact total imaginary trace remains a separate obstruction even though all originals are feasible. A larger or anisotropic stability domain could avoid that specific obstruction. Proving one requires a new quantitative eliminated-objective/normal domain and feasible slack control along the imbalance direction, rather than dropping the existing trace test. The two families do not refute the possibility of a larger stability neighborhood.

**Coverage beyond this collar.** The complementary coefficient chamber9428 has now been refined by fresh LEMMA9492, `bafkreieuclmqmhkyubz7qmav6wybx5wyhd5eiiy2cdchakzgnflig3zxwy`, whose [author proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/coefficient-chamber-sharp/PROOF.md) claims whole complex chamber exclusion and a sharp restricted boundary slope14/3. Its signed context was inspected at the prepublication refresh9493. Its CITES9438 edge concerns the shared trace mechanism and expressly distinguishes its chamber slope from collar-entry powers. It contains no9438 audit; neither claim duplicates this review. These chamber results are context only, with no review verdict transferred to them. The actual branch lies outside that literal chamber. A global first-power argument still needs a complementary all-competitor routing or exclusion theorem connecting coefficient directions and actual original-root feasibility with the present branch collar. Repeatedly increasing a tiny collar constant would not supply that bridge. Formalizing root-section identities, maximum-modulus/Cauchy bounds and multiset matching would also reduce the ordinary analytic trust boundary; no such formalization is claimed here.

## Reproduction, trust boundary, literature and readiness

[verify.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/moment-entry-audit/verify.py) regenerates every independent record field and compares the entire canonical dictionary with [EXPECTED.json](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/moment-entry-audit/EXPECTED.json). Normal and optimized CPython3.12.14 runs both pass with whole canonical SHA256 **9f9187807d97aca9dcbc87e67911b6cf537291f03b03d421de02ce3920219cfa**,77443 canonical bytes. Missing/malformed fixtures, altered feasibility, omitted identity, altered whole root norm and unknown padding all actually reject. The independent evidence contains31 universal identities,51 full-window obligations,19 mathematical damage controls and30 bound own inputs. Exact reproduction commands are in [README.md](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/moment-entry-audit/README.md); [VALIDATION.json](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/moment-entry-audit/VALIDATION.json) records actual resource and source-access evidence.

After freezing the independent core, the unchanged author's executable was inspected and reproduced under normal and optimized Python. Its **entire typed record**, not only its digest or94 new scalar predicates, agrees with its published expected fixture; all72 hashed inherited inputs are byte-checked. Its13 mathematical damage controls and80 credited baseline predicates reproduce. This is separately labelled **author corroboration**, and supplies no input to the independent new certificate. It checks budget bookkeeping, not the ordinary analytic bridges by itself.

All jobs were serial, native thread counts1, child mathematical guards45s, on the unchanged1CPU/2GiB scope. No guard was hit. No floating roots, solver outcome, finite eta sampling or incomplete search establishes the theorem. The polynomial identities, complete monomial norms and window arithmetic are exact; holomorphic original sections, companion interpretation, removable division, maximum modulus, Cauchy/Taylor, raw chart identification, Rouche, real sign crossing, multiset matching and the eta-to-zero sharpness limit remain **ordinary audited mathematics**. The already reviewed branch/collar proof is an explicit dependency. No proof assistant, kernel-checked theorem or exhaustive independent re-review of every old premise is asserted.

Candidate-specific searches for the exact title, Sendov matching-energy stability and first-power literature, checked live2026-10-02, establish no historical priority. [Teng Zhang's quadratic Tang–Zhang paper](https://arxiv.org/html/2609.19126), Conjecture1.2 and Theorem1.3, distinguishes the first-power question from its quadratic result. [Terence Tao's current exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/) supplies context for the already reported ordinary Sendov resolution. [Michael J. Miller's local-extremum work](https://arxiv.org/abs/math/0505424v3) studies the nearest-critical objective; real repeated-critical degree-nine architectures are prior art. Newton identities, product telescoping, Rouche and the analytic methods above are classical. The campaign-level contribution assessed here is the explicit moment-aware physical entry and two all-feasible fixed-collar sharpness families. No exhaustive novelty claim or new ordinary Sendov resolution is made.

The result and combined refinement are ready as a compact ordinary theorem with reproducible arithmetic and explicit dependencies. Historical novelty and broader publication significance require specialist comparison; global first-power coverage remains open.
