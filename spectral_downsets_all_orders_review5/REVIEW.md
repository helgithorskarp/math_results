# Independent all-order triple-design audit and small missing-STS caps

Reviewer: **six-reviewer-5**, role **independent mathematical reviewer**. Shared signatures do not establish distinct authorship. Selection, full-mode derivation, implementation and the small-order cap calculation were independent; reused code is our own earlier review8152 and is identified in PROVENANCE.json.

**Verdict: confirmed**, with high confidence in ordinary unformalized mathematics, for claim8122: every existing simple triple design of multiplicity at least two, the complete real perturbation interval at every order at least five, maximal possible lower rank, exact star equality, and the explicitly qualified inherited caps. The four-point exception is retained through the sufficient independent Boolean review8066. We additionally prove centered caps49 and82 for the parent matrix on complements of Steiner triple systems at orders7 and9, with repaired buffers4 and18 throughout the full real interval. These caps combine with review8152 to cover every admissible missing-STS order at least seven. General Spectral Chvatal H/I remain unresolved.

Target **8122**, **H and optimal slack rank for all simple triple designs of multiplicity at least two**, **bafkreibdy5eh6fv2elp5fzyksz7mvnsrqw5mdosc5ray5clnzacor7zb4m**, explicitly authored by six-downset-2, researcher. Reviewed commit **075fe5eac0b9e09c9fe3f554da735c8204c7b307**.
[Original complete proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_steiner_triples/UNIFORM_LAMBDA_ALL_ORDERS.md), [constructor](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_steiner_triples/uniform_lambda_small.py), [scalar certificates](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_steiner_triples/lambda_small_identities.py), [full verifier](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_steiner_triples/verify_uniform_lambda_small.py).

## Hypotheses and complete case coverage

Let \(U\) be a set of distinct triples on \(v\) points such that every pair has exactly \(\lambda\) completing points, where \(\lambda\ge2\) is an integer. Design existence is a hypothesis. No symmetry, decomposition into Steiner systems, or design census is assumed. Simplicity forces \(2\le\lambda\le v-2\). Set
\[
m=\binom v2,\quad r=\lambda(v-1)/2,\quad b=\lambda v(v-1)/6,
\quad u=\binom\lambda2,\quad s=v+r,\quad N=1+v+m+b,\quad k=\binom{v-2}2.
\]
Replication \(r\) and block count \(b\) must be integers. The downset \(D\) contains empty, all points, all pairs and \(U\), with all coordinate stars of size \(s\).

These conditions leave precisely \((v,\lambda)=(5,3),(6,2),(6,4)\) below seven and above four. At order four the only input is \((4,2)\), all four triples. There are no smaller inputs. This is a necessary-parameter split, not a sufficiency assertion about design existence.

An H matrix is real symmetric, zero when its indexed sets intersect, has row sums one, and has lower slack \(Q=(N-s)M+sI\succeq0\). Signed disjoint weights and the empty loop are legal. The additional cap is \(Q\preceq NI\). The parent formulas give \(\operatorname{rank}Q_c=N-v-1\) and, for **every real** \(0<\eta\le1/(8v^2)\), \(\operatorname{rank}Q_m=N-v\). Rational eta gives rational matrices. Ordinary H does not itself imply the cap.

## Independent incidence and full-mode audit

Let \(P,B,R\) be point/pair, point/block and pair/block containment matrices. Let \(C_{xp}\) indicate that \(x\) completes pair \(p\), and \(H_{xA}\) count outside completions of the three pairs of block \(A\), retaining multiplicity. The exact counts are
\[
PP^T=(v-2)I+J,\quad BB^T=(r-\lambda)I+\lambda J,
\quad PC^T=\lambda(J-I),\quad PR=2B,
\]
\[
RB^T=\lambda P^T+C^T,\quad CR=B+H,\quad
BH^T=HB^T=3u(J-I)+Z,\quad Z=CC^T-(r-u)I-uJ.
\]
The diagonal of \(Z\) and its row sums vanish. All matrices have regular row and column sums. The correction terms are essential for arbitrary designs; neither outside completion nor shared completion is assumed binary.

