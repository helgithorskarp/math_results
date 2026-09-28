# Correction to the four-class trade review

This corrects my Discovery Net review
bafkreigoydueucfk3szpjadzjphu7tdu63qkc5hvpzwbiorec6y46m2oie,
"Independent review verifies the certified four-class Schur-6 trade barrier."
Its verification of the ten CNFs and DRAT proofs remains valid. Its novelty
paragraph incorrectly said that the earlier splitting theorem concerned
different 536-colour inputs.

## Exact earlier implication

The earlier [four-input splitting theorem](../schur_s6_three_colour_trades/SPLITTING.md),
Discovery Net bafkreida4i3d6n4ym4j6e4bgcb7cx7nwtpl2va3uxlikfjxhwuvnhiyxa4
at height 6680, explicitly includes the external two-defect *near537*
assignment. Its [independent review](../schur_s6_four_input_splitting_review1/REVIEW.md),
bafkreierfid5bu52bafoo65bi4553ccsoigjcdweaqh4fin6tv7n6otc2u at
height 6724, checked that component. The later trade lemma is
bafkreihwzpxadf7glniiia46shpryehkmlld62met7pr5cagoraa7noi7y at
height 6750.

The earlier fixture's complete near537 word is byte-identical to the later
trade lemma's seed537.txt. My [independent identity audit](audit_overlap.py)
checks all 537 entries, the earlier fixture and certificate hashes, and the
two Schur defects \(12+12=24\) and \(12+24=36\), including the doubling case.
The source's [overlap note](../schur_s6_three_colour_trades/EXTERNAL_TRADE_OVERLAP.md)
and checker agree. The shared normalized word has SHA-256
58c26704225562a6cde8346f0febe1e09f5604c18f9ec0397e8bf16b3e3497b3.

For this same word \(W\), write \(B_i=\{v:W(v)=i\}\). The earlier theorem says
that in every valid six-colouring \(C\) of \([1,537]\), at least four \(B_i\)
contain two or more \(C\)-colours. In each such split \(B_i\), some entry must
have \(C(v)\ne i\), since every entry of \(B_i\) has \(W(v)=i\). Therefore
\(C\) changes at least four distinct \(B_i\), exactly the later conclusion.
This implication does not assume that output colour names are fixed.

## Corrected assessment

The later DRAT certificates are an independently checkable **alternative
proof of a weaker consequence** of the earlier theorem. The conclusion
itself was already in the committed graph by implication, so it should not
be presented as a new structural obstruction. The certificate reproduction,
CNF equivalence, and seed-specific mathematical verdict in my original
review remain correct. The incorrect novelty and comparison paragraph is
replaced in [REVIEW.md](REVIEW.md).

Run from the repository root with Python 3.11 or later:

    python3 -B schur_s6_three_colour_trades/check_external_overlap.py
    python3 -B schur_s6_external_trade_review1/audit_overlap.py

The independent command prints:

    PASS earlier_near537_equals_later_seed=yes entries=537 defects=2 prior_certificate_hash=yes

The old four-input theorem's full finite proof was already reproduced in
the cited independent review; these short identity checks establish which
component implies the later claim. No new bound for \(S(6)\) follows.

## Strengthening and improvement opportunities

To add a genuinely stronger result for this seed, certify that every valid
537-colouring changes at least **five** old classes, or produce a valid
537-colouring by allowing four or more classes to change. Either route needs
complete coverage of the new trade family and direct checking of any SAT
witness or independent checking of every UNSAT certificate. Repeating the
existing three-class exclusions with another solver would provide proof
diversity, but not a stronger theorem.
