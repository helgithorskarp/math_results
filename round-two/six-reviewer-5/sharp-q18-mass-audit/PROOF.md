# Sharp q18 repair mass: independent reconstruction and two refinements

Actual author: **six-reviewer-5 / independent mathematical reviewer**. This is an ordinary, UNFORMALIZED, exact computer-assisted proof. All conclusions concern one fixed carrier and the fixed comparison coefficient table of LEMMA10276. The data are explicitly exposed, attributed inputs. Own published literal and physical-frame code from REVIEW10302 is adapted; no previous PSD certificate or reviewer verdict is a premise.

## 1. Literal carrier and all-real competitors

Let the core be \(a,b,c\), and let \(Z,W\) be disjoint nine-element pools. The downset \(D\) contains all sets of size at most two and triples with at least two core points, except \(bcz\) for \(z\in Z\). Include the actual empty set. Direct enumeration gives \(N=278\), star sizes \(58,49,49,23^9,24^9\), unique largest star \(S_a\), and \(h=N-s=220\).

A competitor is any REAL symmetric original matrix \(M\), with \(M\mathbf1=\mathbf1\), zero on every intersecting pair, including every proper diagonal, and tight lower Hoffman condition \(L=220M+58I\succeq0\). Impose the original-entry floor \(M_{AB}\ge\tau/220\) on EVERY allowed ordered pair, including the empty loop. Here \(\tau\ge0\). Nonnegative stochasticity implies \(M\preceq I\); equivalently the upper cap holds. No orbit invariance, rationality, particular factors or simple ranks are assumed for competitors.

Set \(E=[-\mathbf1^{\mathsf T};I_{277}]\). Stochasticity uniquely gives
\[
 L=J+ECE^{\mathsf T},\qquad
 278I-L=EUE^{\mathsf T},\qquad U=278I_{277}-J_{277}-C.
\]
Thus \(C=L_{\rm proper}-J_{277}\), its diagonal is 57 and every intersecting off-diagonal is -1. Let \(q=\mathbf1_{S_a}\) in proper coordinates. Support and tight Hoffman saturation give \((\mathbf1_{S_a}-58\mathbf1/278)^{\mathsf T}L(\mathbf1_{S_a}-58\mathbf1/278)=0\). PSD forces the centered vector into the kernel, hence \(Cq=0\). The proper singleton \(\{a\}\) is an anchor. Every other disjoint proper off-diagonal is a free coordinate. For a nonstar row its anchor entry is uniquely recovered from \(Cq=0\). Star rows need no additional free restriction because their star entries are fixed. This gives a COMPLETE affine space of 29,802 independent real coordinates: 19,522 nonstar/nonstar (NN) unit edges and 10,280 nonstar/star anchored trades. Each generator has its own unique nonanchor entry. The literal checker validates every generator, its \(ERE^{\mathsf T}\) completion, support and all row sums. This proves coverage of all real competitors, rather than just the invariant slice.

## 2. Universal dual identity and equality conditions

