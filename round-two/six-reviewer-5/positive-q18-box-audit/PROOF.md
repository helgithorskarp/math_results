# Independent q18 certificate audit and a larger full real box

Actual **six-reviewer-5 / independent mathematical reviewer**, 2026-10-04.
The following is complete ordinary mathematics plus a finite exact certificate
reader, **UNFORMALIZED**. Input coefficients and factors are credited to
six-downset-3, LEMMA10286, source
8b4fb203c18b6ae9e2775fabf93e8579a0d68622. They are explicitly exposed
mathematical DATA, not an independently generated witness. All mathematical
reductions, original matrices, physical norms, actions, residuals and real-box
budgets below are independently reconstructed by the accompanying reader.

## Carrier, original matrices and stated finite scope

Label a,b,c by bits0,1,2, Z by bits3..11 and W by bits12..20. Both pools have
nine points. Enumerate and sort the integer bitmasks of

\[
 D=\{A:|A|\leq2\}\cup\{A:|A|=3,\ |A\cap\{a,b,c\}|\geq2\}
       \setminus\{\{b,c,z\}:z\in Z\}.
\]

Deletion applies to the union. Every subset deletion is checked. There are
278 members, including the actual empty vertex and its allowed loop. Stars
have sizes58,49,49,nine23,nine24; S, containing a, is the unique maximum.
Write h for its indicator on the277 proper members. The ground order and
sorted bitmask order fix every coefficient and original-coordinate position.

Let d=1048576. CERTIFICATE.json gives all143 integer values for unordered
orbit keys of disjoint nonanchor proper pairs, with type
\(o(A)=(A\cap\{a,b,c\},|A\cap Z|,|A\cap W|)\), encoded by the core bitmask.
Define C diagonal57, distinct intersecting entries-1 and those free entries
as numerator/d. For nonstar A uniquely recover its anchor entry by
\(C_{A,a}=-\sum_{B\in S\setminus\{a\}}C_{A,B}\).
All keys are used and all rows of Ch=0 are checked. The star block is58I-J.

With E=[-1^T;I277] define

\[
 U=278I_{277}-J_{277}-C,\quad L=J_{278}+ECE^T,\quad M=(L-58I)/220.
\]

The reader independently checks **all** original positions: symmetry,
support, row sums, centered-star kernel and278I-L=EUE^T. In particular

\[
 L_{0,A}=1-\sum_B C_{A,B},\qquad L_{0,0}=1+\sum_{A,B}C_{A,B}.
\]

The empty loop is retained. All60,597 allowed ordered entries of M are
positive. Their point minimum is17433/20971520, and M00=653267/10485760.

## Complete physical span and both endpoint certificates

The reader builds277 sparse integer vectors of dimensions
23+64+72+27+27+64. The23 TT vectors are the complete orbit indicators.
For Z, eight types carrying Z give eight independent copies of the
zero-sum point functions e0-ej, j=1..8; W has nine such types. Each type's
full copy Gram is a positive multiple of I8+J8. All76,729 frame Gram
positions check cross-sector orthogonality and these actual metrics.

For a nine-point pool, the unsigned point/pair incidence map has rank9:
a row dependence r_i+r_j=0 on every pair forces all r_i=0. Its kernel
therefore has dimension36-9=27. Our explicit kernel vectors choose each
pair (i,j) on1..8 except(1,2) as a free pivot2, put-2 on(1,2), and put
-2*1_{t in(i,j)}+2*1_{t in(1,2)} on(0,t). Every incidence sum is zero;
the27 distinct pivots prove independence. This pays both ZZ and WW.
The64 mixed rectangles (e0-ei) tensor(e0-ej), i,j=1..8, have64 distinct
pivots. Cross-sector orthogonality and the complete dimension count prove
that the frame spans the full proper space; a representation label alone
is not used as a completeness proof.

For C and U separately, all153,458 original-coordinate action positions
check every direction against the fresh prototype action. TT has its full
23-column action; standards have their complete type action in every copy;
the pair and mixed kernels have their actual scalar action. This both proves
invariance and rules out an omitted cross-sector coupling. All six pair/mixed
prototype norms are4. The standard prototypes e0-e1 have norm m_i; their
full energies and norms are the same prototype forms tensored with
(I8+J8)/2. Since this tensor factor is positive definite, a prototype floor
relative to diag(m_i) proves the same physical floor on all copies.

For each of the six non-scalar blocks, let G be the independently computed
Gram and V the supplied triangular integer factor over Q=2^32. Compute
F=G-VV^T/Q^2 entry by entry. The reader proves, before comparing any supplied
margin, that each diagonal-dominance margin is at least m_i/32. For any real y,

\[
 y^TFy\geq\sum_i(F_{ii}-\sum_{j\ne i}|F_{ij}|)y_i^2
          \geq\tfrac1{32}\sum_i m_i y_i^2.
\]

This follows from2|y_i y_j|<=y_i^2+y_j^2; VV^T is PSD regardless of how
V was proposed. Each of the six scalar Grams independently gives its
norm4 floor1/32. The full regenerated record contains every fresh Gram,
physical norm and residual margin. Author compiled margins/hashes are
not positivity premises.

The lower TT block is restricted by deleting the anchor coordinate. This
is a physical section, not an orthonormal quotient. For any TT x perpendicular
to h, y=x-x_a h has anchor coordinate0, x^TCx=y^TCy and
||y||^2=||x||^2+x_a^2||h||^2>=||x||^2. Hence the proved section bound pays
C on h-perp. The independent action and Ch checks establish its only kernel.
Combining the complete sectors proves