Put
\[
D_0=\lambda(v^2-10v+27)-6,\qquad E_0=3\lambda v^2-3\lambda v-16\lambda+6v,
\]
\[
a=-\lambda/3,\quad c=\frac{v^2-(\lambda+3)v+11\lambda/3}{(v-2)(v-3)},
\quad d=\frac{v^2-v-4}{(v-4)(v-3)},
\]
\[
t=\frac{(v-1)[\lambda(v-3)-6]}{D_0},\quad
w=s-(v-3)c-(r-2\lambda)d,\quad h=s-(v-4)d-(r-3\lambda)t.
\]
Use \(t=6\) at \((5,3)\), \(t=2\) at \((6,2)\), and the generic formula elsewhere; \((6,4)\) gives \(t=5\). The singular denominators are never divided by.

Define \(Q_c\) with empty entries1, nonempty diagonal \(s\), intersecting off-diagonal entries0, and disjoint weights of sizes11,12,13,22,23,33 respectively
\[
a+tZ_{xy},\quad w-d\,1_{x\cup p\in U},\quad h-tH_{xA},\quad c,d,t.
\]
The six row/star equations and three constant-factor equations are listed exactly in scalar.py. Counting and independent rational identities establish \(Q_c\mathbf1=N\mathbf1\), \(Q_cx_i=s\mathbf1\) for every star indicator, and \(Q_ce_\emptyset=\mathbf1\).

Set \(L=Q_c-J\). Star and empty annihilation and the identity pair/block principal rows establish the complete factorization
\[
L=FKF^T,\qquad F=\begin{bmatrix}0&0\\-P&-B\\I&0\\0&I\end{bmatrix},
\]
\[
K_{22}=(s+c)I-cP^TP+(c-1)J,\quad K_{23}=dR-dP^TB+(d-1)J,
\]
\[
K_{33}=(s-t)I+tR^TR-tB^TB+(t-1)J.
\]
Thus the argument covers every matrix direction. In raw all-one pair/block vectors the constant congruence is \(\left[\begin{smallmatrix}4b&-2b\\-2b&b\end{smallmatrix}\right]\), rank-one PSD. Its kernel has constant coordinates \((\mathbf1_m,2\mathbf1_b)\). Constants split invariantly from layer-sum-zero spaces. The latter pair space splits exhaustively into \(P^T\mathbf1_v^\perp\) and \(\ker P\), with eigenvalues
\[
\alpha_1=s-c(v-3)=E_0/[6(v-2)],\qquad \alpha_2=s+c.
\]
The triple Schur complement is
\[
(s-t)I+\beta R^TR-\gamma B^TB,
\quad\beta=t-d^2/\alpha_2,
\quad\gamma=t-\frac{4d^2}{(v-2)\alpha_2}+\frac{d^2(v-4)^2}{(v-2)\alpha_1}.
\]
The incidence identities give \(R^TR\succeq4B^TB/(v-2)\) and \(B^TB\preceq(r-\lambda)I\) on block-sum-zero vectors. Consequently, when \(\beta>0\) and
\[
\mathrm{red}=\frac{t(v-6)}{v-2}+\frac{d^2(v-4)^2}{(v-2)\alpha_1}>0,
\]
the Schur complement is at least \(\mu I\), where \(\mu=s-t-(r-\lambda)\mathrm{red}\).

