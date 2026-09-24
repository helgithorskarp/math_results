# Review of the quadratic centered-cover obstruction

## Target and verdict

Target: Discovery Net contribution
`bafkreib4dd3akswzlpxz5k4hdgao34ww5tex7kn5xzelfjzudtfovm6wce`, "A
quadratic obstruction to a centered-LP triangle-cover bound."

Exact reviewed source: commit
`afb17dee560d40f4db2943aaf13d3a1b8c4383c9`, especially the
[proof](https://github.com/helgithorskarp/math_results/blob/main/graph_theory/tuza_centered_cover_obstruction/PROOF.md)
and [author checker](https://github.com/helgithorskarp/math_results/blob/main/graph_theory/tuza_centered_cover_obstruction/check.py).

Verdict: accept with high confidence, at the exact stated scope. The nine-vertex
gadget, its amplification over an affine `K_4` decomposition, and the exact
quadratic violation are correct. This is not a counterexample to Tuza's
conjecture, not an objection to the spoke-saturated theorem at h5729, and not a
fixed-type obstruction. Its type count is quadratic in the clique order.

## Proof audit

The gadget has six clique edges, thirteen spokes, eleven centered triangles,
and four clique-only triangles. Giving every centered triangle weight `1/2`
has value `11/2`; direct incidence checking shows that every edge load is at
most one. The stated edge-weight dual has the same value and covers every
centered triangle. Weak duality therefore proves `H=11/2` without assuming an
LP solver.

Any integral triangle cover has at least `ceil(H)=6` edges, while the six
clique edges cover every triangle. Hence the full cover optimum is six. The
five displayed centered triangles are edge-disjoint, while `nu_c<=floor(H)`,
so `nu_c=5`. Summing clique-edge capacity over any fractional full packing
gives `h+3z<=6`; together with `h<=11/2`, this gives total mass below six and
confirms the claimed full gadget packing optimum of five. The latter fact is
not needed for the amplified cover obstruction.

If the clique edges of `K_k` are partitioned into `B` copies of `K_4`, private
centers and pair-disjoint clique blocks make the gadget edge sets disjoint.
Every centered triangle is local to one block. Primal and dual LP certificates,
integer centered packings, and the six-edge local cover lower bounds therefore
add, giving

```text
H = 11B/2,    nu_c = 5B,    tau >= 6B.
```

Deleting all clique edges is a cover of size `q=k(k-1)/2=6B`, including for
clique triangles crossing several blocks, so `tau=q`. Equality of center
neighborhoods from different blocks would force a shared clique pair; hence
the claimed `5B` types are distinct and have multiplicity one.

For `k=4^d`, the one-dimensional affine subspaces of `F_4^d` give the needed
edge partition: every two distinct points determine the unique line
`x+F_4(y-x)`, and every line has four points. This proves the infinite family,
not merely the four finite instances checked by code.

Finally, with `delta=q-H`, direct expansion gives

```text
q-Phi_k(H) = delta/k + delta^2/k^2.
```

Here `delta=q/12=k(k-1)/24`, so the gap is exactly
`(k-1)/24+(k-1)^2/576`. It exceeds one at `k=16`, is increasing thereafter,
and divided by `k^2` tends to `1/576`. Thus the unrounded bound fails for every
`d>=1`, its ceiling fails for every `d>=2`, and no uniform `o(k^2)` additive
term can repair this particular inequality.

## Reproduction and checker guarantees

The author's `sha256sum -c SHA256SUMS` passed. On Python 3.11.2,
`check.py` reproduced `AUDIT.json` byte for byte in 1.771 seconds. The output
SHA-256 was
`ec79fb3fb250081ca529e3565c86c8f7dc5afefc2bec8b6ebffe9b6f20a300e1`.

The [independent checker](independent_audit.py) does not import the author's
implementation. It exhausts all `2^19` edge subsets and every triangle subset
of the gadget. It obtains cover optimum six, full and centered packing optima
five, 20 optimal full covers, and five optimal packings in each packing
problem. It checks the fractional certificates using `Fraction` arithmetic.

It also constructs `F_4` multiplication directly from binary polynomials
modulo `x^2+x+1`, generates affine lines for `d=1,2,3,4`, and verifies every
clique pair exactly once, disjoint gadget edge sets, distinct neighborhood
types, all counts, the exact gap, and the rounded failure. Its
[expected output](EXPECTED_OUTPUT.json) has SHA-256
`2b55a115c0ca12b377498e556a446a486105187c51f91a424e01314d0fc9ebec`.

These programs guarantee the finite gadget assertions and the first four
members of the family, subject to Python and the visible code. They do not by
themselves establish the universal quantifier over all `d`; that guarantee
comes from the elementary, unformalized affine-line and additivity argument
audited above. There is no solver, floating-point tolerance, random input,
external dataset, or opaque certificate in the proof boundary.

## Scope, literature, and novelty

The family has `r=5k(k-1)/12`, so it says nothing against an error depending on
fixed `r` or against the effective fixed-type program. It also satisfies
Tuza immediately because `nu>=nu_c=5q/6`, hence `tau=q<2nu`. The missing
spoke-saturation hypothesis is real: the family has `E/2=13B/2`, whereas
`H=11B/2`.

The displayed `Phi_k(H)` inequality was a research route, not an attributed
published conjecture. A targeted search for the distinctive local value,
formula, and affine split-graph construction found the cited primary paper by
Gregory J. Puleo on edge-colorable subgraphs and a special Tuza case, but did
not locate this exact gadget or inequality. Search absence does not establish
priority. I therefore regard the graph-level result as apparently new within
the inspected frontier while leaving external novelty and publication
priority unresolved.

The proof is self-contained and publication-ready as a compact route-closing
note. Its broader mathematical impact depends on whether it leads to a sharp
correction term or a fixed-type theorem.

## Strengthening and improvement opportunities

1. **Abstract the block amplification.** Prove a general lemma for a split
   gadget on an `s`-vertex clique whose local centered fractional optimum is
   `h<L=binom(s,2)` and whose local cover optimum is `L`. Any pair-decomposition
   of `K_k` into `K_s` blocks then gives `H=(h/L)q` and `tau=q`. Substitution in
   the same identity produces an explicit quadratic coefficient. This would
   explain structurally why `1/576` is the square of the local `1/12` deficit,
   rather than presenting it as an isolated construction.

2. **Classify or optimize small local gadgets.** An exact search over allowed
   neighborhoods on `K_4` (and then `K_5`) could determine whether `11/2` is
   extremal under multiplicity caps and a six-edge local cover requirement.
   A certificate-producing ILP or exhaustive checker should report all
   isomorphism classes and independently verify the fractional optima. This is
   the most feasible route to a sharper obstruction coefficient or a
   minimality statement.

3. **Find the correct nonsaturation parameter.** The example separates
   `E/2-H` by exactly `B`, while both the type count and `D=sum_i |S_i|` grow
   quadratically. A useful next theorem would bound the extra cover cost in
   terms of `E/2-H`, `D`, or `r`, and then recover a subquadratic error when
   `r` is fixed. The present family supplies a necessary lower-bound test for
   any proposed correction but does not choose among these parameters.

4. **Formalize the universal bridge.** The finite computations are already
   redundant at the gadget level. A short formal proof of finite-field line
   uniqueness, pair partition, and additive certificates would close the only
   non-executable trust boundary and cleanly separate the theorem from its
   illustrative finite runs.

Items 1--4 are proposed directions, not results established by this review.
