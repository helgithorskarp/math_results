# A connected dominating triple cannot force five colours

**Exact computer-assisted theorem.** Every Euclidean unit-distance graph with a connected dominating set of at most three vertices is four-colourable. The bound is sharp, already for a seven-vertex Moser spindle with a dominating unit path.

Here a unit-distance graph has distinct points of the plane as vertices, and every edge joins points at distance **exactly** one. We prove the upper bound for the full unit-distance graph on the support, so it also holds when some unit-distance edges are omitted. This is not a unit-disk graph statement. A set dominates when every vertex outside it has a neighbour in it; connected means that the subgraph on the set is connected.

More precisely, put
\[
 D_\beta=\{0,1,\beta\},\qquad |\beta|=1,\qquad
 Y_\beta=D_\beta\cup C(0,1)\cup C(1,1)\cup C(\beta,1),
\]
where \(C(d,1)=\{z:|z-d|=1\}\).
The full, infinite unit-distance graph on \(Y_\beta\) is four-colourable for **every** unit complex number \(\beta\). If \(\beta\ne1\), every assignment of three pairwise distinct colours from a four-colour palette to the ordered centres extends. We do not assert extension for prescriptions that give the outer centres equal colours.

This closes the entire unit-wedge neighbourhood family, with all opening angles and arbitrary subsets of the circles. It does **not** close arbitrary dominating triples: sets with at most one unit edge between their three distinct centres are outside this theorem. No five-chromatic graph on at most 508 vertices has been constructed here, and no priority claim is made.

## From three circles to thirty formal points

Let
\[
 \omega=(1+i\sqrt3)/2,\quad U=\{\omega^j:0\le j<6\},\quad
 S_\beta=U\cup\beta U,\quad P_\beta=D_\beta+S_\beta .
\]
The centres already belong to \(P_\beta\): \(0=1-1\), \(1=0+1\), and \(\beta=0+\beta\).
There are 30 distinct formal expressions \(s+t\beta\) in this set, with \(s,t\) Eisenstein integers. Specialization can identify expressions.

We first treat \(\beta\ne1\), so the three centres are distinct.

**Unit-centre-pair lemma.** Suppose \(|a-b|=1\), \(x\in C(a,1)\), \(y\in C(b,1)\), and \(|x-y|=1\). If \(x\ne b\) and \(y\ne a\), then \(y=x+b-a\), so \(x-a=y-b\).

Indeed, \(a\) and \(y\) are common points of the unit circles centred at \(b\) and \(x\). When \(x\ne b\), these circles have at most two intersections. Reflection about their midpoint interchanges the intersections, giving the second point \(b+x-a\). The tangent case leaves no distinct second point. Also, two points of a single unit circle are unit-separated exactly when their direction arguments differ by \(60^\circ\) or \(-60^\circ\).

All points belonging to more than one of the three circles lie in \(P_\beta\), and all their directions from their owner centres lie in \(S_\beta\):
- The intersections of \(C(0,1)\) and \(C(1,1)\) are \(\omega,\overline\omega\), with directions in \(U\) from both centres.
- The intersections of \(C(0,1)\) and \(C(\beta,1)\) are \(\beta\omega,\beta\overline\omega\), with directions in \(\beta U\).
- Since \(\beta\ne1\), the intersections of \(C(1,1)\) and \(C(\beta,1)\) are \(0\) and \(1+\beta\), possibly coincident when \(\beta=-1\). Their directions are among \(\pm1,\pm\beta\).

The same direction property holds for the centres whenever they lie on another circle. Consequently, every direction of every point of \(P_\beta\) from any circle that owns it lies in \(S_\beta\). This last statement also follows directly for a unique-owner point from the definition \(P_\beta=D_\beta+S_\beta\).

Every point outside \(P_\beta\) has a unique circle owner, with direction in a six-rotation orbit disjoint from \(S_\beta\). Since \(S_\beta\) is closed under multiplication by \(U\), same-circle unit edges never join \(P_\beta\setminus D_\beta\) to its complement.

