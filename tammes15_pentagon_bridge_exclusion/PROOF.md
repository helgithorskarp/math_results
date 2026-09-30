# Two small pentagon-bridge contact families are impossible

Author: **six-tammes-2**, role: **researcher**. Date: 2026-09-30.
Status: complete author-audited, unformalized computational lemma.
Independent review is pending. Custom exact arithmetic and the written
geometric reduction are the trust boundary.

## 1. Statement

Let `1/2<t<3/5`. Consider distinct unit vectors in R^3 with all pairwise
inner products at most t. A prescribed contact has inner product exactly t.

The proposed schema consists of two disjoint patches:

* A is a combinatorially triangulated polygon with **five or six** vertices.
  It has respectively seven or nine prescribed edges.
* B is a combinatorially triangulated **pentagon**, with its two ears marked.
  It has seven prescribed edges. An ear is a vertex of degree two in this
  prescribed patch, not necessarily in the complete contact graph.
* Each marked B ear has two additional prescribed contacts to an A pair.
  That A pair has at least one common neighbor in the prescribed A graph.
  The two attached pairs may share vertices.

**Lemma. Neither schema can occur.** The first uses ten distinct labels
and eighteen contacts; the second uses eleven labels and twenty contacts.
Extra contacts and additional packing points are arbitrary. The patches
need not be induced subgraphs. There is no assumption about symmetry,
proximity to a known code, a spherical embedding, facial convexity or a
complete triangle/quadrilateral graph. Noncrossing refers only to the
abstract polygon triangulations.

The lemma therefore supplies forbidden subgraphs for fifteen-point
contact-graph searches throughout this interval. It does not establish
that a global optimizer contains either schema. Global Tammes-15 bounds
and optimality remain unresolved.

For the fifteen-point problem, disjoint caps of radius d/2 give
`cos(d)>=113/225>1/2`. The previously certified incumbent has cosine
less than 3/5. Thus a strict improvement on that incumbent cannot contain
either schema. Incumbent existence is needed only for this corollary;
the interval lemma is independent of its quintic and coordinates.

## 2. Complete combinatorial cover

At a contact point, two unit tangent directions have angular separation
at least `acos(t/(1+t))>pi/3`. Indeed the corresponding neighbor dot
product is `t^2+(1-t^2)cos(phi)<=t`. Six contact neighbors would have
a tangent gap at most pi/3, so every contact degree is at most five.

Two distinct unit vectors have at most two common contact neighbors when
t>0. Their two contact planes intersect in a line, which meets the unit
sphere in at most two points. Antipodal vectors have no such neighbor.
Hence an A pair with two old common A neighbors cannot accept a new
distinct B ear. If the two B ears used the same A pair with its old
neighbor, they would have to coincide. Discard precisely these cases,
and cases of prescribed degree exceeding five. In all retained cases
the old A neighbor is unique and the two attachment pairs differ.

The code compares Catalan triangulation generation against a separate
noncrossing-diagonal enumeration, **entry by entry**:

| A size | Triangulations | Independent diagonal subsets | Dihedral A types | Gluing choices per type |
|---:|---:|---:|---:|---|
| 5 | 5 | 10 subsets of two of five diagonals | 1 | 14 |
| 6 | 14 | 84 subsets of three of nine diagonals | 3 | 21, 26, 33 |

Every A triangulation is degree-compatible before adding the bridges.
B has five triangulations, each with exactly two ears. The five marked
patches form one dihedral orbit. Its representative is the fan
`01,02,03,04,12,23,34`, with ears 1,4. A checked automorphism swaps those
ears. Consequently unordered choices of two different A attachment pairs
cover both assignments of the marked B ears. Both spatial orientations
are retained separately below.

These give **14+21+26+33=94** cases. The cases are templates, not asserted
distinct isomorphism types. Each polygon's deterministic ear removal and
reverse reconstruction is checked against all its original edges. Dihedral
orbit coverage is checked without overlap, and every retained pair is
generated directly from its common-neighbor and degree conditions.

## 3. Exact forced coordinates and all orientations

Choose an equilateral contact triangle as the basis of each patch. Its
Gram matrix is

\[
H=(1-t)I+tJ,\qquad \det H=(1-t)^2(1+2t)>0.
\]

Removing ears leaves a triangle. Reversing this operation forces

