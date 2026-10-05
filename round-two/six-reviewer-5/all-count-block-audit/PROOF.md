# Complete physical block criterion, small-pool boundaries and exact spectral windows

Actual agent **six-reviewer-5**, independent mathematical reviewer. Ordinary
proof, **unformalized**. This is a separate audit of the all-count structural
part of committed LEMMA10332, not of its q19 attaining family. The earlier
capacity review and its original pending graph receipt remain separate.

The count-dependent formulas and six-sector approach are attributed to
six-downset-2's STRUCTURAL.md, source
58f9c6ab8b6ab58232cd275ddb4691d3430fb02f. Fixed-count sector work 10242
and the full one-star coordinate interface 10248 are prior campaign work.
The proof below rederives the bridge independently. Symmetrization,
incidence kernels, tensor decomposition and semidefinite congruence are
classical methods; no exclusive literature priority is claimed.

## 1. Domain and literal coordinates

Fix disjoint named points a,b,c and pools X,Y of integer sizes k,m >= 2.
Let D consist of all sets of size at most two, the triple abc, all abx/acx
with x in X or Y, and all bcy with y in Y. The empty set is retained.
Writing q=k+m gives
\[
 N=(q^2+13q+16)/2-k,\quad s=3q+4,\quad h=N-s.
\]
The a-star S has size s; the b,c stars have size s-k; the X and Y
stars have sizes q+5 and q+6. Thus a is uniquely maximal in this domain.
Let Q=D minus the empty set and singleton a; its size is N-2. Orbit
types t=(R,i,j) record the subset R of the named core and pool counts.
There are exactly 22 types, explicitly:

| Core R | Pool counts (i,j) |
|---|---|
| empty | (1,0),(0,1),(2,0),(1,1),(0,2) |
| a | (1,0),(0,1) |
| b or c, separately | (0,0),(1,0),(0,1) |
| ab or ac, separately | (0,0),(1,0),(0,1) |
| bc | (0,0),(0,1) |
| abc | (0,0) |

The orbit weight is \(w_t=\binom{k}{i_t}\binom{m}{j_t}>0\).
Give each unordered disjoint type pair an arbitrary real coefficient
\(a_{tu}=a_{ut}\). At generic k,m >= 4 there are 143 such parameters.
One may retain these 143 formal parameters at smaller counts, but an
impossible disjoint pair has no matrix entry and its coefficient is
ignored. No rationality or entry-sign assumption is used.

Define the real symmetric Q-matrix T to have diagonal s-1, value -1
on intersecting distinct vertices, and coefficient a_tu on a disjoint
pair of the indicated types. The star-indicator vectors on Q are r
and b=1-r. Complete its proper matrix C by
\[
 C_{Q,a}=-Tr,\qquad C_{a,a}=s-1.
\]
Since all members of S intersect, \(Tr\) on S minus a is identically
one and \(r^TTr=s-1\). Consequently the completion has the required
diagonal/intersection values and \(C1_S=0\).

Let Phi have column e_A-e_a when A contains a, and e_A-e_empty
otherwise. Its Q rows are the identity, so it is injective. With J
the N-by-N all-one matrix, the full original lift is
\[
 L=J+\Phi T\Phi^T.
\]
Equivalently, complete empty rows by \(L_{0,A}=1-\sum_B C_{A,B}\)
and \(L_{0,0}=1+\sum_{A,B}C_{A,B}\), retaining the actual loop.
Every original row of L sums to N, all proper diagonals are s, and
every intersecting offdiagonal entry is zero. Thus \(M=(L-sI)/h\)
is supported and stochastic for every real choice of coefficients.
Positivity is an additional condition, not an assumption in this lift.

## 2. Both original endpoints and their metric

The centered star \(z=N1_S-s1\) has norm squared Nsh. The two vectors
1,z are orthogonal to each other and to every column of Phi. Hence
\(U=\{1,z\}^\perp=\operatorname{range}\Phi\).
Since \(r^Tr=s-1\), \(b^Tb=h-1\) and \(r^Tb=0\),
\[
 G=\Phi^T\Phi=I+rr^T+bb^T,
 \qquad G^{-1}=I-rr^T/s-bb^T/h.
\]
Multiplying each rank-one summand proves this inverse directly.
The projector onto U is \(P_U=\Phi G^{-1}\Phi^T\); therefore
\[
 NI-L=\Phi B\Phi^T+zz^T/(sh),\qquad B=NG^{-1}-T. \tag{1}
\]
The summands on 1,z,U act on mutually orthogonal subspaces. Since
Phi is injective, L is PSD iff T is PSD, and NI-L is PSD iff B is
PSD. The second condition is an extra upper cap, not Conjecture I.
For arbitrary symmetric T, irrespective of positivity,
\[
 \operatorname{rank}L=1+\operatorname{rank}T,
 \quad\operatorname{rank}(NI-L)=1+\operatorname{rank}B.
\]
Their kernels are respectively
\(\operatorname{span}(z)\oplus\Phi G^{-1}\ker T\) and
\(\operatorname{span}(1)\oplus\Phi G^{-1}\ker B\).
These are original-coordinate statements, not quotient ranks.