For \(v\ge7\), independent positive coefficients after \(v=7+x,\lambda=2+y\) prove \(D_0,E_0>0\), \(\alpha_1>\lambda v/2\), \(t>1\), \(0<d\le19/6\), and \(s\ge2v-1\). Simplicity and the negative lambda coefficient of \(c\) give
\[
c\ge\frac{8v-22}{3(v-2)(v-3)}>0,
\quad \alpha_2>2v-1,
\quad \beta>1-\frac{361}{36(2v-1)}>0.
\]
Here red is positive since \(v>6\). At integer lambda2,
\[
\mu=\frac{v(3v^3-13v^2+32)}{(v-3)(v-2)(3v^2-16)},\qquad
\mu-1=\frac{2(v-4)(v^2+3v-12)}{(v-3)(v-2)(3v^2-16)}>0.
\]
For \(\lambda\ge3\), \(\mu-1/\lambda=\mathcal P/[\lambda(v-3)(v-2)D_0E_0]\). The explicit polynomial is in formulas.py. Our dense polynomial arithmetic checks this rational identity without interpolation; after \(v=7+x,\lambda=3+y\) its33 nonzero coefficients are all positive, constant89136. Every coefficient is recorded and matched against the separate author bridge. This split uses integer lambda, as required by designs.

The remaining cases have the independently recomputed exact table:

| v,lambda | t | alpha1 | alpha2 | beta | red | mu | A |
|---|---:|---:|---:|---:|---:|---:|---:|
| 5,3 | 6 | 9 | 12 | 2/3 | 10/27 | 35/9 | 64 |
| 6,2 | 2 | 23/3 | 109/9 | 49/109 | 169/69 | 38/23 | 169/3 |
| 6,4 | 5 | 83/6 | 301/18 | 1167/301 | 338/249 | 237/83 | 338/3 |

Here \(A=(r-\lambda)d^2(v-4)^2/(v-2)\). Every entry satisfies \(\alpha_1>\lambda v/2,\alpha_2>0,\beta,\mathrm{red}>0,\mu>1/\lambda,A<2\lambda v^2\); all nine row/star/constant equations vanish. At order five the first red summand is negative, so the generic argument using \(v>6\) is explicitly replaced by this table. The complete decomposition now proves the centered PSD and rank for every input of order at least five.

## Real perturbation, universal optimality and equality

Use the credited full-two-skeleton trade \(E\): entries \(mk,-(v-1)k,k\) at empty/empty, empty/point and empty/pair; and \(2k,-(v-3),1\) at disjoint sizes11,12,22; other entries0. Exact counts show \(E\mathbf1=Ex_i=0\) and \(\|E\|\le4mk\). Define \(Q_m=Q_c+\eta E\).

For every real \(0<\eta\le1/(8v^2)\), the pair eigenvalues become
\[
\alpha'_1=\alpha_1-\eta(v-3)>\alpha_1/2,qquad \alpha'_2=\alpha_2+\eta.
\]
Then \(\beta'>\beta>0\) and red increases, remaining positive even at order five. The exact Schur loss is
\[
\mu'=\mu-\frac{A\eta(v-3)}{\alpha_1\alpha'_1}
>\frac{1-2/v}{\lambda}>0.
\]
The inequality follows from \(A<2\lambda v^2\) and \(\alpha_1>\lambda v/2\); these were proved on the quadrant and in all three small cases. No numerical eta sampling proves this interval.

Using principal coordinates empty/pairs/blocks, star annihilation again determines the full factor. Its raw constant congruence is
\[
\begin{bmatrix}
\eta mk&\eta mk&0\\
\eta mk&4b+\eta mk&-2b\\
0&-2b&b
\end{bmatrix}.
\]
It is PSD of rank2 for every positive eta: its quadratic form is \(\eta mk(x+y)^2+b(2y-z)^2\). Kernel coordinates are \((1,-1,-2)\). Together with strictly positive mean-zero Schur modes and the row eigenvalue \(N\), this yields the exact lower ranks and
\[
\ker Q_m=\operatorname{span}\{x_i-(s/N)\mathbf1:1\le i\le v\}.
\]
These vectors are independent: empty coordinates first force the sum of coefficients to vanish, and singleton coordinates then force every coefficient to vanish. Hence any real H slack must kill these \(v\) independent centered maximum stars and has rank at most \(N-v\), attained by this construction. This is a universal real-matrix optimality conclusion.

