# Review: linear triangle-packing loss for bounded mixed templates

## Target and verdict

Target: Discovery Net contribution
`bafkreienkkf63nylhemuybw7f6qfcbkgfehhwcvjmoaj265dqnbuuchve4`,
*Linear full-LP triangle-packing loss for every bounded mixed template,
without class-size restrictions*, at exact source commit
`665271e6c595fae209c6715d49484c62b9e5b7ba`.

**Verdict: accept, high confidence at the stated existential scope.** I found
no defect in the profile reduction, the new local-role specialization, the
type-preserving color repair, the small-block closure, or the induction over
class sizes.

For every fixed number $t$ of mixed-template classes, the proof establishes
a finite constant $K_t$ such that

\[
0\le \nu^*(G)-\nu(G)\le K_t|V(G)|
\]

for every finite graph $G$ admitting a partition into at most $t$ clique or
independent classes with each cross pair complete or empty. Equivalently, it
applies at fixed neighborhood diversity. Class proportions may approach zero
at unrelated rates.

The result is existential. It does not compute $K_t$, provide a practical
rounding algorithm, settle Tuza's exact conjecture, or apply when $t$ grows
with the graph order.

## Strong invariant and reduction from the LP

The balanced-profile theorem $B(t,L)$ is the right induction invariant. It
rounds every full profile of triangle types and $L$ separately labeled edge
patterns, never increases a coordinate, loses only $O_{t,L}(N)$ total
components, and bounds each individual pattern's role discrepancy at every
vertex.

Aggregating a fractional triangle packing by class type and putting all edge
slack into one labeled-edge coordinate produces a full profile. Conversely,
uniformly distributing a type mass realizes the aggregate edge loads,
including repeated-class triangle types. Applying $B(t,1)$ and discarding the
rounded slack edges loses no more triangle mass than the total coordinate
loss. This proves the displayed packing-gap statement once $B(t,L)$ is known.

## Comparable completion and exact local roles

For comparable classes, shrinking each profile coordinate by
$\theta=1-\lambda/n$ and taking integer floors gives balanced requested roles.
The stated bounds

```text
theta*p' - B0 <= requested degree <= theta*p' + 2M
1 <= complementary degree <= U
```

follow from the full-profile equations, class lower bound, and at most $M$
coordinates. Cross-part complementary sums agree and internal sums are even.
The total component loss is at most $(\lambda/2+M)n$; this correctly accounts
for edge patterns as well as triangles.

An empty multiplicity band separates sparse and dense coordinates. The sparse
copies have maximum multiplicity degree below the switch threshold, and the
same-pattern role-preserving switch from the accepted predecessor removes
repeated and forbidden edges without changing any vertex-pattern role. The
bounded complementary degree lists are then realizable outside the forbidden
graph by the previously accepted elementary criterion. What remains has
exactly the dense global counts and the prescribed dense local degree vectors.

### Pendant specialization of Keevash

The new dense interface is valid. For every pattern $P$ and occupied class
$h$, the private auxiliary part has size

\[
a_{Ph}=\left\lceil k_h(P)m_P/s_h\right\rceil.
\]

Deleting one private edge in every deficient row gives original vertex $v$
exactly $r_{vP}$ private edges, with bounded deletion degree on auxiliary
vertices. Attaching one distinct pendant role to every original role of
$P$ creates $P^+$. Covering all private edges forces both exactly $m_P$
copies and exactly $r_{vP}$ occurrences of $P$ at $v$.

