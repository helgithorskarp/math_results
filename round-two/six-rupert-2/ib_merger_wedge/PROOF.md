# J74: finite I/B merger collars and existence of a full-source receiving sector

**six-rupert-2, researcher; 2026-10-03.** Ordinary proof with exact finite
coefficients. Author checked, unformalized and independently unreviewed.
The global Rupert property of the original Johnson solid J74 remains open.

This packet proves two different statements. The I/B collar and its complete
fixed-parent shadow equality have the explicit receiving bound below. The
full-source corollary has **some smaller positive bound whose value is not
computed**. It uses the already published full classification at the single
receiver q and the published G/HB finite collars as mathematical premises.
The old source-entry enumeration and G/HB coefficient checks are not rerun.

## Original coordinates and the two statements

Let s=sqrt(5)>0, a=(s-1)/4, b=(s+1)/4, c=1/2,
t=(3-s)/2, qx=(s-1)/2. Let K=conv(V0,...,V59) be the original
unit-edge metabigyrate rhombicosidodecahedron J74. Its two nonopposite
gyrated cupolas are reconstructed from the pinned [model8551](../model.py),
source `25fc9695745b6832d068d18544452b7852b5847f`.

Set

```
H=diag(-1,-1,1),  Mx=diag(-1,1,1),  My=diag(1,-1,1),
B=((-a,-c,-b),( c,-b, a),(-b,-a, c)),
G=(( a,-c,-b),(-c,-b, a),(-b, a,-c)).
```

I,H,B,G,HB are proper. Only H,Mx,My are asserted to act on the entire
original body; B and G are not folded into body symmetries.
Every original has squared spatial radius R^2=(11+4s)/4.
The three independent antipodal pairs (0,7),(1,6),(2,5) put zero in the
interior of K, without assuming that K itself is centrally symmetric.

For 0<=eta<=epsilon put

$$
 r=(qx-\epsilon,1,-t-\eta),\quad
 P_r=I-rr^t/(r^tr),\quad M_r=I-2rr^t/(r^tr),\quad
 J_r(Q)=M_rQM_y.
$$

Keep the original physical T in r-perp and original lambda>=1 in

$$ \lambda P_r(QK)+T\subseteq P_rK. \tag{1} $$

The source Q ranges over SO(3). Write

$$
 \delta=1/905077199000,\qquad \rho=1/1000,\qquad
 E_{IB}(r)=\{I,H,B,BH,J_r(I),J_r(H),J_r(B),J_r(BH)\}.
$$

All motion families are sets, retaining merger duplicates.

**Explicit conditional collar.** On the entire closed wedge
0<=eta<=epsilon<=delta, if

$$ \operatorname{tr}(Qe^t)\ge2999999/1000001
       \quad\text{for some }e\in E_{IB}(r), \tag{2} $$

then (1) holds if and only if lambda=1, T=0, Q in E_IB(r).
This is exactly the closed physical relative Cayley radius rho, equivalently
squared Frobenius distance at most 8/1000001. Every such shadow equals
the receiving shadow; in particular it touches its boundary.

For A=G or HB put E_A(r)={A,AH,J_r(A),J_r(AH)}. The published
[G10093/6](../halfturn_merger_wedge/PROOF.md), source
`c6c32dc036534de446baa559d7456418198785e6`, and
[HB10107/0](../hb_merger_wedge/PROOF.md), source
`d176058ada1350f135c5931f84b64d9b946e879f`, prove on the same explicit
closed receiving wedge and physical rho gate that their fits occur exactly
when eta=0, lambda=1, T=0, Q in E_A(r).

**Full-source existence corollary.** There exists a number
0<delta_star<=delta such that, for every
0<=eta<=epsilon<=delta_star, (1) for arbitrary original Q,T,lambda holds
if and only if

$$
 \lambda=1,\quad T=0,\quad
 Q\in E_{IB}(r)\ \cup\
 \begin{cases}E_G(r)\cup E_{HB}(r),&\eta=0,\\
                 \varnothing,&\eta>0.\end{cases} \tag{3}
$$

There is no source proximity premise in this corollary. **No numerical
value, effective lower bound or claim delta_star=delta is supplied.**
Every allowed fit touches an actual receiving support line. Thus this
receiving sector supplies no strict Rupert passage. Receivers elsewhere,
including the remainder of the full receiving sphere, remain unclassified.

## Thirty genuine persistent contacts and their finite weights

The following fifteen oriented original supports remain genuine on the
entire closed explicit wedge:

```
13->31, 31->43, 43->7, 39->47, 47->11, 11->10, 10->28,
28->36, 36->0, 0->4, 4->20, 20->40, 40->48, 48->12, 12->13.
```

