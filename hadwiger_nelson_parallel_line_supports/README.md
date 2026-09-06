# Full-support colour bounds for parallel-line constructions

**Full-support theorem.** For every real spacing \(d\ge1/3\), the unit-distance
graph on
\[
 X_d=\{(x,jd):x\in\mathbb R,\ j\in\mathbb Z\}
\]
is four-colourable. This includes all points of infinitely many complete
parallel lines, with no bound on horizontal extent or number of occupied
lines. Consequently **every finite subgraph** of every such support is
four-colourable and cannot improve the five-chromatic unit-distance record.

A second full-support theorem covers **any three complete parallel lines**,
with arbitrary separations: their unit-distance graph is four-colourable.
More generally, every finite unit-distance graph on \(k\) parallel lines is
\(k\)-degenerate and hence \((k+1)\)-colourable.

The equally spaced support has the following more precise classification.

| Spacing | Conclusion for the entire \(X_d\) |
| --- | --- |
| \(d=1/3\) | \(\chi(X_d)=2\) |
| \(1/3<d<1/2\) | \(\chi(X_d)\le4\); exact value not asserted |
| \(d=1/2\) | \(\chi(X_d)=3\) |
| \(1/2<d<1\) | \(\chi(X_d)=3\) exactly when \(\sqrt{1-d^2}=p/q\) in lowest terms has even \(q\); otherwise \(\chi(X_d)=2\) |
| \(d\ge1\) | \(\chi(X_d)=2\) |

