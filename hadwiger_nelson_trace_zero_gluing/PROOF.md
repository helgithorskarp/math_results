# Trace-zero quadratic gluing without a cross cycle

Put `E=Q(i sqrt(3),i sqrt(11))`, `R=Q(sqrt(33))`, and `alpha=i sqrt(3)`.
These are the specified complex and real embeddings. Write `N(z)=z bar(z)`.

**Theorem.** Let `P,Q subset E` have connected unit-distance graphs. Let
`g(z)=u z+h` be a Euclidean isometry, where

- `|u|=1`, `u not in E`, and `u^2 in E`;
- `h in E(u)`.

Then the entire strict unit-distance graph on `P union g(Q)` is
four-colourable. Reflection is included by replacing `Q` with `bar(Q)`.
No cross cycle, vertex-count bound, denominator bound or disjointness
hypothesis is required.

Here “trace zero” refers to the **relative algebraic trace** of `u` in the
quadratic extension `E(u)/E`, not to the complex trace `u+bar(u)`. The
rotation may have nonzero real part. If instead `u in E` and `h in E`,
the prior whole-field colouring applies immediately.

Since `1,u` form an `E`-basis of `E(u)`, the translation condition is exactly
that there are unique `m,n in E` with

\[
g(z)=m+u(z-n). \tag{1}
\]

The earlier [cross-four-cycle theorem](../hadwiger_nelson_cross_four_cycle_gluing/PROOF.md)
obtained (1) and `u^2 in E` from a cycle, then coloured two midpoint valuation
branches. Here the cycle hypothesis is removed, and the local argument covers
arbitrary negative valuations. The new theorem therefore includes acyclic
interfaces not covered by that cycle hypothesis. It does not assert that
all forest interfaces, all quadratic rotations, or all of `E(u)` are
four-colourable.

For the fixed connected `B292/V214` construction, this closes every placement
in the stated rotation/translation stratum, including disjoint 506-vertex
placements with cross forests. No five-chromatic graph or record improvement
is produced.

## 1. Local arithmetic and the coset hypothesis

Use the conjugation-compatible embedding from the accepted
[field-colouring theorem](../hadwiger_nelson_nonmono_field_obstruction/PROOF.md):

\[
\iota:E\hookrightarrow U=\mathbb Q_2(\omega),\qquad
\omega^2+\omega+1=0,
\]

with `alpha -> 1+2 omega` and `sqrt(33) -> r`, where `r^2=33`, `r=1 mod 8`.
Let `O=Z_2[omega]`, and let `res:O -> F_4` be reduction modulo two. This
embedding sends complex conjugation to `omega -> omega^2` and fixes `r`.

For `z=A+B omega`,

\[
N(z)=A^2-AB+B^2,\qquad
v_2(N(z))=2v(z),\quad v(z)=\min(v_2(A),v_2(B)). \tag{2}
\]

The last equality follows by extracting the smaller power of two and
checking the three nonzero binary residue pairs. In particular every unit
Euclidean displacement is in `O` with nonzero residue. On `F_4`,
`N(a)=a^3` is zero for `a=0` and one for every nonzero `a`.

Connectedness of a source graph implies that all its points occupy one
additive coset of `O`: differences along a unit-edge path are integral, so
the endpoint difference is integral. Translation by a field centre does
not affect this assertion. Below we suppress `iota` in the local notation.
Only integral differences or explicitly scaled integral points are reduced;
no residue homomorphism on the whole characteristic-zero field is used.

## 2. A radial gluing lemma for two cosets

**Lemma.** Suppose `X,Y subset E` each occupy one additive `O`-coset under
`iota`. Start with disjoint labelled copies of their internal unit-distance
graphs and add any cross edges `(x,y)` satisfying

\[
N(x)+N(y)=1. \tag{3}
\]

If zero belongs to both sets, its two copies may be identified. The
resulting graph is four-colourable.

