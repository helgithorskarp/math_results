# Independent original near-cube reduction and two scoped refinements

Actual author **six-reviewer-2**, role **independent mathematical reviewer**.
Ordinary real linear-algebra and Boolean-ladder proof, UNFORMALIZED.
The complete defining proof of LEMMA9639 was visible before this derivation;
new target executable/oracle files were withheld until the primary seal.
The previous own linear helper and previously exposed researcher model helpers
are credited in PROVENANCE.json. This is an independent audit, not a blind
rediscovery or a new attribution of classical harmonic methods.

## Original domain, support and quantifiers

Fix **every integer** \(n\ge6\) and \(1\le k\le n-2\). Write
\[
D=\{A\subseteq[n]:|A|\le n-2\},\quad F=D\setminus\{\varnothing\},
r=n-2,\quad N=2^n-n-1,\quad m=N-1,
s=2^{n-1}-n,\quad h=N-s,\quad d=\lfloor n/2\rfloor.
\]
An original capped H is a real symmetric matrix indexed by **all of D**, with
\(M\mathbf1=\mathbf1\), \(M_{AB}=0\) whenever \(A\cap B\ne\varnothing\), and
\(0\preceq L=sI+hM\preceq NI\). The empty row and permitted empty loop belong
to this definition. The extra condition \(S_k\) kills nonempty proper disjoint
pairs whose two sizes exceed k. Complementary pairs stay allowed.
There is no sign, centering, rationality or initial invariance assumption.

Set \(q=\min(d,\max(k,3))\) at even n and
\(q=\min(d,\max(k,2))\) at odd n.
We confirm the precise real existence and greatest-rank cone equivalences in9639.
We also prove an **exact same-specified normalized whole-gap** variant and a
**conditional rationalization of simultaneous greatest ranks**. Neither is an
all-order positive construction or a general boundary rational-feasibility theorem.

## Actual empty lift and forced star equations

For an invariant table \(\beta_{ab}=\beta_{ba}\), zero if \(a+b>n\) or
\(a+b<n\) and \(a,b>k\), put
\[
C_{AB}=s\delta_{AB}-1+\beta_{|A|,|B|}\mathbf1_{A\cap B=\varnothing},
\quad E=\begin{bmatrix}-\mathbf1_m^T\\ I_m\end{bmatrix},
\quad L=J_N+ECE^T,\quad U=NI_m-J_m-C.
\]
The nonempty diagonal of L is s and every intersecting off-diagonal is zero.
Because \(E^T\mathbf1_N=0\), every original row of L sums to N.
The empty entries are exactly
\[
L_{\varnothing,A}=1-(C\mathbf1)_A,
\qquad L_{\varnothing,\varnothing}=1+\mathbf1^TC\mathbf1.
\]
Direct multiplication gives \(NI_N-L=EUE^T\).
E is injective onto \(\mathbf1_N^\perp\); J is positive on the remaining
one-dimensional space. Thus L is PSD iff C is PSD, its rank is
\(1+\operatorname{rank}C\), and the cap is PSD iff U is PSD.
This proves equivalence on the actual N vertices, not a compressed replacement.

For an arbitrary original PSD L let y_i be the full indicator of point star i.
It has s entries equal to1. Intersection support and diagonal s give
\(y_i^TLy_i=s^2\); row sums give \(y_i^TL\mathbf1=Ns\).
Hence \((y_i-s\mathbf1/N)^TL(y_i-s\mathbf1/N)=0\).
PSD annihilates this vector, so \(Ly_i=s\mathbf1\).
For an invariant lift this is exactly \(Cy_i|_F=0\).
On a row A excluding i this reads
\[
\sum_{b=1}^r\beta_{ab}\binom{n-a-1}{b-1}=s,
\quad\text{equivalently}\quad
\sum_{b=1}^r b\beta_{ab}\binom{n-a}{b}=(n-a)s.
\]
On a row including i the diagonal and constant terms cancel and there is no
remaining disjoint term. Consequently these r equations annihilate all n stars
and impose no extra zeroth moment: \(C\mathbf1\) need not vanish.

