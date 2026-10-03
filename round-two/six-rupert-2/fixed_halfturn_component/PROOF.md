# J74: a complete half-turn receiving component and its width rigidity

six-rupert-2, actual role researcher; 2026-10-03. Exact intermediate
construction and classification for a specified source motion. Author checked,
unformalized, independently **UNREVIEWED**. The global standard Rupert property
of the metabigyrate rhombicosidodecahedron J74 remains **OPEN**.

## The original solid, source motion and quantified claims

Let $K=\operatorname{conv}\{V_0,\ldots,V_{59}\}$ be the ORIGINAL unit-edge J74
of [model8551](../model.py), source
25fc9695745b6832d068d18544452b7852b5847f, graph
bafkreig4wvsmlau4koaib63i3cefofih67cczseu3hgdv2r6r54ga572aq.
The checker reconstructs the two NONOPPOSITE cupola gyrations and matches all
sixty literal originals. Put $s=\sqrt5$ and

$$
a=(s-1)/4,\quad b=(s+1)/4,\quad c=1/2,\quad
v=(-b,a,c),\qquad
G=2vv^T-I=\begin{pmatrix}a&-c&-b\\-c&-b&a\\-b&a&-c\end{pmatrix}.
$$

$v$ is unit and $G$ is an actual proper absolute half-turn. All originals
have squared radius $R^2=(11+4s)/4$. The ORIGINAL pairs $(0,7),(1,6),(2,5)$
are antipodal with independent positive members, so the origin is interior.
No centrality assumption about $K$ is made. The actual full-body symmetries

$$H=\operatorname{diag}(-1,-1,1),\qquad M_x=\operatorname{diag}(-1,1,1)$$

are checked as permutations of all sixty originals. Only $H$ is proper.

Use the whole affine receiving chart $r=(x,1,-y)$, with $x,y\in\mathbb R$,
and $\Pi_r=I-rr^T/(r\cdot r)$. Define

$$F=\{(x,y):\Pi_r(GK)\subseteq\Pi_r K\},\quad
q=((s-1)/2,(3-s)/2),\quad t=(3-s)/2,\quad \ell=(5s-9)/22.$$

The ENTIRE connected component of $F$ containing $q$ is the closed hexagon

$$
\mathcal H=\operatorname{conv}\left\{
(1,0),q,(\ell,t),(\ell,-t),((5-s)/10,-t),((3+s)/6,(s-3)/6)
\right\}.
\tag{1}
$$

The vertices in (1) are in positive cyclic order. Its equivalent six
closed inequalities are

$$
x+y\le1,\quad y\le t,\quad x\ge\ell,\quad y\ge-t,\quad
1+\frac{5-3s}{2}x+2y\ge0,\quad x-y\le1.
\tag{2}
$$

The double area is $63/11-349s/165>0$. This is a complete receiving
component for the FIXED ORIGINAL $G$ with scale ONE and translation ZERO,
not an arbitrary-source receiving exclusion. Other components of $F$ are
not inventoried.

For EVERY receiver in $\mathcal H$, EVERY physical $T\in r^\perp$ and
EVERY enlargement $\lambda\ge1$, the stronger fixed-family assertion is

$$
\lambda\Pi_r(QK)+T\subseteq\Pi_r K
\quad\Longleftrightarrow\quad \lambda=1,\ T=0,
\qquad Q\in\{G,GH,C_r(G),C_r(GH)\},
\tag{3}
$$

where (3) is asserted **separately for each displayed $Q$**, and

$$M_r=I-2rr^T/(r\cdot r),\qquad C_r(g)=M_r g M_x.$$

The displayed motions are retained as a SET; no constant distinct-motion
count is required. The two improper factors make each $C_r(g)$ proper.
All these fits retain actual contact, so they do not furnish a strict
Rupert passage. The previous [all-source three-cell result9918](../joint_phase4/PROOF.md)
found the extra $G$ fit at $q$. Its receiving/source forest and local collar
are not premises of (1)--(3). The present construction continues this fit
over a two-dimensional receiving component.

## Elementary signed ray criterion

For any $w\in\mathbb R^3$,

$$\Pi_r w\in\Pi_r K\quad\Longleftrightarrow\quad
\text{the line }w+\mathbb Rr\text{ meets }K.\tag{4}$$

