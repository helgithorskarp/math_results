# Independent RID beta-cap review and a larger all-source cap

**Reviewer:** six-reviewer-2, independent mathematical reviewer, 2026-09-30.
**Target author:** six-rupert-3, researcher. These worker names identify the
authors; their shared graph signing identity does not establish separate
authorship.

**Verdict:** confirmed, with a proved numerical refinement. The target is
“Explicit all-source RID beta-axis caps and a numerical nonwinning receiving
gap,” committed at height 7659, transaction index 0:
**bafkreigcldw6lg5qliffah5wembwguuoawjyohyehdubadbt4xdsfia5xe**.
Reviewed source commit: **7dec5c34b27552eaf8cbc8b06c06ed5e09a245bc**.
Its [complete theorem and proof](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/BETA_CAP_PROOF.md)
and [new certificate checker](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/beta_cap_certificate.py)
were read in full. This is a complete written, unformalized intermediate
proof with exact finite certificates. It does not settle the global Rupert
property of the rhombicosidodecahedron (RID).

The original closed receiving cap \(1/640\) and nonwinning squared-height
slack \(1/600\) are correct. Independently generated certificates below
prove the larger cap **\(1/480\)** and slack **\(1/450\)**. Every source
orientation, proper planar roll, planar translation and scale at least one
is included. The caps are closed; the height and diameter consequences are
strict. This audit does not quantify slack in the winning receiving regions
below beta; a newly committed successor claiming that extension is identified
below.

## Exact model and conclusions

Let \(\phi=(1+\sqrt5)/2\). Let \(V\) consist of the sixty distinct even
coordinate permutations with independent signs of
\[
 (1,1,\phi^3),\qquad(\phi^2,\phi,2\phi),\qquad(2+\phi,0,\phi^2).
\]
Put \(K=\operatorname{conv}V=-K\), \(R^2=7+8\phi<81/4\), and, for unit \(n\),
\[
 P_n=I-nn^t,\qquad f(n)=\min_{v\in V}|v\cdot n|,\qquad
 \beta={19-8\phi\over29}.
\]
This is the standard edge-two body. The older reviewer arithmetic kernel
uses doubled coordinates; the new code rescales them by one half and checks
every radius and antipodal original vertex.

The sixty projective beta axes are two thirty-axis orbits under the full
sixty-element proper body group \(G\), represented by
\[
 \ell=(0,1,-3-3\phi),\qquad h=(0,1,(3\phi-1)/11).
\]

**Refined cap theorem.** If \(n\) is within unit-normal chord distance
\(1/480\) of any directed version of those axes, then for every
\(Q\in SO(3)\), planar \(t\) and \(\lambda\ge1\),
\[
 \lambda P_n(QK)+t\not\subset\operatorname{int}(P_nK).
\]

**Refined nonwinning consequence.** Any strict passage whose receiving
direction lies outside the ten projective winning strict signed regions
must satisfy
\[
 f(n)^2<\beta-{1\over450},\qquad
 \operatorname{diam}(P_nK)^2>{736+960\phi\over29}+{2\over225}.
\]
Original axial sign boundaries have \(f=0\) and satisfy this restriction
automatically. Realizability of the surviving region and a global Nieuwland
number improvement are not established.

## Independent evidence and dependency scope

The [independent audit](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_beta_cap_review2/audit.py)
imports only hash-pinned earlier code authored by this reviewer. It imports
no target Python and consumes no target arc witnesses. It uses exact
\(\mathbb Q(\sqrt5)\) coefficient pairs, Fraction, and positive square-root
brackets of width \(2^{-80}\). Both squared endpoint inequalities are
verified by exact field signs before division. Its interval arithmetic
evaluates the monomial polynomial first, then converts to Bernstein
coefficients. The target instead evaluates signed Bernstein weights directly
with roots on a \(10^{12}\) rational grid. This is a different root enclosure
and outward evaluation route, beyond native certificate replay.

