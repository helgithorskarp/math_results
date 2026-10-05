# Independent proof audit of the four-mark triangle cap

Actual reviewer: **six-reviewer-1**, independent mathematical reviewer.
Target: committed LEMMA10316, reference
bafkreihbezevl4yjwgryvywc6uvd2pecenlqfhvgras3l4qxburektw7ri,
by six-downset-1. This is an ordinary, unformalized proof audit. The
checker verifies the disclosed coefficient data and independent finite
original-coordinate controls; the universal bridges below are written mathematics.

## Scope and result

Let \(X\) have \(n\ge4\) elements, with distinct marks \(x,y,z,w\).
Attach \(h\) triangles at \(x\) and \(l\) at each other mark, for integers
\(h>l\ge2\). Every private pair lies outside \(X\), and all private
pairs are disjoint. The downset consists of \(2^X\) and the subsets of
these triangles. Put
\[
q=2^{n-1},\quad D=3h,\quad d=h-l,\quad F=h+3l,\quad m=3F,\quad
\ell=m+1,\quad s=q+3h,\quad N=2q+6F=2s+18l,\quad P=I-J/N.
\]
The point stars have sizes \(s,q+3l,q,4\), respectively for the heavy
mark, light marks, unmarked old points and private points. Thus the
heavy star is uniquely largest. The empty vertex and its loop are retained.

The target's rational symmetric supported stochastic matrix exists:
\(M\mathbf1=\mathbf1\), \(M_{AB}=0\) for \(A\cap B\ne\varnothing\),
\[
L=sI+(N-s)M\succeq0,\qquad NI-L\succeq(25/32)P,\qquad
\operatorname{rank}L=\operatorname{rank}(I-M)=N-1.
\]
Both ranks are greatest possible. The stated facet, leaf, old-point and
light-\(S_3\) invariance holds. The exact lower PSD interval and its ranks
also hold.

A proved refinement is that every real \(0<\delta\le3/20\) on the
same construction has both ranks \(N-1\) and
\[
 NI-L_\delta\succeq(1-103\delta/16)P.
\]
In particular the floor is \(11/320\) at \(3/20\), and \(409/512\)
at the rational choice \(1/32\). No entry positivity, optimal upper
interval, overlapping private pairs, \(n\le3\), general Conjecture H/I,
or literature priority follows.

## Original Gram construction and support

For all nonempty old sets take vectors \(g_A\) with Gram
\[
 g_A\cdot g_B=s[A=B]+(q-D)[B=X\setminus A]-1.
\]
Complement differences have eigenvalue \(2D\) and dimension \(q-1\);
zero-total pair sums have eigenvalue \(2q\) and dimension \(q-2\).
For \(G=\sum_Ag_A\), the remaining directions \(E=G-g_X,U=G+g_X\)
are orthogonal with norms squared \(4(q-1),4D\).
These exhaust \(2q-1\) directions, all positive. Direct summation gives
\[
G^2=g_X^2=s-1,\quad G\cdot g_X=D-q+1.
\]
For a mark \(a\), set \(H_a=-\sum_{A\ni a}g_A\).
Each star has \(q\) old rows; distinct stars meet in \(q/2\) rows and
have \(q/2\) complementary cross pairs. Consequently
\[
H_a^2=qD,\quad H_aH_b=0\ (a\ne b),\quad
GH_a=g_XH_a=-D,\quad g_AH_a=D(1-2[a\in A]).
\]

