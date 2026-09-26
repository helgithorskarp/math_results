# Three centered moment forms and constrained nine-plane configurations

Complete author proof; independent review is pending.

Let \(S\subseteq\mathbb F_5^3\) have 72 points and contain no complete
five-point affine line. Write \(a_m\) for its number of affine plane
sections of size \(m\). Moment calculations are in \(\mathbb F_5\);
section sizes and inequalities are ordinary integers.

Define the finite-field barycenter and centered second-moment matrix
\[
\mu=72^{-1}\sum_{x\in S}x=3\sum_{x\in S}x,\qquad
M=\sum_{x\in S}(x-\mu)(x-\mu)^T.
\]
For a column normal \(v\), put
\[
Q(v)=v^TMv=\sum_{x\in S}\bigl(v^T(x-\mu)\bigr)^2.
\]
Under \(x\mapsto Ax+b\), the centered matrix becomes \(AMA^T\).
Its congruence class is therefore an affine invariant. No positivity
interpretation of this finite-field matrix is intended.

**Theorem.** Every such set has \(M\) congruent to exactly one of the
following three types:

| Representative | Possible number \(a_9\) |
|---|---|
| \(\operatorname{diag}(1,0,0)\) | \(11\le a_9\le16\) |
| \(\operatorname{diag}(1,2,0)\) | \(a_9\in\{11,12\}\) |
| \(\operatorname{diag}(1,1,1)\) | \(a_9\in\{11,12\}\) |

These are necessary conditions, not existence assertions. The zero,
nonsquare rank-one, split rank-two and nonsquare-determinant rank-three
types are impossible.

Every nine-point plane has a centered equation
\[
v^T(x-\mu)=a,\qquad a\ne0,\qquad Q(v)=-a^2,              \tag{1}
\]
and its unique fifteen-point parallel companion has centered offset
\(3a\). In particular every nine-point plane avoids \(\mu\).

In the rank-two case the nine-plane normals occupy three projective
lines through the radical. Their occupancy counts, up to ordering, are
\((3,4,4)\) or \((4,4,4)\).

In the nonsingular case the square-valued normals are naturally the 15
edges of a complete graph on the six points of the conic \(Q=0\).
The edges omitted by the nine-plane normals form one of:

* a perfect matching, when \(a_9=12\);
* \(K_{1,3}\sqcup K_2\), \(P_4\sqcup K_2\), or
  \(P_3\sqcup P_3\), when \(a_9=11\).

Here \(P_j\) denotes the path on \(j\) vertices. This restricts the
normal configurations; it does not assert that any of them lifts to
an actual 72-point set.

## 1. Attributed finite-geometry premises

The [global low-plane reduction](../low_planes72/README.md) supplies:

1. A line-free subset of an affine plane of order five has size at most
   16.
2. Low planes, meaning sections of size at most nine, have distinct
   projective normal directions, and at most four of those directions
   lie on any projective line.

The new [no-eight-plane theorem](../no_eight_planes72/THEOREM.md)
establishes \(a_8=0\) and that every section has size at least nine.
The [nine-plane-frame theorem](../nine_plane_frame72/THEOREM.md)
proves \(3a_8+a_9\ge11\), hence
\[
a_9\ge11.                                              \tag{2}
\]
These results are imported with their stated computational trust
boundaries. The argument below does not reprove their SAT exclusions.

## 2. The barycenter determines the low-plane offsets

Fix \(v\ne0\), and let
\[
n_t=\bigl|\{x\in S:v^T(x-\mu)=t\}\bigr| \quad(t\in\mathbb F_5).
\]
Then \(\sum_tn_t=72\), \(\sum_ttn_t=0\), and
\(Q(v)=\sum_tt^2n_t\).

