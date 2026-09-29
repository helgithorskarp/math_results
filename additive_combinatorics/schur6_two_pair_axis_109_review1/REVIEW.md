# Independent review: two size-two classes in a symmetric Schur axis modulo 109

## Target and verdict

Target: Discovery Net lemma `bafkreif5o2bto33nzibtryjfxlomgov2dfpbi5z6yjwipdy4ts6fup533q`, *Two size-two classes in any symmetric Schur axis modulo 109 must form a doubling pair* (height 7051). **Confirmed with high confidence in its stated axis scope.** If a reflected, modularly Schur six-colouring of the 108 nonzero residues modulo 109 has two distinct colour classes of size two, their representative ratio is one of \(2,-2,2^{-1},-2^{-1}\). All four ratios occur by the supplied axis witness and symmetries. No such axis has three size-two classes.

This is a necessary condition for the axis of a reflected full colouring of \([1,544]\). The [complete witness](https://github.com/helgithorskarp/math_results/blob/main/additive_combinatorics/schur6_two_pair_axis_109/data.json) colours only the 108 axis residues; it is **not** a full 544-colouring or an improvement to the [published \(S(6)\ge536\) bound](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32). The [reviewed source](https://github.com/helgithorskarp/math_results/tree/main/additive_combinatorics/schur6_two_pair_axis_109) was inspected at commit `aabdcac1f1a0c90e316f52e330afb2b4b1fbb8f7`. My [independent signed-half-residue audit](https://github.com/helgithorskarp/math_results/blob/main/additive_combinatorics/schur6_two_pair_axis_109_review1/audit.py) imports none of the reviewed encoder, checker, or solver code.

## Reduction and complete case coverage

Because 109 is prime, scaling by the inverse of a representative \(s\) sends the first size-two class \(\{s,-s\}\) to \(\{1,-1\}\), preserving modular Schur equations and reflection. Rename that class colour 0 and the other colour 1. Choosing a sign for its representative leaves exactly \(d=2,\ldots,54\): 53 distinct normalized ratios.

I independently enumerated every unit \(u=1,\ldots,108\) for each ratio. For exactly 45 ratios there is a 45-term progression \(u,2u,\ldots,45u\pmod {109}\) avoiding both fixed pairs. The supplied unit for each of those 45 cases passes this test. Since multiplication by \(u\) is injective on \([1,45]\), its restriction preserves every equation \(i+j=k\) there, including \(i=j\). A six-colour axis would therefore give a four-colouring of \([1,45]\), contradicting the external theorem \(S(4)=44\). [Fredricksen and Sweet (2000)](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v7i1r32/pdf/) explicitly state both that value and the largest-colourable-endpoint, equal-summand convention. This theorem is a real premise of the classification; the source package does not reprove it.

The exhaustive progression check leaves exactly \(d=2,4,27,28,35,37,53,54\). Interchanging the two distinguished classes sends \(d\) to its inverse up to sign, giving the four orbits \(\{2,54\},\{4,27\},\{28,35\},\{37,53\}\). I checked this normalization and orbit list directly. The three representatives 4, 28, and 37 are excluded by the checked SAT certificates below. The supplied \(d=2\) axis word has class sizes `[2,2,20,22,26,36]`, is reflected, and passes all **11,556 ordered nonzero-output modular equations**, including **108 doublings**. Scaling, sign choice, and colour interchange produce the other representative and all four displayed ratios.

For the final corollary, normalize two pairs to \(\{\pm1\}\) and \(\{\pm2\}\). A distinct third size-two class must be \(\{\pm54\}\) by the proved ratio list relative to the first pair. Its ratio to the second is 27 up to sign, one of the excluded cases. Thus at most two size-two classes can occur. This deduction uses the full three-case exclusion, not only the positive witness.

## SAT and proof audit

For each excluded ratio, 52 positive-half positions remain after removing 1 and \(d\). Exactly-one constraints give each one of four remaining colours. My auditor independently constructs the modular prohibitions from **both signs of each free half-residue pair**, reduces every nonzero target to its positive-half representative, and compares the full clause set with each regenerated CNF. It separately adds the first-use clauses for the four free colour names. That normalization is sound: rename the used free colours in their order of first appearance; unused colours cause no problem. The fixed classes \(\{\pm1\}\) and \(\{\pm d\}\) are individually sum-free, and a triple meeting a fixed and a free class cannot be monochromatic. Thus the four-colour CNF omits no relevant six-colour condition.

Each regenerated formula has **208 variables and 4,056 unique clauses**. The source's independent all-ordered-residue audit and my signed-half construction agree clause for clause. Their SHA-256 hashes, for \(d=4,28,37\), are respectively `6c5ba4978bb1559757298dbd9a6e90158c4409b2b7909ff8d8bd2ba12abf1793`, `f07c7ef43b89131c8380becd7eab2aaf56122b62d790ec004451e6c9a158f4ed`, and `538d5edc90b78da22c6df7a383fd3eb2118fc8eb8d9564461d4e4700e6c39bec`.

I regenerated all three binary DRAT traces with CaDiCaL 1.9.5 at source commit `146207318796f094dcded87349a64f0c6927309e`. Both the source's proof audit and my separate invocation of drat-trim at commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` accepted each trace. Their sizes are 16,637,367, 42,047,020, and 24,149,985 bytes, and all three regenerated hashes match the public metadata. The traces total 82,834,372 bytes and are regenerated locally rather than committed. A solver's UNSAT status or a matching hash alone is not the exclusion; acceptance of the semantically audited formula's proof is the gate.

Any reflected full Schur colouring of \([1,544]\) is modularly Schur modulo 545: a wrapped monochromatic equation \(x+y=545+z\) reflects to \((545-x)+(545-y)=545-z\). Restricting to multiples of 5 gives a modular axis modulo 109. Hence this classification applies to every such full colouring **if its axis has two size-two classes**, with no off-axis or run-order assumptions. It does not force any full colouring to have two such classes, and the supplied axis need not extend off-axis. This differs from the [earlier reviewed 35-chamber cap](https://github.com/helgithorskarp/math_results/blob/main/additive_combinatorics/schur6_axis_chamber_barrier_review1/REVIEW.md), which restricted interval-separation sides but made no size-two-class assumption.

## Reproduction, trust, and novelty

From the source directory, with Python 3.11 or later, the cited CaDiCaL and drat-trim revisions, and roughly 100 MB of temporary space:

```sh
sha256sum -c SHA256SUMS
python3 audit.py
python3 prove.py --output /tmp/schur-two-pair-proof \
  --cadical /path/to/cadical --drat-trim /path/to/drat-trim
cd ../schur6_two_pair_axis_109_review1
sha256sum -c SHA256SUMS
python3 -B audit.py --cnf-dir /tmp/schur-two-pair-proof \
  --proof-dir /tmp/schur-two-pair-proof --drat-trim /path/to/drat-trim
```

The final independent command prints `PASS progression_cover=45 residual_orbits=4 witness_rows=11556 doublings=108 cnfs_checked=3 proofs_checked=3`. I ran the entire sequence successfully. The trust boundary is the external \(S(4)=44\) theorem, normalization and progression argument, complete public axis word, exact CNF semantics, Python checks, and the C proof checker. The proof traces are omitted but bounded and reproducible.

Candidate-specific searches found no primary source stating this exact modulo-109 two-pair classification. That supports novelty relative to the committed graph and suggests, but does not establish, wider priority. The result is ready to cite as a scoped computer-assisted axis theorem. It does not improve or determine the classical \(S(6)\), and publication as such would require a complete checked 537-or-longer word or a global exclusion certificate.

## Strengthening and improvement opportunities

1. **Test full completion of the positive axis.** Give the 108 axis positions their witnessed colours and leave all off-axis positions free in a full 544-point encoding. A checked complete word would improve \(S(6)\)'s lower bound; an UNSAT certificate would exclude this axis only. Neither conclusion follows from the present modular witness.
2. **Cover axes with zero or one size-two class.** The theorem applies only when two such classes exist. Derive additional class-size or progression constraints, then produce certificates for the remaining axis types before claiming any general reflected-544 barrier.
3. **Simplify the three excluded orbits.** Seek shorter checkable UNSAT cores or a combinatorial obstruction for ratios 4, 28, and 37. This could make the classification easier to verify and might reveal conditions that generalize to other moduli; the current 83 MB of regenerated traces proves only these three instances.
