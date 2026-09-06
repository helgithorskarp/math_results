# A realized regular phase obstruction with a four-colourable actual kernel

**Construction-family theorem.** The three-variable obstruction in the
[accepted four-clause classification](../hadwiger_nelson_paired_circle_four_clauses/README.md)
is geometrically realizable by two planar unit segments. An explicit
continuous one-parameter family has four distinct centres, no cross-centre
distance in `{0,1,sqrt(3),2}`, and exactly six mixed circle-intersection points.
Its four clauses form two opposite forcing pairs on one shared variable.

The family also defeats **independently chosen A/B orbit phases** and, more
strongly, every colouring satisfying the earlier paired-circle kernel's
owner-group lists and four distinct centre pins. A four-edge path proves this
list obstruction without a solver.

**Exact separation witness.** One member lies in the real quartic field
`Q(eta)`, where `eta=sqrt(2 sqrt(3))` and `eta^4=12`. Its actual paired-circle
kernel has **74 vertices and 198 unit edges**, and has a verified ordinary
four-colouring extending those same four distinct centre pins. Thus the
obstruction is to the prescribed lists and phase methods. The ordinary
four-colouring violates those lists and is not a certificate colouring the
full infinite circle support.

**Transfer lemma.** For every regular paired-circle placement (all cross
separations avoid 1 and 2), allowing arbitrary independent orbit phases in
the two palettes gives no additional feasible placements beyond the
complement-coupled phases. This follows from the two classified clause
obstructions and their bipartite double covers.

No five-chromatic graph on at most 508 vertices is established. Full-support
four-colourability of this newly realized family remains unclassified here.
The result settles geometric realizability of the **three-variable** pattern;
it does not classify every realization or settle the two-variable pattern.

## 1. A family built from two equilateral completions

Let
\[
 \omega=(1+i\sqrt3)/2,\qquad \zeta=\omega^2=(-1+i\sqrt3)/2,
 \qquad U=\{\omega^k:0\le k<6\}.
\]
Take unit complex numbers `y,z` satisfying
\[
 |1-\zeta+y+z|=1,\qquad [1]_U,[y]_U,[z]_U
 \text{ pairwise distinct}.                                  \tag{1}
\]
Define
\[
 a_0=0,\quad a_1=\zeta^2,\qquad
 b_0=-1-y,\quad b_1=-\zeta+z.                                \tag{2}
\]
The A segment has length one. The B segment has vector
`u=1-zeta+y+z`, so it also has length one.

Put `p=-1` and `q=-zeta`. These are the two equilateral completions of the
unit segment `0,zeta^2`. The complete cross-circle intersections are

| Centre pair | First root | Second root |
| --- | --- | --- |
| `a0,b0` | `p` | `-y` |
| `a1,b0` | `p` | `zeta^2-y` |
| `a0,b1` | `q` | `z` |
| `a1,b1` | `q` | `zeta^2+z` |

For example, `p-a0=-1`, `p-a1=zeta`, and `p-b0=y` are unit directions.
Likewise `q-a0=-zeta`, `q-a1=1`, and `q-b1=-z` are unit directions.
The second root is `ai+bj` minus the first; its distances to both centres
are also one. Distinct unit circles have at most two intersections, so this
is a complete list after the distinctness checks below.

Every cross-centre displacement is a difference of one direction from the
orbit of 1 and one from the orbit of `y` or `z`. Two unit directions have chord length in `0,1,sqrt(3),2` if and only if
they belong to the same `U`-orbit. Condition (1) therefore
implies that the four cross distances belong to
\[
 (0,2)\setminus\{1,\sqrt3\}.                                \tag{3}
\]
In particular all four centres are distinct, every cross pair has two distinct
roots, and no mixed point is a centre.

The six named mixed points
\[
 p,q,-y,\zeta^2-y,z,\zeta^2+z                                \tag{4}
\]
are distinct. Coincidence of `p` or `q` with one of the other four would put
`y` or `z` in `U`. A coincidence between `i zeta^2-y` and `j zeta^2+z`,
where `i,j` are 0 or 1, would give
\[
 y+z\in\{0,\zeta^2,-\zeta^2\}.
\]
For unit `y,z`, a zero sum makes them antipodal, and a sum of modulus one
makes their angle difference `+/-120` degrees. Both imply equal `U`-orbits,
contrary to (1). Within either two-point translate, the points are separated
by the unit vector `zeta^2`.

It follows from the complete table that `p` has exactly owners `a0,a1,b0`,
`q` has exactly owners `a0,a1,b1`, and each of the other four points has
one A owner and one B owner. This handles all multiple ownership explicitly.
The construction uses the classical unit diamond; no novelty is claimed for
its equilateral geometry. The assertions concern its realized circle-support
phase and list obstructions.

