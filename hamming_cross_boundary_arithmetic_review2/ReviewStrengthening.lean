import Mathlib.Tactic

/-!
# Independent exact quotient/remainder refinement

This file strengthens the arithmetic kernel reviewed at Discovery Net height
2021.  It proves the exact deficit in the layer-count equality and therefore
the converse omitted by the target: its small-remainder hypothesis is both
necessary and sufficient for that particular arithmetic equality.
-/

namespace HammingCrossBoundaryReview

/-- Exact deficit when quotienting after replicating `layers` copies. -/
theorem layer_quotient_deficit
    {s x layers : ℕ} (hs : 0 < s) :
    layers * x / s =
      layers * (x / s) + layers * (x % s) / s := by
  have hdecomp :
      layers * x = s * (layers * (x / s)) + layers * (x % s) := by
    conv_lhs => rhs; rw [← Nat.mod_add_div x s]
    ring
  rw [hdecomp, Nat.mul_add_div hs]

/-- The target remainder hypothesis is exactly equivalent to equality of
the replicated quotient and the quotient of the replicated volume. -/
theorem layer_quotient_equality_iff
    {s x layers : ℕ} (hs : 0 < s) :
    layers * (x / s) = layers * x / s ↔
      layers * (x % s) < s := by
  rw [layer_quotient_deficit hs]
  constructor
  · intro equality
    have quotient_zero : layers * (x % s) / s = 0 := by omega
    exact (Nat.div_eq_zero_iff_lt hs).mp quotient_zero
  · intro remainder_small
    rw [Nat.div_eq_of_lt remainder_small, Nat.add_zero]

/-- Exact iff form of the target pair-remainder specialization. -/
theorem pair_remainder_equality_iff
    {s nj nk nl : ℕ} (hs : 0 < s) :
    nl * (nj * nk / s) = nj * nk * nl / s ↔
      nl * ((nj * nk) % s) < s := by
  rw [mul_comm (nj * nk) nl]
  exact layer_quotient_equality_iff hs

#print axioms layer_quotient_deficit
#print axioms layer_quotient_equality_iff
#print axioms pair_remainder_equality_iff

end HammingCrossBoundaryReview