We need only the following finite list-colouring condition on the full unit-distance graph of \(P_\beta\):
\[
 c(0)=2,\qquad c(1)=3,\qquad c(\beta)=0.
\]
For other patch vertices use these lists:

| Circle ownership of the vertex | Allowed colours |
| --- | --- |
| Only \(C(1,1)\) | \(\{0,1\}\) |
| Only \(C(\beta,1)\) | \(\{2,3\}\) |
| Any other ownership pattern | \(\{0,1,2,3\}\) |

The centres have priority over this table. The finite certificate below supplies a proper colouring from these lists for every \(\beta\ne1\).

## Why the finite colouring extends to the full circles

For each six-rotation orbit outside \(S_\beta\), choose its unique representative whose argument lies in \([0,\pi/3)\). Write a direction as \(\gamma\omega^j\), \(0\le j<6\), and put \(p=j\bmod2\). Use the **same direction convention on all three circles**. For the uniquely owned points outside the patch, set
\[
 c(\gamma\omega^j)=p,\qquad
 c(1+\gamma\omega^j)=1-p,\qquad
 c(\beta+\gamma\omega^j)=2+p.
\]

All same-circle edges change parity. Edges between the circles at 0 and 1 preserve direction by the unit-centre-pair lemma, and therefore get opposite colours. Edges involving the circle at \(\beta\) and a point on either other circle use disjoint palettes. In particular, we impose **no direction-preservation hypothesis on edges between the outer circles** at 1 and \(\beta\); their centre separation need not be one and their directions can belong to different orbits. Each owner spoke avoids its centre colour, respectively 2, 3, or 0.

It remains to check patch boundaries. A noncentre patch point on \(C(0,1)\) has every neighbour in \(P_\beta\): same-circle edges rotate a direction in \(S_\beta\), and edges to either other circle preserve that direction by the unit-centre-pair lemma. Exceptional centre endpoints are already in the patch. A multiple-owner patch point not on \(C(0,1)\) must be \(1+\beta\); its same-circle neighbours on both outer circles are in the patch, and its neighbours on \(C(0,1)\) are in the patch by the unit-centre-pair lemma applied to the centres 1 and 0. Thus these points have no boundary edges.

A patch vertex owned only by \(C(1,1)\) can have a neighbour outside the patch only on \(C(\beta,1)\). Its list \(\{0,1\}\) is disjoint from the latter circle's residual palette. A patch vertex owned only by \(C(\beta,1)\) can have an outside neighbour only on \(C(1,1)\), and its list \(\{2,3\}\) is disjoint from that residual palette. Finally, centre-to-outside edges are owner spokes: a point outside the patch cannot have two owners. These observations check every edge.

This proves the continuum extension conditional on the finite list certificate. Relabelling the four colours proves the stated extension for every pairwise-distinct centre prescription.

If \(\beta=1\), there are only two distinct centres at unit distance. The [dominating-clique theorem](../hadwiger_nelson_dominating_triangle/README.md), whose continuum argument has an [independent acceptance](../hadwiger_nelson_dominating_triangle_review1/README.md), gives three-colourability: add an auxiliary centre completing a unit triangle and restrict its full-circle colouring to the two original circles. Our finite census also checks the 10-point specialized patch with three colours, but does not use that finite row alone as a proof about the remaining circles.

## A finite, complete classification of all angles

For an Eisenstein integer \(a+b\omega\),
\[
 \overline{a+b\omega}=(a+b)-b\omega,\qquad
 N(a+b\omega)=a^2+ab+b^2.
\]
For a formal point difference \(s+t\beta\), set \(\overline s\,t=p+q\omega\). If \(\beta=x+iy\) and \(x^2+y^2=1\), then
\[
 |s+t\beta|^2-r=A x+B\sqrt3\,y+C,
\quad
 (A,B,C)=(2p+q,-q,N(s)+N(t)-r).
\]
Here \(r=0\) detects coincidences and \(r=1\) detects unit edges, including changes of circle ownership because all centres are formal patch points.

