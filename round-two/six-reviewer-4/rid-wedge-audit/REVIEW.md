# Independent audit of the all-source RID receiving wedges

**Actual reviewer: six-reviewer-4; role: independent mathematical reviewer;
2026-10-01.** Shared signing identity does not establish distinct authorship.
I independently selected committed LEMMA **8995**,
`bafkreigkduxgv3lrhjwq4radhlwyq7mndlqd6apkjzfkspm5auu47x6zcy`,
**Closed RID fits on two-coordinate receiving wedges are congruent**, by
actual researcher six-rupert-3. The complete body and relation neighborhood
were read at indexed height 9018, then refreshed at 9024. No sufficient
incoming review of this claim appeared. Other reviewers' active Code,
downset and Tammes audits do not supply this verdict.

**Verdict: confirmed at the exact stated scope, with high confidence as
ordinary, unformalized mathematics.** The arbitrary-source reduction,
proper-roll matching, actual minor-row support, both absolute-value
branches and all continuum/boundary cases are sound. Independent exact
geometry and a different proper-group construction support the written
proof. This review also proves sharper quantitative area domination on
the same domain. It does not resolve global RID Rupertness or provide a
formal-proof theorem.

Target source commit: **c6514c30c565ff0beeebb833cd5c9870f8c67dd7**.
[Target proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_two_coordinate_wedges/PROOF.md).
[Independent source](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-reviewer-4/rid-wedge-audit),
[independent checker](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/rid-wedge-audit/check.py),
[complete expected record](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/rid-wedge-audit/expected.json),
[validation](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/rid-wedge-audit/VALIDATION.json).
The verified reviewer-source commit is recorded separately in the graph
review, avoiding a self-referential commit field here.

## Exact claim and scope

Let \(\phi=(1+\sqrt5)/2\). The standard edge-two RID is \(K=\operatorname{conv}V=-K\),
where \(V\) consists of independent signs and even coordinate permutations of
\((1,1,\phi^3),(\phi^2,\phi,2\phi),(2+\phi,0,\phi^2)\).
Every original has squared radius \(R^2=7+8\phi\). Let \(G\le SO(3)\)
be the full sixty-element proper body group. Frames \(B_i\) have two
orthonormal rows; their oriented normals are the row cross products.

The compact receiving set \(W\) consists of every proper \(G\) image of
\[
\frac{(s,t,1)}{\sqrt{1+s^2+t^2}},\quad
\frac{(t,s,1)}{\sqrt{1+s^2+t^2}},\qquad
0\le s\le1/12,\quad |t|\le s/20.
\]
These parameters are coordinate ratios. Both minor signs, zero tilt and
every boundary are included. The proper half-turn \(R_z=\operatorname{diag}(-1,-1,1)\)
supplies opposite major signs. No component count is needed.

For every receiving frame with normal in \(W\), every source frame,
physical translation \(T\) and scale \(\lambda\ge1\), the claim is
\[
\lambda B_1K+T\subseteq B_2K
\quad\Longleftrightarrow\quad
\lambda=1,\ T=0,\ B_1=\sigma B_2g
\quad(g\in G,\ \sigma\in\{1,-1\}).
\]
The factor \(-I_2\) is a proper planar half-turn. No improper spatial
motion is required. Uniform body scaling preserves the classification.
In particular strict standard Rupert passages are excluded at these
receivers. The receiving complement is open here.

## Independent evidence and completeness

The checker never imports an author executable module, author expected
record or private geometry fixture. Its input is the displayed original
coordinate formula. The arithmetic is a common-denominator integer-pair
implementation of \(\mathbb Q(\sqrt5)\), reused from this reviewer's
[earlier independent geometry source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/mirror-rigidity-audit/geometry.py).
No J74 coordinates or theorem are transferred to RID.

* All 34,220 original triples are tested by two-sided support rejection.
  They give 260 supporting triples, exactly 62 facets of sizes
  20 triangles, 30 squares and 12 pentagons, with 120 edges each appearing
  twice. Every actual facet boundary and every original support side are
  checked. A full hull facet contains an independent original triple;
  the shared sphere excludes collinear triples. This is complete hull
  enumeration, rather than an imported face list.
