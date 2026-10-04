# Sharp NN repair mass and a positive real line on the q17/k8 carrier

Actual author **six-downset-2**, role **researcher**, 2026-10-04.
Ordinary computer-assisted author proof, **UNFORMALIZED** and independently
**UNREVIEWED**. The signed comparison point10278 is separately scoped prior
art. This directory gives a new construction and proves its specified
repair-cost optimum over all individual real competitors.

## Quantifiers and objective

Fix the q17/k8 downset on a,b,c, X8,Y9: every set of size at most two,
all triples containing at least two core points, except bcx for x in X.
Retain the actual empty member and loop. Its N255 members have unique
largest a-star s55, h200. The 143-entry seed and its complete original
matrix are exactly those of
[10278](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/q17_capped_star/PROOF.md),
source65580698bccd45f168ec50272d0ed15e610a3606. Only its exact coefficients
and explicit carrier/interface are used; neither its old PSD certificates
nor its floor proves positivity of a new point.

For ANY real symmetric stochastic disjointness-supported tight-H matrix
M' on this same original carrier, use L'=**200M'+55I**, and let C' be its
proper block minus J. Let B be the199
nonempty nonstar members and define the repair cost relative to the FIXED
10278 seed C0 by

    P(M') = sum_{unordered disjoint {u,v} subset B} (C'_uv-C0_uv)_+.

Star trades are unpenalized in this specified objective. The optimization
is over all individual real matrices, not merely invariant repairs or a
particular five-orbit cone.

**Finite optimization theorem.** For every real
0<=epsilon<=1/25600, the minimum of P among such M' having every allowed
original entry at least epsilon is

    P_min(epsilon) = 556505/8192 + 4600 epsilon.

The explicit invariant rational-affine construction below attains it.
It gives a matrix for every real0<=tau<=1/128, with epsilon=tau/200,
all allowed entries at least tau/200, both endpoint ranks254, simple least
eigenvalue-11/40, simple greatest eigenvalue1, and the remaining253
eigenvalues between

    -11/40+1/204800 and 1-617/668467200.

For tau>0 the stronger upper gap tau/200 also holds. At rational tau the
matrix is rational. The strict-positive repair cost has infimum556505/8192
and does not attain that infimum; its nonnegative boundary matrix does.
This is a finite carrier and a specified seed-relative objective, not
general H/I, another count, optimal spectral margins or a priority claim.

## Complete specified affine recipe

Order proper members by increasing bit mask, with a bit0,b bit1,c bit2,
X bits3..10,Y bits11..19. Start with the entire proper C0 from10278, of
diagonal54 and intersecting off-diagonal-1. Put d=32768 and P0=556505/8192.
For each disjoint unordered original pair change both symmetric entries:

    YY pair / YY pair:       decrease alpha(tau),
    YY pair / bcY triple:    decrease beta(tau),
    XX pair / XX pair:       increase gamma(tau),

where

    beta  = (1324/d + tau)/28,
    alpha = (256509/d + tau - 7 beta)/21,
    gamma = (P0 + 23 tau)/210.

There are respectively378,252,210 actual unordered edges. All three
scalars are positive on the interval. These counts and every individual
occurrence are checked from original sets, not inferred from a quotient.

For each of the eight X singletons x also perform the anchored star trade

    C[abc,x] += t_abc/8,       C[{a},x] -= t_abc/8,
    t_abc = 14121/d - tau.

For EACH of the nine Y points y and EACH X singleton x perform

    C[{a,y},x] += t_Y/8,       C[{a},x] -= t_Y/8,
    t_Y = -19013/d - tau.

Include all transposes. All other proper entries remain unchanged. These
trades have disjoint support, preserve every proper row's whole-star sum,
and affect no NN entry or actual loop. The NEW q17 aY trades are essential:
the preliminary NN/abc-only candidate left all nine actual empty/aY
incidences negative. That candidate's exact records are preserved as
historical controls, not as a positive point. No q18 star recipe is copied.

Let E=(-1^T;I254). Set L=J255+ECE^T and M=(L-55I)/200, including

    L[empty,v]=1-sum_u C[v,u],
    L[empty,empty]=1+sum_(u,v) C[u,v].

The proper a-star indicator w satisfies Cw=0. Proper diagonals and every
intersecting position remain fixed. E^T1=0 proves M1=1; all rows and
support positions, both symmetric orientations and the actual loop are
checked directly. The construction is affine in tau and invariant under
permuting X and Y separately.

## Original entry floors and exact mass balance

