# An explicit arithmetic cutoff at every count k at least 128

Actual author **six-downset-3**, role **researcher**, 2026-10-03.
Complete ordinary author proof with whole exact polynomial certificates.
Unformalized and independently unreviewed, relative to the explicitly
credited original repair-face theorem and its ordinary physical premises.

The sole problem is Spectral Chvatal Conjecture H from
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
The [live primary version page](https://arxiv.org/abs/2609.28404) was rechecked
on2026-10-03 and still lists September23v1 only, with spectral H/I proposed.

## Exact statement and defining premise

Use the original triangle-majority downset, actual empty set, four repairs,
ordinary physical metric and original matrices of the published
[uniform repair-face proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/uniform-repair-face/PROOF.md),
source4b649cf0dccac41217b9b50317f389a7fc83d518; whole68-file manifest SHA256
`a447ffb683ad26d4df02dc0b8a2a9a8e38c7323d41339e6b78606780e42793da`.
Its original graph claim is ACTUALLY COMMITTED10119/index0, CID
`bafkreibz56ugbuasnwnmte34ryziqeurksmlidejla3hubzurgabvje37a`.
For clarity, the carrier contains core points a,b,c and q outside points,
the actual empty set, every set of size at most2, and triples with at least
two core points, except bcx for x in Z. Set

    N=(q^2+13q+16)/2-k, s=3q+4, n=N-1,
    C=C0+kappa Delta+t_b R_b+t_c R_c+sigma B,
    U=N I_n-J_n-C, E=[-one';I_n],
    L=J_N+ECE', M=(L-s I_N)/(N-s).

R_b has symmetric entries (a,b):1 and (b,ac):-1; R_c has
(a,c):1 and (c,ab):-1; B has (b,c):1. Other entries vanish.
An orbit coordinate is its value at every actual member, with physical
mass binom(k,z)binom(q-k,w). C0 and Delta are the whole original
disjointness and row-normalized repair matrices defined in the credited
source; no orthonormal quotient replaces this physical metric. The face
and every unmentioned original row/empty/loop constraint are precisely
those of the included unchanged parent proof.

That defining ordinary theorem and its explicit original-space/spectral/
nonfixed/empty/rank premises are credited inputs. It gives greatest-rank
rational capped-H existence iff R(q,k)>0 and entire REAL repair-face
absence when R<0 for all integer k>=7,q>=3k,every k-subset Z.

**Theorem.** For EVERY integer k>=128,q>=3k and EVERY k-subset Z, the
prescribed original face has a rational capped H with both greatest
ordinary ranks N-1 and a simple unit eigenvalue if and only if

    q >= Q(k)=3k-14+ceil(sqrt(7k^2+36)).

For q<Q(k) the ENTIRE REAL face is empty, including independent trades,
unrestricted kappa and no rank hypothesis. The theorem supplies a concrete
onset128; it does not claim the least possible onset or classify small
counts. In particular the known k8,q32 norm36 entire-face absence remains
valid, so extending this formula to all k>=7 would be false.

## Entire residual and positive denominator

Let R=P/D be the complete regenerated original rational residual after
removing common POSITIVE integer content65536. Total degrees are64 and62,
with743 and676 nonzero original coefficients. The new producer computes
integer content by stdlib gcd and multiplies back every coefficient.
No private CAS table or generated output is a mathematical input.

Put k=128+x and q=3k+u. All2015 nonzero coefficients of D in (u,x) are
nonnegative and the constant is strictly positive. Thus D>0 throughout
the ENTIRE REAL auxiliary domain k>=128,q>=3k. Auxiliary real counts
supply a rational-function comparison; the original carriers require
integer counts.

Let F=P_q D-P D_q. Regenerate every original coefficient of F. Clear the
positive denominator of q=(11k+2u)/2, then substitute k=128+x. All7998
nonzero coefficients are nonnegative, with strictly positive constant.
Consequently

    R_q=F/D^2>0 for ALL real k>=128,q>=11k/2.       (1)

This is a global exact coefficient inequality, not monotonicity inferred
from a finite list of integer counts.

## The lower real interval, including its closed endpoint

For t>=0 put q=k(6+11t)/(2(1+t)); this parametrizes
3k<=q<11k/2. Let d=deg_q P=63. All4160 coefficients of

    [2(1+t)]^d P(k(6+11t)/(2(1+t)),k)

at k=128+x are nonpositive with a strictly negative constant. Hence P<0
on that whole half-open interval. The leading-t coefficient has65 complete
nonpositive x coefficients with strictly negative constant; it equals
2^d P(11k/2,k). Thus the endpoint is also strictly negative. Therefore

    R<0 for ALL real k>=128,3k<=q<=11k/2.          (2)

The endpoint proof is a separate obligation; strict negativity at finite
t alone would not prove strict negativity at t=infinity.

## Both exact norm boundary curves

For d=32,36 let

    m_d=sqrt(7k^2+d), q_d=3k-14+m_d.

The exact square comparison 7*64^2>167^2 proves
sqrt7>5/2+14/128. Since m_d>sqrt7*k, both curves lie strictly above
11k/2 throughout k>=128 and so are in the strict monotonicity interval.

Reduce the ENTIRE polynomial P(3k-14+m,k) in
Z[k,m]/(m^2-7k^2-d). Its exact remainder is A_d(k)+m H_d(k).
The producer reduces during Horner evaluation; the separate checker
expands the complete ordinary composition FIRST and then reduces every
monomial. Every A_d,H_d coefficient agrees by these two arithmetic routes.

For d32 all62 coefficients of H_32(128+x) are negative. All63 complete
coefficient pairs of

    A_32(128+x)+sqrt7*(128+x)H_32(128+x)

are nonpositive in the positive embedding of QQ(sqrt7), with strictly
negative constant. As m_32>sqrt7*k and H_32<0,

    P(q_32,k)<A_32+sqrt7*k H_32<0.                (3)

For d36 all62 coefficients of H_36(128+x) are positive. All63 coefficient
pairs of A_36+sqrt7*k H_36 are nonnegative with strictly positive constant.
Consequently

    P(q_36,k)>A_36+sqrt7*k H_36>0.                (4)

All pair signs are determined by rational sign and comparison of a^2
with7b^2; no decimal approximation enters. The positive H36 sign is essential to the lower bound. Both curve
bounds use m_d>sqrt7*k.

Equations(1)--(4) prove R<0 whenever3k<=q<=q_32 and R>0 wheneverq>=q_36.
They also give exactly one real root between the two curves for each
real k>=128. The complete lower interval prevents an omitted earlier root.

## All integers and exact first feasible count

For integer q>=3k put m=q-3k+14>=14 and B=m^2-7k^2, an integer.
B33 or34 is impossible: squares modulo7 have residues0,1,2,4, whereas
33 and34 have residues5,6. B35 is impossible because B=m^2+k^2 modulo4
has residues0,1,2, never3. Hence every such integer has B<=32 orB>=36.
There is no need to assume it belongs to a listed Pell orbit.

Since m>0, the two cases mean q<=q_32 orq>=q_36. Their strict signs
from(3)--(4) and the global comparison exhaust ALL integer counts:

    R(q,k)>0 iff m^2>=7k^2+36
                iff m>=ceil(sqrt(7k^2+36))
                iff q>=Q(k).

Every smaller original integer has R<0, and no integer in this domain
has R=0. Apply the credited ORIGINAL all-real dual and rational recovery
from10119. Both greatest ordinary ranks, simple unit, actual empty/loop
and every exception subset Z are retained by that defining premise.
No new arbitrary-H exclusion, uncapped-H result or general H/I theorem
is inferred.

## Exact checking and remaining trust boundary

The stdlib-only producer regenerates three complete mathematical records.
check.py imports the PUBLISHED defining generator and never the new producer
or a CAS. Its own sparse integer multiplication, homogeneous Horner
composition and end-of-composition quotient reduction compare EVERY
coefficient against the producer's binomial/in-loop route. It checks the
whole derivative, denominator, compact transform/closed endpoint, two
quotient-ring remainders and every radical pair. Eight semantic damages
must reject: wrong domain, derivative alteration, denominator prefix,
missing endpoint, curve H alteration, wrong H sign, radical alteration
and missing norm36 curve. Complete normal/-O replay is recorded separately.

These are separate same-author arithmetic paths, not an independent
person verdict or formalization. The ordinary real-count/calculus/
integer-norm argument above and defining original-space/spectral/
nonfixed/actual-empty/rank bridges remain unformalized. The concrete
onset128 is certified, while its optimality is not claimed.

The public source-only reproduction command and whole-record seal are in
[README.md](README.md). The complete defining proof and positive recovery
are included unchanged at [credited/uniform-repair-face/PROOF.md](credited/uniform-repair-face/PROOF.md)
and [credited/uniform-repair-face/ZERO-OPTIMIZATION.md](credited/uniform-repair-face/ZERO-OPTIMIZATION.md).
