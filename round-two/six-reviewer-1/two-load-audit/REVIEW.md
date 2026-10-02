# Independent review: two pendant load values with repeated heavy marks

Actual executing agent: **six-reviewer-1**, role **independent mathematical reviewer**, round two, 2026-10-02. Shared campaign signing identity does not distinguish authors. This target and verdict were independently selected; no researcher assignment or acceptance quota was used.

**Verdict: confirms the new multiple-heavy-mark scope of LEMMA9153**, artifact **bafkreibnbqpqiawc4uizwj5xcgrqwxe5wfdzssis2ikb3ihenj45irvh34**. Original author: six-downset-1, researcher; immutable source commit **733fd3c0067e8dd56a2c68a12361b50abe65fe42**. [Original complete proof](https://github.com/helgithorskarp/math_results/blob/733fd3c0067e8dd56a2c68a12361b50abe65fe42/round-two/six-downset-1/two-load-types/PROOF.md).

The reviewed scope is **every integer k>=2,r>=1,n>=k+r,D>t>=1**, all choices of distinct old marks and fresh coordinates. It includes arbitrarily large dimension, loads and multiplicities. The rational signed H witness has greatest lower rank N-k among **all real H witnesses**, without a cap, permutation invariance or rationality assumption on competitors; its upper rank is N-1, unit eigenvalue simple, and negative endpoint has multiplicity exactly k. The original half-unit scaled cap holds. The improvement below gives a larger explicit rational repair weight and a sharper bound for the original weight.

LEMMA9153 also credits k=1,r>=2 to LEMMA9100 and k=r=1 to LEMMA9005. **This review does not give an independent verdict on 9100 or 9063**. The one-heavy cases are context, not imported proof premises for the k>=2 result. REVIEW9049 already confirms 9005's two-mark scope. Equal loads D=t are a different theorem, credited to 8895/8863; neither the present domain nor the two-type residual decomposition includes that equality.

This is an exact computer-assisted ordinary proof with independently reconstructed arithmetic and original-index controls. No floating-point signs, interpolation, truncated search, author program input or proof assistant supplies the uniform certificate. The ordinary geometric, lift, symmetry, completeness and spectral bridges below remain unformalized.

## Exact statement and conventions

Let X have n elements, with k heavy marks and r light marks, all distinct. At a heavy mark attach D fresh coordinates and at a light mark attach t. For each fresh b attached to x include both {b} and {b,x}, together with every subset of X. All fresh coordinates are distinct and outside X. This is a downset. Put

\[
 q=2^{n-1},\quad a=kD,\quad u=rt,\quad m=a+u,\quad
 N=2q+2m,\quad s=q+D,\quad w=s-1,\quad P=I-J/N.
\]

A signed H witness here is a real symmetric M with M1=1, M_AB=0 whenever A intersects B, and L=(N-s)M+sI positive semidefinite. An empty-set loop is permitted; nonempty diagonal entries must vanish. Negative disjoint weights are permitted. The additional cap M<=I is stronger than the defining H lower condition and is not Conjecture I.

There is an explicit rational such M with

\[
 \operatorname{rank}L=N-k,\quad \operatorname{rank}(I-M)=N-1,
 \qquad (N-s)(I-M)\succeq\tfrac12P.                         \tag{1}
\]

The only maximum intersecting families are the k full heavy stars. For every real H witness, rank L<=N-k. For the constructed M, lambda_min=-s/(N-s) has multiplicity k, lambda=1 is simple, and every nonunit eigenvalue is at most 1-1/[2(N-s)]. No unrestricted H or I theorem follows.

## Maximum families and the universal rank bound

An intersecting family containing a fresh singleton has at most two members. Spokes at distinct marks are disjoint, so a family containing spokes uses only one mark; all its old sets contain that mark. Its size is at most q+d_i, with equality only for the entire marked star. An old-only intersecting family has at most q by pairing every cube set with its complement. Since q>=4,D>=2, the fresh size two and old size q are smaller than s; since t<D, precisely the heavy stars attain s.

For a heavy-star indicator x, support gives x^T M x=0, and L1=N1. Consequently z=x-(s/N)1 satisfies z^T Lz=0, hence Lz=0 by PSD. The k centered stars are independent: at the empty coordinate a vanishing linear combination forces the sum of its coefficients zero; at a spoke unique to a heavy mark the corresponding coefficient then vanishes. This proves rank L<=N-k for all real H witnesses. It does not use the constructed seed or its cap.

## Empty lift and definition-level Gram construction

For a rational nonempty core C with diagonal w and entries -1 at intersections, define

\[
 T_0=\begin{pmatrix}-1^T\\I\end{pmatrix},\quad
 Q=T_0CT_0^T,\quad M=(Q+J-sI)/(N-s).
\]

Then Q1=0, support and row sums hold, and

\[
 L=Q+J,\quad \operatorname{rank}L=1+\operatorname{rank}C,
 \quad (N-s)(I-M)=NP-Q.                                    \tag{2}
\]

T_0 is injective and its column space is 1-perp. The actual empty Gram vector is minus the sum of all nonempty vectors; it is not a free auxiliary vector. The full frame including it has Q's nonzero spectrum. This is the previously credited 7578 lift.

On the 2q-1 nonempty old cube sets let P_c exchange proper complement pairs and have zero full-set row. Use

\[
 C_D=(q-D)P_c+(q+D)I-J.
\]

It is PD: the antisymmetric complement space has eigenvalue 2D, multiplicity q-1; symmetric pair differences have eigenvalue 2q, multiplicity q-2. The remaining two-plane has trace q+D+1 and determinant 2D, so both eigenvalues are positive. This also covers D>q. For its Gram vectors set G=sum g_A, f=g_X and H_i=-sum_{A containing x_i}g_A. Complement counts give

\[
 G^2=f^2=w,\quad Gf=D+1-q,\quad H_iH_j=qD\delta_{ij},
 \quad GH_i=fH_i=-D.                                      \tag{3}
\]

Choose mutually orthogonal spoke residual groups, orthogonal to the old span, with products (q+D)(delta_jl-1/D) within a group. Define S_ij=H_i/D+T_ij. Its squared norm is w, distinct same-mark spokes have product -1, different-mark spokes product zero, and mandatory old products are -1. Each heavy residual group has rank D-1 and zero sum; each light group has rank t because t<D. Their total rank is m-k.

Let L_H be the mean of all heavy spokes and ell the mean of all light spokes. Then L_H^2=q/a, ell^2=(q+D-t)/u, L_H ell=0. Write

\[
 K=G+aL_H+u\ell,\quad
 K^2=B_0=w+m(q-2)+u(D-t)>0,
\]

and for a spoke of group size d in {D,t}, K S_j=w-d. Solving the actual required singleton/spoke product gives

\[
 c_d=\frac{m(w-d-m-1)}{(m+1)((m-1)w-1+d)}.
\]

With C_sum=sum_j c_j S_j, put U_j^0=-K/(m+1)+c_jS_j-C_sum/m. The necessary added diagonal is eta_j=w-(U_j^0)^2. The independent symbolic reconstruction uses the equivalent type mean/deviation formula

\[
 \eta_i=w-\|{-K/(m+1)+c_i\mu_i-C_{sum}/m}\|^2
              -c_i^2(w-\|\mu_i\|^2),\quad
 (\mu_H,\mu_L)=(L_H,\ell),
\]

so it retains both within-mark and between-mark light variance. Let E=a eta_H+u eta_L and

\[
 \zeta_i=\frac m{m-2}\left(\eta_i-\frac E{m(m-1)}\right).
\]

The uniform signs below give zeta_H,zeta_L>0. Set W=P_m diag(zeta_H^[a],zeta_L^[u])P_m. It has row sums zero, rank m-1 and diagonals eta_i: sum_j zeta_j=mE/(m-1) gives the diagonal identity directly. Realize its vectors W_j orthogonally to the old/spoke span, and set U_j=U_j^0+W_j. Norms are w and U_jS_j=-1. These are the only fresh-singleton mandatory off-diagonal products.

Every constructed Gram entry is rational, even though a chosen vector realization can involve irrational coordinates. The nonempty sum is K/(m+1). The old, spoke-residual and W spans are all recoverable from the indexed vectors, and are mutually orthogonal. Thus the seed core has rank

\[
 (2q-1)+(m-k)+(m-1)=N-k-2.                                \tag{4}
\]

## Complete physical frame, including all multiplicities

Put h_0=-(G+f)/2, G_p=G+h_0 and A_i=H_i-h_0. Their nonzero old products are G_p^2=q-1, h_0^2=D and A_iA_j=D(q delta_ij-1). The old frame F_0 acts by

\[
 F_0G_p=(q+1)G_p+(q-1)h_0,\quad F_0h_0=D(G_p+h_0),
 \quad F_0A_i=2DA_i.                                      \tag{5}
\]

Here p=k+r>=3 and q>=2^{p-1}>=p+1. The marked metric D(qI-J_p) is PD because q>p. This physical condition is separate from the enlarged formal polynomial sign domain.

For each light group its spoke mean is H_i/D+Z_i, where the Z_i are orthogonal and Z_i^2=(q+D)(1/t-1/D)>0. Let bar A_H,bar A_L,bar Z be the respective mark means. Let W_s be the heavy type mean of the W_j and

\[
 \alpha=W_s^2=\frac{u(u\zeta_H+a\zeta_L)}{am^2}>0,
 \qquad y=(u/m)(c_HL_H-c_L\ell).
\]

The invariant six-basis (G_p,h_0,bar A_H,bar A_L,bar Z,W_s) has diagonal metric

\[
 q-1,\ D,\ D(q/k-1),\ D(q/r-1),\
 (q+D)(1/t-1/D)/r,\ \alpha,
\]

with only off-diagonal product bar A_H bar A_L=-D. All six directions are independent. Expanding the actual old, spoke, singleton and empty outer products gives its full frame

\[
 F_+=F_0+aL_HL_H^*+u\ell\ell^*+KK^*/(m+1)
             +(am/u)(y+W_s)(y+W_s)^*.                      \tag{6}
\]

The KK weight is exact: m singleton common terms and the actual empty term contribute (m+1)/(m+1)^2. The heavy and light type means of the centered singleton part are y+W_s and -a(y+W_s)/u; their weighted squared sums give a+a^2/u=am/u. Omitting the empty vector changes (6).

For an orthonormal zero-sum vector of heavy-mark coefficients, the heavy standard basis (H_lambda,W_lambda) has orthogonal squared norms qD,zeta_H/D and spoke mean S_lambda=H_lambda/D. For light-mark coefficients the basis (H_lambda,Z_lambda,W_lambda) has squared norms qD,(q+D)(1/t-1/D),zeta_L/t, and S_lambda=H_lambda/D+Z_lambda. Each corresponding full standard frame is

\[
 F_{std}=F_0+d S_\lambda S_\lambda^*
       +d(c_iS_\lambda+W_\lambda)(c_iS_\lambda+W_\lambda)^*, \tag{7}
\]

where d=D or t and F_0 acts by 2D only on H_lambda. For arbitrary zero-sum coefficient vectors, these products are the displayed scalar metric times their Euclidean coefficient product; all constant-type terms cancel. This proves the repeated sectors and orthogonality without assuming a normalized coordinate basis exists in the original indexing.

Within a single group, orthonormal zero-sum index vectors give squared norms q+D,zeta_i and the normalized paired frame

\[
 F_i=\operatorname{diag}(q+D,0)+v_iv_i^*,\qquad
 v_i=(c_i\sqrt{q+D},\sqrt{\zeta_i}).                        \tag{8}
\]

Different group/type zero-sum sums eliminate cross terms in the expanded frame. The untouched old symmetric pair-difference space has dimension q-2 and action 2q; the old antisymmetric space has dimension q-1, and removing all p independent marked directions leaves q-p-1 dimensions with action 2D. Added vectors are orthogonal to these spaces.

| Sector | Dimension |
| --- | ---: |
| Invariant means | 6 |
| Heavy standard sectors | 2(k-1) |
| Light standard sectors | 3(r-1) |
| Heavy within-group pairs | 2k(D-1) |
| Light within-group pairs | 2r(t-1) |
| Untouched high old space | q-2 |
| Untouched low old space | q-k-r-1 |

The sum is N-k-2, agreeing with (4), so no seed direction is omitted. At r=1 the light standard space disappears; at t=1 the light internal spaces disappear; at q=k+r+1 the low old space disappears. None is divided by its vanishing multiplicity. The symbolic light slack remains valid and closes the light standard sector even at t=1.

## Uniform cap reduction and independent certificate

Take h=N-1. Since m>=2D+t, h>2(q+D). The untouched old eigenvalues and the positive old two-plane (whose trace is q+D+1) are below h. Hence hI-F_0 is PD. In the invariant basis its bilinear resolvent is obtained by inverting the actual two-plane action in (5), and by dividing the marked metric by h-2D and the new residual metrics by h. The two-plane denominator is

\[
 \Delta_0=(h-q-1)(h-D)-D(q-1)>0.
\]

In that basis let v_1=L_H, v_2=ell, v_3=K and v_4=y+W_s. The rank-four update budget for (6) is

\[
 B=\operatorname{diag}(1/a,1/u,m+1,u/(am))-(v_i^TRv_j)_{i,j}.
\]

Schur complementation of a positive base shows hI-F_+>0 exactly when B>0. The independent reconstruction derives the shear coefficients from the actual heavy/light marked coordinates of v_4, then checks all six residual coordinates are exactly W_s. Subtracting (uc_H/m)v_1-(uc_L/m)v_2 from v_4 is a determinant-one congruence. The upper left three-block is unchanged and the new border is (-uc_H/(am),c_L/m,0). All 16 sheared entries are rebuilt from the Gram and resolvent. A generic exterior-row subset recurrence computes all four leading determinants, including the last; it does not use the author's bordered adjugate shortcut.

The two internal slacks are

\[
 \sigma_i=1-\frac{c_i^2(q+D)}{h-q-D}-\frac{\zeta_i}{h}>0.    \tag{9}
\]

They imply positivity of the standard frames as well. After scaling their two updates, the budget is

\[
 \begin{pmatrix}1-b_i&-b_ic_i\\-b_ic_i&1-b_ic_i^2-\zeta_i/h\end{pmatrix},
\]

where b_H=q/(h-2D) and b_L=(t/D)b_H+((D-t)/D)(q+D)/h. The inequality h>2(q+D) gives 0<b_i<(q+D)/h<1/2, hence b_i/(1-b_i)<(q+D)/(h-q-D). Its first pivot is positive and its Schur complement is at least sigma_i>0. Thus (9) closes (7) and (8), including absent internal sectors. All untouched gaps are positive. Together with the four leading invariant signs this proves

\[
 NP-Q_{seed}\succeq P.                                   \tag{10}
\]

### Exact signs and arithmetic trust

[derive.py](derive.py) independently reconstructs the two zetas, two slacks and four invariant leading minors in QQ(Q,t,D,a,u), q=Q+4. [algebra.py](algebra.py) uses pinned SymPy1.14.0 sparse rational polynomials, exact factorization/division and UFD cancellation. It reuses this reviewer's published 9049 arithmetic primitives, extended to five variables. No supplied factor list, researcher executable, saved target polynomial, integer packing or expected sign record is input to reconstruction.

Its reduced-fraction invariant is explicit: multiplication can cancel only across the two reduced operands; for addition an irreducible factor with unequal denominator exponents cannot cancel, since exactly one adjusted numerator term is divisible by it. Only equal positive denominator exponents require trial division. A separate native fraction-field GCD implementation checks **2,782 complete rational identities**, including zero and powers, and all reduced numerator invariants. The generic determinant recurrence is the usual exterior expansion by columns already selected; insertion counts selected columns greater than the new column, determining its sign.

[signs.py](signs.py) is a distinct standard-library integer binomial engine. It clears each numerator and denominator by a positive common denominator, splits it into powers of Q, then shifts each four-variable coefficient separately using

\[
 t=T+1,\quad D=t+B+1,\quad a=2D+V,\quad u=t+U,
 \qquad Q,T,B,V,U\ge0.                                    \tag{11}
\]

It checks **every shifted coefficient**, and verifies the **entire inverse binomial transformation** recovers the original coefficient. All shifted coefficients of every numerator and expanded denominator are nonnegative; each Q^0 part has a positive origin constant. Thus all eight rational functions are strictly positive throughout (11), including its boundary. Actual parameters have V=(k-2)D and U=(r-1)t, so all reviewed parameters are covered. Enlarging this sign domain does not remove the physical requirement q>k+r.

| Expression | Raw numerator terms | Q coefficient lemmas | Shifted numerator terms | Largest coefficient |
| --- | ---: | ---: | ---: | ---: |
| zeta_H | 1581 | 6 | 7020 | 1995 |
| zeta_L | 1586 | 6 | 7020 | 1995 |
| Heavy internal slack | 3093 | 7 | 10395 | 2805 |
| Light internal slack | 3095 | 7 | 10395 | 2805 |
| Invariant minor 1 | 34 | 4 | 56 | 35 |
| Invariant minor 2 | 193 | 6 | 252 | 126 |
| Invariant minor 3 | 298 | 5 | 456 | 210 |
| Invariant minor 4 | 15824 | 10 | 39886 | 8500 |

There are 51 numerator coefficient lemmas and 75,480 shifted terms in total; they are never one dense polynomial. [EXPECTED.json](EXPECTED.json) fixes every full rational-function hash, all 16 budget hashes, every complete coefficient hash, all constants/counts/degrees, the inverse identities and all finite records. Hashes detect changes; positivity is proved by inspecting all coefficients, not by trusting a hash. Denominator positivity is checked for expanded denominators as separate coefficient polynomials. Original denominators are also positive from t,D,a,u,m-2,m-1,m,m+1,h,h-2D,h-q-D,Delta_0 and the coefficient denominators. Monic factor normalization preserves the rational scalar, so it does not lose a denominator sign.

## Rank repair and spectral bridge

For the raw core keep the old/spoke vectors and take raw singletons R_j=-S_j/w+E_j, with independent orthogonal E_j of squared norm w-1/w>0. Required norms/intersections persist. Its rank is (2q-1)+(m-k)+m=N-k-1. Its k-dimensional kernel consists precisely of the heavy nonempty-star indicator relations: the old coefficient sum is -H_i and its D heavy spokes sum to H_i. These relations are also in the seed kernel. Thus the kernel of every positive mixture of the seed and raw cores is exactly that raw kernel, and its lower lifted rank is N-k. This attains the universal bound independently proved above.

With A_2=aD+ut, the actual raw nonempty sum has squared norm

\[
 B_{raw}=w+(1-1/w)^2[m(q+D)-A_2]-2m(1-1/w)+m(w-1/w)\ge0.
\]

The full raw trace includes the empty vector:

\[
 T_{raw}=(N-1)w+B_{raw},\qquad Q_{raw}\preceq T_{raw}P.
\]

For C_e=(1-e)C_seed+e C_raw with 0<e<1, (10) gives

\[
 NP-Q_e\succeq[1-e(T_{raw}-N+1)]P.                         \tag{12}
\]

The original e=1/[2(T_raw+1)] therefore gives the claimed half gap and, in fact, the sharper gap below. A positive full gap means I-M has rank N-1 and the unit eigenvalue is simple; kernel L has dimension k, giving the exact negative endpoint multiplicity. These conclusions require the full lift and the actual empty trace, not a nonempty trace surrogate.

## Independent reproduction, controls and exposure

The first complete independent eight-function result and all sign/physical checks preceded reading or running the researcher's algebra engines. The author's theorem, defining proof formulas, expected-result schema and displayed sign counts were visible beforehand: this is an independent algorithm and derivation, **not a blind audit**. No researcher executable or fixture is imported by any public checker. A later native author algebra replay was attempted as corroboration and **did not complete**: its first fixed60s stage timed out inside five-variable randomized multiplication controls, before any sign record. The author algebra replay was stopped; its guard, process scope and thread settings were not increased. No author normal/optimized sign replay or full author comparison is claimed. This operational failure is not a mathematical counterexample, and does not invalidate the completed independent reconstruction. It is a reproducibility limitation of this attempt that the original author should inspect.

[frame.py](frame.py) builds all Gram vectors in original set indices using [literal.py](literal.py), this reviewer's Fraction/Bareiss primitives from 9049, now extended to all mark multiplicities. It computes every entry of the entire physical frame metric and action, every cross-sector zero, the actual empty outer product, untouched actions and exhaustive dimension census. Unnormalized coefficient differences e_i-e_0 avoid square roots. Original-index adjacent heavy/light mark generators simultaneously permute old coordinates and entire fresh groups and preserve every seed and raw lifted entry.

The four independent fixtures are (n,k,r,D,t)=(3,2,1,2,1),(4,2,2,3,1),(3,2,1,5,2),(5,3,2,3,2), with deliberately relocated mark coordinates. They cover 4,573 full-frame entries, dimensions 14,28,28,53 and N=18,32,32,58. They include r=1,t=1,q=k+r+1,D>q, multiple heavy contrasts and the repeated light standard sector. Full PSD ranks, support, every row, all k forced kernels, the actual raw trace and both original/improved mixtures are checked. Seven actual type permutation generators are checked on all original seed/raw entries.

[controls.py](controls.py) independently rebuilds all 64 invariant budget entries in Fraction arithmetic and all 16 leading determinants by the full signed-permutation expansion at four disjoint parameter points. These compare every value to the definition-derived rational functions. Sixteen deliberate failures must be rejected: negative sign, missing strict origin, invalid/boolean/duplicate polynomial terms, zero divisor, equal/nonpositive/boolean loads, duplicate marks, excluded one-heavy scope, a zero-diagonal indefinite residual, a mandatory intersection corruption with lift row sums retained, a changed empty loop, a wrong physical frame, and an incorrectly centered forced star. Three complete signed forward/inverse binomial controls are additional checks. Six additional full-fixture/cache schema damages (extra/missing/changed fields or coefficients) are rejected through the public CLI. Explicit exceptions remain active under Python -O.

Finite cases validate code and reduction; their successful PSD checks do not prove the unbounded range. Uniformity follows from (3)--(11), all coefficient signs, the complete physical decomposition and the ordinary kernel/spectral arguments. The exact trust boundary is CPython rational/integer arithmetic, SymPy sparse polynomial arithmetic/factorization/division, the reviewed code and those ordinary bridges. No external polynomial corpus or raw graph ledger is a reproduction input.

## Strengthening and improvement opportunities

**Proved for the reviewed class, with prior mechanism credited to REVIEW9049 and REVIEW8927.** Let loss=T_raw-N+1. Since w>=5,N>=18,B_raw>=0, loss>=(N-1)(w-1)>=68. The original repair gives

\[
 \beta=1-\frac{loss}{2(T_{raw}+1)}
       =\tfrac12+\frac N{2(T_{raw}+1)}>\tfrac12.
\]

The larger explicit rational choice

\[
 e_{new}=\frac1{2(T_{raw}-N+1)}>\frac1{2(T_{raw}+1)}
\]

still gives the half-unit full gap and the same greatest lower rank and endpoint multiplicities. More generally, **for every real 0<gamma<1 and every real 0<e<=(1-gamma)/loss**, the same mixture has full gap at least gamma and greatest lower rank N-k; this interval lies inside (0,1). Rational e gives a rational witness. This is a sufficient interval from a trace bound, not an optimal interval or endpoint claim. Original/improved weights are checked in every finite fixture, but (12) proves the whole real interval.

The enlarged independent certificate proves the same eight algebraic signs for all real Q,T,B,V,U>=0. This is a formal algebraic refinement, not a downset theorem outside the separately justified q>k+r physical metric domain.

The newly committed [LEMMA9229 three-distinct-load proof](https://github.com/helgithorskarp/math_results/blob/bc6e3ab5654e7ef83d4b2703829d11a8789d94f6/round-two/six-downset-1/three-distinct-loads/PROOF.md), artifact bafkreibgieacu2a3llpxkyu5miqz3ntdawpf76we5s3cfwqeldhxe7kqga, was read in full as subsequent context: its author claims exactly one mark per each of three distinct loads and explicitly leaves arbitrary three-type multiplicities open. This review supplies no verdict on it, does not replay its twelve-sign engine and imports none of its conclusions.

The most consequential further task is extending the complete physical decomposition to repeated multiplicities of three distinct load values. It needs additional between-type residual means, their full Gram metric, complete sector census and cap budgets; the present eight signs supply none of those missing signs. Formalizing the lift/forced-star/completeness/Schur bridges and checker normalization would reduce the remaining ordinary trust. Optimizing the trace repair requires a justified spectral bound on Q_raw or the full pencil, beyond its trace. No such optimization is claimed here.

## Primary literature and prior-art status

[Ellis, Filmus and Friedgut, Section 4 of *Chvatal's conjecture: a proof from The Book*](https://arxiv.org/html/2609.28404v1#S4) supplies the signed weighted Hoffman conventions and distinguishes H from inertia conjecture I. The [primary version record](https://arxiv.org/abs/2609.28404), checked live 2026-10-02, lists v1 dated 2026-09-23. Its theorem on Chvatal's conjecture and its numerical evidence do not prove unrestricted H or I. This pendant family verifies a special H class with an additional upper cap. Targeted primary searches for pendant/two-load downsets produced no usable additional match; historical priority is unassessed.

The credited source chain is 7578 (lift), 8579/8788 (earlier constructions), 8863/8895 (equal loads), 9005 (two unequal marks), 9063/9100 (one heavy mark extensions), and prior scoped independent reviews 8927/9049. Their full committed context and correct canonical identities were inspected; their review verdicts do not transfer to this extension. The new k>=2 proof above is self-contained at the ordinary Gram/lift level. This review supplies an independent certificate and the stated repair application, not first authorship of the target theorem.

The complete independent EXPECTED record SHA256 is **b29d4823d1fcc9cc734120ad478b71fbe2080e832389347adcea671dff4ca6af**. Independent normal definition-level reconstruction took75.563s/81048KiB; the final optimized public algebra phase74.283s/80400KiB reproduced every rational coefficient and budget field. Optimized signs/frames/controls/arithmetic took6.542/6.410/3.765/5.356s, respectively. Full normal/optimized records match; the final frames contain351212 exact checks. An earlier optimized algebra replay approached the guard at89.268s; exact zero short-circuits in the same generic arithmetic lowered the final cost without changing any coefficient or limit. After the optional author algebra timeout, no further expensive algebra replay was run. Frozen-public sign, frame, control and arithmetic replays and whole source bytes are separately verified; frozen-public full algebra is not rerun in this pass, and no such additional run is claimed.

Reproduction and the exact published file set are in [README.md](README.md) and [SHA256SUMS](SHA256SUMS). Generated polynomial caches, private partial runs and operational receipts stay outside this compact packet. All math phases keep fixed 90-second guards and 30,000 terms per polynomial, with six native thread settings one and at most one intensive local job. A timeout, killed process or incomplete stage gives no mathematical verdict.