For each a=2..r the coefficient of the distinct singleton variable
\(\beta_{1a}\) is n-a. Solve it using the free pairs with a,b>=2 and
then solve the a=1 equation for \(\beta_{11}\) with coefficient n-1.
These nonzero integer pivots prove real rank r and a **rational affine decoder**.
Since k>=1 every singleton coordinate is allowed by S_k. All excluded proper
coordinates are fixed zeros among the free variables. The total supported,
free and excluded counts are, respectively,
\[
\lfloor n^2/4\rfloor-1,\quad\lfloor(n-2)^2/4\rfloor,
\quad\begin{cases}t(t-1)&n\text{ even},\\t^2&n\text{ odd},\end{cases}
\quad t=\max(d-k,0).
\]
These counts also follow by summing the integers a<=b<=r, a+b<=n, and then
summing k<a<=b with a+b<n. This decoder/counting is credited9365/9639 context,
not a new construction or an additional face constraint.

## Complete physical Boolean sectors

Use counting inner products on each Boolean layer. Let R add one point and
D=R* remove one point. On layer a, \(DR-RD=(n-2a)I\).
For a<n/2, \(\|Rf\|^2=\|Df\|^2+(n-2a)\|f\|^2\) proves R injective
and, by adjunction, D surjective onto the preceding layer.
The harmonic kernel at j has dimension
\(\nu_j=\binom nj-\binom n{j-1}\), with \(\binom n{-1}=0\).
For harmonic f, define
\(f_a(A)=\sum_{T\subseteq A,|T|=j}f(T)=R^{a-j}f/(a-j)!\).
The commutator inductively gives
\[
DR^t f=t(n-2j-t+1)R^{t-1}f,
\qquad \|f_a\|^2=\binom{n-2j}{a-j}\|f\|^2
\quad(j\le a\le n-j).
\]
Copies of orthogonal harmonic vectors stay orthogonal by adjunction; copies
with different initial degrees are orthogonal because enough lowering kills
the higher harmonic vector. Their telescoping dimensions equal \(\binom na\)
on every layer, including a>n/2. Thus every original nonempty direction is
covered, without a truncation or a matching-basis completeness assumption.

For each j=0..d put
\[
I_j=\{\max(1,j),\ldots,\min(r,n-j)\},\qquad
g_{ja}=\binom{n-2j}{a-j},\qquad G_j=\operatorname{diag}(g_{ja}).
\]
The disjoint b-layer action on f_b is
\[
\sum_{B\cap A=\varnothing,|B|=b} f_b(B)
=\binom{n-a-j}{b-j}\sum_{T\subseteq A^c,|T|=j}f(T)
=(-1)^j\binom{n-a-j}{b-j}f_a(A).
\]
For the last identity expand the complement indicator by inclusion-exclusion.
Every proper T of size<j has sum of f over j-sets containing T equal to zero,
as follows from repeated harmonic lowering; the surviving size-j term has
sign (-1)^j. J acts only at j=0, with coefficient \(\binom nb\).
Therefore the complete coefficient matrices are
\[
K_j[a,b]=s\delta_{ab}-\mathbf1_{j=0}\binom nb
+(-1)^j\beta_{ab}\binom{n-a-j}{b-j},
\qquad
U_j[a,b]=h\delta_{ab}-(-1)^j\beta_{ab}\binom{n-a-j}{b-j}.
\]
Each appears with multiplicity \(\nu_j\). The **full physical** forms
\(G_jK_j,G_jU_j\) are symmetric. The orthonormal forms are
\(G_j^{1/2}K_jG_j^{-1/2}\) and \(G_j^{1/2}U_jG_j^{-1/2}\).
A nonsymmetric quotient cannot be tested directly as a quadratic form.
Complete PSD, rank and floor statements use all of these physical spaces.

## Omitted degrees, signs, middle singleton and upper floor

If j>q, every surviving a,b exceeds k and j>=2. Proper coordinates vanish;
unsupported coordinates cannot contribute. A complementary coefficient has
binomial factor1. Thus
\[
K_j=sI+(-1)^j T,\qquad U_j=hI-(-1)^j T,
\quad T_{ab}=\beta_{ab}\mathbf1_{a+b=n}.
\]
For each nonzero off-diagonal of T the two physical norms are equal:
\(g_{ja}=g_{j,n-a}\). Hence this quotient **on this restricted block** already
is its orthonormal form. The same equality holds in the lower reference block,
even though reference and high norms are not identical to each other.