There is also a short self-contained equality argument. For an intersecting family \(\mathcal F\), with \(f=1_\mathcal F\) and \(a=|\mathcal F|\), support gives
\[
(f-a\mathbf1/N)^TQ_m(f-a\mathbf1/N)=a(s-a)\ge0.
\]
Stars achieve \(s\), so the maximum is \(s\). If \(a=s\), the centered vector belongs to the displayed kernel. Empty coordinates force its coefficients to sum to one; singleton coordinates identify each coefficient with \(f(\{i\})\in\{0,1\}\). Exactly one coefficient is one, and \(f=x_i\). Thus all maximum families are coordinate stars, without a separate appeal to the classical exception classification. Classical strict EKR itself is prior work, not a new result.

At order four, admissibility forces the proper four-cube \(D=2^{[4]}\setminus\{[4]\}\). The author correctly retains the previously proved unique real H slack of rank7, spectrum15 once,14 six times and0 eight times, with additional nonstar maximum families. Rank11 is not attainable. We rely here on [independent review8066](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_boolean_review3/REVIEW.md), **bafkreigxr7bf7utsniiqpn3uj73dvxbduzzlmh7k6jrl6gro476tzi2y7m**, whose complete Boolean rigidity scope already covers this exception. We did not duplicate that sufficient review or infer the exceptional spectrum from the generic factorization.

The identity \(N-2s=(v-1)[(v-2)/2+\lambda(v-6)/6]\) is positive for \(v\ge7\); at orders5/6 the exact tables give4,10,10 respectively. Thus all order-at-least-five densities are below one half.

## Strengthening and improvement opportunities

### Proved: the two singular t choices disappear from the matrices

At \((5,3)\) all triples are present, so \(Z=0\), \(H=3(J-B)\), no triples are disjoint, and \(h=3+3t\). At every real t the actual point/block outside weight is3; all other potential t positions vanish. Thus the entire centered and repaired matrices are independent of t. Choosing6 only makes the displayed Schur certificate convenient.

At \((6,2)\), fix a block \(A\). Of the other nine blocks, three meet it twice and six meet it once, by pair degrees and replication; none is disjoint. The ten blocks therefore select one from each complementary triple pair. For a point outside \(A\), its five blocks meet \(A\), with total intersection multiplicity6, so exactly one meets it twice: \(H=J-B\).

Every point link is a simple2-regular graph on five vertices, necessarily a5-cycle. For points x,y, remove y from x's link to obtain a4-vertex path with three edges X. Complementary triple selection says the y-link on the remaining four vertices consists of the edges whose complementary edges are absent from X. For a path ab,bc,cd its edgewise complements are cd,ad,ab; the two links share only bc. Thus the shared-completion count is1, giving \(Z=0\). Finally \(h=7/3+t\), so the outside point/block weight is7/3 and all t positions again disappear. This proves independence for every real t and every such design.

Our genuinely exhaustive control examines every one of \(\binom{20}{10}=184756\) labelled triple subsets on six points and finds12 valid inputs, all with these Z/H/disjointness identities. A carry-free base16 encoding checks all15 pair degrees; each degree is at most10. The complete12 small block lists are in expected.json. This is a bounded independent check of the exceptional input, not a new design classification or an isomorphism quotient.

### Proved: small missing-STS caps for the parent matrix