Give each group independent spaces with
\(B_iB_j=(s/3)([i=j]-1/h)\).
The heavy simplex has dimension \(h-1\) and sum zero. Each light
\(l\)-by-\(l\) Gram is positive definite. Its mean \(\bar B_g\) has
norm squared \(b_0=sd/(3hl)\); all three light means are orthogonal.
For a group of size \(k\), \(\widetilde B_i=B_i-\bar B_g\) has Gram
\((s/3)([i=j]-1/k)\). Independently in every facet take
\(T_{i1}+T_{i2}+T_{i3}=0\), with Gram \(s([a=b]-1/3)\).
The three marked proper rows are
\[
 V_{ia}=H_g/D+B_i+T_{ia}.
\]
Their norms are \(s-1\); distinct intersecting marked rows pair to
\(-1\), including within a facet. Every intersecting old/marked pair
also pairs to \(-1\). No other old/marked support equations exist.
These rows span \(2q+3F-2\) positive directions. Their sole relation
is the heavy-star indicator: the old sum is \(-H_x\), the marked sum
is \(3hH_x/D\), and the heavy \(B,T\) sums vanish.

For the sum \(K\) of old and marked rows, put \(z=-K/\ell,c_0=z^2\).
A fresh four-mark computation gives
\[
\begin{split}
K&=G+H_x+(l/h)(H_y+H_z+H_w)+3l(\bar B_y+\bar B_z+\bar B_w),\\
K^2&=q\ell+27ld-3h-18l-1,\\
zV_x&=-(q-1)/\ell,\qquad zV_y=-(q+3d-1)/\ell.
\end{split}
\]
Indeed the old norm is \(q+3qh+9ql^2/h-3h-18l-1\), and the light
mean norm is \(9lsd/h\). Their sum is the displayed formula.
The common vector is orthogonal to all \(T,\widetilde B\).

In each group define \(r=1+zV\),
\(B_2=s(k-1)/(3k)\), \(a=r/(2B_2),b=-2a,c=9r/(2s)\), and
\[
P_{i1}=z+a\widetilde B_i+cT_{i2},\quad
P_{i2}=z+a\widetilde B_i+cT_{i1},\quad
P_{i3}=z+b\widetilde B_i+\frac c{k-1}\sum_{j\ne i}T_{j3}.
\]
The required marked/private products are
\(zV+aB_2-cs/3=-1\) and \(zV+bB_2=-1\).
Write \(v=s-1\) and
\[
\begin{split}
\eta_L&=v-c_0-a^2B_2-2sc^2/3,\\
\eta_F&=v-c_0-b^2B_2-2sc^2/[3(k-1)],\quad p_0=-1-c_0-abB_2,\\
\mu&=(2p_0+\eta_F)/3=(s-3)/3-c_0-9r^2/[2s(k-1)],\\
\alpha&=2(2\eta_L-p_0-\eta_F)=2s-27(2k-3)r^2/[s(k-1)],\\
\beta&=\eta_F-\mu=2s/3-3(k+3)r^2/[s(k-1)].
\end{split}
\]
Let \(S_\mu=h\mu_x+3l\mu_y\). The residual facet-mean Gram has
diagonal \(\mu_g\), within-group off-diagonal
\(-k\mu_g^2/[S_\mu(k-1)]\), and cross-group entries
\(-\mu_g\mu_t/S_\mu\). Its row sums vanish. Positive \(\mu\) makes
this the Laplacian of a connected positively weighted graph, with
rank \(F-1\) and sole kernel ones. Its facet contrast parameter is
\(\nu_g=\mu_g+k\mu_g^2/[S_\mu(k-1)]\).
Add orthogonal vectors \(W^A_i,W^F_i\), of norms squared \(\alpha,\beta\),
and set
\[
 W_{i1}=M_i+(W^A_i-W^F_i)/2,\quad
 W_{i2}=M_i+(-W^A_i-W^F_i)/2,\quad W_{i3}=M_i+W^F_i,\quad
 U_{ia}=P_{ia}+W_{ia}.
\]
The identities
\(\mu+\alpha/4+\beta/4=\eta_L,\mu+\beta=\eta_F,
\mu-\beta/2=p_0\) pay every private norm and intersecting leaf/full pair.
Distinct private facets and all old/private pairs are disjoint.

