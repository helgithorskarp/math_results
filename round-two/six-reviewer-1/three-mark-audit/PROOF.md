# Independent proof audit and a larger three-mark repair interval

Reviewer: **six-reviewer-1**, independent mathematical reviewer. This is an
ordinary proof with a completely checked polynomial certificate, not a
proof-assistant formalization. The selected original is **LEMMA10294/0**,
`bafkreig6sm3ykbawfgskgtln2mkhtwyeya55zpul2vjas3vpx6jgvo7naa`, by
six-downset-1. Its construction and coefficient data are credited inputs;
the implementations here are newly written by this reviewer.

## Scope and conventions

Let \(X\) have \(n\ge3\) elements and choose three distinct marks \(x,y,z\).
Attach \(h\) triangles \(\{x,u_i,v_i\}\), \(\ell\) triangles at each of
\(y,z\), with integer \(h>\ell\ge2\). Every private pair is disjoint
from every other pair and from \(X\). The downset \(D\) consists of the
whole old cube and all subsets of these triangles. Keep the actual empty
set, including its permitted loop. Put

\[
 q=2^{n-1},\quad F=h+2\ell,\quad m=3F,\quad e=m+1,\quad
 D_0=3h,\quad s=q+3h,\quad N=2q+6F=2s+12\ell.
\]

The star sizes are \(s\), twice \(q+3\ell\), \(q\) for every other old
element, and \(4\) for every private element. Thus the heavy star is the
unique maximum. A supported symmetric stochastic matrix means real
entries, zero at intersections and at every nonempty diagonal, with a
possible loop at the empty set; entrywise positivity is not required.
Write \(P=I-J/N\). The lower endpoint is \(L=sI+(N-s)M\).

The original claims an invariant rational example with both endpoint
ranks \(N-1\) and \(NI-L\succeq(25/32)P\), a repair for every real
\(0<\delta\le1/8\), and an exact lower-PSD interval for that line. The
audit below pays the whole original geometry, including the empty row
and every physical sector. It also proves

\[
 0<\delta\le3/20\quad\Longrightarrow\quad
 NI-L_\delta\succeq(1-105\delta/16)P\succeq P/64.
\]

Both endpoint ranks remain \(N-1\) throughout this enlarged interval.
At the original rational choice \(\delta=1/32\), the improved floor is
\(407/512\). These upper-cap bounds are sufficient bounds; no optimal
upper-PSD endpoint is claimed.

## Original Gram and support

For every nonempty old set use vectors \(g_A\) with Gram

\[
 g_A\cdot g_B=s[A=B]+(q-D_0)[B=X\setminus A]-1.
\]

There are \(q-1\) complementary proper pairs. Their difference
space has eigenvalue \(2D_0\). The pair-sum space orthogonal to its
sum has eigenvalue \(2q\) and dimension \(q-2\). With
\(G=\sum g_A\), \(E=G-g_X\), \(U=G+g_X\), the remaining orthogonal
directions have squared norms \(4(q-1),4D_0\). This proves positive
old rank \(2q-1\), including \(q=4\).

For each mark set \(H_a=-\sum_{A\ni a}g_A\). Direct cube counting gives

\[
 H_a^2=qD_0,\quad H_a\cdot H_b=0\ (a\ne b),\quad
 G\cdot H_a=g_X\cdot H_a=-D_0,\quad
 g_A\cdot H_a=D_0(1-2[a\in A]).
\]

For a group of \(k=h\) or \(\ell\) facets take mutually independent
group spaces with \(B_i\cdot B_j=(s/3)([i=j]-1/h)\). The heavy
group has its single sum relation; each light group is positive on its
whole \(\ell\)-dimensional span. Set \(\bar B=k^{-1}\sum B_i\),
\(\widetilde B_i=B_i-\bar B\). The heavy mean is zero; the two light
means are orthogonal and have squared norm \(s(h-\ell)/(3h\ell)>0\).
Keep both light means. For each facet take an independent two-dimensional
space \(T_{i1}+T_{i2}+T_{i3}=0\),
\(T_{ia}\cdot T_{ib}=s([a=b]-1/3)\).

The three marked rows are \(H_a/D_0+B_i+T_{ia}\), indexed by
\(\{a,u_i\},\{a,v_i\},\{a,u_i,v_i\}\). Their norms are \(s-1\);
every required marked/old or marked/marked intersection has product
\(-1\). These old and marked rows span dimension \(2q+m-2\), with
the heavy-star sum as their unique relation.