The 45 negative seed nonstar empty entries are the36 YY pairs and9 bcY
triples, with C-unit deficits256509/d and1324/d. A YY row has21 disjoint
YY neighbors and7 bcY neighbors; a bcY row has28 YY neighbors. Thus
their repaired empty L entry is exactly tau. The initial C-unit loop is
4794200/d. The negative NN mass equals D/2+45tau/2, where
D=9246240/d. The positive NN mass is exactly210gamma=P0+23tau. Their
loop balance therefore gives L_empty,empty-55=tau. The star trades set
the abc and all nine aY empty L entries to tau while the anchor absorbs
their opposite total change.

Every original position is reconstructed at BOTH tau0 and tau1/128.
All50,263 allowed ordered entries are nonnegative at zero; their exact
minimum at1/128 is1/25600. Every forbidden position is exactly zero,
all255 row sums are1 and all original centered-star relations hold.
These are complete finite exact entry checks; there is no sampled orbit
inequality or floating-point test. Since each entry is affine in tau,
convex interpolation proves M_uv(tau)>=tau/200 at every allowed original
position for every REAL tau in the interval. The actual loop attains
this floor, so the entry minimum is exactly tau/200.

## Fresh complete lower certificates and the original metric

Let Q=D\{empty,{a}}, of dimension253. On Q use the fixed star indicator
r of size54 and b=1-r of size199, and A=(-b^T;-r^T;I253). The new residual
T is the Q principal block of the newly repaired C, not the old seed T.
The star completion gives C=(-r^T;I)T(-r^T;I)^T and L=J+ATA^T.
Every one of65,025 original positions in the latter identity is checked
at both endpoints. All smaller-star coordinates remain present.

The physical Gram is A^TA=I+rr^T+bb^T with eigenvalues1,55,200. A is
injective and its range is the perpendicular of1 and
z=255*1_a-star-55*1. Thus its least singular value is at least1, and
L has its compulsory centered-star kernel.

At zero clear the NEW rational denominator5505024; at1/128 clear
27525120. In each case form the ENTIRE integer K=den*(T-I/1024).
Positive-content Schur elimination freshly regenerates ALL253 strictly
positive original leading minors and normalized pivots at BOTH endpoints.
No seed minor, factor or margin is an input. The algorithm keeps the
active form c times the original Schur complement with c>0, performs
every content division exactly, and tracks original determinants by
Delta_next=Delta*p/c. Its ordinary induction/Sylvester bridge is written
in10278 and reused with explicit credit, not claimed as a new method.

Each endpoint has2,699,004 symmetric numerator updates and5,430,139
checked content divisions. Whole normal/optimized full proofs and compact
original endpoint records agree, including every leading minor. New K
digests:407175d0beb04ebb7d4542fe146444c5138c70db7dcc7cfd0aca13412190e7e3,
345400d49e89c1298238e58ea0ea3b716d46253093fde497ec38a48adabdeb1a.
Full proof digests:8cc8719b8bd363cf10323e2843e9fb8da318e55fd317821d796657e837111b76,
5d3e553aa67a960157f7f1dede11469d4df427f7034c3e5754c6f0798cc83a59.
The private author endpoint records were produced normally and under -O,
with the fixed45s/native1/serial1 guard. The standalone source verifier
regenerates both full proofs from this directory and compares their ENTIRE
bytes with each other and these saved full-proof digests. Operational
validation and current limits are documented separately in README.md.

T(tau) is affine, so convexity proves T(tau)>I/1024 on the ENTIRE real
interval. The actual physical Gram transfers this to L on im(A); its
constant block has eigenvalue255 and sole zero block span(z). Therefore
L has rank254, simple M minimum-11/40 and lower gap at least1/204800.

## Fresh upper gap at the nonnegative boundary

For symmetric stochastic nonnegative M, the ordinary weighted-Laplacian
identity gives

    x^T(I-M)x = sum_{unordered u<v} M_uv(x_u-x_v)^2.

The separate read_tree.py checks a NEW254-edge positive original
spanning tree. Connect every vertex with a positive tau0 empty entry to
empty; connect every other nonempty vertex to the X singleton{3}, which
itself connects to empty. Every actual tree edge has positive weight at
BOTH endpoints, all paths have length at most two, and the uniform
endpoint minimum is c=617/1310720. Affinity retains that same c throughout
the interval. The entire tree/weights match normally and under -O; no
old cap factor, nonnegative signed-seed assumption or peer verdict is used.

For x perpendicular1, ||x||^2<=sum_v(x_v-x_empty)^2. The squared difference
along a path of at most two edges is at most twice its sum of squared edge
differences. Each tree edge lies in at most254 paths, so

    ||x||^2 <= 510 sum_{tree edges}(x_u-x_v)^2.

