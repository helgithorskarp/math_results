# Independent upper-six proof and seventeen necessary third prefixes

Actual author: **six-reviewer-4**, independent mathematical reviewer.
Shared signing identity does not establish distinct authorship.
This independently written argument audits researcher six-heesch-3's
[h7982 theorem](https://github.com/helgithorskarp/math_results/blob/main/heesch_trapezoid_six_upper_bound/proof.md)
and gives a new necessary six-depth catalog. Contact-ball methods and all
imported geometric reductions retain their existing attribution.

## 1. Tile and explicit imported classification

The skeleton \(S\) has axial vertices \((0,-1),(8,-1),(7,1),(0,1)\).
Axial \((q,r)\) means \((q+r/2,\sqrt3r/2)\). A counterclockwise unit chord
has physical boundary
\[
 v+te+\frac{\sigma}{100}t^2(1-t)^2(e_y,-e_x),\qquad 0\le t\le1.
\]
Seven upper and two left ports have \(\sigma=1\); eight lower ports have
\(\sigma=-1\). The remaining side of length \(\sqrt3\) is straight.
These are physical boundaries of an unmarked connected Jordan disc \(T\).
[provenance.json](provenance.json) pins every input.

A finite packing consists of distinct congruent closed \(T\) copies with
disjoint interiors. A strict-surround chain is a nested sequence
\(F_0=\{A\},F_1,\ldots,F_H\), with \(U_j=\bigcup F_j\) and
\(U_{j-1}\subset\operatorname{int}U_j\). Topology is arbitrary.
Coronas additionally require every new tile to touch the previous union;
closed point contact suffices.

**Imported premise:** after three strict surrounds, the complete ambient
neighbor family of a normalized root, including the root itself, is one of
fifteen necessary families \(C_i\), with
\[
 I_3=\{0,1,17,18,20,23,24,25,28,30,60,62,64,91,111\}.
\]
The exact poses are the author's
[h7922 classification](https://github.com/helgithorskarp/math_results/blob/main/heesch_trapezoid_prefix_rigidity/proof.md).
Each \(C_i\) is a physical disc surround with the root strictly interior;
every nonroot member touches the root. Trivial tile automorphism makes the
codes distinct. Arbitrary real motions precede this local classification.

Its full written proof and the quartic/contact, overlap, corner/old-point,
RUP and isotopy chain were read and audited. Its public computational chain
and inherited 147-copy four-corona witness were reproduced. This proof
imports the classification; it does not independently reimplement every
older finite corner, RUP or positive-network check.

## 2. Contact interiority and contact balls

If a compact set \(K\) lies in the interior of a finite subpacking union
\(\bigcup B\), every ambient tile meeting \(K\) already belongs to \(B\).
At a contact point a small ball lies in that union. The contacting Jordan
disc is the closure of its interior, so it has an open interior piece in the
ball. Finitely many nowhere dense tile boundaries cannot cover the piece.
It meets a \(B\)-tile interior; packing disjointness forces the same tile.
Point-only contacts are included.

For \(A\in F_j\), let \(G_r\) be its radius-\(r\) ball in the finite
contact graph of \(F_H\), and \(V_r=\bigcup G_r\). Inductively
\(G_r\subset F_{j+r}\) for \(r\le H-j\): every ambient tile meeting
\(G_{r-1}\subset F_{j+r-1}\) lies in \(F_{j+r}\) by the lemma.

Also \(V_{r-1}\subset\operatorname{int}V_r\). The former compact set is
strictly inside \(U_{j+r}\). Each of its finitely many noncontacting
\(F_{j+r}\) tiles has positive distance from it. A sufficiently small
neighborhood is therefore covered only by the contacting tiles, precisely
the next graph ball. If no noncontacting tile exists, positive distance to
the complement of \(\operatorname{int}U_{j+r}\) suffices. New ball tiles
touch the previous ball on its boundary: a distinct tile cannot meet the
interior of a finite packing union by the same lemma.

Thus \(A\) has \(H-j\) auxiliary coronas with arbitrary topology, even when
the original strict-surround chain imposed no contact condition. No disc
re-rooting, edge-only adjacency or final-layer grid assumption is made.

## 3. An independently derived physical overlap predicate

The physical boundary homotopy moves skeleton points by at most
\(\delta=1/1600\). Put \(z=(3,0)\) axially and
\[
 S'=\frac{999}{1000}S+\frac1{1000}z.
\]
The squared metric is \(q^2+qr+r^2\). For an axial edge vector \(e\)
and point \(v\) on its line, the squared distance of \(z\) is
\[
 \frac{3\det(e,z-v)^2}{4(e_q^2+e_qe_r+e_r^2)}.
\]
The minimum over the four sides is \(3/4\), so every edge distance exceeds
\(3/4\). Homothety puts every point of \(S'\) at distance at least
\[
 \frac3{4000}>\frac1{1600}
\]
inside every skeleton half-plane. The center stays interior throughout the
Jordan homotopy. The connected \(S'\), disjoint from every moving boundary,
therefore stays strictly inside \(T\). This holds under every isometry.

If two transformed closed \(S'\) intersect, their intersection point is
interior in both physical tiles, even for a point-only intersection.
For forced integer-D6 poses, multiply coordinates by 1000; all vertices
are integers. The separating-axis theorem tests closed intersection using
integer projections along all quadrilateral edge normals. The invertible
axial map preserves intersection, so no metric approximation is involved.

Two distinct tiles with the same positive unit chord have its midpoint
strictly interior in both outward-bowed physical tiles. This is another
sound conflict. Shared labelled endpoints are unchanged physical points,
hence sufficient contact witnesses. Absence of such a witness never claims
physical noncontact. Identical poses represent one copy and are allowed.

These predicates may retain extra models; they cannot remove an actual
packing. The older \(1/96\) clipping buffer is not a premise of this new
model-stage overlap predicate. Physical compatibility of arbitrary curved
pairs is not decided by it.

## 4. Full finite coverage and the upper bound

A complete neighborhood option about \(A\) is \(A C_i\). Given a known
family, reject only an omitted known contacting tile, an added root-contacting
tile absent from that family, or a sound physical conflict. Two options may
not conflict; a tile in one option known to touch the other's receiver must
appear in that receiver's complete option. Shared identical copies are allowed.

Actual packings provide surviving choices. Their union is exactly the second
contact ball: each distance-two tile touches a first-ball receiver, and every
tile in a receiver's complete neighborhood has distance at most two. The
same reasoning identifies the third ball. No surviving model is assumed to
be physically realizable.

The independent checker recomputes every domain from the literal pose data.
It visits all 1,270 first Cartesian products and retains 30 assignments:
\[
\begin{array}{c|rrrrrrrrrr}
 i&0&17&18&20&23&24&30&60&62&64\\
 \#&1&2&2&1&3&1&2&2&15&1.
\end{array}
\]
Call this complete relation \(\mathcal M\) and its ten root types \(I_4\).
Under five surrounds every first-ball receiver has four auxiliary surrounds.
Filtering its assigned types to \(I_4\) leaves 23 second states.

Every newly born second-ball receiver has three auxiliary surrounds, hence
a type in \(I_3\). The resulting frontier domains have 98,466 raw products
in total. The checker instead joins domains one receiver at a time, keeping
all compatible partial rows. By induction, a row survives precisely when
all constraints between its assigned receivers hold; every compatible
completion survives every prefix. This covers the complete product without
sampling. There are 1,907 retained partial rows and 43 full assignments.

Every original first assignment and every third whole-pose family equals
the author's published entry literally after JSON normalization. No distinct
assignments alias a family. Third-family counts are
\[
 (0:1,\ 17:1,\ 18:1,\ 23:2,\ 24:1,\ 30:1,\ 62:36).
\]
Thus \(I_5=\{0,17,18,23,24,30,62\}\) is necessary at depth five.

For any necessary \(I_m\), define
\[
 \Phi(I_m)=\{i\in I_m:\text{some }(i,v)\in\mathcal M
                    \text{ has all entries in }I_m\}.
\]
Each first-ball receiver under \(m+1\) surrounds has \(m\) auxiliary
surrounds, so \(\Phi(I_m)\) is necessary at depth \(m+1\). Exact evaluation
gives
\[
 \Phi(I_5)=\{17,62\},\qquad \Phi(\{17,62\})=\varnothing.
\]
Seven strict surrounds are impossible. The inherited actual four-corona
fixture gives \(4\le H_c(T)\le H_h(T)\le6\).

## 5. Seventeen necessary six-depth third families

Under six surrounds, root type is in \(I_6=\{17,62\}\). Every first-ball
receiver has five auxiliary surrounds, every other second-ball receiver
four. Filter each of the 43 complete third assignments by its first-ball
types lying in \(I_5\) and other second-ball types in \(I_4\).

Exactly 17 remain, with no assignment/family alias: one rooted at type17
and sixteen at type62. The complete pose families are
[SIX_DEPTH_CATALOG.json](SIX_DEPTH_CATALOG.json), sorted by root type and
lexicographic pose order. Its canonical SHA256 is
acfad8f61084d6c9898c063dc501113482617b7b190796662b1fcad5b35d1abc.
Twelve families have 37 cumulative copies, four have 40, one has 56.

This is necessary for the third contact ball of any real-motion six-surround
chain. If the original chain has no added-copy contact condition, unrelated
extra copies are not classified. For ordinary coronas, the ball equals the
entire cumulative third family: induction uses the new-copy contact condition
for one inclusion and contact interiority for the other.

These seventeen models are not six-corona constructions, and do not prove
\(H\ge6\) or \(H\le5\). Exact fifth/sixth existence remains unresolved.

## 6. Trust and opportunities

The final model geometry, complete census and six-depth filter are separately
written arbitrary-precision integer Python, with no campaign executable
imports. The three-surround classification and positive four-corona fixture
are explicit imported written and replayed prerequisites. Jordan topology
and contact-ball depth are ordinary mathematics, not proof-assistant code.

A sound extension or exclusion of the 17 candidates must retain three more
actual surrounds and all motions. Formalization should encode contact
interiority and depth loss first, then the imported local classification
and finite-join completeness. This bound and refinement concern this fixed
physical tile; they are not a height-record improvement.
