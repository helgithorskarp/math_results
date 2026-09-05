# First negative relative trace: exclusion and a sharp limit of residue gluing

Put `E=Q(i sqrt(3),i sqrt(11))`, `alpha=i sqrt(3)` and `R=Q(sqrt(33))`.
Use the fixed conjugation-compatible embedding
`iota:E -> U=Q_2(omega)`, `omega^2+omega+1=0`, with
`sqrt(33)=1 mod 8`. Write `O=Z_2[omega]`, `v(2)=1`, and
`res:O -> F_4`. All local valuations below use this embedding.

**Theorem.** Let `u` be a unit complex number of degree two over `E`,
with relative minimal polynomial `Z^2-T Z+J`. Suppose `v(T)=-1`.
Let `P,Q subset E` be nonempty connected unit-distance source graphs,
and write an arbitrary translation in `E(u)` uniquely as `h=m-u n`.
Set `X=P-m`, `Y=Q-n`. Then:

1. If `X,Y subset O`, the entire strict unit-distance graph on
   `P union (u Q+h)` is four-colourable by the centred residues. On every
   cross edge, one centred endpoint is a local unit and the other is in
   `4O`. In particular **every placement with a shared vertex is
   four-colourable** in this trace stratum.
2. If a cross edge has a nonintegral centred endpoint, its two valuations
   are `-k` and `1-k` for some integer `k>=1`. The source on the more
   negative side occupies that fixed valuation coset. On the other side,
   all cross-edge endpoints have the same residue colour, measured from
   any fixed source anchor.
3. In the latter case, arbitrary permutations of the two source residue
   colourings glue if and only if the cross-edge endpoints on the more
   negative side omit at least one of the four residue colours.

This is a complete test for **these two fixed residue colourings**, not
for all graph colourings. A disjoint, connected-source counterexample to
uniform residue-permutation gluing already occurs for

\[
u=(1+i\sqrt{15})/4,\qquad T=1/2,\quad J=1.
\]

The exhibited graph has **20 vertices, 28 edges, and chromatic number
exactly three**. Its two sources have 13 and 7 vertices. Their cross
interface is exactly a four-edge matching; none of the 24 relative
permutations of their residue colourings glues. Thus a saturated residue
boundary is necessary for a non-four-colourable graph in the nonintegral
branch, but is not sufficient, even with both sources connected.

Reflections are included by replacing `Q` with its complex conjugate.
There is no denominator or cardinality bound in the theorem. Traces of
valuation below `-1`, translations outside `E(u)`, and the general
nonintegral branch's four-colourability remain open here. No five-chromatic
graph, including one with at most 508 vertices, is obtained.

## 1. The local-coset and cross-edge identities

The accepted [base-field theorem](../hadwiger_nelson_nonmono_field_obstruction/PROOF.md)
gives

\[
N(A+B\omega)=A^2-AB+B^2,\qquad v_2(Nz)=2v(z).
\tag{1}
\]

A unit displacement in `E` therefore maps into `O` with nonzero `F_4`
residue. Every connected source occupies one additive `O`-coset, by
adding unit displacements along a path. Residues of differences from
any source anchor give a proper four-colouring of all its strict edges.
Changing the anchor only permutes these four colours by a translation.
We use `O` for the corresponding local condition on elements of `E`;
no quotient of the entire characteristic-zero field by two is asserted.

The [locally integral trace proof](../hadwiger_nelson_integral_trace_gluing/PROOF.md)
derives, without an integrality hypothesis, the identities

\[
J\overline J=1,\qquad T=J\overline T.
\tag{2}
\]

For completeness, conjugate the minimal polynomial and take its
reciprocal: its monic form is
`Z^2-(bar(T)/bar(J)) Z+1/bar(J)`. Equality with the irreducible minimal
polynomial proves (2). In particular `J` is a local unit, and
`J=T/bar(T)` when `T!=0`. The relative trace `T` need not be real or
coincide with the complex trace `u+bar(u)`.

For a cross edge put `x=p-m`, `y=q-n`, `c=bar(x)y` and
`S=Nx+Ny-1`. Multiplying `|x-u y|^2=1` by `u` gives
`c u^2-S u+bar(c)=0`. Reducing by the minimal polynomial yields

\[
cT=S,\qquad \overline c=Jc,
\]

and hence the necessary identity in `E`

\[
q_T(x,y):=N(x)+N(y)-T\overline x y=1.
\tag{3}
\]

All subsequent exclusions use this necessary identity; no unjustified
converse or division by a possibly zero endpoint is needed. Put `D=2T`,
which is a local unit.

## 2. Integral centred sources

Suppose `x,y in O` satisfy (3). Multiply it by two and reduce modulo two:

\[
\operatorname{res}(D)\,\overline{\operatorname{res}(x)}
\operatorname{res}(y)=0.
\]

At least one of `x,y` has zero residue. They cannot both have zero residue:
then `Nx,Ny in 4 Z_2` and `T bar(x)y in 2O`, contradicting (3).
Exactly one is a unit, proving the properness of the common centred
residue colouring on all cross edges. It is already proper internally.

