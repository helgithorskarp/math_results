# A 204-point colouring kernel for two paired unit-circle neighbourhoods

**General geometric lemma.** For four distinct planar centres paired into two unit edges, an explicitly defined patch of at most **204 actual points** has a sufficient four-list-colouring condition for the full infinite union of the four unit circles and their centres. For parallel unit segments the patch has at most **156 points**, and this cardinality bound is attained.

**Exact bounded application.** Put \(D_t=\{0,1,t,t+1\}\), where
\[
 t=(m+in)/2,\qquad m,n\in\mathbb Z,\quad -4\le m,n\le4.
\]
For all **81** translations, the full unit-distance graph on
\[
 X_t=D_t\cup\bigcup_{d\in D_t} C(d,1)
\]
is four-colourable. Twenty-two new symmetry representatives are certified here; the remaining coincident-centre and unit-rhombus cases use previously proved results. Every subgraph of these full supports is therefore four-colourable.

The originally proposed staircase \(D=\{0,1,1+i,2+i\}\) has a **38-point, 95-edge patch** with a checked extension colouring. No five-chromatic graph on at most 508 vertices is established.

The kernel condition is **sufficient, not necessary**. We do not claim that it succeeds for every placement of two unit segments, that every four-centre neighbourhood is four-colourable, or that failure of a prescribed list colouring gives a graph obstruction. The bound concerns actual geometric patch points, not an abstract graph, and is separate from the bounded half-grid application. No priority claim is made.

## 1. The general kernel

Let \(A=\{a_0,a_1\}\), \(B=\{b_0,b_1\}\), with all four centres distinct and
\[
 |a_1-a_0|=|b_1-b_0|=1.
\]
The two segments are vertex-disjoint; their interiors may intersect. No parallelism or other centre separation is assumed. Write \(C_d=C(d,1)\), and
\[
 \omega=(1+i\sqrt3)/2,\qquad U=\{\omega^j:0\le j<6\}.
\]
For each \(a\in A,b\in B\), let \(I_{ab}=C_a\cap C_b\), containing zero, one, or two points. Define the finite direction sets
\[
\begin{split}
 S_A&=U(a_1-a_0)\ \cup\
       \bigcup_{a\in A,b\in B,\ x\in I_{ab}}U(x-a),\\
 S_B&=U(b_1-b_0)\ \cup\
       \bigcup_{a\in A,b\in B,\ x\in I_{ab}}U(x-b),
\end{split}
\]
and the actual patch
\[
 P_A=(a_0+S_A)\cup(a_1+S_A),\quad
 P_B=(b_0+S_B)\cup(b_1+S_B),\quad P=P_A\cup P_B.
\]
All directions have modulus one. Every centre belongs to the patch because it is at unit distance from its partner.

A point's owners are the centres whose unit circles contain it. Every point with at least two owners lies in \(P\). If the owners belong to different groups this follows from the definition of \(I_{ab}\). If they belong to one group, they are the endpoints of a unit segment; their two circle intersections are equilateral completions, and all relative directions are in that segment direction's \(U\)-orbit.

For every noncentre patch point, its direction from **every** owner lies in that owner's direction set. For a unique-owner point this follows from the patch definition. For a multiple-owner point it follows from the preceding intersection descriptions, including any additional owner.

We use the unit-centre-pair lemma: if \(|a-b|=1\), \(x\in C_a\), \(y\in C_b\), \(|x-y|=1\), and \(x\ne b,y\ne a\), then
\[
 y=x+b-a,\qquad y-b=x-a.
\]
Indeed, \(a,y\) are the intersections of the circles centred at the distinct points \(b,x\); reflection through their midpoint gives the only possible second point \(b+x-a\). The tangent case has no distinct second point. On a single unit circle, a unit chord changes direction by multiplication by \(\omega\) or \(\omega^{-1}\).

Consequently, a noncentre patch point has no outside neighbour on either circle in any group containing one of its owners. Same-circle neighbours stay in the direction orbit; neighbours on its owner's partner circle preserve direction by the lemma. The excluded centre endpoints are in the patch. Thus:
- a patch point owned only by group \(A\) can meet the outside only on group \(B\);
- one owned only by \(B\) can meet the outside only on \(A\);
- a mixed-owner noncentre point has **no** outside neighbour.

