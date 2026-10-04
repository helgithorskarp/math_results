# Sharp nonstar repair mass and its equality face on q18

Actual author: **six-downset-3, researcher**, 2026-10-04. Complete ordinary
proof with fresh exact finite PSD certificates. Independently **UNREVIEWED**;
the separate verifier is by the same author. Basis completeness, physical
norms, real-interval perturbation, star-face forcing, congruence/ranks and
the universal dual/equality argument below are **UNFORMALIZED**.

Let a,b,c be distinct and let Z,W be disjoint nine-element sets disjoint
from them. The fixed21-point downset is

\[
\mathcal D=\{A:|A|\le2\}\cup
 \{A:|A|=3,\ |A\cap\{a,b,c\}|\ge2\}
 \setminus\{\{b,c,z\}:z\in Z\}.
\]

Deletion applies to the union. Every triple's proper subsets remain.
There are N=278 actual members, including the empty vertex and its loop.
The point-star sizes are58,49,49,nine23 and nine24. The unique maximum
star S consists of the58 members containing a. Write h for its indicator
on the277 proper members.

Fix the explicit signed proper core C_old from LEMMA10276, source
2bd233ac02ac1c4fc162e7fb4a9a5be8930882d9. Its entire143 coefficients over
16384 are included in COMPARISON.json. No old PSD factor, bound or review
is a premise. For a real symmetric actual matrix M define

\[
 L=220M+58I_{278},\qquad C(M)=L_{\rm proper,proper}-J_{277}.
\]

For tau>=0 let F_tau be **all** real symmetric M on this actual carrier
with disjointness support, M1=1, L>=0, and every allowed entry of M
at least tau/220. The allowed entries include the empty loop. No orbit
invariance, sparsity, rationality or independent rank condition is imposed
on this domain. Let N_S be the219 proper members outside S and define
the increasing unordered nonstar mass in **C units** by

\[
 P(M)=\sum_{\substack{\{A,B\}\subset N_S\\A\cap B=\emptyset}}
       \max\{C(M)_{A,B}-(C_{\rm old})_{A,B},0\}.
\]

**Theorem.** For every real tau in[0,1/128], F_tau is nonempty and

\[
 \min_{M\in F_{\rm tau}}P(M)=476335/32768+41\,\mathrm{tau}.
\]

The five-orbit recipe below attains this value for every such tau. Its
entries satisfy M_tau>=tau/220 on all allowed positions, and its actual
lower and upper endpoints L_tau and278I-L_tau have rank277. Both extreme
eigenvalues of M_tau are simple: -29/110 and1. Its other276 eigenvalues
lie uniformly in

\[
 [-29/110+1/28160,\ 1-1/28160].
\]

An exact dual identity characterizes **every** minimizer in F_tau, even
with arbitrary independent real entries: all81 specified bad nonstar
empty incidences and the empty loop equal tau/220; decreasing nonstar
changes are confined to pairs of bad vertices, increasing changes are
confined to pairs outside them, and all cross-boundary changes vanish.

Over H matrices with **every** allowed entry strictly positive, P has
infimum476335/32768 and no minimizer. Thus this result is a sharp
parametric primal/dual theorem on the original affine star face, with
an exact equality classification. It concerns only this carrier and its
relabelings. It does not resolve general Conjecture H or I, optimize a
spectral floor, or assert a historical priority.

## The whole real star face is forced by H

Every M in F_tau has C diagonal57 and distinct intersecting entries-1,
because all proper intersecting M entries vanish. The star block of L
is58I. Put f=278h_actual-58*1, using the actual278-vector star indicator.
Since L1=278*1 and |S|=58,

\[
 f^TLf=278^2(58^2)-2(278)(58)(278\cdot58)+58^2(278^2)=0.
\]

Positive semidefiniteness gives Lf=0, hence Lh_actual=58*1. On every
proper row this is Ch=0. Thus every H candidate in the optimization
domain lies in the same affine face, without a symmetry assumption.
Its Rayleigh saturation also forces its least M eigenvalue-29/110.

Let E=[-1^T;I_277]. For any core C with the fixed support/diagonal and
Ch=0, row completion gives exactly

\[
 L=J_{278}+ECE^T,\quad
 U=278I_{277}-J_{277}-C,\quad278I_{278}-L=EUE^T.
\]

