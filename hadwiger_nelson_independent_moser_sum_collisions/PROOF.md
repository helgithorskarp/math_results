# Coincidences in an independently rotated three-spindle sum

Put `alpha=i sqrt(3)`, `beta=i sqrt(11)`, `F=Q(sqrt(33))`, and
`E=F(alpha)=Q(alpha,beta)` in their displayed complex embeddings. Let

\[
\rho=(1+\alpha)/2,\quad\eta=(5+\beta)/6,\qquad
M=\{0,1,\rho,1+\rho,\eta,\eta\rho,\eta(1+\rho)\}.
\]

For arbitrary complex numbers `u,v` with `|u|=|v|=1`, take the **set**

\[
S(u,v)=M+uM+vM.
\]

Its graph has one vertex per distinct plane point and **all** pairs at
Euclidean distance exactly one as edges.

**Computer-assisted theorem.** If the map
`M^3 -> S(u,v)`, `(a,b,c) -> a+ub+vc`, is not injective, the strict
unit-distance graph on `S(u,v)` is exactly four-chromatic.

Consequently, any five-chromatic member of this architecture must have
all 343 formal sums distinct. This is a necessary condition within this
construction, not a lower bound for plane unit-distance graphs. The
injective 343-point family remains open here. No graph improving the
509-vertex incumbent is obtained.

## 1. Base arithmetic and local colouring

Write elements of E as `a+b sqrt(33)+c alpha+d beta` with rational
coefficients. Since `alpha beta=-sqrt(33)`, the exact norm is

\[
N(z)=a^2+33b^2+3c^2+11d^2+2(ab+cd)\sqrt{33}.
\]

The [accepted base-field argument](../hadwiger_nelson_nonmono_field_obstruction/PROOF.md)
uses the embedding into `U=Q_2(omega)`, `omega^2+omega+1=0`, given by
`alpha=1+2 omega`, the 2-adic branch `sqrt(33)=1 mod 8`, and
`beta=alpha sqrt(33)/3`. Conjugation commutes with this embedding.
For `O=Z_2[omega]`, with valuation normalized by `nu(2)=1`,

\[
\nu(N(z))=2\nu(z),\qquad O/2O=\mathbb F_4.
\]

Unit displacements are integral with nonzero residue. Colouring by the
zero-th binary digits of the two U-coordinates properly colours the
whole of E. More generally the same works on any field with a compatible
embedding into U. On O the colour is simply its residue in `F_4`.
These are colours of points, not a homomorphism from the field to `F_4`.

The set M has seven distinct vertices and eleven unit edges. The verifier
exhausts its 2,187 three-colour assignments (none proper) and finds a proper
four-colouring. It also checks `lambda conjugate(M)=M` for
`lambda=eta rho`. Every S contains M because `0 in M`, so all upper
bounds below are equalities. Since the source is connected and contains
zero, its points lie in O. Any unit `u in E` is in O, hence `M+uM subset O`.

## 2. Three nonzero differences: a finite exact envelope

A coincidence of addresses gives

\[
a+ub+vc=0,\qquad a,b,c\in M-M.
\]

There cannot be exactly one nonzero difference. Suppose first that all
three differences are nonzero. The set D of such differences has size 34,
and its norm set has size seven. For `A=N(a)`, `B=N(b)`, `C=N(c)`, put

\[
H=A+B-C,\quad \Delta=4AB-H^2,\quad s=\Delta/3.
\]

If `x=-ub/a` and `y=-vc/a`, then `x+y=1`, `N(x)=B/A`, and `N(y)=C/A`.
Taking real parts gives the exhaustive solutions

\[
x=\frac{H\pm\alpha\sqrt{s}}{2A},\qquad
u=-\frac{ax}{b},\qquad v=-\frac{a(1-x)}c. \tag{1}
\]

If `Delta<0` there is no physical solution. If it is zero
there is one; otherwise there are two. The verifier checks the norm-one
and coincidence identities in exact arithmetic, not with numerical
root tolerances. It iterates all `34^3=39,304` difference triples.