Use both spatial endpoints of each edge, giving thirty distinct literal
contacts. For each (i,j,k) with k=i or j set

$$
 m_{ij}=r\times(V_j-V_i),\quad h_{ij}=m_{ij}\cdot V_k,
 \quad N_{ij}=m_{ij}/h_{ij},\quad \tau_{ijk}=V_k\times N_{ij}.
$$

[certificate.json](certificate.json) lists all original labels and each
literal B-source preimage of V_k. The checker verifies every preimage as
a spatial equality, not only as a projected contact. For I the preimage is
k. Hence any fit close to I or B supplies these same actual endpoint
inequalities. No full-body I/B identity is assumed.

Each raw support gap is affine in epsilon,eta. Its values at
(0,0),(delta,0),(delta,delta) are nonnegative for every one of the
sixty originals. All ninety selected heights are positive. These 5,400
original receiving comparisons justify the selected supports on the
entire closed triangle, including q. The two eta=0 silhouette supports
7->3 and 3->39 fail inside the wedge and are **not** selected contacts.
The selected normals have no zero q normal; the full receiving proof below
separately retains its two real zero q normals.

For each of the six targets -ex,+ex,-ey,+ey,-ez,+ez construct positive
raw weights u_l satisfying

$$
 \sum_lu_l(V_{k_l}\times m_l)=\pm e_j,
 \qquad \sum_lu_lm_l=0. \tag{4}
$$

Here all thirty u_l are at least the strictly positive base 1/10000.
Five weights per target receive an additional rational correction. Let
M have their five columns (V_k cross m,m_x,m_z). In the homogeneous
barycentric coordinates of the closed receiving triangle, M is linear.
Its determinant D has degree five. Solve

$$
 Mz=\pm e_j-(1/10000)\sum_{l=1}^{30}(V_{k_l}\times m_l,m_{lx},m_{lz})^t.
$$

After homogenization the right side is linear, so all five Cramer
numerators also have degree five. Every determinant and numerator
Bernstein control is strictly positive after the common exact orientation
choice. These identities give (4) on the whole triangle. Since every
m_l is perpendicular to r and r_y=1, zero x and z force also imply zero
y force; that third force is independently checked as a polynomial identity.

Let beta_l=u_l h_l. Then beta_l>0 and
sum beta_l tau_l=+-e_j, sum beta_l N_l=0. The signed normalized
mass bounds are respectively

$$ 15,\ 9,\ 3,\ 24,\ 4,\ 47. \tag{5} $$

The controls of (bound*D-sum_l u_l h_l D), homogenized to degree six,
are strictly positive. There are, per target, 21 determinant controls,
105 numerator controls and 28 mass controls: **924 strictly positive
controls in total**. Thirty-six torque/force identities and twenty-four
full independent exact Gaussian determinant/inverse fixtures are checked.
The fixed literal column labels came from a private exact LP scout with
verified original primal and dual equations. Production uses no LP solver,
floating input, private scout or earlier collar coefficients.

The selected normal span is not inferred from row rank alone. The exact
two-component determinant of m(13,31),m(31,43) has six strictly positive
oriented degree-two controls. Thus these genuine normals span the entire
receiving plane throughout the closed wedge.

## Rotation, original scale and original physical translation

Write Q=R(d)A about A=I or B with physical left Cayley vector d,
where R(d)=((1-|d|^2)I+2dd^t+2[d]_cross)/(1+|d|^2).
Every original contact satisfies N dot V=1. Fresh corner checks give

$$
 R^2\|N\|^2\le5/3-2s/9<121/100.
$$

At a convex combination of raw receiver corners, the normalized normal
is a convex combination of corner normalized normals with weights
barycentric_weight*h_corner/h. Hence R||N||<11/10 over the whole
closure. The smaller eigenvalue of (NV^t+VN^t)/2 is
(1-R||N||)/2, so

$$ \|d\|^2-(N\cdot d)(V\cdot d)\le C\|d\|^2,
       \qquad C=21/20. \tag{6} $$

Put b0=T/lambda. Apply (1) to the literal source preimage of V. Then

$$ N\cdot R(d)V+N\cdot b_0\le1/\lambda\le1. $$

The full identity in three free Cayley variables is

$$
 (1+\|d\|^2)(N\cdot R(d)V-1)
 =2(V\times N)\cdot d+2(N\cdot d)(V\cdot d)-2\|d\|^2.
 \tag{7}
$$

All ninety literal original endpoint identities are regenerated. Multiply
their inequalities by either signed set of positive beta_l. Actual
translation cancels in all three coordinates by (4). Equations (5)--(7)
give

$$ |d_x|\le15C\|d\|^2,\quad
    |d_y|\le24C\|d\|^2,\quad |d_z|\le47C\|d\|^2. $$

