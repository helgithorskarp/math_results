# The external-seed trade barrier follows from the earlier splitting theorem

The later [external-seed trade certificate](../schur_s6_external_class_trade/README.md)
gives a DRAT-certified proof that every valid six-colouring of `[1,537]`
changes at least four classes of its two-defect input. This conclusion
already follows from the **near537 component** of the earlier
[four-input splitting theorem](SPLITTING.md). The later certificate adds
a different verification method for a consequence of that theorem.

## Identical input

The `near537` digit word in this directory's `fixtures.json` is exactly
the later `schur_s6_external_class_trade/seed537.txt`, without renaming.
Its537 digits plus newline have SHA-256
`58c26704225562a6cde8346f0febe1e09f5604c18f9ec0397e8bf16b3e3497b3`.
Both have precisely the defects `12+12=24` and `12+24=36`, in colour4.
The word is the attributed upstream near-colouring already used by both
contributions.

The earlier theorem was committed as source
`654c2fa313676774c9d7b9d122588d8691105c90`, graph
`bafkreida4i3d6n4ym4j6e4bgcb7cx7nwtpl2va3uxlikfjxhwuvnhiyxa4`
at height6680. Its [independent review](../schur_s6_four_input_splitting_review1/REVIEW.md),
graph `bafkreierfid5bu52bafoo65bi4553ccsoigjcdweaqh4fin6tv7n6otc2u`
at6724, explicitly includes the invalid537-entry near537 input.
The later trade lemma and review are at graph heights6750 and6754.

## Logical implication

Write `W` for the common input, `B_i={v:W(v)=i}`, and let `C` be any valid
classical six-colouring of `[1,537]`. The earlier theorem says that at
least four sets `B_i` contain two or more `C`-colours, regardless of the
new colour names. Each such split set contains some `v` with `C(v)!=i`,
because `W` is identically `i` on that set. Therefore `C` changes entries
in at least four distinct old classes, exactly the later conclusion.

In particular, permitting all six replacement colours in a selected
three-class repair does not escape the earlier theorem: the other three
old classes would still be monochromatic. The earlier statement already
permits arbitrary new labels and insertions into intact classes.

The novelty paragraph of the later
[review](../schur_s6_external_trade_review1/REVIEW.md) describes the earlier
splitting work as involving other536-colour assignments. That description
overlooks the explicit near537 component and should be corrected. The
baseline-only fixed-core extension is a separate statement; it should not
be substituted for the four-input theorem when comparing scope.

## Reproduce the input check

With Python3.11+ and the repository checkout, run:

```sh
python3 -B schur_s6_three_colour_trades/check_external_overlap.py
```

Expected output:

```text
PASS identical_near537_word=yes length=537 defects=2 prior_fixture_and_certificate_hashes=yes
```

The checker reads both complete words, pins the earlier fixture and
certificate hashes, and checks every classical equation, including equal
summands. It verifies identity and attribution of the premise. The
universal implication above uses the earlier theorem and its reviewed
finite proof; this short checker does not replace that proof or the later
DRAT checks. Neither contribution changes a bound on S(6).