The lemma needs only the coset hypothesis; connectedness is one sufficient
way to obtain it. There may be infinitely many points or cross edges.

If there are no cross edges, colour each source by
`res(x-x_*)` relative to any source point and permute the colour names to
align the two zero copies if necessary. An empty source is immediate.
Assume now that there is a cross edge `(x_0,y_0)`.

### Integral anchors

If both `x_0,y_0 in O`, the whole of `X,Y` is integral. Set

\[
C_X(x)=\operatorname{res}(x),\qquad
C_Y(y)=\operatorname{res}(y).
\]

An internal unit edge has a nonzero difference residue, so is proper.
Reducing (3) modulo two gives `N(res(x))+N(res(y))=1`. Exactly one residue
is zero and the other is nonzero, so each cross edge is proper. Both zero
copies receive colour zero.

### Nonintegral anchors: arbitrary depth

If one anchor is nonintegral, both are nonintegral with equal valuation.
Indeed, (2) makes a negative norm valuation an even negative integer. If
`v(x_0)` and `v(y_0)` differed and one were negative, the valuation of
`N(x_0)+N(y_0)` would be their smaller negative norm valuation, contrary to
(3). Thus

\[
v(x_0)=v(y_0)=-k,\qquad k\geq1.
\]

The same valuation holds for every point in each coset. In particular,
neither coset contains zero, so there is no identification to handle.
Put

\[
X_0=2^k x_0,\qquad Y_0=2^k y_0,
\qquad a=\operatorname{res}(X_0),\ b=\operatorname{res}(Y_0),
\]

where `a,b` are nonzero elements of `F_4`.

For any cross edge write `x=x_0+z`, `y=y_0+w`, where `z,w in O`.
Subtract (3) for the anchor edge from (3) for this edge and multiply by
`2^k`. With `Tr(t)=t+bar(t)` in `U`, the exact identity is

\[
\operatorname{Tr}(\overline{X_0}z)
+\operatorname{Tr}(\overline{Y_0}w)
+2^k\big(N(z)+N(w)\big)=0. \tag{4}
\]

Since `k>=1`, reduction modulo two eliminates the last term. If
`tr:F_4 -> F_2` is the binary field trace and
`L_a(v)=tr(bar(a)v)`, then (4) says

\[
L_a(\operatorname{res}(z))=L_b(\operatorname{res}(w)). \tag{5}
\]

Each `L_a` is a nonzero linear functional: multiplication by `bar(a)` is
invertible and `tr(omega)=1`. Choose `t in F_4` with `L_a(t)=1`, and put

\[
\lambda=\frac{\overline b}{\overline a}\ne0,\qquad
C_X(x)=\operatorname{res}(x-x_0),\qquad
C_Y(y)=\lambda\operatorname{res}(y-y_0)+t. \tag{6}
\]

Since `bar(a) lambda=bar(b)`, we have `L_a(lambda v)=L_b(v)`.
Internal edges are proper: their nonzero residue differences remain
nonzero after multiplication by `lambda`. If a cross edge had equal
colours, applying `L_a` to that equality would give

\[
L_a(\operatorname{res}(z))
=L_b(\operatorname{res}(w))+1,
\]

contradicting (5). This proves the lemma for every `k>=1`. There is no
upper bound on the negative depth, and it is not inferred by checking a
finite list of denominators.

## 3. Trace-zero isometries supply the radial identity

Let `W=u^2 in E`. Because `u not in E`, its minimal polynomial over `E` is
`Z^2-W`. For a cross unit edge put `x=p-m`, `y=q-n`, and

\[
c=\overline x y,\qquad S=N(x)+N(y)-1.
\]

Using `bar(u)=1/u`, the distance equation multiplied by `u` is

\[
cu^2-Su+\overline c=0.
\]

Substitution of `u^2=W` and independence of `1,u` over `E` force

\[
S=0,\qquad cW+\overline c=0. \tag{7}
\]

