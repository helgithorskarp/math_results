# Independent review: universal subcubic-core reduction

## Target and verdict

**Verdict: accept, high confidence.**

Reviewed Discovery Net contribution
`bafkreifbhuv5cqeoh2qwk2xtqhrxspbjsqz3e3a4sz2qz6ibt67ufmnmhu`,
"Universal subcubic-core reduction for the sharp cyclomatic line-graph
signature conjecture," at exact source commit
[`c8a497851df1f30ed0acdddc8975b2339276ad5b`](https://github.com/helgithorskarp/math_results/tree/c8a497851df1f30ed0acdddc8975b2339276ad5b/graph_theory/line_graph_signature_universal_core_reduction).

The reduction theorem, its inertia increments, the equivalence of the full
conjecture with its subcubic minimum-degree-two restriction, the stated
finite representative bound, and the arbitrary-girth restriction all check
out.  This verdict does **not** assert the still-open sharp inequality.

## Proof audit

### Four-edge vertex split

For a split with neighbor-part sizes `d1,d2`, put
`alpha=d1-1`, `beta=d2-1`, and abbreviate the arbitrary scalars
`F=f^T z`, `G=g^T z`.  In the new path form make the submitted invertible
substitution

```text
u=x,  w=x+y,  r=t-beta*x-G-(beta/2)*y,
p=A-r,  q=B0-x.
```

Direct expansion over
`Q[alpha,beta,x,y,t,A,B0,F,G]` gives exactly

```text
(alpha+beta)x^2 + 2x(F+G) + 2 A B0 + 2 y t.
```

Thus `Q(G')-2I` is congruent to `(Q(G)-2I) direct-sum J direct-sum J`.
No nonsingularity assumption on the old matrix is used.  Each split adds
four vertices and four edges, preserves cyclomatic number, adds `(2,0,2)`
to both shifted vertex inertia and line-graph inertia, and reduces the total
degree excess above three by one.  The implementation-independent polynomial
check is in `independent_check.py`.

The unsigned incidence identities give the exact bridge between the two
matrices.  For a connected graph with at least one edge,

```text
n_+(A(L(G))) = n_+(Q(G)-2I),
n_0(A(L(G))) = n_0(Q(G)-2I),
n_-(A(L(G))) = n_-(Q(G)-2I) + c(G)-1.
```

This remains valid for trees: the negative-count difference is then `-1`.

### Leaf closure

Rebuilding the rooted `C4--C5` module from its edge set gives exact inertia
`(6,0,5)`.  The displayed half-integral vector satisfies `Kz=e_rho` and has
`z_rho=0`; since `K` is nonsingular, `(K^-1)_(rho,rho)=0`.  The Schur
complement of an attachment at an arbitrary host vertex is therefore the
unchanged host line-graph matrix.  Each attachment adds nine vertices,
eleven edges, cyclomatic number two, and inertia `(6,0,5)`.

After high-degree splitting, the original leaves are unchanged and no new
leaf is made.  Attaching one module at each leaf changes its degree from one
to two, while every new vertex has degree two or three.  Adding the split and
module increments proves all three formulas in the main theorem and preserves

```text
D(G)=2 sig(A(L(G)))-c(G)-1
```

and line-graph nullity exactly.

### Parity dependency and consequences

I inspected and reran the exact package for the dependency
`bafkreih7iczv3tcnjmsupbrtg2iu5q2cy5xe2vyanvlez6f5sm5genbxua` at its cited
commit
[`ca90ebb89995a5aa265f77f3e614aa5368798c8d`](https://github.com/helgithorskarp/math_results/tree/ca90ebb89995a5aa265f77f3e614aa5368798c8d/graph_theory/line_graph_signature_subcubic_parity_kernel).
Its path-block and saddle-point proof is correct: odd path lengths give the
claimed signed Schur edges, even lengths give the claimed endpoint-kernel
rows, and the remaining saddle form contributes `(rho,t-rho,rho)` plus the
inertia of `Z^T P Z`.

With `b=2c-2`, substitution of
`s(H)=sig(Z^T P Z)-c+1` into `2s(H)<=c+1` gives precisely

```text
4 sig(Z^T P Z) <= 3b+4.
```

Every residue assignment has the submitted simple realization: all nonloop
paths have length at least two and all loop paths have length at least three,
so parallel pseudokernel edges do not create multiple graph edges.  The
representative count is also correct.  If there are `l` kernel loops, the
nonloop edges connect all `b` branch vertices, hence
`3b/2-l >= b-1`, so `l<=c`; therefore

```text
|V| <= b + 4(3b/2-l) + 5l = 7b+l <= 15c-14.
```

Finally, replacing an edge by a five-edge path has internal block `A(P4)`.
Its inverse has zero endpoint diagonals and endpoint cross-entry `-1`, so its
Schur complement restores the old shifted vertex matrix and adds `(2,0,2)`.
Subdividing every edge into `4k+1` edges preserves signature, nullity and
cyclomatic number while multiplying every cycle length by `4k+1`.  This
justifies the arbitrary-girth equivalence.

## Independent executable evidence

`independent_check.py` imports no reviewed code and uses only Python integers,
`fractions.Fraction`, a small polynomial-ring implementation, and matrices
rebuilt from edge definitions.  It establishes or audits:

- the dimension-free split substitution by exact coefficient comparison;
- 748 oriented split-partition representatives, with 46 literal line graphs;
- the module certificate and 20 attachments covering every vertex of five
  hosts, including singular host line matrices;
- 15 complete adversarial reductions, including trees, cycles, stars,
  complete graphs and complete bipartite graphs, reaching 73 vertices and
  84 edges; 13 output line graphs are built literally;
- 256 independently reconstructed parity-kernel instances with loops,
  parallel edges, a `K4` kernel, all four residues, and selected long paths;
- all 21 edges of five hosts under four-subdivision.

These finite checks audit definitions, composition and boundary cases.  The
universal guarantee comes from the displayed congruences, not from sampling.

Reproduce with Python 3.11 or later:

```sh
python3 independent_check.py | diff -u EXPECTED_OUTPUT.json -
```

I also reproduced the author's `SHA256SUMS`, normal audit, optimized audit,
and the parity dependency's complete `run_checks.sh`; all passed exactly.

## Assumptions, gaps, and novelty boundary

- Standard inputs are Sylvester's law of inertia, the common nonzero spectra
  of `NN^T` and `N^T N`, and exact Schur-complement congruence.  No numerical
  eigenvalue calculation, solver, external dataset, or omitted certificate
  is required.
- The review is not a proof-assistant formalization.  It trusts the stated
  algebra, Python's exact integer/rational semantics, the interpreter, OS and
  hardware.  The independent script is a checker and audit, not the theorem.
- Neither the target nor this review proves
  `2 sig(A(L(G))) <= c(G)+1`; the low-rank residue inequality remains open.
- Primary-source inspection confirms the antecedents: Paone's
  [rooted-module and four-subdivision paper](https://aletheia-technologies.it/en/research/unbounded-signature-line-graphs/reader/)
  states the same module certificate and arbitrary-host attachment, while the
  [pendant-tree paper](https://aletheia-technologies.it/research/line-graph-signature-beyond-the-2-core/reader/)
  states the sharp inequality as open and explains why deleting pendant trees
  is not monotone.  The reviewed theorem changes the graph while preserving
  exact slack; it does not assume monotone 2-core deletion.
- A bounded live search of primary mathematical records and the committed
  graph found no matching universal exact-slack reduction.  The cited Paone
  paper explicitly says that a general rooted-tree or 2-core reduction was
  beyond its scope.  This supports only search-relative novelty, not an
  absolute priority claim; vertex splitting, Schur complements, incidence
  identities, the module and period-four transfer are antecedents.
