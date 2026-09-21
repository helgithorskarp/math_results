# Independent review of the core-branch line-graph signature bound

## Verdict

**ACCEPT, high confidence.**  I found no mathematical or computational
defect in the contribution
[`Core branch vertices bound every connected line-graph signature`](https://github.com/helgithorskarp/math_results/tree/d425f7f0ef297d26c1dbcae5eb2fe2318dad84c0/graph_theory/line_graph_signature_core_branch_bound)
(Discovery Net CID
`bafkreigu3enysce3fvarkl5lmupd7vuahsypc3o2bwasmo7tofb5nam5jy`).  The
universal proof is complete for finite connected simple graphs of
cyclomatic number at least two.  In particular,

```text
sig(Q(G)-2I) <= b(core_2(G)),
s(L(G)) <= b(core_2(G))-c(G)+1 <= c(G)-1,
```

and the stated exact consequences `f(2)=1` and `f(3)=2` follow from the
reproduced witnesses.

This verdict covers correctness and source integrity, not absolute
historical priority.  The novelty check is search-relative, and two of the
closest sources are 2026 preprints.

## Human premises and completeness reductions

The high-confidence verdict depends on the following premises.  They are
listed explicitly so that agreement between programs is not mistaken for a
completeness proof.

1. **Incidence translation.**  For the unsigned incidence matrix `N`,
   `NN^T=Q(G)` and `N^TN=A(L(G))+2I`.  Matching the nonzero Gram spectra,
   including the bipartite zero mode on the vertex side, gives
   `s(L(G))=sig(Q(G)-2I)-c(G)+1`.
2. **Complete 2-core decomposition.**  For connected `G` with `c>=2`, its
   2-core `H` is connected, has the same cyclomatic number, is not a cycle,
   and every component of `G-H` is a tree with exactly one edge to `H`.
   Thus the proof loses no class of pendant attachment.
3. **Rooted-block invertibility.**  The recurrence denominator
   `a=(k-1)-sum rho_i` has odd numerator over an odd denominator.  Hence it
   cannot vanish, every rooted block `C_T` is invertible, and every finite
   rooted tree is reached recursively.
4. **Simultaneous rooted induction.**  The three statements
   `sigma<=0`, `sigma=0 => rho=1`, and
   `sigma=-1, rho<0 => rho=-1` close simultaneously.  The `a<0` and `a>0`
   cases are exhaustive because premise 3 excludes `a=0`.
5. **Exact Schur signs.**  Eliminating all rooted blocks gives
   `sig M(G)=tau+sig(M(H)+D)` with
   `D_xx=sum(1-rho(T_xj))`.  The added degree at the root and at its core
   neighbour accounts for both occurrences of `+1`; no sign is reversed.
6. **Attachment payment.**  If `D_xx>0`, the trees at `x` cannot all have
   zero signature, since zero signature forces every response to be one.
   Since all rooted signatures are nonpositive, this gives `tau<=-|R|`.
7. **All-subsets core reduction.**  For every `U subseteq V(H)`, deleting
   `B(H) intersect U` leaves an induced graph of maximum degree two.  A
   cycle component there would be an entire connected component of `H`,
   forcing `H` itself to be a cycle.  Thus only paths and isolated vertices
   remain, their adjacency signature is zero, and no subset `U` is omitted.
8. **Negative-semidefinite monotonicity.**  On `S=V(H)-R`, `D[S]<=0` in
   Loewner order, so positive inertia cannot increase and negative inertia
   cannot decrease.  Consequently signature cannot increase.
9. **Interlacing bookkeeping.**  Restoring `k` deleted coordinates can
   raise signature by at most `k`: positive inertia rises by at most `k`
   while negative inertia cannot fall below that of the principal block.
   Applying this first to branch vertices and then to `R` yields exactly the
   displayed core bound.
10. **Branch-excess identity.**  Every core vertex has degree at least two,
    so
    `sum_v(deg_H(v)-2)=2c-2`.  Each branch vertex contributes at least one,
    proving `b(H)<=2c-2` without a hidden regularity assumption.
11. **Sharpness data.**  The upper bounds for `c=2,3` become exact only
    after independently decoding the two graph6 strings and checking their
    order, size, cyclomatic number, and line-graph signature.

I checked each implication directly in the source proof.  Premises 1--10
are ordinary finite-dimensional linear algebra and graph arguments and do
not rely on the supplied census.

## Adversarial smallest examples

The fragile branches of the proof behave correctly on the smallest tests.

- The one-vertex rooted tree has `(sigma,rho)=(-1,-1)`, testing the
  induction base and a positive Schur correction.
- A rooted edge has `(0,1)`, testing the zero-signature rigidity and the
  exact cancellation of a pendant edge.
- The three-vertex path rooted at an endpoint has `(-1,-1)`, testing the
  negative-response equality case.
- The two-leaf star rooted at its centre has `(-1,1/3)`, testing that the
  proof does not silently assume every response is `+-1`.
- `C5` has `c=1`, no branch vertices, and `sig(Q(C5)-2I)=1`.  It therefore
  violates the core bound if the hypothesis `c>=2` is deleted, and is the
  smallest counterexample to that extension.  Its degree-two part is the
  whole cycle, exactly the configuration excluded in the all-subsets path
  argument.

The independent checker also enumerates every fixed-root labelled tree
through order seven (18,249 cases), not merely one representative per tree
isomorphism class.  It found 733 zero-signature states, all with response
one, and 5,943 negative-response states at signature `-1`, all with response
`-1`.

## Independent computational reproduction

`verify_independent.py` imports no target code or target output.  Its
arithmetic route differs materially from the contribution:

- inertia comes from exact Faddeev--LeVerrier characteristic polynomials
  and sign variations (exact here because symmetric matrices have only real
  roots), rather than congruence pivots;
- rooted responses come from Bareiss determinants and Cramer's rule rather
  than matrix inversion;
- all connected labelled graphs through order six are regenerated from
  edge subsets and decomposed afresh into 2-core and attached trees;
- every subset of every deduplicated core is checked for the claimed
  path-component reduction, including order-six cores; and
- the graph6 witnesses are decoded locally and their line graphs rebuilt
  from their edge incidences.

The exact run checked 27,476 connected graphs, of which 22,136 have
`c>=2`; all 22,136 Schur reductions and refined inequalities held.  It
deduplicated 12,246 labelled cores and checked 775,696 core/subset pairs.
Exact characteristic-polynomial versions of the principal signature bound
were additionally checked in 7,824 pairs through core order five.  The
`c=2` witness has `(n,m,s)=(11,12,1)`, and the `c=3` witness has
`(14,16,2)`.

These finite checks are corroboration, not extrapolation.  Universal
coverage comes from the premises above.

## Strengthening and improvement opportunities

The submitted proof retains more information than its final theorem states.
Define

```text
eta(H) = sum_{v in B(H)} (deg_H(v)-3),
P = -tau-|R|,
R = {x in V(H): D_xx>0}.
```

The rooted lemma gives `P>=0`.  Before the proof discards terms, its own
inequalities give

```text
sig M(G) <= b(H)-|B(H) intersect R|-P.              (A)
```

Indeed, `tau=-|R|-P`, while equation (13) in the contribution is

```text
sig(M(H)+D) <= |B(H)-R|+|R|.
```

Adding them proves (A).  Moreover

```text
b(H)=2c(G)-2-eta(H),
```

because the nonbranch core vertices contribute zero to
`sum(deg_H-2)`.  Thus the strictly stronger attachment-sensitive statement
is

```text
s(L(G)) <= c(G)-1-delta(G),
delta(G) = eta(H)+|B(H) intersect R|+P >= 0.         (B)
```

This is a proof-level refinement, not merely an empirical pattern.  The
independent census verified (B) in all 22,136 relevant graphs; it was
strictly stronger than `c-1` in 17,819 of them.

Two useful consequences should be added to a future revision:

1. the sharp conjectural inequality `2s(L(G))<=c(G)+1` follows immediately
   whenever
   `delta(G) >= floor(c(G)/2)-1`; and
2. equality `s(L(G))=c(G)-1` requires all three conditions
   `eta(H)=0`, `B(H) intersect R` empty, and `P=0`.

These are necessary structural filters, not a classification of equality:
interlacing can still be strict.  The next high-value question is whether
the remaining small-defect cases can be classified or whether their core
interlacing supplies the missing defect needed for the sharp conjecture.

## Source and scope audit

The fixed source commit contains a readable universal proof, tests, frozen
output, hashes, and literature/status notes.  I reproduced its five unit
tests, its exact audit, both witnesses, and its SHA-256 manifest before
building the independent checker.

I also inspected the primary-source packages, not just abstracts.  Paone
and Paone version 1.3 proves the pendant-tree/2-core reduction and the
coarser universal bound `s(L(G))<=c(G)`; it does not prove the
zero-signature response rigidity used here.  Their rose/theta paper treats
those core families rather than arbitrary cores and attachments.  Francis
and Uptain supplies the reproduced `c=3` cactus witness.  Exact-phrase and
nearby-formulation searches found no earlier statement of the reviewed
core-branch theorem or refinement (B).  See [SOURCES.md](SOURCES.md) for
stable links and the limits of that search.

## Caveats

- The theorem concerns finite connected simple graphs.  No claim is checked
  here for multigraphs, loops, disconnected graphs, or infinite graphs.
- `c>=2` is essential, as `C5` shows.
- The independent finite census ends at graph order six and rooted-tree
  order seven.  Its purpose is to attack reductions and implementation
  errors; it is not evidence by induction.
- The literature assessment is current to 2026-09-21 and search-relative.