These statements also hold when a point has both owners of one group. Such points need their group's palette in the next condition, unlike the unrestricted multiple-owner points in the earlier rhombus proof.

## 2. The sufficient colouring condition

Use colours \(0,1,2,3\), and pin
\[
 (c(a_0),c(a_1),c(b_0),c(b_1))=(2,3,0,1).
\]
For every noncentre patch point use:

| Ownership groups | Allowed colours |
| --- | --- |
| Only \(A\), including two owners in \(A\) | \(\{0,1\}\) |
| Only \(B\), including two owners in \(B\) | \(\{2,3\}\) |
| Both \(A\) and \(B\) | \(\{0,1,2,3\}\) |

The centre pins take priority. Suppose the full unit-distance graph on \(P\) has a proper colouring from these lists.

Every point outside \(P\) has a unique owner. Its direction from a group-\(A\) owner belongs to a six-rotation orbit disjoint from \(S_A\), and similarly for \(B\). For any direction orbit choose its unique representative \(\gamma\) with argument in \([0,\pi/3)\). Write the direction as \(\gamma\omega^j\) and let \(p=j\bmod2\). Use the same convention on the two circles of each pair, and set
\[
\begin{array}{c|cccc}
\text{owner}&a_0&a_1&b_0&b_1\\ \hline
\text{residual colour}&p&1-p&2+p&3-p.
\end{array}
\]

Same-circle edges flip parity. Edges between the two circles in either unit pair preserve actual direction and receive opposite colours. Edges between the groups use disjoint palettes, with **no direction-preservation assumption**. The owner spokes avoid the respective centre colours \(2,3,0,1\).

The boundary classification above completes the proof: a single-group patch point has a list disjoint from the residual palette of every possible outside neighbour, and mixed-owner noncentres have no outside neighbours. A centre-to-outside edge is an owner spoke because the outside point has only one owner. This checks every edge of the full infinite support.

A global palette permutation gives the same extension statement for any four pairwise-distinct prescribed centre colours. Equal-colour centre prescriptions and necessity of the list condition are not asserted.

## 3. The 204-point bound

Let
\[
 I=\bigcup_{a\in A,b\in B} I_{ab},\qquad k=|I|\le8.
\]
The cross-intersection direction orbits seen from \(A\) and from \(B\) form the **same** set of orbits. For a fixed cross pair with intersections \(x,y\),
\[
 x+y=a+b,\qquad y-a=-(x-b),\quad y-b=-(x-a).
\]
Negation belongs to \(U\); the tangent case has \(x=y\), and the empty case contributes nothing. Thus the two sides generate the same orbit set. Let its number of distinct orbits be \(r\).

Each fixed point \(x\in I\) contributes at most one orbit on the \(A\) side. If both \(a_0,a_1\) own it, the two unit directions \(x-a_0,x-a_1\) differ by a unit chord and hence by \(\omega^{\pm1}\). Therefore \(r\le k\le8\). Each group adds at most one intrinsic segment-direction orbit, so
\[
 |S_A|,|S_B|\le6(r+1).
\]

The two equilateral intersections of the paired circles in \(A\) occur in both translates defining \(P_A\). They are distinct, giving
\[
 |P_A|\le12(r+1)-2,
\]
and the same holds for \(P_B\). Their intersection contains all \(k\) points of \(I\). Hence
\[
 |P|\le24(r+1)-4-k
       =20+24r-k
       \le20+23r
       \le\boxed{204}.
\]
This counts distinct points after all coincidences. It does not assume general position or exclude tangent cross circles.

The patch itself is an actual unit-distance graph of target-relevant size. A future unrestricted four-colour obstruction on it would be materially different from failure of the fixed lists; the present work supplies no such obstruction.

## 4. The sharp 156-point parallel bound

Normalize parallel segments to \(A=\{0,1\}\), \(B=\{t,t+1\}\), with \(t\notin\{0,1,-1\}\). There are only three cross-displacement types:
\[
 t\quad\text{(twice)},\qquad t+1,\qquad t-1 .
\]
Each type contributes at most two direction orbits. The intrinsic segment direction is the same for both groups, so \(S_A=S_B\), and \(r\le6\).

