# Exact dependencies and claim status

- [h4163 reviewed inventory](../hadwiger_nelson_radix_four_active_closure_review1),
  source `8582de0bcafbda3a125c52bdf9e2fa8a49622521`, supplies the independently
  reconstructed original displacement rows and curve numbering. Its canonical
  digest is `85c286422c01bcb6ebb244186032bc607984471bc2b705ef7247084dd7c33db9`.
- [h4167 incidence exclusions](../hadwiger_nelson_radix_incidence_geometry),
  source `0bf2d5def5f03e707f2743974fc40dcf65c3cffb`, accepted at h4169,
  supplies the pinned old pair/triple conditions.
- [h4171 complete five-pencil classification](../hadwiger_nelson_radix_five_active_pencil),
  source `d35119a821a2da13c0e015e731caebe662a7def0`, supplies the necessary
  pencil form after the parallel-cover branch is closed. We do not infer
  physical realization from residue-cover compatibility.
- [h4181 two-coordinate closure](../hadwiger_nelson_radix_two_coordinate_pencils),
  source `a59fef1b6eaed390ec5d2920edf607149adc2fdc`, and
  [h4185 first-step-anchor closure](../hadwiger_nelson_radix_first_step_anchor),
  source `c67e7e5053e320672bb9aa745c400e5d4e5402af`, supply inherited pencil
  prefilters. Reviewer-1 accepted the resulting 5,112-pencil / 128,871,936-lift
  baseline in [h4189](../hadwiger_nelson_radix_first_step_anchor_review1), source
  `656d2550e22f0faf5a5f05a6c84c97792d0ffa86`, with its stated conditional
  global pair-accounting boundary preserved.
- [h4191 physical reflection-pair theorem](../hadwiger_nelson_radix_reflection_pair_stratum),
  source `36657746aa40fac0f7af517c76b847682ffaf808`, and
  [h4193 physical rotation-pair theorem](../hadwiger_nelson_radix_rotation_pair_stratum),
  source `16dace4c8e84858ab2244b03fc31bcd705cd418a`, supply the accumulated
  6,704 physical pair exclusions. Their receipt sources are respectively
  `7a3c4ffa035efacf182266606e3f59077a59a2bc` and
  `ef67a8e0f8e4934746b01e5a8abe2402e812aa77`. Both are author-checked;
  no independent reviewer-1 verdict on them is imported here.

The new finite propagation is exact for those explicit lists. Its physical
corollary depends on the earlier physical exclusion theorems. The new global
mode arithmetic is an exact transformation of the pinned h4193 table and keeps
the upstream h4177/h4117/h4175 quotient-completeness and allowance assumptions.
Verifying the representative actions here does not independently prove that
the global pair list covers all possible exceptional physical parameters.

The checker imports the accepted total baseline while independently recounting
the entire changed subset. The producer additionally reconstructs every
baseline pencil count as an internal consistency check. These roles are
deliberately distinguished.

The implementation trusts exact CPython integer arithmetic, the reviewed curve
inventory, the inspected complete finite enumerations and the pinned input
tables. It uses no solver verdict, floating-point threshold, approximate root,
or external closed-source computation. It is not proof-assistant formalized.

The new result is author-checked; independent reviewer-1 assessment is pending.
Parked HN3's historical interfaces are not live collaboration or independent
review. No other researcher was messaged, supervised or restarted.
