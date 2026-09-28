# A certified two-defect floor for three-class S(6) trades

## Exact statement

Let `W=seed537.txt` assign one of six colours to every integer in `[1,537]`,
and let `B_i={v:W(v)=i}`. A valid *classical* Schur six-colouring has no
monochromatic `x+y=z`, **including `x=y`**.

**Strengthened computer-assisted lemma.** Every six-colour word `C` on
`[1,537]` with **at most one** monochromatic Schur triple differs from `W` at
some entry of at least **four distinct** sets `B_i`. Equivalently, the minimum
number of violations among all words changing entries in at most three seed
classes is exactly **two**, attained by `W` itself. The earlier zero-defect
case remains separately reproducible with `verify.py`.

This is a seed-specific obstruction, not an upper bound for `S(6)` and not a
valid 537-colouring. It places no limit on the number of entries changed within
a selected class or on the replacement colours. The source word itself has
exactly two violations, `12+12=24` and `12+24=36`, both in `B_4`; the class
sizes are `93,163,119,35,63,64`.

The seed is the normalized form of
[umaia1234's public two-violation file](https://github.com/umaia1234/agentic-conjectures/blob/main/problems/schur-6/near_537_two_violations.col).
The original six-line file has SHA-256
`ece0ce91784aca0199ffe24e36104c666c036a6c735181385fd2fabcc7627f25`.
Its class-by-class parsing, exact partition check, and normalization are
recorded in the preceding
[independent-seed checkpoint](https://github.com/helgithorskarp/math_results/tree/main/schur_s6_nonlocal_doubling_search).
The normalized `seed537.txt` here has SHA-256
`58c26704225562a6cde8346f0febe1e09f5604c18f9ec0397e8bf16b3e3497b3`.

The earlier [four-input splitting theorem](https://github.com/helgithorskarp/math_results/blob/main/schur_s6_three_colour_trades/SPLITTING.md)
already implies the four-changed-class conclusion for valid colourings of
this same word. Its external fixture is byte-identical to `seed537.txt`, as
documented in the [overlap audit](https://github.com/helgithorskarp/math_results/blob/main/schur_s6_external_trade_review1/CORRECTION.md).
The strengthened result here covers **every word with at most one defect**
and proves the exact two-defect minimum for this three-class trade family.

## Reduction and certificate

Any valid `C` must change `B_4`, since otherwise the two displayed defects
remain. If `C` changes entries in at most three seed classes, all changed
classes lie in one of the ten three-element subsets of `{1,...,6}` that
contain `4`. For each such subset, `verify.py` constructs a CNF for *every*
recolouring of the selected classes while fixing all other entries to `W`.
All ten CNFs are UNSAT with independently checked DRAT proofs.

For each free vertex `v`, the variables `p(v,c)` have exactly-one clauses
over `c=1,...,6`. The 72,092 unordered Schur triples are enumerated as
`x<=y`, `x+y<=537`; `x=y` uses the two distinct vertices `{x,2x}`. For a
triple whose fixed vertices have at least two different colours, no clause is
needed. If its fixed vertices all have colour `c`, one clause prevents all
its free vertices from taking `c`. If it has no fixed vertex, one clause for
each `c` prevents all its vertices from taking `c`. Therefore the CNF is
satisfiable exactly when a valid colouring exists with changes restricted to
the chosen seed classes. The code independently checks the seed defects and
class sizes before generating any CNF.

Glucose3 generates a proof for each UNSAT result. The separate `drat-trim`
program checks each proof against the exact DIMACS file. `expected.json`
records the number of free entries and clauses, solver conflicts, and SHA-256
hashes and byte lengths of the ten CNFs and proofs. These earlier proofs total about
3 MB and are regenerated into a temporary directory, rather than stored in
the repository. The logical trust boundary is the stated CNF reduction and
the independent DRAT checker; the solver's UNSAT status alone is not used as
evidence.

## Reproduction

Tested with CPython 3.11.2, `python-sat==1.9.dev15` (bundled Glucose3), and
the official [`drat-trim` source](https://github.com/marijnheule/drat-trim)
at commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.
From this directory:

```sh
sha256sum -c SHA256SUMS
python3 -m venv /tmp/schur-s6-trade-venv
/tmp/schur-s6-trade-venv/bin/python -m pip install -r requirements.txt
git clone https://github.com/marijnheule/drat-trim.git /tmp/schur-s6-drat-trim
git -C /tmp/schur-s6-drat-trim checkout 2e3b2dc0ecf938addbd779d42877b6ed69d9a985
make -C /tmp/schur-s6-drat-trim
/tmp/schur-s6-trade-venv/bin/python -B verify.py --drat-trim /tmp/schur-s6-drat-trim/drat-trim
```

The last command prints `UNSAT, DRAT VERIFIED` for groups `124,134,145,146,`
`234,245,246,345,346,456`, then
`PASS all_ten_three_class_trades_unsat=10 drat_verified=10`.
It also compares every regenerated CNF and proof to `expected.json` byte for
byte through SHA-256 hashes. Differences in solver versions may alter proof
bytes even when a new proof passes DRAT; use the pinned version for exact
hash reproduction.

The published lower bound remains `S(6)>=536` from
[Fredricksen–Sweet (2000)](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32).

## Stronger at-most-one-defect certificate

`verify_one_defect.py` strengthens the trade reduction by allowing an
arbitrary one of the 72,092 classical Schur triples to be monochromatic. For
each triple that is not already safe because of two differently coloured
fixed vertices, it introduces a selector `t_e`. Every clause forbidding a
monochromatic colour on that triple gets `t_e` as an extra positive literal.
Thus a monochromatic triple forces its selector to true. A sequential
at-most-one counter constrains all selectors, with one auxiliary prefix
variable per selector except the last. Conversely, any recolouring with at
most one monochromatic triple satisfies the CNF by selecting just that triple.
The CNF is therefore satisfiable **exactly when** a trade of the chosen seed
classes has at most one violation.

Any word with at most one violation must change `B_4`, because both seed
defects lie entirely in that class. Hence any trade changing at most three
classes is covered by one of the ten checked three-class groups containing 4.

All ten three-class CNFs containing class 4 are UNSAT. Nine proofs were
generated by Glucose3 in `python-sat==1.9.dev15`. The difficult `124` case
used the official CaDiCaL command-line solver, release 1.9.5 at commit
`146207318796f094dcded87349a64f0c6927309e`, to write a text DRAT proof
directly. All ten proofs passed independent `drat-trim` verification.
`expected_one_defect.json` gives the exact CNF and proof SHA-256 hashes,
counts, and byte lengths. The largest proof is 34,823,786 bytes; generated
proofs are deleted after checking and are not committed.
Proof bytes can vary with a different solver build; the committed hashes pin
the stated releases and tested build, while DRAT verification carries the
logical conclusion.

After the tools in the preceding reproduction section have been installed,
build the pinned [CaDiCaL source](https://github.com/arminbiere/cadical) and
run the strengthened check from this directory:

```sh
git clone --depth 1 --branch rel-1.9.5 https://github.com/arminbiere/cadical.git /tmp/schur-s6-cadical-195
(cd /tmp/schur-s6-cadical-195 && ./configure)
make -C /tmp/schur-s6-cadical-195 -j4
/tmp/schur-s6-trade-venv/bin/python -B verify_one_defect.py --cadical /tmp/schur-s6-cadical-195/build/cadical --drat-trim /tmp/schur-s6-drat-trim/drat-trim
/tmp/schur-s6-trade-venv/bin/python -B audit_one_defect.py
```

The certificate command ends with
`PASS at_most_one_defect_trades_unsat=10 drat_verified=10`. For a quicker
independent sample, append `--group 456` (or another listed group); each case
is checked against its own committed hashes. The exact minimum of two is
specific to this seed and its three-class trade family. It gives neither a
valid 537-colouring nor an unrestricted proof that 537 is impossible.
The audit independently recounts forced defect selectors on 22 seed-based
assignments and exhaustively checks the at-most-one counter's truth table
through five inputs.
