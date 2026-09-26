# A rigid-cloud boundary between axial and disjoint-cap maps

Complete author proof, 26 September 2026; independent correctness and
priority review are pending. This note identifies why the existing axial
benchmark is not subsumed by a **single** simultaneous disjoint-cap
reflection, even with arbitrarily many caps and independent rigid changes
of source and target coordinates. It introduces no positive subclass,
new Gaussian comparison or Kneser--Poulsen consequence. The full R3 question
remains open.

The relevant comparison sources are the team's
[three-cap theorem](../gaussian_disjoint_cap_reflections/PROOF.md) and
[hemispherical/four-cap extension](../gaussian_cap_auxiliary_certificates/PROOF.md).
Both give their own R5 motions and arbitrary-radius union/intersection
inequalities. The assertion below concerns the endpoint maps in those
theorems; it does not challenge their positivity. It applies even when no
two-dimensional auxiliary-vector certificate has been supplied.

## 1. Equality on one cloud forces a single global branch

Let K be a convex subset of Euclidean R^d, d>=1. For finitely many unit
normals n_i and offsets beta_i, suppose the relatively open caps

\[
C_i=\{x\in K:n_i\cdot x>\beta_i\}
\]

are pairwise disjoint. Let C_0 be the remaining core. Define F to be the
identity on C_0 and the reflection

\[
H_i(x)=x-2(n_i\cdot x-\beta_i)n_i
\tag{1}
\]

on C_i. Empty caps and boundary labels are permitted. Compactness is not
needed for this lemma, though the positive comparison theorems use compact K.

**Rigid-cloud lemma.** Suppose S is a subset of K and

\[
|F(x)-F(y)|=|x-y|\qquad(x,y\in S).
\tag{2}
\]

Then F restricted to S agrees either with the identity or with one of the
global affine hyperplane reflections H_i. In particular, if S affinely
spans R^d, its induced affine isometry has linear part either I or
I-2nn^T for a unit n.

**Proof.** If S lies in the core, the conclusion is immediate. Otherwise
choose x in S intersect C_i and put a=n_i.x-beta_i>0.

For a core point z in S, direct expansion gives

\[
|x-z|^2-|H_i(x)-z|^2=4a(\beta_i-n_i\cdot z).
\tag{3}
\]

By (2), z lies in the i-th boundary plane. Hence H_i(z)=z=F(z).
Points of S in C_i already satisfy F=H_i.

It remains to consider y in S intersect C_j with j different from i. Put

\[
\begin{gathered}
b=n_j\cdot y-\beta_j>0,\qquad
h_i=\beta_i-n_i\cdot y\ge0,\qquad
h_j=\beta_j-n_j\cdot x\ge0,\\
N=n_i\cdot n_j.
\end{gathered}
\]

The separation inequality from the three-cap source has a short direct
proof: on the segment (1-t)x+ty in K, the i-th cap coordinate is
a-t(a+h_i) and the j-th is -h_j+t(h_j+b). Their positive intervals cannot
overlap, so

\[
\frac{a}{a+h_i}\le\frac{h_j}{h_j+b},\qquad h_i h_j\ge ab.
\tag{4}
\]

With v=a n_i-b n_j, expansion of F(x)-F(y)=x-y-2v gives

\[
\begin{split}
|x-y|^2-|F(x)-F(y)|^2
 &=4E,\\
E&=a h_i+b h_j+2abN\ge2ab(1+N).
\end{split}
\tag{5}
\]

Here a h_i+b h_j>=2sqrt(ab h_i h_j)>=2ab. Equality of distances forces
E=0 and consequently N=-1. Thus n_j=-n_i.

Set c=beta_i+beta_j. In this antipodal case h_i=c+b, h_j=c+a, and
E=(a+b)c. Since a+b>0, E=0 implies c=0. Therefore beta_j=-beta_i:
the two boundary planes coincide, and H_j=H_i as affine maps. This
includes the possibility of two opposite caps on the two sides of one
plane. Thus every y in S also has F(y)=H_i(y), proving the lemma.

When S affinely spans R^d, an affine map is uniquely determined on S;
the last assertion follows. QED.

The complete equality case matters. Merely observing that each point is
assigned one reflection would not prove that the same reflection serves
the whole cloud. Convexity of K supplies (4); disjoint caps on a
nonconvex source set do not supply that argument.

## 2. A coordinate-invariant obstruction for two rigid clouds

**Corollary.** Suppose S_1,S_2 are subsets of K, each affinely spanning
R^d, and F preserves all distances within each. Let U_1,U_2 be the linear
parts of their uniquely induced affine isometries. Then

\[
\operatorname{rank}(U_1-U_2)\le2.
\tag{6}
\]