## 2. Actual clauses and the stronger path obstruction

Pin the four centre colours to
\[
 (c(a_0),c(a_1),c(b_0),c(b_1))=(2,3,0,1).                     \tag{5}
\]
Use `1,y,z` as the three cross-orbit representatives, with Boolean phases
`H,Y,Z`. The earlier construction uses A phase `X` and B phase `1-X`.
At a mixed root with directions `omega^k v` and `omega^l w` in slot `(i,j)`,
its clause is
\[
 (X_v=1+i+j+k)\lor(X_w=i+j+l),                              \tag{6}
\]
with values modulo two.

Substituting the first roots in the table gives

| Slot | Direction from A | Direction from B | Clause |
| --- | --- | --- | --- |
| `00` | `-1` | `y` | `(H=0) or (Y=0)` |
| `10` | `zeta` | `y` | `(H=0) or (Y=1)` |
| `01` | `-zeta` | `-z` | `(H=1) or (Z=0)` |
| `11` | `1` | `-z` | `(H=1) or (Z=1)` |

The second root in each slot gives the same clause, by the two-intersection
identity in the parent theorem. The first two clauses force `H=0`; the other
two force `H=1`. This is the three-variable forcing-pair pattern, with genuinely
distinct geometric direction orbits, not a formal assignment of unrelated
Boolean labels.

There is a stronger direct obstruction to the old owner-group lists.
Those lists assign colours `{0,1}` to A-only noncentres, `{2,3}` to B-only
noncentres, all four colours to mixed points, and pins (5) to the centres.
The owners of `p` force `c(p)=1`; those of `q` force `c(q)=0`.
But the five points
\[
 p=-1,\quad \zeta,\quad -\zeta^2,\quad 1,\quad q=-\zeta    \tag{7}
\]
form a four-edge unit path on the circle at `a0`. Its three internal points
have exactly owner `a0`: the only common points of the A circles are `p,q`,
and (4) lists every point with a B owner. The other mixed points have A
relative directions in the distinct `y` and `z` orbits.

Thus every point on (7) must use colours 0 and 1. Alternation along an even
path forces its endpoints to have the same colour, contradicting their two
forced values. Every point of (7) belongs to the intrinsic A direction orbit
and hence to the earlier actual kernel. This proves that **no proper colouring
of that kernel satisfies the old lists**, for every parameter satisfying (1).
It also excludes any such list colouring of the whole infinite support.

Arbitrary independently chosen orbit phases still produce these owner-palette
lists. They therefore cannot repair this family. The obstruction does not
assume complementary phases, constant choices at mixed points, or a solver's
negative answer.

## 3. Nonempty continuous parameter range and an exact quartic member

Let `eta` be the positive real root of `T^4-12`, so
`eta^2=2 sqrt(3)`. Set
\[
 u_*=(\sqrt3-i)/2,\qquad
 y_*=\frac{u_*}{2}(1-\sqrt3+i\eta),\quad
 z_*=\frac{u_*}{2}(1-\sqrt3-i\eta).                          \tag{8}
\]
Since `(1-sqrt(3))^2+eta^2=4`, both `y_*` and `z_*` are unit directions.
Their sum is `(1-sqrt(3))u_*`, and
`1-zeta=sqrt(3)u_*`, so `1-zeta+y_*+z_*=u_*` is unit as required.

The polynomial `T^4-12` is Eisenstein at 3 and irreducible over the rationals.
The coordinates
\[
\begin{split}
 \Re y_*&=-\tfrac34+\tfrac14\eta+\tfrac18\eta^2,\qquad
 \Re z_*=-\tfrac34-\tfrac14\eta+\tfrac18\eta^2,\\
 \Im y_*&=-\tfrac14+\tfrac18\eta^2+\tfrac18\eta^3,\qquad
 \Im z_*=-\tfrac14+\tfrac18\eta^2-\tfrac18\eta^3
\end{split}
\]
show that neither belongs to `U`, whose coordinate field is contained in
`Q(sqrt(3))=Q(eta^2)`. Also
\[
 \Re(y_*/z_*)=1-\sqrt3\in(-1,-1/2),
\]
which is not the real part of any element of `U`. Thus all three orbits in
(1) are distinct. This proves nonemptiness exactly.

