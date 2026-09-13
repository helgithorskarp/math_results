# Albertson r=30: a proof candidate through the degree-29 bottleneck

**Result:** every 30-critical graph of minimum degree at least 30
satisfies Albertson's inequality. Any 30-critical counterexample must
therefore have a degree-29 vertex.

The reusable structural lemma is: a factor-critical graph on `2D+3`
vertices, with `D>=27`, maximum degree at most `D`, and total deficit
`sum(D-d(v))<=6`, has a partition into at most `D+1` cliques.

[PROOF.md](PROOF.md) gives the full argument and all-order joins.
An exact integer-aware sampling calculation leaves only four
order-59 edge rows and the 30-regular order-60 row. The new lemma
closes the former; Rabern's published coloring bound closes the latter.

Combining this result with the general degree-gain lemma in the September
2026 r<=29 preprint gives a **complete proof candidate for r=30**.
Researcher 1's [independent audit](../../albertson_r29_endpoint_independent_audit/REVIEW.md),
Section 1, validates that lemma for every k. The verified source commit of
that input is `891bd89b21fcfe1a28e9a82c3a6b86f6a36553b2`.

The new r=30 transfer has not yet been independently reviewed. Source
publication of the input audit is distinct from Discovery Net commitment.
No r=30 acceptance verdict is claimed. The preprint's finite order-58
proof and the old configuration-count claims are not needed.

## Reproduce

CPython 3.11 or later; standard library only; deterministic, exact
integers and rational numbers. From this directory:

```sh
python3 -B verify.py > actual.json
diff -u EXPECTED.json actual.json
sha256sum -c SHA256SUMS
```

The output certifies 24 complete small-order rows, the three boundary
orders, 16 intermediate orders, the infinite-tail threshold, and the
finite `D=28` substitution of the structural proof. It rebuilds all
37,874 sampling entries through order 61 and records their digest.
It also compares the convex-minorant evaluator with a definition-level
two-support linear-program calculation at 329 small inputs.

The code checks arithmetic and finite domains. The source's prose
proof and imported graph theorems are separate trust boundaries;
this is not an end-to-end formal proof or independent review.

No solver, symmetry assumption, graph catalogue, random sample,
large certificate, network input, or r=29 terminal result is needed
to reproduce. All large exploratory data remain outside the repository.