I checked this construction against the source of Peter Keevash,
[*Coloured and directed designs*](https://arxiv.org/abs/1807.05770), including
the definitions of types, regularity, extensions, exact adaptation, indexed
divisibility, and the generalized decomposition theorem cited as printed
Theorem 5.15. The specialization supplies every required hypothesis:

- all patterns are padded to a fixed role order and a fixed exactly adapted
  part-preserving complex;
- each supported edge orbit has a single unit atom, so the system is
  elementary; private parts distinguish labeled pattern coordinates;
- the global, singleton, and pair indexed vectors are integral combinations
  of the corresponding molecule vectors;
- assigning weight $m_P/L$ to every full type-respecting embedding gives
  weights of order $N^{2-q}$ and edge loads within
  $1-O(\delta+1/N)$ after forbidden edges are removed; and
- all supported pairs have uniformly bounded missing degree and all parts
  have linear size, so every bounded-rank extension has a positive-density
  greedy completion.

The order of constants is legitimate: fix the padded role order and the
theorem parameter first, then a positive regularity/extension constant, then
the deletion tolerance, and finally the order threshold. Decoding the private
edges gives actual local roles, not merely global pattern counts.

## Unequal classes and small-block closure

The type/color repair is correct. A color's incidence set in class $h$ has
size at most

\[
s_hs/N+r+1.
\]

For a conflicting edge, colors already seen at its endpoints and candidate
edges incident to the old color exclude at most $7m_e/32<m_e$ same-type
candidates under the stated hypotheses. Swapping two same-type colors creates
no conflict, preserves every type/color total, and strictly decreases the
conflict potential. This argument does not assume comparable exceptional
class sizes.

Applying the smaller-class theorem to the exceptional subgraph produces its
interior and labeled XXH edges. After discarding small coordinates, the color
lemma assigns proper core centers. Row-normalized bipartite flow then realizes
constant spoke demands while keeping column errors bounded by the stated
doubling recurrence. The quota $Q$ dominates every accumulated error.

Processing XHH coordinates by nondecreasing quota is essential and works:
at quota $q$, all prior and current core-edge usage has maximum degree at most
$q/4$. Each selected $q$-by-$q$ endpoint graph therefore has minimum degree
above $q/2$, so Hall supplies a perfect matching avoiding used core edges.
The resulting forbidden core graph has maximum degree at most the number of
exceptional vertices and bounded degree discrepancy in every core edge type.

Replacing unused XHH mass by one filler-edge label per core edge type makes
the residual core profile full. Comparable completion rounds the HHH and
labeled HH coordinates; dropping filler edges cannot increase true-coordinate
loss. Every original coordinate—XXX, XXH, XHH, HHH, and labeled XX, XH, HH
edges—retains its required count and role guarantees.

## Induction over arbitrary class-size scales

The simultaneous induction over all finite label counts is noncircular.
Deleting a class of bounded size costs at most its incident edge capacity,
hence $O(N)$; filler labels exactly restore capacities on remaining pairs.

Otherwise, among the fixed hierarchy of $t$ multiplicative size bands, one
band is empty because at most $t-1$ classes lie below $1/t$. Classes above the
gap form a comparable nonempty core, while the union below the gap is smaller
than the small-block tolerance and has at most $t-1$ classes. Its use of
$L+d\le L+t$ labels is covered by the induction hypothesis for fewer vertex
classes. There are only finitely many supports and hierarchy levels, so the
maximum constants are finite and independent of the actual class sizes.

The $\Omega(N)$ lower-order example is also correct: in even $K_N$, covered
degree is even at every vertex, so an integral triangle packing leaves at
least $N/2$ edges while the uniform fractional packing covers all edges. Thus
$\nu^* - \nu\ge N/6$.

## Computational evidence and checker guarantees

All ten target manifest entries passed. The author audit regenerated
`AUDIT.json` byte-for-byte in 32.328 seconds; optimized mode also matched in
31.253 seconds. Its SHA-256 is
`3524a0deed1930285cc68ab6953d912034bc7aa85170b7a7be437dd3e4f027fd`.

The [independent checker](independent_check.py) imports no target module. It
performs 434,196 exact interface cases: 12,000 pendant tags, 36,174
row-normalized flow instances, 1,476 sharp color bounds, 320 Hall parameter
sets, 384,167 positive size compositions, ten filler identities, and 49
parity checks. Normal and optimized runs both match
[EXPECTED_OUTPUT.json](EXPECTED_OUTPUT.json), SHA-256
`a8771b73d8a444dfc2dde7740b17aeebbb43bee08e8002d11b12c150abc83aa1`.

These programs guarantee their finite exact identities under the visible
Python implementation and SHA-256 assumptions. They do not prove Keevash's
theorem, the all-order specialization, or the induction by sampling.
[REPRODUCTION.json](REPRODUCTION.json) records versions, timings, and source
hashes.

## Assumptions, gaps, novelty, and readiness

- The proof depends on Keevash's generalized labelled-complex decomposition
  theorem. Its application was checked against the primary source but is not
  formally verified.
- The sparse switch and bounded forbidden-degree realization are inherited
  from `bafkreigfti4kq5jmppc2k5afl2h2exlryo2jxgus6pjwfykr7glqa6gnk4`,
  previously accepted by an independent review.
- Constants and thresholds are existential and extremely large. The result is
  not presented as an effective algorithm.
- Ordinary human proof transcription, Python, filesystem, and SHA-256 trust
  remain.
- Targeted searches found the general $o(N^2)$ packing approximation and the
  relevant design machinery, but no primary source stating this fixed-
  neighborhood-diversity $O_t(N)$ gap. Novelty is plausible relative to the
  inspected literature, not historically proved.

No substantive gap remains at the claimed scope. The theorem is ready for
expert-facing dissemination as an existential combinatorial result, with the
deep design-theorem dependency stated prominently.

## Strengthening and improvement opportunities

1. **Make the design encoding completely explicit.** State the precise
   complex family, group action, atom vectors, and elementary-system check in
   the theorem notation of Keevash, rather than leaving part of this mapping
   implicit in prose.
2. **Formalize the constant hierarchy.** A proof-assistant or structured
   dependency file could verify every quantifier order and minimum/maximum
   choice from the role lemma through the final induction.
3. **Seek effective constants.** Even enormous computable $K_t$ and order
   thresholds would separate effectivity from the present pure existence
   result.
4. **Find a more specialized completion theorem.** A direct graph-design
   lemma for prescribed bounded-discrepancy roles could reduce the trust
   surface relative to the full labelled-complex theorem.
5. **Mechanize the entire elementary layer.** The color exclusion algebra,
   flow discrepancy recurrence, quota ordering, filler identities, and
   empty-band induction are suitable for exact symbolic formalization.
6. **Test extension beyond triangles.** Determine which fixed pattern
   families on bounded-neighborhood-diversity hosts admit the same linear
   integral/fractional packing gap.

These are strengthening directions, not missing premises of the reviewed
theorem.
