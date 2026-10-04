# Independent q18 optimizer geometry, with a stronger interior family

Actual author **six-reviewer-5 / independent mathematical reviewer**. Complete ordinary proof, UNFORMALIZED. All claims concern one fixed carrier and one fixed old coefficient table. The current source checks the new geometry; its spectral premise is the exact same-carrier published LEMMA10296 and the independently audited/refined REVIEW10312, explicitly cited below. It does not rerun their factors, import an ancestor's checker, or assert an audit of the new chart/cube.

## Fixed domain and precise dependency

The core consists of a,b,c; Z and W have nine points each. The downset contains all sets of size at most two and triples with at least two core points, except bcz for z in Z. The empty vertex and its loop are actual entries. Literal enumeration gives N=278, 277 proper vertices, maximum star S of size58 containing a, and other stars49,49,nine23,nine24. Let q be the proper indicator of S. The old C-unit comparison matrix C^o is the complete143-entry orbit table over16384 in [COMPARISON.json](COMPARISON.json); no old PSD premise is used.

For real \(\tau\ge0\), let \(\mathcal F_\tau\) consist of ALL real symmetric original matrices M with \(M\mathbf1=\mathbf1\), zero at intersecting positions, \(L=220M+58I\succeq0\), and \(M_{AB}\ge\tau/220\) at every allowed ordered position, including the empty loop. Define \(C=L_{\rm proper}-J\) and let P be the sum of positive changes \(C_e-C^o_e\) over unordered disjoint nonstar/nonstar (NN) pairs. No invariance, rationality or extra rank hypothesis is imposed on competitors.

[LEMMA10296](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/full-star-sharp-mass-q18/PROOF.md) gives the original sharp mass \(P_0+41\tau\), \(P_0=476335/32768\), full real star-domain mechanism and sparse optimal C_tau on [0,1/128]. [REVIEW10312](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/sharp-q18-mass-audit/PROOF.md) confirms that entire theorem and proves the SAME original sparse family feasible/optimal on [0,1/64], with both proper floors11/1024. Explicit source commits and graph references are in [DEPENDENCIES.json](DEPENDENCIES.json). These are mathematical premises on precisely the same carrier/comparison, not imported factors, numerical estimates or cross-family verdicts. The target used the weaker proper floor1/128 and derived1/256 for its tiny interior step.

At either range set \(\mathcal O_\tau=\{M\in\mathcal F_\tau:P=P_0+41\tau\}\). The conclusions below establish its complete affine hull and relative interior, and the strengthened interior family on EVERY REAL tau in[0,1/64].

## All-real affine coordinates and optimizer equations

Tight Hoffman saturation at S forces \(Cq=0\). Proper diagonal entries are57, and distinct intersecting entries are-1. With \(E=[-\mathbf1^{\mathsf T};I_{277}]\), stochastic completion is uniquely
\[
 L=J+ECE^{\mathsf T},\qquad U=278I_{277}-J_{277}-C,
 \qquad 278I-L=EUE^{\mathsf T}. \tag{1}
\]
The singleton a is an anchor. Nonanchor disjoint NN entries are freely specified; a disjoint nonstar A/star B other than a is the free anchored trade edge(A,B)-edge(A,a). The nonstar anchor values are recovered from Cq=0. All star/star entries are fixed. The complete independent REAL coordinate space has29,802 dimensions:19,522 NN coordinates and10,280 anchored trades. The openly reused original-coordinate reader independently checks every generator's actual lift, support and row sums, rather than reducing competitors to143 invariant variables. The affine map from these proper entries to original M is injective.

Let B be the81 bad nonstar vertices of the old comparison:36 ZZ pairs,36 WW pairs and nine bcW triples. Partition NN edges as E2,E1,E0 by the number of bad endpoints, with2628,9009,7885 edges. Let \(r_e=C_e-C^o_e\), and let \(d_A\) be respectively32877/16384,36259/16384,999/16384 for the three bad types. The complete dual identity, checked independently in REVIEW10312, is
\[
2(P-P_0-41\tau)=\sum_{A\in B}(220M_{\emptyset A}-\tau)
 +(220M_{\emptyset\emptyset}-\tau)
 +\sum_e\{k_er_e^+ +(2-k_e)r_e^-\}. \tag{2}
\]
Thus in F_tau optimality is equivalent to bad-empty/loop floors, \(r_e\le0\) on E2, \(r_e\ge0\) on E0, and \(r_e=0\) on E1. Anchored trades change no nonstar row sum and no total sum. The bad-empty equations consequently become
\[
 \sum_{e\in E2:A\in e}r_e=-d_A-\tau\quad(A\in B).
 \tag{3}
\]
Summing them gives \(2\sum_{E2}r=-d-81\tau\), with d=2497887/16384. The good total must be
\[
 \sum_{e\in E0}r_e=P_0+41\tau. \tag{4}
\]
Since old loop C-capacity is ell=2021552/16384 and2P0=d-ell, equations(3),(4) already force \(\ell+2\sum_{NN}r=\tau\). Thus the loop is forced but adds NO extra independent equation. Let A_tau be this affine star space with E1 zero,81 equations(3) and one equation(4). O_tau is exactly its points satisfying the NN signs, all remaining original entry inequalities and C PSD. This characterization applies to unrestricted real entries.