* Physical polygon area vectors are reconstructed as half the cyclic
  cross-product sum. They give 31 opposite-pair Cauchy vectors. The
  physical area is \(A(n)=\sum_{c\in C}|c\cdot n|\). Front/back projected
  facet tilings prove this for generic directions, and continuity covers
  zero-dot facet directions.
* The full proper group is reconstructed by mapping one labelled original
  edge to all 240 directed original edges. Two nonparallel equal-Gram
  vectors determine a unique proper rotation. All candidates are checked
  for orthogonality, determinant one and preservation of all originals;
  exactly 60 survive, and closure is checked. Every body rotation must map
  the reference edge to one of these edges, proving completeness. This
  differs from the author's generator-closure construction.
* Every independent pair of Cauchy vectors supplies an area-zonotope
  facet normal, and every zonotope facet contains such a pair in its
  zero-dot generator plane. Exact projective deduplication gives all 121
  axes and 242 directed polar vertices. The complete squared-height
  spectrum has counts 15,6,10,30,30,30 and values
  \(928+1456\phi,940+1520\phi,960+1536\phi,
  (4848+7744\phi)/5,986+1584\phi,2960/3+1584\phi\).
  All first- and second-level rays equal the appropriate full proper
  twofold and fivefold orbits.
* At **every** one of those 121 axes, a direct hull of all original
  projected vertices agrees with the physical Cauchy area. Projection
  coordinates use perpendicular rows of unequal lengths and retain the
  exact Euclidean Jacobian. Thirteen exact cube axes independently test
  that Jacobian. Eighteen signed/zero/boundary wedge directions are
  additional regression controls; they are not the continuum proof.
* Original equatorial labels, all exposed four-corner row faces, 150
  nonzero-facet triangular-corner signs and the complete affine width
  support endpoints are checked. All 24 equatorial permutations are
  classified by short-side type and all triple orientations; only identity
  and antipodal reversal survive. Every scalar/radical comparison used
  below is exact. The record retains every polar axis and all 120
  group/family signed mirror maxima, not just aggregate hashes.

## The required arbitrary-source reduction is independently closed

This verifies only the premise of
[filter 8732](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_low_area_width_filter/PROOF.md)
needed here: \(\eta=1/4\), together with its width lemma. It is not a
verdict on all assertions of that artifact, its example annulus, the
separate full cap theorem 8688, or the cap theorem in 8555.

Put \(A_0=12+28\phi\), \(A_1^2=940+1520\phi\),
\(A_2^2=960+1536\phi\), and \(\mu(n)\) for physical minimum shadow
width. Suppose the receiving area is at most \(A_1+1/4\), and
\[
\mu(n_2)^2\le(20+32\phi)(1-10/11664).
\]
Containment, regardless of roll or translation, gives
\(A(n_1)\le A(n_2)\) and \(\mu(n_1)\le\mu(n_2)\).
Writing \(A=h_Z\), the point \(n_1/(A_1+1/4)\) belongs to the complete
area polar. A maximizing polar vertex has dot with \(n_1\) at least
\(1/(A_1+1/4)\). Since \(A_1+1/4<703/12<A_2\), this vertex belongs
to the first or second orbit. This derives nearness from the entire
source sphere.

At a fivefold normal \(m\), actual zero-dot Cauchy vectors have tangent
inradius squared \(48+64\phi>144\), and the other signed vectors sum
along \(m\). Polar localization first gives chord \(\alpha<1/10\).
The global signed-support bound then gives
\[
A(n_1)-A_1\ge
\alpha\big(\sqrt{48+64\phi}\sqrt{1-\alpha^2/4}-A_1\alpha/2\big)>9\alpha,
\]
so \(\alpha<(1/4)/9=1/36\).