The residual span has dimension \(3F-1\), sole relation \(\sum W=0\).
Also \(\sum P=mz\), since \(2a+b=0\) and all trace terms cancel.
The sum of all proper rows is therefore \(-z\). Take the actual empty
row to be \(z\). The proper core \(C\) has rank \(N-3\), exactly two
kernel vectors: heavy-star indicator \(\chi\), and \(\rho\), equal
to \(m/\ell\) on old/marked rows and 1 on private rows. They are
independent and the dimension count exhausts the kernel.

The actual Gram \(Q\) is the negative-row-sum lift
\[
 Q_{00}=\mathbf1^TC\mathbf1,\quad Q_{0A}=-(C\mathbf1)_A,\quad Q_{AB}=C_{AB}.
\]
Thus \(Q\mathbf1=0,\operatorname{rank}Q=N-3\).
The rational seed \(L_0=J+Q,M_0=(L_0-sI)/(N-s)\) is symmetric,
stochastic and supported, with lower rank \(N-2\). Empty was not deleted.

## Uniform positivity, including all boundary counts

Here \(q\ge8,h\ge3,F\ge9,s\ge17\).
The functions \(r_g/s\) decrease in \(q\):
\(r_x=(\ell+1-q)/\ell,r_y=(12l+2-q)/\ell\).
Their positive values at 8 are below \(1/(3h+8)\); their limiting
negative magnitude is \(1/\ell<1/(3h+8)\). Hence \(|r|/s<1/17\).

The numerator of \(c_0\) at \(q=8\), after discarding \(27ld\),
is \(21h+54l+7>0\). Since
\(F^2-16ld=(h-5l)^2\ge0,\ell>3F,h/F>1/4\),
\[
0<c_0<q/(3F)+3/16<s/(3F)-1/16\le s/27-1/16.
\]
Consequently
\[
\mu>s(8/27-9/578)-15/16>s/5,\qquad \mu<s/3.
\]
For the last strict comparison subtract \(s/5\); its slope
\(13/135-9/578>0\), and its value at \(s=17\) is \(15967/36720>0\).
Since \((2k-3)/(k-1)<2,(k+3)/(k-1)\le5\),
\[
s<\alpha\le2s,\qquad s/2<\beta\le2s/3,\qquad
0<\nu<(s/3)[1+5k/(3F(k-1))]\le37s/81<s/2.
\]
These are all-count inequalities; no finite grid supplies their quantifier.

## Complete physical sectors and the actual row frame

For physical vectors define the metric \(\Gamma\) and frame
\(S(u,v)=\sum_{A\in\mathcal D}(\mathrm{row}_A u)(\mathrm{row}_A v)\),
including the actual empty row. Nonzero eigenvalues of the original
row Gram equal those of this physical frame in its metric, by \(VV^*,V^*V\).

The full decomposition consists of:
\(F\) leaf-odd two-blocks \((T_{i1}-T_{i2},W^A_i)\);
\(k-1\) facet-standard four-blocks in each of four groups
\((\widetilde B_t,TS_t,W^F_t,M_t)\), where \(TS_i=T_{i1}+T_{i2}-2T_{i3}\)
and \(t=(1,\ldots,1,-j,0,\ldots)\), \(j=1,\ldots,k-1\);
twenty aggregate directions; and untouched old pair-sum/difference
spaces of dimensions \(q-2,q-5\).

