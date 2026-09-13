# Pair-determined Moser overlays cannot improve Parts-509

Let P be the 509 distinct published Parts points, with the strict unit graph:
all and only pairs at Euclidean distance one are edges. Let M be the seven
complex points

    0, 1, w, 1+w, rho, rho*w, rho*(1+w),
    w=(1+i*sqrt(3))/2,  rho=(5+i*sqrt(11))/6.

Their strict graph is the Moser spindle, with 11 edges. The small controls
exhaustively find zero proper three-colourings and 384 proper four-colourings.
An isometry below may reverse orientation.

**Theorem (exact computer-assisted).** For every Euclidean isometry T with
`|P intersect T(M)| >= 2`, every graph of order at most 508 whose vertices lie
in `P union T(M)` and whose edges have length one is four-colourable.

Each entire union contains Parts' five-chromatic graph P. Thus its minimum
order of a non-four-colourable subgraph is exactly 509, using the previously
certified non-four-colourability of P for this last equality. The new upper
colourability statement needs only exact coordinates and explicit positive
colouring witnesses; it imports no earlier minimization exclusion theorem.

## 1. Exhausting arbitrary plane isometries

Choose distinct m_i,m_j of M and distinct p_a,p_b of P. Necessarily
`|m_j-m_i|^2=|p_b-p_a|^2`. If this equality holds, the two isometries taking
m_i to p_a and m_j to p_b are

    T_+(m)=p_a+(p_b-p_a)*(m-m_i)/(m_j-m_i),
    T_-(m)=p_a+(p_b-p_a)*conjugate((m-m_i)/(m_j-m_i)).

A complex multiplier has modulus one precisely by the matched-length equality.
The displayed maps include every isometry with these ordered coincidences.
Enumerate unordered target pairs a<b and ordered source pairs i!=j; reversing
the source order accounts for the other target order. Enumerating both signs
accounts for reflections. Every allowed T is represented, even when more than
two points coincide with P. Canonicalize by the complete sorted coordinate set,
not graph isomorphism.

In `K=Q(sqrt(3),sqrt(5),sqrt(11))`, the basis products satisfy
`e_i*e_j=R[i&j]*e_(i xor j)` for
`R=(1,3,5,15,11,33,55,165)`. Source coordinates and every normalized displacement
above lie in `K+iK`. All their rational coefficients have denominator dividing
72. Parts' integer coordinate table has denominator 96, so every image has
coefficient denominator dividing 6912. No field restriction was assumed on T;
it follows from the two coincidences. Coefficient equality is exact because the
eight real radicals form a rational basis.

There are seven distinct source squared lengths and 42 different normalized
coordinate templates. Exactly 78,474 target-pair/template routes give 25,590
different seven-point images. Their intersections with P have sizes

| Intersection size | Distinct images |
|---:|---:|
| 2 | 14,143 |
| 3 | 6,369 |
| 4 | 3,027 |
| 5 | 1,115 |
| 6 | 624 |
| 7 | 312 |

Across these images there are 24,751 distinct external points. The checker
reconstructs every external-to-original and external-to-external unit edge
needed for each individual union. A homomorphism of the coefficient ring to
integers modulo 1,000,081 is a sound rejection filter. Its radical-square
identities and invertibility of the coordinate denominators are checked.
Only a nonzero residue rejects an equality; every survivor is evaluated in the
full exact field. Hence modular collisions cannot hide or invent a unit edge.
No numerical tolerance or approximate root test is used.

## 2. Colouring and the deletion budget

For an external set A from one image, let `P-D+A` denote the strict graph on
`(P minus D) union A`. For every original vertex u, the imported witness library
C_u consists entirely of checked proper four-colourings of `P-u`. There are
6,398 rows in total: 509 from the original criticality certificate and 5,889
from the later four-point package. Only these positive rows are imported; no
solver answer, declared set, or earlier exclusion theorem is used.

For c in C_u, a new point q has the list of colours absent from its neighbours
in `P-u`. The graph on A is list-colourable exactly when c extends to `P-u+A`.
The public verifier generates all proper words in `{0,1,2,3}^A` directly and
filters them by these lists, using exact finite bitsets. There are at most five
new points, hence at most 1,024 words. The discovery implementation used a
separate recursive list search; complete coverage and residual entries agree.

Define the conservative obstruction set

    Uhat(A)={u: no row of C_u extends to P-u+A}.

A positive extension at u colours every `P-D+A` with u in D by restriction.
Consequently a non-four-colourable `P-D+A` requires `D subset Uhat(A)`.
This does not assert non-four-colourability for any member of Uhat(A).

If b=|A|, a graph on these coordinates with order at most 508 has
`|D| >= b+1`. Thus `|Uhat(A)| <= b` suffices for its colourability. Otherwise it
suffices to supply a colouring for every `(b+1)`-subset of Uhat(A): any larger
D contains one of these subsets, and restriction gives a colouring.

## 3. Whole and partial spindle selections

For each of the 25,278 images not contained in P, first compute Uhat(A) for its
entire external set A. The histogram of its size is

    0:24034, 1:1106, 2:102, 3:21, 4:8, 5:3, 6:2, 7:2.

A target subgraph may omit some of these new points. This case must not be
silently replaced by the whole-set calculation. For B subset A,

    Uhat(B) subset Uhat(A),

because any colouring extending to A also extends to B. Whenever
`|B| >= |Uhat(A)|`, the existing bound already settles B. For every smaller
nonempty B, enumerate it explicitly and intersect the available parent bounds
if it occurs in several images. Empty B is settled by an original vertex-deletion
row. This accounts for every subset of every image, including images entirely
contained in P.

There are 1,026 such subset routes, giving 715 distinct B. After intersecting
parent bounds, 640 require further list tests. Fresh list tests leave 16 sets
with a bound larger than their cardinality: three two-point sets, seven
three-point sets, three four-point sets, and three five-point sets. Together
they require exactly 42 target deletion sets.

`certificate.json` supplies a proper four-colouring of each resulting
508-point graph. The verifier checks every retained original edge, every
new-to-original edge, and every unit edge between selected new points;
101,723 edge inequalities are replayed. This proves all remaining cases.
No UNSAT answer or negative solver certificate is involved.

Finally, a non-induced unit graph on any of these points is a subgraph of its
strict graph and inherits a colouring. This proves the theorem.

## 4. Validation and limits

An additional checker uses complex coordinates in
`Q(t,r,s)`, where `t^2=-3`, `r^2=-11`, and `s^2=5`. It reconstructs inverses by
rational Gaussian elimination, independently re-enumerates the isometries,
and compares the full external coordinate set, every noncontained placement,
every original edge, and every relevant new edge entry by entry. This is a
second implementation and arithmetic representation, run by the same author;
it is not an external review or a formal proof.

Trust remains in the written finite reduction, the source coordinates,
CPython exact integers/rationals, and the small verifier implementations.
The coordinate table is hash-pinned and separately compared with a fresh parse
of all 509 original radical expressions. SAT is only a witness generator.
Matching hashes bind the files; they are not proofs of their interpretation.

The theorem concerns one added spindle with at least two actual point
coincidences. It does not cover one or zero coincidences with additional unit
contacts, simultaneous coupled spindle additions, other motifs, moving the
original Parts points, or arbitrary smaller plane unit-distance graphs. It
makes no global lower-bound or record-improvement claim.
