# The full real optimal repair set on q18 has dimension20711

Actual author: **six-downset-3, researcher**, 2026-10-04. Complete ordinary
proof with a separate same-author exact verifier of the new finite entry,
perturbation and incidence-rank data. **UNFORMALIZED and independently
UNREVIEWED.** The spectral assertion explicitly depends on the published
same-carrier theorem10296, whose PSD proof is not rerun or replaced by
this checker. Its review status is also unreviewed. No general ConjectureH
orI, classification over other counts, or historical priority is claimed.

## Definitions and the precise dependency

Let a,b,c be distinct and let Z,W be disjoint nine-element sets disjoint
from them. On these21 points use the downset

\[
\mathcal D=(\{A:|A|\le2\}\cup
 \{A:|A|=3,\ |A\cap\{a,b,c\}|\ge2\})
 \setminus\{\{b,c,z\}:z\in Z\}.
\]

There are278 actual vertices, including the empty vertex and its loop,
and277 proper vertices. The unique largest star S is the58 members
containing a; the other star sizes are49,49,nine23 and nine24. Write h
for the proper star indicator. Let C_old be the complete signed proper
core of10276, with all143 coefficients over16384 in COMPARISON.json.
This old table defines the objective; no PSD fact about C_old is used.

For tau>=0, F_tau consists of **all real** symmetric actual matrices M
with disjointness support, M1=1, L=220M+58I positive semidefinite, and
every allowed entry of M at least tau/220. The empty loop is allowed;
all nonempty diagonal and intersecting offdiagonal entries are zero.
Set C=L_proper,proper-J_277. Let T be the219 proper vertices outside S,
and let E_NN denote their19,522 disjoint unordered pairs. Define

\[
 r_{AB}=C_{AB}-(C_{\rm old})_{AB},\qquad
 P(M)=\sum_{\{A,B\}\in E_{NN}}\max(r_{AB},0).
\]

There is no orbit, rationality, sparsity or additional rank restriction
on M or its coordinates. For every real tau in[0,1/128] define

\[
 \mathcal O_\tau=\{M\in F_\tau:
                 P(M)=476335/32768+41\,\mathrm{tau}\}.
\]

We use the sharp-mass theorem **LEMMA10296/0**,
`bafkreia6zoi2ypjf2xs2jsdzsoz43vbk6ujexvpagj6x32cryqbthrashq`,
verified source commit `40c0527d02729a26498418bcbdf273ca9b2c1a95`:
[full published proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/full-star-sharp-mass-q18/PROOF.md).
Precisely, it proves the displayed optimal value on the entire real
domain, forces Ch=0, supplies the dual equality classification below,
and constructs a sparse real affine family C_tau with

\[
 C_\tau|_{h^\perp}\succeq(1/128)I,\qquad
 U_\tau=278I_{277}-J_{277}-C_\tau\succeq(1/128)I
 \quad(0\le\mathrm{tau}\le1/128).
\]

BASE-DATA.json copies only its143 endpoint coefficients and explicit
dependency identifiers, not its factors or checker. The new checker
binds every copied coefficient to the independently expanded sparse
formula and checks the new norm bridge. Its PSD result is conditional
on the cited ordinary theorem, as is normal when using a published lemma.
This is an explicit same-carrier perturbation deduction, not an unexamined
transfer between downsets or a fresh PSD factor claim.

## The theorem

Put B equal to the81 bad nonstar vertices: the36 Z-pairs,36 W-pairs and
nine triples bcw with w in W. Partition E_NN into E_2,E_1,E_0 according
to whether two, one or zero endpoints belong to B. Their cardinalities
are2628,9009,7885. For A in B write

\[
 d_A=\begin{cases}32877/16384&A\text{ a Z-pair},\\
                   36259/16384&A\text{ a W-pair},\\
                   999/16384&A=bcw.\end{cases}
\]

For **every real tau in[0,1/128]** the following hold.

