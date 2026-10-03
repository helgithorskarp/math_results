# A complete upper chart cut for the original twelve-point G20 core

Actual author **six-tammes-2**, role **researcher**, 2026-10-03.
Complete ordinary conditional lemma, with exact coefficient and alternate
arithmetic verification. Independent review of this new lemma is pending;
the argument is unformalized. No global Tammes15 bound is claimed.

**Lemma.** Let t lie in the entire CLOSED interval I=[14/25,593/1000].
Take twelve distinct unit vectors labelled 0,1,2,4,5,6,7,8,9,10,11,12,
all different-point products at most t, with these twenty equalities:

```
0-5 0-6 0-7 0-11 1-2 1-4 1-10 1-12 2-4 2-8 2-10
4-8 5-7 5-9 5-11 6-11 7-12 9-10 9-11 10-12.
```

In the complete original-G20 chart of LEMMA9774, their parameter satisfies
the STRICT inequality z<7/5. Additional contacts are allowed. Other code
points, if present, are arbitrary and play no part in the proof. No
thirteenth point, 5-12 contact, face, degree, cohort, support, tube,
incumbent proximity or optimizer occurrence is assumed.

Consequently one may add the exact strict predicate 7-5z>0 to the lossless
nine-variable arbitrary-three-addition system of LEMMA9912 without losing
any solution, including its critical strip and closed t endpoints. Its
six addition variables, positive radical and all packing conditions remain
necessary; this lemma does not decide that system's feasibility.

## Imported normalization and positive clearing

The [complete original-G20 frame](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/twelve-core-frame/PROOF.md),
LEMMA9774/0, is a logical dependency. It exhausts all four formal sheets
and singular/regularity alternatives, and permits exactly
(epsilon,eta)=(-1,+1), g>1/2 and |z|<5/2. Its whole-core pruning theorem is
imported; no earlier local gate or actual-point13 pruning substitutes for it.
The independent REVIEW9809 concerns that prior frame, not this new cut.

For precision, work in the coefficient basis (p1,p2,p4), with
H_t=(1-t)Id+t11^T and product

    <x,y>_t=(1-t)sum(x_i y_i)+t sum(x_i)sum(y_i).

Here 1 is the three-entry all-ones column. Let B_i be the six B-cluster
coefficient vectors. With d=H_t^{-1}(B12 cross B1), the finite circle chart
is

    p7=t B12+(D z^2-1)/(1+D z^2)*(B1-t B12)
        +2D z/(1+D z^2)*d,       D=(1-t)^2(1+2t).

This chart is taken with its original labelled orientation. There is no
new reflection quotient. In the decomposition
p7=t B12+alpha(B1-t B12)+beta d, its inverse is
z=beta/[D(1-alpha)]; alpha=1 would give the forbidden p7=p1.
Thus every actual core has the finite chart parameter being cut here.
The packing comparison p7.p1<=t gives (1-t)^2 z^2<=1.

The [polynomial lift](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/twelve-core-polynomial-model/PROOF.md),
LEMMA9912/0, supplies the following integral notation and exact numerators:

```
a=1+t, b=1-t, c=1+2t, D=b^2 c, C=1+D z^2,
K=t(9t^2-2t-3), J=a^2+K=9t^3-t^2-t+1, h=9t^2-1,
S=D(t z^2-2z)+t(2t-1), E=C^2-S^2,
G=a^4[(1-t^2)C^2-S^2]-K^2 C^2+2SKt a^2 C,
R=D G, w=sqrt(R)>0, Omega=h J bc a^8 C E.
```

The decoded A-cluster point is p_i=Y_i/Omega. The B-cluster points used
below have p_j=N_j/a^2, where
N8=(-a^2,2ta,2ta) and N12=(2t(1+3t),3t^2-2t-1,-2ta).
All Y_i and N_j are the factored polynomials of the lift, implemented in
[frame.py](frame.py). That file and the small [integer ring](polynomials.py)
are bundled byte-for-byte from9912. Its ordinary packing-to-lift proof is
imported. No old native executable or private data is a new runtime input.

All clearing factors are strictly positive on the actual feasible core.
Indeed t,a,b,c,D,C,h>0 on I. J>=26671/15625>1, since J(14/25)
has that value and J'=27t^2-2t-1>0 on I. The exact identity

    G=a^4(1-t^2)E-(KC-St a^2)^2

and imported G/(a^4 C^2)=g>1/2 give G>0, R>0 and E>0. Hence Omega>0.
These are feasible-domain conclusions, not positivity assumptions on
infeasible boxes. No zero factor E or chart boundary is canceled below.

## Two packing excesses and their full factorizations

Let

    q_ij=<Y_i,N_j>_t-t a^2 Omega.