Indeed the lemma places each U_i in
{I} union {I-2nn^T:|n|=1}. The difference has rank at most one if one
branch is the identity and at most two if both are reflections. Equal
branches cause no exception.

This obstruction survives independent common rigid coordinate changes
on the source and target. Such changes replace both linear parts by
Q U_i P^T, with P,Q orthogonal, and therefore preserve the rank in (6).
Translations affect only the affine constants.

Now take any anchored central flip

\[
X=(0,A,-B),\qquad Y=(0,A,B),
\tag{7}
\]

where A and B each linearly span R^d and d>=3. On the clouds {0} union A
and {0} union (-B), the endpoint affine maps have linear parts I and -I.
Their difference has rank d>2. Consequently **no single disjoint-cap
map of the above form can realize this labeled matching**, even after
independent Euclidean isometries of the full source and target tuples.
The convex set K may be chosen arbitrarily large and the cap count has
no bound. Adding more labels or extending K cannot repair this necessary
condition on the original labels.

This statement does not assume that the endpoint matching is a contraction.
When it is one of our certified axial contractions, it gives a separation
between two positive geometric mechanisms.

## 3. Application to the unchanged axial benchmark

Use exactly [PROOF.md, Section 5](PROOF.md) and [EXPECTED.json](EXPECTED.json):

\[
A=\{(3d/4,1):d\in D_{12}\},\qquad
B=\{(4d/5,1):d\in D_{12}\}.
\]

The rational direction set contains (1,0),(-1,0),(0,1). The three
corresponding vectors in a cloud of slope r form a matrix with
determinant -2r^2. This is -9/8 for A and -32/25 for B, so both clouds
span R3. Adding the common origin makes their affine spans all of R3.
All within-cloud endpoint distances in (7) agree, and

\[
\operatorname{rank}(I-(-I))=3.
\]

The corollary therefore applies to the original 25 labels. Their previous
all-law/all-variance Gaussian and arbitrary-radius ball inequalities still
follow from the original R4 motion. They are not newly proved here.
The argument also applies to every full-dimensional undamped central-flip
domain of modules A or M by restriction to two spanning clouds.

Thus the hemispherical and four-cap theorems do not directly subsume the
axial benchmark by representing its matching with a single cap map. The
proof needs neither their auxiliary-vector condition nor its exact
twelve-normal obstruction. It does not compare the possible internal
energies of two distinct endpoint maps.

## 4. The limitation to one map is essential

The lemma applies separately at each stage of a composition, but the
products of its different reflection branches need not have difference
of rank at most two. We prove no exclusion of finite compositions of
simultaneous disjoint-cap maps.

For example, three successive ordinary coordinate folds x_k->|x_k|,
k=1,2,3, fix the positive orthant and send the negative orthant to its
central reflection. On a bounded box each fold is a one-cap map. Both
orthant clouds can span R3. This illustrates why (6) cannot simply be
telescoped as a rank bound for the final product.

For the specific 25-label axial benchmark,
[COMPOSITIONS.md](COMPOSITIONS.md) separately excludes all finite chains
of **strong contractions** in R3, with changing rigid frames. That proof
is not an exclusion of compositions of the newer disjoint-cap class.
No such larger composition claim is supplied here. Likewise, this note
does not exclude the damped, freely perturbed R2 neighborhood by (2),
since exact within-cloud distance preservation is lost there.

There is no converse containment assertion. Unrestricted extremal-map
and mesh deformation remains researcher 4's lane; the finite certificate
for choosing auxiliary cap directions remains researcher 2's. This
source closes only a specific representation question for the existing
geometric/internal-energy benchmark.

## 5. Provenance and verification boundary

The cap definition, separation inequality (4) and distance deficit in
(5) are credited to the three-cap source, commit
`bd57aa06efc46fd737b962bbd6d96384c4efdf2c`. They are derived explicitly
above so the equality argument can be read on its own. The incoming cap
extension is commit `58ef0e6a38d607cf14f56692d2e80d227760715a`. Its positive
proof and certificate corpus are not independently reviewed here.

The axial core is the frozen portfolio at
`01b707bf3eb19f7bd44b8c45771fffa7b7651b55`; all original proof and checker
files, REGULARITY.md and LIFT_BOUNDARY.md remain unchanged. This is an
author geometric proof and elementary rank calculation, not a formal or
computer-assisted theorem. There is no new checker: the determinant
identities above can be checked directly and the existing fixture is
already in EXPECTED.json. Run `sha256sum -c SHA256SUMS` for source integrity.

No historical novelty is claimed for elementary rigidity or rank facts.
The information added to the portfolio is the precise finite-benchmark
separation, valid for arbitrary cap count and independent rigid frames,
with its one-map boundary. This does not settle historical priority of
the axial Kneser--Poulsen consequence or the matrix-path optimization.
