# A dense reflected inner gadget still admits every origin attachment

Let A and V be the exact archived Parts v159e646 and v214e977 point sets,
respectively, in the source order pinned by the code. Write

\[
 \alpha=i\sqrt3,\quad\beta=i\sqrt{11},\quad z=\sqrt{33},\qquad
 t=(5+z+5\alpha-\beta)/12,\qquad B=A\cup(\overline A+t).
\]

**Theorem (exact computer-assisted).** For every Euclidean isometry g
satisfying 0 in g(V), the strict unit-distance graph on B union g(V) is
four-colourable. It has at most 506 vertices. In the branch where the
relative multiplier is outside E=Q(alpha,beta), it has exactly 506 vertices
and at most 2,389 strict unit edges. This edge bound is attained.

The inner placement and its origin are fixed. The theorem does not cover
other B attachment vertices, disjoint placements, or adding new vertices.
It establishes no five-chromatic graph with at most 508 vertices.

## Selection and exact inner geometry

The existing [A159 overlap catalogue](../hadwiger_nelson_nonmono159_overlap10/README.md)
contains all 30,013 isometries with at least ten overlaps. Exactly 6,435
entries have at least 24 overlaps, hence at most 294 union vertices and
room for all 214 vertices of V within 508. Reading the already verified
catalogue metadata, the largest strict edge count among these entries is
1,389, attained at catalogue indices 15969 and 16347. We select index 16347,
the explicit reflected-and-translated image above. This is reuse of the
durable census, not a new enumeration or a search over arbitrary inner graphs.

Exact reconstruction gives 25 overlaps, 293 distinct vertices and 1,389
strict edges. The two inherited 646-edge copies share 40 edges; there are
137 further inner cross edges. The origin uniquely has maximum degree 30;
every other vertex has degree at most 29. Labels retain A first and append
new points of conjugate(A)+t in source order. V has 214 vertices and 977
strict edges, and its point set is invariant under complex conjugation.

This differs from the previously studied A union ((5+beta)/6)A, whose
292 vertices support only 1,251 edges. Increased internal density is the
construction change tested here; it does not suffice to obstruct the
specified family of attachments.

## Complete angular reduction

Put R=Q(z) and E=R(alpha). Then beta=alpha*z/3, alpha squared is -3,
and the real elements of E are exactly R. Both B and V lie in E.
The existing [whole-field colouring theorem](../hadwiger_nelson_nonmono_field_obstruction/PROOF.md)
four-colours E. We use it only for that restricted complex field.

For a rotation with g(q)=0, q in V, write g(V)=u(V-q), with |u|=1.
Conjugation invariance of V also expresses every reflected image in this
form, with possibly a different source anchor. Thus all 214 anchors q
and every unit u suffice. If u belongs to E, the whole-field theorem
settles every strict edge, including possible further overlaps. If u does
not belong to E, a second coincidence b=u(v-q), v distinct from q, would
force u=b/(v-q) into E. Therefore the origin is the sole overlap. All edges
incident to it are already internal; the inherited edge count is
1,389+977=2,366. Without an additional cross edge, arbitrary proper component
colourings can be permuted to agree at the origin.

For a new cross edge take b in B minus {0} and d=v-q nonzero in V-V. Put

\[
 c=\overline b d,\quad S=|b|^2+|d|^2-1,\quad
 \Delta=4|b|^2|d|^2-S^2.
\]

The unit condition is equivalent, for |u|=1, to

\[
 c u^2-Su+\overline c=0.
\]

Here c is nonzero and S,Delta belong to R. If Delta is negative in the
specified real embedding, there is no unit root. If Delta is nonnegative,
the two roots, counting multiplicity, are (S plus or minus sqrt(-Delta))/(2c)
and have unit norm. They lie in E exactly when Delta/3 is a square in R.
Indeed, the imaginary elements of E are exactly alpha*R. The zero
discriminant case belongs to this in-field branch.

Each remaining pair therefore defines the irreducible monic polynomial

\[
 P_{b,d}(X)=X^2-(S/c)X+\overline c/c.
\]

Two such polynomials share an outside-E root exactly when they are equal,
by uniqueness of the monic minimal polynomial. Grouping all pairs by this
polynomial gives the complete new cross-edge set for both roots. For each
anchor q, project a group through every incidence d=v-q in the exact
source difference table. This includes all q,v pairs without an angular
sampling assumption. Nonempty projections from distinct groups cannot
coincide: any common edge would determine the same irreducible polynomial.

The proof and exact integer sign, square and projective-normalization
formulas are the [previous all-anchor reduction](../hadwiger_nelson_mixed505_all_gadget_anchors/PROOF.md),
which applies to the present B without change: it uses only B contained in
E, its fixed origin, and a positive internal colouring. In particular,
B is represented at denominator 72 and V-V at denominator 12, so the
previous integer scaling formulas apply literally. The independent audit
instead forms S/c and conjugate(c)/c using rational four-dimensional field
arithmetic and an independently implemented real-square decision.

