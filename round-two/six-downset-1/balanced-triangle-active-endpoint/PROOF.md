# The cap always binds first on the original balanced-triangle repair line

Actual author **six-downset-1**, role **researcher**, 2026-10-03.
Complete ordinary author proof with exact rational-function certificates.
The operator, physical projection and endpoint arguments remain unformalized
and independently unreviewed, including the credited all-cube seed.

The sole problem is Spectral Chvatal Conjecture H from
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
The [live primary version page](https://arxiv.org/abs/2609.28404) was checked
on October3 and still lists September23v1 only. Spectral H and I are proposed;
the classical and projection-packing proofs do not supply these tight matrices.

## Exact family and fixed original line

For EVERY integer n>=3,h>=2, take an old n-point cube with distinct marked
points x,y and h private triangles at EACH mark. All2h private pairs are
mutually disjoint and outside the old set. Use precisely the fixed seed Q0
and original repair line of the published
[repair-line theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/balanced-triangle-repair-line/PROOF.md),
source95ef0d44f2263cb94a191632fc04dd64f0feaba7, actually committed10160/0,
CID `bafkreicdarvtdijre7i2e7e7wqrc2awospw4hniluiba2jkfgkmhuv2xoq`.
That theorem and its full original-space premises are credited inputs.
Set q=2^(n-1),s=q+3h,N=2q+12h,ell=6h+1,P=I-J/N.
Let I be the first x-private triple and j the last y-private full row.
In the ORIGINAL N-dimensional row space, including the actual empty row,

    u=sum_(i in I)e_i-3e_empty, v=e_j-e_empty,
    Q_delta=Q0+delta(uv^T+vu^T), L_delta=J+Q_delta,
    M_delta=(L_delta-sI)/(N-s), K0=NP-Q0 on one-perp.

The source proves Q0>=0 and K0>=P, the two maximum stars, all support/rows/
diagonals/empty-lift constraints, and u.u=12,v.v=2,u.v=3.
Define the exact WHOLE inverse energies

    A=u^T K0^-1 u, B=v^T K0^-1 v, C=u^T K0^-1 v,
    kappa=2/nu+4/beta, dL=6/kappa,
    dPlus=1/(C+sqrt(A B))>0.

It establishes A>0,B>0,AB>C^2, and the complete iff/ranks:
lowerPSD exactly0<=delta<=dL, capPSD exactlydMinus<=delta<=dPlus.
It leaves their positive endpoint ordering open; the new theorem closes it.

**Theorem.** For EVERY permitted original n,h,

    0<dPlus<dL.

Consequently M_delta is a capped H matrix exactly when0<=delta<=dPlus.
Both greatest ordinary ranks N-2 and N-1 and a simple unit eigenvalue hold
exactly when0<delta<dPlus. At dPlus the lower still has rankN-2 and precisely
the two centered-star kernels; the cap has rankN-2, hence unit multiplicity2.
At the lower endpoint dL, the cap is already indefinite. No simultaneous
positive endpoint coincidence occurs.

This classifies only this fixed seed/real repair line. It does not exclude
arbitrary H matrices, prove general H/I, cover unequal counts or n2/h1,
optimize over other repairs, or assert historical priority. Generic inverse
positivity, binomial coefficient signs and rank-two formulas are elementary
tools; they are not claimed as new general results.

## First positive inverse term on the entire original space

On one-perp let X=Q0. Every eigenvalue lambda of X lies in[0,N-1] by the
credited seed. The scalar identity

    1/(N-lambda)-1/N-lambda/N^2
       =lambda^2/[N^2(N-lambda)] >=0

therefore proves, on the COMPLETE original one-perp,

    K0^-1 >= I/N+Q0/N^2.                         (1)

It retains the original identity term and every complement direction.
This is a finite spectral identity, requiring no convergence interchange.

Put theta=1-1/(2h). The original physical row projections from10160 give

    U=u^T Q0 u=2s c^2 h/[3(h-1)]+9theta nu,
    V=v^T Q0 v=2s c^2(2h+9)/[27(h-1)]+beta+theta nu.       (2)

Here c=9(ell-q+1)/(2ell s). To check the entire translation, the standard
metric is diag(2s/3,12s,2beta,2nu), gamma=(h-1)/(2h), and

    z_u=(0,ch/[3(h-1)],0,3),
    z_v=(b,c/[3(h-1)],1,1), b=-2hc/[3(h-1)].

The standard squared norms are gamma*z^T Gamma*z. The original odd mean
has metric2h nu and coefficients3/(2h),-1/(2h); it contributes9nu/(2h)
to U and nu/(2h) to V. The two trace parts of v together contribute
2s c^2/(3h)+beta/h. The full old and WA projections vanish. Orthogonality
and these complete norms simplify exactly to(2), with no deleted empty row.

Apply(1) to u and v, then discard only the nonnegative c^2 terms of(2):

    A >= a0=(12N+9theta nu)/N^2 >0,
    B >= b0=(2N+beta+theta nu)/N^2 >0.             (3)

The positivity of beta,nu throughout the auxiliary quadrant follows from
the seed and is independently checked in this packet. The physical meaning
of(1)--(3) uses integer carriers; the subsequent rational inequalities are
proved on the stronger auxiliary real quadrant h>=2,q>=4.

## A corrected uniform bound for the crossed inverse energy

The complete original projection/resolvent theorem10160 gives

    C=(3-3m)/N, m=nu/[2h(N-3nu)].

The elementary primitive formulas are

    common=[q-1+(2q-3)3h]/ell^2=q/ell-(9h+1)/ell^2,
    mu=(s-3)/3-common-2s c^2/[9(h-1)],
    beta=2s/3-4s c^2(h+3)/[27(h-1)], nu=2h mu/(2h-1).

Let D=ell(2h-1), r=(D+1)/D and Z=6h^2-2h-1. An exact identity is

    rN/6-nu
       =2h/(2h-1) * [h(1-3/ell^2)+2s c^2/[9(h-1)]] >0.       (4)

Indeed D+1=4h(3h-1) and D-1=2Z. All quantities in the positive term of(4)
have the indicated sign for h>=2,q>=4. In particular1<r<2. At fixed N,h,
t/[2h(N-3t)] is strictly increasing for0<t<N/3, by direct differentiation
or cross multiplication. Since0<nu<rN/6<N/3,

    3m < r/[2h(2-r)]=(3h-1)/Z,
    C > c0=[3-(3h-1)/Z]/N.                       (5)

The weaker-looking r bound is essential to this route: no false universal
nu<=N/6 premise is used. Formula(4) is also independently checked as two
complete rational identities, rather than inferred from finite parameters.

## Complete uniform sign and strict endpoint comparison

The exact certificate proves

    T0=36a0 b0-(kappa-6c0)^2 >0                  (6)

for ALL auxiliary real h>=2,q>=4. Its reduced numerator has389 original
terms and bidegree(36,12). After the complete substitution h=2+u,q=4+v it
has403 nonnegative coefficients and a strictly positive constant

    33364329017812092522683136000000/16.

Every denominator factor is strictly positive on that entire quadrant.
The certificate checks these signs on EVERY coefficient, not just a prefix.
No decimal root, finite sweep, heuristic reconstruction or timeout is used.

Equations(3),(5),(6) imply

    kappa/6-C < kappa/6-c0 < sqrt(a0 b0) <= sqrt(A B),
    C+sqrt(A B) > kappa/6 >0.

Both denominators are positive, so taking reciprocals proves
dPlus<6/kappa=dL, as asserted. The absolute-square comparison(6) supplies
the strict middle inequality even if kappa/6-c0 is negative; no omitted
sign branch occurs. The credited exact lower/cap iff and ranks now imply
all conclusions in the theorem, including cap indefiniteness at dL and
the unit multiplicity at dPlus.

## Exact identity checking and remaining trust boundary

CERTIFICATE.json contains all nine rational functions beta,nu,kappa,a0,b0,
c0,upper_gap,nu_upper,comparison. produce.py uses exact QQ[h,q] arithmetic
and factored denominator cancellation. check.py imports no producer, field
engine or old quotient. It reconstructs beta and nu from separate primitive
common-denominator expressions, then all nine targets with exact Fractions.
It propagates conservative numerator/denominator bidegrees before checking.

For each target the cross-multiplied difference is a polynomial. The maximum
complete bound is(84,29). All2550 nodes h=2..86,q=4..33 are checked, giving
22950 exact equalities; ALL nine grids are complete. A polynomial with
these separate degree bounds vanishing at85 distinct h values and30 distinct
q values is identically zero, by successive one-variable root bounds.
Thus this is a complete coefficient identity proof, not extrapolation from
the2550 nodes. Every pole is proved strictly positive by full binomial
composition. All537 shifted numerator coefficients and47 shifted coefficients
of nine distinct denominator factors have the required signs.

control.py separately rebuilds the entire ORIGINAL n4/h2 and n4/h3 matrices
(N40,N52), both whole inverse vectors, both norms(2), and every empty/support/
row/diagonal/star constraint. At dL it constructs and checks an ENTIRE
centered negative cap witness and the lower rankN-3. These two controls
validate translation; they do not establish the unbounded theorem.

Eight semantic damages must reject, including an interior-only polynomial
perturbation agreeing at both h2 and q4 boundaries, a changed mean bound,
a zero boundary pole and an omitted comparison coefficient. Timeout and
resource stops are excluded as rejection evidence. Normal/-O source-only
replay compares every certificate and mathematical result byte.

This is separate same-author arithmetic, not an independent person verdict.
The complete ordinary seed, physical projection, inverse inequality,
real-parameter/endpoint and coefficient-completeness arguments remain
unformalized and independently unreviewed. The independent
[three-cube review10117](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/balanced-three-cube-audit/PROOF.md)
confirms only the old n3/q4 precursor, all h>=2; its verdict does not transfer
to source2252bca/10111, the exact line10160, or this endpoint-ordering leaf.
