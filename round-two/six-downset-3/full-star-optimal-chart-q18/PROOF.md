# A complete canonical real chart and an optimal cube on q18

Actual author: **six-downset-3, researcher**, 2026-10-04. Ordinary proof
with a separate same-author exact finite verifier. **UNFORMALIZED and
independently UNREVIEWED.** The explicit center, sharp value and its
spectral floors are published mathematical dependencies. Their original
programs and PSD factors are not imported or rerun. This theorem concerns
one fixed carrier and one fixed signed comparison matrix, not general
Conjecture H, other counts, or historical priority.

## Original domain and exact published dependency

Let a,b,c,Z,W be disjoint, with |Z|=|W|=9. On these21 points put

\[
\mathcal D=(\{A:|A|\le2\}\cup
\{A:|A|=3,\ |A\cap\{a,b,c\}|\ge2\})
\setminus\{bc z:z\in Z\}.
\]

There are278 actual vertices, including the empty vertex and its loop.
The277 proper vertices are indexed by ascending masks, where the bits
for a,b,c,Z,W are respectively0,1,2,3..11,12..20. The largest star S
has58 members and consists of the vertices containing a; h is its proper
indicator. The complement T has219 members. B is the81 bad nonstar
vertices:36 Z-pairs,36 W-pairs and9 bcW triples. Its complement in T
is G. Let E2,E1,E0 be the disjoint unordered NN pairs with two, one,
zero endpoints in B. Their sizes are2628,9009,7885. Free NS coordinates
are disjoint pairs (A,D) with A in T, D in S, D!=a; there are10280.
Every anchor (A,a) is present.

For real tau>=0, F_tau consists of ALL real symmetric actual matrices
M with disjointness support, M1=1, L=220M+58I positive semidefinite,
and every allowed actual entry at least tau/220. There is no symmetry,
rationality, sparsity or added rank restriction. Put C=L_proper-J277.
The fixed signed comparison C_old is the complete143-coefficient proper
core of10276, as reproduced in the parent's COMPARISON.json. Define

\[
r_e=C_e-(C_{\rm old})_e,\qquad
P(M)=\sum_{e\in E_2\cup E_1\cup E_0}\max(r_e,0),\qquad
P_0=476335/32768.
\]

