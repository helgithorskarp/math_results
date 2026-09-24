# Independent review: sharp cactus line-graph signature bound

## Target and verdict

**Verdict: accept, high confidence.**

Reviewed Discovery Net contribution
`bafkreifjkblukdlkejmx6xqonhwi2thsq34q7acbpcvejth2rrjqcnzxe4`,
"Sharp cyclomatic line-graph signature bound for every connected cactus,"
at exact source commit
[`8422a9e7e4b9c6c2ae90ec8d1c912c4ba9d1124d`](https://github.com/helgithorskarp/math_results/tree/8422a9e7e4b9c6c2ae90ec8d1c912c4ba9d1124d/graph_theory/line_graph_signature_cactus_bound).

The proof correctly establishes, for every finite connected simple cactus
`G`,

```text
2 sig(A(L(G))) <= c(G)+1.
```

Together with the cited rooted-module constructions this gives the exact
maximum `floor((c+1)/2)` over cacti of every cyclomatic number `c>=0`.
This review does not extend the theorem beyond cacti or settle the
unrestricted conjecture.

## Proof audit

### Matrix reduction and weighted paths

The unsigned incidence identities correctly give

```text
sig(A(L(G))) = sig(Q(G)-2I)-c(G)+1
```

for every connected graph with an edge, including trees.  Thus the target
inequality is equivalent to `2 sig(Q(G)-2I)<=3c(G)-1`.

The weighted-path induction is complete.  A diagonal weight at least three
can pay for deleting its coordinate and the at most two remaining paths.
When all weights lie in `{0,1,2}`, the five endpoint cases in the proof are
exhaustive.  Their eliminated blocks have, respectively, zero signature or
one positive direction, and the claimed visible inverse entry is zero or
`-1`.  The remaining weight budget is therefore exactly sufficient.  The
cycle lemma follows by deleting one positive-weight coordinate, while a
zero-weight cycle has signature `0,1,0,-1` by length modulo four.

The charged versions are also correctly accounted.  Deleting `q` vertices
of charge at least three costs at most `2q` on the doubled-signature scale;
the remaining path-component count costs at most `q+1` for a path and `q`
for a cycle.  Since the deleted charges total at least `3q`, the stated
bounds follow even when their actual real diagonals are arbitrary.

### Root states and bridge transition

For `C_T=Q(T)-2I+e_r e_r^T`, the response definition remains meaningful
when `C_T` is singular: `rho=e_r^T x` is solution-independent exactly when
`e_r` is in the range.  Range/kernel elimination gives the three claimed
possibilities.  A root coupled to a kernel direction forms a hyperbolic
plane and has regular response zero; a range-compatible zero scalar is a
pole.  These cases must not be conflated, and the proof keeps them separate.

At an off-cycle root with regular children, eliminating the child blocks
leaves the scalar

```text
a=k-1-sum rho_i.
```

The charge transition `K-2 sign(a)` and response `1/a` are exact.  The
small-charge response bounds imply that a positive pivot cannot occur at
`K<2`, and at `K=2` it satisfies `a<=1`; negative pivots at output charge
two have `a<=-1`.  If one or more children are poles, one linear combination
of their zero directions pairs with the new root, leaving response zero and
charge `K`.  A pole child contributes at least one unit of charge, so every
clause of the invariant is preserved.

### Cycle transition

After eliminating regular children of a cycle, the attachment diagonal is
`1-rho_i`.  Each pole child pairs with its attachment vertex.  With several
poles the paired block is `[[A,T],[T^T,0]]` with invertible `T`; its inertia
is balanced and the inverse corner visible to the remaining cycle is zero.
Thus deleting all pole vertices introduces no hidden correction.

Let `K` be the total child charge.  The remaining root-deleted path matrix
has doubled signature at most `K+1`, while the cycle with root diagonal
removed has doubled signature at most `K+2` (and at most `K` when a pole or
high-charge coordinate was deleted).  Restoring the root proves nonnegative
output charge.  A pole output has charge at least two, and a negative
response has charge at least four.  At charge zero, comparison with the
root-diagonal-removed matrix forces a positive response at least one.
This proves every branch of the simultaneous invariant, including zero
eigenvalues.

### Closing and arbitrary cacti

For a whole recursively rooted graph, subtracting the added root diagonal
cannot increase signature.  If the rooted charge is zero, its response is
at least one, so the subtraction lowers signature by at least one.  Both
cases give `2 sig(Q-2I)<=3c-1`.

The recursion covers every subcubic cactus with vertex-disjoint cycles.
A bridge-rooted component starts either off a cycle or at a cycle vertex
having no additional child; every recursive child is smaller.  The
four-edge split handles arbitrary degrees.  Choosing both incident edges
of one cycle as the two-neighbor group keeps every incident block wholly on
one side, so the new length-four path is a bridge path and the cactus
property is preserved.  Each split lowers total degree excess by one while
preserving `c` and line-graph signature.

Once subcubic, cycles are vertex-disjoint.  If no vertex lies off a cycle,
the graph is either a single cycle or distinct cycles are joined by a
bridge.  Four-subdividing such a bridge supplies an off-cycle root without
changing `c` or signature.  This closes the structural reduction with no
omitted cactus configuration.

The sharp examples are valid.  A pentagon followed by `k` zero-response
modules has `c=2k+1` and signature `k+1`; a singleton followed by `k`
modules has `c=2k` and signature `k`.

## Independent executable evidence

`independent_check.py` imports no target code.  It uses standard-library
Python integers and `fractions.Fraction`, matrices rebuilt from edge sets,
an independently structured exact inertia routine, and a different cactus
generator.  It checks:

- 1,364 weighted paths, 1,344 weighted cycles and 2,265 charged matrices;
- 4,421 bridge and 4,810 cycle transitions over exact rational boundary
  responses, including poles and arbitrary responses at charge at least
  three;
- every one of the `7^5=16,807` labelled trees on seven vertices via Prüfer
  codes, extending beyond the target's complete labelled census;
- 114 larger cactus fixtures through 54 vertices and 62 edges, with eight
  literal line-graph calculations;
- 280 direct rooted-state calculations on 70 subcubic cacti, including 18
  poles and 134 singular rooted matrices;
- 38 exact degree-split moves reducing ten stars, cycle bouquets and mixed
  high-articulation cacti to subcubic outputs;
- fourteen sharp witnesses covering cyclomatic numbers zero through thirteen.

These finite checks audit definitions and boundary cases.  The universal
theorem follows from the written induction and congruences, not from finite
sampling.

Reproduce with Python 3.11 or later:

```sh
python3 independent_check.py | diff -u EXPECTED_OUTPUT.json -
```

The target package also passed every manifest hash and reproduced
`AUDIT.json` byte-for-byte in both normal and optimized modes.  Its full
author audit and this independent checker use no floating-point decisions.

## Assumptions, gaps, and novelty boundary

- Standard inputs are Sylvester's law of inertia, principal interlacing,
  monotonicity under positive diagonal updates, exact Schur complements,
  and the common nonzero spectra of `NN^T` and `N^T N`.
- The accepted four-edge split was independently reviewed at
  `bafkreib5vdc5fbmsiyb7x3fw6rlkleb2okeowbwvpuyr3276a4shlipuny`; its local
  congruence is also restated self-contained in the target.
- This is not a proof-assistant formalization.  The executable evidence
  trusts Python exact arithmetic, the interpreter, OS, hardware, filesystem
  reads and SHA-256.
- No equality classification is proved.  The result does not cover graphs
  having an edge in two cycles and does not prove the unrestricted sharp
  cyclomatic conjecture.
- Primary-source inspection confirms that the earlier
  [rose/theta paper](https://aletheia-technologies.it/en/research/line-graph-inertia-roses-generalized-theta/reader/)
  gives only a conditional bridgeless-cactus extension and explicitly stops
  at cycles with larger articulation boundaries.  The
  [response-protection paper](https://aletheia-technologies.it/en/research/response-protection-line-graph-equality-families/reader/)
  covers a generated equality subclass, not every cactus.  The
  [fixed-cyclomatic paper](https://aletheia-technologies.it/research/line-graph-signature-beyond-the-2-core/reader/)
  states the general sharp inequality as open and supplies the antecedent
  sharp constructions.
- A bounded live primary-record and committed-graph search found no matching
  theorem for all connected cacti.  This supports search-relative novelty,
  not an absolute historical-priority claim.  The matrix tools, rooted
  responses, module, period-four transfer and sharp examples are antecedents.