If 0<||d||<=1/1000, summing the squares would give

$$
 1\le C^2(15^2+24^2+47^2)\|d\|^2
 \le132741/40000000<1.
$$

Consequently d=0 and Q=A. At this center the same contacts imply
N_l dot b0 <=1/lambda-1. A positive weighted zero-force sum forces
lambda<=1; therefore the original lambda=1. Now N_l dot T<=0 for
every selected contact. All beta_l are strictly positive and sum beta_l N_l=0,
so every one of these inequalities is an equality. The verified two-normal
span gives T parallel to r; the original physical T in r-perp gives T=0.
No source dilation or translation recentering is substituted for (1).

At q this also checks the complete selected first-order obstruction for
I and B: adding all six raw-weight vectors gives a strictly positive
annihilator of the three torque and two physical screen-translation rows.
Its scale column is strictly positive. Any necessary homogeneous source
contact inequality with nonnegative scale derivative therefore has zero
scale derivative and all contact rows zero. The five-column determinant
has nonzero q value, so all three rotation and both translation derivatives
are zero. Receiving derivatives have zero right side for these spatial
endpoint contacts and remain free within the permitted receiving cone.
The translation screen coordinates are representatives modulo span(r),
an invertible coordinate map on physical r-perp. This first-order fact
alone is not the finite proof; (6)--(7) and the explicit absorption are.

## Complete B shadow equality on the two genuine receiving cells

Use the original rank-two screen
Pi(V)=(Vx-(qx-epsilon)Vy,Vz+(t+eta)Vy). Its kernel is exactly span(r),
and its restriction to r-perp is an isomorphism. In these coordinates

$$
 h_{ij}-m_{ij}\cdot W
 =\det(\Pi(V_j-V_i),\Pi(W-V_i)). \tag{8}
$$

The actual affine support against source V55 on edge27->3 is

$$ ((s-1)/4)\epsilon-((s+1)/4)\eta. $$

It gives the genuine fan wall eta=t epsilon. The whole closed wedge
is the union of the closed triangles with corners
(0,0),(delta,0),(delta,t delta) and
(0,0),(delta,t delta),(delta,delta). Their eighteen-corner interior cycles are

```
13,31,43,7,27,3,39,47,11,10,28,36,0,4,20,40,48,12
13,31,43,7,27,55,39,47,11,10,28,36,0,4,20,40,48,12
```

All support gaps against all sixty original receiving vertices and all
sixty literal B vertices are checked at all three corners of both cells:
**12,960 affine controls**. Every adjacent turn is affine, nonnegative at
the corners and positive at some corner. Every height has the same property.
Thus each height and adjacent turn is positive throughout the relative
interior of its cell. All original pairs are checked by their unique possible
coincidence receiver: if the spatial Vy difference is nonzero, a coincidence
would require x=delta_Vx/delta_Vy, y=-delta_Vz/delta_Vy; if Vy difference
is zero, one projected component is permanently nonzero. No pair coalesces
anywhere on 0<epsilon<=delta, 0<=eta<=epsilon. All 1,770 pair records
are regenerated, with actual q coincidences retained.

For an interior receiver, each cycle vertex lies on two independent
actual supporting lines and is extreme. Each successive segment is an
exposed hull edge. These eighteen edges therefore describe the full
receiving convex polygon. Equation (8) proves that the complete B shadow
is contained in it. Each of its eighteen receiving vertices has a literal
spatial original B preimage, also regenerated. Hence the reverse inclusion
holds and P_r(BK)=P_rK throughout both relative interiors. Continuity of
the finitely generated projected convex hulls extends equality to every
closed boundary, including eta=0, the fan wall, eta=epsilon and q.

The raw normals on 27->3 and 55->39 really vanish at q and are kept
with their zero heights. They are not divided by at q. No eighteen-corner
strict or distinct q hull is asserted. Independently the actual thirteen-corner
q cycle is

```
13,31,7,3,39,47,10,28,0,4,20,40,48
```

All thirteen turns and projected vertices are strictly positive/distinct,
all 1,560 original receiver/B q gaps are nonnegative, and all 14,520
spatial/planar comparisons for these and the two cells agree exactly.
At q there are forty-two distinct projected originals. These checks give
the full converse for I/B rather than relying on the fifteen selected
supports to describe the complete receiving polygon.

Right H preserves the actual source body. Since My preserves K and
P_r M_r=P_r, the map J_r preserves the projected source, the same
physical T, and the same lambda. It is an involution on proper motions.
Relative Cayley trace is preserved by its conjugation identity. Thus the
I/B argument transfers to H,BH and every J_r companion, proving (2).
The proper Cayley trace and squared Frobenius formulas give the stated gates.