If a section has nine points, its four parallel companions have total
63 and each has at most 16 points. Their sizes are therefore
\(15,16,16,16\). Write \(a,b\) for the centered offsets of the nine-
and fifteen-point planes. Modulo five,
\[
n_t=1+3\mathbf1_{t=a}-\mathbf1_{t=b}.
\]
Because \(\sum_{t\in\mathbb F_5}t=\sum_tt^2=0\), the first moment gives
\(b=3a\). The two planes are distinct, so \(a\ne0\).
The second moment is
\[
Q(v)=3a^2-b^2=3a^2-9a^2=-a^2.
\]
This proves (1). Since \(-1=4\) is a square, \(Q(v)\) is a nonzero
square. Replacing \(v\) by a nonzero scalar multiple multiplies
\(Q(v)\) by a square, so the restriction is well-defined projectively.

There are also higher-moment identities. With
\[
T(v)=\sum_{x\in S}(v^T(x-\mu))^3,\qquad
U(v)=\sum_{x\in S}(v^T(x-\mu))^4,
\]
the same residues give
\[
T(v)=a^3,\qquad U(v)=1.                                \tag{3}
\]
Indeed \(\sum_tt^3=0\), \(\sum_tt^4=-1=4\), and \(a^4=1\).
In particular \(a=T(v)^3\). These extra identities are available for
future compatibility tests but are not required to classify \(M\).

## 3. Only three congruence types survive

Every symmetric form over \(\mathbb F_5\) diagonalizes by congruence.
For a nonzero form, polarization gives a vector of nonzero self-pairing;
split it off and repeat. Every nonzero diagonal entry scales to 1 or 2.
Pairs of entries 2 may be replaced by pairs of entries 1, because
\[
B=\begin{pmatrix}1&1\\1&-1\end{pmatrix},\qquad B^TB=2I_2.
\]
The rank and the square class of the determinant of the nondegenerate
part distinguish the seven resulting types.

Evaluating at the 31 projective representatives whose first nonzero
coordinate is 1 gives this table:

| Diagonal representative | \(Q=0\) | Nonzero square | Nonsquare |
|---|---:|---:|---:|
| \((0,0,0)\) | 31 | 0 | 0 |
| \((1,0,0)\) | 6 | 25 | 0 |
| \((2,0,0)\) | 6 | 0 | 25 |
| \((1,1,0)\), split rank two | 11 | 10 | 10 |
| \((1,2,0)\), anisotropic rank two | 1 | 15 | 15 |
| \((1,1,1)\) | 6 | 15 | 10 |
| \((1,1,2)\) | 6 | 10 | 15 |

Every nine-plane normal is in the square column, and the normals are
distinct. Equation (2) excludes every type with fewer than eleven entries
in that column. Precisely the three stated types survive.
The small table can be checked directly; the supplied audit additionally
diagonalizes all \(5^6=15\,625\) symmetric matrices and verifies their
projective character counts.

## 4. Rank one: an affine dual line-free set

For \(Q(v)=v_1^2\), its square-valued projective normals have unique
representatives \((1,u,w)\), with \(u,w\in\mathbb F_5\). They form an
affine plane in the dual projective plane. Five collinear points in this
affine plane would violate the imported exclusion of five collinear
low-plane normals. The nine-plane normals thus give a line-free subset
of \(\mathbb F_5^2\), which has size at most 16.

Equation (1) also gives \(a=\pm2\). In centered primal coordinates every
nine-point plane consequently passes through one of the two points
\((2,0,0)\) and \((-2,0,0)\), according to its offset. This does not
say whether those two points belong to \(S\).

## 5. Rank two: three almost-full pencils

For \(Q(v)=v_1^2+2v_2^2\), the radical is
\(R=(0,0,1)\). It is the sole zero of \(Q\) in the projective plane.
Projective lines through \(R\) correspond to directions
\((v_1:v_2)\) in \(\operatorname{PG}(1,5)\).

At the representatives \((1,t)\), \(t=0,1,2,3,4\), and \((0,1)\),
the values of \(v_1^2+2v_2^2\) are
\[
1,\ 3,\ 4,\ 4,\ 3,\ 2.
\]
Exactly three are squares. Thus the 15 square-valued normals form three
projective lines through \(R\), each with \(R\) removed. The nine-plane
normals occupy at most four points on each line, giving \(a_9\le12\).
Together with (2), their occupancies must be \((3,4,4)\) or \((4,4,4)\).

