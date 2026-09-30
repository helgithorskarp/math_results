# Orthogonal transports sharpen the RID source bound and certify a piecewise receiver cover

**six-rupert-3 — researcher — 2026-09-30.**

The normal transports in the source reduction have axes perpendicular to
the reference normal. The intervening roll has that normal as its axis.
Using this structure gives the full rotation-chord bound

\[
                   \|Q-I\|\le\sqrt{(a+\delta)^2+E^2},               \tag{1}
\]

in place of the earlier sum of three factor angles. The resulting receiver
criterion includes the entire preceding actual-torque-hull criterion.
A four-piece certificate then excludes every source orientation on a larger
**closed** RID receiver triangle, including all its boundaries.

The new triangle contains the preceding one and has **90/49 times its
unit-z chart area**. Its left corner's normal chord is greater than **1/40**
from the threefold center. Every piece's actual torque ball clears the
full rotation remainder by more than **2/25**. Source normal, full original
rotation, roll, translation and scale at least one are unrestricted.
The global Rupert property of the rhombicosidodecahedron remains **open**.

This is a complete unformalized geometric proof with exact finite
hypotheses. Independent review is not asserted. The useful refinement is
the body-specific use of the structured composition bound and the exact
closed-piece receiver cover. No historical priority claim is made for
elementary quaternion identities or coefficient-sign certificates.

## 1. A structured rotation-composition lemma

Let `n0` be a unit vector. Let `U,V` be rotations about unit axes
perpendicular to `n0`, and `C` a rotation about `n0`. Include identity
factors by choosing any axis of the specified type. Write the three
operator chords as

\[
 d=\|U-I\|,\qquad e=\|C-I\|,\qquad a=\|V-I\|,
                    0\le a,d,e\le1/10.
\]

**Orthogonal-composition lemma.** For `Q=UCV`,

\[
 \|Q-I\|\le\sqrt{(a+d)^2+e^2}<1/4,\qquad
 \theta(Q)\le(101/100)\sqrt{(a+d)^2+e^2}.                            \tag{2}
\]

Here `theta` is the full principal proper rotation angle, not a planar
angle or normal chord. The operator chord of a proper rotation is
`2sin(theta/2)`.

Choose unit-quaternion lifts with nonnegative half-angle cosines. With
axes `x,y` perpendicular to `n0`, their factors are

\[
 q_U=(c_d,(d/2)x),\quad q_C=(c_e,sn_0),\quad
 q_V=(c_a,(a/2)y),\qquad c_t=\sqrt{1-t^2/4}.
\]

Signs of the transport rotations are absorbed in `x,y`. The roll has
signed half-angle sine `s`, with `|s|=e/2`. The scalar component of
their product is

\[
 w=c_dc_ec_a-\frac{ad}{4}
             \{c_e x\cdot y+s(x\times n_0)\cdot y\}.           \tag{3}
\]

Since `x` and `x cross n0` form an orthonormal pair in the perpendicular
plane, `c_e x+s(x cross n0)` is unit, including either roll sign. The braces are at most one.
Thus, putting

\[
 P=(1-d^2/4)(1-a^2/4)(1-e^2/4),\quad p=\sqrt P,\quad W=p-ad/4,
\]

we have `w>=W`. All factors are small: `P>=(399/400)^3>(99/100)^2`,
so `W>99/100-1/400>0`. The product lift is the positive principal lift.
The following exact polynomial identity proves the chord comparison:

\[
 \begin{split}
 (a+d)^2+e^2-4(1-W^2)
  &=2ad(1-p)+\frac{a^2d^2(8-e^2)}{16}
                  +\frac{e^2(a^2+d^2)}4\ge0.                     \tag{4}
 \end{split}
\]

Every term is nonnegative: `p<=1` and `e<=1/10`. Therefore
`||Q-I||^2=4(1-w^2)<=4(1-W^2)<=(a+d)^2+e^2`.
The last quantity is at most `1/20<1/16`. For chord `t<1/4`, the
derivative of `2arcsin(t/2)` is at most `8/sqrt(63)<101/100`, since
`(101/100)^2(63/64)>1`. This proves (2), including all zero cases.

The checker expands (4) as a four-variable rational polynomial identity
modulo `p^2=P`; it does not infer a general identity from sample values.
Eighty-one rational quaternion products also audit the scalar formula,
direct matrix products, trace/chord relation and inequality for both
rotation signs and identity factors. Those are arithmetic audits; the
continuous proof is (3)--(4) and the perpendicular-axis argument.

## 2. RID frame decomposition and the stronger receiver criterion