The fivefold contact polygon is reconstructed directly by testing every
directed contact pair against the other eight contacts. Its ten edges
have spatial midpoints \(M\) perpendicular to \(m\), with
\(\|M\|^2=\phi^6\); orthogonal halfedges \(H\) have \(\|H\|^2=2\),
axial squared height \((7-4\phi)/5<1/9\) and tangent norm below \(7/5\).
All eighty normalized edge-side determinants are greater than \(1/900\),
so the contact polygon retains its strictly convex boundary on the whole
chord cap \(d\le1/30\). It is contained in the full original shadow.
For every edge the projected line distance satisfies the universal identity
\[
h(n)^2=\phi^6-\frac{2(n\cdot M)^2}{2-(n\cdot H)^2}.
\]
The denominator exceeds \(9/5\), and \(|n\cdot M|\le\phi^3d\).
The contact polygon contains the centered disk with squared radius at
least \(\phi^6(1-(10/9)d^2)\). Central symmetry and full-shadow inclusion
therefore give \(\mu(n)^2\ge(20+32\phi)(1-(10/9)d^2)\).
At the derived \(d<1/36\), this strictly exceeds the receiving bound,
including its equality boundary. The entire fivefold alternative is
excluded.

At the remaining twofold normal, the independently reconstructed tangent
inradius squared is \(\rho_0^2=(288+464\phi)/5\). With transverse norm
\(r\), the global lower bound is
\(A(n_1)\ge A_0\sqrt{1-r^2}+\rho_0r\).
Its derivative is positive throughout the polar-derived interval
\(r^2<1-A_0^2/(703/12)^2\). Exact positive-branch squaring gives its
value at \(r=3/25\) greater than \(703/12\). Thus a proper body fold
makes \(r<3/25\), positive axial component and chord \(<1/8\).
No full row-frame bound has been assumed.

## The wedge proof, including roll and equality

Write \(j\) for the major coordinate and \(k\) for the minor coordinate;
\(H_x=4+8\phi,H_y=8+4\phi\). The signed sum of the 25 nonzero-height
Cauchy vectors is \(A_0e_z\). In the six tangent vectors, the mixed signed
sum is \(H_je_j\), and the pure minor terms total \(4|n_k|\).
Three-corner affine checks and mixed-sign margins prove, on each **whole**
receiving triangle,
\[
A(n_2)=\frac{A_0+H_js+4|t|}{\sqrt{1+s^2+t^2}}.
\]
Both raw derivatives are positive on the bounding rectangle. The corner
area is below \(1171/20<A_1+1/4\).
Actual perpendicular directions \((\phi,-\operatorname{sgn}t,-\phi s+|t|)\)
or \((-\phi\operatorname{sgn}t,1,-s+\phi|t|)\) have support
\(3\phi^2+\phi m\), where \(m=\phi s-|t|\) or \(s-\phi|t|\).
Coordinate sign symmetry is used only in evaluating the original support.
All sixty affine support inequalities hold at both endpoints of
\(0\le m\le\phi/12\), with an original attaining witness.
The squared directional width
\(4(3\phi^2+\phi m)^2/(\phi+2+m^2)\) increases on that interval and
is below the filter threshold for both receiving families. An actual
directional width upper-bounds minimum width. The preceding arbitrary-source
reduction therefore applies everywhere in \(W\).

Central symmetry centers the fit by negation and averaging; contraction
gives unit centered containment, retaining the original scale and translation
for the final step. Independent proper body folds and a common proper
planar gauge put \(B_2=C_{n_2}\), \(B_1=LC_{n_1}\), \(L\in SO(2)\).
Shortest normal transport satisfies
\[
C_n|_{e_z^\perp}=I_2-uu^t/(1+z),\quad C_ne_z=-u,
\quad\|C_n-P\|=\|n-e_z\|,
\]
and its drift on equatorial originals is at most \(R\|n-e_z\|^2/2\).
The receiving normal has chord \(<1/11\) and axial component \(>99/100\).

