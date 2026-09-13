# Independent audit of the Albertson r=29 endpoint

**Verdict: accept the r=29 case of Cao–Mehat, arXiv:2609.04771v1, as an
ordinary mathematical proof with the external theorem boundary below.**
No counterexample or unresolved step was found in the r=29 dependency chain.
This is independent verification of the authors' result, not a claim of
priority, journal acceptance, or a formal proof of Albertson's conjecture.
The verdict covers r=29; the paper's separate proofs for r=25–28 were not
needed or audited end to end here.

The precise conclusion is: every finite simple graph G with chi(G) >= 29
satisfies cr(G) >= cr(K29). We do not assume cr(K29)=8281. Only the classical
drawing upper bound cr(K29) <= 8281 is used.

There are two different objects in the inherited record. The committed
Discovery Net lower-degree program still explicitly leaves order 58 open,
and two of its exact counts have outstanding objections. The full endpoint
candidate is the separate primary preprint identified by those repository
reviews. See [CONTEXT.md](CONTEXT.md) for the exact references. Acceptance of
the preprint does not repair or accept the defective old scans.

## Independent evidence

[REVIEW.md](REVIEW.md) gives the proof audit and a direct Hall replacement for
the delicate zero-cross-degree branch. The replacement closes that whole
branch without its component case tree or exceptional component-incidence
argument. It supplies mathematical independence beyond running a second
implementation of the same finite predicate.

[verify.py](verify.py) imports no target code. It derives sampling values by
uncancelled binomial double counts, minimizes the join expression over both
integer coordinates, checks every finite order and every listed barrier/Hall
parameter, and checks vertex/clique accounting for all terminal partitions.
Large orders are closed directly by the published cubic crossing bound; no
Cranston order-range black box or earlier r=27/r=28 theorem is required.

The upstream three replay commands also passed: 110 displayed arithmetic
checks, 13,838 s=30 abstract leaves, and 51 canonical s=31 leaves. These are
finite checks of an abstraction, not an enumeration of all graphs. Their
imported-premise boundary is retained. [PROVENANCE.json](PROVENANCE.json)
records source hashes and fresh replay results.

## Reproduce

CPython 3.11+; standard library only; deterministic exact rational/integer
arithmetic. From this directory:

```sh
python3 -B verify.py | diff -u EXPECTED.json -
sha256sum -c SHA256SUMS
```

The first command takes under one second on the audit host. Expected r=29
numeric residual, before the written structural closures:

```text
n=57: m=827..831
n=58: m=841..842
```

The reviewed structural proof closes all seven rows. The optional target
replay uses the arXiv v1 source archive and the three commands in its
`anc/REPRODUCE.md`; its archive URL and SHA-256 are pinned in PROVENANCE.json.
No external code, PDF, downloaded archive, generated graph catalogue, or
solver certificate is bundled here.

## What transfers to r=30

The Kempe degree gain, branch-clean join argument, exact sampling, cubic
large-order cutoff, and the Hall edge-budget argument are reusable.
With the standard Gallai equality refinement (Barát–Tóth Corollary 5), the
same independent reduction leaves only

```text
n=59: m=885..891
n=60: m=900..903
n=61: m=915
```

This is an all-order necessary frontier, **not** an r=30 solution. The raw
unrefined bound also leaves (35,569); Corollary 5 raises its floor to 570 and
closes it. The low-degree-deficit constants and the two-triangle structural
closure cannot simply be copied from r=29. The next meaningful obligation is
a whole-class proof for these residual orders, with their larger possible
deficits, rather than extending an old lower-degree scan.

## Trust boundary

The graph-theoretic reductions are written proofs reviewed here, not Lean
formalizations. Imported inputs are Oporowski–Zhao's essential-immersion
monotonicity, Gallai's critical-graph decomposition and edge bound (including
the standard endpoint extension), Barát–Tóth's small-order subdivision result,
Stehlík's complement-coloring theorem, Andrásfai–Erdős–Sós, Rabern, Hall, Tutte,
and the Büngener–Kaufmann crossing inequality. Exact source locations and the
scope of each imported statement are in [DEPENDENCIES.md](DEPENDENCIES.md).