\[
 C|_{h^\perp}\succeq I/32,\qquad U\succeq I/32.
\]

Because E^TE=I+J>=I, congruence transfers these nonzero spectral floors:
the positive eigenvalues of ECE^T equal those of C^{1/2}E^TEC^{1/2},
which dominates C; EUE^T is treated the same way. The J summand of L
acts only on1 and has eigenvalue278. Thus L and278I-L each have rank277;
L has the simple centered-star kernel and278I-L the simple constant kernel.
The least M eigenvalue is exactly-29/110 and the greatest exactly1, both
simple. The point lower spectral gap is at least1/7040.

There is also a direct upper gap bound. With any allowed entry floor w>0,
I-M is the weighted Laplacian of the nonnegative offdiagonal M entries.
It dominates w times the empty-centered unit star Laplacian, whose positive
spectrum is1 (276 times) and278. Hence every nonconstant M eigenvalue is
at most1-w. At the point we may take w=17433/20971520.

## Every independent real repair coordinate, and the stronger radius

A symmetric support-preserving proper repair R has zero diagonal and zero
star/star entries. The additional equation Rh=0 forces each nonstar anchor
entry from its other star entries. Consequently the entire affine repair
space has exactly29,802 independent **real** coordinates:19,522 nonstar/
nonstar unit edges and10,280 anchored trades
edge(A,B)-edge(A,a), where A is nonstar and B is a disjoint nonanchor star.
Distinct nonanchor entries are a left inverse, proving independence and
surjectivity. The reader constructs each sparse generator and its literal
E R E^T, checks every supported row and position, and derives every actual
entry coefficient l1 budget, including the empty loop. No orbit symmetry
or rationality is assumed for perturbations.

Let k_A count the disjoint nonanchor star entries for a nonstar A. Independent
literal enumeration gives k=17,18,35,37,51,54 with multiplicities9,1,36,2,153,18,
respectively. Thus sum k=10280 and sum k^2=500204. If every independent
coordinate has absolute value<=epsilon, each nonanchor entry of R is bounded
by epsilon and each anchor entry by k_A epsilon. Therefore

\[
 \|R\|_{op}\leq\|R\|_F\leq\sqrt{2(29802+500204)}\,\epsilon
       =\sqrt{1060012}\,\epsilon<1030\,\epsilon.
\]

The Frobenius envelope itself is attained when all independent coordinates
are positive; no optimal operator norm or maximal PSD box is claimed.
Set **epsilon=1/65920=1/(64*1030)**. Since Rh=0, both endpoint proper floors
remain at least1/32-1/64=1/64 for **all** independent real coordinates in
this closed box. Ranks and simple kernels persist. The actual lower M
gap remains at least1/14080.

For every original allowed position (i,j), use its separately computed
literal l1 budget B_ij to prove

\[
 M_{ij}(t)\geq M_{ij}(0)-\epsilon B_{ij}/220.
\]

All60,597 inequalities pass, including loop budget39044 and anchor-empty
budget10280. The smallest interval endpoint is
**w_box=97291577/118803660800>1/2048**, at position(0,105), budget179.
Thus every allowed entry of every matrix in the real box exceeds1/2048,
and its upper gap is at least w_box. These are real interval bounds,
not sampled points or an inference from finitely many parameter choices.

This radius improves the published1/3814656 by the exact factor
29802/515 (about57.868), while retaining the stated entry floor and
both endpoint ranks. The reader also checks every published-radius
entry bound. The improvement is in the full29,802-coordinate box,
not just the143-variable symmetric subspace.

## Signed-center comparison and necessary mass cut

COMPARISON.json contains the old143 values over16384. Their entire values
and orbit order were independently bound to LEMMA10276's published
CERTIFICATE.json at source2bd233ac02ac1c4fc162e7fb4a9a5be8930882d9.
Old factors/margins were exposed as data but are not a PSD premise.
The old literal matrices and every row/loop are freshly reconstructed.
There are81 bad nonstar empty incidences (36 ZZ,36 WW,nine bcW), but82
bad incidences in total: the additional abc star incidence must not be
silently included in the nonstar budget. The negative nonstar deficit is
d=2497887/16384 in C units, and old loop capacity ell=2021552/16384.

For arbitrary real supported star-preserving changes, let P and T be total
positive and negative unordered NN changes in C units. Anchored trades
leave each nonstar proper row sum unchanged. Nonnegative empty incidences
require at least d net row decrease on the81 bad vertices. A unit of
negative NN mass pays at most two of these deficits, so T>=d/2. The
empty loop changes by2(P-T); its nonnegativity forces P>=T-ell/2. Hence

\[
 P\geq(d-ell)/2=476335/32768>0.
\]

Any H matrix on this carrier also lies on the stated star face: the
centered star vector f=278*1_S-58*1 has f^TLf=0 by the58I star block,
L1=278*1 and |S|=58; PSD implies Lf=0 and hence Ch=0. This justifies
the necessary cut beyond symmetric recipes. This paragraph proves a
necessary capacity inequality, not an optimality or PSD-sufficiency result.

At the new dense point, all19,522 NN changes are accounted for:9919
increase,9603 decrease,none unchanged. P=802154061/262144,
T=3266119971/1048576 and2(P-T)=-57503727/524288. The entire original
loop identity agrees with M00=653267/10485760. The later sharp mass,
equality face and sparse primal of LEMMA10296 are separate published
mathematics, cited as context and independently unreviewed here.
