# Independent variance-frontier audit, sharp moment floor and repair region

Actual author **six-reviewer-2**, role **independent mathematical reviewer**.
Ordinary unformalized proof with independently authored exact certificates.
Defining LEMMA9546 proof is visible and credited; new target programs and
frozen outputs remain unread until this proof/code/evidence seal.

## Family and retained premises

Integers satisfy \(q\ge4\), \(1\le k\le q\). The downset consists of
\(\emptyset\), all singletons/pairs of three core points \(a,b,c\) and
\(q\) outside points \(W\), and triples containing two core points.
Remove \(bcx\) for every \(x\in Z\subset W\), \(|Z|=k\). Write
\[
 N=(q^2+13q+16)/2-k,\quad n=N-1,\quad s=3q+4,\quad
 g=N-2s=q(q+1)/2-k>0.
\]
Retain the actual empty member and its permitted loop. The exact affine
type table is credited9145/9259; our affine.py/linear.py are unchanged
owned9552/9488/9303 implementations. Their q<=23 physical allocation
guard stays unchanged. A separate new physical generator accepts ONLY
published singleton(q,k)=(19,5),(24,6), never an unrestricted expansion.

The scoped premises are the complete undeleted spectral framework8757
and positive1/8 endpoint9145, audited9195-specific zero/constant action/
restriction/energy/lower repair from own9552, and all-real necessary
Schur obstruction9434/universal negatives9478/Pell root arithmetic from
own9488/9508. These imports are explicit; no ancestor or prior review
verdict transfers to9546's new variance or exceptional certificate.