Exactly forty originals of $GK$ coincide spatially with originals of $K$.
The other twenty are identified in [expected.json](expected.json). For each
noncommon $w=GV_k$, all sixty values $R^2-w\cdot V_j$ are strictly positive.
Thus $w\notin K$. Moreover $w\cdot z<R^2$ for every $z\in K$.
If $z=w+ur\in K$, then $u(w\cdot r)<0$. In particular $w\cdot r$ cannot
vanish at any feasible receiver, and the ray sign is forced:

$$\sigma_k=-\operatorname{sign}(w\cdot r),\qquad
w+\tau\sigma_k r\in K\text{ for some }\tau>0.\tag{5}$$

On every connected subset of $F$, each of these twenty signs is constant.
For the component of $q$, freeze the signs at $q$.

This is elementary convex geometry and one-variable elimination. The new
content here is the exact component and contact closure for the original
named solid; no novelty claim is made for the general ray criterion.

## Necessary component bounds from actual supporting planes

For each of the sixty-two listed ORIGINAL spatial facets, rebuild an
outward plane $N_f\cdot z\le h_f$, choosing $h_f>0$. The checker verifies
all $62\cdot60=3,720$ original point inequalities and the ENTIRE tight
original facet. Necessity below uses actual supports only. Sufficiency
will use literal convex combinations of originals, not an assumption that
these sixty-two halfspaces completely describe $K$.

For a noncommon $w$, put $d_f=h_f-N_f\cdot w$ and
$a_f=\sigma_k N_f\cdot r$. A ray meeting $K$ must have

$$d_f-\tau a_f\ge0\quad\text{for every }f.\tag{6}$$

When $d_f<0$, (6) requires $a_f<0$ and $\tau\ge d_f/a_f$.
When $d_f=0$, it requires $a_f\le0$. For a negative $d_f$ and positive
$d_i$, eliminating $\tau$ gives the necessary linear form

$$\sigma_k(d_fN_i-d_iN_f)\cdot r\ge0.\tag{7}$$

If $a_i>0$, this follows by comparing the lower and upper ray bounds; if
$a_i\le0$, both terms in the same inequality already have the required
sign. Also retain $-\sigma_k N_f\cdot r\ge0$ for $d_f\le0$.

[ray.py](ray.py) reconstructs all rows, giving 1,191 distinct nonzero
affine forms in $(x,y)$. At all six closed corners their 7,146 controls
are nonnegative. Each of the six normalized sides of (2) is a literal
row (7). In original facet/source order, the witnesses are

| Side in cyclic order | Original moved source $k$ | Negative facet $f$ | Positive facet $i$ |
|---|---:|---:|---:|
| $1-x-y\ge0$ | 14 | 32 | 24 |
| $1-(3+s)y/2\ge0$ | 15 | 40 | 36 |
| $-1+(9+5s)x/2\ge0$ | 20 | 39 | 10 |
| $1+(3+s)y/2\ge0$ | 57 | 41 | 36 |
| $1+(5-3s)x/2+2y\ge0$ | 18 | 17 | 7 |
| $1-x+y\ge0$ | 25 | 30 | 22 |

The raw triples are divided by the absolute value of their first nonzero
coefficient; their inequality direction is preserved. They are recorded
in [certificate.json](certificate.json) and checked against the newly
rebuilt original rows. Consequently any feasible receiver with the $q$
sign pattern lies in all six halfplanes (2).

Here $0<\ell<1$, $0<t<1$, and the first/last inequalities imply
$x\le1-|y|\le1$. Thus the whole intersection lies in the unit box, and
clipping this box with the six genuine inequalities is a COMPLETE
intersection calculation. It gives exactly (1). All endpoints remain.
Every side vanishes at its two cyclic endpoints and is strict at the
other four. These checks and positive area also verify the literal
convex hexagon; area alone is not a coverage argument.

## Sufficient rays from actual original triangles

For every one of the twenty noncommon source originals and every one of
the six receiver corners, the certificate supplies a positive rational
quadratic-field ray parameter $\tau_{kj}$ and three nonnegative
quadratic-field barycentric coefficients summing to one, at three
literal ORIGINAL facet vertices. It checks the vector identity

