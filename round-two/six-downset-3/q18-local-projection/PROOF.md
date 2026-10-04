# Explicit global and local retractions to all feasible q18 optimizers

Actual author **six-downset-3 / researcher**, 2026-10-04. This is a new
ordinary argument with a separate exact finite checker by the same author.
It is **UNFORMALIZED and independently UNREVIEWED**. The sharp dual identity,
optimizer equations and stronger interior center are explicit published
mathematical premises. Their executables, matrix data and PSD factors are
not imported or rerun here. The finite checker pays the new residual map
and bounds; the all-real, norm and feasibility bridges below are ordinary
proofs. Source or graph commitment does not constitute mathematical review.

## Fixed carrier, objective and published premises

Let a,b,c,Z,W be disjoint, with |Z|=|W|=9, and put

\[
 \mathcal D=(\{A:|A|\le2\}\cup
 \{A:|A|=3,\ |A\cap\{a,b,c\}|\ge2\})
 \setminus\{bcz:z\in Z\}.
\]

There are N=278 actual vertices, including empty and its loop. The
277 proper vertices use ascending masks, with a,b,c in bits0,1,2, Z in
bits3..11 and W in bits12..20. The unique maximum star S comprises the
58 proper members containing a. Its proper indicator is h. The nonstar
set T has219 members. Let B comprise the36 ZZ pairs,36 WW pairs and nine
bcW triples. Put G=T\B. The disjoint unordered NN pairs E2,E1,E0 have,
respectively, two, one, zero bad endpoints; their counts are2628,9009,7885.

For tau>=0, F_tau consists of ALL real symmetric actual matrices M,
supported on disjointness, with M1=1, L=220M+58I PSD and every allowed
ordered M entry at least tau/220. In particular the empty loop is allowed.
No orbit invariance, rationality, sparsity or added rank condition is
imposed on competitors. Write C=L_proper-J277. Fix the exact old comparison
C_old from10276: the complete143-entry table over16384 specified in the
sharp-mass and geometry premises. For NN edges e put r_e=C_e-(C_old)_e,

\[
 P=\sum_{e\in E2\cup E1\cup E0}r_e^+,\qquad
 P_0=476335/32768,\qquad \Delta=P-P_0-41\tau.
\]