There is a stronger endpoint restriction. Suppose `x` is a unit and
`y=2z`. Equation (3) reduces modulo two to
`1-res(D) bar(res(x)) res(z)=1`, so `res(z)=0` and `y in 4O`.
The case with the sides reversed is identical.

An overlap has `x=u y` with `x,y in E`; since `u notin E`, it forces
`x=y=0`. If an overlap exists, connectedness therefore puts both entire
centred sources in `O`. Their common point receives colour zero in both
copies. This proves the shared-vertex corollary, including strict edges
and vertex identification. If there are no cross edges, independent
source colourings suffice, with any common point aligned.

## 3. Nonintegral anchors: an endpoint residue restriction at every depth

Suppose an edge has `a=v(x)<0`. A zero opposite endpoint is impossible
by (3) and (1). The three terms in (3) have valuations

\[
2a,\quad 2b,\quad a+b-1,\qquad b=v(y).
\tag{4}
\]

If `a=b<0`, the last is the unique smallest valuation, impossible for a
sum equal to one. Otherwise exchange the sides so `a<b`. Under a side exchange use the
conjugate of (3), which replaces `T` by `bar(T)` and preserves its
valuation; write `T` for that ordered trace from this point on. If `b>a+1`,
`2a` is uniquely smallest, again impossible. Valuations are integers,
so the only remaining case is `b=a+1`. Thus they are `-k,1-k`, `k>=1`.
The more negative side is fixed for this entire source pair: all points
of that source differ integrally from this anchor and retain valuation
`-k`. Applying (4) to every cross edge forces each opposite endpoint to
have valuation `1-k`.

Fix one edge `(x_0,y_0)` with these ordered valuations and put

\[
X_0=2^k x_0,\quad Y_0=2^{k-1}y_0.
\]

Both are local units. For any other edge write
`x=x_0+z`, `y=y_0+w`, with `z,w in O`. The scaled equation is

\[
F(X,Y):=N(X)+4N(Y)-D\overline X Y=2^{2k},
\quad X=2^k x,\quad Y=2^{k-1}y.
\tag{5}
\]

Subtract its anchor version and divide by `2^(k-1)`. Direct expansion,
with `Tr(t)=t+bar(t)`, gives the exact integral identity

\[
\begin{split}
0={}&2\operatorname{Tr}(\overline{X_0}z)
+4\operatorname{Tr}(\overline{Y_0}w)
-D(\overline{X_0}w+2\overline zY_0)\\
&+2^k\big(2N(z)+2N(w)-D\overline z w\big).
\end{split}
\tag{6}
\]

Modulo two only `-D bar(X_0)w` remains. Its first two factors are units,
so `res(w)=0`. All cross endpoints in the less negative source therefore
have the same residue colour, including the case `k=1` when that source
is integral. This proof covers every depth; finite checks below are only
validation of the identity and boundary behaviour.

Let its constant boundary colour be `b`. Under a permutation it may be
sent to any one colour `c`. The two residue colourings glue precisely
when the more negative source's boundary avoids `c`. Arbitrary
permutations on that source do not change whether all four colours
occur. This proves the equivalence in the theorem. There is no overlap
in this branch, since the more negative source excludes zero.

Consequently a non-four-colourable two-source placement with this trace
and a cross edge must be disjoint, lie in the nonintegral branch, and
have all four residue colours on the more negative boundary. These are
necessary conditions only.

## 4. A connected 20-vertex obstruction to the colouring method

Take `u=(1+i sqrt(15))/4`. It has modulus one, and its minimal polynomial
is `Z^2-(1/2)Z+1`. It is outside `E`: otherwise `sqrt(5)`, obtained by
dividing `i sqrt(15)` by `alpha`, would be in `R=Q(sqrt(33))`, which it is
not. This also proves the degree-two hypothesis.

The four designated pairs `(x,y)` are

\[
(1/2,1),\quad(-1/2,-1),\quad
\left(\frac{-36-9\alpha}{38},\frac{-4-\alpha}{19}\right),\quad
\left(\frac{-36+9\alpha}{38},\frac{-4+\alpha}{19}\right).
\tag{7}
\]

In each pair `bar(x)y` is real. The first two satisfy (3) directly. For
each last pair `x=(9/2)y` and `Ny=1/19`, so

\[
Nx+Ny-\tfrac12\overline x y
=\frac{81}{76}+\frac4{76}-\frac9{76}=1.
\]

Thus all four pairs give actual Euclidean unit edges from `x` to `u y`.

Here is an explicit connected completion of each source, using only
unit paths in `E`. Put

\[
\eta=(1+\alpha)/2,\qquad \nu=(13+8\alpha)/19.
\]

Both have norm one, as does `eta nu`. Start `P` with `1/2,-1/2`. Add the
successive vertices of the six-step path from `1/2` with displacements

\[
1,-\eta,-\nu,-\nu,\eta\nu,\eta\nu,
\]

and its complex conjugate. Deduplicate equal points, retaining the first
occurrence. The endpoints are the last two `x` values in (7). These two
paths and the edge `1/2 -- -1/2` give **13 distinct connected vertices**.

Let `Q`, in order, be