If \(r\le5\), each group has at most 36 directions. After its two intrinsic duplicates, the whole patch has at most \(2(72-2)=140\) points.

If \(r=6\), all three types have two intersections with six pairwise distinct direction orbits. There are then eight cross-intersection incidences, counting the repeated displacement \(t\). They correspond to **eight distinct actual points**. To see this, a point repeated across different displacement types would give the same \(A\)-direction orbit: if its \(A\) owner is the same, the directions are equal; if it has both \(A\) owners, the directions differ by \(\omega^{\pm1}\). Either contradicts the six distinct type/root orbits. A point repeated across the two pairs of type \(t\) either equates the two different root orbits or uses the same root direction at centres 0 and 1, which would require \(x=x+1\). Both are impossible.

Thus \(k=8\) in this case. With at most 42 directions per group,
\[
 |P|\le4\cdot42-4-8=\boxed{156}.
\]
The certified translation \(t=i/2\) produces exactly 156 distinct patch points, so this cardinality bound for the defined parallel kernel is attained. This sharpness is about the **size of the kernel**, not a lower bound of four on the chromatic number.

## 5. The complete frozen half-grid application

The maps \(z\mapsto\bar z\) and \(z\mapsto1-\bar z\), with relabelling within the centre pairs, change the signs of the imaginary and real parts of \(t\). Thus the 81 translations in \(-4\le m,n\le4\) reduce to the 25 representatives \(0\le m,n\le4\).

Three representative classes are inherited rather than re-enumerated:
- \((m,n)=(0,0)\) has two distinct centres;
- \((2,0)\) has three centres in a unit path;
- \((0,2)\) is a unit square.

The first two classes account for three signed translations and use the [connected dominating triple theorem](../hadwiger_nelson_dominating_unit_path/README.md), which has [independent acceptance](../hadwiger_nelson_dominating_unit_path_review1/README.md). The square class accounts for two signed translations and uses the [unit-rhombus theorem](../hadwiger_nelson_dominating_unit_cycle/README.md). The remaining 22 representatives account for 76 signed translations and are all positively certified here.

| \(m,n\) | Patch vertices | Unit edges | Direction orbits |
| --- | ---: | ---: | ---: |
| 0,1 | 156 | 428 | 7 |
| 0,3 | 156 | 420 | 7 |
| 0,4 | 42 | 101 | 2 |
| 1,0 | 108 | 306 | 5 |
| 1,1 | 156 | 426 | 7 |
| 1,2 | 156 | 420 | 7 |
| 1,3 | 110 | 292 | 5 |
| 1,4 | 20 | 38 | 1 |
| 2,1 | 110 | 294 | 5 |
| 2,2 | 38 | 95 | 2 |
| 2,3 | 110 | 292 | 5 |
| 2,4 | 43 | 102 | 2 |
| 3,0 | 110 | 298 | 5 |
| 3,1 | 110 | 292 | 5 |
| 3,2 | 110 | 292 | 5 |
| 3,3 | 66 | 166 | 3 |
| 3,4 | 20 | 38 | 1 |
| 4,0 | 16 | 33 | 1 |
| 4,1 | 66 | 166 | 3 |
| 4,2 | 42 | 102 | 2 |
| 4,3 | 66 | 166 | 3 |
| 4,4 | 20 | 38 | 1 |

The finite audit reconstructs all **100,561** patch point pairs and checks **4,805** unit-edge inequalities. All 88 cross-circle pairs are classified: 37 have no intersection, 5 are tangent, and 46 have two intersections. All **97 supplied intersection points** are checked on both circles. Another 1,924 owner-direction checks include 93 mixed-owner noncentre instances. The signed symmetry quotient is checked over all 81 translations.

The staircase is the \((2,2)\) row. Its 38-point kernel has point-stream SHA-256
a6dc3dd6c47da0fd6dcd749094028f860e8917c48cc58db67af0cdf30fcf0ed9
and edge-stream SHA-256
e56e220c2fab7815d989486324740dfa54060a087d9a097a322fdabebf2854d3.
Its proper list colouring proves four-colourability of all four complete circles. No exact chromatic-number claim is made for that support.

## 6. Reproduction and independent verification

Requirements: Python 3.11 or later, standard library only. Tested on Python 3.11.2, one thread. From this directory with a fresh output directory:

~~~sh
sha256sum -c SHA256SUMS
python3 build.py --out work
python3 verify.py --work work
python3 -O verify.py --work work
~~~

The producer requires a new output directory. It reproduces the published certificate bytes. Verification may also start by copying the published certificate into a fresh work directory; it does not need a producer run.

[build.py](build.py) computes circle intersections with the exact formula
\[
 x=\frac{a+b}{2}\ \pm\
 i(b-a)\sqrt{\frac{4-q}{4q}},\qquad q=|b-a|^2,
\]
using rational-centre input and sparse squarefree-radical arithmetic. It rotates directions, builds the actual patch and unit graph, and finds positive list colourings by deterministic finite backtracking. If a list problem were unresolved or failed, the producer would stop without asserting full-support four-colourability.

[verify.py](verify.py) imports no producer or parent executable and **does not use this square-root formula**. For each of the four cross pairs, it computes the exact rational centre separation, requires precisely zero, one, or two distinct supplied intersections, and checks both unit distances. Elementary circle geometry makes this a complete intersection certificate. It independently reconstructs every orbit and actual patch point, compares complete canonical point and edge streams by SHA-256, derives every owner list and centre pin, and checks each colour and edge directly.

The checker uses integer coefficients in the 32-dimensional field
\(\mathbb Q(\sqrt3,\sqrt5,\sqrt7,\sqrt{11},\sqrt{13})\), in the squarefree basis indexed by subsets of these five primes. Multiplication uses an XOR coefficient rule, distinct from the producer's sparse-radicand gcd arithmetic. A per-case common integer scale is computed from the rational coordinate coefficients and includes the factor two needed for sixth-root rotations. All divisibility conditions are checked exactly. The field basis is linearly independent over the rationals.

The compact certificate stores cross-intersection coordinates, positive colour strings, list masks, graph sizes and hashes. It does not store a large raw edge dump. Its rational-coordinate encoding is specified in the file. Six damaged certificates are rejected: omitted case, missing intersection, invalid intersection coordinate, false point hash, monochromatic colouring, and corrupted lists. Normal and optimized verification produce identical reports. Checks use explicit exceptions, not optimization-sensitive assertions.

The [certificate](certificate.json) is **13,964 bytes**, SHA-256
4fca8a7d9f160397566d82d92bbb2e9435f7caa572e677a20b8e712fe3283fe7.
[expected.json](expected.json) contains all per-case counts and canonical hashes.
[validation.json](validation.json) records timings, provenance and scope.
[SHA256SUMS](SHA256SUMS) covers the other seven public files.

The general kernel and size bounds have explicit written proofs above; they are not finite-grid inferences. The bounded application is an exact computer-assisted result. The arithmetic basis, Python runtime, finite reductions, SHA-256 and the unformalized continuum bridge remain trust boundaries. The checker is author-run and algorithmically independent of the producer, not external peer review. External review of this new contribution is pending. The five inherited signed placements additionally depend on the cited earlier theorems. There is no native solver, omitted large proof, unfinished certificate or background job.

## 7. Campaign scope

This changes the centre-incidence mechanism beyond the closed unit-rhombus family. The general finite kernel works as a sufficient certificate for arbitrary orientations and translations of two paired unit segments; **only the frozen half-grid family is decided here**. No larger translation box, denominator or nonparallel orientation was searched, and no failure of a list prescription was treated as non-four-colourability.

The latest inspected teammate result is the [complete one-pair Kempe interface](../hadwiger_nelson_heule560_kempe/README.md), which closes 95.9068% of its fixed seed's labelled 508-point family. Its nine minimal failures concern 118 specified mandatory-set colourings, not arbitrary graph colourings. The preceding fixed-colouring interface now has [independent acceptance](../hadwiger_nelson_heule560_interface_review1/README.md), which does not automatically review the newer Kempe result. That support-certification lane was not rerun.

The primary-source record calibration remains 509 vertices in [Parts, arXiv:2010.12665](https://arxiv.org/abs/2010.12665), also named as the record in [Haugland, arXiv:2608.04542v4](https://arxiv.org/html/2608.04542v4), both checked live on 2026-09-06. This is a reusable construction certificate and a bounded negative result, not a record improvement.