Its sign is the sign of the actual excess p_i.p_j-t, because a^2 Omega>0.
For the two surviving noncontact pairs define

```
F5=t a^10 b c(3t-1),          F6=a^5 b c(3t-1)(3t+1),
q_5,12=F5(A5+B5 w),          q_6,8=F6(A6+B6 w).
```

Both F5,F6 are strictly positive throughout I. The q's are exactly affine
in w. All of the following are WHOLE integer polynomial identities,
not numerical factorizations or equalities checked only near the incumbent.
Let L5,M6,H10,H12 be the four explicit integral polynomials defined by
[FACTORS.json](FACTORS.json): a row [i,j,0,v] means v*t^i*z^j. Their
degrees are respectively (8,3),(11,3),(10,4),(12,4). Define

```
Z=t(3t+1)z-(1+2t),
M5=1+2t-t^2-2tbc z,
Q=(1+t)D z^2-2D z+2t^2-t+1.
```

Then

```
A5=2D(bz+1)C L5,                B5=-2(bz+1)C M5,
B6=2(bz+1)M6,
A5^2-B5^2 R = a b^5 c^3 J C^2 *
    32(bz+1)^2(1-bz)(bc z+t) Z Q,
A6^2-B6^2 R = a^2 b^4 c^3 J *
    4(bz+1)^2 Q H10 H12,
a Q=D(az-1)^2+4t^2.
```

The last identity proves Q>0. [algebra.py](algebra.py) derives the raw
excesses from the lift, performs two remainder-free integer divisions,
and compares every coefficient in these identities. A7th identity checks
the closed chart boundary M5(t,1/b)=1-5t^2 by positive b clearing.

Z=0 is the exact chart z=(1+2t)/(t(3t+1)) of the credited prior rational
G20+5-12 family. That motivates the factor but supplies no capacity,
feasibility threshold or extra-contact premise. Z changes sign and is
NEVER canceled as a positive factor. We never import t>=1/sqrt(3) from
that different family into an arbitrary G20 core.

## Six signs on three complete closed boxes

Put t_c=113/200 and z_c=71/50. The following three CLOSED rectangles cover
the ENTIRE outer target I x [7/5,5/2], including every seam and endpoint:

```
lower-corner: [14/25,t_c] x [7/5,z_c],
upper-t:     [t_c,593/1000] x [7/5,5/2],
upper-z:     I x [z_c,5/2].
```

Exactly six strict sign obligations suffice:

| Polynomial | Whole closed rectangle | Sign | Exact Bernstein extremum supporting the sign |
|---|---|---|---|
| L5 | I x [7/5,5/2] | positive | min=32873967510792/19073486328125 |
| Z | upper-t | positive | min=349/200000 |
| Z | upper-z | positive | min=174/15625 |
| M6 | lower-corner | positive | min=2061983389011795564/298023223876953125 |
| H10 | lower-corner | negative | max=-14404525232418503178827290793/16000000000000000000000000000 |
| H12 | lower-corner | positive | min=1312218403673868411168/37252902984619140625 |

For a polynomial f of separate degrees(n,m), transform its box to
t=t_a+(t_b-t_a)x, z=z_a+(z_b-z_a)y. If c_rs are its transformed power
coefficients, its tensor Bernstein coefficients are

    B_ij=sum_{r<=i,s<=j} c_rs * binom(i,r)/binom(n,r)
                                 * binom(j,s)/binom(m,s).

The Bernstein basis functions are nonnegative and sum to1 on the CLOSED
unit square. Thus a strict sign of every B_ij proves the strict sign of
f on the whole box, including the boundary. All216 rational coefficients
are actually checked; whole ordered coefficient-array hashes, exact
minima/maxima and all boxes are stored in [CERTIFICATE.json](CERTIFICATE.json).
[check.py](check.py) repeats every coefficient calculation and compares
every certificate entry. [schema.py](schema.py) also checks the25
elementary open or boundary cells of the three-box union.

The alternate [audit.py](audit.py) imports no primary sparse polynomial,
division, expansion or Bernstein routine. An independent uncancelled
degree compiler proves that the seven cleared residuals have degrees at
most(58,12). Every residual is checked at ALL767 different tensor-grid
points t=-1,...,57 and z=0,...,12:5369 exact integer zeros. A polynomial
of separate degrees at most(58,12) vanishing on59 x13 different points
is identically zero. Thus this is a complete interpolation proof of the
identities, not heuristic sampling. It includes exceptional t=-1,0,1
without division. Radical affinity is checked by the degree compiler.

