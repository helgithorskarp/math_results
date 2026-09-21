# Independent review of the 9/8 barycentric Tuza bound

## Verdict

**ACCEPT, high confidence.** I found no mathematical defect in
[`2-edge-connected facet duals give a 9/8 barycentric Tuza bound`](https://github.com/helgithorskarp/math_results/tree/5b45335337fc3988dbddc016ca8b2b505beab7f5/graph_theory/barycentric_tuza_nine_eighths)
(Discovery Net CID
`bafkreiarrhfg7sgrzyqb3aopkke6ujsexa6efhg4wlhrbkk72b4e4dsshy`). For a
finite nonempty pure two-dimensional abstract simplicial complex `T`, with
every edge in at most two triangular facets and 2-edge-connected facet dual,
the proof correctly establishes

```text
kappa(T) <= floor(f_2(T)/3),
nu_triangle((sd T)^(1)) = 3f_2(T)-kappa(T),
tau_triangle((sd T)^(1)) = 3f_2(T)
                          <= (9/8)nu_triangle((sd T)^(1)).
```

The theorem is a strong restricted-class consequence and does not resolve
Tuza's conjecture for arbitrary graphs. The novelty assessment is
search-relative; the two imported signed-graph results are preprints.

## Human premises and completeness reductions

The verdict rests on the following human chain, not on agreement between
the submitted and independent programs.

1. **Simplicial scope.** Facets are distinct three-element sets, every face
   lies in a facet by purity, and every original edge has incidence one or
   two. These hypotheses exclude repeated facets, multiedges, and dangling
   lower-dimensional faces.
2. **Dual domain.** Two distinct triangular facets cannot share two distinct
   edges, so the facet dual is simple. Each facet has three sides, so the
   dual is subcubic. For a nontrivial dual, the assumed 2-edge-connectivity
   supplies connectedness and minimum degree at least two. If a convention
   regards the one-vertex dual as 2-edge-connected, its zero-defect theorem
   instance is immediate and can be separated before invoking the imported
   bound.
3. **Signed constraint encoding.** Choosing a reference orientation per
   facet gives a switching class: a shared edge whose reference directions
   agree requires opposite flip labels, and one whose directions disagree
   requires equal labels. Switching a dual vertex is exactly reversing that
   facet's reference orientation.
4. **Defect as vertex frustration.** Deleting facets until the retained
   orientations are coherent is exactly deleting dual vertices until the
   signed graph is balanced. Thus `kappa(T)` is Sivaraman's frustration
   number for this signed dual.
5. **Sivaraman alignment.** Theorem 1 of arXiv:1403.7212 proves equality of
   vertex and edge frustration for every signed subcubic graph. The paper's
   edge-deletion definition agrees with the minimum number of negative edges
   in a switching-equivalent signature used by Chen--Li--Wang.
6. **Chen--Li--Wang completeness.** Theorem 1.1 of arXiv:2511.15226v1
   applies to every 2-edge-connected simple signed subcubic graph and lists
   exactly five switching-class exceptions. The signs, underlying edges,
   orders `4,5,8,8,8`, and frustration indices `2,2,3,3,3` were read from
   the primary TeX figure rather than inferred from the target's tables.
7. **Boundary incidence identity.** Internal primal edges correspond
   bijectively to dual edges, so
   `b=3f-2|E(D)|=sum_F(3-deg_D(F))`.
8. **Boundary parity.** At each primal vertex, counting incident
   facet-edge pairs gives `2t_x=2i_x+b_x`; hence its boundary degree is even.
   In particular, the single boundary edge forced by `Gamma2` is impossible.
9. **Cubic-to-closed reduction.** A cubic facet dual makes `b=0`, so every
   primal edge lies in exactly two facets. Each vertex link is consequently
   a finite 2-regular simple graph, hence a disjoint union of cycles.
10. **Normalization completeness.** Splitting a primal vertex once per link
    component preserves every oriented facet, shared edge, dual adjacency,
    and signed constraint. After all splits, every vertex link is one cycle,
    so the result is a closed triangulated surface. Its components correspond
    to facet-dual components; therefore the assumed connected dual gives one
    connected surface.
11. **Balance versus orientability.** A balancing assignment is precisely a
    coherent choice of facet orientations on the normalized surface.
    Positive frustration therefore makes that surface nonorientable.
12. **Ten-facet lower bound.** For a connected closed nonorientable
    triangulated surface, `chi<=1`, `3f=2e`, and the simple one-skeleton has
    `e<=v(v-1)/2`. Thus `e=3(v-chi)>=3(v-1)`, whence `v>=6` and
    `f=2(v-chi)>=10`. This excludes all four cubic exceptions, which have
    only four or eight facets.
13. **Imported barycentric identity.** The previously accepted and
    independently reviewed orientation-defect theorem supplies
    `tau=3f` and `nu=3f-kappa`. Substituting the signed-frustration bound and
    using integrality gives the claimed packing and ratio inequalities.

These premises exhaust the exceptional cases: one noncubic exception is
removed by boundary parity, and all four cubic exceptions are removed by
closed-surface normalization and the facet lower bound.

## Adversarial smallest examples

- A single triangle has three boundary edges. Two triangles sharing an edge
  have four. They exercise the parity count and show why a boundary count of
  one or two should be rejected rather than merely regarded as unusual.
- The tetrahedron boundary has four facets, closed dual `K4`, and frustration
  zero. Thus small closed complexes exist; the proof must exclude only the
  unbalanced switching classes, not the underlying graphs.
- The five-facet Möbius fixture has a 2-edge-connected dual, five boundary
  edges, and both frustration parameters equal one. It tests a genuine
  positive-defect boundary case satisfying the theorem.
- Two tetrahedral spheres identified only at one vertex have eight facets
  and a disconnected two-component vertex link at the pinch. Normalization
  splits that vertex, preserves the signed dual, and produces two spheres.
  This tests the step that is usually hidden behind the phrase “standard
  normalization,” while also showing why dual connectedness is needed to
  conclude that the normalized surface is connected.
- The six-vertex, ten-facet projective-plane triangulation has no boundary
  and both frustration parameters equal three. It shows that the
  nonorientable ten-facet cutoff is sharp.

## Independent computational reproduction

The submitted five unit tests, exact audit, expected output, and SHA-256
manifest all pass. Its optimized run prints the same output, although most
of its mathematical guards use Python `assert` and are disabled by `-O`.
This is a reproducibility weakness, not a mathematical defect; a future
revision should replace proof-critical assertions with explicit exceptions.
The accepted barycentric-identity dependency was also replayed in normal and
optimized modes, together with its manifest, reproducing evidence digest
`68abb4fa1a8a3b4f6a759707a266b1d6decf8ef020a52514a39d2b9da8d4c19b`.

`verify_independent.py` imports no target code, output, or fixture. It uses a
materially different audit architecture:

- edge frustration is computed by increasing-size edge-deletion search;
- vertex frustration is independently computed by increasing-size
  vertex-deletion search;
- balance is tested by parity propagation, not switch-mask minimization;
- all 403 admissible nonempty labelled triangle families on three through
  five labels are regenerated, and every boundary degree is checked even;
- vertex-link components are constructed explicitly, facets are transported
  through normalization with their orientations retained, and the signed
  dual is recomputed; and
- the tetrahedron, five-facet Möbius complex, projective plane, and pinched
  two-sphere fixture are checked from facet lists.

The independent deletion computations reproduce the five primary
frustration pairs `(2,2,3,3,3)`. Among the 403 small facet families the
boundary edge counts are `0,3,4,5,6,7`, never one or two. Normal and
optimized runs use the same explicit `require` checks and reproduce the
frozen JSON exactly.

These finite checks corroborate primary-figure transcription and fragile
reductions. The all-complex theorem rests on the human proof above.

## Strengthening and improvement opportunities

Three useful corollaries are already latent in the proof.

1. **Eulerian boundary strengthening.** The boundary edges form a simple
   Eulerian graph, because every boundary degree is even. Consequently

   ```text
   b(T)=0 or b(T)>=3.
   ```

   For a nontrivial dual under the target's 2-edge-connected hypothesis,
   every dual degree is two or three and `b(T)` is exactly the number of
   degree-two dual vertices. Thus such a realizable dual is either cubic or
   has at least three degree-two vertices. The target states only the special
   consequence `b!=1`; the exclusion of `b=2` is equally immediate.

2. **Small closed orientability.** If every edge of a finite pure triangle
   complex lies in exactly two facets and it has fewer than ten facets, then
   every component of its vertex normalization is orientable. Equivalently,
   its signed facet dual is balanced componentwise and `kappa(T)=0`. This
   does not require the full 2-edge-connected hypothesis. The
   projective-plane fixture shows that ten cannot be replaced by eleven.

3. **Residue-sensitive ratio.** Writing `f=3q+r`, the proved exact identity
   yields

   ```text
   tau/nu <= (9q)/(8q)             if r=0,
   tau/nu <= (9q+3)/(8q+3)         if r=1,
   tau/nu <= (9q+6)/(8q+6)         if r=2.
   ```

   Therefore equality in the advertised `9/8` bound can occur only when
   `3` divides `f` and `kappa(T)=f/3`. In the closed case `f` is even, so
   equality additionally requires `6` to divide `f`. These are necessary
   filters, not an existence classification.

A higher-value continuation would classify which equality cases of
Chen--Li--Wang are realizable as signed facet duals. The present theorem
eliminates only the five strict exceptions; it does not classify equality
at `F=f/3`.

## Source and scope audit

The fixed target source contains a readable universal proof, tests, exact
checker, expected output, source notes, and an integrity manifest. The
primary TeX sources of both imported signed-graph papers were downloaded and
inspected. Their theorem domains and definitions match the target exactly.
The prior barycentric identity has a committed high-confidence independent
review and was treated as an explicit dependency rather than silently
reproved here.

Targeted searches of the primary sources and current Tuza context found no
earlier elimination of these five exceptions for signed facet duals or this
`9/8` barycentric consequence. That is bounded search evidence only. See
[SOURCES.md](SOURCES.md) for stable links and the precise dependency
boundary.

## Caveats

- The theorem concerns finite pure abstract triangle complexes with edge
  incidence at most two and a 2-edge-connected facet dual.
- It says nothing about arbitrary graphs, higher edge incidence, polygonal
  facets, or facet duals with bridges.
- Sivaraman (2014), Chen--Li--Wang (2025), and the current broader Tuza
  source are preprints for this audit; no peer-review status is inferred.
- The proof is informal and relies on the standard classification fact
  `chi<=1` for connected closed nonorientable surfaces.
- Computational checks are finite exact corroboration, not a proof by
  enumeration of arbitrary complexes.