\[
a_{new}=\frac{2t}{1+t}(a_i+a_j)-a_{old}.
\tag{1}
\]

There are at most two points at contact distance from i,j; the old
triangle corner is already one of them. Distinctness forces the other.
Thus every realization of the prescribed patch has these coordinates,
up to a common orthogonal transformation. No embedding assumption is
needed. A collision at any stage already prevents a realization.

For an attached A pair, put `w=a_i^THa_j` and let o be its old common
neighbor. The new B ear is forced to be

\[
u=\frac{2t}{1+w}(a_i+a_j)-a_o.
\tag{2}
\]

In a unit realization, `(a_i+a_j) dot a_o=2t` implies
`1+w>=2t^2>0`. In addition, the checker certifies `1+w>0` on the whole
interval for every generated pair. Norm and contact identities for (1)
and (2) are checked exactly as rational functions in Q(t).

The two marked pentagon ears have the required inner product

\[
\kappa=\frac{t(9t^2-2t-3)}{(1+t)^2}.
\tag{3}
\]

Their Gram matrix has rank two throughout the interval:

\[
1-\kappa=\frac{(1-t)(3t+1)^2}{(1+t)^2}>0,\qquad
1+\kappa=\frac{1-t-t^2+9t^3}{(1+t)^2}>0.
\]

The latter numerator has positive Bernstein coefficients on [1/2,3/5].
No antipodal or parallel marked-ear case is discarded.

For each gluing let u,v be the two forced A-frame ears. A necessary
scalar equation is `u^THv-kappa=0`. When it holds, exactly two isometries
map the independent B ears to u,v. To see this constructively, for a B
point x set

\[
\begin{aligned}
\beta_1&=x^THb_p,&\beta_2&=x^THb_q,\\
r_1&=\frac{\beta_1-\kappa\beta_2}{1-\kappa^2},&
r_2&=\frac{\beta_2-\kappa\beta_1}{1-\kappa^2},\\
\lambda_x&=\frac{\det(H)\,x\mathbin\cdot(b_p\times b_q)}{1-\kappa^2}.
\end{aligned}
\]

Its two A-frame images are

\[
r_1u+r_2v\ \mathbin\pm\ \lambda_x H^{-1}(u\times v).
\tag{4}
\]

The ordinary coefficient dot and cross products in this expression are
distinguished from the H-metric dot. The H-normal's squared norm is
`(1-kappa^2)/det(H)`, independent of the frame, so (4) covers the two
orientations. The checker verifies the fixed ears, anchor Gram matrix,
all unit norms and all prescribed contacts on every tested branch.
All divisions have been covered by the positivity above or by exact
invertibility at the isolated root.

## 4. Residuals and explicit contradictions

The 94 exact scalar residuals divide as follows:

| Model index | A size/type | Cases | No interval root | Identically zero | Isolated-root cases |
|---:|---|---:|---:|---:|---:|
| 0 | pentagon fan | 14 | 12 | 2 | 0 |
| 1 | hexagon type 0 | 21 | 21 | 0 | 0 |
| 2 | hexagon type 1 | 26 | 24 | 2 | 0 |
| 3 | hexagon type 2 | 33 | 27 | 3 | 3 |
| Total | | **94** | **84** | **7** | **3** |

For every nonzero numerator the stdlib checker uses a signed exact Sturm
sequence, removes endpoint factors, and counts distinct roots in the
open interval. The three active cases are model3/cases19,22,26. Their
only relevant root is `t=1/sqrt(3)`, of `3t^2-1`, isolated between
57735/100000 and 57736/100000. The checker verifies the factor identity,
the residual's vanishing in the exact quotient, both bracket signs and
the complete root count. No numerical root list or trusted CAS
factorization is used to establish coverage.

All fourteen identity-case orientations violate packing. The witness
inner-product gap is one of just two positive rational functions:

\[
C=1-t>0,\qquad
G=\frac{(1-t^2)(5t^2-1)}{1-t-t^2+9t^3}>0.
\tag{5}
\]

C records an exact collision. G is strictly positive since t>1/2 and
t<3/5. The actual rational functions are recomputed, and their numerator
and denominator Bernstein signs are also checked.

All six isolated orientations likewise violate packing. Their witness
inner products are one of

\[
R=2t-1/3>t,\qquad S=2/3+t/3>t.
\tag{6}
\]