For signs, that auditor translates L5,M6,H10,H12 to the center of their
whole boxes and bounds every nonconstant Taylor monomial by its absolute
coefficient times the box radii. It checks all204 translated coefficients;
the strict bounds pass on all four boxes without subdivision. L5's
alternate lower bound is
19851309774979139449556299723/128000000000000000000000000000>0.
For the two Z boxes it uses the explicit derivatives
Z_z=t(3t+1)>0 and Z_t=(6t+1)z-2>0, and the exact positive lower-left
corner values in the table. [AUDIT_EXPECTED.json](AUDIT_EXPECTED.json)
records every exact alternate bound and identity-grid digest.

## Excluding every feasible point in the outer target

Suppose an actual packing has z>=7/5. Its imported bound gives z<5/2,
so the complete cover applies. In all cases bz+1>0 and Q>0.

On lower-corner, B6=2(bz+1)M6>0. Since H10<0<H12, the second squared
identity gives A6^2-B6^2 R<0. The positive root therefore satisfies
B6*w>|A6|. Hence A6+B6*w>0, so q_6,8>0 contradicts packing. No sign
of A6 is assumed; squaring alone without B6>0 would be invalid.

On upper-t or upper-z, A5=2D(bz+1)C L5>0 and Z>0. The chart gives
0<bz<=1. If bz<1, every factor on the right side of the first squared
identity is positive, so A5^2>B5^2 R. Thus A5>|B5|*w and
A5+B5*w>0. This contradicts q_5,12<=0, regardless of B5's sign.
Again the positive-A guard is essential.

It remains to handle bz=1 rather than divide it away. Here

    M5(t,1/b)=1-5t^2<=1-5(14/25)^2=-71/125<0.

Thus B5=-2(bz+1)C M5>0 while A5>0 and w>0, giving the same packing
contradiction directly, even though the squared identity is zero.
Finally bz>1 already violates the necessary chart inequality; it is
not a discarded singular fiber. These cases exhaust the entire closed
outer rectangle. Therefore every actual original G20 core has z<7/5.

## Evidence, controls, credit and remaining scope

The normal and optimized executions of generation, Bernstein replay,
alternate identity/sign audit and controls are recorded in
[VALIDATION.json](VALIDATION.json). All whole outputs and generated
certificate bytes agree. All native threads are1; jobs are serial under
the unchanged1CPU/2GiB scope and fixed20-second internal/25-second
subprocess guards. Timeout, incomplete enumeration or a solver status is
not used as a mathematical exclusion. No solver or floating-point library
is a proof dependency. The private SymPy1.14.0 discovery factorization
is replaced by the portable exact coefficient and interpolation checks.

[controls.py](controls.py) rejects22 damaged scope/cover/factor/certificate
packets. The alternate interpolation audit actually detects a nonzero
residual after an L5 coefficient is corrupted. Both sign methods reject
a polynomial with a zero at the closed t endpoint. Three unsigned-square
or reversed-root counterexamples are rejected and three valid radical
guards pass. The exceptional bz=1 case is explicitly retained.

At the credited prior rational-family parameter t=29/50, z=5400/3973
with exact positive w=454484658996081/225033203125000, all12 unit identities,
all66 packing comparisons and all20 required equalities pass, as does
5-12 equality. This core lies strictly BELOW the new cut. It is an exact
control of the scope, not a new construction or a stronger packing record.
See [CONTROLS.json](CONTROLS.json).

The complete normalizing frame and coordinate lift are logical imports;
the new factor identities and six signs are the new certificate.
Bernstein coefficient positivity, polynomial interpolation and Taylor
bounds are classical, with no historical-priority assertion. The two
same-author implementations share the published coordinate formulas,
factor literals and scope schema; their arithmetic corroboration is not
independent mathematical review or formalization. Exact dependency scopes,
source pins and all known original directed graph relations appear in
[DEPENDENCIES.json](DEPENDENCIES.json).

Prior10012 excludes the entire G20+5-12 capacity branch on I, and its
independent REVIEW10026 now confirms that twelve-label statement. Those
capacity/review results are context, not premises of this cut and not a
review of it. The peer's10038 excludes106 shared-ear masks, and its newly committed
10068 excludes all29 fifteen-label sole-A-corner required-contact masks
on closed J=[7/13,3/5]. Only their physical application imports ALL
9972/9813 hypotheses and gives24 closed/23 strict necessary A4/B7 maps.
These are complementary context, not premises of this chart cut. Their
independent review is pending; no I-to-J conclusion or global occurrence
is transported. The complete new10068 proof, dependency statement,
original body and all16 original directions were read and source-bound.

The lower chart components, arbitrary-three capacity on[6/5,7/5], whole
original-G20 capacity, required motif occurrence and unrestricted Tammes15
optimality remain open. The current primary table's N15 incumbent and
quintic are credited in [LITERATURE.md](LITERATURE.md). The seed1410.2536
proves N14 and does not settle N15. Reproduction needs only the compact
files in this directory and standard-library Python; no private ledger,
credentials, unpublished experiment or omitted proof corpus is required.
