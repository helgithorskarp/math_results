# Locally integral quadratic traces obstruct two-gadget constructions

Let `E=Q(i sqrt(3),i sqrt(11))`, with its specified complex embedding, and
let `R=Q(sqrt(33))` be its real subfield. Use the accepted embedding
`iota:E -> U=Q_2(omega)`, where `omega^2+omega+1=0`, which commutes with
complex conjugation. Put `O=Z_2[omega]`. “Locally integral” below always
refers to this fixed embedding (the branch `sqrt(33)=1 mod 8`).

**Theorem.** Let `u` be a unit complex number of degree two over `E`, with
minimal polynomial

\[
Z^2-TZ+J\in E[Z].
\]

Suppose `iota(T) in O`. For any connected unit-distance source graphs
`P,Q subset E` and any `h in E(u)`, the entire strict unit-distance graph
on `P union (u Q+h)` is four-colourable. Reflections are included by
conjugating the second source. No cross cycle, denominator bound,
cardinality bound or disjointness is assumed.

There is a stronger conclusion when `iota(T)` is a local unit:

**Unit-trace field theorem.** If `iota(T) in O^*`, the embedding extends
compatibly with complex conjugation to `E(u) -> U`. The strict unit-distance
graph on the whole of `E(u)` has chromatic number exactly four. This part
needs no source connectedness or two-copy restriction.

Here `T` is the **relative algebraic trace over E**, not necessarily the
complex trace `u+bar(u)`. The theorem contains the prior
[trace-zero gluing theorem](../hadwiger_nelson_trace_zero_gluing/PROOF.md)
as `T=0`, and now includes nonzero traces of every nonnegative local
valuation. Traces of negative local valuation and translations outside
`E(u)` are not closed by this statement. No field-wide four-colouring is
asserted merely from `T in 2O`.

For the fixed connected alternative `B292/V214` construction, every
placement in the stated stratum is therefore four-colourable, including
disjoint 506-vertex placements. No five-chromatic graph is produced.

## 1. Arithmetic and the self-reciprocal minimal polynomial

The prior [field theorem](../hadwiger_nelson_nonmono_field_obstruction/PROOF.md)
supplies the following facts. For `z=A+B omega in U`,

\[
N(z)=z\overline z=A^2-AB+B^2,
\qquad v_2(N(z))=2v(z),
\quad v(z)=\min(v_2(A),v_2(B)). \tag{1}
\]

Consequently a unit Euclidean displacement in `E` maps to an element of
`O` with nonzero residue in `F_4=O/2O`. A connected source graph occupies
one additive `O`-coset: add its integral unit-edge displacements along a
path. The three nonzero elements of `F_4` have norm one, and zero has norm
zero. Conjugation induces the Frobenius automorphism on `F_4`.

Since `bar(u)=1/u`, conjugating the minimal polynomial and taking its
reciprocal gives another monic quadratic vanishing at `u`:

\[
Z^2-\frac{\overline T}{\overline J}Z+\frac1{\overline J}.
\]

Minimality forces

\[
J\overline J=1,\qquad T=J\overline T. \tag{2}
\]

In particular `J` is a local unit by (1), and if `T!=0`, then
`J=T/bar(T)`. These identities are valid for non-real traces as well.

Because `[E(u):E]=2`, there are unique `m,n in E` with `h=m-u n`.
Thus the isometry is `g(z)=m+u(z-n)`. For any cross unit edge, put
`x=p-m`, `y=q-n`, `c=bar(x)y` and `S=N(x)+N(y)-1`. Multiplying the distance
condition by `u` gives `cu^2-Su+bar(c)=0`. Reduction modulo the minimal
polynomial yields

\[
cT=S,\qquad \overline c=Jc. \tag{3}
\]

The first equation is the new quadratic cross identity

\[
q_T(x,y):=N(x)+N(y)-T\overline x y=1. \tag{4}
\]

Although `q_T` need not be real on arbitrary arguments, (4) is an identity
in `E` on every actual cross edge. The proof may colour the larger graph
of all pairs satisfying (4). No division by `x` or `y` is involved.

## 2. Even local trace: two-coset gluing

Assume `iota(T) in 2O`, including `T=0`. Suppress `iota` in local formulas.
The centred source sets occupy two additive `O`-cosets. We prove the
slightly stronger lemma that any two such cosets' internal unit graphs,
with any cross edges satisfying (4), glue to four colours. Zero copies
may be identified if zero is in both sets.

If there are no cross edges, colour each coset by residues of differences
from a chosen point, aligning the zero copies by colour permutation if
needed. Empty sources are immediate. Otherwise choose a cross-edge anchor
`(x_0,y_0)`.

If either anchor has negative valuation, both have the same negative
valuation. To see this, suppose `a=v(x_0)<v(y_0)=b`, with `a<0`. The three
terms on the left side of (4) have valuations