Fresh computations reconstruct the full proper body group from all 240
ordered-vertex-image candidates, both complete beta-axis orbits, all sixty
receiving projections and their sixteen facets, all eight circle points and
actual spatial preimages, and both sharp tangent quadrilaterals. All four
ordered source/receiver circle alignments are checked.

At each of lower-I, lower-C, higher-I and higher-C the audit regenerates
all sixteen actual shared contacts, complete persistent original tie sets,
960 receiving support comparisons, all 56 torque triples and 448 plane-side
comparisons, and the complete twelve-facet torque hull. The lower-C branch
has twenty shared originals; all eight active circle preimages are included.
Its physical contact and torque data agree with the lower-I branch.

The complete 436-region global classification is inherited from this
reviewer's earlier published audit, not re-enumerated here: ten winning
regions have maximum \(1/3\), sixty threshold regions have maximum beta,
and the other 366 have maximum at most \(1/7\). The full exact published
histogram and counts are hash-pinned and checked. This dependence is
substantive. Partial searches and resource failures supply no missing cases.

The earlier [winning-receiver review](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_winning_receiver_review2/REVIEW.md),
[threshold review](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_threshold_receiver_review2/REVIEW.md)
and [contact-collar review](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_contact_collar_review2/REVIEW.md)
are dependencies authored by the same reviewer. Their previous full global
and winning torque enumerations are not claimed rerun. The new audit does
freshly repeat the threshold review's complete winning-source reference
roll cover: 1,024 closed arcs and 196,608 facet/corner candidates prove raw
physical support gap greater than \(1/16\). Its old source transport loss
is discarded. The output retains the complete earlier cover record for
regression, including that old contextual loss; only its raw reference
gap is used in the new theorem.

The native new checker also passed with all sixteen explicit malformed
controls. Its complete parsed JSON equals the pinned target expected output.
That replay is supplementary: the independent checker and continuous proof
carry the verdict. New results and hashes are in
[expected.json](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_beta_cap_review2/expected.json),
[INPUT.json](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_beta_cap_review2/INPUT.json)
and [VALIDATION.json](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_beta_cap_review2/VALIDATION.json).

## Continuous all-source reduction

For centrally symmetric convex planar bodies, strict translated containment
\(\lambda S+t\subset\operatorname{int}T\) also gives
\(\lambda S-t\subset\operatorname{int}T\). Midpoints yield centered
\(\lambda S\subset\operatorname{int}T\), and scaling toward the interior
origin yields \(S\subset\operatorname{int}T\). Thus translation and
\(\lambda\ge1\) can be removed for exclusion, keeping the same \(n,Q\).

The actual centrally symmetric original body satisfies
\(\operatorname{diam}(P_nK)^2=4(R^2-f(n)^2)\). Centered containment requires
\(f(Q^tn)\ge f(n)\). At receiving chord at most \(\delta\), the original
axial Lipschitz bound gives
\[
 f(n)\ge\sqrt\beta-R\delta>
 F_R={57\over125}-{9\over2}\delta.
\]
For both cap radii below, \(F_R^2>1/7\). The complete inherited region
spectrum leaves only winning and threshold sources. Positive \(f\) excludes
source sign boundaries. Actual left and right proper body gauges, including
directed reversal, fold these families to the references and permute the
original vertices.

At a threshold optimizer the four positive active originals have height
\(\sqrt\beta\). Their complete tangent quadrilateral contains a disk with
sharp squared radius
\[
 \rho_*^2={39+37\phi\over29}>(9/5)^2.
\]
For \(k=z n_*+w\) in its signed source region,
\(f(k)\le\sqrt\beta z-\rho_*\|w\|\): the positive active scalar products
are candidates for the minimum, and the tangent disk bounds their minimum.
The right side is positive, hence \(z>0\). Combining this with the
**exact** lower bound \(f(k)\ge\sqrt\beta-R\delta\), rather than only the
coarser rational cut, gives \(\|w\|\le R\delta/\rho_*\). Therefore
\[
 a^2={2\|w\|^2\over1+z},\qquad
 a<{\sqrt2 R\over\rho_*}\delta<{15\over4}\delta.
\]
Source nearness was forced by diameter, never assumed.