$$
w+\tau_{kj}\sigma_k r_j
=\beta_0V_{i_0}+\beta_1V_{i_1}+\beta_2V_{i_2}\in K.
\tag{8}
$$

All 120 identities are recomputed directly. No computed ray point is
trusted merely because it satisfies the facet halfspaces. Genuine zero
barycentric coefficients at edges/corners are allowed. Every original
corner/source pair occurs exactly once. The 120 strict sign margins
$-\sigma_k w\cdot r_j$ have minimum $(15-s)/22>0$.

For any $p\in\mathcal H$, write $p=\sum_j\theta_jp_j$ with nonnegative
$\theta_j$ summing to one. Because raw $r_y=1$, also
$r=\sum_j\theta_jr_j$. For each $w$, set

$$
c_k=\sum_j\frac{\theta_j}{\tau_{kj}}>0,\qquad
z_k=\sum_j\frac{\theta_j/\tau_{kj}}{c_k}
       (w+\tau_{kj}\sigma_k r_j)\in K.
$$

Then $z_k=w+c_k^{-1}\sigma_k r$. This proves (4) throughout the ENTIRE
closed hexagon. The forty common originals already lie in $K$.
Linearity and convexity then give $\Pi_r(GK)\subseteq\Pi_rK$ everywhere.

All twenty signs remain strict and constant on this hexagon. The necessary
bounds and sufficient rays therefore prove that its whole sign stratum
in $F$ is exactly $\mathcal H$. This convex set is connected and contains
$q$. Since feasible connected sets cannot change any sign, it is the
ENTIRE connected component of $F$ containing $q$. No source direction,
silhouette chamber or numerical search range is omitted from that
fixed-motion/component assertion.

## Antipodal contacts close enlargement and physical translation

The new width certificate is a separate finite receiving cover of the
whole hexagon. Its five nontrivial straight-line split nodes each retain
BOTH closed children, yielding six nondegenerate closed leaves. For a
split line $L$, a parent point has either $L\ge0$ or $L\le0$ (both at
equality). Thus exact clipping gives full closed coverage recursively.
Both children have positive area, and their areas sum to the parent as
a checksum. This linear case split, rather than an area-only inference,
is the cover proof. The checker reconstructs every leaf from the root,
rejecting missing, duplicate, unused and ancestor references.

On each leaf, the certificate specifies three ORIGINAL directed edges
$e_i=V_{j_i}-V_{i_i}$ with fixed signs $\epsilon_i$. Define

$$m_i(r)=\epsilon_i(e_i\times r),\qquad h_i(r)=m_i(r)\cdot V_{i_i}.$$

For ALL original receiving vertices, at ALL closed leaf corners, the
checker proves both $h_i-m_i\cdot V_j\ge0$ and
$h_i+m_i\cdot V_j\ge0$. These 8,640 actual point controls extend over
the whole leaves by affinity. There are 36 genuine ORIGINAL source
preimages of the positive and negative contacts: both $V_{i_i}$ and
$-V_{i_i}$ lie spatially in $GK$, verified as images of literal originals.
No centrality of $K$ is used.

Every leaf has $h_i\ge0$ and $\sum_i h_i>0$ throughout. Its three spatial
edge vectors have nonzero constant determinant, either $1/2$ or
$(s-1)/4$. For a physical enlarged translated fit, the genuine opposite
source contacts imply

$$\lambda h_i+m_i\cdot T\le h_i,\qquad
\lambda h_i-m_i\cdot T\le h_i.\tag{9}$$

Summing (9) over both signs and over $i$ gives
$2\lambda\sum_i h_i\le2\sum_i h_i$. Hence $\lambda\le1$, and the
mandated $\lambda\ge1$ forces $\lambda=1$. The two separate inequalities
then give $m_i\cdot T=0$ for all three $i$, including a possibly zero
height. Thus $e_i\cdot(r\times T)=0$ for a basis of $\mathbb R^3$, so
$r\times T=0$. Since $T\in r^\perp$, this forces $T=0$.

Conversely the exact rays prove the unit/T0 fit. This proves (3) for $G$.
Actual RIGHT $H$ gives $GHK=GK$. For the proper companions,
$\Pi_rM_r=\Pi_r$ and $M_xK=K$, so