Let \(K\) be their sum and \(z_0=-K/e\). Writing \(d=h-\ell\),

\[
 K=G+H_x+(\ell/h)(H_y+H_z)+3\ell(\bar B_y+\bar B_z),
 \quad c_0=z_0^2={qe+18\ell d-3h-12\ell-1\over e^2}.
\]

Its marked score is \(-(q-1)/e\) in the heavy group and
\(-(q+3d-1)/e\) in either light group. For each group put
\(r=1+z_0\cdot V_i\), \(B_2=s(k-1)/(3k)\),
\(a=r/(2B_2), b=-2a, c=9r/(2s)\). The three old-span private
projections are

\[
 P_{i1}=z_0+a\widetilde B_i+cT_{i2},\quad
 P_{i2}=z_0+a\widetilde B_i+cT_{i1},\quad
 P_{i3}=z_0+b\widetilde B_i+{c\over k-1}\sum_{j\ne i}T_{j3}.
\]

For example an intersecting marked/private leaf product is
\(z_0\cdot V_i+aB_2-cs/3=-1\). A private full set intersects the
three marked rows of its facet, with product \(z_0\cdot V_i+bB_2=-1\).
Other proper intersections are covered by the old and marked formulas;
private pairs in different facets are disjoint.

Define the required residual norms \(\eta_L,\eta_F\) by subtracting
these projection norms from \(s-1\), and put
\(p_0=-1-c_0-abB_2\), \(\mu=(2p_0+\eta_F)/3\),
\(\alpha=2(2\eta_L-p_0-\eta_F)\), \(\beta=\eta_F-\mu\).
Expanding the displayed projections gives

\[
 \mu={s-3\over3}-c_0-{9r^2\over2s(k-1)},\quad
 \alpha=2s-{27(2k-3)r^2\over s(k-1)},\quad
 \beta={2s\over3}-{3(k+3)r^2\over s(k-1)}.
\]

## Uniform scalar positivity and completeness

For both groups, elementary linear-over-linear comparison in \(q\)
gives \(|r|/s<1/(3h+4)\). Also
\(0<c_0<q/(3F)+1/6\), using
\(F^2-12\ell(h-\ell)=(h-4\ell)^2\). Hence

\[
 s/5<\mu<s/3,\quad s<\alpha\le2s,\quad s/2<\beta\le2s/3.
\]

For clarity the only small-count exception in the estimate is
\(h=3,\ell=2\). For \(h\ge4\), \(F\ge8\), \(s\ge16\), and
\(h/F>1/3\), the formula implies
\(\mu>(421/1536)s-5/6\); its margin over \(s/5\) is at least
\(169/480>0\). When \(h=3,\ell=2\),
\(c_0=q/22+1/242\) and the corresponding margin is greater than
\(4748/23595>0\). These cover every allowed count.

Let \(S_\mu=h\mu_x+2\ell\mu_y\). Take mean vectors with diagonal
\(\mu_g\), same-group off-diagonal
\(-k\mu_g^2/[S_\mu(k-1)]\), and cross-group off-diagonal
\(-\mu_g\mu_t/S_\mu\). This is the Gram of a connected weighted
Laplacian: rank \(F-1\), sole relation \(\sum M_i=0\).
Its within-group contrast eigenvalue
\(\nu_g=\mu_g+k\mu_g^2/[S_\mu(k-1)]<31s/63<s/2\).
Take independent residual vectors of norms \(\alpha_g\) and
\(\beta_g\), denoted \(W^A_i,W^F_i\), and use

\[
 W_{i1}=M_i+(W^A_i-W^F_i)/2,\quad
 W_{i2}=M_i+(-W^A_i-W^F_i)/2,\quad W_{i3}=M_i+W^F_i.
\]

The identities \(\mu+\alpha/4+\beta/4=\eta_L\),
\(\mu+\beta=\eta_F\), \(\mu-\beta/2=p_0\) prove all private
norms and support equations for \(U_i=P_i+W_i\). The residual
span has dimension \(3F-1=m-1\), sole private-row sum relation.
Together the proper rows span \(N-3\) dimensions. Their two kernel
relations are the heavy-star indicator \(\chi\) and
\(\rho=(m/e\text{ on old/marked},1\text{ on private})\).
They are independent and exhaust the kernel.

The sum of all private projections is \(m z_0\); the sum of all
proper rows is therefore \(-z_0\). Thus the actual empty row is
precisely \(z_0\), not an independently chosen quotient coordinate.
The full Gram \(Q\) has rank \(N-3\), \(Q1=0\), and the same support.
The seed \(L_0=J+Q\) is positive with rank \(N-2\).

