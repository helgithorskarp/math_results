# Independent consecutive-triangle cap proof and constant repairs

Actual author **six-reviewer-5**, independent mathematical reviewer, 2026-10-04.
Target LEMMA10230/0 is by six-downset-1. Ordinary unformalized proof with fresh
exact computation. Its entire graph proof was exposed; no author native code,
coefficient certificate, expected record or validation file was opened or run.

## Scope and conclusions

For integers \(n\ge3,h\ge3\), put \(q=2^{n-1},l=h-1,g=h+l,m=3g,e=m+1\),
\(s=q+3h,N=2q+12h-6,D=3h,w=s-1\).
The carrier is the entire old n-cube plus h private triangles at old mark x
and l at distinct mark y, with every private pair disjoint from the old set
and the other pairs. Retain all N vertices including the actual empty loop.

The construction below confirms the ENTIRE target: rational symmetric M,
intersection zeros, \(M1=1\), \(L=sI+(N-s)M\succeq0\), \(I-M\succeq0\),
both greatest ranks N-1, sole lower kernel the centered heavy-star indicator,
simple unit, and the target's scaled cap floor above 3/4.

Additional proved refinements for the SAME original seed and three-pair line:
\(0<\kappa<2\); the lower form is PSD iff \(0\le\delta\le6/\kappa\), of rank
N-2 at either endpoint and N-1 in the interior; every \(0<\delta\le1/8\)
attains both maximal ranks with
\[
 NI-L_\delta\succeq[1-(3+2\sqrt6)\delta]P
 \succeq(5-2\sqrt6)P/8,\qquad P=I-J/N.
\]
The constant rational \(\delta=1/32\) retains floor
\((29-2\sqrt6)/32>3/4\), and rational delta gives rational entries.
This is a sufficient cap interval, not its optimal endpoint or general H/I.
Ordinary H/greatest lower-rank existence is already9361.

## Old and marked space, including the retained light mean

On every nonempty old set use \(A=sI+(q-D)P_{\rm old}-J\), where proper
complements are exchanged and the full-set row of Pold is zero.
Let its vectors be \(g_A\), \(G=\sum g_A,g_F=g_X,H_t=-\sum_{t\in A}g_A\).
Direct original counts give
\[
 G^2=g_F^2=w,\quad Gg_F=D-q+1,\quad H_x^2=H_y^2=qD,\quad H_xH_y=0,
 \quad GH_t=g_FH_t=-D.
\]
For proper complement pairs, sums \(p_i\) and differences \(d_i\) satisfy
\(p_ip_j=4q\delta_{ij}-4,d_id_j=4D\delta_{ij},p_id_j=d_ig_F=0,p_ig_F=-2\).
The orthogonal \(E=G-g_F,U=G+g_F,R=H_x+H_y+G+g_F,A_o=H_x-H_y\)
have squared norms \(4(q-1),4D,2D(q-2),2qD\).
The remaining q-2 sum contrasts and q-3 difference complement have positive
metrics and old-frame eigenvalues 2q,2D. The difference coefficient vectors
for R,Ao have disjoint supports and norms squared (q-2)/2,q/2.
This is a positive complete old decomposition of dimension 2q-1.

At each mark introduce orthogonal full h-facet B spaces,
\(B_iB_j=(s/3)(\delta_{ij}-1/h),\sum B_i=0\), and independent facet T spaces,
\(T_{ia}T_{ib}=s(\delta_{ab}-1/3),\sum_aT_{ia}=0\).
Marked rows are \(V_{tia}=H_t/D+B_{ti}+T_{tia}\).
Retain all h heavy and l light facets. Every required original pairing is -1:
old/marked uses \(g_AH_t=D(1-2[t\in A])\); marked pairs use the displayed Gram.

The light mean \(\bar B=l^{-1}\sum_{j<l}B_{yj}\) has norm squared s/(3hl).
Recenter only the light facets by \(\widetilde B_j=B_{yj}-\bar B\);
their contrast Gram is \((s/3)(\delta_{ij}-1/l)\). Heavy contrasts use B itself.
The retained light B vectors are independent. Old rows, facet averages and
T differences recover the entire old/marked span of dimension 2q+6h-5,
with exactly the heavy-star relation.

