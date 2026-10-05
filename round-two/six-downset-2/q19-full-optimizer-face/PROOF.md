# Full q19 sharp feasibility, Schur reduction and optimizer tube

Actual author: six-downset-2, researcher, 2026-10-05. Ordinary
computer-assisted proof, unformalized and independently unreviewed.
Actual source-only normal/optimized, adverse-input and cold reader
evidence is recorded separately in VALIDATION.json. Source publication
and actual graph commitment are separate obligations.

## Fixed carrier and statement

Let a,b,c,X,Y be disjoint, |X|=9, |Y|=10. D contains all sets of size
at most two and all triples with at least two core points, except bcX
triples. Keep the actual empty vertex and allowed loop. N=303, the
unique largest a-star S has s=61, h=N-s=242. Write B=D\(S union
{empty}), |B|=241, and Q=D\{empty,a}, |Q|=301. The carrier, exact
comparison C0, individual positive NN repair cost and complete physical
criterion are prior ACTUAL LEMMA10332/0, source58f9c6ab8b6ab58232cd275ddb4691d3430fb02f:
[proof](https://github.com/helgithorskarp/math_results/blob/58f9c6ab8b6ab58232cd275ddb4691d3430fb02f/round-two/six-downset-2/q19-sharp-star-extension/PROOF.md)
and [physical criterion](https://github.com/helgithorskarp/math_results/blob/58f9c6ab8b6ab58232cd275ddb4691d3430fb02f/round-two/six-downset-2/q19-sharp-star-extension/STRUCTURAL.md).

An original competitor is a REAL symmetric M on D with row sums1,
zero on intersecting pairs, entries at least epsilon on EVERY disjoint
pair including the empty loop, and L=61I+242M>=0. Put tau=242epsilon
>=0. The a-star Rayleigh bound forces lambda_min(M)=-61/242. At tau=0
we include the nonnegative closed relaxation; positive tau gives strict
original allowed support. No symmetry or additional upper PSD premise
is imposed on unrestricted competitors.

Set C=L_proper,proper-J. On unordered disjoint pairs e in B put
delta_e=C_e-C0_e and P=sum_e max(delta_e,0). The comparison's143 free
coefficients are29u/32768, recovered from the exact defining10278
fixture. Its bad empty/nonstar vertices K have types YY,bY,cY,bcY,
with |K|=75. KK/KG/GG mean both/exactly one/neither endpoint in K.
Write P0=8421443/65536.

We prove:

1. For EVERY REAL tau>=0, individual-real original sharp feasibility
   P=P0+38tau is equivalent to S9xS10-invariant sharp feasibility.
   The latter has180 original entry rows,25 zero KG coordinates, five
   sharp empty/loop equations, and a complete lower PSD criterion of
   physical Schur sizes13,5,6 plus three scalar forms. This is a
   reduction, not existence beyond the interval below.
2. For EVERY REAL 0<=tau<=1/8, new rational endpoint certificates and
   affine interpolation attain the unrestricted bound. Thus for ALL
   individual-real competitors and EVERY REAL epsilon in[0,1/1936],

       min P=8421443/65536+9196epsilon.

   The interpolated centers satisfy T,Bcap>=I/1024, both greatest
   original endpoint ranks302, and other301 lower/upper gaps1/247808.
3. At EACH tau in this interval the complete original optimizer set
   has affine hull E_tau of dimension24969; its invariant affine hull
   has dimension113. Its relative interior is exactly strict KK/GG
   repairs, strict nonforced allowed-entry surpluses, and T positive
   definite. The75 bad empty entries and empty loop are forced.
   The original spectral condition is retained in this classification.
4. In the35865 individual free Q-edge coordinates, if e_tau is the
   interpolated center, EVERY e in E_tau with

       ||e-e_tau||_infinity<=2^-25

   is an original sharp optimizer. Its nonforced C-unit entry surplus
   is at least3721/1048576, both comparisons are at least I/2048, both
   ranks302, and other301 gaps at least1/495616. This relative cube
   has the full24969 dimensions, with113-dimensional invariant part.

The interval and radius are sufficient bounds, not largest possible
ones. No general H/I, different count, optimal radius or global floor
maximality is asserted.

## Original kernel, complete coordinates and automatic upper PSD

For ANY original competitor put z=N1_S-s1. Intersecting S and original
support give 1_S^TM1_S=0. Stochasticity then gives

    z^TMz=-Ns^2, ||z||^2=Nsh, z^TLz=0.

PSD implies Lz=0, while L1=N1; hence L1_S=s1 and C1_S=0. The star
principal block is the FIXED singular C_SS=sI_s-J_s. All proper
diagonals of C are s-1, intersecting offdiagonals are -1. There are
exactly35865 disjoint unordered pairs in Q. Arbitrary real values on
them determine all remaining proper coefficients by

    C_a,v=-sum_(D in S\{a}) C_D,v              (v in B).       (1)

The star rows already have zero star sum, so this is the entire proper
kernel completion. Conversely every original competitor has this
unique completion. Write r_i=sum_j C_ij. Rows uniquely complete the
original empty vertex, including its actual loop, as

    L=[[1+sum_i r_i,(1-r_i)_i],[(1-r_i)_i,(1+C_ij)_ij]].      (2)

These affine identities hold for arbitrary real free coordinates.
With Psi=[-1^T;I_302], L=J+Psi C Psi^T. Psi has full column rank and
image1^perp, so L>=0 iff C>=0.

For the residual lift let r=1_(S intersect Q), b=1-r. Phi has columns
e_A-e_a on star Q and e_A-e_empty on B. The prior complete lift gives

    T=C_Q,Q, G=Phi^TPhi=I+rr^T+bb^T,
    G^-1=I-rr^T/61-bb^T/242,
    L=J+Phi T Phi^T,
    NI-L=Phi Bcap Phi^T+zz^T/(sh), Bcap=NG^-1-T.             (3)

The301 independent columns exhaust {1,z}^perp. Thus L>=0 iff T>=0.
If T,Bcap>=delta I, G>=I implies their nonzero lifted spectra are at
least delta. The remaining directions are1 and z in(3). This proves
ranks302 and other eigenvalue gaps delta/242. It is the ordinary lift
and metric proof of10332 applied to NEW witness factors.

The unrestricted upper PSD follows without adding it to feasibility:
M is nonnegative, symmetric and stochastic, so for every real v,

    v^T(I-M)v=sum_(unordered i<j)M_ij(v_i-v_j)^2>=0.         (4)

The loop contributes zero. Hence NI-L=h(I-M)>=0. When epsilon>0,
the empty edges alone give for v^T1=0

    sum_(A!=empty)(v_A-v_empty)^2=||v||^2+N v_empty^2
                                  >=||v||^2,

so each nonunit eigenvalue is at most1-epsilon. The stronger uniform
gaps in our statement come from NEW exact Bcap checks, also at tau0.

## Full-star Schur criterion

Let A=C_S,B. The kernel gives A^T1_S=0. For u in R^61,v in R^241
and u_bar=(1_S^Tu)/61, direct completion of squares yields

    (u,v)^TC(u,v)=61||u-u_bar1_S+Av/61||^2+v^TRv,
    R=C_B,B-A^TA/61.                                      (5)

Thus C>=0 iff R>=0; R positive definite gives just the star kernel.
All star coupling energy is retained. The exact checker constructs
every58081 entry of A^TA and R from the full original matrix, checks
all241 range columns and every58081 Schur identity/action position.

For invariant coordinates use the COMPLETE physical decomposition
proved in10332:22 orbit constants,8 X-standard types with8 copies,
9 Y-standard types with9 copies, and harmonic/mixed dimensions27,35,72.
The metrics are actual orbit and standard-function weights. Schur
elimination of star coordinates in the trivial block uses

    Astar=61W-ww^T, sum w=60,
    Astar^-1=(W^-1+11^T)/61.                              (6)

In each standard block Astar=61W and inverse W^-1/61. The fixed star
blocks are positive definite. Hence the lower criterion is EXACTLY the
13-dimensional trivial Schur form,5-dimensional X-standard Schur form,
6-dimensional Y-standard Schur form and three unchanged lower scalars.
Their physical dimensions exhaust B:

    13+5*8+6*9+27+35+72=241.

This census alone is not the completeness proof. The ordinary orbit,
pair-incidence and mixed rectangle decomposition and actions are the
credited10332 premise. New checks pay both entire inverse products
in(6), all full-original Schur actions and freshly computed full factor
identities in the six reduced forms. All original lower/upper physical
actions and twelve fresh shifted factors are separately paid. Schur
forms are generally quadratic in the coordinates; interval interpolation
uses the ORIGINAL affine T,Bcap, not interpolation of those Schur forms.

## All-real averaging equivalence

G0=S9xS10 permutes pools, fixing a,b,c,empty,a. It preserves D,S,K,
NN disjointness, the actual loop and C0. Average original M over the
finite conjugations. This preserves symmetry, rows, support, every
allowed floor, lower PSD and the centered-star/proper kernel identities.
There is no rationality restriction on the original M. Convexity of
x->max(x,0), permutation of all objective edges, and invariance of C0
give P(C_bar)<=P(C). The unrestricted lower bound below gives
P(C_bar)>=P0+38tau, so a sharp original matrix averages to a sharp
one. The reverse existence implication is inclusion. Averaging need
not fix each optimizer or make every optimizer invariant.

A disjoint Q-pair orbit is completely determined by both core masks
and pool cardinalities: any such two pairs are related by separate
permutations of X,Y. The literal census has exactly143 unordered
orbits, split5 KK,25 KG,34 GG and79 star. No b,c swap is imposed.
Thus all invariant matrices are the143 real free coefficients with
completion(1)-(2). For these coordinates the180 original entry rows are
143 proper pair rows,13 anchor/NN rows,22 empty/Q rows, empty/anchor
and actual loop. The explicit10332 binomial budgets count all disjoint
subsets, with intersecting core masks suppressing the corresponding
term; they cover every72817 ordered allowed original position. Along
with sharp signs/five equalities and the full lower Schur criterion,
they are necessary and sufficient for invariant sharp feasibility for
ANY tau>=0. The averaging argument makes this also an existence
criterion for individual-real sharp feasibility, not a certificate of
existence at an unconstructed larger tau.

## Unrestricted cost and full affine optimizer geometry

Let ell_v^0 be comparison empty/v budgets and e0^0 its actual loop.
Set D0=-sum_(v in K)ell_v^0 and P0=(D0-e0^0)/2. The complete mass
identity of10332 (generic method credited to10296/10306) is

    2(P-P0)=sum_(v in K)E_v+E_0
       +2sum_KK(delta_e)_+ +sum_KG|delta_e|
       +2sum_GG(-delta_e)_+.                            (7)

E_v,E_0 are the actual C-unit original entries. This identity holds
for all individual real free coordinates, with no symmetry or PSD
premise. Floors give P>=P0+38tau. Equality is EXACTLY

    E_v=tau (every75 bad v), E_0=tau,
    delta_KK<=0, delta_KG=0, delta_GG>=0.                (8)

Define E_tau by the affine part of(8) in the35865 free coordinates.
Star trades are unpenalized and cancel from bad/loop degrees by the
kernel. Actual row completion gives

    E_v-ell_v^0=-sum_(NN edges incident to v)delta_e,
    E_0-e0^0=2sum_(all NN edges)delta_e.                (9)

The literal counts are1800 KK,10820 KG,11245 GG and12000 star free
edges. KG equalities are10820 independent coordinate rows. After
deleting their columns the75 bad-degree rows form the unsigned KK
incidence matrix. The KK graph is connected and nonbipartite: YY forms
KG(10,2), any overlapping pair of its vertices has a common disjoint
YY neighbor, and Y0Y1,Y2Y3,Y4Y5 is a triangle. Each bY,cY,bcY joins
a YY pair avoiding its Y. A left-null row has y_i+y_j=0 on every edge;
the triangle forces zero there, connectivity forces all75 zero. Thus
the bad rows have rank75. The loop is an independent row because its
coefficient on a GG column is2, while every bad row has coefficient0.
Consequently

    dim E_tau=35865-10820-75-1=24969.                  (10)

chart.py checks the entire edge census, saves an actual74-edge KK
spanning tree and triangle, and checks a GG column for the loop. This
is a combinatorial real-rank proof, not a floating rank computation.

Invariant KG gives25 coordinate rows. The four bad-type degrees and
loop have rank5: the minor with columns Y/Y,YY/YY,YY/bY,YY/cY,YY/bcY
has determinant of absolute value117573120, with both whole rational
inverse products checked. Every180 scalar row generator is exact.
Thus the invariant affine dimension is143-25-5=113.

The full optimizer set is E_tau intersected with all original entry
halfspaces, sharp-sign halfspaces and T>=0; upper PSD is automatic.
It is convex. A center strict in every nonforced scalar/sign constraint
and with T positive definite has a relative open ball, proving its
affine hull is all E_tau. Its relative interior is EXACTLY these strict
conditions: sufficiency follows from finite scalar continuity and PD
openness. A zero scalar gives a proper supporting face since the center
is strict. A nonzero v with v^TTv=0 also gives a proper supporting face
since the center's quadratic value is positive. This proves necessity.
The invariant space has the identical argument in its113 dimensions.
The needed centers and uniform quantitative neighborhoods follow next.

## Fresh exact endpoints and whole real interval

CANDIDATE-TAU0.json and CANDIDATE.json give ALL143 rational values at
tau0 and tau1/8. Whole file hashes:

    tau0 e5f121f8751b8a86528d3a3eb4ca6c5736a892666aff800820f848fd8a85f93d
    tau1/8 1ee9671ebb7da1efb6d2a674c01e5e4595576acc0d18eb3cb205f59e40165cb8.

At each endpoint check.py constructs full303-square L and301-square T
in two openly reused same-author implementations, compares EVERY entry,
checks all72817 allowed floors,303 rows/support/star equations, all23865
individual NN repairs/cost, the complete301-dimensional basis/all90601
Gram positions and181202 lower/upper physical action positions. It
checks all58081 original Schur identities/actions, six new exact Schur
PD factors and twelve new full factors shifted by1/1024. Complete factor
identities and positive pivots are checked before digests. Neither search
nor rational recovery code is imported by check.py.

The endpoint nonforced entry surplus and strict KK/GG repair magnitude
minima respectively are:

    tau0: 777/131072, 6179/1048576;
    tau1/8: 327/65536, 2611/524288.

Both exceed mu=1/256. Each shifted physical factor is positive definite,
giving T,Bcap>=delta I with delta=1/1024. Costs are8421443/65536 and
8732739/65536. These are new dense witnesses; no old factor/floor is
transported. For EVERY real tau in[0,1/8] define free coordinates

    e_tau=(1-8tau)e_0+8tau e_(1/8).                  (11)

Every original entry, row, repair coordinate, sharp equation, T and
Bcap is affine. The convex coefficients in(11) preserve all equalities,
mu scalar/sign margins and delta physical bounds on the ENTIRE real
interval. Identity(7) gives unrestricted sharpness there. This ordinary
convexity argument is not a finite sampling inference. epsilon=tau/242
has endpoint1/1936, larger than the prior specified four-coordinate
template endpoint19967/55508992. Neither endpoint proves global maximality.

## Uniform full-face tube

Let v=e-e_tau be in the homogeneous tangent space of E_tau, with
||v||_infinity<=rho=2^-25. Every KG coordinate, bad-degree variation
and loop variation is zero. Each entry of DeltaT is a free coordinate
or fixed zero. The symmetric row-sum bound gives

    ||DeltaT||_op<=301rho<delta/2.                  (12)

Bcap changes by -DeltaT. Both comparisons therefore remain at least
I/2048. Original completion effects are also required. A NN empty
row has at most240 free NN terms; its star changes cancel by(1).
A free-star empty row has at most241 NN terms. A nonstar anchor entry
has at most60 free-star terms. The empty/anchor row sums the12000 star
free terms. The bad empty and loop variations vanish by E_tau. Every
other allowed proper entry changes by one free coordinate. The literal
degrees and entire counts are checked by chart.py. Hence EVERY
nonforced original entry changes by at most12000rho, giving

    mu-12000rho=3721/1048576>0.                    (13)

Each KK/GG sign stays strict by mu-rho>0. Forced entries remain exactly
tau. Thus the ENTIRE relative cube is sharp original feasible. It
contains a relative open ball in E_tau, so has all24969 dimensions;
its invariant intersection has113. Equation(3) gives ranks302 and
other gaps1/(2048*242)=1/495616. At tau>0 every allowed original entry
is strictly positive, including the forced entries.

## Dependency and trust boundary

The10332 lift and complete ordinary physical criterion are premises;
earlier interface10248 and D3 sector mechanism10242 are credited there.
Only143 exact defining integers from10278 are coefficient data. New code
openly reuses whole pinned same-author model.py/physical.py from source
7fcf6b63229f54bc65a4fac50b41590b0aa6f052, calling formula/action functions.
It does not load that source's old factors, template floor or validation.
Whole source hashes precede mathematical imports. Reuse is neither an
independent implementation nor independent review.

D3's q18 mass10296, optimizer geometry10308/source88c6c7ea0905fe51d4ecab5703a3e9cd18d3344c
and chart10326 are conceptual antecedents. Review10324 concerns q18 only.
No peer executable, numerical witness, physical floor, factor or verdict
is imported into q19. Reynolds averaging, Schur complements and relative
interior are standard tools; no priority claim is made for them. New
content is this fixed-q19 complete reduction, exact dense endpoint
extension and full optimizer geometry with the quantified tube.

At the closing refresh, R5's source-published independent all-count audit
e759ea9f03c47e463a080e4a7b8bf94fc56c585b was read in full:
[scoped review](https://github.com/helgithorskarp/math_results/blob/e759ea9f03c47e463a080e4a7b8bf94fc56c585b/round-two/six-reviewer-5/all-count-block-audit/REVIEW.md)
and [ordinary proof](https://github.com/helgithorskarp/math_results/blob/e759ea9f03c47e463a080e4a7b8bf94fc56c585b/round-two/six-reviewer-5/all-count-block-audit/PROOF.md).
It confirms10332's all-count physical criterion, proves smaller-pool
and exact spectral-window refinements, and also describes the standard
kernel/averaging existence argument. These are credited prior and
concurrent context. It explicitly excludes q19 primal witnesses,
numerical factors/gaps and sharp attainment from its verdict. It gives
no independent review of this new interval, Schur certificates, optimizer
classification or tube. No review program or certificate was opened or
executed, and no review graph commitment is asserted here. This source
attribution was added after author checks, with the mathematical code,
input witnesses and entire evidence unchanged.

The primary target remains Ellis--Filmus--Friedgut Conjecture H,
[arXiv2609.28404v1 Section4](https://arxiv.org/html/2609.28404v1#S4),
live reverified2026-10-05; general H/I remain unresolved.

Bounded FLOAT CVXPY/SCS searches only discovered candidates. Rational
recovery rounded nonpivot deltas to denominator2^20 and solved five
equality pivots EXACTLY. Solver status and recovered entry feasibility
are not spectral proof; the fresh entire rational checks establish the
endpoint facts. Ordinary averaging, completeness, rank and real interval
bridges above remain unformalized. The private endpoint/chart evidence
and new source-only normal/optimized/adverse/cold completion are recorded
separately in PROVENANCE.json and VALIDATION.json; neither is independent
review. Source delivery and actual graph commitment are distinct. Timeout,
interruption, UNKNOWN and resource kills prove no mathematical absence.