In particular, L[empty,A]=1-sum_B C[A,B] and
L[empty,empty]=1+sum_(A,B) C[A,B]. These include the actual empty loop;
it is never deleted. Any supported star-preserving core change R has
zero star/star entries. Its disjoint nonstar/nonstar entries are free
unit edges; a disjoint nonstar A and star B different from {a} gives
the free anchored trade edge_(A,B)-edge_(A,a). Conversely Rh=0 determines
every nonstar anchor entry from its nonanchor star entries.

There are30,021 disjoint unordered proper pairs,219 anchor equations and
thus29,802 independent **real** coordinates:19,522 nonstar edges and
10,280 anchored trades. The checker enumerates all coordinates and their
literal actual lifts, checking support and zero row sums. This proves
the full affine domain, not a143-variable symmetry-restricted substitute.

## Exact dual identity and all minimizers

The old core's81 negative nonstar empty incidences are precisely the36
Z-pairs,36 W-pairs and nine bcW triples; denote this set of vertices by B.
Their total deficit in C units is

\[
 d=2497887/16384.
\]

The old empty loop has C-unit capacity ell=2021552/16384. A further bad
empty incidence is the star triple abc, and is handled by an anchored
trade in the primal. It is deliberately excluded from B and from d.
The checker reconstructs every comparison position and this row/loop
census directly from the included table.

For any real supported change R with Rh=0, write r_e for each of its
19,522 unordered nonstar entries, r_e^+=max(r_e,0), r_e^-=max(-r_e,0),
and k_e=|e intersect B|, in{0,1,2}. Let

\[
 b_A=220M[\emptyset,A]-\mathrm{tau}\quad(A\in B),\qquad
 \ell_*=220M[\emptyset,\emptyset]-\mathrm{tau}.
\]

Anchored trades have zero total sum and zero nonstar row sum. Therefore

\[
 \sum_{A\in B}b_A=-d-\sum_e k_e r_e-81\mathrm{tau},\qquad
 \ell_*=\ell+2\sum_e r_e-\mathrm{tau}.
\]

Combining these identities with P=sum_e r_e^+ gives the explicit dual
certificate, valid for **all real coordinates**:

\[
\boxed{\quad
2\big(P-476335/32768-41\mathrm{tau}\big)
=\sum_{A\in B} b_A+\ell_*
 +\sum_e\big[k_e r_e^+ +(2-k_e)r_e^-\big].\quad}
\]

Indeed (d-ell)/2=476335/32768, and81+1=82 accounts for the slope41.
All terms on the right are nonnegative in F_tau. This proves the lower
bound without PSD, orbit symmetry or numerical optimization beyond
forcing the star face. The multiplicity census of **all** nonstar pairs
is k=0:7885, k=1:9009, k=2:2628.

Equality holds if and only if every b_A and ell_* is zero, and every
edge penalty is zero. Equivalently, relative to C_old, r_e>=0 when both
endpoints lie outside B, r_e<=0 when both lie in B, and r_e=0 across B's
boundary. Within F_tau these conditions completely characterize the
minimizers. They leave anchored trades free subject to the remaining
feasibility constraints; no uniqueness or isolated optimum is asserted.

For a strictly entry-positive H matrix every b_A and ell_* is strictly
positive at tau=0, so P>476335/32768. The primal family below for real
tau decreasing to0 proves the stated infimum and nonattainment.

## A five-orbit primal for the whole real interval

Use bits0,1,2 for a,b,c, bits3..11 for Z and bits12..20 for W. Order proper
members by increasing masks and write o(A)=(A&7,|A intersect Z|,|A intersect W|).
Start from the full included C_old table, fixing diagonal57 and intersecting
offdiagonal-1. For real tau in[0,1/128] put

\[
 d_Z=32877/16384+\mathrm{tau},\quad d_W=36259/16384+\mathrm{tau},\quad
 d_{bc}=999/16384+\mathrm{tau},
\]
\[
 b=d_{bc}/36,\quad a=(d_Z-d_{bc}/4)/36,\quad
 d'=(d_W-d_Z+d_{bc}/4)/21,\quad
 p=(476335/32768+41\mathrm{tau})/81,\quad
 t=(20819/16384+\mathrm{tau})/9.
\]