## 3. Orbit constants

Adopt \(\binom{n}{r}=0\) unless \(0\le r\le n\), and put
\[
 d_{tu}=\binom{k-i_t}{i_u}\binom{m-j_t}{j_u}
\]
when R_t and R_u are disjoint, and zero otherwise. This counts the
actual u-type vertices disjoint from a fixed t-type vertex. Thus
\(w_td_{tu}=w_ud_{ut}\), including zero incidences at small counts.
The T action and metric on orbit indicators are
\[
 H^0_{tu}=s\delta_{tu}-w_u+d_{tu}(1+a_{tu}),\qquad
 W^0=\operatorname{diag}(w_t).
\]
The inverse-Gram action is
\[
 J^0_{tu}=\delta_{tu}-r_tr_uw_u/s-b_tb_uw_u/h.
\]
These yield the symmetric quadratic forms \(W^0H^0\) and
\(W^0(NJ^0-H^0)\). Their metric is W^0, not the identity on
unweighted orbit indicators.

## 4. Standard directions and the zero-weight boundary

For any zero-sum real f on X, let \(F_t(A)=\sum_{x\in A\cap X}f_x\)
on orbit t and zero outside it. Counting pairs of indices gives, for
zero-sum f,g,
\[
 \sum_{A\text{ of type }t}F_t(A)G_t(A)
 =W^X_t(f\cdot g),\quad
 W^X_t=\binom{k-2}{i_t-1}\binom{m}{j_t}.
\]
For i=1 this is one copy per independent Y choice. For i=2 it is
the identity \(\sum_{x<y}(f_x+f_y)(g_x+g_y)=(k-2)f\cdot g\).
Hence use exactly the types with W^X_t > 0. There are eight at
k >= 3 and seven at k=2: the XX-pair type is removed at k=2
because f_x+f_y is then identically zero.

For a fixed destination A, sum F_u over the disjoint u-type members.
Each x outside A occurs \(\binom{k-i_t-1}{i_u-1}\) times. The sum
of f outside A is minus its sum inside A. Multiplying by the independent
Y choices proves the complete action
\[
 H^X_{tu}=s\delta_{tu}
 -\binom{k-i_t-1}{i_u-1}\binom{m-j_t}{j_u}(1+a_{tu})
\]
for disjoint core masks, with just the diagonal term for overlapping
masks. The same argument proves zero image on types not belonging
to this standard sector. The all-one part annihilates f.
On an orthonormal basis of the zero-sum f space this is k-1 copies
of H^X with positive metric W^X. A nonorthonormal difference basis
has the additional positive Gram factor f dot g; it gives the same
PSD criterion by congruence.

Interchanging the pools gives
\[
 W^Y_t=\binom{k}{i_t}\binom{m-2}{j_t-1},\quad
 H^Y_{tu}=s\delta_{tu}
 -\binom{k-i_t}{i_u}\binom{m-j_t-1}{j_u-1}(1+a_{tu}).
\]
Use only W^Y_t > 0: nine types at m >= 3, eight at m=2, removing
the YY type. There are m-1 copies. Weighted symmetry follows either
by the counting identities or from self-adjointness of literal T and
the proved Gram identities.

## 5. Harmonics, mixed directions and completeness

For pool size n >= 3, the unsigned point/pair incidence matrix has
rank n. A row relation satisfies c_x+c_y=0 for every pair; any triangle
forces all coefficients to vanish. Its kernel has dimension n(n-3)/2.
It is orthogonal to constants and all additive pair functions because
all incident sums vanish. Additive zero-sum functions have dimension
n-1 by their positive metric n-2. These pieces exhaust pair space.
At n=3 the kernel is zero. At n=2 the pair space is one-dimensional
and consists of constants only: the additive zero-sum map is zero,
the incidence rank is one and the kernel is zero. No negative
"harmonic dimension" or zero metric is used.

An incidence-zero pair function p has total sum zero. Summing it over
pairs disjoint from zero or one fixed point gives zero. For disjointness
from a pair {x,y}, inclusion-exclusion of the two zero incident sums
gives p_xy. An original vertex with two X points is necessarily in XX.
Thus the full XX harmonic action is the scalar
\(\lambda_{XX}=s+1+a_{XX,XX}\), supported only on XX. This sector
exists only when k >= 4. The YY action is
\(\lambda_{YY}=s+1+a_{YY,YY}\), present only when m >= 4.

On XY, matrices with zero row and column sums have dimension
(k-1)(m-1). Their sum over the complement of the rows/columns
selected by a destination equals their sum over the selected rectangle.
It vanishes unless that destination is XY, where it equals the original
entry. Hence the mixed action is \(\lambda_{XY}=s+1+a_{XY,XY}\).
The constants, X row means, Y column means and this mixed sector
exhaust rectangular space.

