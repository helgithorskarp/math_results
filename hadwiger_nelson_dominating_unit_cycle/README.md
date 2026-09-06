# A dominating unit four-cycle cannot force five colours

**Exact computer-assisted theorem.** Every Euclidean unit-distance graph with a dominating four-cycle is four-colourable. The bound is sharp.

A dominating four-cycle means four distinct graph vertices with cyclic unit edges whose vertex set dominates the whole graph. The cycle need not be induced. A unit-distance graph has distinct points of the plane as vertices, and each edge has Euclidean length **exactly** one; extra unit-distance pairs may be omitted. This is not a unit-disk graph statement.

The geometric theorem is stronger. For every \(|\beta|=1\), let
\[
 D_\beta=\{0,1,\beta,1+\beta\},\qquad
 Y_\beta=D_\beta\cup\bigcup_{d\in D_\beta} C(d,1),
 \quad C(d,1)=\{z:|z-d|=1\}.
\]
The full unit-distance graph on this infinite support is four-colourable. When \(\beta\ne\pm1\), every assignment of four pairwise distinct colours to the ordered centres \(0,1,\beta,1+\beta\) extends. We do not claim extension of all proper prescriptions allowing equal centre colours.

This covers the entire unit-rhombus family, including the unit square \(\beta=i\), every opening angle, and every finite or infinite subsupport. It does not exclude all connected dominating sets of size four, arbitrary four-centre sets, or points outside these four circles. No five-chromatic graph on at most 508 vertices or record improvement is established, and no priority claim is made.

## The finite patch and its boundary

Write
\[
 \omega=(1+i\sqrt3)/2,\quad U=\{\omega^j:0\le j<6\},
 \quad S_\beta=U\cup\beta U,\quad P_\beta=D_\beta+S_\beta.
\]
This patch consists of **36 formal expressions** \(s+t\beta\), with Eisenstein integers \(s,t\). Specialization may identify them. All centres already lie in it: use \(0=1-1\), \(1=0+1\), \(\beta=0+\beta\), and \(1+\beta=1+\beta\) with the latter \(\beta\) a direction.

Assume first \(\beta\ne\pm1\), so the four centres are distinct. We call the centre pairs
\[
 \{0,1\},\quad\{0,\beta\},\quad\{1,1+\beta\},\quad
 \{\beta,1+\beta\}
\]
the **side pairs**, and the remaining pairs the diagonals. Every side separation is one. A diagonal may also have length one at special angles.

We use two elementary facts. On one unit circle, unit chords change direction by \(\pm60^\circ\). For unit-separated centres \(a,b\), if
\[
 x\in C(a,1),\quad y\in C(b,1),\quad |x-y|=1,
 \quad x\ne b,\quad y\ne a,
\]
then \(y=x+b-a\), and hence \(x-a=y-b\). To prove the latter statement, the circles centred at the distinct points \(b,x\) have \(a,y\) as intersections. Reflection through their midpoint sends \(a\) to \(b+x-a\), the only other possible intersection. A tangent pair has no distinct second intersection. This unit-centre-pair lemma is also used in the [preceding three-centre theorem](../hadwiger_nelson_dominating_unit_path/README.md).

All points with more than one circle owner are in \(P_\beta\). For a side pair, the two intersections are equilateral completions and their directions from both owners lie in \(U\) or \(\beta U\). For the diagonal pairs,
\[
 C(0,1)\cap C(1+\beta,1)=\{1,\beta\},\qquad
 C(1,1)\cap C(\beta,1)=\{0,1+\beta\}.
\]
Both displayed pairs contain two distinct points, so these are the complete intersections. In particular, a **noncentre** point with multiple owners must have a side pair among its owners.

For every noncentre point of \(P_\beta\), every direction from every owner lies in \(S_\beta\). A unique-owner point has this property by the definition of the patch; a multiple-owner noncentre point has it by the equilateral intersection description. Since \(S_\beta\) is closed under multiplication by \(U\), a same-circle unit edge from a noncentre patch point remains in the patch.

There are only two types of remaining boundary behaviour.

