import HypercubeSquareLift

namespace HypercubeSquareLiftReview

open SimpleGraph
open HypercubeSquareLift

variable {V : Type*}

/-- Square-freeness of the lift forces square-freeness of the left layer. -/
theorem squareFree_left_of_lift {G₀ G₁ : SimpleGraph V} {D : Set V}
    (hfree : SquareFree (twoLayerLift G₀ G₁ D)) : SquareFree G₀ := by
  intro x y hxy hwitness
  exact hfree (by simpa) hwitness.inl

/-- Square-freeness of the lift forces square-freeness of the right layer. -/
theorem squareFree_right_of_lift {G₀ G₁ : SimpleGraph V} {D : Set V}
    (hfree : SquareFree (twoLayerLift G₀ G₁ D)) : SquareFree G₁ := by
  intro x y hxy hwitness
  exact hfree (by simpa) hwitness.inr

/-- The intersection-independence hypothesis is necessary for a square-free
two-layer lift. -/
theorem indep_intersection_of_squareFree_lift
    {G₀ G₁ : SimpleGraph V} {D : Set V}
    (hfree : SquareFree (twoLayerLift G₀ G₁ D)) :
    (G₀ ⊓ G₁).IsIndepSet D := by
  rw [SimpleGraph.isIndepSet_iff]
  intro u hu v hv huv hboth
  apply hfree (show (twoLayerLift G₀ G₁ D).Adj (.inl u) (.inl v) by
    simpa using hboth.1)
  exact ⟨.inr u, .inr v, by simp, by simp, by simpa using hu,
    by simpa using hboth.2, by simpa using hv⟩

/-- Exact characterization of square-freeness for the two-layer lift. -/
theorem squareFree_twoLayerLift_iff {G₀ G₁ : SimpleGraph V} {D : Set V} :
    SquareFree (twoLayerLift G₀ G₁ D) ↔
      SquareFree G₀ ∧ SquareFree G₁ ∧ (G₀ ⊓ G₁).IsIndepSet D := by
  constructor
  · intro hfree
    exact ⟨squareFree_left_of_lift hfree, squareFree_right_of_lift hfree,
      indep_intersection_of_squareFree_lift hfree⟩
  · rintro ⟨hfree₀, hfree₁, hind⟩
    exact squareFree_twoLayerLift hfree₀ hfree₁ hind

/-- Saturation of omitted vertical host edges forces domination in the
intersection graph. -/
theorem dominates_intersection_of_saturated_lift
    {G₀ G₁ H : SimpleGraph V} {D : Set V}
    (hsat : SquareSaturatedIn (twoLayerLift G₀ G₁ D)
      (twoLayerLift H H Set.univ)) :
    Dominates (G₀ ⊓ G₁) D := by
  intro v hvD
  have hhost : (twoLayerLift H H Set.univ).Adj (.inl v) (.inr v) := by simp
  have hmissing : ¬(twoLayerLift G₀ G₁ D).Adj (.inl v) (.inr v) := by
    simpa using hvD
  obtain ⟨a, b, hxb, hay, hxa, hab, hby⟩ :=
    hsat.closes_omitted hhost hmissing
  cases a <;> cases b <;> simp_all
  case inl.inr =>
    obtain ⟨rfl, huD⟩ := hab
    exact ⟨_, huD, by simpa [adj_comm] using hxa, by simpa using hby⟩

#print axioms squareFree_twoLayerLift_iff
#print axioms dominates_intersection_of_saturated_lift

end HypercubeSquareLiftReview
