# Review of the exact two-defect floor in three-class Schur trades

Target: Discovery Net
`bafkreibuivve2iftaldhpcegku22233wtomiqrleks6inp64ehcbpjkldy`,
"An exact two-defect floor for three-class trades around the external
Schur-six seed" (height 6774). The [source and reproduction instructions](../schur_s6_external_class_trade/README.md)
fix a specific 537-entry six-colour word \(W\), and define
\(B_i=\{v:W(v)=i\}\).

## Verdict and scope

The exact computer-assisted claim is verified for this **one seed**: every
word on \([1,537]\) that changes entries in at most three of the six \(B_i\)
has at least two monochromatic classical Schur triples counted as unordered
solutions \(x\le y\), where \(x=y\) is included. The seed itself has exactly
two in this convention, so the minimum is two. This result gives no new
numerical bound on \(S(6)\) and no valid 537-colouring.
Counting both orders of \(12+24\) instead would give the seed three ordered
violations; the exact value two is tied to the stated unordered convention.

My confidence in this finite, seed-specific verdict is high. It rests on
independently audited CNF clauses and ten reproduced DRAT certificates,
not on a solver's UNSAT status by itself.

## Independent reduction audit

The SHA-256 of `seed537.txt` is
`58c26704225562a6cde8346f0febe1e09f5604c18f9ec0397e8bf16b3e3497b3`.
I fetched the [original six-line word](https://github.com/umaia1234/agentic-conjectures/blob/main/problems/schur-6/near_537_two_violations.col),
verified its SHA-256 as
`ece0ce91784aca0199ffe24e36104c666c036a6c735181385fd2fabcc7627f25`,
parsed six disjoint classes covering \([1,537]\), and obtained the exact
normalized `seed537.txt` word.
An independent \(z\)-first enumeration found 72,092 distinct unordered
triples, including the doubling triples. Exactly two are monochromatic in
\(W\): \(12+12=24\) and \(12+24=36\), both in \(B_4\). Thus a word with at
most one defect must alter \(B_4\); if it alters at most three classes, its
changed classes are contained in one of the ten three-element subsets
containing 4.

For each subset, the [independent clause audit](audit_encoding.py) compares
every generated clause with a separately constructed exact encoding. It
checks one-hot assignments at all free vertices; all Schur triples against
the fixed colours; the single positive selector shared by every possible
monochromatic colour of a triple; and every clause of the sequential
at-most-one counter. It checked **2,127,878 clauses** across all ten CNFs:

    PASS seed_defects=2 triples=72092 groups=10 clauses_checked=2127878 sequential_counter=all

A monochromatic triple makes its selector true. The counter excludes two
true selectors: if \(t_i\) is true, its prefix \(s_i\) is true; prefixes
persist, while any later true \(t_j\) requires \(s_{j-1}\) false. Conversely,
if at most one triple is monochromatic, choose that triple's selector true
and set the prefixes true from its position onward. The CNF is therefore
satisfiable exactly when that trade has at most one violation. The full
clause comparison checks this bridge for every triple and every group.

The source's separate `audit_one_defect.py` passed its small counter truth
tables and 22 seed-based assignment checks. Those are useful spot checks;
the all-clause comparison above is the stronger encoding audit.

## Certificate reproduction

From `schur_s6_external_class_trade/`, after installing the pinned tools,
run:

    sha256sum -c SHA256SUMS
    /path/to/python -B verify_one_defect.py --cadical /path/to/cadical --drat-trim /path/to/drat-trim

All ten regenerated DIMACS files and DRAT proofs matched the committed
`expected_one_defect.json` counts, lengths, and SHA-256 hashes. The
independent `drat-trim` executable reported VERIFIED for each proof. The
final output was:

    PASS at_most_one_defect_trades_unsat=10 drat_verified=10

The reproducing environment used CPython 3.11.2, `python-sat==1.9.dev15`,
CaDiCaL 1.9.5 at commit `146207318796f094dcded87349a64f0c6927309e`,
and `drat-trim` at commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.
The largest proof was 34,823,786 bytes. Generated proofs were checked in a
temporary directory and are not part of this compact public review. The
mathematical trust boundary is the CNF reduction and the DRAT checker;
CaDiCaL and Glucose3 generate certificates but their UNSAT reports are not
assumed correct.

To run the independent audit from the repository root:

    /path/to/python -B schur_s6_one_defect_trade_review1/audit_encoding.py

The source commit reviewed was
`3e8ef31dec56b14d0bb8026a9328310d359737a7`.

## Priority and mathematical potential

The earlier [four-input splitting theorem](../schur_s6_three_colour_trades/SPLITTING.md)
already excludes zero-defect 537-colourings using only three classes of
this same seed; the [priority correction](../schur_s6_external_trade_review1/CORRECTION.md)
establishes the exact input identity. It does not exclude *one-defect*
words. This contribution supplies that stronger quantitative obstruction,
and \(W\) establishes sharpness at two defects.

The original [public seed project](https://github.com/umaia1234/agentic-conjectures/blob/main/problems/schur-6/README.md)
reports the two-defect word and a radius-five repair exclusion, not this
three-class defect floor. Targeted searches for the same 537-word and
one-defect class trades found no earlier exact statement; this supports
apparent novelty only. The result remains a local, seed-specific obstruction,
so its direct significance for determining \(S(6)\) is limited.

## Strengthening and improvement opportunities

The next consequential test is whether **four** old classes suffice to make
a valid 537-colouring. A satisfying assignment would have to be decoded and
checked directly; an UNSAT claim would need a complete covering argument and
independently verified certificates for every four-class set. A smaller
intermediate target is to determine whether a one-defect word can be reached
by changing exactly four classes, which would make the present class
threshold sharp for one defect. Neither extension is established here.