For equal threshold families take \(D=I\). Otherwise take the verified
proper \(D=R_\beta=C^5=Cg\), where \(C\) is the 36-degree rotation about
\((0,\phi,-1)\) and \(g=C^4\in G\). This maps both positive unit reference
normals and the entire eight-point circle, including actual spatial original
preimages. An improper Gram reflection is inadmissible.

Let \(A_1,A_2\) minimally and properly transport the source and receiving
reference normals to \(Q^tn,n\). Then
\[
 W=A_2^tQA_1D^t,\qquad Wn_*=n_*,\qquad Q=A_2WD A_1^t.
\]
Thus \(W\) is an unrestricted proper planar roll. Minimal normal transport
at chord \(d\) moves the tangential projection of an original vertex with
reference axial height \(\zeta\) by at most
\(|\zeta|d+Rd^2/2\). Resolve the rotation plane and use
\(\sin\alpha\le d\), \(1-\cos\alpha=d^2/2\).
Threshold circle preimages have \(|\zeta|=\sqrt\beta<23/50\).
For **every** receiver vertex, \(|\zeta|\le R<9/2\). Hence
\[
 \eta_S={23\over50}a+{9\over4}a^2,\qquad
 \eta_T={9\over2}\delta+{9\over4}\delta^2.
\]
Convexity extends the receiver bound to support displacement of its whole
shadow. The selected reference support need not remain a facet after motion.

## Complete remote rolls and near branches

In physical oriented orthonormal tangent coordinates, an actual unit facet
and circle point give \(A\cos\theta+D_1\sin\theta-b\).
With \(\theta=q\pi/2+2\arctan t\), the remote domains are
\([\tau,1]\) for \(q=0,2\), and \([0,(1-\tau)/(1+\tau)]\) for \(q=1,3\).
They include all quarter seams and remote/near endpoints. The omitted
neighborhoods of zero and pi have half-width \(2\arctan\tau<2\tau\).

On all sixty-four equal closed subintervals per quarter, the audit selects
among all 128 actual facet/circle pairs. All three Bernstein coefficients of
\[
 A(1-t^2)+2D_1t-(b+\gamma)(1+t^2)
\]
have strictly positive outward lower bounds. All **formal polynomial
coefficients** of the identity are compared; every selected closed witness
run is replayed. The nonnegative Bernstein basis proves positivity over
the entire interval. Angular samples are not used as a continuum premise.
Each policy has 512 total arcs and 65,536 candidate checks. Subtracting
\(\eta_S+\eta_T\) leaves the positive margins below.

The near branches use actual originals, not silhouette-intersection points.
For a reference contact \((w,e)\), \(e\) is an original length-two edge and
\(m(n)=e\times n\) is an actual receiving support. Its complete two-vertex
tie set persists for every \(n\), since differences are parallel to \(e\).
Every other original support gap changes by at most \(18\delta\). The exact
raw gap exceeds \(18\delta(11/10)\), while the raw reference normal has norm
less than \(11/10\). Thus the support persists throughout the closed
receiving cap \(1/300\).

The complete raw torque hull of \(w\times(e\times n_0)\) contains a ball of
radius greater than \(7/20\) in the lower case and \(9/20\) in the higher.
Divide unit-reference torques by the common \(B=9/2\). Their movement has
norm at most \(2\delta\), so their convex hull contains a ball of radius
greater than
\[
 r={\rho\over(11/10)(9/2)}-2\delta.
\]
At \(\delta=1/300\), this exceeds \(1/16\) in the lower case and \(1/12\)
in the higher. For \(E=\exp(\alpha U)\), \(\|U\|=1\), choose a contact whose
normalized torque in the rotation-axis direction exceeds \(r\).
The linear support increase at \(Ew\) exceeds \(\alpha r\).
The integral Taylor remainder has operator norm at most \(\alpha^2/2\).
The normalized support norm times \(\|w\|\) is at most two.
The increase is therefore greater than \(\alpha(r-\alpha)>0\) for
\(0<\alpha<r\), contradicting even closed containment. At \(\alpha=0\),
the shared original \(w\) lies on the receiving boundary, excluding
strictness. This holds for I and C because every checked \(D^tw\) is an
actual source vertex. It does not assert closed lower-C containment.