\[
2a,\quad 2b,\quad v(T)+a+b,
\]

with the last term absent if `T=0`. Because `v(T)>=1`, the first is the
unique smallest valuation. Their sum cannot have valuation zero. The
case with the roles reversed is identical. Zero endpoints, whose
valuation is infinite, cause no exception. Thus either both anchors are
integral, or `v(x_0)=v(y_0)=-k` for some integer `k>=1`.

### Integral anchor branch

Both source cosets are then integral. Assign `C_P(x)=res(x)` and
`C_Q(y)=res(y)`. Internal unit edges have nonzero residue differences.
On a cross edge (4) reduces to `N(res(x))+N(res(y))=1`, since `T in 2O`.
Exactly one residue is zero, so the cross edge is proper. Both zero
copies receive colour zero.

### Nonintegral anchor branch: every depth k

Put `X_0=2^k x_0`, `Y_0=2^k y_0`, with nonzero residues `a,b in F_4`.
All points in each source coset have valuation `-k`, so neither contains
zero. For a further cross edge write `x=x_0+z`, `y=y_0+w`, with `z,w in O`.
Subtract the two versions of (4) and multiply by `2^k`. With the local
conjugate trace `Tr(t)=t+bar(t)`, the exact identity is

\[
\begin{split}
0={}&\operatorname{Tr}(\overline{X_0}z)
+\operatorname{Tr}(\overline{Y_0}w)
-T(\overline{X_0}w+\overline zY_0)\\
&+2^k\big(N(z)+N(w)-T\overline z w\big).
\end{split} \tag{5}
\]

Every term is integral. Since `T in 2O` and `k>=1`, reduction modulo two
removes all but the two trace terms. Writing
`L_a(v)=tr_(F4/F2)(bar(a)v)`, we obtain

\[
L_a(\operatorname{res}(z))=L_b(\operatorname{res}(w)). \tag{6}
\]

These are nonzero binary linear functionals. Choose

\[
\lambda=\frac{\overline b}{\overline a},\qquad
L_a(t)=1,
\]

and set

\[
C_P(x)=\operatorname{res}(x-x_0),\qquad
C_Q(y)=\lambda\operatorname{res}(y-y_0)+t. \tag{7}
\]

Multiplication by `lambda!=0` preserves distinct residue colours on
internal unit edges. Since `L_a(lambda v)=L_b(v)`, equal colours on a
cross edge would turn (6) into an equality differing by one. This is
impossible. The argument holds for every `k>=1`, without a denominator
cutoff; checking sample depths is not the proof.

An overlap in the actual isometric union can only be the common centre:
`p-m=u(q-n)` with `q!=n` would put `u` in `E`. Thus the zero identification
handled above is the only one required, and the colouring is proper on
the entire strict plane graph. This completes the even-trace branch.

## 3. Unit local trace: a compatible whole-field embedding

Assume now `iota(T) in O^*`. From (2), substituting `w=u/T` into the
minimal polynomial gives

\[
w^2-w+\frac1{N(T)}=0. \tag{8}
\]

Under the fixed embedding, `N(T)` is an odd element of `Z_2`, because
it lies in the real subfield and has valuation zero. The polynomial (8)
therefore has coefficients in `Z_2` and reduces modulo two to
`Z^2+Z+1`. Its two roots in `F_4` are `omega` and `omega^2`, both simple.

Each lifts uniquely to a root in `O`. Explicitly, if a root `w_j` is known
modulo `2^j`, write `w_(j+1)=w_j+2^j delta`. Since the derivative
`2w_j-1` is a unit reducing to one, the equation modulo `2^(j+1)` determines
one and only one `delta in F_4`. These compatible finite roots converge in
the complete ring `O`, giving a root `w_*` with either chosen nonzero
residue. This is the elementary Hensel step, not an assumption that a
root inferred from finite precision is already exact.

Conjugation fixes the coefficients of (8) and exchanges its two residue
roots. The uniqueness of each lift consequently gives

\[
\overline{w_*}=1-w_*,\qquad
N(w_*)=\frac1{N(T)}. \tag{9}
\]

Set `u_*=iota(T) w_*`. Then `u_*` is a root of the image of the minimal
polynomial, and `N(u_*)=1`. Sending `u` to `u_*` extends `iota` to a field
embedding `tilde(iota):E(u) -> U`: the irreducible minimal polynomial is the kernel
relation, and a nonzero field homomorphism is injective. Conjugation
commutes with this extension because it does so on `E` and

\[
\overline{u_*}=1/u_* = \widetilde\iota(\overline u).
\]