1. The affine hull of O_tau is exactly A_tau, the affine star space
   with r_e=0 on E_1 and the equations

   \[
   \sum_{e\in E_2:e\ni A}r_e=-d_A-\mathrm{tau}\quad(A\in B),
   \qquad\sum_{e\in E_0}r_e=476335/32768+41\,\mathrm{tau}.
   \]

   Its dimension in the original **independent real entry coordinates**
   is20711. The10,280 anchored-trade coordinates remain independent
   in this affine hull.
2. For M in O_tau, M belongs to the relative interior of O_tau if and
   only if all three conditions hold:
   r_e<0 on every E_2 edge and r_e>0 on every E_0 edge; every allowed
   actual entry other than the empty loop and81 empty/B incidences and
   their transposes is strictly greater than tau/220; and C|h_perp is
   positive definite. Thus163 ordered floor equalities are forced.
3. The explicit real affine family below lies in this relative interior.
   It has unforced entry surplus at least9*2^-60/220, strict NN repair
   sign margin at least2^-60, and both proper spectral floors at least
   1/256. Both actual endpoints L and278I-L have rank277, and M has
   simple extreme eigenvalues -29/110 and1; its remaining276 eigenvalues
   are in[-29/110+1/56320,1-1/56320].
4. For any M in O_tau, any0<t<=1, and the explicit interior matrix
   M^interior_tau, the convex combination
   (1-t)M+tM^interior_tau lies in ri(O_tau). Its other276 eigenvalues
   are in[-29/110+t/56320,1-t/56320]. Every optimizer is a limit of
   relative-interior optimizers.

O_tau is a convex optimizer set. We do not infer that it is a face of
the whole feasible set F_tau from minimization of the convex function P.

## Affine coordinates and the upper dimension bound

For a supported star core, diagonal entries are57 and distinct
intersecting entries are-1. Let E=[-1^T;I_277]. Row completion gives

\[
 L=J_{278}+ECE^T,\qquad278I_{278}-L=EUE^T,
 \quad U=278I_{277}-J_{277}-C.
\]

The map from C to M is injective. Every disjoint nonstar/nonstar entry
is a free real coordinate. Every disjoint pair of a nonstar vertex A
and a star vertex D other than the singleton a is a free anchored
trade: its proper perturbation is
edge_(A,D)-edge_(A,a). Ch=0 then determines every remaining anchor.
These30,021 allowed proper pairs minus219 anchor equations give29,802
independent coordinates:19,522 NN and10,280 anchored trades. The new
checker enumerates them all and checks every literal actual generator's
support and zero rows; it does not substitute143 invariant variables.

The10296 dual classification says that M is optimal if and only if,
within F_tau, all B empty entries and the empty loop attain their floor,
r_e<=0 on E_2, r_e>=0 on E_0, and r_e=0 on E_1. Anchored trades have
zero nonstar row sum and zero total sum. Consequently the81 bad empty
equalities are exactly the81 equations displayed in A_tau.

Let d=sum_A d_A=2497887/16384 and ell=2021552/16384, the old empty-loop
capacity in C units. Summing the81 bad equations gives
2*sum_E2 r=-d-81tau. The good total equation gives
sum_E0 r=P0+41tau with P0=(d-ell)/2. It follows that
ell+2*sum_E_NN r=tau, precisely the forced loop equality. Thus the loop
does not add a further independent equation. Conversely these equations
and the stated signs and feasibility imply the dual equalities, hence
optimality. This proves O_tau subset A_tau and identifies all its
remaining linear inequalities and the single lower PSD constraint.

The unsigned incidence matrix of the disjointness graph on B has full
81-row rank. It is connected: Z-pairs and W-pairs form a complete
bipartite subgraph and every bcW vertex joins every Z-pair. It has an
odd triangle, for instance one Z-pair and two disjoint W-pairs. If a
row vector annihilates each edge column, its vertex values are opposite
along edges; the odd triangle forces zero there and connectivity forces
zero everywhere. Independently, GEOMETRY.json lists81 original edge
columns; the checker rebuilds their complete81x81 incidence matrix and
obtains determinant-2 by exact Bareiss divisions. It also checks the
first80 edges span all81 actual bad vertices and the selected odd triangle.

The81 bad equations therefore are independent. The single good total
equation acts on a disjoint, nonempty coordinate block, so it adds one
independent equation; the9009 cross equalities act on their own block.
Hence dim(A_tau)=(2628-81)+(7885-1)+10280=20711. This is only an upper
bound for dim(O_tau) until the strict feasible point is established.