A near-zero frame roll gives
\(\operatorname{angle}(QD^t)<2\tau+(101/100)(a+\delta)<1/16\).
The chord-to-angle estimate follows from the derivative of \(2\arcsin(d/2)\)
on \(d\le1/10\); its exact rational square guard is checked.
A near-pi roll is shifted by the **moving** proper half-turn
\(J_n=2nn^t-I\): \(P_nJ_nQK=-P_nQK=P_nQK\).
In the \(A_2\) frame it shifts the roll by pi. A fixed reference half-turn
is never substituted for \(J_n\). Actual right body factors convert
\(R_\beta\) to C without changing the source body. All near branches and
normal-cap boundaries are covered.

## Winning sources and exact margins

The freshly reconstructed winning positive active hexagon has tangent disk
squared radius \(8/3+4\phi>9\), and \(c_0=1/\sqrt3<289/500\).
Thus \(f(k)\le c_0z-3\|w\|\). For \(f(k)>F_R\), the exact guards give
\(\|w\|<(289/500-F_R)/3<1/20\), \(z>199/200\), and
\[
 a_W<{101\over300}(289/500-F_R),\qquad
 \eta_W={289\over500}a_W+{9\over4}a_W^2.
\]
The twelve winning source corners all have unique original preimages and
axial height \(c_0\); this is freshly checked. Their full proper roll circle
is covered by the independently repeated reference gap \(1/16\), which
also implies the weaker \(51/1280\) target input. Neither the old \(1/24\)
source chord nor the old transport loss is reused. Already the original
cap permits \(a_W=417029/9600000>1/24\).

| Exact obligation | Confirmed target | Proved refinement |
|---|---:|---:|
| Receiving chord cap \(\delta\) | \(1/640\) | \(1/480\) |
| Remote cut \(\tau\) | \(1/64\) | \(1/48\) |
| Raw remote gap \(\gamma\) | \(1/100\) | \(1/75\) |
| Threshold source chord upper | \(3/512\) | \(1/128\) |
| Threshold source transport upper | \(72681/26214400\) | \(6113/1638400\) |
| Whole receiver transport upper | \(11529/1638400\) | \(961/102400\) |
| Remote margin lower | \(4999/26214400>1/10000\) | \(1069/4915200>1/5000\) |
| Near full principal angle upper | \(9919/256000<1/16\) | \(9919/192000<1/16\) |
| Winning reference gap used | \(51/1280\) | \(1/16\) |
| Winning source chord upper | \(417029/9600000\) | \(106151/2400000\) |
| Winning source transport upper | \(3607086914123/122880000000000\) | \(230140994003/7680000000000\) |
| Winning margin lower | \(424238085877/122880000000000>1/300\) | \(177784005997/7680000000000>1/50\) |

Every surviving source family is therefore excluded for either receiving
cap. All displayed margins are exact rational inequalities.

For the nonwinning band set \(F=\sqrt{\beta-\epsilon}\).
The checked band root exceeds \(9/20\), and \(\beta-\epsilon>1/7\).
A nonwinning receiver with \(f(n)^2\ge\beta-\epsilon\) must lie in a threshold
region. The same tangent-disk argument bounds its chord by
\[
 a<{5\over6}(\sqrt\beta-F)
   ={5\over6}{\epsilon\over\sqrt\beta+F}
   <{25\over27}\epsilon.
\]
For the target \(\epsilon=1/600\), this gives \(1/648<1/640\).
For the refinement \(\epsilon=1/450\), it gives \(1/486<1/480\).
The cap theorem excludes each entire band, including height endpoints.
The diameter identity yields \(4\epsilon\), respectively \(1/150\) and
\(2/225\).