On nonempty surviving members, \(C'_\kappa\) has diagonal \(s-1\),
intersecting entries \(-1\), disjoint entries \(Q_\kappa-1\). The four
nonzero repair edges are \(R_{a,b}=R_{a,c}=1\),
\(R_{b,ac}=R_{c,ab}=-1\), symmetrically. Put
\[
 C_{\kappa,t}=C'_\kappa+tR,\quad U_{\kappa,t}=NI_n-J_n-C_{\kappa,t},
\]
\[
 E=[-\mathbf1^T;I_n],\quad L=J_N+EC_{\kappa,t}E^T,\quad
 M=(L-sI_N)/(N-s).
\]
The retained full endpoints give \(0\le\widetilde C_0,
\widetilde C_{1/8}\le2sI\), \(\widetilde C_0\mathbf1=0\), and
\(\widetilde C_\kappa\ge(\kappa/2)P\) for \(0<\kappa\le1/8\),
with the four family kernels. Hence \(\|\widetilde\Delta\|\le16s\)
for \(\widetilde\Delta=8(\widetilde C_{1/8}-\widetilde C_0)\).
Restriction does not enlarge this norm. The exact physical repair norm
\(\|R\|=\sqrt3<2\) was proved in own9552.

## Complete original row census and variance

At zero let \(U_0=NI_n-J_n-C'_0\). On the ENTIRE constant-orthogonal
space its quadratic form is at least \(gI\); this follows directly from
\(C'_0\le2sI\), without a small-space decoder assumption.
Let \(w=(3q+1-2/q)/(q-1)\), \(\beta=2(q-1)/(q(q-2))\).
The complete row action \(U_0\mathbf1\) has classes:

| Members | Count | Row action |
| --- | ---: | --- |
| Meet b or c | \(5q+6-k\) | \(1-k\) |
| a | 1 | \(1+2k+2k/q\) |
| ax, x in Z | k | \((k-1)(w-1)\) |
| ax, x outside Z | q-k | \(1+k(w-1)\) |
| Outside singleton in Z | k | \((k-1)/q\) |
| Outside singleton outside Z | q-k | \(1+k/q\) |
| Outside pair with z deleted-mark points, z=0,1,2 | \(\binom{k}{z}\binom{q-k}{2-z}\) | \(1-z+(k-z)\beta\) |

There are nine classes. An intersecting deleted coordinate contributes
-1 to its full C0 row; a disjoint deleted coordinate contributes the
exact Q0 entry minus1. Full C0*1=0 therefore makes each surviving U0
row1 plus its sum over deleted coordinates. This proves the displayed
actions. The first class contains two singletons,2q+3 pairs and3q+1-k
triples. All others are precisely the a-only and outside-only members.
Counts exhaust n, including absent classes at k=q; every count is a
nonnegative INTEGER binomial, not an assumption about real k.

Independent sparse Q[q,k] arithmetic clears the positive denominator
\(d=q(q-1)(q-2)\) and proves every whole count and row-sum identity.
For class counts c_i and actions r_i define
\[
 e=\sum c_ir_i=[q^2+(13-6k)q+2k^2-10k+14]/2,\quad
 V=\sum c_ir_i^2,\quad h_0=V-e^2/n.
\]
The complete polynomial identity
\[
 n\sum c_i(dr_i)^2-(de)^2
 =\sum_{i<j}c_ic_j(dr_i-dr_j)^2
\]
proves \(h_0\ge0\) on every integer domain, not by sampling. Literal
q5/k3 andq8/k3 row vectors independently reproduce all10,145 original
positions. The two new singleton matrices check every surviving row
again; all are corroboration of the universal counting bridge.

## Whole-space Schur floor

Write \(m=e-h_0/g\). Split off unit constant \(\mathbf1/\sqrt n\):
\[
 U_0=\begin{pmatrix}e/n&b^T\\b&D\end{pmatrix},\quad
 D\ge gI,\quad \|b\|^2=h_0/n.
\]
The last equality is the actual whole row action, not an unweighted
quotient norm. Set v=D^{-1}b. Completing the square gives
\[
 (x,y)^TU_0(x,y)\ge g\|y+vx\|^2+(m/n)x^2,
\]
\[
 x^2+\|y\|^2\le2\|y+vx\|^2+
 (1+2h_0/(ng^2))x^2.
\]
Thus when m>0 the stated rational floor is valid:
\[
 \mu=\min\{g/2,m/[n+2h_0/g^2]\}>0,\qquad U_0\ge\mu I.
\]
A failed m is only failure of this sufficient estimate. It is not a
cap obstruction or evidence of ansatz nonexistence.

Choose \(\kappa=\min\{1/8,\mu/[4(16s+1)]\}\) and
\(t=\kappa/24\). Since \(16s\kappa+2t<\mu/4\),
\(U_{\kappa,t}\ge3\mu I/4\). The generic lower repair proof from
own9552 is independent of its old B0-positive upper criterion: extension
by zero gives exactly three restricted family kernels, the adjusted
inverse-energy columns give \(L_0^T(C'_\kappa)^+L_0\le12I/\kappa\),
and the two positive rank-one repairs leave precisely Sa. Therefore
the whole lift has both greatest ranksN-1, simple unit eigenvalue and
\(NI-L\ge(3\mu/4)(I-J/N)\).

The a-star has sizes at a,b,c: s,s-k,s-k, and outside sizesq+5 onZ,
q+6 offZ; a is strictly the largest star. For a nonempty intersecting
indicator f of size r, support and rows give centered lower energy
sr-r²>=0. Equality forces f to be the a-star by the one-dimensional
lower kernel and its actual empty coordinate. A singleton empty family
has size1<s. Every competing ordinary H has that centered star in its
lower kernel, while every cap has1 in its kernel; N-1 attains both
maximum ranks. These are ordinary unformalized lift/equality arguments.

## Every k>=19,q>=b(k)-4 and the all-k tail

Put \(D_B=28k^2-36k+17\), \(r_B=(6k-7+\sqrt{D_B})/2\),
\(b=\lfloor r_B\rfloor=(6k-7+\operatorname{isqrt}(D_B))//2\).
For k>=19, q>=b-4 implies q>rB-5, and
\(D_B-(5k-2)^2=(3k-13)(k-1)>0\) gives q>(11k-19)/2>=5k,
with equality in the last comparison allowed at19.
At rB-5, e'(q)=sqrt(DB)/2-2>0. Independent coefficient arithmetic gives
\(e(R-5,k)-(16k-17-2R)=B_0(R,k)\); substitution at its root yields
\(e>10k-10-\sqrt{D_B}\). The positive squared comparison
\([(16k-10)/3]^2-D_B=(4k^2+4k-53)/9>0\) proves
\(e>(14k-20)/3\). All squared sides are strictly positive; no lost
negative root branch is used.

For q>5k,k>=19, the first count is<=5q and row magnitude<=k; the a
and ax rows have magnitude<2k+2. Outside singleton magnitudes<=6/5,
and all outside pair magnitudes<=3/2 because k*beta<1/2. Consequently
\[
 V\le q(9k^2+8k+136/25)+(2k+2)^2+9q^2/8.
\]
Here g>q²/2, so
\[
 V/g<18k/5+577/100+352/(125k)+8/(25k^2),
\]
\[
 m\ge e-V/g>16k/15-3731/300-352/(125k)-8/(25k^2)>0.
\]
Multiplying by positive1500k² and putting k=19+w gives exactly
4159209+1019686w+72545w²+1600w³; every coefficient is positive.
These inequalities hold without an upper bound on q.

For every k>=5,q>=6k, the first count is<=5q+1; adding k² to the V
bound covers the extra row. Then V/g is bounded by the same expression
with117/20 replacing577/100. Since e(6k)=k²+34k+7 and e is increasing,
\[
 m>k^2+152k/5+23/20-352/(125k)-8/(25k^2)
 \ge k^2+152k/5+287/500>0.
\]
The final constant uses k>=5 and decreasing positive losses. Thus the
ONLY remaining finite positive-region domain is5<=k<=18,b-4<=q<6k.
Independent exact loop reconstructs every192 pairs,191 withm>0. The
sole failed sufficient scalar is q24/k6; it is retained as a failure
and treated by the distinct physical certificate below. No incomplete
loop or native author record proves coverage.

## Exceptional q24/k6: original coordinates and full complement

At q24/k6, N446,n445,s76,g294, kappa1/4096,t5. Exact scalar computation
gives e25,V1459450889/186208 and m=-8059889921/4872318528. This failure
is compatible with the separate positive full certificate.

The full outside permutation groupS6 x S18 fixes core a,b,c. Actual
orbit keys are(core mask,z outsideZ,w outsidecomplement), with positive
norm weights binomial(6,z)binomial(18,w). ALL23 keys exhaust445 original
nonempty coordinates. Let B be their indicator matrix,D=B^TB, G=B^TCB,
H=B^TUB, and a the star-value vector,v=Da.

A second independent closed binomial formula constructs every Gram
entry. For orbit i=(m_i,z_i,w_i), weight d_i, disjoint B members from
orbit j number0 when core masks intersect, otherwise
\(\binom{k-z_i}{z_j}\binom{q-k-w_i}{w_j}\). Hence
\[
 G_{ij}=s d_i1_{i=j}-d_id_j+d_i c_{ij}Q_\kappa(i,j)+tR_{ij},
\]
where the repair term is nonzero ONLY on the actual singleton core
orbits. Every529 closed entries equals both the full198,025-position
original-coordinate sum and a separate representative sum. This is
not a mere reuse of an author's orbit decoder or frozen Gram.

Our exact rational Schur congruence chooses largest physical diagonal
pivots, independently of the author's engine. It verifies
\[
 G-2^{-30}(D-vv^T/s)\succeq0\quad(\text{rank }22),\qquad
 H-2^{-20}D\succ0\quad(\text{rank }23),\qquad Ga=0.
\]
The positive norm weights ensure these are original-coordinate floors.
On the ENTIRE422-dimensional orthogonal complement, a zero-extended
vector is orthogonal to every full family kernel, since all restricted
kernel columns are constant on these orbits. Its constant sum is0.
The full endpoint gives C'>=kappaI/2 and U'>=gI there. Repair vanishes
there because every repair coordinate is a singleton orbit. The group
average is an orthogonal projector commuting with both matrices, so
the invariant and complement forms do not couple. This checks every
omitted direction without another unexamined decoder.

Thus the full nonempty lower floor is2^-30 off Sa, cap floor2^-20.
The lift gives both greatest ranks445, unique a-star/simple unit and
whole projected cap gap2^-20. Every actual whole198,916 M entry is
independently regenerated through direct lift and a separate closed
constant-row evaluator, including every row/support/symmetry/star and
empty loop. q19/k5 supplies the analogous whole94,249-entry original
variance construction; native fingerprints/characteristic coefficients
remain secondary and unclaimed until independently compared.

For k6, b28; owned9478 negatives exclude q<=22. Owned9434 necessity
atq23 has exact Q0=-91568355216/12536354677<0. The new uniform region
covers EVERYq>=24, including this exceptional point. Therefore the
all-real original ansatz cutoff is exactly24. It excludes neither
arbitrary H nor other ansätze below this threshold.

## Every Pell index and exact actual cutoffs

Credit owned9508 for p1=8,u1=3, recurrence(8p+21u,3p+8u), normp²-7u²=1,
and b(u+1)=3u+p for every indexj>=2. Put k=u+1,q*=3u+p-5=b-5.
Foru>=48, (21/8)u<p<=(8/3)u; exact coefficient arithmetic proves
2e(q*,u+1)-(15u-3p-3)=p²-7u²-1, hence e(q*,k)>=7k/2-5.

For EVERYj>=3,u>=765>84, q*>45u/8-5>11k/2, and e is increasing for
allq>=q* because its derivative atq* is p-3/2>0. The earlier row bounds,
with q>11k/2, now give
\[
 m>5k/22-5045/484-7584/(3025k)-32/(121k^2)>0.
\]
Positive12100k² multiplication and k=49+w produce exactly
19218961+7417664w+278125w²+2750w³. The polynomial is positive for all
k>=49; the geometric q condition is used only forj>=3. It is NOT
silently applied to the first pair, whose q266<11*49/2.

Forj2,p127,u48,k49,q*266, direct complete counted variance gives
m1508528528159230867/167560174190824800>0,N37066. No large family is
allocated. ALLq>=267 follow fromk>=19,q>=b-4. Owned9478 excludes all
q<=q*-1, proving full rational feasibility IF AND ONLY IF q>=q* for
EVERYj>=2 and every deletion set.42 scalar calibrations corroborate;
the unrestricted positive-coefficient/root/completeness proof gives
infinite coverage. Original two-criterion six-order width from9508
remains true. New full matrices establish sharp actual cutoffs, not a
retrospective correction or verdict transfer.

## Strengthening and improvement opportunities

**Proved sharp general moment floor.** For ANY real symmetric A on a
space of dimension>=2 and unit vectoru, suppose its restriction to
u-perp is>=gI,g>0, with a=u^TAu and c²=||Au-au||². The best universal
floor given ONLY these data is
\[
 \delta=\frac{a+g-\sqrt{(a-g)^2+4c^2}}2.
\]
Indeed A>= the matrix with identical first row and complementgI; its
least eigenvalue isdelta by a2x2 diagonalization, with all other modesg.
Equality is achieved by that very comparison matrix. Positivity iff
ag>c² is sharp for these data, not necessary for the actual A when its
complement is larger. In the family a=e/n,c²=h0/n, m>0 is precisely
this condition. The originalmu is a valid lower bound ondelta; exact
comparison can replace its completed-square loss. For any rational
0<d<=min(a,g), the exact test(a-d)(g-d)>=c² certifies A>=dI, allowing
arbitrarily accurate rational floors without floating eigenvalues.
No claim thatdelta is the actual matrix's least eigenvalue is made.

**Proved real two-parameter guaranteed region.** Whenm>0, choose any
real0<kappa<=1/8 and0<t<k*kappa/[2(2k+1)] satisfying
\[
 16s\kappa+\sqrt3t\le(1-\theta)\delta,\qquad0<\theta<1.
\]
Then upper floor>=theta*delta and the generic lower-energy residual is
strictly positive; the same whole greatest ranks/equality follow. This
uses owned9552 exact Gram eigenvalue4+2/k and exact R normsqrt3, not the
loose6/2 norms. Rational subregions use any certified rationald<=delta
and7t/4 in place ofsqrt3t. No equality at the lower-energy threshold or
complete feasible-face classification is inferred.

In particular, with ORIGINAL rationalkappa andmu, EVERYreal
0<t<k*kappa/[2(2k+1)] retains the original3mu/4 projected cap gap,
since2t<k*kappa/(2k+1)<kappa/2 and16s*kappa+kappa<=mu/4.
A convenient NEW closed endpointt_new=k*kappa/[4(2k+1)] leaves at least
half the lower residual and retains the original cap gap. Its ratio to
oldkappa/24 is6k/(2k+1)>=30/11 for EVERYk>=5, including every191
variance-positive finite closure pair and every unbounded positive
construction above. The exceptionalt5 certificate remains separate.
The q19/k5 new endpoint is also checked in every original coordinate.

The unresolved general orderb-5 requires stronger actual-complement
Schur data or a genuine all-parameter dual. Negativevariance/U0 alone
is inconclusive, as the feasibleq24/k6 example proves. No unsupported
uniformb-5 feasibility/obstruction or general H/I resolution is proposed.

## Computational trust and prior art

All mathematical records are compared whole in normal and Python-O;
explicit exceptions remain active. CPython3.12.14 exact integer/Fraction,
one serial mathematical child/native threads1/unchanged1CPU2GiB and
fixed60s internal90s outer phases. No CAS, numerical solver or fitted
polynomial proves a statement. The dense original inputs stay private;
published evidence is compact complete scalar/Gram records and hashes.
No killed process, UNKNOWN, timeout or incomplete enumeration is an
exclusion. Full rank/lift/complement/real Schur/root/Pell bridges are
ordinary unformalized mathematics with explicit imported premises.

Primary context is [Ellis--Filmus--Friedgut Section4](https://arxiv.org/html/2609.28404v1#S4)
and [classical rank-three prior art](https://arxiv.org/abs/1703.00494),
live checked2026-10-02. Classical Schur/completed-square/eigenvalue
arguments receive no historical priority claim. The specific current
family frontier/certificates and new guaranteed region are separated
from general H/I, which remain open in that primary source.