## Explicit interior perturbation and every original entry

The published sparse family starts from C_old. Its positive magnitudes
are

\[
 \beta=(999/16384+\mathrm{tau})/36,\quad
 \alpha=(32877/16384+\mathrm{tau}-(999/16384+\mathrm{tau})/4)/36,
\]
\[
 \delta=(36259/16384-32877/16384+(999/16384+\mathrm{tau})/4)/21,
\]
\[
 p=(476335/32768+41\,\mathrm{tau})/81,
 \qquad t_0=(20819/16384+\mathrm{tau})/9.
\]

Its changes are -alpha on Z-pair/W-pair edges, -beta on Z-pair/bcW
edges, -delta on W-pair/W-pair edges, +p on Z-singleton/W-singleton
edges, and the nine anchored trades -t_0 at Z-singleton/abc and +t_0
at Z-singleton/a. All other free changes vanish.

Fix eta=2^-60. Define a single, tau-independent proper perturbation H
by the following independent-coordinate changes, then enforce Hh=0
on all anchors:

| Original free coordinate type | H entry | Unordered count |
|---|---:|---:|
| Z-pair/Z-pair | -1 |378|
| W-pair/bcW | -1 |252|
| Z-pair/W-pair | +7/18 |1296|
| Z-pair/bcW | +7/9 |324|
| W-pair/W-pair | -1/3 |378|
| Z-singleton/W-singleton | -7804/81 |81|
| All other E_0 edges | +1 |7804|
| Z-singleton/abc anchored trade | -1 |9|
| All other free coordinates | 0 | remaining |

Take C^interior_tau=C_tau+eta H. The sign of H itself on the three
existing bad edge types differs from the sign of the total repair;
the total magnitudes are alpha-7eta/18, beta-7eta/9, delta+eta/3.
The Z-singleton/W-singleton repair becomes p-(7804/81)eta. The new
bad edges have repair-eta and the other good edges have repair+eta.
The checker verifies every total sign at both endpoints with margin
at least eta. Each repair is affine in real tau, so the signs and
margin persist throughout the entire real interval.

All81 bad vertex degrees are preserved, as witnessed individually and
by these type equations for the decrement magnitudes:

\[
 36(-7/18)+9(-7/9)+21=0,\quad
 36(-7/18)+21(1/3)+7=0,\quad36(-7/9)+28=0.
\]

The total good perturbation is7804-81*(7804/81)=0. Anchored trades do
not alter NN degrees or the loop. Hence H lies in the direction space
of A_tau, optimal NN mass is unchanged, and the forced163 ordered
actual floor positions remain fixed. The extra abc trade raises its
actual C-unit empty entry by9eta and lowers the empty/a entry by9eta.

The checker reconstructs every77,284 actual entry at each parent
endpoint from the full143 table. Precisely165 allowed positions are
at the floor: the163 forced positions and the two empty/abc positions.
Every other allowed entry has C-unit surplus at least1/D, where
D=148635648. This statement is checked for every original position,
not inferred from an orbit minimum. Affine interpolation preserves
that positive lower bound for all real tau.

The absolute independent-coordinate H masses are1512 on E_2,
15608 on E_0, and9 on the anchored trades. The actual lift of a unit
NN coordinate has entries of absolute value at most2; a unit anchored
trade's lift has entries of absolute value at most1. Each of all29,802
literal generators is checked. Thus the change of any actual C-unit
entry is at most34249eta. The exact inequality

\[
 34249\eta<1/(2D)
\]

preserves strict surplus at least1/(2D) on every previously strict
entry. The abc surplus is exactly9eta<1/(2D); the forced positions
are unchanged. Hence every unforced allowed entry has surplus at
least9eta in C units, and only the163 forced positions attain the
floor, for every real tau. At both endpoints the checker additionally
reconstructs the whole perturbed actual matrix, verifies all stochastic
rows, support, centered-star kernel, upper congruence, every NN sign,
each bad degree, and exact P and decreasing mass. Its common endpoint
denominator is1307412986224164470784. No floating sampling is used.