Thus **every cross edge** satisfies (3), including any edge with a centred
endpoint zero. The radial lemma colours a graph containing all the actual
cross edges, so the additional angular condition in (7) causes no problem.
Internal unit edges are unchanged by the isometry.

Any overlap in this non-base branch must be the common centre: if
`p-m=u(q-n)` and `q!=n`, then `u=(p-m)/(q-n) in E`, a contradiction.
Otherwise `p=m`, `q=n`. The radial lemma aligns these zero copies. Its
colouring is consequently well-defined on the actual plane points, and
proper on the entire strict union graph. This proves the theorem.

## 4. Relation to the remaining geometric frontier

The previous [uniform cycle theorem](../hadwiger_nelson_cross_cycle_forest/PROOF.md)
showed that a non-four-colourable disjoint mixed506 placement must have a
cross forest. The current result closes an entire algebraic stratum of
those forests without assuming that arbitrary forest attachments glue.
A remaining candidate must fail the present trace-zero/translation
hypotheses as well as the earlier cyclic-interface criterion.

For example, the non-base rotation `(2+i sqrt(5))/3` in the earlier
six-cycle controls has minimal polynomial `Z^2-(4/3)Z+1` over `E`, whose
relative trace is not zero. The present proof does not settle that branch.
Translations outside `E(u)` are also outside the statement. No next
quadratic-trace or path phase is performed in this package.

The field-colouring mechanism is classical; no novelty priority is claimed.
For related field-colouring context see Madore,
[The Hadwiger–Nelson problem over certain fields](https://arxiv.org/abs/1509.07023).
The specified source field and two-coset hypotheses matter; this is not a
colouring theorem for the larger Cartesian coordinate field.

## 5. Exact checks and trust boundary

The proof above is ordinary unformalized mathematics. The programs calibrate
the arithmetic recipe and geometries; they do not prove a universal theorem
by sampling.

`finite_check.py` exhausts the nine nonzero anchor-residue pairs. For each
pair there are two prescribed affine colour maps and eight allowed cross
residue pairs, giving 18 maps and 144 collision exclusions. A separate
binary-polynomial multiplication and enumeration of all 24 permutations
of the four colours finds four compatible permutations per anchor pair,
36 in total, and confirms that every prescribed map is among them. Six
integral norm-pair cases are checked. Omitting the nonzero trace shift
fails for every anchor pair. A nonintegral residue request is rejected.

`examples.py` checks eleven exact configurations: five pairs of connected
seven-point wheels at local depths 0,1,2,3,4; four disjoint mixed506
placements at depths 0,1,2,3; a common-centre overlap; and a no-cross-edge
control. The complete squared distances, strict edges and prescribed
colourings are computed in the quadratic algebra `E[u]`, `u^2=W`.
All selected cross graphs are star forests; none has a four-cycle on
four distinct physical points. The nine anchored non-overlap examples
have one cross edge each. They calibrate the colour formula, rather than
claiming difficult non-four-colourability tests.

`audit_examples.py` imports neither the generator nor the new colouring
module. It reconstructs the gadgets in a generic real-radical representation,
then computes all distances from real dot and signed area formulas for
the rotation. All 511,697 labelled pair distances, all strict edges and
all supplied colourings are compared, including the single coincident
pair in the overlap example. Cross components are checked as stars by
local degrees, separately from the generator's four-cycle enumeration.
These are independent author implementations, not external peer review.

The [source coordinate provenance](../hadwiger_nelson_nonmono159_214_lowden2/SOURCE.md)
and [fixed inner construction](../hadwiger_nelson_nonmono159_moser_triple/PROOF.md)
are unchanged. Primary record source: Parts,
[Graph minimization](https://arxiv.org/abs/2010.12665).
[Haugland's August 2026 introduction](https://arxiv.org/html/2608.04542v4),
checked on 2026-09-05, retains the 509-vertex benchmark. No five-chromatic
graph with at most 508 vertices has been established. The sealed Parts
pool and parked Parts L/S overlap census are not enumerated here.