The inequalities follow respectively from `t>1/3` and `t<1`.
Exact quotient arithmetic reduces each actual witness Gram entry to
the displayed form, and its interval sign is checked.

The compact [certificate](certificate.json) identifies every witness
pair and both orientations. The [expected output](EXPECTED.json) records
the recomputed C/G gaps and R/S Gram entries for all twenty branches.
No identity or root branch remains, so the schema cannot be a packing.
This proves the lemma before adding any further points; an extension
polytope or extra-point capacity argument is unnecessary.

## 5. Reproduction, validation and limitations

Use CPython >=3.11, standard library only:

```sh
python3 -B tammes15_pentagon_bridge_exclusion/check.py | cmp - tammes15_pentagon_bridge_exclusion/EXPECTED.json
python3 -B tammes15_pentagon_bridge_exclusion/check.py --selftest
python3 -B -O tammes15_pentagon_bridge_exclusion/check.py --selftest
(cd tammes15_pentagon_bridge_exclusion && sha256sum -c SHA256SUMS)
```

The optional generator uses SymPy1.14.0:

```sh
python3 -B tammes15_pentagon_bridge_exclusion/generate_certificate.py | cmp - tammes15_pentagon_bridge_exclusion/certificate.json
```

The generator independently derives all 94 A/B coordinates, forced ears
and scalar residuals in SymPy's Q(t) field, comparing each with the
integer rational-function implementation before factorization. It also
constructs both frames in that field and verifies all twenty witness
Gram entries against the stdlib expressions, reducing modulo `3t^2-1`
where needed. It reads no certificate, expected output, coordinates,
scratch input or network. It shares the geometric formulas and combinatorial
cover, so this is a separate arithmetic check, not independent peer review.

Selftests cover field inversion and linear solving, constant polynomial
normalization, endpoint and repeated-root Sturm counting, and seven
false-certificate rejections: a false bracket, a prescribed edge as a
zero/root witness, an invalid orientation, and a missing entry from each
active/zero/root table. Rejections remain active under Python -O.
The geometric reflection and two-orientation arguments are unformalized.
Ordinary Python execution and custom exact integer/Fraction arithmetic
remain in the trust boundary.

## 6. Literature and complementary frontier

The [Musin–Tarasov seed](https://arxiv.org/abs/1410.2536) proves the
fourteen-point problem. The live [spherical-code table](https://spherical-codes.org/)
retains an unstarred fifteen-point row, with the same
[coordinate file](https://spherical-codes.org/data/3/15), SHA256
`1b77ee43d73613885d3fdcfb03dc8fad2e40302ff9c9ff639559cc9b326fb805`.
The known incumbent construction and its exact polynomial are prior art;
this is not a new packing or a historical-priority claim.

This lemma continues six-tammes-2's earlier
[eight/five](../tammes15_reflection_family_exclusion/PROOF.md) and
[seven/six](../tammes15_seven_six_family_exclusion/PROOF.md) forbidden
families. It uses fewer labels and contacts and needs no extension
certificate. These families have different schemas; no inclusion or
supersession of either earlier family is claimed. Their arithmetic helpers
are reused in this self-contained directory. None is a premise of the
new interval lemma.

The current complementary source by **six-tammes-1**, role **researcher**,
[zero-triangle reduction](../tammes15_eight_quad_reduction/TWO_ZEROS.md),
source `facf5229d14e35bd0cd6674dfdaff7f71d9f95e5`, excludes the whole
two-zero-triangle-four distribution and one mixed profile. Under its
explicit complete connected convex cellular TQ, degree3..5, q8 assumptions,
ten necessary profiles and eleven global auxiliary types remain.
Its lemma is committed as
`bafkreiejc2toh5rhgmpxt6tprk4ggr7gk3nedfoeewazpurkhcp22pqu2q`, h7380.
This context is not a premise or an independently reviewed verdict.
Its largest mixed profile has only ten triangle-incident vertices, making
the ten-label clause a possible filter where thirteen-label motifs cannot
occur. Neither the existence nor the forced occurrence of our prescribed
bridges in those profiles is established here.

Useful next work is to prove an occurrence restriction or apply these
small forbidden subgraphs inside a complete justified contact-graph
enumeration. Larger faces, embedding/optimizer coverage and surviving
geometric profiles remain separate obligations. Repeatedly finding that
a specified patch is forbidden does not resolve those obligations.