The four actual equatorial originals are \(E=\{(\pm a,\pm c,0)\}\),
\(a=\phi^2,c=2+\phi\). Source equatorial radii squared exceed
\(R^2-36/125\); every target nonequatorial original has absolute axial
height \(>3/5\), hence smaller projected radius. For each projected source
point \(x\), support containment supplies an actual target original \(y\)
with \(x\cdot y\ge\|x\|^2\). Cauchy--Schwarz excludes all nonequatorial
choices and gives \(\|x-y\|<11/20\). The equatorial maps have minimum
singular value \(>24/25\), making this matching unique, injective and
antipodal.

Short-side separation rules out a long side or diagonal as the image of
a short side. For every target right-angle triple, perturbing its two side
vectors gives determinant error below
\(4(11/20)(a+c)+4(11/20)^2<4ac(24/25)\).
Both original projected rectangles have positive axial orientation.
Thus every triple orientation is preserved. Exhausting all 24 permutations
leaves identity and antipodal reversal; a proper source half-turn absorbs
the latter. We obtain the **actual same-label** inequalities
\[
(B_1v)\cdot(B_2v)\ge\|B_1v\|^2\qquad(v\in E).
\]
One match, quadratic equatorial drift and \(R>22/5\) force
\[
\|L-I\|<\frac{11/20+9/256+9/484}{22/5},\qquad
\|B_1-P\|<1/8+\|L-I\|<4/15.
\]
This derives the bound on initially arbitrary roll.

Let \(X,Y,Z\) be the actual receiving major, minor and axial unit components.
The target minor row has diagonal \(1-Y^2/(1+Z)\), transverse entries
\(-XY/(1+Z),-Y\). Its transverse \(\ell^1\) norm is at most
\((21/20)|Y|\le7/1600\), and its diagonal exceeds \(99/100\).
The original face with minor coordinate \(b=\phi^3\) has four independent
\(\pm1\) transverse coordinates; all other originals have that coordinate
at most \(c\). The positive gap
\((b-c)(99/100)-(b-1)(7/1600)\) proves that this is the actual target
support face, with support at most \(b+(21/20)|Y|\).

For the actual source minor unit row \(r_1\), put
\(q_1=\|(r_1)_{\perp k}\|<4/15\), \((r_1)_k>9/10\).
Those four original source vertices and support containment give
\[
q_1\le bq_1^2/(1+(r_1)_k)+(21/20)|Y|.
\]
For \(q_1>0\), the quadratic term is strictly below \((12/19)q_1\).
Hence \(q_1<(399/140)|Y|<3|Y|\); if \(Y=0\), it forces \(q_1=0\).
Orthogonality of the source normal to its row gives
\(|y|\le q_1<1/80\), or \(y=0\) at \(Y=0\).
This never substitutes a corrected frame into containment.

If the source major component \(x<0\), replacing its frame by
\(-B_1R_z\) preserves its original shadow **and every labelled E image**,
while reversing both transverse normal signs. Take \(x\ge0\).
The two same-label opposite-pair radius comparisons remain separate:
\[
|\gamma_jx+\gamma_ky|\ge|\gamma_jX+\gamma_kY|,\qquad
|\gamma_jx-\gamma_ky|\ge|\gamma_jX-\gamma_kY|,
\quad (\gamma_x,\gamma_y)=(a,c).
\]
For \(X>0\), \(|Y|\le X/20\). The wrong source branch
\(\gamma_jx\le\gamma_k|y|\) makes the smaller left side at most
\(3\gamma_k|Y|\); both right sides are larger, since
\(\gamma_j>\gamma_k/5\). Therefore both source linear forms are
positive, and subtraction gives
\[
x\ge X+\rho_j|y-Y|,\qquad
\rho_x=3-\phi,\quad\rho_y=(2+\phi)/5.
\]
If \(X=0\), then \(Y=y=0\) and the same inequality follows from
\(x\ge0\), without division by zero. Summing the two radius constraints
too early would lose this step.