## Cap on every physical direction

The original Gram cap is equivalent to the frame inequality
\(S\preceq(N-1)\Gamma\) on the physical span, where
\(S(v,w)=\sum_{A\in D}(v\cdot V_A)(w\cdot V_A)\) includes the
actual empty vector. Leaf parity, orthogonal sum-zero facet profiles,
and group sums produce the following metric-and-frame-orthogonal blocks:

* \(F\) leaf-odd blocks \((T_{i1}-T_{i2},W^A_i)\), dimension two each.
* \(k-1\) standard blocks per group
  \((\widetilde B_t,TS_t,W^F_t,M_t)\), dimension four each, where
  \(TS_i=T_{i1}+T_{i2}-2T_{i3}\). The Helmert profiles
  \((1,\ldots,1,-j,0,\ldots,0)\) exhaust the sum-zero space.
* An even block \((E,U,R,H_c,\bar B_y+\bar B_z)\) of dimension five
  and an odd block \((H_d,\bar B_y-\bar B_z)\) of dimension two,
  with \(R=H_x+H_y+H_z+3U/2\),
  \(H_c=2H_x-H_y-H_z\), \(H_d=H_y-H_z\).
* Three group-trace blocks \((TS_g,W^F_g)\), dimension two each,
  and the two-dimensional whole-group mean space \((M_x,M_y)\).
* Untouched old pair-sum and pair-difference spaces of dimensions
  \(q-2,q-4\), with frame eigenvalues \(2q,6h\).

Their dimensions sum to \(N-3\), including the zero old odd space
at \(n=3\). The first five old aggregate directions are orthogonal,
with norms \(4(q-1),4D_0,3D_0(q-3),6qD_0,2qD_0\).
Both nonzero light means are retained. Mean-group sums have Gram
\(M_x^2=2h\ell\tau, M_x\cdot M_y=-h\ell\tau\),
\(M_y^2=\ell\mu_y-\ell^2\mu_y^2/S_\mu\), where
\(\tau=\mu_x\mu_y/S_\mu\), and hence are independent.

Here is an explicit check of the frame bridge. A proper old row other
than \(X\) has coefficients on
\((E,U,R,H_c,H_d,\bar B_y,\bar B_z)\)

\[
 \left({1\over2(q-1)},0,{3-2(i_x+i_y+i_z)\over3(q-3)},
 {-2i_x+i_y+i_z\over3q},{i_z-i_y\over q},0,0\right).
\]

Each of its eight mark patterns has multiplicity \(q/4\), except
000 and 111 have \(q/4-1\). The full old row is
\((-1/2,1/2,0,\ldots,0)\). The common vector coefficients are
\((-1/(2e),\ell/(he),-F/(3he),-d/(3he),0,-3\ell/e,-3\ell/e)\).
Heavy marked rows have old coefficients
\((0,-1/(2D_0),1/(3D_0),1/(3D_0),0)\); light marked rows have
\((0,-1/(2D_0),1/(3D_0),-1/(6D_0),\pm1/(2D_0))\), and their
own light-mean coefficient one. Marked leaf/full trace coefficients
are \(1/(6k),-1/(3k)\). Private leaf/full trace coefficients are
\(c/(6k),-c/(3k)\), their full-residual coefficients
\(-1/(2k),1/k\), and their group-mean coefficients respectively
\((1/h,0),(0,1/\ell),(-1/\ell,-1/\ell)\).
There are \(2k\) leaf and \(k\) full rows of each kind.

Summing these complete row types cancels every aggregate/trace/mean
cross entry; parity and sum-zero profiles cancel the other crosses.
Exchange of the two light groups splits the seven-dimensional first
aggregate space into the stated five and two. This pays every original
direction, without a missing multiplicity or empty-set assumption.

For a standard block the normalized diagonal frame entries are
\(s(1+2a^2),s[1+c^2/3+2c^2/(3(k-1)^2)],3\beta/2,3\nu\).
Its only off-diagonal magnitudes are
\(s|ac\zeta|\sqrt2/3, |a|\sqrt{3s\beta},
 |c\zeta|\sqrt{6s\beta}/6, |c|k\sqrt{6s\nu}/[3(k-1)]\),