If `sqrt(s) in F`, both rotations lie in E and the base-field result
applies. Otherwise `s` is positive in the specified real embedding and
`E(sqrt(s))` has degree two over E. Indeed a positive real F-element
which is a square in E is already a square in F: writing a square root
as `r+t alpha` forces `rt=0`, and the other possibility gives a
nonpositive physical square. Two positive nonsquare radicands define the
same extension exactly when their ratio is a square in F. The generator
uses this test to deduplicate fields and then exact tuples to deduplicate
ordered phase pairs. It does not quotient away unproved symmetries.

The complete census is:

| Quantity | Count |
|---|---:|
| Positive / zero / negative norm triples | 238 / 6 / 99 |
| Nonphysical difference triples | 5,760 |
| Labelled roots in E / outside E | 53,504 / 13,248 |
| Distinct ordered phase pairs in E / outside E | 1,716 / 6,528 |
| Positive nonsquare radicands / quadratic extensions | 32 / 31 |
| Outside-E pairs with compatible local field embedding | 3,024 |
| Remaining outside-E pairs with checked positive colouring | 3,504 |

For the local filter, `s` is a square in `Q_2` exactly when its valuation
is even and its odd unit is `1 mod 8`. Such a square root is fixed by
local conjugation, so adjoining it extends the embedding compatibly.
The test uses exact rational coefficients and successively lifted roots
of 33. Precision is increased until the valuation and three unit bits
are determined; it is not a numerical cutoff. The other 3,504 supports
have 340--342 distinct points. All their complete unit graphs receive
explicit colourings checked after identifying equal points.

## 3. Two nonzero differences: finitely many lines of phases

If precisely two differences are nonzero, permute the three summands
and apply a global unit scaling. The support then has the form

\[
B+vM,\qquad B=M+uM,\qquad
u=-a/b\in E,\quad a,b\in D,\quad N(a)=N(b). \tag{2}
\]

The third unit phase v is still arbitrary. There are exactly 30 such u.
Conjugating and then multiplying by `lambda=eta rho` sends the support
to `M+bar(u)M+bar(v)M`. Thus 16 representatives modulo conjugation suffice,
with no restriction on v. The 16 sets B have 26--47 vertices, and their
sums have at most 329 physical points. As above, `B,M subset O`.

If `v in E`, the support is already coloured by the base-field result.
For `v outside E`, the pair map `B x M -> B+vM` is injective: any equality
with a nonzero M-difference would imply `v in E`. Edges having zero
difference in one factor are Cartesian edges and can always be coloured
by `res(B) + res(M)` in `F_4`.

An additional edge has differences `a in (B-B)\{0}` and `b in D` and
satisfies `N(a+vb)=1`. Since `bar(v)=1/v`, multiplying by v gives

\[
c v^2+S v+\bar c=0,\quad
c=\bar a b,\quad S=N(a)+N(b)-1. \tag{3}
\]

Thus any additional edge outside E forces an irreducible quadratic

\[
v^2-Tv+J=0,\qquad T=-S/c,\quad J=\bar c/c. \tag{4}
\]

Conversely its two distinct physical unit roots exist exactly when
`Delta=4N(a)N(b)-S^2>0` and `sqrt(Delta/3) notin F`. They are

\[
v=T/2\ \pm\ \frac{\alpha}{2c}\sqrt{\Delta/3}. \tag{5}
\]

The verifier checks both norm identities and both polynomial identities.
Every outside-E unit-contact equation is degree two, so it vanishes at
one root of (4) exactly when its monic polynomial equals (4). The two
physical roots therefore have the **same complete edge graph**. Grouping
all ordered difference pairs by the exact `(T,J)` key is exhaustive.
Phases with no such extra contact have only Cartesian edges, even if
they are transcendental or have higher algebraic degree.

## 4. A local filter for integral Minkowski factors

The following argument applies to any `B,M subset O`, not just these
spindles. For an outside-E quadratic unit v, expanding (3) modulo its
minimal polynomial gives, on every mixed unit edge,

\[
N(a)+N(b)+T\bar a b=1. \tag{6}
\]

If `T=0` or `nu(T)>=1`, reduction modulo two shows that exactly one of a,b
has nonzero residue. Their residue sum is therefore nonzero.

If `nu(T)=-1`, both a,b being local units would make the third term of
(6) have the unique negative valuation. If both are nonunits, every term
on the left has positive valuation. Both possibilities are impossible;
again exactly one is a unit. Thus the same sum of residues is a proper
colouring, including the Cartesian edges. Because v is outside E,
representations of points are unique and this colour is well defined.