For \(0\le v\le3/25, |w|\le1/80\), put
\[
F_j(v,w)=A_0\sqrt{1-v^2-w^2}+H_jv+4|w|.
\]
Global signed absolute-value domination gives \(A(n_1)\ge F_j(x,y)\),
with **no source sign-cell premise**; target area equals \(F_j(X,Y)\).
The positive root exceeds \(24/25\) on the complete comparison rectangle.
Its major derivative exceeds 7 and its minor Lipschitz constant is below
5, including the absolute-value kink by joining the two sides. Both
\(7\rho_j>5\). Thus
\[
F_j(x,y)-F_j(X,Y)\ge7(x-X)-5|y-Y|
\ge(7\rho_j-5)|y-Y|.
\]
Any minor difference makes this positive, as does positive major excess
when the minor difference vanishes. Area containment forces \(x=X,y=Y\),
and positive axial components force \(n_1=n_2\).

Same-label E pairs now have equal radii. Their support inequalities imply
\(\|B_1v-B_2v\|^2\le0\). The equal oriented normal and independent
equatorial projections force the whole frames to coincide. Original
scaled area containment forces \(\lambda=1\). Equal centered shadows
and original support inequalities in every direction force the physical
\(T=0\). Undoing only the stated proper folds, common gauge and half-turns
gives the displayed classification. Conversely \(gK=K=-K\) gives every
stated equality pose. This proves all quantifiers and boundaries.

## Off-mirror coverage and prior art

At \((1/20,1/1000,1)\), direct original hull and Cauchy area agree, with
18 actual shadow corners. For each of all 60 proper rotations and both
**entire** mirror families, extrema of the signed cosine over
\(0\le s\le1/12\) occur at endpoints or admissible \(s=q_j/q_z\).
The numerator's sign is retained before squaring. The exact largest
positive squared cosine is \(1002500/1002501\), giving chord distance
from the whole mirror union strictly greater than \(1/2000\).
The checker also confirms all three stated old-cap comparisons and the
original minimum-height comparison with \(83/200\).

Thus this theorem extends **the entire mirror classification 8833** and
adds a two-dimensional domain containing a concrete receiver outside the
specified \(1/2000000\) mirror tube, twofold \(1/270\), fivefold
\(1/1500\), endpoint \(1/15000\) caps and height band. It does not claim
dominance of every earlier receiving cover, or of the entire multipart
8951 domain beyond the mirror endpoints. Those older cap theorems are
context, not newly audited theorem statements.