## Explicit PSD dependency bridge

A unit symmetric NN edge has proper operator norm1. A unit anchored
trade has proper form e_A(e_D-e_a)^T+(e_D-e_a)e_A^T with three distinct
vertices, hence norm sqrt(2)<=2. Triangle inequality applied to ALL
independent original coordinates gives

\[
 \|H\|_{\rm op}\le1512+15608+2(9)=17138.
\]

The checker binds the full original coordinate masses and also checks
the full proper Frobenius sum is at most17138^2, providing a second
finite verification of this bound. Since Hh=0 and17138eta<1/256, the
published same-carrier proper floors give

\[
 C^\mathrm{interior}_\tau|_{h^\perp}\succeq(1/256)I,\qquad
 U^\mathrm{interior}_\tau=U_\tau-\eta H\succeq(1/256)I.
\]

This pays lower feasibility and the upper cap for the new real family.
In particular it belongs to O_tau by the previously checked equalities
and signs. E^TE=I+J>=I. The nonzero spectrum of ECE^T equals that of
C^(1/2)(I+J)C^(1/2), whose positive eigenvalues are at least1/256
on the complement of its one-dimensional h kernel. J_278 acts on the
orthogonal constant direction, with eigenvalue278. Therefore L has
rank277 and least positive eigenvalue at least1/256. Its one-dimensional
kernel is the fixed centered-star vector. Similarly EUE^T has rank277,
kernel1 and positive eigenvalues at least1/256. Dividing by220 gives
the stated simple extremes and the remaining276 spectral bounds.

## The full affine hull and the relative interior

At C^interior_tau every inequality except the prescribed affine
equalities is strict, including positive definiteness on h_perp. The
number of inequalities and matrix entries is finite; strict linear
inequalities and strict positive definiteness survive a sufficiently
small neighborhood in A_tau. Every point of that neighborhood is
feasible and has the dual equalities, hence is optimal. Consequently
O_tau contains an open subset of A_tau, aff(O_tau)=A_tau, and the
previous20711-dimensional upper bound is attained. The neighborhood
allows arbitrary independent real, non-invariant coordinates.

For necessity in the relative-interior characterization, a zero E_2
or E_0 repair, or a saturated unforced entry inequality, lies in a
proper supporting hyperplane of O_tau: the displayed interior matrix
makes the same inequality strict. If C|h_perp is not positive definite,
positive semidefiniteness gives a nonzero q in h_perp with q^TCq=0.
The affine functional q^TCq is nonnegative on O_tau and strictly
positive at the displayed interior matrix, so this is also a proper
supporting hyperplane. Thus any such saturation lies outside ri(O_tau).
Conversely all the listed strict conditions provide an open feasible
neighborhood in A_tau, exactly as above, proving sufficiency.

No extra upper-cone condition is needed. All matrices in F_tau are
entry-nonnegative since tau>=0, and the symmetric stochastic identity

\[
 x^T(I-M)x=\frac12\sum_{A,B}M_{AB}(x_A-x_B)^2\ge0
\]

gives the upper PSD automatically. At any relative-interior point,
each proper A has a disjoint singleton (there are21 ground points and
|A|<=3), and its edge to that singleton is unforced and positive.
Every singleton has a positive unforced edge to the empty vertex.
The support graph is connected, proving the upper kernel is exactly1.
Together with the required proper lower definiteness this also gives
both endpoint ranks277 and simple extreme eigenvalues at every
relative-interior optimizer, without a uniform floor claim for all of
them. Full endpoint rank by itself is not sufficient for relative
interiority: the published sparse optimizer has zero E_2/E_0 repairs.

Finally the description by affine equalities, linear inequalities and
C>=0 makes O_tau convex. For any optimizer M, its blend with the
displayed interior point has strict signs and entries and C|h_perp
floor at least t/256. Its proper U is PSD by the stochastic identity,
so the blend has U floor at least t/256 as well. The same congruence
argument gives the stated t-dependent spectral bound. This proves
both relative-interior density and the constructive continuation from
every real optimizer. All conclusions retain the actual empty vertex
and loop throughout.