Use the standard edge-length-two sixty-vertex RID model `V`,
`K=conv(V)=-K`, `phi=(1+sqrt(5))/2`, `R=sqrt(7+8phi)` and the closed
unit-z chamber cell

\[
 A=(0,0,1),\quad B=(0,\phi^{-2},1),\quad
 D=\left(\frac1{\phi(\phi+2)},\frac1{\phi+2},1\right),\quad u\in ABD.
\]

For `n=u/||u||`, `n0=B/||B||`, put

\[
 \begin{split}
 F&=\min_{v\in V}|v\cdot n|,&c_0&=1/\sqrt3,&
 \beta&=(19-8\phi)/29,\quad\delta=\|n-n_0\|,\\
 a&=(101/200)(c_0-F),&
 E&=c_0a+\sqrt{5/3}\,\delta+\frac R2(a^2+\delta^2),\\
 \Theta_\perp&=(101/100)\sqrt{(a+\delta)^2+E^2}.
 \end{split}                                                       \tag{5}
\]

The [directional source reduction](DIRECTIONAL_TRANSPORT_PROOF.md),
source `30c9c86753797307cc17b56ffd76aa88d94987df`, graph
`bafkreihl44hhtwxjrezrxurevchfwpfgkeojhbl2ctkimksjg4efia346u`, supplies
the following construction when `F^2>beta` and `E<=77/1000`.
Diameter and winning-region coercivity gauge every possible source normal
by an actual proper body symmetry into normal chord at most `a` from `n0`.
Selected long-edge supports exclude remote roll and leave residual roll
chord at most `E`. Minimal transports `A1,A2` from `n0` to the source
and receiver normals and an actual proper axial body rotation `h` give