$$\Pi_r(C_r(g)K)=\Pi_r(gK).\tag{10}$$

This preserves the entire translated/enlarged shadow condition and gives
(3) for all displayed motions. Positive summed height in (9) supplies an
actual nonzero support contact, excluding strict interior containment for
this family. Neither a local rotation collar nor an arbitrary-source
classification follows from this width argument.

## Author verification and precise trust boundary

[check.py](check.py) rebuilds the ORIGINAL solid and named motions,
all actual facet planes, all necessary ray forms, all 120 barycentric ray
identities, all 120 strict sign controls, the complete BOTH-child receiving
tree and every actual opposite support. It checks only exact standard-library
Fraction arithmetic in ordered $\mathbb Q(\sqrt5)$, credited to
[the earlier public field implementation](../q5.py). Pre-import pins are
in [DEPENDENCIES.json](DEPENDENCIES.json). No old source tree, proof corpus,
local dual/collar, floating generator, private journal or old receiving
theorem is an input.

A different, direct projected-hull algorithm checks all six receiving
corners: 5,700 source point/receiving edge comparisons. The rank-two screen
$z\mapsto(z_x-xz_y,z_z+yz_y)$ has kernel $\mathbb Rr$ and preserves
projection containment. It confirms equal shadows at corners0,4,5 and
proper closed containment at corners1,2,3. At $q$, receiver/source have
13/12 hull corners. This is corroboration at six fixtures; the conic proof
above supplies the continuum. All 720 literal original companion point
identities are also checked.

The COMPLETE mathematical records in normal and optimized Python match
[expected.json](expected.json). [VALIDATION.json](VALIDATION.json) records
fresh empty relocated replays, [semantic certificate rejection controls](controls.py),
hashes, commands, measured resources and exact scope. Hashes bind the
regenerated records; the ordinary convex-cone and width identities above
give their mathematical meaning. This is an ordinary author-checked exact
proof, not proof-assistant formalization or independent review.

From the repository root, CPython3.11.2, standard library:

```bash
python3 round-two/six-rupert-2/fixed_halfturn_component/check.py --output /tmp/j74-G-normal.json --compare round-two/six-rupert-2/fixed_halfturn_component/expected.json
python3 -O round-two/six-rupert-2/fixed_halfturn_component/check.py --output /tmp/j74-G-optimized.json --compare round-two/six-rupert-2/fixed_halfturn_component/expected.json
```

Production has no numerical search, tolerance, empty-region inference,
solver or proof enumeration. It uses one intensive child at a time,
threads one and unchanged1CPU2GiB under a45-second local child guard.
Failure, timeout or incomplete certificate is not mathematical exclusion.

## Located literature and complementary context

[Gosain--Grimmer Table4](https://arxiv.org/html/2509.08190#S3.T4)
retains J72,J73,J74,J75,J77 without a strict passage.
[Zeng Sections1.1--1.2](https://arxiv.org/html/2604.26531)
reports87/92 Johnson solids Rupert, uses proper rotations, physical
translation and strict INTERIOR containment, and leaves the
rhombicosidodecahedron non-Rupert assertion conjectural.
[The proved Noperthedron](https://arxiv.org/abs/2508.18475)
is a different solid. Bounded fresh primary/graph/source searches do not
certify exhaustive historical priority. Strict containment is essential;
proper shadow inclusion with contact does not establish Rupert property.

The full original/source-matched complementary
[RID fixed-motion segment9896](../../six-rupert-3/rid_midpoint_closed_family/PROOF.md)
and [pentagonal all-source triangle9932](../../six-rupert-1/pentagonal_whole_triangle31/PROOF.md)
were read for method context. The former classifies one different body's
touching segment; the latter covers every source over a different body's
receiving triangle. Their bodies, centrality, proper groups, fields,
contacts, constants, source decoders, local collars and equality inventories
are not premises here. No reviewer verdict or production replay of them
is claimed.

The next frontier is a genuine five-wrench local rotation obstruction
around $G$ on these new actual receiving pieces, followed by any required
full original-source cover. Other original source rotations on this
hexagon and the global named J74 property remain OPEN.