For any `z in E(u)` write its image as `A+B omega`, with `A,B in Q_2`.
Colour `z` by the two coefficients of `2^0` in the binary expansions of
`A` and `B`, as in the accepted field theorem. If `|z-z'|=1`, compatible
conjugation and (1) imply that both local coordinate differences are
integral and at least one is odd. Their zero-th digits therefore differ.
This works on the whole field, including points outside `O`; it is not a
ring homomorphism from a characteristic-zero field to `F_4`.

The upper bound is four. The lower bound is four because `E(u)` contains
`E`, which contains the Moser spindle. Thus its chromatic number is exactly
four. In particular every union in the theorem is coloured. The two
local trace cases exhaust `T in O`, proving the main theorem.

## 4. Why the two branches must be distinguished

The exact control `u=(2+i sqrt(5))/3` has irreducible minimal polynomial
`Z^2-(4/3)Z+1` over `E`. Its relative trace has local valuation two, so
Section 2 closes **all** centred two-source placements with translation
in `E(u)`, not just the path example that suggested studying this case.

However, this particular extension cannot embed in `U` compatibly with
conjugation. Indeed, if `z in U` has norm one, then either its residue is
`omega` or `omega^2`, making `Tr(z)` odd, or its residue is one. In the
latter case write `z=1+2w`; the norm equation gives `Tr(w)=-2N(w)`, hence

\[
\operatorname{Tr}(z)=2-4N(w)=2\pmod4.
\]

Thus a norm-one element of `U` never has conjugate trace divisible by
four. A compatible image of the control rotation would have norm one
and conjugate trace `4/3`, which is zero modulo four, a contradiction.
This is an obstruction to this particular embedding method, not a claim
that the extension needs five colours.

Conversely, the unit-trace control `u=(1+i sqrt(35))/6` has relative trace
`1/3`. The points `x=1`, `u y=u/3` have unit separation, but both source
anchors `1` and `1/3` have residue one. Plain centred residue colouring
therefore collides on this edge. The unit-trace embedding colours it
properly. One cannot merely drop the even-trace assumption from the
centred-residue argument.

The non-real-trace controls multiply rotations by
`rho=(-1+i sqrt(3))/2`; their minimal polynomials have trace `rho T`
and constant `rho^2`. They check that the general statement is about
relative trace, not only real coefficients with `J=1`.

## 5. Exact evidence, scope and provenance

`check_algebra.py` verifies both coefficient identities in the generic
scaled expansion (5) using an exact sparse polynomial ring. It independently
enumerates all 49,152 candidate roots for the 192 unit traces in
`(Z/16)[omega]`, matching all 384 roots against the two lifted constructions.
Nine odd normalized constants are also lifted compatibly through 32 bits,
checking the polynomial and conjugate-branch identities at every precision.
The local norm-one trace obstruction is checked modulo four. These finite
checks supplement the arbitrary-precision proof above.

`examples.py` checks thirteen exact geometries: connected wheel pairs,
three disjoint mixed506 placements, a six-point local-coset path, a common
centre, a no-cross-edge control, and two 49-point grids in the whole
unit-trace extension. Negative centred depths one through three and
non-real relative traces are included. The path's sources are not asserted
connected; they satisfy the stronger local-coset lemma directly. Both grid
examples use mixed points `A+B u`, beyond the two-source form, and one has
nonintegral coefficient offsets.

A separate `audit_examples.py` imports neither the new arithmetic nor the
generator. It rebuilds the source gadgets using generic real-radical
coordinates and obtains distances by dot and signed-area formulas. Every
one of the 386,299 labelled pair distances, all strict edges and all
supplied colours are checked. These are independent author implementations,
not external peer review or a formal verification of the infinite theorem.

The [uniform cycle result](../hadwiger_nelson_cross_cycle_forest/PROOF.md)
locates the earlier forest frontier; the current proof does not depend on
its acceptance. General forests are still open. The theorem excludes the
locally integral quadratic-trace stratum with translations in `E(u)`,
not all quadratic or higher-degree rotations and not all translations.
Neither the sealed Parts pool nor the parked Parts L/S census is enumerated.

The [archived source coordinates](../hadwiger_nelson_nonmono159_214_lowden2/SOURCE.md)
and [fixed inner construction](../hadwiger_nelson_nonmono159_moser_triple/PROOF.md)
are unchanged. Field-colouring and Hensel lifting are classical methods;
no novelty priority is claimed. Related primary context: Madore,
[The Hadwiger–Nelson problem over certain fields](https://arxiv.org/abs/1509.07023).
Record source: Parts, [Graph minimization](https://arxiv.org/abs/2010.12665).
[Haugland's August 2026 introduction](https://arxiv.org/html/2608.04542v4),
checked on 2026-09-05, retains the 509-vertex benchmark. No five-chromatic
unit-distance graph with at most 508 vertices has been established.