1. A multiple-owner noncentre patch point has no neighbour outside \(P_\beta\). Choose a side pair among its owners. Every other centre is a side neighbour of at least one of those owners. The unit-centre-pair lemma therefore puts every neighbour on either remaining circle back in the patch; neighbours on owner circles were already handled. Exceptional centre endpoints are in \(D_\beta\subset P_\beta\).
2. A unique-owner patch point can have an outside neighbour only on the circle at the diagonally opposite centre. Side contacts preserve a direction in \(S_\beta\); the unique unhandled centre is its opposite.

The two colour palettes below put each diagonal pair in different palettes. No direction-preservation assumption is made for arbitrary diagonal-circle contacts.

## The finite list condition and continuum colouring

Pin
\[
 (c(0),c(1),c(\beta),c(1+\beta))=(2,3,0,1).
\]
For other patch vertices, impose the following lists.

| Ownership | Allowed colours |
| --- | --- |
| A unique owner at 0 or 1 | \(\{0,1\}\) |
| A unique owner at \(\beta\) or \(1+\beta\) | \(\{2,3\}\) |
| More than one owner | \(\{0,1,2,3\}\) |

The centres have priority over the table. The certificate supplies a proper list colouring for every \(\beta\ne\pm1\).

Every point outside \(P_\beta\) has a unique owner and its direction belongs to a six-rotation orbit disjoint from \(S_\beta\). Choose each orbit's unique representative \(\gamma\) with argument in \([0,\pi/3)\). If a direction is \(\gamma\omega^j\), set \(p=j\bmod2\), using the same representative and parity convention for all four circles. Colour the residual points by
\[
\begin{array}{c|cccc}
\text{point}&\gamma\omega^j&1+\gamma\omega^j&
 \beta+\gamma\omega^j&1+\beta+\gamma\omega^j\\ \hline
c&p&1-p&2+p&3-p.
\end{array}
\]

Every same-circle unit edge changes parity. A unit edge between the circles at 0 and 1, or between those at \(\beta\) and \(1+\beta\), preserves direction and gets opposite colours. All other pairs of circles use disjoint palettes, so all their residual contacts are proper, including contacts joining different direction orbits. Owner spokes avoid the centre colours \(2,3,0,1\).

For the boundary, multiple-owner noncentre patch points have no outside neighbours. A unique-owner point uses its owner's palette and can meet an outside point only on the opposite diagonal circle, with the other palette. A centre-to-outside edge is an owner spoke, since a point outside the patch has a unique owner. This checks every edge of the full infinite graph.

Thus the finite list certificate proves the continuum upper bound. Any four distinct centre prescriptions follow by a global permutation of the four colours.

When \(\beta=1\), the distinct centres are \(0,1,2\); when \(\beta=-1\), they are \(-1,0,1\). These are unit paths and their full-circle supports are four-colourable by the [connected dominating triple theorem](../hadwiger_nelson_dominating_unit_path/README.md). The present census checks their specialized 13-point patches with four colours, but those finite rows alone are not used as continuum proofs. These two degenerate cases are the only mathematical dependency on the preceding theorem, which now has an [independent acceptance](../hadwiger_nelson_dominating_unit_path_review1/README.md); the nondegenerate boundary argument is written in full above.

## A complete exact census of all opening angles

An Eisenstein integer \(a+b\omega\) has norm \(a^2+ab+b^2\). For a formal difference \(s+t\beta\), let \(\overline s\,t=p+q\omega\). On \(\beta=x+iy\) with \(x^2+y^2=1\),
\[
 |s+t\beta|^2-r=A x+B\sqrt3\,y+C,\qquad
 (A,B,C)=(2p+q,-q,N(s)+N(t)-r).
\]
The target \(r=0\) detects vertex identifications; \(r=1\) detects edges and circle ownership changes because every centre is a formal patch point.