## Full-source entry by compactness, with an unspecified receiving radius

The mathematical premise at q is the **full** arbitrary-source result
of [joint9918](../joint_phase4/PROOF.md), source
`82e94dc282701d753065b9b0e771a0ff715b55bd`:
every original SO(3), physical T, lambda>=1 closed fit at q has
lambda=1, T=0, and belongs to the finite set

$$
 E_0=F\cup\{M_q A M_x:A\in F\},\quad
 F=\{I,H,B,BH,G,GH,HB,HBH\}.
$$

This is imported as an ordinary theorem, not established by a new sampled
q LP or source forest. Because Mx=My H and F is closed under right H,
E0 equals the q specialization of
E_IB(r) union E_G(r) union E_HB(r). The checker compares these complete
matrix sets exactly. No distinct-branch assumption is used. Every member
has a continuous named extension to a center in this union as r tends to q.

Choose r_in>0 with the spatial ball B(0,r_in) contained in K. Such a
positive r_in exists from the verified independent antipodal pairs.
Every receiver and every rotated source contain projected disks of radius
r_in. Since the receiver is contained in a disk of radius R, any fit (1)
satisfies lambda<=R/r_in. Also 0 is in the source, so T belongs to
P_rK and ||T||<=R. Therefore SO(3), the allowable scale interval and
the allowable world translations form a compact ambient parameter set.

Suppose there were no positive receiving bound ensuring entry into the
union of the closed rho collars. For each integer j choose a fit with
0<=eta_j<=epsilon_j<=min(delta,1/j) outside every such collar.
Extract a subsequence Q_j->Q0, lambda_j->lambda0, T_j->T0.
The receiving projectors tend to P_q, physicality passes to the limit,
and finite-vertex containment is closed. Thus the limit is a fit at q.
The imported theorem gives Q0 in E0, lambda0=1, T0=0.
Choose a continuous center e(r) with e(q)=Q0. Then
tr(Q_j e(r_j)^t)->3, so eventually the relative trace exceeds
2999999/1000001. This contradicts the choice outside all closed collars.

Consequently some delta_star>0, reduced to at most delta, makes every
original fit enter the completed I/B,G,HB collar union. The I/B theorem
above and the explicitly imported G/HB theorems give exactly (3), including
every touching eta=0 fit and every q merger. Their converses supply every
listed fit. This proof asserts existence, not an algorithm or effective
positive lower bound for delta_star. In particular the explicit delta
proved for each individual collar is not an entry bound.

## Reproduction and mathematical dependencies

With CPython3.11.2 and only its standard library, from the public repository:

```bash
python3 round-two/six-rupert-2/ib_merger_wedge/check.py --output /tmp/j74-ib.json
python3 -O round-two/six-rupert-2/ib_merger_wedge/check.py --output /tmp/j74-ib-O.json
python3 round-two/six-rupert-2/ib_merger_wedge/controls.py --output /tmp/j74-ib-controls.json
```

The checker needs only its own compact directory and the before-import
pinned original model.py/q5.py. EXPECTED.json contains the whole compact
mathematical record. `--transcript` can regenerate every literal gap,
coefficient and pair record into a separate scratch file; these verbose
outputs are omitted from publication. `--emit` skips only the fixed
EXPECTED comparison, never an original mathematical gate. Semantic false
fixtures consult neither EXPECTED nor fingerprints. The validation receipt
records normal/optimized and fresh empty relocation checks and resources.

Ordered-field arithmetic is credited to the published code7140. Small
determinant/Cramer/Bernstein algorithms are adapted with attribution from
[local9677](../whole_phase56_collar/algebra.py) and
[local9918](../phase4_contacts/duals.py), and the free-variable polynomial
helpers from [HB10107](../hb_merger_wedge/polynomial.py). The old D4
contact stencils, bounds and region are not transferred. No novelty is
claimed for these classical algorithms or compactness itself.
The three external mathematical premises for (3), and the distinction
between runtime and ordinary dependencies, are recorded in DEPENDENCIES.json.

Primary status refreshed2026-10-03: [Gosain--Grimmer Table4](https://arxiv.org/html/2509.08190#S3.T4)
retains J72,J73,J74,J75,J77 as unresolved Johnson solids.
[Zeng Section1.2](https://arxiv.org/html/2604.26531#S1.SS2) reports87 of92
Johnson solids Rupert and retains the RID negative assertion as a conjecture.
The [Noperthedron theorem](https://arxiv.org/abs/2508.18475) concerns a
different solid. A failed or timed-out search is not a nonexistence proof.
This is a regional lemma and noneffective continuation corollary, not a
global non-Rupert proof of J74 or a passage construction.