\[
 Q=A_2 S_0^t\operatorname{diag}(W,1)S_0(A_1')^t,
                   A_1'=h^tA_1h,\qquad hn_0=n_0.                  \tag{6}
\]

Here the rows of the proper frame `S0` complete the reference projection;
its third row is `n0`. A source planar half-turn is allowed by central
symmetry and preserves its cross-product normal. Equation (6) is precisely
the full proper frame relation in Section 5 of the directional proof.
It keeps the projected source set unchanged.

The axes of `A2` and `(A1')^t` are perpendicular to `n0`: minimal
normal transports have this property, inversion preserves it, and
conjugation by `h` preserves the perpendicular plane. The middle factor
rotates about `n0`. Their chords are bounded by `delta,E,a`.
The inherited global axial maximum gives `a>=0`. Also `F>2/5` and
`c0<7/12` imply `a<1111/12000<1/10`; `delta<E<=77/1000` unless zero.
Thus the lemma applies, and (5) bounds the full gauged angle.
No estimate of the form `US subset S+E Disk` is assumed: `E` remains
the parent's selected directional support-gap bound.

Use the ten persistent original endpoint probes from the
[actual-hull proof](ACTUAL_TORQUE_HULL_PROOF.md), source
`684f35df160134d1fefb14da75f5948ce8ac00ce`, graph
`bafkreiepyjhiavm5s4reqzgverqayeq6dhmjsof4g4xutfnsw7a6wafipm`.
Their length-two edges `ej` give supporting normals `mj=ej cross u`
at actual vertices `vj` throughout closed `ABD`. Define

\[
 T_j(u)=v_j\times(e_j\times u),\quad
 r_{10}(u)=\min_{\|z\|=1}\max_j z\cdot T_j(u).
\]

**Stronger all-source receiver criterion.** If

\[
        F^2>\beta,\qquad E\le77/1000,\qquad
                   r_{10}(u)>R\|u\|\Theta_\perp,                  \tag{7}
\]

then no strict containment `lambda P_n(Q_original K)+t subset int(P_n K)`
exists for any source proper rotation, planar translation and `lambda>=1`.
Central symmetry and convexity center and reduce scale while retaining
strict containment. For any positive gauged angle, the actual torque
support and exponential remainder give a positive original support
displacement, at least `theta(r10-R||u||theta)`, contradicting centered
closed containment. At zero angle the gauged shadows coincide and cannot
fit strictly. These are the actual-hull proof's arguments with the new
full-angle bound. Since `sqrt((a+delta)^2+E^2)<=a+delta+E`, (7) includes
the **entire** preceding actual-hull criterion, and consequently its
earlier directional criterion and closed `1/100` threefold caps.

## 3. Closed receiver cover with separate phase and torque bounds

Set

\[
 U_0=B,\qquad U_1=L_{35}=(0,\phi^{-2}-1/35,1),\qquad
                         U_2=C_7=(6/7)B+(1/7)D.
\]

For `Mij=(Ui+Uj)/2`, use the four **closed** triangles, in this order:

\[
 (U_0,M_{01},M_{02}),\ (M_{01},U_1,M_{12}),\
 (M_{02},M_{12},U_2),\ (M_{01},M_{12},M_{02}).                      \tag{8}
\]

Their union is the complete original closed triangle. If one barycentric
coordinate is at least `1/2`, the point is in its corner triangle.
Otherwise all three are at most `1/2` and the point is in the middle
triangle. This covers boundaries, including the equality case. Each piece
has a quarter of the original oriented chart area, checked exactly.

On each piece, common sixty strict axial signs extend the minimum corner
axial bound to every interior point using linearity and the norm triangle
inequality. A positive normal-cap cone extends the maximum corner normal
chord to the entire piece. Convexity bounds chart norm and center drift.
The monotonic nonnegative expression in (5) then bounds all possible
source angles on the **whole** piece, not just at its corners.
All phase prerequisites and factor domains are checked. A separate center
hull perturbation proves origin interiority with radius greater than `1/3`
everywhere on all four pieces.

The centered actual torque-ball radii certified for pieces 0--3 are

\[
                         3/5,\quad3/5,\quad29/50,\quad3/5.         \tag{9}
\]

For each piece, the exact homogeneous-polynomial lemma of the actual-hull
proof checks all `120 triples x 7 nonempty simplex faces`. A candidate
plane is excluded by opposite strict support gaps, or its squared facet
distance polynomial has nonnegative coefficients. Every actual facet is
covered. Changing facets, vanishing irrelevant normals, open edges and
corners are included. Corner balls alone are not used as a continuum proof.

The classifications `(opposite,distance,degenerate)` are respectively
`(726,114,0)`, `(728,112,0)`, `(728,112,0)`, `(728,112,0)`.
Total: **3,360 cases**, **2,910 opposite** and **450 distance**, with none
unresolved. For each piece its own radius in (9) minus its whole-piece
`R Lstar Thetastar_perp` is **strictly greater than 2/25**. The least
certified rational margin is the piece-1 lower bound

\[
 \frac{1588673338575226028695541865900711}
      {19531250000000000000000000000000000}>2/25.                  \tag{10}
\]

Applying (7) on every piece proves all-source strict passage exclusion
on the entire closed `B,L35,C7` triangle. The checker validates

\[
 L_{45}=B+(7/9)(L_{35}-B),\qquad
 C_{10}=B+(7/10)(C_7-B).
\]

Thus the entire preceding triangle is contained, and the unit-z chart-area
ratio is `(9/7)(10/7)=90/49`. No spherical-area ratio is claimed.
The exact normal-chord lower enclosure at `L35` exceeds `1/40`.
The receiver sphere outside the certified regions remains unresolved.

## 4. Reproduction, trust, provenance and limits

Use Python 3.11+ standard library. From repository root run each command
separately, keeping all solver/BLAS/OpenMP threads one:

```sh
python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/orthogonal_receiver_certificate.py --piece 0 --self-test
python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/orthogonal_receiver_certificate.py --piece 1 --self-test
python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/orthogonal_receiver_certificate.py --piece 2 --self-test
python3 -B rhombicosidodecahedron_mirror_cluster_obstruction/orthogonal_receiver_certificate.py --piece 3 --self-test
```

Each run regenerates the standard original probes and center subhull:
1,800 vertex/corner supports, 120 center triples/1,200 supports, fifteen
complete center facets, positive center stress and 540 full-pool supports.
It verifies the general four-variable polynomial identity, 81 rational
quaternion/matrix audits, the exact four-piece partition, whole-piece phase
and origin bounds, all 840 facet/stratum cases and 480 normal/support,
4,800 support-gap and 480 homogenized-distance arithmetic audits.
The direct arithmetic points do not supply continuum coverage.

Each self-test rejects eight malformed controls: parallel or nonunit
transport axes, an excessive or negative factor chord, a missing or
reversed partition piece, an insufficient actual ball radius and a false
input digest. Refusal of a sufficient certificate is not mathematical
nonexistence in an uncertified region.

Each output must match the corresponding record in
[orthogonal_receiver_expected.json](orthogonal_receiver_expected.json),
SHA256 `6eaaf32e88a8b46e1732c159fd062f2b6fadbe12c8925e9475ce130a20cee366`.
Merge that file's `common` fields with the requested `pieces` record to
reconstruct the complete JSON. Sorted two-space JSON plus a final newline
reconstructs every original output byte. The four normal runs took
10.27--10.84 seconds each, with observed peak child RSS below 21 MiB.
All four optimized publication-copy runs also matched every output byte,
taking 10.72--11.65 seconds each with peak child RSS 23,996 KiB across the
serial replays. Explicit checks remain active under `-O -B`.
All four piece replays are required for the complete cover.

Every sign decision uses exact ordered `Q(phi)`/Fraction arithmetic.
Radical endpoints are checked on the denominator-`10^12` rational grid.
Complete coefficient and stratum-record hashes identify the generated
data; every case is regenerated and checked, so no large hidden transcript
is a proof input. The continuous trust boundary is the cited source/roll
construction, standard model and exact kernels, (3)--(4), monotonic
whole-piece bounds, the facet/simplex lemma, complete midpoint cover and
the support exponential-remainder argument. No float, solver, sampled-angle
cover or incomplete computation supplies a theorem premise.

The checker pins actual-hull expected SHA256
`b74584ad4ed343925de777ca5b98f1217c95fdb08f073920acee28c8cd8aaaac`,
the directional
parent SHA256 `cda8f8555f21e41b412478adb776416a9161828e53f5dce77f51376adc250b33`,
and adaptive input SHA256
`53c852471e2d787b8958f01cc6f6e1b5c210ce3ee2b3a524ddbe1a59e9514e98`.
The published source/roll theorem is an explicit dependency. In the
preceding pass, a separate full parent replay timed out at its 55-second
limit and was stopped. No further expensive parent replay or limit increase
is made here. Its unchanged published source already has completed prior
normal and optimized replays with identical output; the present four
short runs independently regenerate all new hypotheses. The incomplete
attempt supplies no new proof fact and no mathematical verdict.

Current primary status was checked on 2026-09-30:
[Steininger--Yurkevich's RID discussion](https://arxiv.org/html/2508.18475#S9.SS1),
[Zeng's retained conjecture](https://arxiv.org/html/2604.26531), and
[Gosain--Grimmer's named-solid tables](https://arxiv.org/html/2509.08190)
retain the global RID question. The last source required successful
direct primary-site retrieval after a browsing retrieval error.
The standard projection formulation is
[Steininger--Yurkevich](https://arxiv.org/html/2112.13754).
Bounded searches do not establish historical priority.

Complementary full proofs and checkpoints read include
[six-rupert-1's deltoidal all-source area caps](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/global_area_proof.md),
source `5596212ab31932f7dd8b90cf6f1ad73c66afbe16`, graph
`bafkreigpe3pe5qqrekltisoss3zikl3znyydtso7utxsvag2yu2ykz3tsm`, and
[six-rupert-2's J77 all-source diameter caps](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_all_source_diameter_caps/PROOF.md),
source `97ce8ace4dd4398a9f397428ccc9758ed5e1b028`, graph
`bafkreiglthsm4hsiclzvbmvkvs6yybdtoh6bcb73j2ol44gmyrgbqa5ixq`.
The new [independent J77 review](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_all_source_review1/README.md),
**six-reviewer-1**, source `e78fafefba916f04dc61ec7e2f9556e1469776a1`, graph
`bafkreialgb2n4e3yjo77r7gkgmaclia4evw2zkww7rgrzsw3ywznxopfum`,
confirms that body's theorem and proves radius `1/1400` via exact concave
roll endpoints. Its proof and checkpoint were read; it does not review RID.
The same refresh found
[six-rupert-2's directional J77 receiver domains](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_directional_receiver_domains/PROOF.md),
source `f7cfae81911e86c562b226a04f7966989812f94d`, graph
`bafkreihbeoxtt3rmagrfbwqkn47u3oqm6jt55v7ffayh5yqnxt72fo6eym`.
Its full proof and updated checkpoint were read. It certifies all-source
caps `1/200` and a whole receiver triangle using actual original heights
and quadratic support/diameter coefficient certificates while retaining
translation. Its extension is unreviewed; the earlier J77 review does not
review this newer theorem or RID. The present rotation-composition lemma
is independent of central symmetry, although RID's translation removal
and torque exclusion use that body's hypotheses.
The inherited general active-set reduction is credited to
[six-rupert-2's diameter proof](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_projection_diameter/PROOF.md).
No body-specific theorem or constants transfer to RID. No reviewer was
directed and no verdict was requested or influenced.

The next useful frontier is a substantially larger certified receiver
domain using structured source/roll bounds and a finite adaptive cover,
or a genuinely different coercivity argument for other axial regions.
The complementary receiver sphere remains open. Neither a failed
sufficient bound nor an incomplete cover proves non-Rupertness.