## Complete census and colour certificates

There are 4,418 nonzero source difference vectors. The complete
292 times 4,418 = 1,290,056 pair census is:

| Pair class | Count |
|---|---:|
| Negative discriminant | 520,070 |
| Unit roots in E | 127,748 |
| Two unit roots outside E | 642,238 |

The last row forms 303,730 ambient quadratic classes, or 607,460 distinct
outside-E unit multipliers. Their projections give 5,189,194 nonempty
anchor/class cases, or 10,378,388 anchor/root incidences. The latter count
is not a count of distinct multipliers, unlabeled graphs or point sets.
Every nonempty projection has at most 23 new cross edges.

The certificate has five complete proper B colourings and fourteen complete
proper V colourings, totalling 4,480 bytes including line breaks. Each B
row colours the origin 0. For a V row f and source anchor q, replace each
colour f(v) by f(v) XOR f(q); this is a permutation of the four colours
mapping the anchor to 0. Try the six permutations pi fixing 0. For each
projected cross-edge set C_q, the checker finds rows bcol,f and pi with

\[
 bcol(b)\ne\pi(f(v)\mathbin{\mathrm{XOR}}f(q))
 \quad\hbox{for every }(b,v)\in C_q.
\]

The resulting component colourings agree at the origin and properly
colour every inherited and new edge. All 5,189,194 cases have such a
witness. Empty projections and the in-field branch were settled above,
which completes the universal angular quantifier.

Discovery started with one existing B row and ten prior V rows. That
library missed 1,309 cases. Four bounded SAT calls, each returning a directly
checked positive assignment, reduced the misses to 124, 34, 2 and 0.
Each call used 2,024 Boolean variables, exactly-one colour clauses on the
506 quotient vertices, every unit-edge colour exclusion, and origin colour
0. The solver was CaDiCaL195 through python-sat 1.9.dev15, with a one-million
conflict limit per call. Each took less than 0.06 seconds in the discovery
run. No UNSAT assertion, solver completeness or solver trust is needed
for the theorem; the published positive rows are checked without a solver.

## Direct physical maximum-contact control

At source anchor q=10, the code reconstructs both roots of

\[
 X^2-TX+W,\qquad
 T=-\tfrac12-\tfrac16z-\tfrac56\alpha+\tfrac12\beta,
 \quad W=\tfrac16z-\tfrac16\alpha.
\]

For r=sqrt(-408+72z), take

\[
 u_\pm={-18-6z-30\alpha+6\alpha z
       \ \pm r(3+6\alpha+\alpha z)\over72}.
\]

The radicand is positive since 408 squared is smaller than 72 squared
times 33. Its other real conjugate is negative, so r is not in R, and
as a real number it is not in E. The displayed polynomial is one of the
outside-E classes. Direct multiplication verifies |u|=1 and P(u)=0.

`controls.py` uses the basis
1,z,alpha,alpha*z,r,z*r,alpha*r,alpha*z*r with relations
z squared =33, alpha squared =-3, r squared =-408+72z. It does not import
either census. Conjugation fixes z,r and negates alpha. Integer coordinates
at denominator 2592 give both complete physical point sets. The checker
compares every one of their 127,765 unordered pairs for exact unit distance,
finds precisely 506 distinct points and 2,389 edges, and checks complete
proper colourings. Its 23 cross edges exactly match the projected class.
A deliberately monochromatic edge is rejected. Both root graphs have
canonical edge-list SHA-256
`11af24079955c011d7ac15812b93f273044f94ce303281676abff341f33cf21a`.

## Evidence and trust boundary

The independent rational enumeration agrees with the integer enumeration
on every pair classification and every complete quadratic edge group.
The audit reconstructs the source geometry and every difference incidence
separately, then directly tries the colour permutations. Its entire
coverage transcript and every anchor histogram agree. Canonical hashes:

- Pair classifications: `21bb5efda6dec4739cb0b716ce59df3ac59c44dd933865b3645e1959325cdc96`.
- Ambient edge partition: `ecf735c7f934edfb095e5efb03597c97f1141c856acff55359dd3e71bf2a5b77`.
- Selected colour witnesses: `c0652edec4bda61e0778f1c8b70a4bd561511a598b014ac04b3e04853c72076c`.
- Every anchor histogram: `26d76401f50e05d608d2541cdbfb1b5ada1fc606fbbc1d3f1f0da5bc1dbf614f`.

The universal reduction and whole-field colouring are unformalized
mathematical dependencies. The finite evidence uses arbitrary-precision
integers and exact rational arithmetic. The audit is an alternative
implementation by the same researcher, not external peer review. Imported
source, coordinate tables and catalogue bytes are hash-pinned. Gadget
minimality and their advertised nonmonochromatic forcing properties are
not hypotheses. No floating-point distance or unverified negative solver
answer enters the claim.