The aggregate directions are
\[
E,U,R,H_c,H_{d1},H_{d2},\bar B_y,\bar B_z,\bar B_w,\
TS_x,TS_y,TS_z,TS_w,W^F_x,W^F_y,W^F_z,W^F_w,M_x,M_y,M_z,
\]
with group subscripts denoting sums,
\(R=H_x+H_y+H_z+H_w+2U,H_c=3H_x-H_y-H_z-H_w,
H_{d1}=H_y-H_z,H_{d2}=H_y+H_z-2H_w\).
The first nine norms squared are
\(4(q-1),4D,4D(q-4),12qD,2qD,6qD,b_0,b_0,b_0\).
The trace norms are \(6ks,k\beta_g\).
For \(\tau=\mu_x\mu_y/S_\mu\), the mean Gram has heavy diagonal
\(3hl\tau\), heavy/light \(-hl\tau\), light diagonal
\(l\mu_y-l^2\mu_y^2/S_\mu\), and light off-diagonal
\(-l^2\mu_y^2/S_\mu\).
Its three-coordinate restriction is positive definite, since
\(M_w=-M_x-M_y-M_z\) and the full mean kernel is ones.
The mark profiles \(H_a+U/2\) have Gram \(D(qI-J)\), positive for
\(q>4\); these remove four old difference directions, leaving \(q-5\).
The total dimension is
\[
2F+4(F-4)+20+(q-2)+(q-5)=N-3.
\]

Here is a direct all-row account of the aggregate frame. An old proper
row other than \(X\), with incidence bits \(i_x,i_y,i_z,i_w\), has
first-nine *coordinate coefficients*
\[
\left(\frac1{2(q-1)},0,\frac{4-2\sum i}{4(q-4)},
\frac{-3i_x+i_y+i_z+i_w}{6q},
\frac{i_z-i_y}{q},\frac{2i_w-i_y-i_z}{3q},0,0,0\right).
\]
Each bit pattern has count \(q/8\), except 0000 and 1111 have \(q/8-1\).
The full old row is \((-1/2,1/2,0,\ldots)\).
The common vector coefficients are
\[
(-1/(2\ell),3l/(2h\ell),-F/(4h\ell),-d/(4h\ell),0,0,
-3l/\ell,-3l/\ell,-3l/\ell).
\]
A heavy marked row has first four
\((0,-1/(2D),1/(4D),1/(4D))\); a light row has
\((0,-1/(2D),1/(4D),-1/(12D))\).
Its \(H_{d1},H_{d2}\) coefficients are respectively
\((1/(2D),1/(6D)),(-1/(2D),1/(6D)),(0,-1/(3D))\),
and its own light mean coefficient is 1.
Marked leaf/full trace coefficients are \(1/(6k),-1/(3k)\).
A private row has the common first nine, trace coefficients
\(c/(6k),-c/(3k)\), \(W^F\) coefficients \(-1/(2k),1/k\),
and mean coefficients \((1/h,0,0),(0,1/l,0),(0,0,1/l),
(-1/l,-1/l,-1/l)\) by group. Each marked or private type has counts
\(2k,k\). The empty has only the common coefficients.

These formulas also pay the cross-term bridge. Leaf odd signs cancel
opposite leaf rows. Zero-total orthogonal facet profiles cancel every
group-constant projection and each other. Trace coefficients sum to
zero in each three-row facet, so trace/first-nine and trace/mean crosses
vanish. First-nine/mean terms vanish using \(\sum M_i=0\); common
private scores are the same for every facet. Untouched old spaces
are orthogonal to \(G,g_X,H_a\) and therefore have no marked, private
or common projection. Their old frame eigenvalues remain \(2q,2D\).
All light-equivariant matrices have constant diagonal and off-diagonal
group entries. Hence the first nine split into the even five-block
\((E,U,R,H_c,\bar B_y+\bar B_z+\bar B_w)\) and two light-standard
two-blocks, with profiles \((1,-1,0),(1,1,-2)\), of norms squared 2,6.
They are mutually orthogonal in metric and frame. Thus the above
census pays every cross term as well as every dimension.

## Every cap block outside the even five