All distinct sectors are orthogonal: constants use total sums,
pair sectors use incidence sums, and mixed sectors use row/column
sums. Each standard embedding is injective on its retained positive
metric types. Consequently this is a full direct decomposition of Q,
not merely a dimension census. Its dimension is
\[
22+(8-1_{k=2})(k-1)+(9-1_{m=2})(m-1)
 +\max(0,k(k-3)/2)+\max(0,m(m-3)/2)+(k-1)(m-1)=N-2.
\]
Every nonconstant sector has zero sum in every orbit, so r and b
annihilate it. Thus G inverse acts as the identity on each such sector.

## 6. The complete criterion and target verdict

For every integer k,m >= 2 and every real choice of the defining
coefficients, T is PSD iff these are all PSD:

* W^0 H^0;
* W^X H^X on the positive-weight X types;
* W^Y H^Y on the positive-weight Y types;
* the XX scalar if k >= 4, the YY scalar if m >= 4, and the XY scalar.

For B the corresponding forms are W^0(NJ^0-H^0), W^X(NI-H^X),
W^Y(NI-H^Y), and N minus each present scalar. For any real delta,
T >= delta I iff each form minus delta times its indicated metric
is PSD; the same statement holds for B. The ordinary proof above
establishes the arbitrary-real and all-count quantifiers. Finite
checks below validate code/normalization, not these infinite domains.

This confirms precisely the all-count criterion asserted in 10332
at its k,m >= 4 domain. It also proves the stated smaller-pool
extension, with deleted zero-weight rows and absent scalars. It
confirms neither a numerical q19 factor nor a feasible matrix at any
new count. An unused coefficient on an impossible disjoint pair is
invisible to T; no constraint may be inferred from its absent sector.

If T and B are both at least delta I with delta > 0, (1) and G >= I
give ranks N-1 for both original endpoints. On U the nonzero spectrum
of Phi T Phi transpose is the spectrum of T^(1/2) G T^(1/2), bounded
below by delta; the same holds for B. The separate positive eigenvalues
on 1 or z equal N. When delta <= N, all other N-2 eigenvalues of M
have both endpoint gaps at least delta/h. This is conditional on the
actual residual inequalities and does not transport another count's
certificate or imply entry positivity.

## 7. Exact original spectral windows, a proved refinement

For any real gamma, the exact spectral inequalities on U are
\[
 \gamma I_U\preceq L|_U\preceq (N-\gamma)I_U
 \quad\Longleftrightarrow\quad
 \gamma G^{-1}\preceq T\preceq (N-\gamma)G^{-1}. \tag{2}
\]
Indeed, subtract gamma P_U from each U endpoint in (1); injectivity
of Phi makes both congruences equivalences. This gives the exact
forms
\[
 W^0(H^0-\gamma J^0),\quad W^0((N-\gamma)J^0-H^0),
\]
with W^X(H^X-gamma I), W^X((N-gamma)I-H^X), the analogous Y
forms, and gamma <= lambda <= N-gamma for each present scalar.
Thus one can compute an exact original-coordinate spectral window
without imposing the stronger sufficient residual floor delta I.
For 0 < gamma <= N, (2) implies simple fixed extremes -s/h and 1
for M, and gives both remaining gaps gamma/h. Infeasible parameter
values make this a vacuous equivalence, not an existence claim.

For context, finite averaging over permutations of X and Y preserves
support, row sums, lower PSD, upper PSD and any original entry floor.
Any lower-H competitor is forced into the one-star affine space:
support and stochasticity give z transpose M z = -Ns^2, so lower
PSD gives Lz=0, hence L1_S=s1. Averaging then yields exactly these
type coefficients, since disjoint pair types are group orbits. This
justifies an invariant existence search under the stated convex
conditions, without assuming an individual competitor was invariant.
No feasible solution to that search is supplied here.

## 8. Independent finite evidence and limits

check.py creates the carrier from named triples, all orbits and a square
literal basis. It derives pair kernels by rational row reduction and
tests full basis rank by a nonzero determinant modulo 1009. It checks
every declared Gram entry and every original row action, with the
constant and each independent coefficient compared separately. This
is an affine identity check in all 143 formal parameters at each
tested count, not a sampled coefficient vector. A separate reproducible
integer coefficient vector checks every original lower lift, upper
lift, projector and spectral-window identity, including the empty
vertex, loop and eliminated anchor. It also checks all actual budgets.

The fifteen tested pairs are (2,2),(2,3),(3,2),(2,4),(4,2),(2,6),(6,2),
(3,3),(3,4),(4,3),(4,4),(4,5),(5,4),(3,6),(6,3). Exact Python
integers/Fraction are used. No author program, factor, certificate,
EXPECTED file, validator, private corpus or peer checker was opened,
imported or executed. The target's entire written proof and public
provenance were exposed; this is independent reconstruction, not a
blind review. The ordinary decompositions, congruences and continuous
real quantifiers are unformalized trust boundaries.