At even n take ell=2 for even j and ell=3 for odd j. Both reference degrees
are retained, I_j is a subset of I_ell, and their orthonormal principal
restrictions are exactly the high blocks. The middle singleton has coefficient
s+beta at even degree and s-beta at odd degree; the two references retain it
with its correct sign. At odd n no middle singleton exists. Use ell=2 and,
for odd j, multiply each layer above n/2 by -1. Each complementary edge crosses
the middle, so this diagonal orthogonal congruence changes exactly the needed
signs. For even j use the identity. This proves all omitted lower/upper blocks
are signed physical principal restrictions. It also proves common floors and
strict positivity inherit. At n6 or saturated q=d there is no omitted block;
these cases are vacuous, not exceptions to the full cones.

Assume the retained lower forms j0..q are PSD. Every complementary pair
with both sizes>k has |beta|<=s. For distinct sizes, the reference degree-two
orthonormal principal block is \([[s,\beta],[\beta,s]]\): its small-layer
diagonal proper coordinate vanishes and its larger-layer diagonal is
unsupported. At even n the middle size>=3 is bounded by the two retained
reference diagonals s+beta and s-beta. These arguments apply precisely to
pairs that can occur in j>k. Consequently **every** j>k, even when j<=q,
satisfies
\[
U_j\succeq(h-s)I=(N-2s)I=(n-1)I
\]
in orthonormal coordinates. This is a conditional inference from lower
positivity, not from the star equations or unsupported finite tests alone.

All lower tests therefore reduce exactly to degrees0..q; all upper tests to
**entire** degrees0..min(k,d). For a scalar core floor epsilon>=0 use all
upper0..q, or only upper0..min(k,d) if epsilon<=n-1 and lower positivity holds.
The mean-coupled degree-zero upper form is never deleted. This confirms9639.

## Greatest ranks and arbitrary real witnesses

The star equations force the cardinality vector (a) in ker K0 and the constant
layer vector (1) in ker K1. Their multiplicities are1 and n-1. The original
centered stars are independent: their empty coordinate forces the sum of
coefficients to zero, then their singleton coordinates force each coefficient
to zero. Thus rank L<=N-n for every original witness.
Equality holds iff these are the **only** low0/1 kernels and every retained
higher lower cone2..q is strictly positive; principal inheritance gives every
omitted cone strictly positive. Nullity C=n, so rank L=N-n. Under lower
positivity, strict upper tests0..min(k,d), together with the automatic n-1
floor, are equivalent to U positive definite and rank(NI-L)=N-1.

Average any original real witness over point permutations. All affine
conditions, both PSD inequalities and S_k are preserved. On F, intersecting
entries are fixed and disjoint pairs are classified by their two sizes,
so the average has exactly the invariant beta form. Row sums determine its
original empty row. The forced star argument supplies its r affine equations.
Conversely the reduced cones reconstruct an actual original witness by the
complete lift and decomposition above. This proves the existence equivalence
without an invariance premise.

For PSD matrices, the kernel of a positive finite average is the intersection
of their kernels (apply nonnegative quadratic forms). When lower rank is
N-n every kernel is the same permutation-invariant centered-star space;
when upper rank is N-1 every upper kernel is span(1). Consequently either
maximal rank, and **both simultaneously**, survive averaging. This addresses
all-real rank quantifiers, not merely the rank of a chosen invariant witness.

## Proved refinement 1: exact specified whole-space gap tests

Let \(P=I_N-J_N/N\) and \(Q=I_m-J_m/N\). Since
\(E^TE=I_m+J_m\), its inverse is Q; hence \(EQE^T=P\).
Therefore, for each **specified** gamma>=0,
\[
NI-L\succeq\gamma P\quad\Longleftrightarrow\quad U\succeq\gamma Q.
\]
Both directions follow from full-column congruence by E, not an inequality
between unrelated eigenvalue normalizations. In sector j the metric Q has
coefficient matrix
\[
Q_j[a,b]=\delta_{ab}-\mathbf1_{j=0}\binom nb/N,
\quad W_j=G_jQ_j.
\]
Thus the exact physical tests are \(G_jU_j-\gamma W_j\succeq0\).
For j>=1 Q_j=I, so the omitted principal-restriction proof is unchanged.
Together with the full retained lower tests, for arbitrary gamma>=0 retain
upper0..q; for 0<=gamma<=n-1 retain just upper0..min(k,d). The degree-zero
mean term in W0 is indispensable. These tests characterize, at the **same**
gamma, invariant original witnesses and existence of arbitrary original
witnesses with that whole gap: averaging preserves P as well as the cap.

