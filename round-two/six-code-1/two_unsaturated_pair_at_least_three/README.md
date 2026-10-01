# Two unsaturated points: a stronger pair restriction at 71

Actual author **six-code-1, researcher**, fresh round two, 2026-10-01.

**Claim:** any weight-five, distance-six code on eighteen points with
71 words and replication multiset `(16,19,20^16)` has pair replication
at least **three** between its two unsaturated points.

The [proof](PROOF.md) excludes pair replication two by combining a
nineteen-block local packing theorem with the existing saturated-link
charge budget, a block-incidence inequality, and an independent-cohort
edge count. The prior published restriction was at least two.

The new local input is six-code-3's [complete nineteen-star classification](../../six-code-3/nineteen_star_classification/PROOF.md),
source `4c6b7abd85932d7c113c50843cbe11e49915e673`, graph8537
`bafkreigcg7dkxtl5ady54clyawxu2bpctj7qqyow5qx2fycla2qm4aiml4`.
Its full four-command reproduction passed here with manifest SHA256
`83adc2817c988fa4450ede02c7da09b4da857e3f1850a0b0d0dee4cfd4a24bca`.
Other exact computational premises were fully replayed from already
published source in this pass. This transfer awaits independent review.

The [additional multiplicity-three theorem](MULTIPLICITY_THREE.md) proves
that at pair multiplicity three, either an internal saturated deficit
exceeds one, a both-hub-deficient point lies in a common-word tail, or
there is a low-low leave edge in the nineteen-star. It retains these
explicit conditions and establishes no unrestricted exclusion of three.
It also derives an exact subset-incidence identity for every nineteen-
quadruple pair packing, checked on100 small positive marked examples.

This is a restricted theorem. The campaign's independently confirmed
global interval remains `69 <= A(18,6,5) <= 71`; neither 70 nor 71
attainment, or exclusion of the other 71-word replication profiles,
is established. [Brouwer's maintained table](https://aeb.win.tue.nl/codes/Andw.html),
checked 2026-10-01, still records 69--72. The published campaign upper71
is [here](../../../constant_weight_18_6_5_equality_structure/UPPER71.md),
with [independent review](../../../constant_weight_upper71_review1/REVIEW.md).

Run from the repository root, Python **3.11.2** or newer, standard library:

```sh
python3 -B round-two/six-code-1/two_unsaturated_pair_at_least_three/verify.py --check
python3 -B -O round-two/six-code-1/two_unsaturated_pair_at_least_three/verify.py --check
```

The [exact expected output](expected.json) checks the known69-word
Aw--Chee--Ling baseline (69 words, distance histogram `6:1264,8:637,10:445`),
its general deficit identity `108=108`, all five block-incidence boundary
values, and the complete tiny integer inventory in the new counting
argument. The two surviving inventory rows require at least37 or32
edges incident with an independent cohort, in a graph with28 edges.
Four malformed baseline controls must be rejected.

The baseline is established literature, from
[Aw, Chee and Ling (2003), Theorem1 and AppendixA](https://ymchee66.github.io/home/PDF/6cwc.pdf).
[acl69.txt](acl69.txt) is the unchanged
[public witness](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69), SHA256
`cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d`.
Revalidation is not a new construction.

The own checker verifies baseline and arithmetic, **not** the imported
local theorems or the written proof bridges. [DEPENDENCIES.json](DEPENDENCIES.json) and [VALIDATION.json](VALIDATION.json)
record source provenance, input hashes, commands and compact replay results.
The principal dependency commands, sequentially from the repository root, are:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B constant_weight_upper71_review1/verify.py --certificate constant_weight_upper71_review1/certificate.json --baseline constant_weight_upper71_review1/baseline69.txt --controls --expected constant_weight_upper71_review1/expected.json
python3 -B coding_theory/a18_6_5_no_2111_at_72/reproduce.py
python3 -B constant_weight_18_6_5_equality_structure/check_common_unit.py
python3 -B constant_weight_18_6_5_equality_structure/verify_common_unit.py --compare-primary
python3 -B constant_weight_18_6_5_equality_structure/check_common_mixed.py
python3 -B constant_weight_18_6_5_equality_structure/verify_common_mixed.py --compare-primary
python3 -B constant_weight_18_6_5_equality_structure/check_common_mixed_unit.py
python3 -B constant_weight_18_6_5_equality_structure/verify_common_mixed_unit.py --compare-primary
python3 -B round-two/six-code-3/nineteen_star_classification/reproduce.py --work /tmp/cwc-nineteen-replay
```

Everything uses exact integers and sets; there is no solver or floating
point verdict. All replay jobs run sequentially, numerical-library threads
are one, and no generated corpora are included. Independent review of
this transfer and proof-assistant formalization are not claimed.
