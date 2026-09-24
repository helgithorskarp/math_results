# Sources, dependencies, and novelty boundary

Primary and campaign sources checked on 23 September 2026:

- [Kabluchko and Prochno, arXiv:2007.05247v2](https://arxiv.org/html/2007.05247),
  *The maximum entropy principle and volumetric properties of Orlicz
  balls*. Their Theorem A gives a leading precise-volume equivalence by
  Gibbs tilting and sharp large deviations. Those mechanisms are prior
  work. It does not state the first relative Edgeworth coefficient for the
  exact diagonal section and flat potential treated here.
- [Johnston and Prochno, arXiv:2012.11568](https://arxiv.org/html/2012.11568),
  *A Maxwell principle for generalized Orlicz balls*. Quantitative Gibbs
  marginal limits for generalized Orlicz balls are prior work. Their
  framework is not the present exact diagonal-section correction, and the
  predecessor explains the mismatch caused by the flat zero level of
  \(g(x)=(|x|-1)_+\).
- The campaign's
  [sharp simplex orthant-projection theorem](../sharp_simplex_orthant_projections/PROOF.md),
  Discovery Net artifact
  `bafkreiethi6omrbebnho7hld27gxk5qcmo6fuyvjcxu2pdboccrcskjuci`,
  committed at height 5647 and independently accepted at height 5661. It
  supplies the geometric optimization and section identity.
- The direct target is the campaign's
  [leading simplex-envelope asymptotic](../simplex_envelope_asymptotics/PROOF.md),
  Discovery Net artifact
  `bafkreico3jit4pykibuuahra6bxgwokgdzmnz6ucsxqbviqmtuhp25dm5e`,
  committed at height 5663, source commit
  `aea74701bc168bce9468d3048306a6b915f58944`. It proves only
  \(C_n\sim\kappa\beta^n/\sqrt n\) and explicitly claims no effective rate.

Targeted live searches covered combinations of “Edgeworth expansion,”
“Orlicz ball,” “hyperplane section,” “second-order volume asymptotic,” and
“Gibbs.” They found the general leading-asymptotic and Maxwell-principle
antecedents above, but no primary source stating the coefficient

\[
-\frac{237}{20}+\frac{284}{15}\frac{\sqrt5-1}{2}
\]

for this section or projection constant. This is a bounded,
search-relative novelty statement, not certification of historical
priority. Multivariate Edgeworth expansion itself is classical and is not
claimed as new; the advance is its singular-mixture implementation and the
resulting exact first correction for these constants.

The follow-up all-orders search on 23 September 2026 additionally used
“all-order asymptotic expansion,” “Poincaré expansion,” and “higher-order
Orlicz volume.” It located the same leading-volume, Maxwell-principle, and
large-deviation literature, but no primary result giving a full expansion
for this exact diagonal section or the displayed second coefficient. The
source graph target for that follow-up is Discovery Net artifact
`bafkreieagokxm3ks7m75uj3muwb3fymbmkcedg4wcfiy3i7yxnx4e55kku`,
committed at height 5671.
