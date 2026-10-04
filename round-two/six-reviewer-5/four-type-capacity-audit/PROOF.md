# Independent four-type capacity audit and unequal-light extension

Actual author six-reviewer-5, independent mathematical reviewer, 2026-10-04.
Ordinary proofs below are complete at the stated scope and UNFORMALIZED.
Only the capacity/degree and necessary-envelope components of LEMMA10332
are reviewed. No all-count physical PSD criterion, q19 feasible optimizer,
attainment, rank, recipe endpoint, or general H/I verdict is asserted.

## Original-coordinate necessity and the credited mass identity

Let a downset have N members, maximum-star size s and h=N-s>0. An original
H competitor M is real symmetric, stochastic, zero on intersecting pairs
(including every nonempty diagonal), and has hM+sI positive semidefinite.
Let S be the maximum star and z=N1_S-s1. Support and M1=1 give
z'Mz=-Ns^2 and z'z=Nsh. Thus L=hM+sI satisfies z'Lz=0; PSD forces Lz=0,
and L1=N1 implies L1_S=s1. On proper members C=L_proper-J has C1_S=0.
This is an ordinary Rayleigh/kernel argument for EVERY individual real
competitor; it does not assume invariance or a rational matrix.

For a comparison C0 with the same fixed diagonal/intersection values and
C0 1_S=0, write B for nonstar proper members. The original completion is
L0=J+E C0 E', E=[-1';I]. Its nonstar empty budgets and actual loop budget
are ell_v=1-sum_w C0_vw and ell0=1+sum_vw C0_vw-s. This definition does
not presume PSD of C0 or feasibility of the comparison. On unordered
disjoint NN edges let delta=C-C0 and c_e=1+C0_e. Both centered-star row
identities imply that star changes have zero row sum on B. Therefore the
ACTUAL empty budgets satisfy E_v=ell_v-sum_incident delta_e and
E0=ell0+2sum_e delta_e. The empty loop and unordered factor two are retained.

Let K={v in B:ell_v<0}, G=B\K, d_v=-ell_v, D=sum_K d_v,
P0=(D-ell0)/2 and P=sum_e(delta_e)_+. Expanding sums gives

\[
2(P-P_0)=\sum_K E_v+E_0+2\sum_{KK}(\delta_e)_+
                  +\sum_{KG}|\delta_e|+2\sum_{GG}(-\delta_e)_+.
\]

Indeed sum_K E_v+E0=-2P0+sum_KG delta+2sum_GG delta;
subtract this from 2(P-P0) and use 2x_+-x=|x|. This generic identity is
credited to prior10296/10306, with the original lift credited to10248.
No count-specific numerical premise or prior PSD certificate is used.
If every allowed original M entry is at least tau/h, tau>=0, then
E_v,E0>=tau and delta_e>=tau-c_e. Hence, universally,

\[
P\ge P_0+\frac{|K|+1}{2}\tau+
       \sum_{KK}(\tau-c_e)_++\frac12\sum_{KG}(\tau-c_e)_+ . \tag{1}
\]

This is a NECESSARY envelope, not an existence theorem or optimal cost
curve. Equality in the weaker plane P=P0+(|K|+1)tau/2 requires all bad and
loop budgets equal tau, KK changes nonpositive, KG changes zero and GG
changes nonnegative. Put x_e=-delta_e on KK. Then each bad degree is
sum_incident x_e=d_v+tau and 0<=x_e<=c_e-tau. The negative-flow condition
is only one necessary component of full equality/feasibility.

## Five-orbit iff without equal-light demands or capacities

Take distinct core points b,c and a set Y of m>=3 points. The bad vertices
are all YY pairs, B_y={b,y}, C_y={c,y}, T_y={b,c,y}. Join precisely disjoint
original sets. Demands are constant on each named type:
d=(dYY,dB,dC,dT)>0. Capacities c=(c0,c1,c2,c3,c4) are respectively YY/YY,
YY/B, YY/C, YY/T and B/C. They may be real and need not satisfy c1=c2
or dB=dC. Let tau>=0. For m=3 the YY/YY edge type is absent and c0 is
irrelevant; other four types have actual edges.

Set n=binom(m-1,2), p=m-2, a2=binom(m-2,2), r=m-1 and U_j=c_j-tau.
All denominators below are positive. Define

\[
\beta=(d_T+\tau)/n,\quad A=d_{YY}+\tau-p\beta,
\quad B=d_B+\tau,\quad C=d_C+\tau,
\quad W=2(B+C)/r-A.
\]

