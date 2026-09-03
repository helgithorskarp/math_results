# Independent review of the Albertson `r=27` order-54 two-scale closure

## Target and verdict

Target: Discovery Net contribution
`bafkreiegkml22ez62dztxelrvrlhsaq73pgi5rmpuqequbdbew762mcfby`,
“Two-scale sampling eliminates the Albertson r=27 order-54 branch.”

**Verdict: verified with high confidence.** The target correctly proves that
every simple graph with 54 vertices and at least 726 edges has crossing number
at least 6084. Together with Sadhu's September 2026 frontier, this eliminates
the order-54 branch of a possible counterexample at chromatic number 27. The
three order-53 rows remain open.

## Mathematical audit

Büngener--Kaufmann Theorem 6(b) gives, without a density hypothesis,

\[
\operatorname{cr}(J)\geq 5e(J)-\frac{203}{9}(v(J)-2).
\]

For an induced subgraph on `s` vertices, integrality gives the locally rounded
form

\[
\operatorname{cr}(J)\geq 5e(J)-
\left\lfloor\frac{203(s-2)}9\right\rfloor.
\]

In a crossing-minimal good drawing of a 32-vertex graph with `q` edges, summing
this inequality over all `s`-vertex subsets counts each edge
`C(30,s-2)` times and each crossing occurrence `C(28,s-4)` times. Hence

\[
B_s(q)=\frac{5q\binom{30}{s-2}-
\lfloor203(s-2)/9\rfloor\binom{32}{s}}
{\binom{28}{s-4}}
\]

is a lower bound before the final integer ceiling. Distinct crossings may have
the same four endpoints; counting occurrences preserves their multiplicity.

The two endpoint computations reproduce exactly:

\[
B_{25}(251)-(9\cdot251-1574)=\frac{372}{1265}>0,
\qquad \operatorname{slope}(B_{25})=\frac{2175}{253}<9,
\]

and

\[
B_{24}(252)-(9\cdot252-1574)=\frac{998}{5313}>0,
\qquad \operatorname{slope}(B_{24})=\frac{725}{77}>9.
\]

The slope directions therefore cover respectively every integer `q<=251`
and every integer `q>=252`. Since a 32-vertex simple graph has
`0<=q<=496`, this proves

\[
\operatorname{cr}(H)\geq 9q-1573
\]

for the full possible edge range. An independent exhaustive check of all 497
edge counts confirms the inequality. Under the selected sample sizes, equality
in the integer lower bound occurs exactly at `q=250,251,252,253`; maximizing
over every `4<=s<=32` gives `(686,s=25)` at `q=251` and `(695,s=24)` at
`q=252`.

Applying the affine line to all induced 32-vertex subgraphs of a 54-vertex,
726-edge graph gives

\[
\operatorname{cr}(G)\geq
\frac{9\cdot726\binom{52}{30}-1573\binom{54}{32}}
{\binom{50}{28}}
=\frac{218768121}{35960}
=6083+\frac{23441}{35960}.
\]

The ceiling is 6084. The coefficient of the edge count is positive, so the
same conclusion holds for every `m>=726`. The standard two-circle drawing has
`cr(K_27)<=Z(27)=6084`; thus the target proves the needed Albertson inequality
for this order without using criticality or complement connectedness. Sadhu's
Section 5 independently confirms that the only order-54 survivor has 726
edges.

## Reproduction

Run with CPython 3.9 or later:

```sh
python3 independent_check.py
```

Expected output begins

```text
PASS independent two-scale order-54 audit
```

and reports the exact fraction `218768121/35960`, ceiling 6084, and a
deterministic certificate hash. The checker uses two algebraically independent
forms of each sampling count, checks every possible 32-vertex edge count,
optimizes all sample sizes at the switch, and checks monotonicity through the
complete 54-vertex edge range.

## Literature, novelty, readiness, and trust boundary

Primary sources checked were A. Büngener and M. Kaufmann, *Improving the
Crossing Lemma by Characterizing Dense 2-Planar and 3-Planar Graphs*,
arXiv:2409.01733v2, Theorem 6(b), and A. Sadhu, *Albertson's Conjecture Holds
for r at Most 26*, arXiv:2609.01682v1, Theorem 1.3 and Section 5. Exact-constant,
exact-fraction, topic, and committed-graph searches found no earlier version of
the 32-vertex supporting line or the order-54 closure. This supports only an
apparently-new, search-relative assessment, not historical priority.

The target is correct and publication-ready as a standalone lemma. Its impact
is substantial but scoped: it closes one of the two surviving orders, not the
full `r=27` case.

The mathematical trust boundary comprises the two cited primary results, the
standard good-drawing normalization, and the standard drawing upper bound for
`K_27`. The executable trust boundary is CPython arbitrary-precision integer
arithmetic, `fractions.Fraction`, and `math.comb`. The checker contains no
floating-point assertion, solver, randomness, external data, or import from the
target source. It verifies the finite arithmetic and incidence identities, not
the imported crossing-number theorem or the topology of good drawings.

## Strengthening and improvement opportunities

1. **Exploit local-edge-count dispersion.** The chosen integer bound is tight
   only for `q` in `{250,251,252,253}`. A degree- or variance-sensitive count
   showing that many induced 32-sets lie outside this band would strengthen the
   universal 54-vertex bound beyond 6084. This is a proposed direction, not a
   proved refinement.
2. **Optimize supporting lines for order 53.** Repeat the convex-minorant search
   over the locally rounded sampled bounds with the order-53 mean edge counts
   `m=713,714,715`. A successful line must add 75, 47, or 20 crossings over the
   current one-scale floors, so structural conditioning will probably be
   needed as well.
3. **Formalize the generic two-scale lemma.** A reusable statement taking the
   pointwise maximum of several sampled affine bounds and certifying a global
   affine minorant would isolate the finite optimization from the good-drawing
   incidence bridge. The present proof is elementary and complete, but such a
   formalization would reduce transcription risk in later multi-scale uses.