The [sharp-mass theorem10296](https://github.com/helgithorskarp/math_results/blob/40c0527d02729a26498418bcbdf273ca9b2c1a95/round-two/six-downset-3/full-star-sharp-mass-q18/PROOF.md)
and its [complete independent audit10312](https://github.com/helgithorskarp/math_results/blob/bfa286572e2ef4cf6b301fb926eab339eed7a715/round-two/six-reviewer-5/sharp-q18-mass-audit/PROOF.md)
supply the following same-carrier identity for every real M in F_tau:

\[
 2\Delta=\sum_{A\in B}\sigma_A+t+
 \sum_{e\in E2\cup E1\cup E0}
       \{k_er_e^+ +(2-k_e)r_e^-\},\tag{1}
\]

where k_e is the number of bad endpoints,
sigma_A=220M_empty,A-tau and t=220M_empty,empty-tau. Thus

\[
 \sigma_A,t\ge0,\quad \Delta\ge0,\qquad
 \sum_B\sigma_A+t+\sum_{E1}|r_e|\le2\Delta.\tag{2}
\]

Every feasible M has Ch=0, and stochastic completion is uniquely

\[
 L=J278+ECE^T,\quad E=[-1^T;I277],\quad
 U=278I277-J277-C,\quad278I278-L=EUE^T.\tag{3}
\]

These equations can also be obtained directly by tight-star saturation:
for f=278*1_S-58*1 one has f^T L f=0, so PSD forces Lf=0.
The proper star block is58I, giving Ch=0. Proper diagonal entries of C
are57 and intersecting offdiagonal entries are-1. For a nonstar row,
changes of its proper NS entries sum to zero because Ch=0. Consequently
such changes contribute neither to its full row sum nor to the total
sum in(3). All proper star/star entries are fixed.

The [geometry theorem10308](https://github.com/helgithorskarp/math_results/blob/88c6c7ea0905fe51d4ecab5703a3e9cd18d3344c/round-two/six-downset-3/full-star-optimal-geometry-q18/PROOF.md)
and the [complete geometry audit and strengthened center10324](https://github.com/helgithorskarp/math_results/blob/df5a588c88f57babcb489c8690399fa5be50a0f7/round-two/six-reviewer-5/q18-optimal-geometry-audit/PROOF.md)
establish the following for EVERY real tau in[0,1/64]. Define
O_tau={M in F_tau:P=P0+41tau}. Its affine hull A_tau is the full original
star space with

\[
 r|_{E1}=0,\qquad
 \sum_{e\in E2:A\in e}r_e=-d_A-\tau\ (A\in B),\qquad
 \sum_{E0}r_e=P_0+41\tau,\tag{4}
\]

where d_ZZ=32877/16384, d_WW=36259/16384, d_bcW=999/16384.
An element of A_tau belongs to ri(O_tau) exactly when its E2 repairs
are negative, E0 repairs positive, every unforced original allowed entry
is strictly above its floor, and C is positive definite on h-perp.

Use specifically the published10324 center
C*_tau=C_tau+eta H, eta=2^-20, with its complete sparse recipe and H
as defined in that cited proof. For all real tau in[0,1/64], its E2/E0
repair margins are at least eta. Exactly163 allowed ordered positions
are forced floors: the81 empty/bad incidences and their transposes,
and the empty loop. Every other allowed actual entry has surplus at
least9eta/220. Both C* restricted to h-perp and U*=278I-J-C* have floor
39/4096. These are existing ordinary results, independently checked by
10324; this new proof does not duplicate their endpoint construction.

Finally use the original pivot incidence from the
[canonical chart10326](https://github.com/helgithorskarp/math_results/blob/54ef84d14c0fb6133cbfb8ce6840bfe722226d61/round-two/six-downset-3/full-star-optimal-chart-q18/PROOF.md).
Starting at the smallest bad mask24, breadth-first search of the literal
bad disjointness graph in ascending-neighbor order supplies80 tree edges.
Append the chord(12288,49152). A has rows the81 ascending bad vertices
and columns these81 original pivot edges, with entries1 at either endpoint.
Let Q=2A^-1. CERTIFICATE.json exposes all81 integer rows of Q and every
original label. The new checker freshly verifies BOTH entire products
AQ=QA=2I, then every new residual column and actual completion. Reusing
this attributed finite datum asserts no new inverse or chart discovery.

## Precise theorem

For every real tau in[0,1/64], the affine map Pi_tau defined below is a
retraction from the full real original star space onto A_tau. It preserves
all proper NS entries, all nonpivot E2 entries and all E0 entries other
than the gauge g=(2,4). For every M in F_tau its proper correction D and
actual correction obey

\[
 \|D\|_{op}\le10\Delta,\qquad
 \|EDE^T\|_{\max}\le2\Delta,\tag{5}
\]

where ||.||_max is the maximum absolute ORIGINAL entry, including the
empty row and loop. Pi_tau(M) need not be feasible far from the specified
center. A second, GLOBAL map repairs this remaining issue. Set

\[
 \theta=\frac{3\Delta}{\eta+3\Delta},\qquad
 \Phi_\tau(M)=(1-\theta)\operatorname{Pi}_\tau(M)+\theta M^*_\tau,
 \qquad\eta=2^{-20}.\tag{5a}
\]

For EVERY real M in F_tau, without a neighborhood hypothesis, Phi_tau(M)
is a feasible optimizer. Phi_tau is a continuous retraction of F_tau
onto the WHOLE O_tau. It fixes every optimizer, and maps every input
with Delta>0 into ri(O_tau). Its actual distances obey

\[
 \begin{split}
  \|M-\Phi_\tau(M)\|_{\max}
  &\le\frac{\Delta(3+\eta/110)}{\eta+3\Delta}
   \le\frac{346030081}{110}\Delta,\\
  \|M-\Phi_\tau(M)\|_{op}
  &\le\frac{139}{110}\frac{\Delta(3+10\eta)}{\eta+3\Delta}
   \le\frac{218628791}{55}\Delta.\tag{5b}
 \end{split}
\]

Both inequalities therefore also bound distance to the FULL FEASIBLE
optimizer set. The global constants are large; the separate local
result gives much smaller constants and preserves all proper NS entries.

The new LOCAL assertion is: for ANY real feasible M satisfying

\[
 \delta=\|C(M)-C^*_\tau\|_{op}\le2^{-32},\tag{6}
\]

one has Pi_tau(M) in ri(O_tau). Its NN sign margins are at least eta/4,
all unforced allowed original M entries have surplus at least8eta/220,
and both proper lower and upper floors are at least1/128. Its actual
endpoints have rank277; its extreme eigenvalues are simple -29/110 and1,
and the other276 have gaps at least1/28160 from either extreme.
In particular the FULL FEASIBLE optimizer set, allowing every real
original coordinate, satisfies

\[
 \begin{split}
  \operatorname{dist}_{\max}(M,O_\tau)
     &\le\|M-\operatorname{Pi}_\tau(M)\|_{\max}\le\Delta/110,\\
  \operatorname{dist}_{op}(M,O_\tau)
     &\le\|M-\operatorname{Pi}_\tau(M)\|_{op}\le139\Delta/11.
 \end{split}\tag{7}
\]

This supplies an explicit feasible optimizer rather than merely removing
wrong signs. Pi_tau fixes every optimizer and is idempotent on its entire
affine target. The blended global map changes proper NS entries towards
the center; Pi_tau itself preserves them. No optimal constants or maximal
ball are claimed. Feasibility is a hypothesis in BOTH distance results;
only the sharper local assertion also requires(6).

## Deriving the correction from original slacks

Let z_e=r_e on E1 and z_B(A)=sum_{e in E1:A in e}z_e, with SIGNED z_e.
Keep every entry except the mixed edges, the81 pivot edges and the good
gauge g. Add the following proper matrix D, with zero diagonal:

\[
 D_e=-z_e\quad(e\in E1),\qquad
 D_{p_j}=w_j,\quad w=A^{-1}(\sigma+z_B),\qquad
 D_g=v=\tfrac12(\sum_{E1}z_e-\sum_B\sigma_A-t).\tag{8}
\]

Put C_hat=C+D and
Pi_tau(M)=(J278+E C_hat E^T-58I278)/220. Equation(8) is affine in the
original matrix entries for fixed tau. It changes no proper NS entries;
thus Dh=0 and all star equations, fixed support and diagonal remain.

The actual bad-empty identity and the vanishing nonstar sum of NS changes
give, separately for every bad A,

\[
 \sum_{e\in E2:A\in e}r_e
       =-d_A-\tau-\sigma_A-z_B(A).\tag{9}
\]

Adding w supplies sigma+z_B at those same81 original rows. Deleting z
also removes precisely z_B, so the new rows give(4). Each incidence
column sums to2, hence

\[
 \sum_jw_j=\tfrac12(\sum_B\sigma_A+\sum_{E1}z_e).\tag{10}
\]

The completion's loop change is twice the total unordered proper change.
Mixed and pivot changes together therefore change it by
-2sum z+2sum w=sum sigma-sum z. The original excess loop is t; the gauge
adds2v=sum z-sum sigma-t and cancels this excess exactly. The factor1/2
in(8) and the signed z_B are necessary. They are checked on every unit
residual below, not inferred from an orbit average.

The old loop capacity is ell=2021552/16384. Its new floor and the new
bad equations, whose sum gives2sum_E2 r=-d-81tau with
d=2497887/16384, imply

\[
 \tau=\ell+2\sum_{NN}\widehat r
   =\ell-d-81\tau+2\sum_{E0}\widehat r.
\]

Since (d-ell)/2=P0, the E0 total is P0+41tau. Thus(4) holds fully.
Conversely at any point of A_tau, sigma=t=z=0, giving D=0. Pi_tau is
therefore a retraction onto the WHOLE affine space, not just an image
subspace or an invariant sector. Its unchanged selected entries are
exactly the20711 canonical coordinates; all10280 free anchored entries
are included. This algebraic fact is independent of positivity/PSD.

## Complete residual columns and two different norm bounds

For an unordered supported proper pair e, let F_e have1 at its two
symmetric positions and0 elsewhere. Then ||F_e||op=1. The9091 residual
columns of D are exactly the following, where A is a bad vertex,
j(A) its row index, and (A,V) a mixed edge with V good:

\[
 \begin{array}{ll}
 \sigma_A:&\frac12\sum_j Q_{j,j(A)}F_{p_j}-\frac12 F_g,\\
 z_{AV}:&-F_{AV}+\frac12\sum_j Q_{j,j(A)}F_{p_j}+\frac12F_g,\\
 t:&-\frac12F_g.
 \end{array}\tag{11}
\]

The exact maximum column l1 norm of A^-1 is7/2. This fresh finite bound
is verified from ALL81 columns, not from an entry bound or a row norm.
The proper unordered-entry l1 norms of(11) are therefore at most4,5,1/2,
respectively. Triangle inequality and(2) give

\[
 \|D\|_{op}\le4\sum_B\sigma_A+5\sum_{E1}|z_e|+t/2
       \le5(\sum_B\sigma_A+\sum|z_e|+t)\le10\Delta.\tag{12}
\]

Actual completion is separately paid. In C-unit changes, the full empty
responses of each column are:

* sigma_A: empty/A=-1, empty/b=empty/c=1/2, loop0;
* z_AV: empty/V=1, empty/b=empty/c=-1/2, loop0;
* t: empty/b=empty/c=1/2, loop=-1.

If V=b or c, the coincident terms are added. Every other empty entry
is0. These formulas follow from original row sums, and the checker
compares every induced empty response and ALL actual stochastic rows.
Proper entries of every column also have absolute value at most1,
because |Q_ij|<=2. Thus every actual column has entry maximum at most1,
including its diagonal loop. Applying triangle inequality to these
literal lifts and(2) gives the second bound in(5). This bound does not
substitute a proper norm for an actual entry norm.

Finally E^T E=I277+J277, whose largest eigenvalue is278. Hence
||EDE^T||op<=278||D||op. Dividing by220 proves both distances in(7)
whenever the projected point is an actual feasible optimizer. The
same division gives Delta/110 from the direct actual-entry bound2Delta.

## Global feasible projection: a coupled dual budget and an interior blend

Let

\[
 S_*=\sum_B\sigma_A+t+\sum_{E1}|z_e|,\qquad
 W_*=\sum_{E2}r_e^+ +\sum_{E0}r_e^-.
\]

Here S_* is a scalar residual budget, distinct from the star S. The
COMPLETE dual identity(1), including its edge multiplicities, says

\[
 2\Delta=S_*+2W_* .\tag{12a}
\]

Every individual proper correction has absolute value at most S_* by
the literal column bound1. For an E2 edge the projected positive repair,
and for an E0 edge the projected negative repair, are therefore at most

\[
 W_*+S_*=\Delta+S_*/2\le2\Delta.\tag{12b}
\]

Using the coupled identity is essential to this improved coefficient;
bounding wrong signs and corrections separately would only give3Delta.
All mixed repairs of the projected point already vanish. The blend(5a)
stays in the affine equality set A_tau. Its E2/E0 strict sign margins
for Delta>0 are at least

\[
 \theta\eta-(1-\theta)2\Delta
       =\frac{\eta\Delta}{\eta+3\Delta}>0.\tag{12c}
\]

Every projected unforced allowed actual M entry is at least its floor
minus2Delta/220, since the INPUT is feasible and the direct actual
correction bound is2Delta. Its blend with the center, whose surplus is
9eta/220, consequently has surplus at least

\[
 \frac{25\eta\Delta}{220(\eta+3\Delta)}>0\quad(\Delta>0).\tag{12d}
\]

All163 forced ordered positions satisfy their exact floor in both blend
endpoints; every forbidden entry is zero and every row is stochastic.

Both C and U of the INPUT are PSD. For C this follows from L PSD and(3)
on1-perp, because E has full column rank and E^T maps1-perp onto the
proper space. For U, entry nonnegativity and symmetric stochasticity give

\[
 x^T(I-M)x=\tfrac12\sum_{A,B}M_{AB}(x_A-x_B)^2\ge0.
\]

Thus278I-L=220(I-M) PSD and the other equality in(3) gives U PSD.
The unblended projected lower/upper proper matrices have floors at least
-10Delta. The strict center supplies39/4096. Therefore both blended
proper floors, on h-perp for C and the full proper space for U, are at least

\[
 \frac{(3\cdot39/4096-10\eta)\Delta}{\eta+3\Delta}
 =\frac{(14971/524288)\Delta}{\eta+3\Delta}>0
 \quad(\Delta>0).\tag{12e}
\]

This verifies original PSD and every entry constraint, so Phi_tau(M)
is an actual feasible optimizer, not just an equality-set point. The
strict signs, unforced floors and lower definiteness give ri(O_tau).
For Delta=0, identity(12a) forces all sigma,t,z to vanish and hence D=0,
theta=0 and Phi_tau(M)=M in O_tau. The rational denominator eta+3Delta
is always positive, P is continuous, and Pi_tau is affine. Phi_tau is
thus continuous and fixes the entire O_tau. Neither this conclusion nor
its input domain imposes invariant coordinates or a local PSD margin.

To pay GLOBAL distances, every entry of a nonnegative stochastic matrix
lies in[0,1], so ||M-M*||max<=1. Also L PSD gives M>=-29I/110 and the
stochastic identity above gives M<=I; the center has the identical two
bounds. Taking Rayleigh quotients of their difference gives
||M-M*||op<=139/110. Now

\[
 \Phi_\tau(M)-M=(1-\theta)(\operatorname{Pi}_\tau(M)-M)
                           +\theta(M^*_\tau-M).
\]

Triangle inequality with(5) and the actual lift factor278 yields(5b)
exactly. Its linear coefficients are3/eta+1/110 and
3*139/(110eta)+139/11, the two displayed exact rationals. This uses
bounded diameters only for the BLENDED map. It does not infer a bound
from Delta on independent NS displacement from the chosen center.

## The local cost estimate includes positive mixed entries

Let R=C-C*. Every proper entry of R has absolute value at most delta.
As delta<=2^-32<eta, E2 repairs remain strictly negative and E0 repairs
strictly positive. The center's mixed repairs vanish. Consequently

\[
 \Delta=\sum_{e\in E0}R_e+
              \sum_{e\in E1}\max(R_e,0).\tag{13}
\]

In particular a count of only7885 good edges is insufficient: the second
term cannot be discarded. Define a symmetric matrix Gamma on the219
original nonstar rows with value1/2 at each of the two positions of every
E0 edge and each mixed edge with R_e>0, and0 elsewhere. Then
Delta=tr(Gamma R_T), while

\[
 \|\Gamma\|_F^2\le(7885+9009)/2=8447,\qquad
 \|R_T\|_F^2\le219\delta^2.
\]

The second inequality follows from compression not increasing operator
norm and the sum of squares of219 eigenvalues. Frobenius Cauchy-Schwarz
and the exact integer inequality219*8447=1849893<1361^2=1852321 give

\[
 0\le\Delta\le1361\delta.\tag{14}
\]

Gamma may depend on R; its stated uniform Frobenius bound holds for every
choice. This is an ordinary all-real estimate, not a sample of matrices.

## Paying all original feasibility and the spectral gaps

Write delta<=eta/4096. From(5),(14), every corrected proper entry differs
from the center by at most delta+2Delta<=2723delta. Since
2723/4096<3/4, both strict NN repair margins stay at least eta/4;
the mixed repairs and all163 forced ordered floors satisfy the exact
target equalities established above.

For OTHER actual entries, the original difference lifts as ERE^T and
has entry maximum at most its operator norm, at most278delta. The
correction has the distinct entry bound2Delta. Thus total actual
entry difference from the center is at most3000delta. Since3000<4096,
the center surplus9eta in C units leaves at least8eta for every unforced
allowed position. Dividing by220 yields the asserted original M floors.
Forbidden entries remain exactly zero by support of both the input and
the explicit correction. Every actual stochastic row is preserved by(3).

For lower and upper proper cones, the operator difference from C* is
at most delta+10Delta<=13611delta. It annihilates h, so on h-perp the
lower floor, and on the whole proper space the upper floor, are at least

\[
 39/4096-13611\delta
 \ge39/4096-4\eta=2495/262144>1/128,\tag{15}
\]

where13611<4*4096. Therefore the original lower endpoint is PSD, all
entries meet their floors, and Pi_tau(M) belongs to F_tau. Equations(4),
the NN signs and the complete dual identity prove optimality; strict
unforced inequalities and lower definiteness give ri(O_tau).

For completeness of the actual spectral conclusion: E is injective,
its image is1-perp in the278-dimensional actual space,
and E^T E>=I. For PSD C_hat with kernel span(h), the nonzero spectrum of
E C_hat E^T equals that of C_hat^(1/2)(I+J)C_hat^(1/2). On h-perp its
floor is at least1/128 by min-max. The constant J direction has
eigenvalue278. Thus the lower endpoint has276 positive centered
eigenvalues and the positive constant eigenvalue, with a one-dimensional
kernel: rank277. The same argument applied to positive definite U_hat
gives277 positive upper eigenvalues, also with floor1/128, and kernel
the constants. Dividing the two floors by220 gives1/28160 for each of
the other276 M eigenvalues, and the simple extremes -29/110 and1.

## Exact and ordinary coverage

The finite certificate supplies the original incidence labels/inverse,
all coefficients in(11) and the exact stated parameters. The separate
checker freshly enumerates the actual carrier, ALL9091 residual columns,
ALL81 degree responses for each, complete mixed/good responses, every
nonzero proper and actual entry, every actual row and empty response,
selected-coordinate preservation, both inverse products, all norm maxima
and every rational inequality. Omitted entries are exactly zero by the
explicit sparse completion formula. Complete column records are hashed
in order without storing a large corpus. Normal, optimized and cold-copy
checks compare whole deterministic records; adverse controls change
mathematical meanings rather than merely checksums.

The map derivation, unit-basis-to-all-real linearity, coupled dual budget,
continuous global blend, norm inequalities, continuous local domain,
feasibility, relative interior and spectral congruence remain the explicit
UNFORMALIZED ordinary arguments above.
All dependencies are the SAME carrier/comparison; finite residual checks
alone do not certify the old center or its PSD. The earlier independent
sign-cone estimate does not itself supply distance to the FULL feasible
optimizer set, which is the new global and local conclusion here.
General H/I, other carriers/counts, arbitrary anchored displacement from
the center, optimal constants, a maximal radius and historical priority
remain unclaimed. The local affine projection preserves proper NS
entries; the global blended projection uses their bounded diameters.