Let \(C^o\) be the exact old comparison table in [COMPARISON.json](COMPARISON.json), denominator 16,384, with its actual completion \(M^o\). Use C-units: \(220M^o\) is the completed numerator matrix divided by this denominator. The old negative empty incidences have 82 proper neighbors. Precisely 81 are NONSTAR: the 36 pairs in each pool and nine \(bcw\) triples. The remaining neighbor is the star triple \(abc\). Write this nonstar set as \(B\). Exact full-row calculation gives
\[
 d=-\sum_{A\in B}220M^o_{\emptyset A}=2497887/16384,
 \quad \ell=220M^o_{\emptyset\emptyset}=2021552/16384,
 \quad (d-\ell)/2=476335/32768=:P_0.
\]
For every unordered NN edge \(e\), define \(r_e=C_e-C^o_e\), \(r_e^+=\max(r_e,0)\), \(r_e^-=\max(-r_e,0)\), \(k_e=|e\cap B|\), \(P=\sum r_e^+\), and \(T=\sum r_e^-\). The \(k=0,1,2\) counts are 7885,9009,2628. Let \(b_A=220M_{\emptyset A}-\tau\) and \(b_*=220M_{\emptyset\emptyset}-\tau\). Every anchored trade changes neither the bad empty entries nor the loop. An NN unit edge changes their sum by \(-k_e\) and the loop by 2. Consequently
\[
 \sum_B b_A=-d-81\tau-\sum_e k_er_e,
 \qquad b_*=\ell-\tau+2\sum_e r_e.
\]
Adding these equations, separating positive and negative parts, gives the identity for EVERY real competitor:
\[
 2\bigl(P-P_0-41\tau\bigr)
 =\sum_{A\in B}b_A+b_*+
 \sum_e\bigl(k_er_e^+ +(2-k_e)r_e^-\bigr). \tag{1}
\]
The reader independently checks the constant, floor coefficient 82, every actual generator column, and both formal positive/negative coefficients of every NN column. All terms on the right are nonnegative. Therefore \(P\ge P_0+41\tau\). Equality is equivalent to all 81 bad empty entries and the loop being at the floor, good/good NN changes being nonnegative, bad/bad changes being nonpositive, and all mixed bad/good NN changes being zero, together with the remaining original-entry and PSD feasibility conditions. Anchored trades retain their independent freedom subject to those conditions. No restriction to five orbit variables enters this lower bound.

## 3. A new sparse primal, with every original entry checked

Put
\[
 d_Z=32877/16384+\tau,\quad d_W=36259/16384+\tau,
 \quad d_b=999/16384+\tau,
\]
\[
 A=(d_Z-d_b/4)/36,\quad B_0=d_b/36,\quad
 W_0=(d_W-d_Z+d_b/4)/21,
\]
\[
 p=(P_0+41\tau)/81,\qquad t=(20819/16384+\tau)/9.
\]
Relative to \(C^o\), change every disjoint pair of the following types by the indicated amount:

| Proper types | Change | Unordered count |
|---|---:|---:|
| ZZ / WW | \(-A\) | 1296 |
| ZZ / bcW | \(-B_0\) | 324 |
| WW / WW | \(-W_0\) | 378 |
| Z singleton / W singleton | \(+p\) | 81 |
| Z singleton / abc | \(-t\) | 9 |

The last nine changes also induce \(+t\) at Z singleton / anchor. All other free coordinates are unchanged. The reader constructs the literal whole \(C,U,L,M\) at \(\tau=0,1/128,1/64\), denominator 148,635,648. It binds ALL 143 exposed center coefficients to these independently computed formulas. At each endpoint, all 77,284 original matrix positions and 60,597 allowed inequalities are checked, including the loop. All 81 bad incidences and the loop equal \(\tau\) in C-units. The NN sign counts are 81 positive, 1998 negative, 17443 zero, with
\[
 P=P_0+41\tau,\qquad T=d/2+(81/2)\tau.
\]
All penalties in (1) vanish. At zero the allowed-zero count is 165 ordered positions (82 incidences in both directions and the loop). Other endpoint entries obey their floors. Since every original entry minus its floor is affine in \(\tau\), checking the two outer endpoints proves ALL entry inequalities for every REAL \(0\le\tau\le1/64\), once PSD below is established.

## 4. Fresh physical PSD at the midpoint

At \(\tau=1/128\), all original coefficients are independently reconstructed. [blocks.py](blocks.py) constructs 277 literal proper-coordinate basis vectors with sector dimensions TT23, Z64, W72, ZZ27, WW27, ZW64. TT consists of all orbit indicators. Each standard sector has its complete eight copies; their physical copy Gram has diagonal 2 and off-diagonal 1, and is positive definite. Pair sectors are the 27-dimensional incidence kernels with exact free-pivot decoders, and mixed rectangles have 64 exact free pivots. All 76,729 basis Gram positions check cross-sector orthogonality and the physical standard-copy metric. These constructive ranks and counts prove completeness. Every one of 153,458 lower/upper action positions is checked; no prototype-only PSD inference is accepted.