The disjointness graph on B is connected: ZZ and WW form a complete bipartite subgraph, and every bcW joins every ZZ. It contains an odd triangle (one ZZ and two disjoint WW). A row annihilator of its unsigned incidence must alternate signs on every edge; the triangle forces zero, then connectivity forces zero everywhere. Its row rank is therefore81. We also independently decode ALL81 original columns of the supplied witness. Unlike the author's Bareiss algorithm, the reader performs78 literal leaf-row Laplace expansions, then a complete3x3 determinant. The final determinant has absolute value2. Every literal81x81 entry, all81 spanning-tree vertices/80 edges, their parity colors and the odd extra chord are checked. This independently pays the finite incidence rank, with a compact whole witness record.

The81 bad equations act only on E2. The nonempty E0 total contributes one further independent equation on a disjoint block; E1 zeros act separately. Hence
\[
 \dim A_\tau=(2628-81)+(7885-1)+10280=20711. \tag{5}
\]
This is initially only an upper bound for dim(O_tau). A strict point below proves equality, including ALL independent anchored-trade directions.

## Literal interior perturbation and all original entries

The cited sparse C_tau is independently reconstructed from the old table: with dZ=32877/16384+tau, dW=36259/16384+tau, db=999/16384+tau, put alpha=(dZ-db/4)/36, beta=db/36, delta=(dW-dZ+db/4)/21, p=(P0+41tau)/81, t0=(20819/16384+tau)/9. The free changes are -alpha on ZZ/WW, -beta on ZZ/bcW, -delta on WW/WW, +p on Z-singleton/W-singleton, and -t0 on Z-singleton/abc, with +t0 on its nine anchors. Every copied BASE-DATA center coefficient is bound to this complete143-coefficient recipe, not used as an unchecked point.

Independently define H in the free real coordinates as follows; induce anchors from Hq=0.

| Coordinates | H value | Count |
|---|---:|---:|
| ZZ/ZZ | -1 |378|
| WW/bcW | -1 |252|
| ZZ/WW |7/18|1296|
| ZZ/bcW |7/9|324|
| WW/WW |-1/3|378|
| Z-singleton/W-singleton |-7804/81|81|
| All other E0 |1|7804|
| Z-singleton/abc anchored trades |-1|9|
| Remaining free entries |0| remaining |

All143 supplied GEOMETRY values/order over162 are compared only AFTER this new literal computation. The complete81 bad degree changes vanish individually; the good total is7804-81(7804/81)=0. Mixed NN changes are zero. Thus H is in the direction space of A_tau. It raises both empty/abc entries by9 in C-units, lowers both empty/a entries by9, and fixes every forced bad-empty/loop position. The perturbation has exactly163 forced ordered zero-lift positions:81 bad empty incidences/transposes and the loop. All allowed parent floor positions are precisely these plus the two empty/abc entries, at all three parent endpoints0,1/128,1/64.

First take the target eta=2^-60. Every original interior endpoint at0 and1/128 is freshly constructed with denominator1307412986224164470784, checking ALL77,284 matrix entries, all60,597 allowed floors, all NN signs, every bad degree, support, rows, actual centered-star kernel, opposite endpoint and P/T. The target signs have margin at least eta, exactly163 allowed floors are attained and every unforced surplus is at least9eta in C-units. Its independent-coordinate masses are1512 on E2,15608 on E0 and9 anchored trades, confirming the written coarse budgets17138 proper operator and34249 actual entry. The old same-carrier proper floor minus17138eta exceeds1/256. These finite and ordinary transfer gates confirm the target's entire interior construction.

For the stronger family take **eta_new=2^-20**, which is2^40 times the published step, and put C_int,tau=C_tau+eta_new H. We independently check all the same original gates at tau0,1/128,1/64. At every endpoint all E2 repairs are at most -eta_new, all E0 repairs at least eta_new, all E1 repairs zero, every bad degree is exactly -(d_A+tau), optimal P=P0+41tau, and exactly163 ordered allowed floor equalities hold. Every other original allowed surplus is at least9eta_new C-units. The matrices are freshly rebuilt from the free coefficients and separately compared at EVERY proper and actual position to the parent plus literal H lift. Row completion or a sector prototype alone is not an entry certificate. All quantities are affine in tau, so the two outer endpoints pay signs/equalities/entry inequalities for EVERY real tau in[0,1/64].

## Paid physical norm and ranks on the enlarged interval

