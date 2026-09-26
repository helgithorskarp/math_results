# Sources and campaign context

* Elsholtz et al., *Maximal line-free sets in F_p^n*,
  [author manuscript](https://arxiv.org/html/2310.03382v2),
  [published article](https://doi.org/10.1007/s10998-024-00617-x).
  This is the problem context and source of the original 70-point
  construction. The universal local-consistency proof here does not
  use a construction or classification from that paper.
* The committed [complete upper bound 71](../upper_bound71/THEOREM.md),
  Discovery Net `bafkreia7wiim7o3xqlzuvr2ifw4ul6zcwvjnil4vcxhouyutvhv5fpq7si`,
  height 5986, source commit `e81f511a02ac5ef43f1005408ba370df110b7007`.
  This is the current numerical frontier. Its first AA representative
  supplies the 72-weight control. Its global exclusion is needed only
  to conclude that this locally consistent example cannot be glued.
  The current verifier does not replay its SAT proofs.
* The earlier [planar marginal obstruction](../../additive_combinatorics/line_free_planar_lp_obstruction/PROOF.md),
  Discovery Net `bafkreifwjecau65opqj3hmj5ba2d4dlig2advvmkjtkx5xztwpovu24o4y`.
  It shares point marginals across all 155 planes, with a fixed grid
  section and a parallel section of size at most ten. The present
  theorem fixes every fiber cardinality and shares full fiber laws
  across the 30 projection planes, uniformly for every admissible
  71-weight quotient. Neither relaxation contains the other as stated.
  Its small `planar_cap.cpp` is reused with attribution and fully replayed.
* The published [low-pair reduction at 71](../low_pair71/README.md)
  and [affine-asymmetry result](../affine_asymmetry71/README.md) were
  inspected as teammate work. At the prepublication graph refresh the
  follower was still at height 5995, before those submissions became
  visible. Neither active graph claim is used as a premise. This theorem
  applies to any quotient meeting its displayed inequalities, independently
  of how a global candidate is reduced to that quotient.
* The six maximum-planar examples in the teammate's
  `affine_asymmetry71/REPRESENTATIVES.txt` suggested the ordinary
  templates. Those templates are verified directly as thirteen explicit
  small sets here; no completeness claim from that catalogue is imported.
  The seven small-section templates were found in a private planar search.
  Only the explicit templates and their 20-element affine profile covers
  are needed for the constructive proof.

The geometric argument isolates a local-to-global failure. No new
classification of three-dimensional sets, improved numerical bound,
or independent acceptance of the exact extremal value is asserted.