We use the complete ordinary q18 optimizer-geometry theorem **10308/0**,
graph `bafkreifiauc33i6a3pumyecwlfcprotceve2xb6c47iavaqyvhcpexv3qy`,
source `88c6c7ea0905fe51d4ecab5703a3e9cd18d3344c`:
[published proof](https://github.com/helgithorskarp/math_results/blob/88c6c7ea0905fe51d4ecab5703a3e9cd18d3344c/round-two/six-downset-3/full-star-optimal-geometry-q18/PROOF.md).
Its original143 comparison entries, sparse center formula, perturbation
formula and ordinary spectral dependency are part of that cited theorem.
No review verdict on a different dense matrix is used here.

For EVERY real tau in[0,1/128], that theorem establishes the minimum
P0+41tau on F_tau, with optimizer set O_tau and affine hull A_tau given
by the star space Ch=0 together with

\[
r_e=0\ (e\in E_1),\quad
\sum_{e\in E_2:e\ni A}r_e=-d_A-\tau\ (A\in B),\quad
\sum_{e\in E_0}r_e=P_0+41\tau.
\]

Here d_Zpair=32877/16384, d_Wpair=36259/16384 and d_bcW=999/16384.
It constructs the specific center Cint_tau=Ctau+eta H with eta=2^-60,
specified entry by entry in its proof and GEOMETRY.json. In particular
this SAME center, for the full REAL interval, satisfies:

* every E2 repair is at most -eta and every E0 repair at least eta;
* the actual empty loop and81 empty/B incidences,163 ordered positions,
  attain the floor; all other allowed actual entries have surplus at
  least9eta in C units, i.e.9eta/220 in M units;
* Cint_tau|h_perp and Uint_tau=278I-J-Cint_tau both have floor1/256.

Those statements are explicit external ordinary mathematical premises.
The new checker verifies the new chart, every new literal sparse lift,
every inverse product and every rational perturbation inequality. It
does not recertify the parent center or pretend to supply fresh PSD
factors. The unformalized completeness and real-cube bridges follow.

## The theorem and chart

For every real tau in[0,1/128], the map below is an explicit affine
bijection from R^20711 onto A_tau. Its inverse reads the selected
nonpivot/nongauge/nonanchor ORIGINAL entries. It therefore provides
complete coordinates for every real optimizer, including asymmetric
ones. The coordinate cube

\[
|x_j|\le\rho=2^{-74}\quad(j=1,\ldots,20711)
\]

around Cint_tau lies entirely in ri(O_tau), uniformly over the whole
real tau interval. On the ENTIRE CLOSED cube the NN sign margins are
at least eta/2, all unforced allowed M entries have surplus at least
8eta/220, the163 forced positions stay fixed, and the proper lower
and upper floors are at least1/512. Both actual endpoints have rank277,
the extreme eigenvalues of M are simple and equal to -29/110 and1,
and its other276 eigenvalues belong to

\[
[-29/110+1/112640,\ 1-1/112640].
\]

For two distinct proper vertices u,v, let F_uv be the symmetric proper
unit-edge matrix. All unordered edges are ordered lexicographically
by their ascending masks. Let p1,...,p81 be the81 pivot edges in
CHART.json. They are the same selected original edges used for the
parent incidence-rank witness: the BFS spanning tree rooted at mask24
with ascending neighbor scans, followed by chord (12288,49152).
The first80 edges span all81 bad vertices; this chord closes the odd
triangle (24,12288,49152). Let A be their unsigned incidence matrix,
whose rows use ascending B masks, and let Q=2A^-1.

The new certificate provides ALL81 rows of Q as textual integers.
The fresh checker reconstructs all original incidence entries and
checks BOTH A Q=2I and Q A=2I, all13122 product entries. It also checks
every Q entry belongs to{0,+/-1,+/-2}; there are6226 zero,145 minus1,
14 minus2,98 plus1 and78 plus2 entries. No bound is inferred merely
from the parent's determinant2. Thus the original selected incidence
matrix is invertible over the rationals, and indeed over the reals.

For each of the2547 E2 edges e={u,v} not among the pivots, let b_e
be its original incidence vector and put

\[
K_e=F_e-\sum_{j=1}^{81}(A^{-1}b_e)_j F_{p_j}.
\]

For each of the7884 E0 edges e other than the lexicographically first
gauge g=(2,4), put K_e=F_e-F_g. Finally, for EVERY one of the10280
free NS coordinates e=(A,D), put K_e=F_AD-F_Aa. These20711 matrices
are indexed in that order: ascending nonpivot E2, ascending nongauge
E0, ascending free NS. There are no E1 coordinates. Define

\[
\Phi_\tau(x)=C^{\rm int}_\tau+\sum_e x_eK_e,
\qquad
M_\tau(x)=\frac{J_{278}+E\Phi_\tau(x)E^T-58I_{278}}{220},
\quad E=[-\boldsymbol1^T;I_{277}].
\]

Each x_e is a completely independent REAL variable in C units, not an
orbit coefficient, lifted M entry, inverse numerator or generator
coefficient divided again by2. The checker represents K numerators
over2 solely to avoid fractional arithmetic in the finite verification.

## Every original generator and completeness

For a nonpivot bad edge, its bad degree vector is b_e-A A^-1 b_e=0.
Thus it fixes every original bad empty incidence. Its proper row sums
are all zero, so its actual lift has no empty-row terms. For a good
generator the total unordered good edge sum is0. For an anchored
trade the nonstar star sum is0 and every proper star-kernel row is0.
Its two nonstar-row terms cancel and its star rows have opposite sums.
All three kinds have proper total sum0, so the actual empty loop is
fixed. None changes a cross NN entry or any diagonal/intersecting entry.

These facts are verified for EACH individual generator, not just its
type or quotient. Sparse checking is exact: from proper edges H_uv,
the only possible extra lifted entries are

\[
(EHE^T)_{0,u}=-\sum_vH_{uv},\qquad
(EHE^T)_{0,0}=\sum_{u,v}H_{uv}.
\]

Every omitted entry is exactly zero by this formula. The checker visits
all nonzero proper and actual positions, verifies their literal support,
the whole star kernel, all bad degrees, good mass, forced floors and
every nonzero stochastic row sum. Zero rows are checked through the
complete support formula, not assumed from a quotient. Its complete
coverage is49830 proper and101458 actual unordered sparse positions.
It accumulates the entire entrywise envelopes on21012 proper and21208
actual unordered positions; entries outside those envelopes are exactly0.
Whole column and both complete envelope hashes appear in EXPECTED.json.
No20711 dense matrices or large column corpus are stored.

Projection onto the20711 selected ORIGINAL free entries sends every
K_e to the corresponding unit coordinate: the compensating edges
are pivots, the one good gauge, or singleton-a anchors, none selected.
The checker verifies this for every literal column. This proves linear
independence over the reals and gives the promised coordinate inverse
x_e=(C-Cint_tau)_e.

For surjectivity, subtract from any element of A_tau its extracted
chart coordinates. All nonpivot bad entries vanish. The remaining
pivot vector w has A w=0 and hence w=0. All nongauge good entries
vanish; the total-good equation then makes its gauge entry0. All free
NS entries vanish; Ch=0 then makes each remaining singleton-a anchor0.
Every cross NN coordinate, diagonal and intersecting entry was fixed
already. The remainder is therefore identically zero at EVERY original
proper entry, and the injective actual completion is zero as well.
This proves the complete affine bijection, not only a dimension count.

In these coordinates the FULL optimizer domain is precisely the x
satisfying the original linear floor inequalities, the E2 negative/E0
positive repair inequalities, and Phi_tau(x)|h_perp positive semidefinite.
Cross coordinates and bad/loop equalities are automatic. This follows
from the parent's full equality characterization, or directly from
the exact mass equations and its universal sharp lower bound. Thus
the entire optimizer domain is a spectrahedron in these coordinates;
it is not asserted to be all of R^20711 or a face of F_tau.

## Exact all-real cube bounds

Write R(x)=sum x_eK_e. The checker obtains the following fresh whole
entry and column sums, with the numerators' common factor2 removed:

\[
\max_{f\in E_2\cup E_1\cup E_0}\sum_e|(K_e)_f|=7884,
\quad
\max_{i,j}\sum_e|(EK_eE^T)_{ij}|=10280.
\]

The first maximum is attained at good gauge (2,4); the second at
actual empty/a incidence (0,1) and its transpose. Both are sums of
ALL20711 literal columns at each original position, not sums of orbit
maxima or a proper-space norm substituted for an actual-entry bound.
Every bad column has at most8 proper edge terms and proper absolute
edge sum at most8; the total bad sum is13522. Good and anchored columns
each have two unit edge terms, giving totals15768 and20560. Hence

\[
\sum_e\sum_{u<v}|(K_e)_{uv}|=49850.
\]

A symmetric proper unit edge has operator norm1. The triangle inequality
therefore bounds ||R(x)|| by49850rho on the entire independent coordinate
cube. This is a PROPER277-space norm; it is never claimed to bound the
Frobenius norm of the full278-space actual lift. Actual entries have
their separately checked10280rho bound.

The exact integer/rational gates, checked afresh, are

\[
7884\rho<\eta/2,
\qquad10280\rho<\eta,
\qquad49850\rho<1/512.
\]

All these follow from rho=eta/16384=2^-74. No floating samples or vertex
sampling of the20711-dimensional cube is used. For arbitrary independent
real |x_e|<=rho, each original NN repair changes by at most7884rho,
each actual C-unit entry by at most10280rho, and the proper operator
by at most49850rho. The parent uniform eta/9eta/1/256 margins therefore
give the theorem's eta/2,8eta,1/512 margins, for EVERY real tau throughout
its closed interval. The exact mass equations and strict signs give
P=P0+41tau. Strict inequalities and proper lower definiteness give
relative interior by the parent's iff criterion. In particular even
the chart cube's boundary lies in the relative interior of O_tau.

The corresponding proper U changes by -R, so the SAME bound pays its
floor1/512. E^TE=I+J>=I; the nonzero eigenvalues of ECE^T are those
of C^(1/2)(I+J)C^(1/2) on the range of C and hence at least1/512.
The actual J acts on the orthogonal constant direction. As Ch=0 and
C is strictly positive on h_perp, L has its fixed one-dimensional
centered-star kernel and rank277. The strictly positive proper U
gives rank277 for EUE^T=278I-L with kernel1. Dividing the common
positive floor by220 proves the simple extremes and the stated other276
eigenvalue gap1/112640. This is a new exact perturbation bridge from
the explicitly cited parent floors, not a fresh factorization claim.

## Evidence boundary

The producer performs exact rational Gauss-Jordan elimination and may
be untrusted. The checker never imports it; it uses full integer product
identities, original sparse position equations, a coordinate left inverse
and complete entry envelopes. Finite replay validates these exact gates.
The argument that they prove a real affine bijection, a real uniform
cube and the actual spectral statements is the ordinary proof above,
which remains unformalized. Same-author checks and a shared signing
identity do not constitute independent review. Parent theorem10308 and
its parent10296 remain ordinary dependencies with their own scopes and
review status; a future parent review does not automatically review this
new chart. No infeasibility or maximal possible repair radius is claimed.
