# Exact q18 subset radius and full star-to-bad transport threshold

Actual **six-downset-3 / researcher**, 2026-10-05. This is a **private,
ordinary author-complete proof, unformalized and independently unreviewed**.
New source/isolated cold publication gates have not been paid. Exact
certificate reproduction and rejection controls are separate evidence.

## Fixed original domain and credited premises

Use only the published q18 carrier and witness of
[source 782bc](https://github.com/helgithorskarp/math_results/blob/782bc9042896c0f3887b1807dbd991f75fa13c9b/round-two/six-downset-3/q18-ns-fiber-obstruction/PROOF.md),
with the explicitly credited decoder and coupled Schur/radius theorem in
[source 87c1](https://github.com/helgithorskarp/math_results/blob/87c1eba73573ab49ed9131f6496c6703ce03fd1e/round-two/six-downset-3/q18-schur-weight-radius/COUPLED-PROOF.md).
The ground is {a,b,c} union Z union W, |Z|=|W|=9. The downset contains
all sets of size at most two and all triples with at least two core
points, except bcZ. The actual empty vertex and its loop are retained.
N=278; the unique maximum proper star S=S(a) has s=58; the family B
consists of 36 ZZ pairs, 36 WW pairs, and nine bcW triples.

For each real tau in [0,1/256], F_tau consists of ALL original real
symmetric, disjoint-supported stochastic matrices M such that

    L=220M+58I is positive semidefinite,
    M_AB >= tau/220 on every allowed entry, including the empty loop.

There is no invariant, rational or rank restriction on competitors.
For the 277 proper vertices set C=L_proper-J277. The credited original
star-forcing theorem gives C positive semidefinite, C1_S=0 and
C_SS=58I-J58. Intersecting proper entries of C equal -1. Set

    v(M)=C_SB 1_B,
    d(M)=max_{s in S,A in B}|M_sA-M_dagger,sA|.

Thus sum_S v(M)=0 and every change in an S/B C entry is 220 times
the change in the corresponding ORIGINAL M entry. The fixed rational
witness M_dagger is feasible throughout the tau interval by its
published ordinary feasibility theorem, treated explicitly as a
premise. Its original PSD factor/program is not imported or replayed.

The sharp cost theorem at graph10296, its complete parent review10312,
and the fixed comparison theorem10276 are credited inputs. With
P0=476335/32768 and P the same unordered disjoint NN positive-increment
cost, put Delta=P-P0-41tau. The published all-real Schur/dual estimate is

    Delta(M) >= (||v(M)||^2/58-cap)_+/2,
    cap=4998177/1024.                                      (1)

The parent review does not transfer to the witness or this successor.
The witness source is public; its graph broadcast remains accepted
without observed commitment. The combined87c1 source is public with an
unsigned/unsubmitted graph draft held on that dependency. This new
result has no public source commit or graph submission.

The complete original-entry decoder in census.py is openly adapted
from this author's87c1 recipe. It reads only whole SHA256-pinned
CANDIDATE.json as defining DATA, reconstructs all277 masks and143 free
orbit keys, and checks all81 original S/B column kernels. No parent
producer, EXPECTED record, PSD factor or peer executable/data is loaded.

All58 coordinates of v_dagger=v(M_dagger) are nonzero. Its positive
set P consists of a, abc, nine aZ and nine aW; its negative set N
consists of ab, ac, nine each of abZ,acZ,abW,acW. These remain fixed
groups; no sign restriction on the coordinates of v(M) is imposed.
Let J=P minus {abc}, so |J|=19, |N|=38, and set

    alpha=v_dagger,abc=148830682779/1073741824,
    V=sum_P v_dagger=2912214312567/1073741824.       (2)

## The proposed positive-entry floor clipping is inactive here

There are exactly1296 disjoint original P/pure-pair positions. For
each such position let m=C_dagger,sA+1. Its eight exact margin levels
and original multiplicities are

| m | count |
|---|---:|
|9662602243/4294967296|324|
|12355403917/4294967296|252|
|6378710269/2147483648|324|
|6540952253/2147483648|36|
|3272641101/1073741824|36|
|3274036067/1073741824|36|
|13109854543/4294967296|36|
|8137812173/2147483648|252|

The minimum is the first listed level. For all real tau in [0,1/256],

    (min m-tau)/220 >= 9645825027/944892805120 > 1/100 > 1/320.

Consequently, for every real e in [0,1/320], every proposed clipped
decrease min(220e,m-tau) equals 220e. This is an exact failure to improve
the previous positive-group envelope on this whole window. It says
nothing about nonexistence of Hoffman matrices. The full census output
stays in scratch; the eight levels are a compact classification.

## An original-column subset gives a stricter necessary curve

Every vertex of N and abc intersects every bcW triple. Thus ALL351
entries on (N union {abc}) times {bcW} are fixed at -1 for every
feasible M. Each individual column kernel therefore gives

    sum_{s in J} C_s,bcw=39, for each of the nine w in W.     (3)

Only1224 disjoint J/pure-pair entries change sum_J v; their total
possible decrease is 220*1224e=269280e. All72 abc/pure-pair positions
are disjoint, while all its bcW entries are fixed. Hence, whenever
d(M)<=e, for EVERY real e>=0,

    z:=v_abc(M) >= a(e):=alpha-15840e,
    y:=sum_J v(M) >= b(e):=V-alpha-269280e.          (4)

Here 1224=72+18*64, and72 is the exact abc count. The new checker
checks every original support position, all351 fixed positions and
all nine separate column sums39, rather than relying on an averaged
column. In particular T=a+b=V-285120e recovers the older group bound.

Both a and b are strictly positive throughout [0,1/320]: their slopes
are negative and their exact values at1/320 are positive. Cauchy on
the fixed groups {abc}, J, N, together with sum_S v=0, gives

    ||v||^2 >= z^2+y^2/19+(z+y)^2/38.              (5)

For z>=a>0 and y>=b>0 the right side is strictly increasing in each
variable. Its partial derivatives are 2z+2(z+y)/38 and
2y/19+2(z+y)/38, respectively, and both are positive. Thus define

    E(e)=a(e)^2+b(e)^2/19+(a(e)+b(e))^2/38,
    Gamma(e)=(E(e)/58-cap)/2.                       (6)

Equations (1),(4),(5) prove

    Delta(M)>=max(0,Gamma(e))                       (7)

for EVERY real tau in [0,1/256], EVERY real e in [0,1/320], and EVERY
individual-real M in F_tau with d(M)<=e. No new vector sign assumption,
symmetry restriction or numerical optimization is used in this bound.

The exact polynomial is

    Gamma(e)=12192398885089082532395943/5082077992306981470208
             -9406885144672125/9244246016 *e
             +29481408000/551 *e^2.                (8)

The negative derivative at1/320 and positive quadratic coefficient,
checked exactly, imply a strictly negative derivative throughout
[0,1/320]. Gamma is therefore strictly decreasing there.

For the previous Psi(e)=((V-285120e)^2/760-cap)/2 the exact identity is

    Gamma(e)-Psi(e)=(20a(e)-T(e))^2/44080,
    20a(e)-T(e)=64399343013/1073741824-31680e.       (9)

The latter is strictly negative at1/500 and decreases thereafter.
The refinement is therefore strict for every real e in
[1/500,1/320]. It is small numerically; no general H/I advance or
priority claim is inferred from this one-witness improvement.

## All58 boxes and the exact smaller root

Let k_s=220 times the number of B vertices disjoint from the original
star vertex s. The complete support counts are 81 on a, 73 on nine
aZ, 72 on ab,ac,abc and nine aW, and64 on the36 abZ/acZ/abW/acW.
For ANY real e>=0 consider the specified relaxation R_e:

    |q_s-v_dagger,s|<=k_s e for ALL58 original s,
    sum_S q_s=0, q_abc>=a(e), sum_J q_s>=b(e),
    ||q||^2<=58cap.                                (10)

For every real e in [1/500,1/320] the unique minimum-energy vector
in the boxes and linear constraints is

    q_abc(e)=a(e),
    q_s(e)=b(e)/19, for s in J,
    q_s(e)=-(a(e)+b(e))/38, for s in N.             (11)

It has zero sum and energy E(e). ALL58 lower and upper box conditions
are checked at BOTH endpoints,116 exact original-coordinate checks.
Each slack is affine in e, so nonnegative endpoint slacks prove every
box for EVERY real e in the whole window. Inequality (5) proves
optimality; strict monotonicity in (4) and equality in each Cauchy
inequality prove uniqueness. This is an ordinary interval bridge,
not an inference from samples.

Define r_* as the smaller root of Gamma. A positive multiple of Gamma
has these primitive integer coefficients in increasing degree:

    c0=1354710987232120281377327,
    c1=-574609977651128967364608000,
    c2=30213110461589631371575296000.

Its discriminant c1^2-4c0c2 is positive and nonsquare, checked exactly
as integers. The signs Gamma(1/363)>0 and Gamma(1/362)<0, together
with strict decrease, identify

    r_*=(-c1-sqrt(c1^2-4c0c2))/(2c2),
    2757398/10^9 < r_* < 2757399/10^9,
    1/363 < r_* < 1/362.                           (12)

For0<=e<r_* the lower energy bound exceeds58cap, so R_e is empty.
At r_* vector(11) is feasible with norm squared58cap. For ALL e>=r_*
the SAME q(r_*) stays in the enlarged boxes; both decreasing lower
group bounds remain satisfied. Hence R_e is feasible iff e>=r_*,
for ALL real e>=0. Every original sharp optimizer necessarily obeys
d(M)>=r_* for every tau in the stated interval.

The old root r_c=(V-sqrt(474826815/128))/285120 has exact grid cage
2757375/10^9 < r_c <2757376/10^9. At the rational separator

    e_sep=2757387/10^9,
    Psi(e_sep)=-2314196308554620818154398505199/
                       267401227875123200000000000000000 <0,
    Gamma(e_sep)=1294923559419946699679138888187/
                       155092712167571456000000000000000 >0.

Thus r_c<e_sep<r_* and every sharp original optimizer has d(M)>e_sep.
The threshold improvement is exact, without a floating root estimate.

## Complete classification of the full original S/B transport relaxation

For ALL real e>=0 and tau in [0,1/256], define T_{e,tau} as the set
of real rectangular matrices A indexed by the ORIGINAL58 S rows and
ORIGINAL81 B columns, with

    A_sB=-1 when s intersects B,
    A_sB>=tau-1 on ALL3906 disjoint entries,
    |A_sB-C_dagger,sB|<=220e on EVERY original entry,
    sum_s A_sB=0 for EACH of the81 individual B columns,
    ||A1_B||^2<=58cap.                              (13)

All792 intersecting entries are fixed. This relaxation imposes every
original S/B support entry, floor, radius and individual column kernel,
as well as the aggregate energy ball. It does not impose global
stochastic equations, a C_BB block, or positive semidefiniteness of
the completed original matrix. Every sharp original optimizer maps
into (13).

The new transport construction produces exact endpoint matrices
A^0,A^1 at e0=1/363,e1=1/362 and tau_max=1/256, with row sums
q(e0),q(e1) from(11). It uses a deterministic integer network flow on
ten original row types and three original column types. Its compact
23-type recipes are defining certificates in TRANSPORT.json. The
construction is followed by a separate literal checker which does
not import or execute the flow algorithm. The shared original DATA
decoder is explicitly acknowledged; this is not independent review.

For EACH endpoint, the literal checker reconstructs EVERY58*81=4698
original entries from the recipe, pays ALL3906 displacement and floor
conditions, ALL792 fixed intersecting entries, ALL58 row equations and
ALL81 individual column equations. It also checks all23 original cell
multiplicities and the exact58-coordinate energy identity. Its minimum
floor slacks at the two endpoints, in increasing radius order, are

    257698037837/1700807049216 >0,
    4252017624307/27986006900736 >0.                (14)

The maximum absolute allowed C displacement is220e at each endpoint.
The endpoint matrices are transport/target certificates; the first
has energy above58cap and is NOT claimed to belong to T_{e0,tau}.

For an arbitrary real e in [e0,e1], put theta=(e-e0)/(e1-e0) and

    A(e)=(1-theta)A^0+theta A^1.                    (15)

This is an explicit original matrix recipe for all real e. Each fixed
intersection and individual column sum is preserved by linearity.
Every allowed floor is preserved by convexity, at tau_max and hence
at every tau<=tau_max. The triangle inequality gives, entry by entry,

    |A(e)-C_dagger| <= (1-theta)220e0+theta220e1=220e.

All58 row sums equal (1-theta)q(e0)+theta q(e1)=q(e), because q(e)
is affine. Consequently the original transported aggregate energy is
exactly E(e) throughout this whole real interval. The construction
does not rely on a permutation averaging bridge or a solver optimum.

At e=r_* the explicit matrix A(r_*) satisfies all of(13), with energy
exactly58cap, for EVERY tau in [0,1/256]. For every e>=r_* the SAME
A(r_*) remains feasible because the entry radius bounds only widen.
For0<=e<r_*, equations(3)-(7), applied directly to the original
columns in(13), give energy strictly exceeding58cap; hence (13) is
empty. Therefore

    T_{e,tau} is feasible IFF e>=r_*,
    for ALL real e>=0 and ALL real tau in [0,1/256]. (16)

On the full real interval [1/363,1/362], the minimum aggregate energy
over (13) with only the last energy-ball constraint omitted is E(e).
Its aggregate58-vector is uniquely (11); the transport matrix need
not be unique. Inequality(5) supplies the lower bound and (15)
attains it with every original entry/floor/column constraint.

This closes the full S/B column/floor transport relaxation for this
fixed witness. It neither constructs an original stochastic PSD
Hoffman matrix at r_* nor proves the best distance to the original
sharp-optimizer set. Original full-matrix extension and stronger
Schur/dual directions remain open. General signed H and inertia I
are separate conjectures in
[EFF Section4](https://arxiv.org/html/2609.28404v1#S4); the weighted
Hoffman formulation does not require nonnegative entries. Standard
Cauchy, Schur, convexity, flow and algebraic-root mechanisms are
prior mathematics. All completeness and real-parameter arguments
above are ordinary, unformalized and independently unreviewed.