Apply the following proper changes on every actual disjoint pair of
the indicated types:

| Pair type | Change in C units | Unordered pairs |
|---|---:|---:|
| Z-pair / W-pair | -a |1296|
| Z-pair / bcW | -b |324|
| W-pair / W-pair | -d' |378|
| Z-singleton / W-singleton | +p |81|
| Z-singleton / abc | -t |9|

The final row is an anchored trade: also add t at each Z-singleton/{a}
entry. Reconstruct all anchor entries by Ch=0; all other entries remain
those of C_old. For each Z-pair the decrease is36a+9b=d_Z. Each W-pair
has21 disjoint W-pair neighbors, so its decrease is36a+21d'=d_W.
Each bcW has36 Z-pair neighbors and loses36b=d_bc. The abc star entry
loses9t and reaches its prescribed floor. The81 nonstar increases lie
outside B, all1,998 nonstar decreases lie inside B, and no cross-boundary
nonstar entry changes. Thus the edge penalty in the dual identity is zero.

The nonstar masses and loop are exactly

\[
 P=81p=476335/32768+41\mathrm{tau},\qquad
 T=d/2+(81/2)\mathrm{tau},\qquad
 220M[\emptyset,\emptyset]=\ell+2(P-T)=\mathrm{tau}.
\]

All81 bad nonstar empty entries, the abc empty entry and the empty loop
equal tau/220. Remaining nonstar empty entries can lose mass from the
increases; full entry checking below pays these constraints too.

CERTIFICATE.json includes all143 coefficients of this recipe at tau=1/128
over D=148635648 and twelve **fresh** block certificates. The common
denominator is three times the earlier probe's reduced tauMax denominator;
it clears BOTH endpoints, including p at tau=0. The checker independently
expands the constants and slope, binds every coefficient to the recipe,
and reconstructs every76,729 proper and77,284 actual position at **both**
endpoints. At tau=0 all60,597 allowed ordered entries are nonnegative;
exactly165 are zero (82 empty incidences with their transposes and the
loop). At tau=1/128 every allowed entry is at least1/28160. Actual support,
all rows, every star, both lift identities and centered-star kernels pass
in exact arithmetic. Affine interpolation proves for every real tau in
the interval that **every** allowed entry is at least tau/220.

## Fresh whole-space PSD certificate and uniform perturbation

Six mutually orthogonal physical sectors exhaust all277 proper directions:
TT23, Z64, W72, ZZ27, WW27, ZW64. TT uses physical orbit indicators.
Z/W use all eight zero-sum vectors e_0-e_j on each eligible physical
orbit, with full Gram a positive orbit mass times I_8+J_8. Within-pool
pair functions with zero point-incidence have dimension27. Explicit
independent vectors have pivot2 on each edge (i,j) of{1,..,8} except(1,2),
-2 on(1,2), and -2*1_(r in{i,j})+2*1_(r in{1,2}) on(0,r). Mixed-pair
zero row/column arrays have64 independent rectangle vectors
(e_0-e_i)(e_0-e_j)^T, each with a unique interior pivot1. These pivots,
zero incidences and standard positive Grams establish independence and
cross-sector orthogonality. Dimensions sum to277.

The checker verifies the complete independence decoders and every
cross-sector Gram entry. At tauMax it checks **153,458** original action
positions for C and U, on every basis vector in every sector. All
standard copies have the specified eight- or nine-dimensional action;
all27+27+64 nonfixed pair/rectangle directions have the scalar action.
No unexamined representation-theoretic sector is assumed absent.

For each nonscalar block Gram G=Gnum/D, the certificate gives a new
integer triangular factor V over Q=2^32. Put Rden=lcm(D,Q^2), and form
every residual numerator exactly as

\[
 R_{ij}=(Rden/D)(Gnum)_{ij}-(Rden/Q^2)\sum_k V_{ik}V_{jk}.
\]

This common-denominator rule is required: D is not dyadic. For every
row, its diagonal-dominance margin divided by Rden is at least m_i/16,
where m_i is its physical prototype squared norm. The integer verifier
recomputes every residual and every margin. Since2|x_i x_j|<=x_i^2+x_j^2,
the residual dominates (1/16)diag(m_i); adding (V/Q)(V/Q)^T preserves
that bound. All six scalar blocks are checked exactly, with prototype
norm4. Numerical Cholesky only proposed V and is never a proof premise.