For leaf odd the metric is \(\operatorname{diag}(2s,\alpha)\), with
coordinate rows \((1/2,0),(-1/2,0),(-c/2,1/2),(c/2,-1/2)\), once each.
The standard prototype metric is
\(\operatorname{diag}(2s/3,12s,2\beta,2\nu)\), with coordinates/counts
\[
\begin{array}{c|c}
(1/2,1/12,0,0)&4\\
(1/2,-1/6,0,0)&2\\
(a/2,c/12,-1/4,1/2)&4\\
(-a,c/[6(k-1)],1/2,1/2)&2
\end{array}
\]
Both metric and coordinate-frame form multiply by the squared facet
profile norm divided by 2. Normalization removes that factor.
For the trace block the metric is \(\operatorname{diag}(6ks,k\beta)\);
marked coordinates \((1/(6k),0),(-1/(3k),0)\) and private coordinates
\((c/(6k),-1/(2k)),(-c/(3k),1/k)\) have counts \(2k,k\).

Direct outer products give standard normalized diagonal entries
\(s(1+2a^2),s[1+c^2/3+2c^2/(3(k-1)^2)],3\beta/2,3\nu\);
its four nonzero off-diagonal magnitudes are
\[
s|ac z_*|\sqrt2/3,\quad |a|\sqrt{3s\beta},\quad
|cz_*|\sqrt{6s\beta}/6,\quad
|c|k\sqrt{6s\nu}/[3(k-1)],\qquad z_*=(k-3)/(k-1).
\]
All other off-diagonal entries vanish. Leaf normalized diagonals are
\(s(1+c^2),\alpha/2\), off magnitude \(|c|\sqrt{2s\alpha}/2\);
trace diagonals are \(s(1+c^2),3\beta/2\), off magnitude
\(|c|\sqrt{6s\beta}/2\).

Use \(|a|<3/17<3/13,|c|<9/34<9/26,|z_*|\le1,
k/(k-1)\le2,\beta\le2s/3,\nu<37s/81<29s/57\),
\(\sqrt2<3/2,\sqrt{58/19}<7/4\).
The standard absolute row sums are bounded by
\(1009s/676,1135s/676,19s/13,1907s/988\), all below \(2s\).
For example the four off-diagonal bounds divided by \(s\) are
\(27/676,9/26,3/26,21/52\); the fourth diagonal is at most \(29/19\).
Leaf and trace row sums are bounded by \(991s/676<2s\).

The full residual mean Gram has absolute row sum \(2\mu_g<2s/3\).
Each mean occurs on three private rows, so its frame operator is
three times that Gram and is below \(2s\). Untouched old eigenvalues
\(2q,2D\) are below \(2s\).

For each light-standard two-block put \(t=l/h\). Its normalized frame
has diagonals \(6h+qt,s(1-t)\), and off-diagonal square \(qst(1-t)\).
The bit-pattern old scores contribute \(2qD^2\) times the squared
light profile norm; marked light scores supply the remaining outer
products. Heavy, common, private and empty scores in these directions
are zero. Both copies are paid, including factors 2 and 6.
For \(T=N-1\), the first cap diagonal is \(q(2-t)+18l-1>0\), and
\[
\det(TI-S_{\rm light})=(T-6h)(T-s)+3l(T-2s)
=(2q+18l-1)(q+3h+18l-1)+3l(18l-1)>0.
\]
Thus these blocks are capped at \(T\); all earlier blocks are below
\(2s<T\).

## Full coefficient certificate and its universal decoding

In the even five basis the metric is
\(\Gamma_5=\operatorname{diag}(4(q-1),4D,4D(q-4),12qD,sd/(hl))\).
The old frame has entries
\[
(S_{\rm old})_{00}=4(q^2-1),\ (S_{\rm old})_{01}=-4D(q-1),\
(S_{\rm old})_{11}=4D^2,\
(S_{\rm old})_{22}=8D^2(q-4),\
(S_{\rm old})_{33}=24qD^2,
\]
and no others. The full frame is
\[
S_5=S_{\rm old}+3h j_xj_x^T+9l j_lj_l^T+ZZ^T/\ell,
\]
where \(j_x=(0,-2,q-4,3q,0)\),
\(j_l=(0,-2,q-4,-q,sd/(3hl))\), and
\(Z=(-2(q-1),18l,-3F(q-4),-9qd,-3sd/h)\).
The \(\ell=m+1\) common contributions include all private rows and
the actual empty. These scores follow from every row/count above.

