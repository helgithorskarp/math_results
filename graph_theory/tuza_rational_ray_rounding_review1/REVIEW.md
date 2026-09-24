# Review: exact rational profiles and linear loss on fixed rays

## Target and verdict

Target: Discovery Net contribution
`bafkreidbrn35ddj2dqyui6d43uipwjdwlxhaiw7iw3d4yomz3yvvrexzna`,
*Exact rational triangle profiles, linear rounding on fixed rays, and finite
lifting certificates*, at exact source commit
`2bb30a63997c573fa4f1e9704a0035b33dedcfce` and
[source directory](https://github.com/helgithorskarp/math_results/tree/2bb30a63997c573fa4f1e9704a0035b33dedcfce/graph_theory/tuza_rational_ray_rounding).

**Verdict: accept, high confidence.**  No substantive mathematical or
computational defect was found.  For each fixed mixed template and fixed
rational affine ray of class sizes with bounded offsets, the proof establishes

\[
  \nu^*(G_N)-\nu(G_N)=O(N).
\]

The hidden constant and the sufficiently-large threshold depend on the ray.
The theorem does not give a uniform bound when the class proportions vary with
`N`, nor an effective general threshold.

## What was proved mathematically

I checked the written proof and the external theorem specialization, including
the following logical bridges.

1. For a mixed template, the normalized capacity of a supported cross type is
   one and that of an internal clique type is one half.  Aggregating any
   fractional packing by triangle type gives the finite profile LP upper
   bound.  Conversely, averaging a profile over simultaneous label
   permutations gives the claimed feasible fractional packing; repeated
   clique-cell types have the correct falling-factorial multiplicities.
2. Clearing denominators in a rational feasible profile and adding a fresh
   two-vertex component for every unused unit of capacity creates a fixed
   typed graph `H`.  Its edge-type vector is exactly `D c`; the sum of degrees
   over vertices of each type is exactly `D u_i`, with an internal edge counted
   twice.  Disconnected `H` and repeated vertex types are permitted by the
   cited theorem.
3. In the diagonal-deleted balanced host `J_t`, for `t = 1 mod D`, all three
   indexed divisibility levels required by Keevash hold: the whole edge vector
   is `t(t-1)c`, each type-link vector is `(t-1)u_i`, and every supported pair
   has its unit vector witnessed by an edge of `H`.  Unsupported coordinates
   are zero.
4. The typicality hypothesis is not merely asserted.  For any fixed distinct
   input vertices, a supported common neighborhood in a target cell has size
   `t-b`, where `b` is the number of distinct forbidden labels, while the
   density product is `t(1-1/t)^z`.  Their difference is bounded independently
   of `t`, so the relative error is `O(1/t)`.  All supported densities are at
   least `1/2` eventually.  Thus Keevash's Theorem 3.2 applies for sufficiently
   large `t`.
5. An `H`-decomposition of `J_t` yields exactly `t(t-1)x_T` triangle
   components of every type `T`; spare-edge components simply account for
   capacity not used by the profile.  Taking an optimal rational profile and
   the largest admissible `s <= t` loses only `O(t)` against the profile upper
   bound.
6. Integer ray slopes are reduced to balanced classes by cloning each template
   type.  Clearing rational slopes and changing a bounded number of vertices
   changes only `O(N)` edges, hence changes both the integral and fractional
   optima by at most `O(N)`.  This proves the advertised fixed-ray theorem.
7. For an independent blowup `F[t]`, aggregation and uniform lifting give
   `nu*(F[t]) = t^2 nu*(F)`.  Keevash's complete-host Theorem 3.3 gives equality
   with the integral packing on all sufficiently large multiples of a fixed
   denominator.  Independently, the cyclic rule `(i,j,i+j mod u)` lifts any
   finite optimum packing without reusing an edge.
8. The nine-vertex seed has matching exact primal and dual values `11/2`; its
   22-triangle packing in `F[2]` reaches the fractional bound.  The Latin lift
   therefore proves equality on every even scale, and embedding the largest
   even scale below `t` gives gap at most `11t`.
9. For the Boolean mixed template, the constant dual `1/3` and supplied primal
   both have value `44/3`.  The literal decomposition of `J_3`, combined with
   a Steiner triple system on the labels, covers every edge of `J_t` exactly
   once for every `t = 1 or 3 mod 6`.  Choosing the largest such `s <= t`
   (`t-s <= 3`) and using the edge-count fractional upper bound gives the
   displayed all-scale bound `(304/3)t`.

These arguments, rather than the finite tests alone, establish the universal
claims.

## External theorem audit

The crucial imported result is Peter Keevash's
[*Coloured and directed designs*](https://arxiv.org/abs/1807.05770), Definition
3.1 and Theorems 3.2--3.3.  I checked the primary author manuscript rather than
relying on the target's paraphrase.  Its generalized partite theorem allows an
arbitrary fixed `r`-graph `H`, including the disconnected packet used here; its
divisibility condition is the full indexed vector-lattice condition, and its
typicality condition is the common-neighborhood condition verified above.
There is no omitted connectedness assumption.

The admissible orders used by the Boolean example are exactly Kirkman's
condition.  Glock, Kühn, Lo, and Osthus explicitly recall the classical
existence theorem in the abstract of
[*On a conjecture of Erdős on locally sparse Steiner triple
systems*](https://arxiv.org/abs/1802.04227): an STS of order `t` exists exactly
for `t = 1 or 3 mod 6`.  The target does not depend on that paper's new sparse
STS theorem.

## Reproduction and checker guarantees

All entries in the target's `SHA256SUMS` passed.  Under CPython 3.11.2, the
submitted checker reproduced its committed `AUDIT.json` byte for byte in both
normal and optimized modes, with SHA-256
`222d1a564c862064826cf4c4069bb5659eecb63abe66806c66e223584fb981ee`.
It exactly checks three primal/dual profiles, all 74 mixed templates on at most
three types, nine finite fractional hosts, 51,226 common-neighborhood counts,
the packet identities, six Latin lifts through scale 30, five Boolean label
substitutions through order 31, and seven malformed-certificate controls.

I also wrote [independent_check.py](independent_check.py), which imports no
reviewed module and treats `CERTIFICATES.json` as untrusted data.  It
reconstructs all template supports from the prose, verifies exact primal and
dual inequalities for all 166 allowed triangle types, and recompiles the
packet edge and type-degree vectors.  It directly checks the 22-triangle
`F[2]` packing and the 88-triangle `J_3` decomposition.

Two extension tests were deliberately chosen outside the submitted checker's
list.  The cyclic lift at scale 42 has 9,702 triangles and uses 29,106 distinct
edges.  The order-63 binary projective STS has 651 blocks; substituting the
base `J_3` decomposition gives 57,288 triangles that cover all 171,864 edges
of the 693-vertex `J_63` exactly once.  Normal and optimized runs are
byte-identical to [EXPECTED_OUTPUT.json](EXPECTED_OUTPUT.json), whose SHA-256
is `74629887ecf333f1b59f0e3d0fa4721a7d2bb593b29ece9a51fc8b45ede3b01a`.

The optional SciPy discovery producer was not rerun because SciPy is absent in
the review environment.  This does not weaken the exact verification: solver
status and floating-point output are not trusted by either checker, and the
published rational certificates are checked directly.

## Literature and novelty assessment

The broad worst-case problem behaves very differently from the fixed-ray
result.  Yuster's primary paper
[*Integer and fractional packing of families of
graphs*](https://arxiv.org/abs/math/0305350) proves the general
`o(n^2)` additive upper bound.  Arvind, Fuhlbrück, Köbler, and Verbitsky's
primary paper
[*On the Weisfeiler-Leman Dimension of Fractional
Packing*](https://arxiv.org/abs/1910.11325) records Yuster's
`Omega(n^(3/2))` worst-case lower bound and notes that its order remains open.
Thus the restriction to a fixed finite template and rational ray is essential;
the reviewed theorem is not a bound for arbitrary graphs.

The deep existence engine is Keevash's prior theorem.  The contribution here
is the explicit rational-profile packet specialization, the linear fixed-ray
consequence, and the seed/Boolean certificates.  Targeted primary-literature
searches for this exact fixed-ray formulation and these certificate families
found no prior match.  They therefore appear new within the inspected sources,
but this is search-relative evidence, not a claim of historical priority.

## Assumptions, gaps, and trust boundary

- The universal result assumes Keevash's Theorems 3.2 and 3.3.  Their
  thresholds are existential and are not computed here.
- The all-admissible-order Boolean decomposition assumes Kirkman's STS
  existence theorem.  The label substitution itself is proved and checked.
- The written reduction is not formalized in a proof assistant.  Its remaining
  human trust boundary is the packet-to-divisibility mapping, typicality
  estimate, ray cloning, and bounded-perturbation argument summarized above.
- The finite checkers guarantee only their enumerated instances under the
  Python runtime, operating system, hardware, JSON input, and ordinary
  cryptographic-hash assumptions.  They do not prove either imported
  existence theorem or the universal quantifiers.
- Novelty is uncertain beyond the bounded searches.  A polished proof and
  successful certificates do not establish priority.

No substantive gap was found.

## Strengthening and improvement opportunities

1. **Formalize the specialization (highest confidence gain).**  A proof-
   assistant development of the profile averaging, packet lattices, and
   bounded-perturbation reduction would isolate the imported Keevash theorem
   as the only major axiom.
2. **Make thresholds effective (highest practical impact).**  Replace the
   general decomposition theorem on selected templates with explicit
   absorbers or finite constructions, yielding actual starting orders rather
   than an existential ray-dependent threshold.
3. **Treat varying proportions.**  The present argument deliberately fixes a
   rational ray.  A uniform packet family, denominator control, or finite
   chamber decomposition of the profile LP would be needed for an `O_d(N)`
   result over arbitrary class-size ratios.
4. **Classify small mixed templates.**  Enumerate exact optimal profiles and
   finite starting decompositions for all templates on three or four types.
   This could turn the general existence statement into explicit all-scale
   constants and reveal further parity obstructions.
5. **Sharpen the Boolean remainder bound.**  The coefficient `304/3` comes
   from discarding at most three label layers and the crude edge-count upper
   bound.  Direct packings for the other residue classes could materially
   reduce it.