## 6. Rank three: a graph on the six conic points

Take \(Q(v)=v_1^2+v_2^2+v_3^2\). Its zero locus \(C\) has six projective
points. For \(p\in C\), the tangent is \(L_p=\{v:p^Tv=0\}\).
The square-valued locus \(E\) has 15 points. The following small incidence
facts hold:

1. Each \(L_p\) contains \(p\) and five points of \(E\).
2. Each point of \(E\) lies on exactly two of the six tangents.
3. Each pair of distinct tangents meets in a distinct point of \(E\).

For an elementary check, list
\[
C=\{(1,2,0),(1,3,0),(1,0,2),(1,0,3),(0,1,2),(0,1,3)\}
\]
and use the displayed tangent equations. This verifies all six tangent
sections and their fifteen pairwise intersections. The checker repeats
those evaluations exactly. Thus \(E\) is identified with the edges of
\(K_6\), an edge recording its two tangent endpoints.

Let \(G\) be the graph consisting of the \(a_9\) nine-plane normals.
On every tangent at most four of its normals may occur. Consequently
\(\deg_G(p)\le4\), and the handshaking identity gives \(a_9\le12\).
The complement \(H=K_6\setminus G\) has no isolated vertices.

If \(a_9=12\), then \(H\) has three edges covering six vertices, so it is
a perfect matching. If \(a_9=11\), it has four edges, six nonisolated
vertices, and total degree eight. Its degree sequence is either
\((3,1,1,1,1,1)\) or \((2,2,1,1,1,1)\). The first gives
\(K_{1,3}\sqcup K_2\). The second gives \(P_4\sqcup K_2\) or
\(P_3\sqcup P_3\): no cycle is possible with only two vertices of
degree two. This proves the listed alternatives.

## 7. Simultaneous conditions in the BBB normalization

The prior frame theorem supplies coordinates with ordered section
profile \((9,15,16,16,16)\) along all three axes. In that gauge,
\[
\mu=(2,2,2),\qquad M_{11}=M_{22}=M_{33}=1,\qquad
M_{ij}=\sum_{x\in S}x_ix_j+2\quad\hbox{in }\mathbb F_5.   \tag{4}
\]
For one axis, the first raw moment is 4, giving barycenter coordinate
\(3\cdot4=2\); its centered second moment is 1. Centering subtracts
\((72\bmod5)\mu_i\mu_j=2\cdot4=3\), which is addition of 2.

Only the three off-diagonal entries are unknown. Among their 125
possibilities, the surviving types have respectively 4, 16, and 77
matrices. The excluded types account for the other 28: six split
rank-two and 22 nonsquare-determinant rank-three matrices. These finite
counts are audit controls, not claims of geometric realizability.

For any nine-plane \(v^Tx=d\), its centered offset is
\(a=d-2(v_1+v_2+v_3)\); (1) and (3) apply in these same coordinates.
Diagonalizing \(M\) generally changes the BBB profiles, so the two
normalizations must not be imposed simultaneously without a separate
argument.

## 8. Evidence and limits

The proof after the attributed premises uses finite-field algebra and
elementary finite geometry. The standard-library replay checks every
symmetric matrix, every tangent incidence, all relevant normal subsets,
the low-profile identities, and affine covariance controls. The
normal-subset enumeration confirms 875 admissible subsets of size at
least eleven in the rank-two square locus and 345 in the nonsingular
square locus. These are necessary normal configurations, not point sets.

The inherited planar and low-plane certificates and the weighted
nine-plane inequality were replayed. The 1,252 new mixed-plane DRAT
proofs and the preceding 164 two-eight-plane proofs are explicit
dependencies, not rerun or independently reviewed here. Ordinary code,
the written reductions and those prior computer-assisted theorems remain
trust boundaries. There is no floating-point premise, new SAT verdict,
proof-assistant formalization, or peer-review claim.

The known frontier remains \(70\le r_5(\mathbb F_5^3)\le72\).
The advance excludes four affine moment types and restricts the two
surviving higher-rank types to nearly saturated, explicitly described
normal configurations. It does not settle existence at 71 or 72.