Its total and common empty projection are
\[
 K=G+H_x+(l/h)H_y+3l\bar B,\quad z=-K/e,\quad
 K^2=2q(3h-1)-4,\quad c_0=z^2=q/[2(3h-1)]-1/(3h-1)^2.
\]
The common marked scores are \(v_x=-(q-1)/e,v_y=-(q+2)/e\).

## Full private completion

For each group k=h,l set
\[
 B_2=s(k-1)/(3k),\ r=1+v,\ a=r/(2B_2),\ b=-2a,\ c=9r/(2s).
\]
Private projections are
\[
 P_{i1}=z+a\widetilde B_i+cT_{i2},\
 P_{i2}=z+a\widetilde B_i+cT_{i1},\
 P_{i3}=z+b\widetilde B_i+\frac c{k-1}\sum_{j\ne i}T_{j3}.
\]
The required scores are \(v+aB_2-cs/3=-1,v+bB_2=-1\); their total is mz.
Set
\[
 \eta_L=w-c_0-a^2B_2-2sc^2/3,\quad
 \eta_F=w-c_0-b^2B_2-2sc^2/[3(k-1)],\quad p=-1-c_0-abB_2,
\]
\[
 \mu=(2p+\eta_F)/3,\quad\alpha=2(2\eta_L-p-\eta_F),\quad\beta=\eta_F-\mu.
\]
Fresh exact field algebra verifies
\[
 \mu=(s-3)/3-c_0-9r^2/[2s(k-1)],\
 \alpha=2s-27(2k-3)r^2/[s(k-1)],\
 \beta=2s/3-3(k+3)r^2/[s(k-1)].
\]
All are positive on real h>=3,q>=4 by the whole coefficient check below.
Let
\[
 \tau=\mu_x\mu_y/(h\mu_x+l\mu_y),\
 \nu_x=(h\mu_x-l\tau)/(h-1),\
 \nu_y=(l\mu_y-h\tau)/(l-1).
\]
Facet means have diagonals mu, within-group off-diagonals mu-nu and
cross score -tau. Their row sums vanish; contrasts have eigenvalues nu_x,
nu_y and the remaining nonzero eigenvalue is g*tau. The inequalities
tau<mu_x/l and tau<mu_y/h prove positivity.
Add orthogonal WA,WF of squared norms alpha,beta and use
\[
 W_{i1}=M_i+(WA_i-WF_i)/2,\quad
 W_{i2}=M_i+(-WA_i-WF_i)/2,\quad W_{i3}=M_i+WF_i.
\]
The identities \(\mu+\alpha/4+\beta/4=\eta_L,\mu+\beta=\eta_F,\mu-\beta/2=p\)
give every private diagonal and leaf/full intersection pairing for U=P+W.
Old/private and different-facet private pairs are disjoint; all constraints
are exhausted. W has rank m-1 and sole relation sum W=0. Projecting relations
onto W and then the complete old/marked space proves rank C=N-3 and exactly
two nonempty kernels: heavy-star indicator and r, with r=m/e on old/marked
rows and r=1 on private rows. Total nonempty vector is K+mz=-z.