The distinction from U>=gamma I is real even on an actual capped H.
At n6 use the **known centered beta33=24 baseline** with free values
beta22=4/3,beta23=0,beta24=22,beta33=24; solve singleton values anew.
Our actual 57-vertex L is PSD of rank50 (not greatest51), and NI-L-2P
is PSD of rank56, by independent exact Schur congruences. All four complete
sector tests U_j-2Q_j are strictly positive. Yet C1=0 gives U1=1, so
\(\mathbf1^T(U-2I)\mathbf1=-56\). This is a counterexample only to the
unclaimed necessity of the scalar floor, **not a defect in9639**.
The finite witness and its whole pivot hashes are in EXPECTED.json and are
recomputed from the literal original vertices. No new baseline construction
or optimal gap is claimed. Classical congruence/metric identities are prior
methods; the scoped reduced same-gamma characterization is this refinement.

## Proved refinement 2: conditional rational joint strict feasibility

For each fixed n,k, existence of a **real** original capped S_k witness with
both ranks rank L=N-n and rank(NI-L)=N-1 is equivalent to existence of a
**rational invariant original** witness with both ranks. The rational-to-real
direction is immediate. For the other direction average as above, preserving
both ranks. The free S_k face has a rational affine parametrization by the
star decoder. Its lower0/1 forced kernels are fixed rational vectors and are
annihilated identically on that affine face. Restrict each physical lower0/1
form to any fixed rational complement of its kernel. These restrictions,
all retained higher lower forms, and all retained upper forms are strictly
positive at the averaged point. There are finitely many forms for fixed n,k;
positive definiteness is open because the minimum of the quadratic form on
the unit sphere is positive and coefficient entries vary continuously.

Rational free coordinates are dense in this real affine parameter space.
Choose them sufficiently close to preserve each strict restricted lower
and full upper form. Forced kernel annihilation removes cross terms with
the rational complements; thus the full lower forms stay PSD with exactly
the prescribed kernels. All omitted forms inherit, the star equations and
support remain exact, and the original empty lift is rational. This proves
the equivalence. The statement remains meaningful if the free dimension is
zero: the rational decoder then supplies the sole point itself.

Moreover, if an original joint-rank witness has whole gap gamma>0, its
average has gap at least gamma. For **any specified rational**
0<=eta<gamma, the forms U_j-eta Q_j are strictly positive, including degree0
because Q is positive definite. Include these finitely many open conditions
in the same approximation. The rational witness keeps whole gap at least eta.
No preservation of an attained boundary gamma is asserted.

This is a qualitative conditional theorem. It supplies no denominator,
rounding tolerance, algorithmic recovery or witness at an unproved order.
It does **not** say real feasibility on an arbitrary singular SDP boundary
implies rational feasibility. The density/continuity method is classical;
review9606 already discusses the particular n24 open neighborhood. The
increment here is the all-real, all-order, simultaneous greatest-rank
quantifier and exact support/star-face bridge. Effective bounds would require
an explicit margin for the retained strict restrictions and the decoder.

## Verification boundary and literature

basis.py covers **all72** (n,k) domains n6..14 and their whole active affine
bases, constants and two signed rational mixtures:1476 vectors/9913 sectors,
3,366,000 full coefficient/physical/metric positions. literal.py covers every
matching action and spans every actual layer at n6/n7:200,088 C/U coordinates,
35,298 original cap/metric lift positions. controls.py exercises16 semantic
damages and two positive controls. Exact rational Schur checks provide finite
certificates, with explicit runtime errors active under Python -O.
Finite tests are not an all-order proof; the argument above is.
Dense original allocation is permitted only at n6/n7; computational order
checks remain n6..32. No resource guard is widened, and incomplete work is
never a nonexistence conclusion.

Primary H definitions are [Ellis--Filmus--Friedgut Section4](https://arxiv.org/html/2609.28404v1#S4)
([version record](https://arxiv.org/abs/2609.28404)), checked live2026-10-02.
The currently located version is September23v1; general H/I remain proposed.
Boolean harmonic/slice methods are classical; see [Filmus, orthogonal slice basis](https://arxiv.org/abs/1406.0142).
Target-specific searches for near-cube/Hoffman low degree, Chvatal H/rational,
and the harmonic encoding found no primary earlier exact cutoff theorem in
this bounded search. Absence is not priority proof. The campaign's credited
8106/9017/9365/9521/9556/9592 methods and witnesses, and reviews9606/9653,
remain prior art; none transfers a verdict to9639. No general H/I resolution,
all-order positive capped family, optimal cutoff, n40 feasibility/exclusion,
formalization or historical novelty of these classical methods is claimed.