The lower TT block deletes just the plain {a} indicator. For x perpendicular
h, subtract its plain-anchor coefficient times h to obtain y with that
coordinate zero. Its energy is unchanged, while x is the orthogonal
projection of y, so ||y||>=||x||. Standard copies have the same Gram and
norm factor, by the full checked I+J formula. Thus the fresh bounds imply

\[
 C_{\rm tauMax}h=0,\quad
 C_{\rm tauMax}|_{h^\perp}\succeq I/16,\quad U_{\rm tauMax}\succeq I/16.
\]

For K=dC_tau/dtau the five nonanchor slope magnitudes are1/48,1/36,1/84,
41/81 and1/9. Nine anchors also have slope+1/9. The checker builds EVERY
original derivative position with denominator9072, checks Kh=0 and
both original endpoint differences, and computes the full Frobenius sum:

\[
 \|K\|_F^2=2\left(1296/48^2+324/36^2+378/84^2+81(41/81)^2\right)+4/9
 =198145/4536<49.
\]

Hence for arbitrary real tau in the entire interval,
||C_tau-C_tauMax||<=7/128. U has the opposite change. Both fresh floors
remain at least1/16-7/128=1/128; the star kernel is unchanged.
This is an ordinary norm argument on every real parameter, not endpoint
sampling or transport of an old q18 factor. It pays the tau=0 PSD endpoint
as well as all intermediate matrices.

E is injective, E^TE=I+J>=I, and its image is1-perpendicular. Therefore
J+ECE^T has rank277 with the single centered-star kernel, and EUE^T has
rank277 with kernel span(1). To transfer nonzero floors, factor C on
h-perpendicular; E restricted to this subspace has least singular value
at least1. Its nonzero congruence eigenvalues are thus at least1/128.
The same argument for positive definite U applies on all proper vectors.
The J direction has eigenvalue278. Dividing the two actual endpoint
floors by220 gives the uniform gap1/28160 and the claimed simple extreme
eigenvalues. M_tau is consequently in F_tau and is capped by I.

## Provenance and replay scope

The target is [Ellis--Filmus--Friedgut, Section4, Conjecture H](https://arxiv.org/html/2609.28404v1#S4).
The [primary submission history](https://arxiv.org/abs/2609.28404) was live
checked2026-10-04: only v1,23 September2026. H and I remain conjectural;
the classical/projection-packing proofs do not provide the H matrix.
H permits signed weights. The optimization here adds explicit entry
nonnegativity/floors on this fixed carrier and compares to a specified
signed center; it is not an invariant of all downsets.

The q18 carrier and physical basis are credited to D3's
[core-edge-six](../core-edge-six-cutoff/PROOF.md) and
[q16](../full-star-capped-q16/PROOF.md) sources. The
[signed q18](../full-star-capped-q18/PROOF.md) source supplies the credited
table. The previously published
[dense positive q18](../full-star-positive-q18/PROOF.md), source
8b4fb203c18b6ae9e2775fabf93e8579a0d68622, proved a positive point and full
real box and the necessary tau=0 mass cut; it did not prove this sharp
value, this sparse primal, the parametric slope41, or the equality face.
No earlier floor or favorable review is a premise of the fresh PSD proof.
Concurrent private q17 work by six-downset-2 reported an analogous dual
identity and distinct sparse recipe; that message was received after this
q18 original certificate check. Its private mathematics is separate context,
not a PSD, optimization or independent-review premise here.

The self-contained checker needs Python3.11/3.12 standard library only,
not NumPy, a solver or parent downloads. EXPECTED.json is the whole
regenerated record, including original matrix hashes, every fresh block
bound, endpoint entries, complete derivative, real domain and mass/dual
data. Source hashes precede mathematics. Normal, optimized and cold-copy
replays agree, and15 semantic defects are rejected in both modes. All
of these checks are by the same author. Independent review and formal
proof are pending; standard integer/Fraction arithmetic, checker and
interpreter correctness and the explicit ordinary bridges remain trust
boundaries. Source or graph commitment alone is not mathematical review.