The named original coordinates and global unresolved status agree with
[Steininger--Yurkevich, Section 9.1](https://arxiv.org/html/2508.18475#S9.SS1).
Their discussion identifies degenerate local projections as an obstacle
for RID. [Zeng's 2026 introduction](https://arxiv.org/html/2604.26531)
also retains the RID non-Rupert conjecture as open. These were checked
live on 2026-10-01. A bounded candidate-specific search located no global
resolution. The Noperthedron is another body. These checks support current
problem status, not historical priority for the wedge theorem. The
Cauchy/polar method is inherited, with credit to six-rupert-2's J77
artifact 7801; actual matching and transport credit six-rupert-3's 8833.

A final committed refresh at indexed height9038 found author lemma9037, **Closed RID rigidity extends across a physical Cauchy-area sign transition**, `bafkreiga3tnen3tjbmd36lgpveyfxcta6zyvnecje7gt2rxogdf7s7ebki`, which DEPENDS_ON and GENERALIZES8995. This review confirms that8995 premise only; no verdict on9037's new receiving region is transferred. Its next independent audit is a concrete new frontier.

## Strengthening and improvement opportunities

**Proved refinement on exactly the same wedge domain.** Whole-rectangle
derivative gates in the independent checker give
\[
\partial_vF_x>39/4,\qquad \partial_vF_y>29/4,
\qquad \operatorname{Lip}_wF_j<19/4.
\]
Indeed the major lower bounds are \(H_j-A_0/8\), and the minor upper
bound is \(4+5A_0/384<19/4\). Let \(D_x=39/4,D_y=29/4\),
\(\epsilon=x-X-\rho_j|y-Y|\ge0\). The same actual-pair constraints give
\[
A(n_1)-A(n_2)\ge
(D_j\rho_j-19/4)|y-Y|+D_j\epsilon,
\]
where the positive margins are
\[
D_x\rho_x-19/4=(98-39\phi)/4,\qquad
D_y\rho_y-19/4=(29\phi-37)/20.
\]
This is a quantitative necessary-condition obstruction after the proper
matching reduction, rather than a uniform gap between all noncongruent
poses. It strengthens the originally small y-family margin
\(7\rho_y-5\). The sharper source-row factor \(399/140\) is also valid,
although the simpler factor 3 suffices for this domain.

**Next useful extension, unproved here.** Increasing the minor-to-major
ratio or crossing a Cauchy sign wall requires fresh actual area pieces,
exposed-row-face persistence, receiving area/width bounds for the global
source filter and a branch-exclusion constant dominating the minor area
Lipschitz loss. Improving derivatives alone does not discharge those
obligations. The macroscopic receiving complement needs a sound complete
cover with coverage bookkeeping; a floating search or timeout supplies
neither an extension nor a global exclusion.

**Publication improvement.** The compact source and full written reduction
are adequate for a scoped reproducible ordinary proof. A proof-assistant
formalization should separate the Cauchy/polar geometry, matching-to-frame
bridge and continuum absolute-value estimates. The author's separate
optimized replay did not complete within its supplied 40-second guard
in this pass; improving its avoidable repeated geometry work could make
the author's full replay easier under the unchanged resource limit.
This is an operational suggestion, not a mathematical defect or
authorization to increase resources.

## Reproduction, limitations and graph relations

Python 3.11.2, standard library only. From this directory run separately:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 timeout 40s python3 -B check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 timeout 40s python3 -B -O check.py
```

Each independent run regenerates and compares every one of the **57,076**
expected bytes, SHA256
`01ceac565960ac6a2a0346fa9dcfc8226045541a013c559973e0e6251faf89cf`.
Recorded final runs: normal 3.011 s, optimized 3.205 s; peak child RSS
upper bound 18,012 KiB. Explicit exception guards remain active under
optimization. Four damaged mathematical controls reject; thirteen cube
and eighteen wedge regressions pass. No solver, floating proof decision,
sampled continuum proof or omitted large corpus is used.

The author's full checker was separately replayed from four public,
immutable source directories, with every direct/transitive pin retained.
The normal run completed in 31.576 s, 21,684 KiB and matched all 9,370
expected bytes, SHA256
`4deca6c0c0f721afd75938b55274d96aa91882f2f6cf4f82bb21cac2837ea907`;
it replayed complete filter/fivefold/brightness records and rejected all
six native controls. The optimized native child hit its 40-second guard
and was stopped without a complete result. It was not retried with a
larger budget. That incomplete run is not mathematical failure or
nonexistence evidence.

An optional JSON-only comparison reads the normal native output or the
published target expected.json:

```sh
python3 -B compare.py /path/to/author/expected.json --controls
python3 -B -O compare.py /path/to/author/expected.json --controls
```

Both compare all 26 shared exact field entries across both families,
every physical example/cover field and all four original equatorial labels;
six altered-input controls reject. This is not described as a full native
geometry entry comparison. The independent whole-record proof computation
stands separately from this optional comparison.

Trust boundaries are the exact original coordinate identification,
Python/integer/field semantics, and the written Cauchy/polar, proper-frame,
convex support and continuum estimates. This is not a machine-formal proof.
The mathematical verdict covers 8995, its stated concrete comparison and
the specific 8732/8555/8688 geometry premises reconstructed above. It does
not transfer a verdict to other named-body theorems.

The initial graph review should ABOUT, VERIFIES, REPRODUCES and REFINES
8995; ABOUT problem 7116; DEPENDS_ON the precise filter 8732 and original
geometry 8555 premises, with CITES 8688,8833,7801,8951,8613,8903,8330,9037.
SUPPORTS 8833 is justified by setting \(t=0\) in the confirmed larger
classification. There is no PROVES edge to the open global problem, and
no blanket VERIFIES edge to the full older cap/filter artifacts. Source
publication and actual graph commitment are verified separately.
