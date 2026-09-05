# A cross four-cycle forces four-colorability of two connected E-gadgets

Let

\[
E=\mathbb Q(i\sqrt3,i\sqrt{11}),\qquad
R=\mathbb Q(\sqrt{33}).
\]

These are subsets of the complex and real planes in the specified embeddings.
The four-coordinate notation is
`(a,b,c,d)=a+b sqrt(33)+c i sqrt(3)+d i sqrt(11)`.
In particular, `E` is the restricted complex field, not a larger Cartesian
coordinate field.

**Theorem.** Let `P,Q subset E` have connected unit-distance graphs, and let
`g` be any Euclidean isometry. Suppose there are distinct `p_0,p_1 in P`
and `q_0,q_1 in Q` such that the four points
`p_0,p_1,g(q_0),g(q_1)` are distinct and all four distances
`|p_i-g(q_j)|` are one. Then the strict unit-distance graph on
`P union g(Q)` is four-colorable.

There is no cardinality, denominator, or disjointness restriction. It is
enough that each source set has a connected spanning graph of unit edges.
The connectedness hypothesis supplies the local integrality used below.

For the fixed 292-vertex inner union `B=A union ((5+i sqrt(11))/6)A`, with
`A=v159e646`, and the 214-vertex gadget `V=v214e977`, this closes **every
placement with a cross four-cycle**, including every disjoint 506-vertex
such placement. No five-chromatic graph is produced. A non-four-colorable
composition of these two gadgets must have a cross graph containing no
four-cycle.

## 1. The local arithmetic supplied by the field coloring

We use the embedding from the previously proved
[whole-field four-coloring](../hadwiger_nelson_nonmono_field_obstruction/PROOF.md).
Here are the precise properties required.

Let `r in Z_2` satisfy `r^2=33`, with `r=1 mod 8`. Let `omega` satisfy
`omega^2+omega+1=0` in the unramified quadratic extension `U` of `Q_2`.
With `alpha=i sqrt(3)` and `beta=i sqrt(11)`, set

\[
\iota(\alpha)=1+2\omega,\qquad
\iota(\beta)=(r/3)(1+2\omega),\qquad
\iota(\sqrt{33})=r.
\]

This is an injective field map. Complex conjugation corresponds to
`omega -> omega^2`, with `r` fixed. For `z=A+B omega`, its conjugate norm is

\[
N(z)=A^2-AB+B^2.
\]

Write `O=Z_2[omega]`. For nonzero `z`, the elementary norm calculation in
the cited proof gives

\[
v_2(N(z))=2\min(v_2(A),v_2(B)).
\]

In particular, an element of norm one is in `O` and has nonzero residue
in `O/2O=F_4`. Reduction modulo two on `O` will be denoted by `res`.
For every `z in O`, the parity of `N(z)` is zero when `res(z)=0`, and one
otherwise. The three elements `1,omega,omega^2` have norm one and their
residues are exactly the three nonzero elements of `F_4`.

If the unit-distance graph of `P` is connected, every `p-p_0` maps into
`O`: follow a unit-edge path and add its integral differences. The same
holds for `Q`. Thus each component occupies one additive coset of `O`
after applying `iota`. Only these differences and the integral expressions
specified below are reduced modulo two. No residue homomorphism on the
whole characteristic-zero field is being assumed.

## 2. The four-cycle supplies midpoints and a quadratic

An orientation-reversing isometry is handled by replacing `Q` with its
complex conjugate, which remains a connected subset of `E`. We may write
`g(z)=u z+h`, with `|u|=1`. Put

\[
d=p_1-p_0,\quad e=q_1-q_0,\quad
m=(p_0+p_1)/2,\quad n=(q_0+q_1)/2.
\]

The two distinct points `g(q_0),g(q_1)` are the intersections of the unit
circles about `p_0,p_1`. They are symmetric about `m`, so

\[
g(z)=m+u(z-n),\qquad
\operatorname{Re}(\overline d\,u e)=0.
\]

Equivalently, the midpoint relation and perpendicularity give

\[
|d|^2+|e|^2=4,\qquad
u^2=W:=-\frac{d\overline e}{\overline d e}\in E.
\]

Both `d,e` are nonzero. If `u in E`, then `h=m-un in E`, and the prior
whole-field coloring already colors the entire union.

Assume now `u not in E`. Its minimal polynomial over `E` is `X^2-W`.
For any cross edge, write `x=p-m` and `y=q-n`. Multiplication of
`|x-u y|^2=1` by `u` gives