A nonnegative, individually capacitated real KK flow with all stated
degrees exists IFF 0<=beta<=U3 and the following CLOSED interval is nonempty:

\[
\max\{0,(B-nU_1)/r,(C-nU_2)/r,W/4\}\le\eta\le
\min\{U_4,B/r,C/r,(a_2U_0+W)/4\}. \tag{2}
\]

To prove necessity, average ANY individual real flow under the finite
permutation group S_m, without swapping b,c. Each vertex's demand and each
edge's cap are preserved. The five orbit values alpha,zB,zC,beta,eta obey

\[
a_2\alpha+p(z_B+z_C+\beta)=d_{YY}+\tau,\quad
nz_B+r\eta=B,\quad nz_C+r\eta=C,\quad n\beta=d_T+\tau.
\]

The incidence counts follow directly from disjoint sets: a YY vertex has
a2 other YY neighbors and p neighbors of each light type; each B/C vertex
has n YY and r opposite-light neighbors; a T vertex has n YY neighbors.
There are no other edge types. Eliminating gives
zB=(B-r eta)/n, zC=(C-r eta)/n and a2 alpha=4eta-W, since 2p/n=4/r.
Every cap and sign inequality is now exactly one bound in (2), plus the
beta bounds. Conversely any eta in (2) constructs all edge values and
satisfies every original individual degree and capacity. For m>=4 use
alpha=(4eta-W)/a2. For m=3, a2=0 forces 4eta=W and alpha is unused;
set alpha=0 without imposing any inequality involving the absent c0 edge.
For m=2 each T vertex is isolated, so positive dT+tau is impossible.
The larger m>=3 domain is for THIS KK graph, not an extension of the
full10332 spectral carrier criterion to smaller k or m.

If dB=dC and c1=c2, one may additionally average b,c. The source's zeta
interval for m>=4 follows by zeta=(B-r eta)/n:

\[
\max\{0,[A-a_2(c_0-\tau)]/(2p),[B-r(c_4-\tau)]/n\}\le\zeta\le
\min\{c_1-\tau,A/(2p),B/n\}.
\]

Thus the original iff is confirmed, and (2) removes its equal-light
restrictions with a separately paid zero-edge boundary. All real and
unbounded-in-m quantifiers are proved by averaging/elimination above,
not inferred from rational samples or a count grid.

## Fresh q19 literal reconstruction and full necessary envelope

Use core a,b,c, disjoint pools X,Y of sizes9,10 and every set of size<=2,
plus abc, ab_z, ac_z for all z in X or Y, and bc_y only for y in Y.
The actual downset has N=303,s=61,h=242,241 nonstar proper members.
The 143 defining q17 entries are mathematical DATA copied from10278;
divide each source integer by31 and use 29u/32768 on the new disjoint
nonanchor pairs. Fixed diagonals are60, intersecting entries-1, and the
a-singleton anchor is completed by the centered-star row identity.
All302^2 comparison positions, all22 ground stars, every downward deletion,
all143 types, every original budget and every NN edge are reconstructed.
No q17 PSD/factor/floor premise is imported.

The negative-budget set has45 YY,10 B,10 C and10 T vertices. Fresh exact
values are dYY=362147/32768, dB=dC=10683/32768, dT=13379/16384;
c0=84533/32768,c1=c2=17921/16384,c3=19371/16384,c4=25083/32768.
D=16777855/32768, ell0=2089103/8192 and P0=8421443/65536.
There are23865 NN edges:1800 KK,10820 KG,11245 GG. The KK counts are
630,360,360,360,90 across the five orbits.

The complete q19 KK-flow floor region is exactly
0<=tau<=25083/32768. Literal feasible flows at both endpoints are included
in RECORD.json and checked on all75 degrees and1800 capacities. Convex
interpolation pays every real intermediate tau because degrees and caps
are affine. Beyond this endpoint the actual B/C cap is negative, excluding
any such nonnegative KK flow. This does NOT exclude general H competitors
with positive KK changes and greater cost.

Every individual KK/KG capacity in (1) is retained. Grouping gives21 exact
breakpoints and22 closed linear pieces, including the final unbounded
formal piece; RECORD.json lists them all. This computation extends the
source's selected penalties without claiming a feasible floor domain.
In particular all405 YY/X-singleton KG edges have c=3755/8192, giving
P>=P0+38tau+(405/2)(tau-3755/8192)_+. Thus the weak affine plane cannot
be saturated above that floor even while KK flows may still exist.
Neither this penalty nor the KK endpoint proves mathematical nonexistence
of H. The q19 PSD/star-release recipe and its much smaller attained floor
interval were not audited here.