where \(\zeta=(k-3)/(k-1)\). The scalar bounds give
\(|a|<3/13,|c|<9/26,|\zeta|\le1,k/(k-1)\le2\).
Using \(\sqrt2<3/2\), \(\nu<29s/57\),
\(\sqrt{58/19}<7/4\), their four row sums divided by \(s\)
are bounded by \(1009/676,1135/676,19/13,1907/988<2\).
The same direct leaf and trace row sums give \(991s/676<2s\).
The mean Laplacian has eigenvalues at most \(2\max\mu_g<2s/3\);
the private frame is three times this Gram. Both untouched eigenvalues
are below \(2s\). All these bounds are below \(N-1\).

For the odd two-block put \(t=\ell/h\). Its normalized frame has
diagonals \(6h+qt,s(1-t)\) and off-diagonal square
\(qs t(1-t)\). With \(T=N-1\), its first cap diagonal is positive;
its determinant equals

\[
 (2q+12\ell-1)(q+3h+15\ell-1)-6q\ell
 =2q(q+3h+12\ell-1)+(12\ell-1)(q+3h+15\ell-1)>0.
\]

For the remaining even-five block the metric is
\(G_5=\operatorname{diag}(4(q-1),4D_0,3D_0(q-3),6qD_0,
2sd/(3h\ell))\). Cube counting gives old frame entries
\(S_{00}=4(q^2-1),S_{01}=S_{10}=-4D_0(q-1),
S_{11}=4D_0^2,S_{22}=6D_0^2(q-3),S_{33}=12qD_0^2\), others zero.
The remaining whole frame is

\[
 S_5=S_{\rm old}+3h j_xj_x^T+6\ell j_lj_l^T+ZZ^T/e,
\]

\(j_x=(0,-2,q-3,2q,0)\),
\(j_l=(0,-2,q-3,-q,sd/(3h\ell))\),
\(Z=(-2(q-1),12\ell,-3F(q-3),-6qd,-2sd/h)\).
The last term includes all private common projections and the actual
empty row. Our polynomial code independently sums all eight old patterns
and the full old row, then clears \(3h\ell\) in every entry.

Set \(d=1+u,\ell=2+v,q=4+w\). The disclosed data has 59 whole
polynomials and 55 whole rational fields. Our reader verifies every one
of the 25 initial entries of \(G_5^{-1}(TG_5-S_5)\), all 30 ordered
Schur updates, and all five pivot working links. The five numerator
sizes are 9,31,50,72,103: all 265 coefficients are nonnegative and each
constant is positive. Every denominator factor has nonnegative
coefficients and positive constant. Consequently all pivots are positive
for every real \(u,v,w\ge0\). Multiplying the row-normalized Schur
matrices by the positive corresponding metric diagonals gives the
symmetric Schur congruence, proving \(TG_5-S_5\succ0\).

For each cleared identity our reader computes a full coordinate-degree
bound and coefficient absolute-sum bound \(C\). It chooses \(B>2C\)
and evaluates at \((B,B^{D_u+1},B^{(D_u+1)(D_v+1)})\).
Distinct exponent triples within the bounds have distinct base positions.
If the integer value is zero, reducing successively modulo \(B\) shows
every integer coefficient is zero, since its absolute value is below
\(B/2\). Bounds include all factors and denominator powers, rather
than assuming a sampled equality. The largest encoding bound is
250729 bytes, below the fixed 4 MiB guard. Together with the exhaustive
physical bridge, this proves \(Q\preceq(N-1)P\) for every allowed
integer count; finite controls are supplementary validation.
Therefore \(NI-L_0\succeq P\).

## Exact lower-PSD repair line

On proper rows let \(a\) be the heavy-private indicator divided by
\(h\), and \(b\) the indicator of all light private full sets divided
by \(2\ell\). Their supports are disjoint and their sums are 3 and 1.
With \(p=a-3b\), \(c=(a+3b)/6\), set

\[
 C_\delta=C+\delta(ab^T+ba^T)
 =C-(\delta/6)pp^T+6\delta cc^T.
\]

Only disjoint proper pairs change. The exact relations are
\(p\cdot\chi=c\cdot\chi=p\cdot\rho=0\), \(c\cdot\rho=1\).
The full physical dual is

\[
 Z_*={M_x\over2h\ell\tau}-{W^F_y+W^F_z\over\ell\beta_y},
 \qquad \kappa=\|Z_*\|^2
 ={1\over h\mu_x}+{1\over2\ell\mu_y}+{2\over\ell\beta_y}.
\]

Heavy mean scores give \(1/h\), light leaf mean scores cancel their
full-residual scores, and light full scores are \(-3/(2\ell)\).
Old, marked, and actual empty scores are zero. Thus the proper score
vector is exactly \(p\). The paid full physical span proves
\(p^TC^\dagger p=\kappa\). In particular any solution \(Cx=p\)
has \(x^TCx=p^Tx=\kappa\). The uniform scalar estimates give

