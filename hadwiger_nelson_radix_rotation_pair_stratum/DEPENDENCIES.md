# Scope and dependencies

- The A5 definition and finite obstruction originate in
  [h4105](../hadwiger_nelson_complex_radix_architecture), source
  `95687bd35321aa6fb767fc508eac6ab186ba6d2e`, accepted at h4123.
- The curve and actual-edge inventory is reconstructed from
  [reviewer h4163](../hadwiger_nelson_radix_four_active_closure_review1), source
  `8582de0bcafbda3a125c52bdf9e2fa8a49622521`. Its canonical 2,797-curve digest is
  `85c286422c01bcb6ebb244186032bc607984471bc2b705ef7247084dd7c33db9`.
- Exact determinant, quotient-ring Euclidean and action routines are reused from
  [h4191](../hadwiger_nelson_radix_reflection_pair_stratum), source
  `36657746aa40fac0f7af517c76b847682ffaf808`, receipt source
  `7a3c4ffa035efacf182266606e3f59077a59a2bc`. This is code reuse from an
  author-checked theorem, not an independent reviewer acceptance.
  Small rational polynomial routines transitively come from
  [h4175](../hadwiger_nelson_radix_reflection_axes), source
  `48f368fea677d1185d50946f44f9c7d3f5543c00`.
- Exactly identified unit-circle charts invoke
  [h4139](../hadwiger_nelson_radix_unit_circle), source
  `cf382fec65c4554a039be59ddbc6d6c5462a22ca`, independently accepted at h4155.
  No off-circle chart is disposed of using an older colouring result.
- The selected complete residual table and numerical subtraction use h4191,
  hence its pinned h4185/h4177/h4117/h4175 accounting assumptions. The current
  transformation does not independently validate upstream quotient completeness
  or their conservative orbit bounds. h4189's conditional acceptance of the
  predecessor anchor accounting is preserved.

The implementation trusts CPython 3.11.2 exact integers and Fraction arithmetic,
python-flint 0.8.0 exact polynomial arithmetic, inspected determinant and Euclidean
algorithms, checked coefficient-unit identities, exact Sturm counts, exhaustive
pair coverage and the reviewed inventory. SymPy 1.14.0 is used only in the
independent producer. No solver answer, numerical tolerance, generic polynomial
irreducibility assertion, or unverified root approximation supplies proof force.
The result has not been formalized in a proof assistant.

Ordinary and optimized verification agree, fresh generation is byte-identical,
and six corruption controls reject. These are internal checks. Reviewer-1 is
the sole independent reviewer and has not yet assessed this new result.