The actual empty row is z. Its full lift is
\(Q_{00}=1'C1,Q_{0A}=-(C1)_A,Q_{AB}=C_{AB}\).
It kills ones and retains rank N-3; \(L_0=J+Q\) has rank N-2.
All entries of \(M_0=(L_0-sI)/(N-s)\) are rational and have required support
and rows. The empty loop is computed, not discarded.

## Whole physical cap and exact signs

Let Gamma be the physical metric, and S the sum of squared scores against
ALL original rows including empty. Put TS=T1+T2-2T3.
Each leaf-odd block has metric diag(2s,alpha) and frame
\[
 [[2s^2(1+c^2),-sc\alpha],[-sc\alpha,\alpha^2/2]].
\]
Each within-group contrast profile t has basis (Btilde_t,TS_t,WF_t,M_t),
metric diag(2s/3,12s,2beta,2nu) times sum(t_i^2)/2, and representative frame
\[
 4(s/3,s,0,0)^{\otimes2}+2(s/3,-2s,0,0)^{\otimes2}
 +4(as/3,cs,-\beta/2,\nu)^{\otimes2}
 +2(bs/3,2cs/(k-1),\beta,\nu)^{\otimes2}.
\]
These scores include every marked/private leaf/full row. The profiles
(1,...,1,-j,0,...,0) are a complete orthogonal choice.

The first five aggregate bases (E,U,R,Ao,Bbar) have metric
(4(q-1),12h,6h(q-2),6qh,s/(3hl)).
The old frame has entries S00=4(q^2-1),S01=S10=-12h(q-1),
S11=36h^2,S22=36h^2(q-2),S33=36h^2*q, others zero.
Add \(3h j_xj_x'+3l j_yj_y'+z_*z_*'/e\), where
\[
 j_x=(0,-2,q-2,q,0),\quad j_y=(0,-2,q-2,-q,s/(3hl)),\
 z_*=(-2(q-1),6l,-3(q-2)g,-3q,-s/h).
\]
The proper old membership cells (ix,iy) have counts q/2-1,q/2,q/2,q/2-1
and first-four coefficients
(1/[2(q-1)],0,(1-ix-iy)/(q-2),(iy-ix)/q).
The full old row has (-1/2,1/2,0,0,0). Marked projections are H_g/D
plus the light mean; private and empty projections are the common z=-K/e.
These original counts give the displayed whole frame.

Each group's trace (sum TS,sum WF) has metric diag(6ks,k*beta) and frame
\[
 [[6ks^2(1+c^2),-3ksc\beta],[-3ksc\beta,3k\beta^2/2]].
\]
Every cross term to the first five bases cancels in the full leaf/full sum.
The final mean sum_xM has metric hl*tau and frame 3g*hl*tau^2, hence
eigenvalue 3g*tau; group mean sums cancel its old-projection cross scores.
The untouched old spaces retain eigenvalues 2q,6h.

Leaf swaps kill distinct odd characters. Facet permutations give
diagonal-plus-constant cross scores and constants kill contrasts. Every new
old projection lies in span(G,Hx,Hy), so untouched old directions are
orthogonal on BOTH forms. Together with the aggregate cancellations this
proves the complete simultaneous block decomposition. Its dimension is
\[
 2g+4[(h-1)+(l-1)]+5+2+2+1+(q-2)+(q-3)=N-3.
\]

[field.py](field.py) independently builds all these rational forms over
characteristic-zero QQ(h,q), variable order h,q. It divides each cap row by
its positive metric entry and computes EVERY leading Gaussian pivot:
block sizes2,4,2,2,4,2,5,1,1,1, plus nine scalar signs,33 obligations.
Every complete numerator AND denominator after h=3+u,q=4+v has positive
constant and all nonzero coefficients positive. This is an exact polynomial
argument on the whole quadrant, not finite sampling.
All division parameters h,l,l-1,q,q-1,q-2,s,e and metrics are positive.
Positive pivots preserve leading-minor signs under positive row
normalization; Sylvester gives all complete symmetric cap blocks positive.
Nonzero whole-Gram and physical-frame spectra coincide. Consequently
\(Q<(N-1)P\) on its range and \(NP-Q\succeq P\) on ones-perp.

[polynomial.py](polynomial.py) uses standard-library sparse rational
polynomials, independently of the CAS/producer. It recomputes every whole
binomial shift. Original row clearing satisfies \(a_{ij}d_{ij}=D_i n_{ij}\).
Independent recursive leading determinants verify
\(\Delta_i d_i=\Delta_{i-1}n_iD_i\) for every pivot.
All76 cleared entries and24 leading pivots give100 complete coefficient
identities, with full block/scalar coverage and1573 shifted cap coefficients
counting repeated numerator/denominator occurrences.
The ten-dimensional aggregate is split after proving its couplings zero;
these counts are not the author's151-entry/315-update certificate.

The same fresh field constructs the full kappa below. The numerator of
2-kappa has bidegree(31,10),297 coefficients, and297 positive shifted
coefficients. Its shifted denominator is strictly positive.
The whole shift check proves kappa<2. Generated complete coefficients stay
in ignored work/ and are reproduced from source.

## Original inverse, exact lower line and constant cap interval

Delete singleton x and the last light private full row j. The retained A0
is positive definite: a zero-extended kernel combination of heavy star and r
is killed first at j and then at x. The removed column coefficients are
\(z_i=-r_i+(m/e)\chi_x(i)\); hence \(A_0z=b_0,b_0'z=w,t'z=-3\),
where t indicates the first heavy private triple.

Let tx=e_first-ones_x/h, ty=-e_last+ones_y/l. The full physical inverse dual is
\[
 Z=\frac{\sum t_{xi}M_{xi}}{\nu_x}+\frac{\sum t_{yj}M_{yj}}{\nu_y}
   +\frac{\sum_xM}{hl\tau}-\frac{2WF_{\rm last}}{\beta_y}.
\]
It scores1 on the first heavy triple,-3 on j,zero on EVERY other original
row including empty and all old/marked rows. Orthogonal contrast/mean/WF
directions give
\[
 \kappa=\|Z\|^2=t'A_0^{-1}t
 =(h-1)/(h\nu_x)+(l-1)/(l\nu_y)+1/(hl\tau)+4/\beta_y>0.
\]
The complete retained physical basis identifies the full original inverse.

Change the three symmetric pairings between that heavy triple and j by
delta. They are disjoint and avoid x. Deleting x, the whole remaining
principal is congruent to \(A_0\oplus[6\delta-\kappa\delta^2]\).
The surviving heavy relation has coefficient1 at x for EVERY real delta;
reinserting x adds exactly one zero direction. The whole negative-row-sum
lift retains inertia off ones, and J adds one positive direction. This proves
the COMPLETE lower iff interval and its endpoint/interior ranks.

Rebuilding empty changes its loop by6delta and the entire Q by
\(\delta(uv'+vu')\), where u=-3e_empty+sum_heavy_triple e_i,
v=-e_empty+e_j. Both sums vanish; u^2=12,v^2=2,u*v=3. Its two nonzero
eigenvalues are3+/-2sqrt6, so the norm is \(\rho=3+2\sqrt6<8\).
The seed cap yields \(NP-Q_\delta\succeq(1-\rho\delta)P\).
Since kappa<2, every0<delta<=1/8 has positive lower Schur and uniform
positive cap floor(5-2sqrt6)/8. At1/32 the floor is(29-2sqrt6)/32>3/4.
The target's smaller delta0=1/[4(8+kappa)] gives its claimed gap too.

Actual stars have sizes s,s-3,q,4, with x uniquely largest. For ANY real
ordinary H, \(L[S,S]=sI,L1=N1\) makes the centered maximum-star indicator
have zero energy, so PSD puts it in ker L. Lower rank at mostN-1 follows.
Row sums force the same upper-rank ceiling; the repairs attain both.

## Validation and trust

[original.py](original.py) uses original bitmask sets and an overcomplete
physical coordinate Gram, separately from the block-score route. It checks
every support/diagonal/star/kernel, whole row completion, ALL internal and
cross metric/frame entries, positive literal LDLs, deleted column, every
original inverse dual score and the entire empty-lift update.
At(n,h)=(3,3),(4,3),(3,4) it compares6060 original positions and10566 physical
positions, plus ALL THREE repairs delta0,1/32,1/8.
Finite controls are validation; the full written decomposition and exact
field/shift proof establish the unbounded quantifiers.

Six isolated normal/optimized positive children match ENTIRE records;
24 semantic damages reject mathematically. CPython3.12.14/SymPy1.14.0/
mpmath1.3.0, exact integers/Fractions or QQ(h,q), native1/serial1/45s guard.
The external CAS is trusted for fresh expressions and their written binding;
the separate polynomial reader checks pivots/signs completely, not every
CAS formula's independent authenticity. Physical/completeness/spectral/Schur
and rank bridges remain ordinary unformalized mathematics. No author hash,
solver status, timeout or ancestor theorem is an unchecked premise.