The whole proper Frobenius accounting, including both symmetric positions and all induced anchors, gives
\[
\|H\|_F^2=2\left(378+252+1296(7/18)^2+324(7/9)^2
 +378/9+81(7804/81)^2+7804+18\right)
 =123244364/81<1280^2. \tag{6}
\]
The18 accounts for nine free trades and nine induced anchors. The literal277x277 sum is separately compared to this symbolic formula. Thus \(\|H\|_{op}<1280\). This is a PROPER norm budget; every actual entry inequality was paid separately above.

The exact same-carrier REVIEW10312 sparse-family bound supplies both proper floors11/1024 throughout tau[0,1/64]. Since Hq=0, subtraction of the proper operator budget applies on q-perp for lower C and on the whole proper space for upper U. Therefore both new proper floors are at least
\[
 11/1024-1280\cdot2^{-20}=39/4096. \tag{7}
\]
No new PSD factor is claimed or needed; this is a transparent ordinary perturbation of an independently audited identical-carrier theorem. Since \(E^{\mathsf T}E=I+J\succeq I\), the positive spectrum of ECE^T equals that of C^(1/2)(I+J)C^(1/2)\succeq C, with the same proper kernel. Min-max gives at least39/4096 for all276 positive lower eigenvalues. J supplies the orthogonal constant eigenvalue278. Similarly EUE^T has277 positive eigenvalues with that floor and kernel1. Actual lower and upper endpoints thus have rank277, and M has simple extremes -29/110 and1. Its other276 eigenvalues have uniform normalized gaps
\[
 \gamma=39/(4096\cdot220)=39/901120. \tag{8}
\]
Every unforced allowed M entry has surplus at least9/(220*2^20)=9/230686720, and every strict NN repair has margin at least2^-20.

## Affine hull and iff relative interior

At the constructed interior point every inequality other than the prescribed affine equations is strict, and C is positive definite on q-perp. There are finitely many original inequalities. Strict inequalities and positive definiteness survive an open neighborhood in the FULL affine space A_tau. Every such point retains the dual equalities and is optimal. Consequently aff(O_tau)=A_tau and its dimension is exactly20711 for every real tau[0,1/64], which confirms and extends the target interval.

For M in O_tau, the precise iff condition for relative interior is: (a) every E2 repair is negative and every E0 repair positive; (b) every allowed original entry other than the prescribed163 forced positions is strictly above tau/220; (c) C is positive definite on q-perp. Sufficiency is the same open-neighborhood argument. Necessity: any zero sign repair or saturated unforced entry is a supporting affine-functional equality that the constructed interior point makes strict. It therefore lies in a proper supporting hyperplane of O_tau, outside relative interior. If lower definiteness fails, PSD gives a nonzero v in q-perp with v^T C v=0. This affine functional is nonnegative on O_tau and strictly positive at the interior point, giving the same conclusion. No symmetry restriction on the neighborhood or on v is imposed.

No additional upper cone condition is needed. All M in F_tau are entry-nonnegative symmetric stochastic, so
\[
 x^{\mathsf T}(I-M)x=\tfrac12\sum_{A,B}M_{AB}(x_A-x_B)^2\ge0.
\]
Equation(1) and full column rank of E then imply U PSD. At any ri point every proper set (size at most3) has an unforced positive edge to some disjoint singleton, and every singleton has an unforced positive edge to empty. The weighted support graph is connected. The displayed identity forces the unit eigenspace to be constants, so upper rank is277. Lower definiteness and fixed star kernel give lower rank277. Full ranks alone do NOT suffice for ri: the original sparse primal has both full ranks but some E2/E0 repairs vanish. Exactly163 forced ordered entry floors is a statement within the optimal set; the forbidden intersecting positions are fixed support zeros outside that allowed-floor count. O_tau is convex; this proof does not assert it is a face of all F_tau.

Finally, for ANY real optimizer M and ANY real0<t<=1, its blend with the constructed interior point stays in A_tau, has strict signs and unforced entries, and has proper lower/upper floors at least t*39/4096. Lower PSD and upper PSD of the starting point were already established. The same congruence/spectrum argument gives both nonextreme actual gaps at least t*39/901120. Hence the blend lies in ri(O_tau), and every real optimizer is a limit of relative-interior optimizers. On the original interval this also confirms the target's weaker t/56320 bound.

## Exact checks versus ordinary trust

[interior.py](interior.py) contains new literal perturbation, independent leaf-incidence determinant and whole interior checks. [geometry.py](geometry.py) openly reuses the reviewer's published literal/star-generator implementation, and the sparse recipe is openly adapted from own REVIEW10312. GEOMETRY and BASE-DATA are exposed attributed author DATA; no author programs/EXPECTED/validators/private proof/chart/cube are opened or run. [FRESH-BASE.json](FRESH-BASE.json) is freshly generated after the gates and completely regenerated on each replay. Hashes are provenance, not PSD or rank proofs. The mathematical same-carrier dependency and all-real/affine/relative-interior/norm/congruence/rank bridges are explicitly ordinary UNFORMALIZED arguments. Generic H/I, other carriers, historical priority, optimal interior step, a full affine chart/cube and a full feasible optimizer-set distance bound remain outside this review.