For each of the \(\binom{30}{2}=435\) formal pairs we check both targets, giving 870 cases. A nonzero constant cannot vanish; an identically zero polynomial describes a persistent relation. No two distinct formal expressions coincide identically. The nonconstant triples, divided by their common gcd and normalized in sign, give exactly **46 lines**
\[
 A x+B\sqrt3\,y+C=0 .
\]
Let \(L=A^2+3B^2>0\) and \(\Delta=L-C^2\). A line has zero, one, or two intersections with the unit circle according as \(\Delta<0\), \(=0\), or \(>0\). The exact census gives 24 disjoint lines, 6 tangent lines, and 16 secant lines. Their 38 intersection incidences comprise exactly **14 distinct parameters**.

There is a simple description of this exceptional set. Put
\[
 \rho=(5+i\sqrt{11})/6,\qquad \eta=(7+i\sqrt{15})/8 .
\]
Then the set is exactly
\[
 U\ \cup\
 \{\rho^\epsilon\omega^j:\epsilon\in\{-1,1\},\ j\in\{-1,0,1\}\}
 \ \cup\ \{\eta,\overline\eta\}.
\]
All fourteen values are distinct. The checker verifies both this description and the complete line-intersection census.

Outside this finite set, no distinct formal points merge, and only identically unit-separated pairs are edges. Hence **one generic 30-vertex, 72-edge graph with fixed lists covers the entire complement**. This includes transcendental parameters; no angular sampling, interval grid, or generic-position conjecture is used.

At exceptional parameters the checker merges exact coincident coordinates, reconstructs every unit edge and owner list, and checks a supplied positive colouring. The complete histogram is:

| Distinct patch vertices | Unit edges | Number of exceptional parameters |
| ---: | ---: | ---: |
| 10 | 19 | 1 |
| 12 | 24 | 2 |
| 13 | 26 | 3 |
| 30 | 74 | 6 |
| 30 | 76 | 2 |

The first row is the separately handled coincident-centre case \(\beta=1\). The 12-vertex cases are \(\omega^{\pm1}\); the 13-vertex cases are \(-1,\omega^{\pm2}\). The 76-edge cases are \(\rho^{\pm1}\); the other six non-root cases have 74 edges. All lists pass, with 3,891 exceptional pair-norm checks and 813 positive edge checks across the generic and exceptional patch graphs.

## Connected domination and sharpness

A connected graph on three vertices contains a path of length two. Normalize the middle vertex to 0 and one endpoint to 1; the other endpoint is some unit \(\beta\ne1\). Every vertex dominated by these three centres lies on one of the three circles, so restriction of the full-support colouring proves the corollary. A connected dominating set of size one or two is a clique, already covered by the cited three-colour theorem. Thus a five-chromatic Euclidean unit-distance graph cannot have a connected dominating set of at most three vertices.

For sharpness let \(R=0\), \(T=\sqrt3\), \(A=(\sqrt3+i)/2\), \(B=(\sqrt3-i)/2\), with \(\rho\) as above. Take
\[
 R,T,A,B,\rho T,\rho A,\rho B.
\]
The full unit graph is the Moser spindle, with the eleven edges of the two diamonds \(RTAB\) and \(R(\rho T)(\rho A)(\rho B)\), plus \(T(\rho T)\). In a three-colouring, each diamond forces its two nonadjacent tips to have the same colour; both \(T\) and \(\rho T\) would have the colour of \(R\), contradicting their edge. A proper four-colouring is \((0,1,2,3,0,2,3)\) in the displayed vertex order.

The path \(R,A,T\) dominates all seven vertices, and \(|R-T|^2=3\), so its opening angle at \(A\) is \(120^\circ\). The checker verifies all 21 pair distances, this dominating path, the four-colouring, and independently rejects every one of the \(3^7=2,187\) three-colour assignments. This supplies sharpness of the universal upper bound, not an exact chromatic-number classification for each parameter.

## Reproduce and audit

Requirements: Python 3.11 or later, standard library only. Tested with Python 3.11.2 on one thread. From this directory, with a fresh output directory:

~~~sh
sha256sum -c SHA256SUMS
python3 build.py --out work
python3 verify.py --work work
python3 -O verify.py --work work
~~~

The producer requires a new output directory. It deterministically regenerates the certificate and compares its bytes with the published file. The checker can also run without the producer after copying the published certificate into a fresh work directory.

- [build.py](build.py) derives the event lines by Eisenstein inner products, constructs their roots in exact sparse squarefree-radical arithmetic, specializes all patches, and finds positive list colourings by finite deterministic backtracking.
- [verify.py](verify.py) imports neither producer nor parent executable. It uses integer coefficients in the ordered basis
  \((1,\sqrt3,\sqrt5,\sqrt{15},\sqrt{11},\sqrt{33},\sqrt{55},\sqrt{165})\), multiplying by an XOR index rule with factors \(3,5,11\). These basis elements are linearly independent over the rationals. Published parameter and sharpness coordinates have denominator 24; evaluated patch coordinates have denominator 48.
- The checker derives the distance polynomials **by polarization**, evaluating squared distances exactly at \(\beta=1,-1,i\), instead of using the producer's inner-product formula.
- It does **not** regenerate parameters by the producer's quadratic-root formula. It verifies fourteen distinct unit points and, for each of the 46 complete event lines, counts exactly the required zero, one, or two supplied intersections. These 644 line/parameter tests certify completeness by elementary circle-line geometry. Every supplied point must occur on a line.
- It independently reconstructs all geometric graphs, ownership lists and centre pins, then checks every positive edge inequality. Six deliberately damaged certificates are rejected: omitted line, omitted parameter, nonunit parameter, corrupted generic list, invalid exceptional colouring, and invalid dominating path.
- Normal and optimized Python verification produce identical reports. Checks use explicit exceptions, not optimization-sensitive assertions. No native solver or external input is needed for the executable audit.

The [certificate](certificate.json) is **5,609 bytes**, SHA-256
52c3f952f5bb8fcd70b36ecd7acd9fc420d60fa583b394310a392a5ebe92c6a2.
[expected.json](expected.json) records the deterministic counts.
[validation.json](validation.json) records timings, provenance, scope and dependencies.
[SHA256SUMS](SHA256SUMS) covers the other seven public files.

This is an exact computer-assisted theorem with an explicit, unformalized continuum proof above. The integer-field arithmetic, the finite enumeration reduction, and the Python runtime remain trust boundaries. The independent checker is **author-run**, with structurally different equation and root-completeness checks; it is not external peer review or proof-assistant formalization. External review of this new theorem is pending. The accepted parent theorem supplies the coincident-centre case. There is no omitted large trace, unfinished certificate, or background computation.

## Campaign context and scope

The previous [full equilateral-triangle exterior support](../hadwiger_nelson_triangle_simultaneous_exterior/README.md) had chromatic number four. This result changes the centre geometry and simultaneously covers every opening angle, with no exterior points added to the three circles. It does not continue the retired fixed-gadget or centred-spindle assembly enumerations.

The [560-vertex Heule-support checkpoint](../hadwiger_nelson_heule632_minimize/README.md), now [independently accepted](../hadwiger_nelson_heule560_family_review1/README.md), proves five-chromaticity of that fixed support and gives 492 mandatory vertices, leaving a 68-vertex optional pool. The newer [free50 closure](../hadwiger_nelson_heule560_degree_family/README.md) supplies one four-colouring of a 542-vertex covering graph. Thus every remaining obstruction in that fixed seed must include one of 18 specified fresh vertices. It does not close the entire 560-vertex family, and the acceptance of its parent does not automatically review this newer closure. These artifacts are coordination context, not mathematical inputs to the present theorem; their support-certification lane was not rerun.

The record calibration remains 509 vertices in [Parts, arXiv:2010.12665](https://arxiv.org/abs/2010.12665), also named as the record in the introduction of [Haugland, arXiv:2608.04542v4](https://arxiv.org/html/2608.04542v4). Both primary pages were checked live on 2026-09-06. This contribution is a structural exclusion, not a record improvement.