For an explicit continuous family, let
\[
 u_\theta=e^{i\theta},\quad s_\theta=u_\theta-1+\zeta,
\]
and, wherever `0<|s_theta|<2`, put
\[
\begin{split}
 y_\theta&=\frac{s_\theta}{2}
       -i\frac{s_\theta}{|s_\theta|}\sqrt{1-|s_\theta|^2/4},\\
 z_\theta&=\frac{s_\theta}{2}
       +i\frac{s_\theta}{|s_\theta|}\sqrt{1-|s_\theta|^2/4}.
\end{split}                                                   \tag{9}
\]
These are unit directions summing to `s_theta`; hence their B segment has
unit vector `u_theta`. At `theta=-pi/6`, (9) gives exactly (8), and
`|s_theta|=sqrt(3)-1` lies strictly between 0 and 2. The finitely many excluded
orbit equalities remain false in a sufficiently small open neighbourhood,
by continuity. Thus the admissible parameter set contains an open interval.
This is an existence proof of a continuous family, not a claim that an
unspecified sample exhausts a parameter interval. No numerical endpoint or
maximal parameter interval is claimed.

For (8), the four cross squared distances in order `00,01,10,11` are
\[
 (q_+,q_+,q_-,q_-),\qquad
 q_\pm=(1+\sqrt3\pm\eta)/2.                                \tag{10}
\]
They satisfy (3), as follows already from the unit directions and orbit
separation. The exact checker additionally compares these field expressions
and verifies two distinct intersections for every slot.

## 4. Independent phases do not enlarge the regular feasible family

This statement concerns all regular placements of two unit segments, not only
(2). A regular placement has four distinct centres and no cross separation 1
or 2. Use the same direction representatives for both groups, but now give
A arbitrary phases `A_v` and B arbitrary phases `B_v`. Write `C_v=1-B_v`.

If one complement-coupled clause is
\[
 (X_v=p)\lor(X_w=q),
\]
the independent-phase conditions at the two cross roots are
\[
 (A_v=p)\lor(C_w=q),\qquad
 (A_w=q)\lor(C_v=p).                                        \tag{11}
\]
This is the bipartite double cover of the signed clause. At a tautological
base clause, (11) may impose a relation between its two copied variables,
but it is satisfied whenever `A_v=C_v`; it is not silently dropped when
reasoning about the independent system.

If the coupled formula is satisfiable, set `A=C=X` and obtain an independent
solution. Conversely, suppose the coupled formula is unsatisfiable. By the
[accepted four-clause theorem](../hadwiger_nelson_paired_circle_four_clauses/README.md),
regularity forces exactly four proper binary clauses with one of the two
classified support patterns: a single pair of variables, or a hub and two
leaves. Both support graphs are bipartite.

For either bipartition `S,T`, the variables `A_S,C_T` in (11) form one copy of
the original signed formula, while `C_S,A_T` form another. Both copies are
unsatisfiable. Therefore the independent system is unsatisfiable as well.
We have proved exact equality of the feasible placements for the two phase
procedures throughout the regular family.

This lemma does not handle unit/tangent cross distances, assert that every
arbitrary graph colouring uses orbit phases, or make the kernel lists
necessary for graph colourability. The explicit path (7) supplies the stronger
list obstruction for family (2), independently of this double-cover argument.

## 5. A positive colouring of the actual 74-point kernel

For (8), construct the earlier kernel as follows. In each group include the
six rotations of its segment direction and all six rotations of the
owner-relative cross-intersection directions. Translate that direction set
by both centres in the group, then take the union of the two patches.

The exact direction sets have sizes 18 and 24. Within each group, its two
translates overlap precisely in its two equilateral completions. The patches
therefore have 34 and 46 points, overlapping in the six mixed points. Their union has **74 distinct
points and 198 unit edges**. The [certificate](certificate.json) stores a
proper four-colouring with centre colours `(2,3,0,1)`. Its canonical streams
have hashes

```text
points: 5cf77673a80f4c571fb405c8ace8cf7dde1b84c4e9d62718c9bb7083018aa0d9
edges:  5a8c522eecb9dd9a5702fb94fd857a8bb472db2dddc8ca57a97e1ee3cfc54464
```

The deterministic producer found this positive colouring in 75 backtracking
nodes. The checker validates every edge directly and does not trust the
search. The displayed colouring has 20 vertices outside their old owner-group
lists. That is consistent with the proved list impossibility.

This is a concrete distinction between **list feasibility** and ordinary
four-colourability on the same actual kernel, even with the same centre pins.
The kernel's previous extension theorem requires the lists. Therefore this
ordinary colouring does **not** establish four-colourability of the entire
infinite circle support. No chromatic lower bound, smallest witness, or
criticality claim is made for this kernel.

## 6. Exact reproduction and independent verification