\[
c u^2-Su+\overline c=0,
\qquad c=\overline x y,\qquad S=|x|^2+|y|^2-1.
\]

After substituting `u^2=W`, linear independence of `1,u` over `E` forces
`S=0`. This remains valid when `x=0` or `y=0`. Therefore **every cross edge**,
not just the original four, satisfies the radial identity

\[
|p-m|^2+|q-n|^2=1. \tag{1}
\]

All overlaps in this branch occur at the common midpoint. Indeed, an
identity `p-m=u(q-n)` with `q!=n` would put `u` in `E`; otherwise both sides
are zero.

The rest of the argument colors a graph containing all pairs satisfying
(1), so it does not need to enumerate the remaining cross edges.

## 3. Even diagonals

Apply `iota`, suppressing it in the local notation. The vectors `d,e` are
in `O` by connectedness, and `N(d)+N(e)=4`. Their residues are either both
zero or both nonzero, because the norm of a nonzero `F_4` element is one.

First suppose `d,e in 2O`. Since `m=p_0+d/2` and `n=q_0+e/2`, all the
centered component points `p-m` and `q-n` are in `O`. Assign colors

\[
C_P(p)=\operatorname{res}(p-m),\qquad
C_Q(g(q))=\operatorname{res}(q-n).
\]

Every internal unit edge has a difference of norm one and hence a nonzero
residue, so its endpoints have different colors. On a cross edge, (1)
reduces modulo two to

\[
N(\operatorname{res}(p-m))+N(\operatorname{res}(q-n))=1.
\]

Exactly one of these residues is zero and the other is nonzero. Thus the
cross edge is properly colored. If the midpoint belongs to both components,
both prescriptions give it color zero, so the coloring is well-defined.

## 4. Unit diagonals

Now `d,e` have nonzero residues. For every `p in P,q in Q`, put

\[
X_p=2(p-m),\qquad Y_q=2(q-n).
\]

These are in `O`, and their residues are the fixed nonzero values
`res(d)` and `res(e)` respectively. Choose the unique
`rho in {1,omega,omega^2}` such that

\[
\operatorname{res}(\rho e)=\operatorname{res}(d).
\]

Both `X_p+d` and `rho Y_q+d` belong to `2O`. Define

\[
C_P(p)=\operatorname{res}\left(\frac{X_p+d}{2}\right),\qquad
C_Q(g(q))=\operatorname{res}\left(\frac{\rho Y_q+d}{2}\right). \tag{2}
\]

The first expression is `res(p-p_0)`. Differences of the second expression
are `res(rho(q-q'))`. Since `rho` has norm one, internal unit edges in both
components are properly colored.

Suppose the endpoints of a cross edge had equal colors. Equation (2) would
give `X_p-rho Y_q in 4O`. Taking norms and using `N(rho)=1` gives

\[
N(X_p)\equiv N(Y_q)\pmod4.
\]

But (1) gives `N(X_p)+N(Y_q)=4`, so `2N(Y_q)=0 mod 4`, contradicting the
odd norm of `Y_q`, whose residue is nonzero. Every cross edge is therefore
properly colored.

There is no overlap in this branch: a midpoint in `P` would give `X_p=0`,
whereas every `X_p` has nonzero residue. The same argument applies to `Q`.
This completes the proof of the theorem, using only congruences modulo two
and four. No assertion about the chromatic number of all of `E(u)` is needed.

## 5. An explicit arithmetic recipe

`verify.py` implements these two colorings. The earlier field module computes
`r=sqrt(33)` to the required binary precision. For an element
`(a+b sqrt(33)+c alpha+d beta)/D`, it computes the two coordinates in
`U=Q_2+Q_2 omega` modulo `2^k`, accounting for powers of two in `D` before
reducing. It rejects a request to reduce a nonintegral element.

In the unit case only the three lifts `(1,0)`, `(0,1)` and `(3,3)` modulo
four are needed for `rho`. They represent `1,omega,omega^2`. A color is the
two-bit value `A+2B` for residue `A+B omega`. Division by two in (2) is
performed on an even pair modulo four, giving a pair modulo two.

`audit.py` checks the complete finite congruence argument directly:

- There are six ordered pairs of elements of `F_4` whose norms sum to one;
  all have different entries.
- There are 216 choices of units `X,Y in (Z/4)[omega]` and one of the three
  lifts `rho`, with `N(X)+N(Y)=0 mod 4`. Every choice has `X!=rho Y`.