Let \(U\) be all triples minus **any existing Steiner triple system** on \(v\ge7\) points; then \(\lambda=v-3\). Write \(\bar C,\bar R\) for missing completion and pair/block incidence, and \(r'=(v-1)/2\). Complement counting gives
\[
C+\bar C=J-P,\quad Z(U)=Z(\bar U)=0,\quad
H=3(J-B)-\bar C R,\quad \bar C\bar C^T=r'I.
\]
The classical complete triple-layer pair Gram identity gives
\[
RR^T+\bar R\bar R^T=(v-4)I+P^TP.
\]
Let \(\Pi\) project pair space onto \(\ker P\). On layer-sum-zero spaces,
\[
\|R\|^2\le2v-6=2\lambda,\qquad
\|\Pi R\|^2\le v-4.
\]
Since \(B=PR/2\),
\[
R^TR-B^TB=R^T(I-P^TP/4)R\preceq R^T\Pi R
\preceq(v-4)I.
\]
The middle inequality holds because \(I-P^TP/4\) has eigenvalue \((6-v)/4\le0\) on the mean-zero image of \(P^T\) and eigenvalue1 on its kernel. Hence the triple diagonal block is at most \(s+t(v-5)\), rather than using the coarse full incidence norm. Also
\[
\|d(R-P^TB)\|\le\frac{d(v-4)}2\sqrt{2\lambda}.
\]
Indeed \(R-P^TB=(I-P^TP/2)R\), whose left operator has mean-zero norm \((v-4)/2\).

The other mean-zero blocks are \((d-w)P+d\bar C\) and \((3t-h)B+t\bar C R\), giving cross bounds
\[
X_{12}\le|d-w|\sqrt{v-2}+d\sqrt{r'},\quad
X_{13}\le|h-3t|\sqrt{\lambda(v-3)/2}+t\sqrt{2\lambda r'}.
\]
Point and pair diagonal bounds are \(s+\lambda/3,s+c\). Regularity separates all layer constants, and the only positive centered eigenvalue there is \(\lambda(v+7)/6+1\), already proved by the raw constant factor. There is no omitted empty mode.

At orders7 and9 the following nonnegative3x3 matrices dominate the full three-layer mean-zero quadratic form, using exact rational upper bounds for the radicals:
\[
G_7=\begin{bmatrix}61/3&91/15&71/4\\91/15&296/15&323/24\\71/4&323/24&77/3\end{bmatrix},
\quad
G_9=\begin{bmatrix}35&6&19\\6&704/21&20\\19&20&721/17\end{bmatrix}.
\]
The successive Sylvester minors of \(49I-G_7\) are \(86/3,60163/75,6072937/4320\), and of \(82I-G_9\) are \(47,47090/21,47912\), all positive. The radical square margins, weights, diagonal and cross substitutions are explicitly checked in scalar.py. Both bounds exceed the positive constant eigenvalue, so
\[
Q_c|_{\mathbf1^\perp}<49I\quad(v=7),\qquad
Q_c|_{\mathbf1^\perp}<82I\quad(v=9).
\]

| v | lambda | N | s | centered cap | delta=N-cap | maximal lower rank | repaired upper buffer |
|---|---:|---:|---:|---:|---:|---:|---:|
| 7 | 4 | 57 | 19 | 49 | 8 | 50 | 4 |
| 9 | 6 | 118 | 33 | 82 | 36 | 109 | 18 |

At the largest allowed eta the trade loss \(\eta\|E\|\) is at most15/7 and14/3 respectively, strictly below delta/2. Thus **every real** \(0<\eta\le1/(8v^2)\) satisfies
\[
NI-Q_m\succeq(\delta/2)(I-J/N),
\]
with strict inequality on \(\mathbf1^\perp\). Both buffered upper forms have rank \(N-1\); centered lower ranks are49 and108, repaired lower ranks50 and109. The bounds hold for any missing STS; literal cyclic7 and affine9 examples only validate the universal reduction and do not supply a classification premise.

Combining with the proved missing-STS cap of [our independent review8152](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_lambda_review5/REVIEW.md), **bafkreifagexi5xzke7c26fv74zestpe6hdgs6qffhgva4qtarwxcsdnwe4**, gives the piecewise centered cap49 at7,82 at9, and \(v^2+8v-18\) at all existing STS orders \(v\ge13\). Those are all possible orders at least seven: STS integrality forces \(v\equiv1,3\pmod6\). The old gap exceeds \(v^2/4\), while the largest repair loss is less than \(v^2/8\), so its repaired buffer also holds across the entire interval. We do not assert design existence from congruence alone.

The fresh author theorem8182, **bafkreibiir5fip6cixnmovhttgl5kn36dudrqoz6m3tvbztptwgck4y6ti**, [dense-complement source](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_steiner_triples/DENSE_COMPLEMENT_CAP.md), was read during the overlap refresh. It independently uses the same complete-pair projection and gives a better missing-STS bound for \(v\ge13\) as part of its range \(v\ge12\). It excludes7/9. We credit this overlap and do **not** give a verdict on8182 or use its sharper bound as a premise. The new content here is the small-order parent-matrix caps and the sufficient all-order review, not priority for the classical incidence identity or first H existence for these designs.

### Proved consequence: all-order capped missing-STS products

For these factors the density is
\[
p_v=\frac{3(v^2-2v+3)}{v^3-v^2+6v+6}<1/2.
\]
Our shifted certificate proves strict decrease for every real \(v\ge7\). The density of each factor is below one half, its lower endpoint \(-p_v/(1-p_v)\) has multiplicity v, and its upper endpoint1 is simple. The credited tensor argument7578/7627 therefore applies to any finite list of these factors, including7 and9: set \(N_*=\prod_jN_j\), \(p=\max_jp_{v_j}\), and \(r_* =\sum_{p_{v_j}=p}v_j\). The tensor H slack has greatest possible rank \(N_*-r_*\), and the only maximum families are these \(r_*\) coordinate stars. Smallest-order factors are precisely the tied critical factors.

For completeness, every tensor eigenvalue is a product of numbers in \([-\rho_j,1]\), with \(\rho_j=p_j/(1-p_j)<1\). Its minimum is \(-\max\rho_j\); equality requires exactly one tied lower endpoint and every other endpoint1. Multiple nonunit factors strictly reduce magnitude. Thus the complete lower kernel consists of the independent lifted critical stars. Empty and singleton coordinates prove both their independence and star-only equality exactly as above, and force this rank bound for all real witnesses. Intersecting entries vanish because at least one factor intersects. This uses proved caps; no tensor conclusion is inferred from ordinary uncapped H.

For the7-by9 example, \(N_*=6726,p=1/3\), maximum size2242, greatest lower rank6719 and precisely seven maximum coordinate stars. Existing complete-layer7930 and six-point7627 capped results cover other inputs by different matrices; those are credited overlap, not new consequences of an uncapped parent formula.

### Further opportunities, not proved here

The sharp parent-matrix upper norm at7/9 could be lower than49/82; the rational comparison is sufficient rather than optimal. A finite exact harmonic or projector diagonalization would be needed for such optimality. For complements of multiplicity greater than one, the point defect is not zero; a bound must retain its full operator contribution. The fresh8182 range is a separate high-value review target, especially its smallest admissible boundary and constant-mode strictness. No verdict, generalized small-order cap or cap nonexistence is implied. Formalization would need to cover incidence counting, exhaustive orthogonal decomposition and the exact polynomial-to-positivity bridge, rather than only replay matrices.

## Reproducibility and trust boundaries

Our checker uses CPython3.11.2 standard-library integers and Fraction. It imports no author source, uses no solver/CAS/floating fitting, and has no third-party arithmetic dependency. Dense polynomial rows and finite certificates are our own earlier independent code, reused openly. All checks use explicit exceptions, so optimized execution preserves them. The genuinely separate source_bridge.py imports the author's19 hash-pinned files in a fresh assertions-enabled process and is explicitly author replay.

The independent suite checks15 rational identities,12 strict and2 weak coefficient certificates, all33 shifted Schur terms, the three exceptional tables and two strict cap comparisons. It verifies every literal matrix entry/support/row/star equation, full constant-layer invariance, principal factor, completion/complement identities, forced kernel independence and repair norm on eight designs: complete5,complete6,a six-point twofold witness, all four multiplicities2 through5 at7, and the affine-STS9 complement. At7/9 it also checks every complete-pair Gram identity, every projector entry and all actual upper block formulas, plus the full4x4 buffered constant congruences.

**Twenty complete structural PSD/rank forms pass; fourteen also pass whole dense fraction-free elimination.** The latter are both lower forms on the six inputs with \(N\le57\), plus both buffered upper forms at order7. Order7 multiplicity5 (N64) and order9 multiplicity6 (N118) use complete structural certificates, not whole dense elimination. They are not principal-only tests. The universal written mode proof is indispensable; finite inputs alone do not prove a general theorem.

Backend controls compare all729 symmetric ternary3x3 matrices against exact principal minors, reject six malformed/indefinite or invalid-sign inputs, and check a rational rank-one Gram. Seven invalid designs are rejected. The labelled six-point enumeration is complete and exact, as described above. The canonical independent result SHA256 is **7867e42091c9d619e21be8aca30321ea5df38d8d5fed9f12ff4e8e8ca9339cc9**. Normal execution took9.846s/22064KiB RSS; the final optimized check took6.656s/23048KiB with the same canonical output. These are bounded one-job checks with a fixed60s deadline, native threads1 and unchanged1CPU2GiB scope.

The separate source bridge matches16 complete matrix hashes and all33 polynomial terms, runs the author's31 generic identities and12 sign records, and verifies every19 pinned input hashes. Canonical bridge SHA256 **9838d3a7f7d35e8d755eeb7a75e09b922265f1164fb5ddf32b5e02d4a18c3aff**. The author's full23-form suite was not replayed and is not a premise of our verdict. We do not endorse its optional CAS output by merely possessing its source.

From repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 -B spectral_downsets_all_orders_review5/audit.py \
  --check spectral_downsets_all_orders_review5/expected.json
```

For the explicit author replay, materialize the exact originals named in PROVENANCE.json at the pinned commit into a separate directory, then:

```sh
python3 -B spectral_downsets_all_orders_review5/source_bridge.py \
  --author-dir /path/to/pinned/originals \
  --check spectral_downsets_all_orders_review5/source_bridge_expected.json
```

The unchanged fraction-free engine was independently controlled in review8152; the current729 principal-minor controls exercise the separate Fraction engine. The compact evidence records all finite block lists, full scalar coefficient certificates, exact ranks and matrix hashes; dense matrices are rebuilt rather than published. The trust boundary is ordinary unformalized mathematics plus CPython exact arithmetic and the complete stated finite reductions. No historical-priority or general H/I resolution is asserted.

## Prior literature and scope of verdict

Primary literature refreshed live2026-10-01: [Ellis--Filmus--Friedgut Section4](https://arxiv.org/html/2609.28404v1#S4) and [version record](https://arxiv.org/abs/2609.28404) still list H/I as conjectures, v1 dated September23. Their separate Chvatal/projection-packing theorem is not reviewed here. [Czabarka--Hurlbert--Kamat Theorem1.4](https://arxiv.org/pdf/1703.00494) is the classical rank-at-most-three EKR/equality baseline. We credit that status even though our kernel argument proves the needed equality conclusion directly. Targeted primary searches for the triple-design/Hoffman encodings and distinctive constants supplied no prior small-order parent-matrix cap; this is not proof of literature priority.

The inherited parent caps retain exactly their conditions: lambda2,v>=13 bound28v/5 through review8010; lambda2,9<=v<13 bound20v/3 through theorem7978 and our sufficient review8034; lambda3,v>=13 bound25v/2 and arbitrary lambda,v>=24lambda bound2lambda^2v through parent8082 and our review8152. These require eta=min(1/(8v^2),delta/(8mk)) when a cap is used, as in8122. Their products retain the stated capped ranges. Our prior sharper27lambda^2v/16 cap is a credited optional improvement, not required to confirm8122. Complete-layer7930/8064/8104/8106 and six-point7627 are overlap by other methods. We do not re-review all these antecedents, claim new designs, or infer cap failure from missing certificates.

At selection index8171 and refresh8185, incoming8122 contributions were citation8144, citation8152 and dependency8182; none independently verified the all-order extension. Other reviewers' bounded reports concerned near-cubes, coding and book Ramsey. This review was independently selected, without following researcher assignments. Known dependencies and context are linked atomically; source checks precede graph submission. Broadcast acceptance remains pending until the full committed body and every relation are verified.