The [producer](build.py) uses coefficient vectors in `1,eta,eta^2,eta^3`,
reducing polynomial products by `eta^4=12`. The
[checker](verify.py) imports no producer or parent executable. It uses the
quadratic tower
\[
 \mathbb Q(\sqrt3)[\eta]/(\eta^2-2\sqrt3),
\]
storing `A+eta B`, with `A,B` represented as rational pairs in `Q(sqrt(3))`.
This supplies a separate arithmetic decomposition.

The checker derives the exact parameter (8), unit segments and all 18 orbit
exclusions. For each cross pair it checks two distinct supplied roots at
unit distance from both centres; the at-most-two-intersections theorem then
certifies completeness without repeating the producer's second-root formula.
It reconstructs the six mixed points, all direction sets, points, lists and
unit edges. It also checks:

| Audit | Count |
| --- | ---: |
| Actual point-pair squared norms | 2,701 |
| Unit-edge inequalities in the positive colouring | 198 |
| Root unit-distance checks | 16 |
| Direct independent-phase root truth checks | 512 |
| Direct complement-coupled root truth checks | 64 |
| Edges in the explicit list-obstruction path | 4 |
| Malformed certificates rejected | 9 |

The truth checks evaluate actual potential colours against centre pins,
independently of the symbolic clause derivation. All 64 independent-phase
assignments and all eight coupled assignments fail, but the exact path proof
already establishes the stronger list failure without relying on enumeration.
For the general transfer lemma, the checker separately tests the double covers
of both abstract obstruction forms over 16 and 64 assignments. Both have zero
models; deleting either pair of lifted clauses corresponding to one original
clause restores respectively one or four models for each of the four deletions.

The nine rejection controls alter a root count, exact parameter, coupled clause,
independent clause, even path, kernel lists, ordinary colouring, graph hash,
and full-support claim flag. Checks raise explicit errors and survive `-O`.

The certificate has **1,935 bytes**, SHA-256

```text
e21c45ca9ebf3bb33c2ed4d74c24a1c69188ff5c29c50cc4c19532863a79b207
```

Python 3.11 or later and its standard library suffice. From this directory,
choose fresh output directories:

```sh
sha256sum -c SHA256SUMS
python3 build.py --out work/build
python3 verify.py --out work/check
python3 -O verify.py --out work/check-optimized
```

The producer must reproduce the certificate byte for byte. Normal and optimized
verification must match [expected.json](expected.json). Execution and context
are recorded in [validation.json](validation.json). No native solver, CAS,
floating-point premise, external coordinate file or omitted large artifact is
needed. The public positive search is bounded by its fixed 74-point instance;
its output is checked rather than used as a negative decision procedure.

The full family, continuity statement, list-path argument and general
independent-phase transfer remain written mathematics. The checker establishes
the exact example and finite identities, not a numerical inference of those
universal claims. Trust remains in those arguments, the accepted parent
classification for Section 4, quartic irreducibility, Python exact arithmetic,
canonical encoding and ordinary hardware. This is author-run algorithmic
verification. External review of this new result is pending; no priority claim
or proof-assistant formalization is claimed.

## 7. Campaign boundary

The realization question posed by the
[independent review](../hadwiger_nelson_paired_circle_four_clauses_review1/README.md)
is now answered positively for the three-variable pattern. Its most immediate
repair—allowing independent A/B orbit phases—cannot work, even for other
regular placements. The old kernel lists also fail on the entire new family,
while the exact 74-point kernel is ordinarily four-colourable.

This is useful negative evidence about a construction method. No actual
five-chromatic obstruction is supplied and the full supports in this family
remain unclassified. The two-variable pattern, other placements realizing the
three-variable pattern, unit/tangent boundaries, and possible full-support
repairs are outside this completed milestone. No larger search or changed
geometric mechanism has begun.

The shared-midpoint family remains closed and now has
[independent acceptance](../hadwiger_nelson_shared_midpoint_review1/README.md).
The teammate's [bounded H560 decision](../hadwiger_nelson_heule560_global_decision/README.md)
and [independent review](../hadwiger_nelson_heule560_global_decision_review1/README.md)
were inspected as coordination context, not mathematical dependencies. Its
516-vertex critical support and remaining selector family were not duplicated.

The target baseline remains
[Parts's 509-vertex construction](https://arxiv.org/abs/2010.12665), also
identified as the record in [Haugland's August 2026 manuscript](https://arxiv.org/html/2608.04542v4).
Both primary sources were checked live on 6 September 2026. Targeted searches
for paired-circle phase/palette formulations supplied no matching antecedent;
this limited search is not a priority proof. This pass ends at the exact
realization, list obstruction and positive finite-kernel separation.