These are written mathematical theorems using classical greedy colouring,
finite graph compactness, and explicit coordinate colourings. The programs
supply exact finite audits and odd-cycle witnesses; their finite fixtures
are not an enumeration of the universal parameter families. No new priority,
sharp threshold at \(1/3\), or five-chromatic graph is claimed. The named HN
objective remains a graph on at most 508 vertices, compared with the
509-vertex graph in [Parts's primary paper](https://arxiv.org/abs/2010.12665).
[Haugland's August 2026 primary paper](https://arxiv.org/html/2608.04542v4)
also identifies 509 as the current record; checked on 6 September 2026.

## 1. Directional degeneracy for finitely many parallel lines

After a rigid motion, the supporting lines are horizontal. Order any finite
set of actual vertices lexicographically by \((x,y)\), first increasing in
\(x\), then increasing in \(y\). For a vertex \(v=(x,y)\), consider one
supporting line at height \(h\). Its unit neighbours satisfy
\[
 (x'-x)^2=1-(h-y)^2.
\]
If \(|h-y|<1\), there are at most two such points, one strictly left of \(v\)
and one strictly right. At most the left one occurs earlier. If \(|h-y|=1\),
there is one point with the same \(x\); the \(y\)-tie rule puts it on one side
of the ordering. If \(|h-y|>1\), there is none. This includes the vertex's
own line, where the neighbours have \(x'=x\pm1\).

Thus there is at most one earlier neighbour per supporting line, hence at
most \(k\) in total. Greedy colouring in this order uses at most \(k+1\)
colours. The ordering also restricts to every subset, proving degeneracy.
Vertical unit edges are included rather than collapsed by a projection.

The [de Bruijn--Erdős compactness theorem](https://users.renyi.hu/~p_erdos/1951-01.pdf)
then gives the same colour bound on the entire union of the lines, because
every finite subgraph has this bound. In particular, no unit-distance graph
on any three parallel lines is five-chromatic. The claim concerns abstract
proper colourings; it imposes no measurability requirement. Compactness and
ordinary choice are explicit set-theoretic premises of the infinite statements.

## 2. Horizontal projection of the infinite line family

For a finite set \(D\subset\mathbb R_{>0}\), let \(G(\mathbb R,D)\) have an
edge when the absolute difference of its two real vertices belongs to \(D\).
In any finite subgraph, a vertex has at most one earlier neighbour at each
prescribed positive distance. Increasing order therefore gives
\[
 \chi(G(\mathbb R,D))\le |D|+1, \tag{1}
\]
again using compactness for the infinite graph. This is the classical
finite-distance greedy bound, not a new graph-colouring principle.

For a unit edge in \(X_d\), let \(k\) be its absolute row difference.
Its absolute horizontal difference is
\[
 \delta_k=\sqrt{1-k^2d^2},\qquad k\ge0,\ kd\le1. \tag{2}
\]
If none of these differences is zero, projection to the \(x\)-coordinate is
a graph homomorphism into \(G(\mathbb R,D_d)\), where
\[
 D_d=\{\delta_k:k\ge0,\ kd<1\}.
\]
Different points with the same \(x\) can receive the same colour: under
this hypothesis they are never adjacent. Every unit edge is accounted for
by (2), so pulling back a colouring of the distance graph colours all rows
simultaneously.

For \(1/3<d<1/2\), the only row differences are \(0,1,2\), and
\[
 D_d=\{1,\sqrt{1-d^2},\sqrt{1-4d^2}\}.
\]
Equation (1) proves four-colourability. For \(1/2<d<1\), only \(0,1\) occur,
so (1) gives three colours. For \(d>1\), only same-row edges remain, giving
two colours. The only excluded spacings at or above \(1/3\) are
\(1/3,1/2,1\), where vertical unit edges make this projection invalid.
They are settled explicitly next.

## 3. The three vertical-edge boundaries

In each construction, choose one representative \(t\) of every coset of the
stated additive subgroup \(H\) in \(\mathbb R\). All unit edges preserve the
coset. Unique integral coefficients in that coset make the colour formulas
well-defined.

**Spacing \(d=1/3\).** Put
\[
 a=2\sqrt2/3,\qquad b=\sqrt5/3,\qquad H=\mathbb Z+\mathbb Za+\mathbb Zb.
\]
The numbers \(1,a,b\) are linearly independent over \(\mathbb Q\), as follows
from the standard basis of \(\mathbb Q(\sqrt2,\sqrt5)\). Write
\(x=t+m+na+pb\), uniquely, and colour
\[
 c(x,j/3)=m+p+j\pmod2. \tag{3}
\]
The complete unit-step table is:

| Absolute row difference | Horizontal difference | Colour change in (3) |
| --- | --- | --- |
| 0 | \(\pm1\) | 1 |
| 1 | \(\pm a\) | 1 |
| 2 | \(\pm b\) | 1 |
| 3 | 0 | 1 |

Larger row differences exceed unit distance. This proves bipartiteness of
the full support, including the vertical edges between rows three apart.
A same-row unit edge proves the exact chromatic number is two.

**Spacing \(d=1/2\).** Let
\(H=\mathbb Z+\mathbb Z\sqrt3/2\), write
\(x=t+m+n\sqrt3/2\), and use
\[
 c(x,j/2)=m+j\pmod3. \tag{4}
\]
Same-row edges change \(m\) by one. Edges between adjacent rows change
\(n\) by one and \(j\) by one, independently in sign. Vertical unit edges
change \(j\) by two. Every change in (4) is nonzero modulo three.
The points \((0,0),(0,1),(\sqrt3/2,1/2)\) form a unit equilateral triangle,
so the chromatic number is exactly three.

**Spacing \(d=1\).** Use \(H=\mathbb Z\), write \(x=t+m\), and colour
\(c(x,j)=m+j\pmod2\). Horizontal and vertical unit steps both change the
colour. For \(d>1\), there are no cross-row edges and each line can use its
usual two-colouring. A unit edge gives the lower bound two in each case.

## 4. Exact classification when only adjacent rows interact

Suppose \(1/2<d<1\), and put \(a=\sqrt{1-d^2}\). The only unit displacements
are \((\pm1,0)\) and \((\pm a,\pm d)\).

If \(a\) is irrational, choose coset representatives for
\(H=\mathbb Z+\mathbb Za\). For \(x=t+m+na\), the two-colouring
\[
 c(x,jd)=m+j\pmod2
\]
changes colour on every allowed displacement.

If \(a=p/q\) is rational in lowest positive terms and \(q\) is odd, choose
coset representatives for \((1/q)\mathbb Z\), write \(x=t+n/q\), and use
\[
 c(x,jd)=n+(1-p)j\pmod2. \tag{5}
\]
A same-row unit step changes \(n\) by \(q\), which is odd. An adjacent-row
step changes \(n\) by \(\pm p\) and \(j\) by \(\pm1\); the change in (5)
is congruent to \(p+1-p=1\) modulo two.

If \(q\) is even, coprimality forces \(p\) odd. There is an explicit simple
odd cycle on just two of the rows. Start with the zigzag
\[
 v_k=(kp/q,(k\bmod2)d),\qquad 0\le k\le q.
\]
It has \(q\) unit edges and ends at \(v_q=(p,0)\). Return along the lower
line through \((p-1,0),(p-2,0),\ldots,(1,0),(0,0)\). There are \(p\) further
unit edges. The total length \(p+q\) is odd. All interior zigzag horizontal
coordinates are nonintegral because \(p,q\) are coprime, so no internal
zigzag vertex coincides with the return path. Both paths are individually
simple and meet only at their endpoints. This is an actual geometric odd
cycle, not a periodic quotient or an artificial wrap edge.

The preceding three-colour upper bound and this cycle prove
\(\chi(X_d)=3\) in exactly the even-denominator cases. The same proof gives
the familiar two-line classification for any separation \(0<d<1\); the
restriction \(d>1/2\) here ensures that the *entire infinite comb* has no
additional row interactions.

## 5. Classical context and scope

Distance graphs on the real line were studied by Eggleton, Erdős and Skilton
in [Colouring the real line](https://users.renyi.hu/~p_erdos/1985-09.pdf)
(1985). Our use of (1) is an elementary application of the greedy bound.
The passage to full infinite supports uses Theorem 1 of the
[1951 de Bruijn--Erdős paper](https://users.renyi.hu/~p_erdos/1951-01.pdf).

Guldan's [On a problem of colouring the real plane](https://dml.cz/handle/10338.dmlcz/126170)
(1991), Theorem 2, already uses two-line zigzag odd cycles followed by an
integer return path to prove lower bounds for strips. The cycle in Section 4
uses that classical mechanism with general reduced \(p/q\) and records the
exact parity criterion needed for this full support. Guldan also discusses
continuous strips and the rational plane; those are different supports from
an infinite family of discrete parallel lines. No priority is asserted for
the elementary bounds, colour formulas, or zigzag construction.

Attribution addendum, 6 September 2026: Theorem 4.3 of Axenovich, Choi,
Lastrina, McKay, Smith and Stanton, *On the Chromatic Number of Subsets of
the Euclidean Plane*, Graphs and Combinatorics 30 (2014), 71–81, already
states and proves the exact two-parallel-line classification used here.
See the [authors' manuscript](https://wwwalt.math.kit.edu/iag6/~axenovich/media/euclid-submitted-4-2011.pdf).
This attribution does not alter the theorem statements or certificates.
The subsequent [rational-height support theorem](../hadwiger_nelson_quarter_rational_heights/README.md)
extends the campaign's exclusions to specified arbitrarily small spacings.

The campaign contribution is a consolidated, checked exclusion of the complete
geometric families stated here, with all vertical-edge boundaries handled
and precise distinctions between upper bounds and exact chromatic numbers.
It does not classify spacings below \(1/3\), assert four colours are ever
necessary in \((1/3,1/2)\), or decide arbitrary configurations on four or more
parallel lines. A finite fixture whose greedy word uses four colours need
not itself be four-chromatic.

The [paired-circle consolidation](PAIRED_CIRCLES.md) preserves the preceding
program's durable theorems and their limitations. That mechanism is retired
under the current coordination gate; none of its list/phase claims is used
in these proofs. HN-2's [H560 closure through 503 vertices](../hadwiger_nelson_heule560_criticality_bound/README.md)
is separate fixed-support context and likewise is not a mathematical premise.

## 6. Reproducible exact audit

Requirements: Python 3.11 or later, standard library only; tested with
Python 3.11.2. From this directory, use fresh output directories:

```sh
sha256sum -c SHA256SUMS
python3 -B build.py --out work
python3 -B verify.py --out audit
python3 -O -B verify.py --out optimized
```

[build.py](build.py) deterministically constructs 12 finite fixtures, colours
them using the proved orderings or explicit formulas, and regenerates
[certificate.json](certificate.json) byte for byte. It identifies unit edges
through the horizontal root equation for each pair of rows. These fixtures
contain 1,061 vertices in total, with no claim that their union is one graph
or that they exhaust any continuous family.

[verify.py](verify.py) imports no producer or earlier package. It uses a
prime-parity representation of the real multiquadratic field and computes
squared Euclidean distances directly on **73,075 point pairs**. It checks
**2,638 actual unit-edge colour inequalities**, the directional predecessor
bounds, and the explicit coordinate formulas. Positive algebraic signs use
convergent rational root enclosures; no floating-point comparisons occur.
Distinct squarefree radicals form independent rational basis elements in
the containing multiquadratic field.

The audit also checks all **24 signed unit-step generators** at the three
boundary spacings (12, 8, and 4 respectively), the half-spacing triangle,
73 odd-denominator parameter controls, six complete distance-graph controls,
and **38 exact odd-cycle witnesses** with 744 cycle edges in total. The
cycles range from 3 to 37 vertices. These finite controls check the formulas;
their extension to all parameters is proved in Sections 1--4.

Eight malformed certificates are rejected, including a vertical-edge case
incorrectly passed to the horizontal projection. All semantic checks use
explicit exceptions and run identically with Python assertions disabled.
[expected.json](expected.json) gives the detailed results;
[validation.json](validation.json) records replay and normal/optimized checks.

Certificate size: **6,359 bytes**. SHA-256:

```text
5e293486a3837ee6311a1e7d7bd7a107b015abc6b2180352d3cfd5b42c8ce635
```

The universal proof, compactness premise, coordinate-coset uniqueness and
geometric edge classification are written mathematics. Executable checks are
finite audits, not a proof assistant or an independent-author review. No
native solver, private input, large trace or numerical search is needed.
This full-support milestone is complete; no smaller spacing or new line-count
phase is started in this package.