The compact disclosed DATA is exactly the 38415-byte author certificate
from source 9e7ada1cd3b0b966815e1711c9212e94dad2881f,
SHA256 3cdbf637209133ce6549fe9567a39d39cff4abff5d422f5ea31e40dde5cf0cb7.
It has 59 full polynomials, 55 fields, all 25 initial addresses and
30 ordered Schur updates. Independently reconstructed forms in
\(d=1+u,l=2+v,h=l+d,q=8+w\) bind every initial field of
\(\Gamma_5^{-1}(T\Gamma_5-S_5)\), for all real \(u,v,w\ge0\).
Every cleared update is checked in full, with exact working links.
The five numerator supports have 9,31,50,72,103 terms. All 265
coefficients are nonnegative, with positive constants; every
denominator factor has the same positivity properties.

The reader's integer identity decoding is justified as follows.
For the entire cleared expression bound every coordinate degree by
\(D_i\), and bound every coefficient magnitude by the sum \(C\) of
product coefficient \(\ell^1\) bounds. Choose a power of two \(B>2C\),
and substitute \(B,B^{D_0+1},B^{(D_0+1)(D_1+1)}\).
Every admissible monomial occupies a distinct base-\(B\) position.
If the encoded expression is zero, its lowest nonzero coefficient
would be divisible by \(B\), impossible for magnitude below \(B/2\).
Successive reduction proves all coefficients zero. This is complete
coefficient decoding, not point sampling. Every factor, power, degree
and norm bound is paid; the largest encoding bound is 272033 bytes,
within the fixed 4 MiB guard.

Since the original cap form is symmetric with positive metric,
row-normalized Schur pivots equal symmetric pivots divided by the
positive metric diagonal at each stage. Positive pivots therefore
prove \(T\Gamma_5-S_5\succ0\).
The complete sector census and the \(VV^*,V^*V\) bridge now give
\(Q\preceq TP\). Hence \(NI-L_0=NP-Q\succeq P\), with sole kernel ones.

## Whole original dual, exact real lower line and outside witnesses

On proper rows let \(a_0\) be \(1/h\) on all heavy private rows,
and \(b_0'\) be \(1/(3l)\) on all light private full rows, zero elsewhere.
Their disjoint supports have sums 3 and 1. Set
\(p=a_0-3b_0'\), \(c_*=(a_0+3b_0')/6\).
Then
\[
 C_\delta=C+\delta(a_0b_0'^T+b_0'a_0^T)
 =C-\delta pp^T/6+6\delta c_*c_*^T.
\]
Every modified pair is disjoint. Also
\(p^T\chi=c_*^T\chi=p^T\rho=0,c_*^T\rho=1\).

The complete physical dual is
\[
 Z_*=\frac{M_x}{3hl\tau}
       -\frac{2(W^F_y+W^F_z+W^F_w)}{3l\beta_y}.
\]
The mean term gives heavy private score \(1/h\), light score
\(-1/(3l)\); the \(W^F\) term cancels each light leaf and gives each
light full total \(-1/l\). All old, marked and actual empty scores vanish.
Thus its full score is \(p\), and
\[
\kappa=\|Z_*\|^2=\frac1{3hl\tau}+\frac4{3l\beta_y}
=\frac1{h\mu_x}+\frac1{3l\mu_y}+\frac4{3l\beta_y}.
\]
The physical span is complete, so this score specifies a unique dual.
Every solution \(Cx=p\) therefore has
\(p^Tx=x^TCx=\kappa\). Such a solution exists since \(p\) is orthogonal
to both core kernels. The two finite controls independently invert
an original principal submatrix and check every original equation,
including both removed rows, without using this dual as solver input.
Uniform bounds give \(0<\kappa<5/(hs)+13/(3ls)\le23/102\).