If `nu(T)=0`, use the
[unit-trace field theorem](../hadwiger_nelson_integral_trace_gluing/PROOF.md).
For completeness, the unit-root minimal polynomial satisfies
`J bar(J)=1` and `T=J bar(T)`. Setting `w=v/T` gives
`w^2-w+1/N(T)=0`. Since `N(T)` is odd, its two simple residue roots in
`F_4` lift to conjugate roots in O. Multiplying by T extends the embedding
to `E(v)` and preserves norm one and conjugation. The whole field,
including B+vM, is consequently four-colourable.

This leaves only the finite contact quadratics with `nu(T)<=-2`.
The valuation is intrinsic to `(T,J)`; excluding all other valuations
before grouping cannot lose a direction belonging to a retained key.
The code computes `nu(T)=nu(S)-(nu(N(a))+nu(N(b)))/2` exactly.
No theorem closing all negative-trace fields is being asserted.

## 5. Finite certificates and geometric independence

The 16 representative two-factor collisions yield **5,064** retained
irreducible contact quadratics. Both roots of each are physical, hence
these represent 10,128 labelled root cases; different u or quadratics
are not asserted inequivalent under all isometries. Every graph is
four-coloured. Its exact Cartesian edges plus all contact directions
with the same key agree with the direct all-pairs plane geometry.

All explicit colour words use the original 343 addresses in product
order, `49i+7j+k`. Each word must descend to physical points: all addresses
for the same point receive the same colour. Every strict edge is then
checked. The certificate has 483 shared words and assigns one to every retained
three-factor phase pair and every retained two-factor quadratic. The
verifier regenerates their entire inventories; there are no unlisted
solver timeouts or excluded exceptions.

The native checker obtains the metric in two ways. Its first formula
expands the E-norm of `z0+z1 sqrt(s)`. The second writes the actual real
coordinate in `F(sqrt(s))` and the imaginary coordinate as `sqrt(3)`
times another element of that real field, and tests `x^2+y^2=1` in its
four-dimensional basis. It compares every unit-edge list. This is a
separate derivation of the metric, sharing exact coordinate generation;
it is an author audit, not external peer review or fully independent
input provenance. All accepted integer inputs have absolute numerator,
common denominator and radicand numerator/denominator at most `10^9`.
The displayed degree-three integer expressions are bounded by `2^110`,
well inside signed 128-bit range. No floating-point distance is used.

Trust remains in the unformalized reductions and local field arguments,
the completeness of the exact Python enumeration, ordinary Python/C++
execution and the compiler. SAT produced positive witnesses during
exploration; the published replay does not use or trust a SAT solver.
All coordinate data derive from the seven displayed source points.
Raw root inventories, solver logs and built binaries are not required
public inputs and are not committed.

## 6. Relation to the record lane

The earlier [correlated family](../hadwiger_nelson_correlated_moser_cube/README.md)
proved `M+uM+u^2 M` four-colourable and explicitly left two independent
rotations open. This result treats a different locus in that open
family: every coincidence, without imposing `v=u^2`. It does not claim
to close the independent family. The local arguments reuse earlier
field and trace mathematics, including the
[first negative-trace boundary](../hadwiger_nelson_first_negative_trace/PROOF.md).
Minkowski sums and local-field colourings themselves are established
methods; no priority claim is made for them.

An all-three-factor coincidence would have supplied at most 342 vertices,
beating 509 by at least 167 if it were non-four-colourable. A two-factor
coincidence would have supplied at most 329. These exact supports failed
that test. The useful next question is whether *injective* independent
phases can accumulate mixed contacts that defeat four-colouring, or
whether a structural product colouring closes that larger family.
Running further searches on the collision locus is now unnecessary.

The graph refresh also found the reviewed
[complex-radix collision theorem](../hadwiger_nelson_radix_collision_residues/PROOF.md).
It concerns a single radix with Eisenstein-integral digits and gives three
colours under a monic degree-four hypothesis. It does not imply this theorem:
M already needs four colours, and eta has algebraic trace `5/3`, so is not
an algebraic integer. The present support also has two free unit phases.
That result is related collision-locus methodology, not a closed host reused
here or a prerequisite of the current computation.