There are \(2\binom{36}{2}=\mathbf{1,260}\) formal pair/target cases. Nonzero constants do not vanish, and zero polynomials describe persistent relations. Distinct formal expressions cannot coincide identically. After gcd and sign normalization the nonconstant polynomials give **62 distinct lines**
\[
 A x+B\sqrt3\,y+C=0.
\]
For \(L=A^2+3B^2>0\), the discriminant \(\Delta=L-C^2\) determines the number of unit-circle intersections: zero for \(\Delta<0\), one for zero, and two for positive \(\Delta\). There are 36 disjoint, 6 tangent and 20 secant lines. Their **46 root incidences** give **22 distinct unit parameters**.

Put
\[
 \rho=(5+i\sqrt{11})/6,\qquad \eta=(7+i\sqrt{15})/8.
\]
The complete exceptional set is exactly
\[
 U\ \cup\ \rho U\ \cup\ \overline\rho U\
 \cup\ \{\eta,-\eta,\overline\eta,-\overline\eta\}.
\]
All 22 parameters are distinct. The checker verifies this description and every line-intersection count independently.

Outside this set, the 36 formal points remain distinct and only identically unit-separated pairs are edges. Hence a single generic graph with **36 vertices and 92 edges**, with fixed lists, covers every other angle, including transcendental parameters. No angle sampling or approximation is used.

The exceptional graphs are completely reconstructed by exact specialization:

| Patch vertices | Unit edges | Number of parameters |
| ---: | ---: | ---: |
| 13 | 26 | 2 |
| 14 | 29 | 4 |
| 36 | 94 | 12 |
| 36 | 96 | 4 |

The 13-point cases are \(\beta=\pm1\), the 14-point cases are the four nonreal sixth roots in \(U\), and the 96-edge cases are \(\pm\rho,\pm\overline\rho\). All other non-root cases have 94 edges. Every generic and exceptional colouring passes, with 10,600 exceptional pair-norm checks and 1,772 patch edge checks. At the nondegenerate exceptional parameters, the checker additionally verifies 696 owner-direction incidences and 144 multiple-owner noncentre instances supporting the boundary classification.

The proposed unit square \(\beta=i\) is explicitly checked as a generic specialization: 36 distinct patch points, 630 pair norms, the same 92 edges and owner lists, and the generic positive colouring. This does not claim that the square's chromatic number is exactly four.

## Dominating four-cycles and sharpness

Take any four distinct points \(a,b,c,d\) in a unit four-cycle. Apply a Euclidean isometry to put \(a=0\), \(b=1\), and \(d=\beta\) with \(|\beta|=1\). The points \(a,c\) are the intersections of the unit circles centred at \(1,\beta\), so \(c=1+\beta\). Distinctness excludes \(\beta=\pm1\). Thus **every Euclidean realization of a four-cycle is one of these nondegenerate unit rhombi**, regardless of any additional diagonal edge.

If the cycle dominates the graph, every other vertex lies on one of its four unit circles. The full-support colouring restricts to the graph, proving the corollary. In particular, any five-chromatic Euclidean unit-distance graph must have no dominating four-cycle.

For sharpness, set
\[
 R=0,\quad T=\sqrt3,\quad
 A=(\sqrt3+i)/2,\quad B=(\sqrt3-i)/2,
\]
and use the seven points
\[
 R,T,A,B,\rho T,\rho A,\rho B.
\]
Their full unit graph is the Moser spindle. Its eleven edges form the two diamonds \(RTAB\) and \(R(\rho T)(\rho A)(\rho B)\), plus \(T(\rho T)\). In any three-colouring, the two nonadjacent tips of a diamond have the same colour; both \(T\) and \(\rho T\) would therefore have the colour of \(R\), contradicting their edge. A four-colouring in the displayed order is \((0,1,2,3,0,2,3)\).

The unit cycle \(R,A,T,B,R\) dominates these seven vertices. Its diagonals bisect, \(R+T=A+B\), and \(|R-T|^2=3\), so normalization at \(A\) gives an opening of \(120^\circ\). The checker verifies every one of the 21 point pairs, the complete eleven-edge graph, the dominating four-cycle, the positive four-colouring, and all \(3^7=2,187\) assignments to exclude three colours. This proves sharpness of the universal bound. It is a small known lower-bound control, not a return to the retired spindle assembly search.

## Reproduction and trust boundary