These finite checks validate the small-ring calculations. The uniform
geometric reduction and connectedness argument are the proof in Sections
1–4, not conclusions inferred from these tables.

## 6. Exact calibration on the mixed506 construction

The pinned coordinate tables reconstruct the connected component graphs
`B` (292 vertices, 1,251 edges) and `V` (214 vertices, 977 edges). Every
possible seed four-cycle must use a pair of component diagonals whose
squared lengths sum to four. The exact diagonal census is:

| Rotation-root branch | Complementary squared-length pairs | Unordered diagonal-pair choices |
|---|---:|---:|
| Roots in `E` | 26 | 2,551,052 |
| Roots outside `E` | 51 | 1,748,914 |
| Total | 77 | 4,299,966 |

The two norm supports have 1,056 and 372 distinct values. The square test
for the branch is whether `|d|^2 |e|^2/3` is a square in `R`: this is
necessary and sufficient for the perpendicular rotation to lie in `E`.
The test includes no approximate distance or angle. These are labeled
segment-pair counts, not numbers of distinct placements or graphs.

For each of the 51 outside-field squared-length types, the program chooses
one exact pair of diagonals. There are 43 cases of unit diagonals and eight
of even diagonals. In these source types every possible diagonal midpoint
is external to its component; the generator checks this by exact membership
for every contributing component pair. In particular, the selected cases
are disjoint 506-vertex placements. Their complete cross-edge counts are
four in 28 cases, five in 17, six in four, nine in one, and ten in one.
Both quadratic roots are covered by the same algebraic edge identities.

The generator computes every cross edge in the selected cases by the
radial identity and perpendicularity, checks the coloring on every internal
and cross edge, and records compact hashes in `calibration.json`. It also
checks a five-vertex midpoint-overlap control for the stronger local-coset
version of the coloring lemma. That control does not assert connectedness
of its three-point component sets.

A separate audit reconstructs `B` using a generic real-radical complex
multiplication, checks the square classification with rational field
arithmetic, and computes the auxiliary colorings using exact `E` coordinates
and the earlier whole-field coloring function. It then represents every
point as `A+B u`, `A,B in E`, with `u^2=W`, and tests every pair by multiplying
out the conjugate norm in this quadratic algebra. Each norm has a constant
and a linear coefficient; it is one exactly when both required identities
hold. The irreducible polynomial makes the calculation valid for both roots.

This full pair traversal checks `51*binomial(506,2)=6,516,015` pairs, matches
every selected edge stream and coloring hash, and confirms every proper
coloring. These 51 examples calibrate the implementation. The theorem closes
the whole four-cycle family by the uniform proof, not by treating the
selected examples as an exhaustive placement search.

## 7. Scope and provenance

The source coordinate [provenance](../hadwiger_nelson_nonmono159_214_lowden2/SOURCE.md)
and [fixed inner union](../hadwiger_nelson_nonmono159_moser_triple/PROOF.md)
are reused. The preceding [single-hub reduction](../hadwiger_nelson_mixed506_single_hub_reduction/PROOF.md)
suggested studying the remaining cross four-cycles. Combined with that
result, a non-four-colorable disjoint mixed506 placement must have a
four-cycle-free cross graph and at most one hub, of degree at most ten.
For a placement with no hub, its nontrivial cross components are paths and
even cycles of length at least six. These remaining possibilities are open.

The local residue mechanism is classical and the base-field implementation
has its own published proof and review. No priority claim is made for the
modular coloring method. For related field-coloring context see Madore,
[The Hadwiger–Nelson problem over certain fields](https://arxiv.org/abs/1509.07023).
The result here concerns compositions of connected subsets of the specified
`E`; no larger Cartesian-field chromatic bound is asserted.

Primary construction source: Parts,
[Graph minimization](https://arxiv.org/abs/2010.12665).
[Haugland's August 2026 introduction](https://arxiv.org/html/2608.04542v4),
checked on 2026-09-05, retains the 509-vertex benchmark. The present theorem
produces neither a five-chromatic graph nor a record improvement.

Trust rests in the unformalized geometric and local-arithmetic arguments,
the pinned coordinate inputs and dependencies, exact Python arithmetic and
ordinary execution. The programs are author cross-checks using different
representations, not external peer review or proof-assistant formalization.
No solver verdict, floating-point distance, root approximation or omitted
large certificate is used.