\[
1,-1,(-4-\alpha)/19,(-4+\alpha)/19,0,-\eta,-\overline\eta.
\]

The point zero connects to `1,-1,-eta,-bar(eta)`. The non-real `y` values
connect to `-bar(eta)` and `-eta`, respectively, so `Q` is connected.
All of `P` lies in `1/2+O` and all of `Q` in `O` by these unit paths.

With `F_4` colour encoding `a+b omega -> a+2b`, the anchored residue
strings in the stated source order are

```
P: 0112321232313
Q: 0000123
```

The four pairs (7) have residue colour pairs `(0,0),(1,0),(2,0),(3,0)`.
No two permutations of the residue colours can avoid all four collisions:
one of the four colours on the first side equals the single chosen
boundary colour on the second. The exact checker finds that these are
**all** cross edges. They form a matching, so this example also excludes
using cross-acyclicity alone to justify gluing these fixed colourings.

For the strict graph on the ordered points `P` followed by `u Q`, the
following is a proper three-colouring:

```
01120210202102011122
```

Exact reconstruction gives 16 edges in `P`, 8 in `Q`, and 4 cross edges,
with 20 distinct physical vertices. The triangle on `0,-1,-eta` in `Q`
proves the lower bound three. Hence this graph's chromatic number is
exactly three. In particular this is a counterexample to a proposed
colouring procedure, **not** to graph four-colourability. The source table,
full strict edge hash and colouring are recorded in `expected.json`.

## 5. Construction consequence and limits

The connected fixed alternative `B292/V214` sources from the
[inner construction](../hadwiger_nelson_nonmono159_moser_triple/PROOF.md)
are both contained in `E`. For relative trace of valuation `-1`, every
placement with an overlap is now excluded, as is every disjoint placement
whose centred source cosets are both integral. A remaining nonintegral
506-vertex candidate must saturate all four boundary residues on the
more negative side. The 20-vertex witness shows why that filter must be
followed by tests using additional source colourings or actual graph
colourability; passing it is not positive evidence for chromatic number
five. No fixed B/V family is exhaustively enumerated here.

There is also no compatible extension of the fixed embedding to `E(u)`
when `v(T)<0`: a compatible image of `u` has norm one and therefore
valuation zero by (1), as does `J`. The relation `T=u+J/u` would then make
`T` integral, a contradiction. This rules out that particular whole-field
embedding method, not every four-colouring of the field.

The earlier [integral-trace theorem](../hadwiger_nelson_integral_trace_gluing/PROOF.md)
closes all placements with `v(T)>=0`. This contribution supplies a
conditional exclusion and an exact method boundary at `v(T)=-1`; it does
not close that entire stratum. The [cross-cycle result](../hadwiger_nelson_cross_cycle_forest/PROOF.md)
is relevant context for the forest frontier but is not a dependency of
this proof. Neither the sealed Parts pool nor the parked Parts two-overlap
census is restarted.

## 6. Exact checks, trust, and sources

`local_checks.py` checks both coefficients of the generic polynomial
identity (6). It independently enumerates all 48 units `D` and all
196,608 integral `(D,x,y)` triples modulo eight, recovering 4,608 solutions;
every solution has one unit endpoint and the other divisible by four.
For each scaled depth `k=1,2,3`, all 110,592 unit triples `(D,X,Y)` are
tested against (5). Each yields 2,304 solutions. Grouping by the two
source-coset residues confirms a single shallow-side boundary residue
in every group. These finite checks do not replace the uniform proof.

`verify.py` checks seven exact geometries: a shared-centre wheel pair,
a disjoint integral-centred B/V pair, the same geometry expressed with a
non-real relative trace, two nonintegral wheel pairs including depth
three, the connected saturation witness, and its side-swapped reflected
copy. It checks connectedness, every strict distance and edge, all
relative colour permutations, and proper positive colourings.

`audit.py` imports neither the generator nor its field/local arithmetic.
It independently reconstructs source gadgets and paths, embeds the
physical plane coordinates into the full real radical ring
`Q(sqrt(3),sqrt(5),sqrt(11))`, and squares coordinate differences directly.
It compares **all 256,183 labelled pair distances**, all strict edges,
source connectedness and supplied colours. For both saturation witnesses
it independently computes the local colours using `alpha=1+2 omega`
and tests all 576 pairs of colour permutations, then checks a triangle
and the positive three-colouring. These are separate author
implementations, not external review or formal verification.

The trust boundary is the accepted base-field embedding, exact archived
source coordinates, the unformalized algebra and valuation arguments,
and ordinary Python integer/Fraction execution. No solver, floating-point
distance test, unresolved computation or private input is required.
No novelty priority is claimed for local colouring or residue arguments.
Related primary context: Madore,
[The Hadwiger-Nelson problem over certain fields](https://arxiv.org/abs/1509.07023).
The record reference is Parts,
[Graph minimization](https://arxiv.org/abs/2010.12665).
[Haugland's August 2026 introduction](https://arxiv.org/html/2608.04542v4),
checked 2026-09-05, still identifies the 509-vertex benchmark. This work
does not improve it.