Requirements: Python 3.11 or later, standard library only. Tested with Python 3.11.2 on one thread. From this directory, using a fresh output directory:

~~~sh
sha256sum -c SHA256SUMS
python3 build.py --out work
python3 verify.py --work work
python3 -O verify.py --work work
~~~

The producer requires a new directory and compares the regenerated certificate bytes with the published file. For verification without production, copy the public certificate into a fresh work directory and run the checker.

[build.py](build.py) uses Eisenstein inner products to obtain affine equations, sparse exact squarefree-radical arithmetic to construct all roots, and deterministic finite backtracking for positive list colourings.

[verify.py](verify.py) imports neither the producer nor any parent executable. It uses integer multiplication in the ordered basis
\[
 (1,\sqrt3,\sqrt5,\sqrt{15},\sqrt{11},\sqrt{33},\sqrt{55},\sqrt{165})
\]
with an XOR coefficient rule. Coordinates have denominator 24 and specialized formal patch coordinates have denominator 48. The eight basis elements are linearly independent over the rationals.

The checker derives every distance polynomial by **polarization at \(\beta=1,-1,i\)**, instead of the producer's Eisenstein inner-product formula. It does not regenerate roots by the producer's quadratic formula. It checks 22 distinct unit parameters and, for each of the complete 62 lines, exactly the required zero, one, or two supplied intersections. These **1,364 circle-line parameter tests** certify completeness using the elementary circle-line count. Every supplied parameter must occur on a line. It also checks the displayed closed-form exceptional set, exact coordinate identifications, every owner list, centre pins and every edge inequality.

Six damaged certificates are rejected: missing equation, missing parameter, nonunit parameter, corrupted generic list, invalid exceptional colouring, and invalid dominating cycle. Normal and optimized verification give identical reports; checks use explicit exceptions rather than optimization-sensitive assertions.

The producer and checker extend their respective implementations from the preceding unit-path package. Their independence here is between two arithmetic representations, two equation derivations and two root-completeness mechanisms; they are author-run, not independent-author peer review.

The [certificate](certificate.json) is **9,449 bytes**, SHA-256
ec3397d2f0958e374ff07b8768302c0c9cc9727f99164bff94e5c48ef7f3714f.
[expected.json](expected.json) gives deterministic results.
[validation.json](validation.json) records timings, dependencies and scope.
[SHA256SUMS](SHA256SUMS) covers the other seven public files.

This is an exact computer-assisted theorem with an explicit unformalized continuum argument. Exact field arithmetic, the finite-enumeration reduction, JSON, SHA-256 and the Python runtime remain trust boundaries. The two degenerate continuum cases use the prior unit-path theorem; no external data or executable is needed for this finite audit. External review of this new result is pending. There is no native solver, omitted large proof, unfinished certificate, or background computation.

## Campaign context

This changes the number and incidence pattern of the centres after the [universal connected-three-centre closure](../hadwiger_nelson_dominating_unit_path/README.md). It closes a complete transferable four-centre family at once. Its full-support upper bound generalizes the previous three-circle upper bound by adding the fourth centre and circle; the degenerate cases still use the preceding theorem. It does not decide connected four-centre configurations without a spanning unit cycle, and no fifth centre or new exterior support has been started.

The latest inspected teammate result is the [complete fixed-colouring interface](../hadwiger_nelson_heule560_interface/README.md), which closes about 85.7191% of the fixed 560-seed's labelled 508-point family. Every residual obstruction must contain one of three specified pairs, but failure to extend that fixed colouring does not prove graph non-four-colourability. Its [560-point parent and 492/68 reduction are independently accepted](../hadwiger_nelson_heule560_family_review1/README.md); that acceptance does not automatically review this newer interface. These are coordination context only; that support-certification lane was not rerun.

The record calibration remains 509 vertices in [Parts, arXiv:2010.12665](https://arxiv.org/abs/2010.12665), also named as the record in [Haugland, arXiv:2608.04542v4](https://arxiv.org/html/2608.04542v4), both checked live on 2026-09-06. This structural exclusion does not improve that record.
