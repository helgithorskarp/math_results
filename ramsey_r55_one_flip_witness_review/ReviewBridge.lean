import OneFlipWitness

namespace RamseyOneFlipReview

open RamseyOneFlip

universe u

variable {V : Type u} [DecidableEq V]

/-- Any family of at least three blue defect clauses contains an exact
three-clause subfamily disjoint from every clause through the pivot. -/
theorem exists_three_defects_disjoint_from_pivot_clauses
    (color : V → V → Bool) (w : V)
    (blues side : Finset (Finset V))
    (hthree : 3 ≤ (blueDefectClauses color w blues).card)
    (hside : ∀ B ∈ side, w ∈ B) :
    ∃ witness : Finset (Finset V),
      witness ⊆ blueDefectClauses color w blues ∧
      witness.card = 3 ∧
      Disjoint side witness := by
  obtain ⟨witness, hwitnessSub, hwitnessCard⟩ :=
    Finset.exists_subset_card_eq hthree
  refine ⟨witness, hwitnessSub, hwitnessCard, ?_⟩
  rw [Finset.disjoint_left]
  intro B hBside hBwitness
  have hBdefect := hwitnessSub hBwitness
  have hwNotB : w ∉ B := (Finset.mem_filter.mp hBdefect).2.1
  exact hwNotB (hside B hBside)

/-- The target's unique-four-clause theorem therefore supplies the exact
three-element witness category used by the downstream fan budget, and this
category is automatically disjoint from all side clauses through `w`. -/
theorem unique_red_four_clause_supplies_exact_three_witness_category
    (color : V → V → Bool) (reds blues side : Finset (Finset V))
    (w : V) (R0 : Finset V)
    (hR0 : R0 ∈ reds) (hwR0 : w ∈ R0) (hR0card : R0.card = 4)
    (hunique : ∀ R ∈ reds, w ∈ R → R = R0)
    (hunsat : SelectedUnsatisfiable reds blues)
    (hredMono : ∀ R ∈ reds, Monochromatic color true R)
    (hredNoExtend : ∀ R ∈ reds, w ∉ R → ∃ v ∈ R, color w v = false)
    (hblueNoExtend : ∀ B ∈ blues, w ∉ B → ∃ v ∈ B, color w v = true)
    (hside : ∀ B ∈ side, w ∈ B) :
    ∃ witness : Finset (Finset V),
      witness ⊆ blueDefectClauses color w blues ∧
      witness.card = 3 ∧
      Disjoint side witness := by
  apply exists_three_defects_disjoint_from_pivot_clauses color w blues side
  · exact unique_red_four_clause_forces_three_blue_defects
      color reds blues w R0 hR0 hwR0 hR0card hunique hunsat hredMono
      hredNoExtend hblueNoExtend
  · exact hside

#print axioms exists_three_defects_disjoint_from_pivot_clauses
#print axioms unique_red_four_clause_supplies_exact_three_witness_category

end RamseyOneFlipReview