For each TT/Z/W lower or upper prototype Gram \(G\), the exposed lower triangular dyadic factor \(V/2^{32}\) is DATA. The exact residual is freshly calculated as \(R=G-VV^{\mathsf T}/2^{64}\), using common denominator \(\operatorname{lcm}(148635648,2^{64})\). In particular TT lower uses 10,459,303,889,793,315,766,272. Let \(m_i\) be the literal physical masses. Every row satisfies \(R_{ii}-\sum_{j\ne i}|R_{ij}|\ge m_i/16>0\). The residual inequality follows directly from \(2|x_ix_j|\le x_i^2+x_j^2\); hence \(G\succeq\operatorname{diag}(m_i)/16\). Factor PSD is an algebraic identity, with no numerical factorization trust. Author compiled margins are checked only after the independent computation. All six scalar Grams are separately recomputed and give the same or better physical floor. The standard copy Gram transfers each prototype floor to all copies; pair/mixed action is scalar on the complete sectors.

For lower TT, delete only the singleton anchor coordinate from the energy certificate, not a vertex from the carrier. The sole lower kernel is \(q\). For an arbitrary \(v\perp q\), subtract a multiple of \(q\) to obtain the certified anchor-zero section \(w\). Since \(v\perp q\), \(\|w\|^2=\|v\|^2+\lambda^2\|q\|^2\ge\|v\|^2\), and \(v^{\mathsf T}Cv=w^{\mathsf T}Cw\). Thus the proper lower floor is at least 1/16 on \(q^\perp\). The full upper proper matrix has floor at least 1/16. The physical, nonorthonormal basis and lower section arguments are ordinary analytic bridges, explicitly UNFORMALIZED.

## 5. Proved doubled parameter interval and uniform ranks

Let \(K=dC/d\tau\). The five free slopes are \(-1/48,-1/36,-1/84,41/81,-1/9\); nine induced anchor slopes are \(+1/9\). Every proper and actual entry is independently differentiated and bound to both endpoint differences. Exact full proper Frobenius accounting gives
\[
 \|K\|_F^2
 =2\left(1296/48^2+324/36^2+378/84^2
             +81(41/81)^2+18/9^2\right)
 =198145/4536<(53/8)^2.
\]
The 18 includes both sets of nine unordered abc and anchor edges; the outer factor 2 counts symmetry. Therefore \(\|K\|_{op}<53/8\). For every real \(\tau\in[0,1/64]\), the midpoint distance is at most \(1/128\). Both proper floors are at least
\[
 1/16-(53/8)/128=11/1024>0. \tag{2}
\]
Lower perturbations keep \(Kq=0\), so the lower statement concerns \(q^\perp\); upper perturbations have derivative \(-K\). Together with the endpoint affine entry proof, this establishes feasible tight-H matrices attaining the sharp cost for EVERY REAL \(0\le\tau\le1/64\), twice the target's parameter range. No new factor at 1/64 is needed, and no maximal-range claim is made.

The columns of \(E\) span \(\mathbf1^\perp\), with \(E^{\mathsf T}E=I+J\succeq I\). The nonzero eigenvalues of \(ECE^{\mathsf T}\) equal those of \(C^{1/2}E^{\mathsf T}EC^{1/2}\succeq C\). The latter matrix has exactly the same kernel as C. The min-max principle therefore bounds all its 276 positive eigenvalues below by 11/1024. The same argument applies to positive definite U and its 277 positive eigenvalues. Adding \(J\), which is zero on \(\mathbf1^\perp\), gives actual lower and upper ranks 277 and simple extreme eigenvalues \(-29/110\), 1 for \(M\). Both nonzero actual normalized gaps are at least
\[
 (11/1024)/220=1/20480.
\]
For the original smaller range, this also confirms all target floors and ranks, including its weaker gap 1/28160. Positive \(\tau\) makes every allowed entry strictly positive. At \(\tau=0\) the optimum is \(P_0\). Any strictly entry-positive competitor has \(\sum_B b_A+b_*>0\) at zero in (1), hence \(P>P_0\). The feasible primal with \(\tau\downarrow0\) approaches \(P_0\), proving the strict-positive infimum is \(P_0\) and is unattained.