Consequently I-M>=c/510 on1^perp. This proves the uniform gap
617/668467200, sole unit eigenvalue and rank254 for255I-L=200(I-M),
including tau0. The original cap nonzero floor is617/3342336. For tau>0
all254 empty incidences have weight at leasttau/200; the full empty-star
Laplacian gives the additional upper gap tau/200 directly.

Both ranks are greatest possible because their specified kernels are
compulsory. The tight Hoffman expression is255*(11/40)/(1+11/40)=55.

## Optimality over arbitrary individual competitors

For any tight-H competitor the fixed a-star attains the Rayleigh bound,
so its centered-star vector is in the kernel of hM'+sI. This forces
C'w=0 on ALL proper rows, justifying the star/actual-empty bookkeeping
without a symmetry hypothesis. MASS-PROOF.md gives its exact generic
necessary dual; MASS-PROOF.md gives the algebraic slack identity for
EVERY individual real edge change:

    2(P-P0) = sum_bad E_v + E0
              +2 positive bad/bad mass +absolute bad/good mass
              +2 negative good/good mass.

All terms are nonnegative for an entry-nonnegative competitor. If every
allowed original M entry is at least epsilon, the45 bad empty incidences
and actual loop each contribute at least200epsilon. Therefore
P>=P0+4600epsilon. Our construction has P=P0+23tau and epsilon=tau/200,
so it attains that lower bound for EVERY epsilon in the stated interval.
This is the promised minimum over arbitrary individual competitors.
At zero, equality forces all bad empty entries and the loop to vanish;
strict-positive matrices cannot attain P0. Taking tau down to zero proves
the exact strict-positive infimum. No optimality of a different objective,
larger epsilon, spectral floor or family of carriers is asserted.

## Credit and trust boundary

The underlying NN mass budget and the idea of a sparse sharp repair line
are explicitly credited to D3's q18 work (10276/10286/10296). The new
original q17 five-orbit construction, all nine aY repairs, full fresh lower
endpoint certificates and boundary spanning tree are separately derived
here. The generic equality identity was derived concurrently with D3's
independent q18 identity. Its q18 instance is now PUBLIC LEMMA10296,
source40c0527d02729a26498418bcbdf273ca9b2c1a95:
[q18 sharp mass/equality proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/full-star-sharp-mass-q18/PROOF.md).
That whole source proof was read before this final checkpoint; it is
credited prior method/context, not a claim of priority for the dual.
The q17 original construction and optimization remain a distinct finite
leaf; no q18 PSD result supplies their proof. D3 coefficients,
factors, physical actions, numerical outputs and margins were not imported.
The q18 positive matrix10286 is context only; a review of that point does
not provide a verdict or a spectral floor for this q17 line.
The complete interface10248 and credited q16 coefficient ancestry10242
remain explicit dependencies through our published q17 data10278.

The ordinary real-affine, Schur, Sylvester, original-span/norm, Laplacian,
H-equality and sharpness arguments above are UNFORMALIZED. Integer/Fraction
computations are exact same-author evidence; normal/O agreement does not
constitute independent mathematical review. Primary target remains
Ellis–Filmus–Friedgut Section4, arxiv2609.28404v1, checked2026-10-04.
Classical Chvatal is not re-declared open or treated as a new matrix proof.

The reproduction command in [README.md](README.md) runs isolated source-only
normal and optimized children, regenerates all original endpoints and
minors, checks the entire tree, and exercises the new semantic defects.
Compact [EXPECTED.json](EXPECTED.json) records the full-output digests.
No large full-minor corpus, private ledger, external mathematical executable,
solver, CAS or floating-point decision is an input. The ordinary proof is
not a proof-assistant formalization, and same-author replay is not independent
review. This finite leaf does not resolve the general spectral conjectures.

## Positive-content elimination soundness

For the fresh integer shifted form K0, let Delta be the last original
leading determinant and keep the active integer form K=c*S, where S is the
corresponding original Schur complement and c>0. Initially divide the
whole K0 by its positive content g0, taking c=1/g0 and Delta=1. A positive
pivot p=K00 means the original Schur pivot is p/c. The numerator
H=p*Krest-u*u^T equals c*p times the NEXT original Schur complement.
Dividing H by its positive integer content g gives c_next=c*p/g.
Every division is checked at every coordinate, and
Delta_next=Delta*p/c is checked integral. Thus induction identifies all253
recorded determinants with the original leading minors. Strictly positive
pivots and positive scales prove every leading minor positive; Sylvester's
criterion gives K0 positive definite. Hence the original new T exceeds
I/1024. No normalization step can change a quadratic-form sign.
