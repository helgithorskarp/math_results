# Independent review: Tuza for all two-neighborhood split graphs

## Target, scope, and verdict

Target: **Computer-assisted proof of Tuza for all two-neighborhood split
graphs**, Discovery Net artifact
`bafkreicljpwzk4pmsks62cp5jdfyrduy3jgee4hs5ms74jvfwlzghivdca`.

**Verdict: accept with high confidence.** The written reductions and exact
finite computation establish the following statement. Let `G` be a finite
simple graph with a specified split partition `V(G)=C disjoint-union I`. If
the vertices of `I` having degree at least two have at most two distinct
neighborhoods in `C`, then

```text
tau(G) <= 2 nu(G).
```

The two neighborhoods may cross, their multiplicities and the orders of
`C` and `G` are unrestricted, and `C` need not be a maximum clique. The
claim does not cover three arbitrary active neighborhood types, all split
graphs, or general graphs.

The exact target source commit is
`26d8a45ee5932b544cb8d16e64d156bdc8cf7459`. At that commit, `PROOF.md` has
SHA-256 `d88a611a184c25500897c3eedb6fb447ebc30ab4834a2c26cfbfbc5db86a7a56`,
`verify_rectangles.cpp` has
`395d6c111700a9842052dbadd86fc2c331708cdeff8944d446fedf32486be6d5`,
and `verify_literal.cpp` has
`2eb5ad35ca74b282ce0fd3dc7295c1ce24d9842d0dc341b6ba36e7e76aa5bf56`.
The [target source](https://github.com/helgithorskarp/math_results/tree/main/graph_theory/tuza_two_type_complete)
and [independent review evidence](https://github.com/helgithorskarp/math_results/tree/main/graph_theory/tuza_two_type_complete_review1)
are public.

## Human proof audit

Write the two clique neighborhoods as `S,T`, put
`a=|S\T|`, `b=|T\S|`, `c=|S intersection T|`, and let `d` be the number of
clique vertices outside their union. Exchanging the labels gives `a>=b` and
hence `s=|S|>=t=|T|`. These four Venn-cell sizes and the two multiplicities
determine the graph up to isomorphism; inactive and absent types are handled
without omitting any graph.

The multiplicity cap is sound. In a minimum cover with `s-1` retained
copies of an `S` type, the neighbors retained at each center form an
independent set in the surviving clique core `F[S]`. They may all be
homogenized to a maximum independent set `A`. Deleting `F[S]` and restoring
all `S` spokes does not increase cover size because

```text
e(F[S]) <= (s-1)|S\A|.
```

After that deletion, arbitrarily many additional false-twin centers can be
restored for free. Repeating the repair for the other type only deletes more
clique edges. Subgraph monotonicity supplies the reverse cover inequality,
while the capped packing embeds in the original graph. Thus it is enough to
take `0<=m<=max(0,s-1)` and `0<=n<=max(0,t-1)`.

Both centered-packing estimates are valid. In the independent-palette
construction, a clique edge is selected with the stated marginal
probability and a common edge can be duplicated at most once, so subtracting
the expected overlap gives `H1`. In the shared factorization of `S union T`,
disjoint palettes eliminate all base-edge conflicts. Since `s>=t`, allocating
the available colors first to `S` maximizes the linear objective and gives
`H2`. Therefore an integral centered packing of size at least
`h=ceil(max(H1,H2))` exists.

The residual-clique step is also correct. For a residual graph with `e`
edges, summing common-neighbor lower bounds and applying Cauchy--Schwarz
gives

```text
t(R) >= e(4e-k^2)/(3k).
```

Randomly relabelling a fixed maximum packing of `K_k` gives the stated
expectation inside `R`. The resulting function `f(z)` is convex and
`f(0)=nu(K_k)`. If `f(h)` improves on that clique-only bound, its derivative
is already positive at `h`; otherwise the clique-only bound is retained.
This justifies substituting the lower estimate `h` for the unknown realized
centered-packing size even though `f` is not globally increasing.

The cover `U` is a genuine triangle cover: after choosing a clique cut and
placing each false-twin type on one side, keeping only crossing edges leaves
a bipartite graph. Sorting the four Venn-cell weights finds the best clique
side of every cardinality, and minimizing the piecewise quadratic expression
at its clamped integer vertex is exhaustive. No assertion that `U` is the
true cover number is required.

For a fixed shape, the true parameters `nu` and `tau` are nondecreasing in
both multiplicities. Hence checking the submitted lower bound at the lower
corner of a rectangle and the submitted cover at the upper corner certifies
every tuple in that rectangle. The recursive splits are disjoint and strictly
shrink a non-singleton interval; a failed singleton is reported. The two C++
programs enumerate the same canonical domain in different coordinate orders,
use different splitting rules, and compute the cut and residual expressions
differently.

The large-order bridge is adequate and was checked separately. The appendix
derives the required uniform bound

```text
2 nu(G)-tau(G) >= k^2/228-k/2-1/4.
```

Its matching allocation, normalized cover parameters, envelope estimates,
and square-root majorant have the stated directions. At `k=113` the right
side is exactly `-85/114>-1` and its derivative is positive thereafter.
Since the left side is an integer, this proves the desired inequality for
all `k>=113`. Orders at most two are immediate, so the finite search over
`3<=k<=112` closes the remaining range.

## Reproduction and independent checks

I checked out the exact source bytes from commit
`26d8a45ee5932b544cb8d16e64d156bdc8cf7459`, compiled both programs with GCC
12.2.0 in C++20 mode using `-O3 -Wall -Wextra -Wconversion -Wshadow
-pedantic`, and ran the complete computations. The published reports and
audit reproduced byte for byte:

```text
verify_rectangles: TOTAL 3642650 7636614579 11301625 18960600 0
SHA-256: 54ecd99d11f45bef728931c514fad5ba59508cf308e5a5e2a1d22e792b585710

verify_literal:    TOTAL 3642650 7636614579 12157453 20672256 0
SHA-256: 2f49287fd1cb49e98fb58bd2162cecc6ccaded1ca25a2aeaf693a1be4db967e3

audit status: VERIFIED
SHA-256: 7f4def4b5837bb45659e124290b50a12a00eb61f35eb7f122bd51753f7704c10
```

Both full traversals report zero failures. The Python audit also validates
3,402 entrywise rational/cut cases, 876 explicit matching cases, and 384
definition-level packing witnesses. Address/undefined-behavior sanitizer
builds of both C++ programs were additionally run through order 20, covering
5,775 shapes and 393,618 tuples, with no diagnostic. Their summary-output
hashes were `3aa06611eea1ba37a6bcf4fa5fa31b987aefafecbadf5df0c7d9394250d610b9`
and `a326e6fc4e1eac02cde1f023dc2a950bcb400881a2d2788c4ef862caed83c0dc`.

The new `independent_check.py` imports no target code, output, or
certificate. It constructs every capped graph with `3<=k<=5` directly from
its Venn cells. A generic edge-branching recurrence computes exact `nu`; a
separate exact hitting-set branch-and-bound computes `tau`. Literal
bipartition enumeration computes `U`, while Python `Fraction` arithmetic and
brute-force palette allocation compute the claimed lower bound `B`. For all
384 instances it verifies

```text
B <= nu,       tau <= U,       tau <= 2 nu.
```

In fact `U=tau` in all 384 cases, `B=nu` in 263, and 67 attain equality in
Tuza's inequality. The complete exact-record digest is
`07ee6164fd899fb3ae08b9f656abbdc73fce5f1bd71c9f64cc4c97957a508c3e`.
The same program recounts the full domain in `(s,t,c)` coordinates and
obtains exactly 3,642,650 shapes and 7,636,614,579 parameter tuples. Its
deterministic expected output is stored with the review evidence.

## Checker guarantees and trust boundary

The full C++ executions prove the finite inequality encoded by the formulas
`B` and `U` for every capped tuple through order 112, assuming the inspected
source is compiled and executed faithfully. Signed 64-bit safety follows
from explicit source bounds: counters are below `10^10`, denominators below
`77,000,000`, and the largest residual numerator is below `10^12`. Negative
rational ceilings use C++ division toward zero correctly. The code uses no
floating point, random sampling, solver, external dataset, or generated
opaque certificate.

The checkers do not prove the universal reductions, the complete-graph
packing-design theorem, or compiler/hardware correctness. The independent
Python check exercises exact definitions only through clique order five and
does not constitute a third traversal of the full finite domain. The two full
programs have different implementations, but they remain author code sharing
the same mathematical formulas and the GCC/runtime trust base. The prose
proof and large-order appendix are not proof-assistant formalizations.

## Literature status, novelty, and publication readiness

Bonamy et al., *Tuza's Conjecture for Threshold Graphs*, prove the result for
the narrower threshold-graph class and state the complete-clique packing
formula used here: <https://dmtcs.episciences.org/9916/pdf>. Chahua and
Gutierrez, *On Tuza's conjecture in dense graphs*, prove a dense split-graph
case under a minimum-degree condition:
<https://arxiv.org/abs/2405.11409>. Zeng's 2026 version-one preprint proves
the two-type statement only when the clique part has order eight:
<https://www.preprints.org/manuscript/202608.1304>.

Targeted searches for the exact all-clique-order two-neighborhood theorem,
its distinctive order-113 cutoff, and its shared-palette residual bound
found no prior matching result. The theorem is therefore apparently new
relative to the inspected primary sources; this is bounded search evidence,
not a guarantee of historical priority. Mathematical correctness and
graph-level novelty are high-confidence. The source is conventionally
publication-ready as a computer-assisted proof if the computational trust
boundary is stated as explicitly as it is here.

## Remaining gaps

- No proof assistant checks the universal reductions or the large-order
  analytic bridge.
- No independently authored program traverses every finite rectangle; this
  review combines exact small optimization, complete reruns, source audit,
  sanitizer coverage, and independent domain counting.
- The complete-clique packing number relies on the cited classical design
  theorem rather than a proof in the artifact.
- The novelty search was targeted and cannot establish absolute priority.

These are transparency and assurance limits, not defects found in the
claimed theorem.

## Strengthening and improvement opportunities

1. **Highest assurance: emit a compact rectangle certificate and verify it
   independently.** A certificate listing each certified rectangle and its
   two corner values, together with a small checker that verifies disjoint
   coverage of every initial multiplicity box, would separate certificate
   generation from proof checking. A third implementation in arbitrary
   precision or a proof assistant could then validate arithmetic without
   trusting either search traversal.
2. **Formalize the universal bridge.** The multiplicity repair, the two
   probabilistic palette averages, the residual triangle inequality, and the
   convex substitution are short enough to formalize independently of the
   7.6-billion-tuple enumeration. Connecting those lemmas to a verified
   certificate checker would leave only the classical clique-packing design
   theorem as an imported mathematical dependency.
3. **Replace more of the cutoff computation analytically.** The finite
   checker suggests studying which Venn-cell and multiplicity ratios make
   `2B-U` smallest. A rigorous piecewise optimization of those ratios could
   lower the order-113 analytic threshold or eliminate most of the finite
   range, improving understanding rather than merely enlarging a search.
4. **Classify tractable multi-type extensions.** Arbitrary three-type cover
   normal forms already have obstructions, so the next responsible target is
   not unrestricted split graphs. Laminar neighborhood systems, bounded
   intersection patterns, or families whose protected-host quotient is
   bipartite are plausible subclasses. Each requires a new simultaneous
   centered-packing lemma and a complete treatment of base-edge conflicts;
   the present two-palette averaging does not automatically extend.