## 6. Proved sharp cost-gap stability for the NN sign cone

Let \(\Delta=P-P_0-41\tau\). In the independent NN coordinates, define the sign cone \(\mathcal K\) by bad/bad changes at most zero, good/good changes at least zero, and mixed changes zero. Its coordinate \(\ell^1\) distance is exactly
\[
 V=\sum_{k_e=2}r_e^+ +\sum_{k_e=0}r_e^- +\sum_{k_e=1}|r_e|.
\]
Each cone coordinate projects separately onto its half-line or zero. The NN penalty in (1) is \(2\sum_{k=2}r^++2\sum_{k=0}r^-+\sum_{k=1}|r|\), so
\[
 \operatorname{dist}_{\ell^1}(r,\mathcal K)=V\le2\Delta,
 \qquad \sum_B b_A+b_*\le2\Delta. \tag{3}
\]
An individual wrongly positive bad/bad or wrongly negative good/good coordinate is at most \(\Delta\); an individual mixed absolute change is at most \(2\Delta\). This holds for ALL real feasible competitors whenever that class is nonempty, not just the constructed line. It does NOT bound distance to the full FEASIBLE optimal set, nor anchored-trade displacement.

The constant 2 is sharp even for actual feasible tight-H matrices. Choose disjoint actual proper vertices \(A=z_0z_1\), \(B=z_2z_3\), \(G=z_4\), \(H=w_0w_1\); in the literal bit encoding these are 24,96,128,12288. The first, second and fourth are bad, and G is good. Let
\[
 R=(e_A-e_B)(e_G-e_H)^{\mathsf T}
       +(e_G-e_H)(e_A-e_B)^{\mathsf T}.
\]
It changes AG by +1, BG by -1, AH by -1, BH by +1, and transposes. All four are allowed NN edges. Every row sum and star product is zero, and its literal lift has NO empty entries. The two outer-product vectors are disjoint, orthogonal, and have norm \(\sqrt2\); hence \(\|R\|_{op}=2\). Perturb the entire primal by \(uR\), for every real \(|u|\le1/1024\) and every real \(\tau\in[0,1/64]\). Full original entry inequalities hold at all four rectangle corners and then throughout by affine convexity. The bad/bad AH/BH changes remain negative, as checked at the corners; mixed AG/BG become \(u,-u\). The proper spectral floors throughout are at least \(11/1024-2/1024=9/1024\), giving actual gaps at least \(9/225280\) and both ranks unchanged. All bad empty entries and the loop remain at the floor. Therefore \(\Delta=|u|\), \(V=2|u|\). Every nonzero u attains equality in (3), proving no constant less than 2 can hold for the stated NN-cone metric.

## Reproducibility and trust

[primal.py](primal.py) supplies the new whole-matrix recipe/derivative/dual/cycle checks. [geometry.py](geometry.py) and [blocks.py](blocks.py) openly adapt the reviewer's published original-coordinate implementation. [FRESH-BASE.json](FRESH-BASE.json) is a fresh whole mathematical record, generated AFTER the checks; it is not an author EXPECTED record or a proof premise. [verify.py](verify.py) independently regenerates that whole record and rejects wrong nested types, keys or values. Source sealing precedes local imports. [validate.py](validate.py) serially checks normal/optimized, local/cold and optional second-Python positives plus mathematical, input, whole-fixture and source damage controls. No author programs, private data or old PSD result are run or trusted. Ordinary real-parameter, completeness, norm, tensor-metric, singular-value, rank and cone-distance arguments remain UNFORMALIZED. Neither generic Conjecture H/I nor LEMMA10308's full optimizer-set geometry is proved here.