\[
 0<\kappa<{5\over hs}+{13\over2\ell s}
 \le {5\over39}+{1\over4}={59\over156}.
\]

Modulo \(\chi\), decompose a vector as a ran\((C)\) component plus
a multiple of \(\rho\). For \(\delta>0\), minimizing the energy
over the latter component cancels the entire positive
\(6\delta cc^T\) term, leaving \(C-(\delta/6)pp^T\) on ran\((C)\).
Its positivity is exactly \(\delta\kappa\le6\). It is strictly
positive before equality and has a single extra null direction at
equality. At zero the original two kernel directions return.

For \(\delta<0\), the original \(\rho\) has energy \(6\delta<0\).
For \(\delta>6/\kappa\), choose \(Cx=p\) and let
\(v=x-(c^Tx)\rho\). Then \(c^Tv=0,p^Tv=\kappa,v^TCv=\kappa\),
so \(v^TC_\delta v=\kappa(1-\delta\kappa/6)<0\).
The actual empty negative-row-sum lift preserves this proper energy;
centering \((0,v)\) preserves it too. This proves the exact interval
\(0\le\delta\le6/\kappa\), with lower ranks \(N-2\) at both
endpoints and \(N-1\) inside after \(J\) is added. These negative
witnesses concern this proposed line only.

## Proved larger cap interval and greatest ranks

Lift \(a,b\) to zero-sum full vectors \(A=(-3,a), B=(-1,b)\).
Then \(L_\delta-L_0=\delta(AB^T+BA^T)\),
\(A\cdot B=3\), \(A^2=9+3/h\), \(B^2=1+1/(2\ell)\).
The two nonzero eigenvalues of \(AB^T+BA^T\) are exactly

\[
 3\pm\sqrt{(9+3/h)(1+1/(2\ell))}.
\]

This follows by its action on \(\operatorname{span}(A,B)\), and the
operator vanishes on its orthogonal complement. Its largest eigenvalue
is at most \(3+5/\sqrt2<105/16\), since
\((105/16-3)^2-25/2=49/256>0\).
As both vectors lie in \(1^\perp\), the seed cap proves
\(NI-L_\delta\succeq(1-105\delta/16)P\) for \(\delta\ge0\).
At \(3/20\) this is \(P/64\); at \(1/32\), \(407P/512\).
Also \((3/20)\kappa<6\), so the enlarged positive interval lies
strictly inside the exact lower interval.

The remaining lower kernel is the centered heavy star, and the upper
kernel is exactly the constants. Every supported stochastic admissible
matrix has the centered maximum-star zero lower energy: the star's
proper diagonal entries are \(s\) and its off-diagonal intersections
are zero. A PSD lower endpoint therefore has rank at most \(N-1\).
Stochasticity similarly bounds the upper rank by \(N-1\). The
constructed ranks attain both ceilings; the minimum eigenvalue of
\(M_\delta\) is \(-s/(N-s)\) and is simple, as is its unit eigenvalue.
All index formulas respect leaf swaps, group facet permutations,
unmarked-old permutations and exchange of the light marks, so the full
matrices are invariant. Rational \(\delta\) gives rational matrices.

## Independent controls and limits

The source rebuilds every original set and every original Gram position
at \((n,h,\ell)=(3,3,2),(4,3,2),(4,4,3)\), with
\((N,s)=(50,13),(58,17),(76,20)\). It checks all star sizes, immediate
subset closure, support, norms, empty sum, both kernel relations, full
physical dimension, every cross-block metric/frame entry and literal
invariance generators. It independently binds all 75 even-five form
positions and all original dual scores. Full rational symmetric
elimination checks the original seed, its cap, the lower ranks at
\(1/32,3/20,6/\kappa\), and the new \(1/64\) upper floor. No floating
eigenvalue, target runtime, target EXPECTED file, private corpus or
inherited reviewer verdict supplies a gate.

These finite instances do not establish the infinite theorem by
sampling. The ordinary reductions, dimension argument, scalar bounds
and complete polynomial identities above pay its quantifiers. The
remaining trust boundary is the ordinary unformalized proof, the fresh
code, CPython and arbitrary-precision arithmetic. The disclosed author
certificate is explicit data input, checked in full; its hash alone is
not a mathematical proof. No global Conjecture H/I, entrywise-positive
extension, four-mark theorem, or optimal upper interval follows here.
