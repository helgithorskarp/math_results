import Parts509Attachment

/-!
A reviewer-side strengthening of the small vertex-cut classification.

For the classification at one fixed deletion set `S`, it is enough that the
core surviving that particular deletion is connected. Exact attachment degree
can also be weakened to the lower bound `d ≤ degree`.
-/

namespace Parts509AttachmentReview

open Parts509Attachment

universe u

variable {V : Type u} [Fintype V] [DecidableEq V]
variable (G : SimpleGraph V) [DecidableRel G.Adj]

theorem small_vertex_cut_iff_eq_neighborFinset_local
    {D S : Finset V} {d : ℕ}
    (hcore : CoreDeleteConnected G D S)
    (h_toCore : ∀ ⦃x⦄, x ∈ D → ∀ ⦃y⦄, G.Adj x y → y ∉ D)
    (hdegree : ∀ x ∈ D, d ≤ (G.neighborFinset x).card)
    (hS : S.card ≤ d) :
    ¬DeleteConnected G S ↔
      ∃ x ∈ D, x ∉ S ∧ S = G.neighborFinset x := by
  rw [deleteConnected_iff_no_deleted_neighborhood G hcore h_toCore]
  push Not
  constructor
  · rintro ⟨x, hxD, hxS, hxsub⟩
    refine ⟨x, hxD, hxS, ?_⟩
    exact (Finset.eq_of_subset_of_card_le hxsub (hS.trans (hdegree x hxD))).symm
  · rintro ⟨x, hxD, hxS, rfl⟩
    exact ⟨x, hxD, hxS, Finset.Subset.rfl⟩

#print axioms small_vertex_cut_iff_eq_neighborFinset_local

end Parts509AttachmentReview