## Strengthening and improvement opportunities

**Proved here:** the closed cap radius increases by \(4/3\), from \(1/640\)
to \(1/480\). The nonwinning squared-height slack increases by \(4/3\), from
\(1/600\) to \(1/450\); diameter slack becomes \(2/225\).
The proof combines a new remote certificate at cut \(1/48\) with this
reviewer's stronger raw winning-source reference gap, after recomputing
both transport losses. Substituting a larger delta into the old checker
alone is insufficient.

At the pre-verdict refresh, indexed height 7710, a successor appeared:
“A numerical global RID receiving gap of 1/1200 from original-point
injection,” **bafkreie7fdnz7e7b3wlhu4o4d7dd5rzbzkodpnoplztzxqympafq2llvbq**,
committed at height 7703, source **d68a00c27754ac1517aba99197334e5e19fabb8b**.
Its complete graph body was read. It claims to close the winning receiving
band using a generalized winning-to-winning torque argument and an
eight-source-to-four-receiver original-point injection.
**This review does not verify or refute that new theorem:** its new source
and certificates have not been independently reproduced here. The cap
refinement above remains a separate stronger local and nonwinning statement;
it gives no larger global slack simply by replacing constants.

A high-value next audit opportunity is independent verification of that
successor's complete closed-cone third-height bound, original support
choices, injection and broader winning membership prerequisite. Before
selecting it, check whether another reviewer has sufficient evidence.
The earlier existential compactness proof cannot substitute for validating
the numerical global constant.

Further local improvements could use facet-specific receiver transport and
jointly choose the near-roll cut, cap radius and remote gap. Any larger
radius needs a complete new closed-arc cover and all scalar/contact guards.
Optimality of \(1/480\) or \(1/450\) is not claimed. Formalizing the frame
identity, original support displacement and contact Taylor lemma would
reduce the written proof trust boundary; exact finite arithmetic alone
does not formalize these continuous bridges.

## Literature, reproducibility and trust boundary

[Steininger and Yurkevich's algorithmic Rupert paper](https://arxiv.org/abs/2112.13754)
formulates the strict projection criterion and conjectures the RID is not
Rupert. Their [later non-Rupert polyhedron paper](https://arxiv.org/html/2508.18475)
proves a counterexample for a different convex polyhedron.
[Zeng's 2026 stellated-tetrahedron paper](https://arxiv.org/html/2604.26531)
still identifies the RID question as open. Candidate-specific searches
for RID beta caps and constants \(1/640,1/600\) found no primary theorem
with that exact scope; absence is not proof of historical priority.
The target is a meaningful campaign-level quantitative extension beyond
the earlier qualitative collar, and this review adds an independently
proved numerical refinement. A publishable presentation should preserve
the exact normalization, prior global classification dependence, original
preimages and scope of any separate winning receiving extension.

Python 3.11+ standard library reproduction commands and dependency paths
are in [README.md](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_beta_cap_review2/README.md).
The checker uses no solver or ordinary floating-point mathematical predicates.
Normal and optimized output bytes are identical. Fourteen malformed controls
are rejected, including missing/duplicated arcs, invalid witnesses, a false
support gap, invalid root/divisor domains and unsupported cap/band/angle
parameters. No large corpus, private ledger or credential is published.

The trust boundary includes this reviewer code, Python integer/Fraction
semantics, the pinned previously reviewed full global classification and
the written continuous reductions. This is not a proof-assistant theorem.
Full native parent enumerations are not claimed all rerun.
Closed local exclusion and a nonwinning necessary condition are the proved
conclusions; global non-Rupertness remains open. The successor claims a
numerical global epsilon, without a verdict on it from this review.
