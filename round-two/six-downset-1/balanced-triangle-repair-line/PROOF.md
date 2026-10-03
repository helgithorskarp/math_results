# Exact original three-pair repair line for the balanced private-triangle seed

Actual author **six-downset-1**, role **researcher**, 2026-10-03.
Ordinary author proof. The original-space projection, congruence,
resolvent and completeness arguments below are unformalized and independently
unreviewed. Exact arithmetic checks are separate validation obligations.

The sole problem family is [Spectral Chvátal Conjecture H](https://arxiv.org/html/2609.28404v1#S4).
Live abstract/version-history/Section 4 checks on October 3 still find only
September 23 v1, with H and I proposed. Its classical/projection-packing
results do not provide the matrices considered here.

The seed is precisely the original balanced private-triangle seed of
[source2252bca](https://github.com/helgithorskarp/math_results/blob/2252bcaacf4798c6b13d75b4918792fd7c8bbe9c/round-two/six-downset-1/balanced-triangle-all-cubes/PROOF.md),
actually committed **10111/0**, CID
`bafkreiailm2w3yvzhfqflc2nwzrnv3o2v3xuxygp5zzkk6if7aumqrylaq`.
Its all-dimension proof is unformalized and independently unreviewed.
The independent [review10117](https://github.com/helgithorskarp/math_results/blob/bdab8a1bb779a940737e73d90b579ff8a19b863d/round-two/six-reviewer-5/balanced-three-cube-audit/PROOF.md)
confirms only the old three-point cube, all h>=2; it establishes the sufficient
norm-based repair interval and a larger rational repair. That verdict does
not cover this exact endpoint or the all-dimension seed. The rank-two update
and original Schur mechanisms are credited; the new obligation here is the
full real repair-line classification and explicit uniform inverse energies.

## Family, fixed line and precise statement

For integers n>=3,h>=2 take an old n-point cube with distinct marks x,y,
and h triangles at each mark, all 2h private pairs mutually disjoint and
outside the old set. Let the downset be their union. Set

    q=2^(n-1), D0=3h, s=q+3h, N=2q+12h, ell=6h+1.

Let C0 be the exact nonempty Gram constructed in source2252bca, and let
Q0 be its WHOLE negative-row-sum lift, including the actual empty row.
This fixes the seed, including all free entries; the result does not quantify
over arbitrary matrices for the downset. Let I be the first x-private triple,
and j the last y-private full row. Define the ORIGINAL N-dimensional vectors

    u=sum_(i in I)e_i-3e_empty, v=e_j-e_empty,
    Q_delta=Q0+delta(uv^T+vu^T), L_delta=J+Q_delta,
    M_delta=(L_delta-sI)/(N-s), P=I-J/N.

Every real delta retains symmetry, M1=1, the original intersection zeros,
every nonempty diagonal, and the actual empty loop with its required lift
value. Put K0=NP-Q0 on 1-perp, and define the EXACT rational inverse energies

    A=u^T K0^-1 u, B=v^T K0^-1 v, C=u^T K0^-1 v,
    kappa=2/nu+4/beta, dL=6/kappa,
    dMinus=1/(C-sqrt(A B))<0, dPlus=1/(C+sqrt(A B))>0.

Here beta,nu are the positive seed residual scalars. A>0,B>0 and AB>C^2.
The square roots specify real endpoints exactly, rather than numerical
approximations. The following statements hold for EVERY permitted n,h:

1. L_delta is PSD iff 0<=delta<=dL. In the open interval its rank is N-2,
   with exactly the two original centered maximum-star kernels. At either
   endpoint its rank is N-3. Outside the closed interval it has one negative
   direction, so it is not an ordinary H certificate.
2. I-M_delta is PSD iff dMinus<=delta<=dPlus. Its rank is N-1 in the open
   interval and N-2 at either endpoint. The unit eigenvalue of M_delta is
   simple precisely in the open interval when the cap is PSD.
3. M_delta is a capped H matrix iff 0<=delta<=min(dL,dPlus). It simultaneously
   attains greatest ordinary lower rank N-2, cap rank N-1 and a simple unit
   eigenvalue iff

       0<delta<min(dL,dPlus).

At zero the seed has the extra lower kernel. At dL the lower develops its
extra kernel; at dPlus the cap develops its extra kernel. If the two positive
endpoints coincide, both changes occur there. No ordering of those endpoints
for all n,h is asserted without a separate exact sign certificate.

These are absence statements on THIS fixed real one-parameter line, not
absence of H matrices for the family or general H/I. Rational choices inside
the interval give rational matrices. The ordinary greatest-rank bound is
credited prior9361 and the seed source; the present result does not claim that
bound as new or optimize over other repairs.

## Whole original lower congruence, including necessity

Source2252bca supplies a positive definite retained ORIGINAL principal A_*
of size N-4, obtained by deleting singleton x,singleton y and private row j.
The two original nonempty star indicators are kernels of C0 and C_delta for
every real delta: the updated private rows contain neither mark. Their
coefficients at singleton x,y form the identity matrix. Elementary invertible
column operations can therefore subtract these two kernel vectors to erase
those two singleton coordinates. The WHOLE C_delta is congruent to the
principal obtained by deleting x,y, plus a two-dimensional zero block.
This proves necessity as well as sufficiency of that retained-plus-j principal.

Let z_* be the ORIGINAL coefficients of row j in the retained basis, and r
the indicator of I in that basis. The source proves

    C0[j,j]=z_*^T A_* z_*=s-1, r^T z_*=-3,
    r^T A_*^-1 r=kappa=2/nu+4/beta.

The two-mark completion gives the last equality from the complete W-mean and
WF residual directions, rather than a scalar approximation. The updated
principal has off-diagonal column A_*z_*+delta r and unchanged A_* and last
diagonal. An invertible Schur congruence is therefore

    A_* direct-sum [6delta-kappa delta^2].

A_* is positive definite for ALL parameters. The scalar is positive exactly
for 0<delta<dL, zero at the two endpoints, and negative everywhere else.
This gives all stated C_delta inertias and kernel dimensions without ignoring
any original row or treating a principal minor as sufficient by itself.

The negative-row-sum lift is Q_delta=T C_delta T^T, with T having retained
identity nonempty rows and empty row -1^T. It has full column rank; C_delta
is also the nonempty principal of Q_delta. Thus positivity is equivalent,
rank is unchanged, and Q_delta kills the original ones vector. Adding J
contributes precisely one positive direction on span(1), orthogonal to
1-perp. This proves all lower ranks and the negative-direction assertion.
For an interior delta, the two surviving star kernels lift to
chi_x-(s/N)1 and chi_y-(s/N)1; their independence and dimension finish the
entire original kernel statement.

The whole update at empty has entries -delta to I, -3delta to j, and
6delta on its loop; the only nonempty changes are the three free disjoint
I-to-j pairs. It is exactly delta(uv^T+vu^T), not a repair followed by deletion
of empty. Its rows sum to zero and both centered-star pairings vanish.

## Whole cap, rank-two necessity and complete complement

The seed proves K0>=P on 1-perp; it is therefore strictly positive there.
Set a=K0^-1/2 u,b=K0^-1/2 v in that WHOLE (N-1)-dimensional space. The
vectors u,v are independent since

    u.u=12, v.v=2, u.v=3, 12*2-3^2=15>0.

Invertibility implies A=a.a>0,B=b.b>0,AB>C^2. On 1-perp the cap is congruent
to I-delta(ab^T+ba^T). The symmetric rank-two operator has nonzero eigenvalues
C+sqrt(AB)>0 and C-sqrt(AB)<0: use its trace 2C and its two-dimensional
determinant C^2-AB, or act on span(a,b). Its remaining N-3 directions have
eigenvalue zero, so the congruent cap has eigenvalue one on the COMPLETE
orthogonal complement. Positivity is equivalent to the two scalar inequalities
1-delta(C+sqrt(AB))>=0 and 1-delta(C-sqrt(AB))>=0. They give exactly the
closed interval [dMinus,dPlus], not merely a sufficient norm bound.

At either endpoint precisely one scalar vanishes because dMinus<0<dPlus;
in the interior neither does. Reinserting span(1), which is always the
original cap kernel, gives ranks N-2 and N-1. The relation

    (N-s)(I-M_delta)=NP-Q_delta

has a positive scale, proving the cap and simple-unit claims. Intersecting
the exact lower/cap intervals gives the classification in the statement.
This argument includes the physical-range complement, star directions and
the empty row; no small quotient is asserted to exhaust the original space.

## Uniform rational energies from complete physical projections

Use the seed's orthogonal B_i,T_i1,T_i2,T_i3,M_i,WA_i,WF_i physical spaces
in both mark groups, with sum B_i=0,sum_a T_ia=0,sum_(all facets)M_i=0.
Put TS_i=T_i1+T_i2-2T_i3=-3T_i3. For a single chosen facet let t_i=e_i-1/h
within its mark group. Its coefficient squared norm is (h-1)/h. The complete
standard block metric/frame of source2252bca are Gamma4,S4, with

    Gamma4=diag(2s/3,12s,2beta,2nu), F4=N Gamma4-S4>0,
    E4(z)=(Gamma4 z)^T F4^-1(Gamma4 z), gamma=(h-1)/(2h),
    z_u=(0,c h/[3(h-1)],0,3), z_v=(b,c/[3(h-1)],1,1), b=-2a.

The physical row image R u equals

    [c h/(3(h-1))] TS_(x,t_i)+3M_(x,t_i)+[3/(2h)]M_odd,

where M_odd=sum_x M-sum_y M. Indeed the private triple's old projections sum
to 3z and cancel -3 times the actual empty row z; its B coefficients sum
to 2a+b=0; its WA/WF coefficients cancel. The T sum is
c[-T_i3+sum_(j!=i)T_j3/(h-1)], exactly the displayed centered TS contrast.
Splitting M_i into centered within-mark and group mean gives the last term.

The physical image R v has standard coefficients z_v in the y contrast,
even trace coefficients (-c/(6h),1/(2h)), the NEGATIVE of those coefficients
in the odd trace, and odd-mean coefficient -1/(2h). Its old component again
cancels the actual empty z. Explicitly

    [c/(h-1)]sum_(j!=i)T_j3
      =[c/(3(h-1))]TS_ti-[c/(3h)]sum_y TS,

while WF_i=WF_ti+(1/h)sum_y WF and M_i=M_ti-M_odd/(2h). This accounts for
every original coefficient; both physical images have zero leaf-odd and
untouched-old components.

The seed's COMPLETE simultaneous metric/frame decomposition is orthogonal
on both forms, and therefore on the resolvent. In each fixed sector the old,
trace and mean blocks are separately block diagonal, as the complete original
row sums prove. Thus no old/trace coupling is being omitted in an inverse.
The two mark contrasts are orthogonal; the trace blocks for u vanish. Only
the odd mean couples R u,R v. The actual empty contributes to the seed frame
but is already retained in both the frame and the cancellation above.

The representative common trace metric is h*diag(12s,2beta), its frame is
h*[[12s^2(1+c^2),-6cs beta],[-6cs beta,3beta^2]], so set

    T2=[[12s(N-s(1+c^2)),6cs beta],
        [6cs beta,beta(2N-3beta)]],
    E2=(-2sc,beta)^T T2^-1(-2sc,beta)/h,
    m=nu/[2h(N-3nu)].

T2 is strictly positive by the seed cap. The odd mean metric/frame are
2h nu,6h nu^2, giving N-3nu>0 and the above m. The two trace contributions
to the v energy are each E2, the standard contributions are gamma E4, and
the odd-mean energies/cross energy are 9m,m,-3m. All inverses exist throughout
the physical domain because the seed proves the stricter floor-one cap.

Finally R maps the ORIGINAL vertex space into its complete physical row
space, Q0=R^*R and RR^*=S as an operator with physical metric. Direct
multiplication gives the Woodbury identity on the whole 1-perp space

    K0^-1=(1/N)[I+R^*(N I-S)^-1 R].

The identity term retains the ENTIRE kernel complement of R; replacing
K0^-1 by a physical inverse alone would lose it. Using the original Euclidean
pairings 12,2,3, the exact inverse energies are therefore

    A=[12+gamma E4(z_u)+9m]/N,
    B=[2+gamma E4(z_v)+2E2+m]/N,
    C=[3-3m]/N.

They are rational in q,h, computable by TWO right sides of one positive
four-dimensional solve and one positive two-dimensional solve, with no
N-dimensional inverse and no truncation of original modes. Complete
physical projections and the ordinary Woodbury argument supply the
unbounded bridge; finite controls alone do not supply it.

## Exact certificate and remaining status

energies.py uses the unchanged seed sector source and performs exact shared
Gaussian elimination after positive metric row division. symbolic.py retains
all ten compact solution coefficients, all six pivots, and eight exact
energy expressions in QQ(h,q). Its first run completes in 1.670308s/18180KiB
with unchanged60s,512terms,32MiB,native1/serial1/1CPU2GiB. It checks all
compact original inverse equations and positive shifted pivot polynomials.
The separate check_inverse.py imports neither energies.py, the seed recipe,
the physical sector module nor the field engine. Its unchanged credited
integer/Fraction decoder proves every encoded denominator positive on the
whole auxiliary quadrant. Separate closed forms and conservative rational
degree propagation give bound (146,56): ALL18 full coefficient identities
are verified on8,379 degree-complete Cartesian nodes,150,822 equalities.
These comprise all10 compact inverse equations and all8 energy expressions;
all7 distinct positive denominator polynomials and27 factor occurrences
are checked. Clearing nonzero denominators and the univariate root bound
in each variable prove the QQ(h,q) identities. This is not sampling a few
parameter values and extrapolating their validity.

original_control.py reconstructs all actual original rows, both complete
physical projections and the ENTIRE mean-gauged original cap inverse.
It verifies all coefficients of the full Woodbury inverse, original support,
row sums, actual empty/loop and both centered-star kernels. Atn4,h2,N40 and
n4,h3,N52 it checks the seed/interior/lower-endpoint lower ranks, explicit
ORIGINAL negative lower witnesses on both sides, exact rational isolation
of the positive cap endpoint, a whole cap PSD/rank check immediately inside,
and an explicit whole negative cap witness immediately outside. At BOTH
positive/negative algebraic cap endpoints it verifies every original null
equation in QQ[e]/(e^2-AB), without floating square roots. The cap endpoint
rank comes from the ordinary whole rank-two proof, not an unperformed
algebraic full PSD elimination.

The two fixtures retain1,600/2,704 original matrix positions,72/96 complete
physical projection coordinates,80/104 original inverse equations and80/104
whole Woodbury equalities. Both cap endpoints contribute80/104 original
algebraic null equations. Their exact endpoint comparisons dPlus<dL remain
finite fixture controls, not uniform ordering evidence.

Eight semantic altered certificates reject with ValueError in each replay
mode; a wrong energy agrees identically on the h=2 AND q=4 boundary lines,
so its rejection also exercises interior complete-grid coverage. A timeout,
killed process or incomplete run is explicitly not semantic rejection.
Both complete private source-only normal and optimized runs agree on every
byte of the7,894-byte mathematical record, SHA256
`8b475f843984ff98e6f6128bf0fb30a885e725faebcfc3a6a73423d82be8d3fa`.
The compact47,974-byte inverse certificate is entirely regenerated and
compared, SHA256
`5a82f1b95656a232c2f96c2c2d055343911c21566fe03207b9abd671fdf7c5ec`.
This compact source packet contains the complete ordinary proof, all
18 inverse/energy coefficient identities and complete original controls.
[README.md](README.md) gives source-only reproduction; [SOURCES.json](SOURCES.json)
records all credited utility bytes. [VALIDATION.json](VALIDATION.json) binds
the sealed replay. The all-parameter bridges remain unformalized and
independently unreviewed.

The existing ONE original n4,h2 full40-dimensional inverse control from the
previous pass verifies all three energies exactly, including C=67/928, and
places dPlus<dL for THAT fixture only. Its finite comparison is not transported
to the unbounded domain. No uniform endpoint ordering or best gap is claimed.

Scope excludes n=2,h=1,unequal triangle counts, overlapping private pairs,
other seeds/repair faces, arbitrary downsets and general H/I. No new resource
or worker is needed. Uniform ordering of the two positive endpoints is a
separate frontier requiring a complete exact sign argument; this theorem
is the exact min-endpoint classification, without asserting that ordering.