After quotienting \(\chi\), write a proper vector as \(u+t\rho\),
\(u\in\operatorname{ran}C\). For \(\delta>0\) its energy is
\[
u^TCu-\delta(p^Tu)^2/6+6\delta(c_*^Tu+t)^2.
\]
Replace \(t\) by \(t+c_*^Tu\); this is invertible. The remaining
rank-one downdate on the positive range is PSD exactly when
\(\delta\kappa\le6\), positive definite when strict.
Thus the entire lower interval is \([0,6/\kappa]\); the proper rank
is \(N-2\) inside, \(N-3\) at both ends. The actual lift preserves
that rank and adding \(J\) adds one, giving the stated lower ranks.

For \(\delta<0\), \(\rho\) has energy \(6\delta<0\).
For \(\delta>6/\kappa\), take \(Cx=p\) and
\(v=x-(c_*^Tx)\rho\). Then \(c_*^Tv=0,p^Tv=\kappa\), and its energy
is \(\kappa(1-\delta\kappa/6)<0\).
Centering the full original vector \((0,v)\) preserves this energy
in \(L_\delta\), since the lift annihilates ones and \(J\) kills
centered vectors. At \(\delta=6/\kappa\), this \(v\) is the additional
core null vector. The controls give complete centered witnesses at
\(-1,7/\kappa\), including their actual empty coordinates.
These witnesses refute only this line outside its interval.

## Proved improved cap, greatest ranks, rationality and invariance

Lift \(a_0,b_0'\) to zero-sum full vectors
\(A=(-3,a_0),B=(-1,b_0')\). The actual perturbation is
\(\delta(AB^T+BA^T)\), and
\[
A^TB=3,\quad\|A\|^2=9+3/h\le10,\quad
\|B\|^2=1+1/(3l)\le7/6.
\]
Its two nonzero eigenvalues are \(3\pm\|A\|\|B\|\); therefore its
operator norm is at most \(3+\sqrt{35/3}<103/16\).
The last strict comparison follows from
\(35/3<(55/16)^2\). It acts in ones-perpendicular, giving the refined
cap stated above. For \(0<\delta\le3/20\), the floor is at least
\(11/320>0\) and \(\delta\kappa<6\), so both ranks are \(N-1\).
At \(1/32\) the floor is \(409/512>25/32\).

Stochasticity forces \(\operatorname{rank}(I-M)\le N-1\).
For any supported stochastic \(M\) with \(L\succeq0\), the heavy-star
indicator has \(\chi^TM\chi=0\) and \(L\mathbf1=N\mathbf1\).
Its centered indicator therefore has zero \(L\)-energy, so is a
nonzero kernel vector. Thus the lower ceiling is also \(N-1\).
The attained lower kernel is exactly the centered heavy star; the
upper kernel is exactly ones. The least eigenvalue
\(-s/(N-s)\) and unit eigenvalue of \(M\) are simple.

Every Gram entry and lifted entry is rational for integer counts and
rational \(\delta\); the rational existence statement uses \(1/32\).
The real parameter interval does not assert rationality at irrational
parameters. Every formula respects leaf swaps, group facet permutations,
unmarked old permutations and permutations of the three identical
light groups. This proves actual original invariance.

## Strengthening and improvement opportunities

The proved \(3/20\) range and the \(11/320,409/512\) floors strengthen
the target's stated sufficient cap. A parameter-dependent norm
\(3+\sqrt{(9+3/h)(1+1/(3l))}\) is also a valid sufficient bound.
It does not identify the optimal upper PSD interval. A sharper next
step is an original-coordinate two-vector resolvent of \(NI-L_0\),
with proof that the physical mean reduction preserves that resolvent.
Formalizing the original-to-physical frame bridge and the symmetric
Schur certificate would remove the most consequential ordinary proof
trust boundaries. Unequal light counts and additional marks need fresh
complete physical sectors and certificate data; this verdict does not
transfer to those separate claims.
