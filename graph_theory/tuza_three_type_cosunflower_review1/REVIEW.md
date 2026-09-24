# Independent review: Tuza for three-type co-sunflower split graphs

## Target, scope, and verdict

Target: **Computer-assisted Tuza theorem for all three-neighborhood
co-sunflower split graphs**, Discovery Net artifact
`bafkreihjynqkf2kkbn2i37w5gtiewx5jb74fkuzodhhlbag72xo2jsscky`.

**Verdict: accept with high confidence.** The proof establishes the following
precise statement. Let `G` be a finite simple graph with a specified split
partition `V(G)=C disjoint-union I`, and discard vertices of `I` having at
most one neighbor in `C`. If the remaining clique neighborhoods have at most
three distinct values and, when there are three, they satisfy

```text
S0 union S1 = S0 union S2 = S1 union S2,
```

then `tau(G) <= 2 nu(G)`. Clique order, multiplicities, and clique vertices
outside the common union are unrestricted. The theorem does not cover three
arbitrary neighborhoods, all split graphs, or general graphs.

The exact target source commit is
`f6e398604f8781071079248208c58dae79ae1a30`. At that commit, `PROOF.md` has
SHA-256 `960b203f819d12343ddd0b6bb33621b3e232326b25e255553e43aa572213cf11`,
`verify.cpp` has
`82ac02b1611d2505b1700d0f6f3f225ef8c91e24a5987e417f164d07aa7f5129`,
and `audit.py` has
`b66e24134c75d74853dae20901426c4ec9039d6465914f6b5c6729a813bfaedb`.
The [exact target source](https://github.com/helgithorskarp/math_results/tree/f6e398604f8781071079248208c58dae79ae1a30/graph_theory/tuza_three_type_cosunflower)
and [independent review evidence](https://github.com/helgithorskarp/math_results/tree/main/graph_theory/tuza_three_type_cosunflower_review1)
are public.

## Human proof audit

Write `Pi=U\Si`, where the three `Pi` are pairwise disjoint, and set
`pi=|Pi|`, `c=|S0 intersection S1 intersection S2|`, `u=|U|`,
`d=|C\U|`, and `si=u-pi`. Relabelling gives `p0<=p1<=p2`; exactly three
distinct types is equivalent to `p1>=1`, and activity is equivalent to
`s2>=2`. These conditions give a complete canonical parameterization, not
merely a subfamily.

The multiplicity cap is valid. For one type of size `s`, homogenize the
surviving spokes of its `s-1` retained centers to a maximum independent set
`A` of the surviving clique core `F[S]`. Every edge of `F[S]` meets `S\A`,
so

```text
e(F[S]) <= (s-1)|S\A|.
```

Deleting those core edges and restoring all spokes therefore does not cost
more than the removed spokes. All further copies of the type can then be
restored freely. Repeating the operation for the other types only deletes
more clique edges. Together with subgraph monotonicity, this proves that
`1<=mi<=si-1` suffices without changing `tau` or losing the required packing
lower bound.

The uniform analytic bridge is sound. Independent modular matching palettes
make the centered packing expectation an inclusion-exclusion probability.
Its quadratic part `delta` is a sum, over ordered clique-vertex pairs, of
probabilities of a union of increasing selection events; hence it is
nonnegative and coordinatewise nondecreasing. The discarded linear term is
a corresponding union probability over single vertices and lies in `[0,u]`.
This proves the stated centered-packing lower bound.

For a residual clique graph with `e` edges, degree summation and
Cauchy--Schwarz give

```text
t(R) >= e(4e-k^2)/(3k).
```

Triangles with equal vertex-label sum modulo `k` are edge-disjoint, because
two triangles sharing an edge have different third vertices and hence
different sums. Combining one such class with the centered packing and
expanding yields the claimed quadratic lower bound for `2nu`.

The clique-cut cover is also correctly normalized. Averaging a side of size
`ell` inside `U`, or putting all of `U` on that side, gives the two pieces of
the cover function. Its unconstrained quadratic minimizer produces
`R=min(r,2alpha-1)` and rounding `ell` to an integer costs at most `1/4`.
The co-sunflower identity gives exactly

```text
(u-pi)(u-pj) - u(u-pi-pj) = pi*pj >= 0,
```

which is the required pairwise-union estimate. After summing it and scaling
the multiplicities down monotonically, one obtains
`delta>=alpha R-R^2/3` with the correct inequality direction.

The remaining quartic argument was checked coefficient by coefficient in
exact rational arithmetic. In particular,

```text
g''(t)-1/18 = (8/9)(1-t)(2-t),
g(9/25)-9g'(9/25)^2 = 3855551/1464843750 > 1/400.
```

At `k=199`, the resulting lower bound on the integral quantity
`2nu-tau` is `-299/400>-1`, and its integer-order difference is positive
thereafter. The refined outside-vertex argument is also correctly directed:
outside `[1/4,1/2]` the quartic is at least `31/3456`, while inside that
interval integration in `alpha` gains at least `(25/144)(1-alpha)`. At
`k=55` the first margin is `-2129/3456>-1`; the second case is stronger when
`d>=3`. Thus the analytic omissions from the finite search are proved, not
sampled.

For the finite remainder, both centered-palette estimates are legitimate.
The independent palettes use exact inclusion-exclusion. The shared palette
uses disjoint colors; because `s0>=s1>=s2`, greedily assigning its limited
colors in that order maximizes the linear expectation. The residual-clique
function is convex and equals `nu(K_k)` at zero. If its value at the lower
estimate `h` improves on the clique-only bound, its derivative at `h` is
positive, so substituting `h` for the unknown realized centered-packing size
is safe.

The four sign choices in the cover computation are exhaustive up to swapping
the two clique-cut sides. The five constant-weight clique cells are correct.
On each sorted-weight interval the cover objective is an integral quadratic,
and evaluating its clamped floor minimizer finds its exact minimum. Finally,
the rectangle implication uses monotonicity of the true graph parameters:
for every point `x` between corners `lo` and `hi`,

```text
nu(x) >= nu(lo) >= B(lo),   tau(x) <= tau(hi) <= U(hi).
```

It does not assume that either numerical formula is monotone. Every split is
disjoint, strictly shrinks an integer interval, and ends either in a certified
box or a reported failing singleton.

## Reproduction and independent checks

I compiled the exact source with GCC 12.2.0 in C++20 mode using `-O3 -Wall
-Wextra -Wconversion -Wshadow -pedantic` and ran the complete single-threaded
calculation. It took 791.35 seconds on this host. The report reproduced the
published file byte for byte:

```text
TOTAL 11539903 497893855660344 2317590705 4623641507 441165614683344 0
SHA-256 7d342e7d9d74431befba3a3aefcafc08bf01168361d689c975c1e13c469a5ecf
```

The columns are shapes, represented tuples, certified boxes, visited boxes,
analytically certified tuples, and failures. The Python 3.11.2 author audit
then reproduced `AUDIT.json` byte for byte with SHA-256
`91c1a459af137f30c876247fc63bca9a5430633533f2f732a9be7f80e783a647`.
It rechecked 3,239 entrywise rational/cut cases, 992 explicit palette cases,
237 packing witnesses and exact covers, the full domain counts, and the
analytic constants.

An AddressSanitizer/UndefinedBehaviorSanitizer build with GCC 12.2.0 at
`-O1` completed through order 55 with no diagnostic:

```text
TOTAL 82305 21198379395 18527198 36972091 1918024632 0
summary-output SHA-256 7ce16b1f0f3044bcc6f32c11bb28d023073203c616f08e20f7a61a9a73d5ca89
```

The new `independent_check.py` imports no target source, output, or
certificate. It directly constructs every capped three-type co-sunflower
graph with clique order at most five. A generic include/exclude recurrence
computes exact `nu`; a separate generic hitting-set branch-and-bound computes
exact `tau`. Literal enumeration of clique bipartitions and center-type
placements computes the submitted cut bound, while `Fraction` arithmetic and
exhaustive shared-palette allocation compute the packing bound. For all 237
instances it verifies

```text
B <= nu,   tau <= U,   tau <= 2nu.
```

Here `U=tau` in all 237 cases, `B=nu` in 113, and the minimum exact Tuza slack
is two. The exact-record digest is
`8b2762adc4ac4fd23de51897bcd1ee38e7e92cfeae249e81d91b5f7b8c7ab48d`.
The same independent program counts the finite domain in ordered
neighborhood-size coordinates and obtains exactly 11,539,903 shapes,
497,893,855,660,344 tuples, and 441,165,614,683,344 analytic-tail tuples. It
also reconstructs the rational quartic and both threshold margins. Its
deterministic JSON has SHA-256
`418c4415cf3d99100473189cc1945582311261c654765c9262740929bbb553ca`.

## Checker guarantees and trust boundary

The full C++ execution proves the finite inequality encoded by `B` and `U`
for every capped tuple through order 198, together with the analytically
removed outside-vertex tail, assuming the inspected source was compiled and
executed faithfully. Signed 64-bit arithmetic is safe: centered-expectation
partial numerators are below `2*10^12`, the residual numerator is below
`10^13`, cover intermediates are below one million, and the largest actual
counter is below `5*10^14`, all far below `2^63`. Negative ceilings use C++
division toward zero correctly. The computation uses no floating point,
random sampling, solver, external dataset, or opaque certificate.

The checker does not prove the universal reduction, the classical exact
packing formula for complete graphs, or compiler and hardware correctness.
The at-most-two-type branch is the previously reviewed theorem
`bafkreicljpwzk4pmsks62cp5jdfyrduy3jgee4hs5ms74jvfwlzghivdca`, rather
than new code in this artifact. The independently authored Python program is
definition-level only through clique order five and is not a second traversal
of all finite rectangles. The universal proof is not formalized in a proof
assistant, and the complete traversal remains author code whose search and
checking logic are combined in one program.

## Literature status, novelty, and publication readiness

Bonamy et al., *Tuza's Conjecture for Threshold Graphs*, prove the conjecture
for the narrower class with nested neighborhoods and supply the matching and
complete-clique packing facts used here
(<https://dmtcs.episciences.org/9916/pdf>). Chahua and Gutierrez prove the
dense split-graph case under a minimum-degree hypothesis
(<https://arxiv.org/abs/2405.11409>). Zeng's 2026 version-one preprint treats
two neighborhood types only when the specified clique has order eight
(<https://www.preprints.org/manuscript/202608.1304>).

Targeted searches for the exact pairwise-common-union condition, the term
“co-sunflower” in this Tuza setting, and an all-order three-neighborhood split
theorem found no prior match. The theorem is therefore apparently new
relative to the inspected primary sources. This is bounded search evidence,
not proof of historical priority. Mathematical correctness and graph-level
novelty are high-confidence; absolute literature priority remains uncertain.
With its explicit computational boundary and reproducible source, the result
is ready to present as a computer-assisted theorem.

## Remaining gaps

- No proof assistant checks the cap, probabilistic expectations, analytic
  bridge, or connection from the finite formulas to the graph theorem.
- No independently authored implementation traverses all 4,623,641,507
  visited boxes; the review combines a complete rerun and source audit with
  exact small optimization, sanitizer coverage, and independent domain
  counting.
- The compact report contains aggregate counts rather than a separable list
  of box certificates, so a third party must rerun the search program rather
  than check a generated proof object.
- The complete-clique packing formula and the accepted at-most-two-type
  theorem remain explicit mathematical dependencies.
- The novelty search cannot establish absolute priority.

These are assurance and scope limits, not defects found in the claimed
theorem.

## Strengthening and improvement opportunities

1. **Separate certificate generation from checking.** Emit a compact stream
   of certified four-dimensional boxes, each with its corner values, plus a
   domain-partition certificate. A small arbitrary-precision checker could
   verify the formulas, disjointness, and complete coverage without trusting
   the recursive search implementation. This is the highest-value assurance
   improvement.
2. **Formalize the universal bridge.** The cap repair, probability
   interpretations, residual triangle bound, clique-cut averaging, and
   quartic certificate are short enough to formalize independently of the
   large enumeration. Connecting those lemmas to a verified certificate
   checker would leave only the classical clique-packing existence theorem
   and the two-type branch as imported results.
3. **Optimize `g_alpha` jointly instead of replacing `alpha` by one.** The
   current reduction deliberately loses information. Exact semialgebraic
   minimization in `(alpha,R)`, retaining `d/k`, could lower the order-199
   threshold and enlarge the analytic outside tail. This is a plausible
   proved refinement once a rational inequality certificate is supplied.
4. **Quantify departures from the co-sunflower condition.** The proof uses
   the hypothesis through the inequalities
   `u|Si intersection Sj| <= si*sj`. A useful next theorem would assume a
   controlled violation factor and re-optimize the resulting quartic. This
   could cover “near co-sunflower” triples without claiming arbitrary
   three-type split graphs; the missing work is a positive uniform gap after
   the weakened pairwise estimate.
5. **Classify the unrestricted three-type obstruction.** The existing
   five-cycle core work addresses covers, while this theorem succeeds because
   the centered-packing conflicts admit clean inclusion-exclusion. A finite
   classification of complement-intersection patterns, paired with a packing
   lemma for each pattern, is a more responsible route toward arbitrary
   three-type neighborhoods than extrapolating the present palette argument.
