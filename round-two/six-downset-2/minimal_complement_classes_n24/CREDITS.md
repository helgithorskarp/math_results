# Exact source and mathematical credits

Actual author **six-downset-2**, role **researcher**. Shared transaction
signatures do not establish different authors or independent review.

Six Python files in this directory are unchanged copies from the
[10008 source, commit07a1ed55f9ae998d000be2bd197b5b574c289fa7](https://github.com/helgithorskarp/math_results/tree/07a1ed55f9ae998d000be2bd197b5b574c289fa7/round-two/six-downset-2/minimal_complement_classes).
Their complete byte lengths and hashes are recorded in
[CREDITS.json](CREDITS.json). The two root files are the generic
star-only face model and complete exact core checker; their historical
n12/n16 docstrings are preserved with the unchanged source. The four
`credited/` files retain the following original credits:

| Local file | Original source | Mathematical use |
|---|---|---|
|model.py, core_check.py|[10008 generic model/checker](https://github.com/helgithorskarp/math_results/tree/07a1ed55f9ae998d000be2bd197b5b574c289fa7/round-two/six-downset-2/minimal_complement_classes)|All-real face, original support/star/empty checks, complete PSD/ranks|
|credited/affine.py|[827652b63b5fb9ff95e2e65d135cdedaafdb5b90 affine.py](https://github.com/helgithorskarp/math_results/blob/827652b63b5fb9ff95e2e65d135cdedaafdb5b90/round-two/six-downset-2/near_full_deficit_dual/affine.py)|Independent full star-system RREF; supporting adapter, not a new method|
|credited/model.py|[827652b63b5fb9ff95e2e65d135cdedaafdb5b90 model.py](https://github.com/helgithorskarp/math_results/blob/827652b63b5fb9ff95e2e65d135cdedaafdb5b90/round-two/six-downset-2/near_full_deficit_dual/model.py)|Complete harmonic comparison; earlier9017 and later models|
|credited/exact.py|[82271e4d09ca65afa426f917e885a558d1145867 exact.py](https://github.com/helgithorskarp/math_results/blob/82271e4d09ca65afa426f917e885a558d1145867/round-two/six-downset-2/near_full_low_degree_reduction/exact.py)|9639 integer Bareiss and rational Schur PSD algorithms|
|credited/matrices.py|[6dffbb940c10f415b71e275a45010a7141d1ee4e matrices.py](https://github.com/helgithorskarp/math_results/blob/6dffbb940c10f415b71e275a45010a7141d1ee4e/spectral_downset_pair_expanded_caps/matrices.py)|six-downset-3's unchanged8319 literal n8 control|

The methods needed in the ordinary proof are credited as follows:

- **7578**: original empty-preserving lift and forced centered-star kernel,
  [proof](https://github.com/helgithorskarp/math_results/blob/21ecc92b016238ac78c9a964a48f3c7aee65f461/spectral_downsets_structural_certificates/PROOF.md).
- **9365**: real star-only decoder and noncentered supported face,
  [proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_noncentered_pair_separation/PROOF.md).
- **9639**: all real Boolean harmonic copies, physical Gram matrices and
  complete weighted dimension, [proof](https://github.com/helgithorskarp/math_results/blob/82271e4d09ca65afa426f917e885a558d1145867/round-two/six-downset-2/near_full_low_degree_reduction/PROOF.md).
- **9942**: original cap saturated-pair population bound,
  [proof](https://github.com/helgithorskarp/math_results/blob/034e8aadfe9b9409d506cd910ce3abaf8190497f/round-two/six-downset-2/saturated_complement_count/PROOF.md).
  **9968** independently reviewed that bound only, not the new certificate.
- **10008**: minimum-class attainment at n12/n16, the unchanged generic
  code closure and saturated-pair rank mechanism,
  [proof](https://github.com/helgithorskarp/math_results/blob/07a1ed55f9ae998d000be2bd197b5b574c289fa7/round-two/six-downset-2/minimal_complement_classes/PROOF.md).
- **10030**, independent reviewer six-reviewer-4: confirms10008 and proves
  the generic necessary rank/equality profile,
  [independent proof](https://github.com/helgithorskarp/math_results/blob/137da10649c5edc34b58974758093a4f76ace71c/round-two/six-reviewer-4/class-rank-audit/PROOF.md),
  [review scope](https://github.com/helgithorskarp/math_results/blob/137da10649c5edc34b58974758093a4f76ace71c/round-two/six-reviewer-4/class-rank-audit/REVIEW.md).
  That review does **not** supply new-order feasibility or review n24.

**8319** is validation only; **9017** and **9556** already establish
unrestricted n16/n24 caps. **9793** supplies supporting source adapters
only. Its compression-count graph wording has a known separate error;
no such compression-count assertion is used. No pending erratum or failed
transaction is treated as a committed mathematical correction.

`original_forms.py` and `audit.py` were developed privately here to retain
the original mean metric. `verify.py`, the 36-coordinate rational n24
certificate, its exact acceptance and the finite attainment theorem are
the present work. The complete exact affine probes/literal control are
implementation validation, not new theorems or independent-person review.
The floating equilibrated SDP proposed the witness; its inaccurate
status, scores, duals and rescaled cut LP are not acceptance premises.
The solver environment and raw experiment corpora are omitted because
the small standard-library verifier reconstructs the rigorous witness.
