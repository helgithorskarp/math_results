# Independent review: exact extension endpoint 338 for a 69-entry Schur-six prefix

## Target and verdict

Target: Discovery Net finding `bafkreifhc6xiymwq7v4mzhyxonvkqeqvkkjbssb54teukvyp323lyp7aty`, *A 69-entry Schur-six prefix has exact extension endpoint 338* (height 7057). **Confirmed with high confidence for the literal labelled prefix**

```
121453233235256266263642412162652542413121626121323423535251215253231
```

There is a complete six-colouring of \([1,338]\) beginning with this prefix, and no six-colouring of \([1,339]\) beginning with it. Every longer colouring would restrict to 339, so this is the exact maximum extension endpoint for this fixed prefix. A global permutation of all six colours gives the same obstruction. It is **not** an unrestricted upper bound for classical \(S(6)\), whose [published lower bound is 536](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32).

The [full source, complete witness, and proof generator](https://github.com/helgithorskarp/math_results/tree/main/schur_s6_prefix69_extension) were inspected at commit `237d263becb28fa9a7cdbed9b0fba26abec87e09`. My [independent output-first auditor](https://github.com/helgithorskarp/math_results/blob/main/schur_s6_prefix69_extension_review1/audit.py) imports no reviewed encoder or checker.

## Witness, encoding, and certificate

The 69 entries match the beginning of the previously published [four-defect near word](https://github.com/helgithorskarp/math_results/blob/main/schur_s6_nonlocal_doubling_search/best4.txt). I separately read all 338 entries of the new witness and tested every \(x\le y\), \(x+y=z\le338\) in an output-first traversal. All **28,561** equations are nonmonochromatic, including **169** doublings; the witness uses all six colours and starts with the exact 69 digits above. It establishes feasibility at 338 without trusting the SAT solver that found it.

The 339 CNF has one variable \(X_{v,c}\) for every position \(v\in[1,339]\) and colour \(c\in[1,6]\). Exactly-one constraints give each position one colour. For every unordered Schur equation \(x\le y\), \(x+y=z\le339\), and each colour, one negative clause forbids a monochromatic triple; when \(x=y\), the duplicate literal collapses to a two-literal clause. Finally 69 positive units fix the displayed prefix. These conditions are both necessary and sufficient for a valid extension; there is no reflection assumption, reserved class, extra symmetry condition, or omitted doubling.

I rebuilt the entire CNF clause **multiset** independently by traversing output \(z\) first, rather than the source generator's first summand \(x\). Its 28,730 triples, including 169 doublings, contribute to exactly **177,873 unique clauses** on **2,034 variables** after the one-hot and prefix clauses are included. Every generated clause and multiplicity matches. The 3,184,605-byte CNF has SHA-256 `b454847f2307822f31a2054b461096f1addc85bf3a48179caed4f8a5b6bb1dc2`.

Using CaDiCaL 1.9.5 at source commit `146207318796f094dcded87349a64f0c6927309e`, I regenerated a binary DRAT trace. It has **16,811,935 bytes** and SHA-256 `70406c65d476271ab08ba944cc313fee1a7f45818d7cba284b52c298309a3efa`, matching the source record. A fresh invocation of drat-trim built from commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` returned `s VERIFIED`; my independent auditor invoked the checker again after validating the CNF and proof bytes. The retained proof core uses 19,010 input clauses and 138,294 learned clauses. The checked refutation establishes UNSAT at 339, completing the exact endpoint argument.

This is distinct from the earlier [81-entry Fredricksen–Sweet baseline-prefix obstruction](https://github.com/helgithorskarp/math_results/tree/main/schur_s6_prefix81_obstruction): the literal prefix here comes from a different near word. It also replaces the earlier unproved 80-entry diagnostic for that near word with a certificate at a shorter prefix and a first-impossible endpoint. No result is claimed for its 68-entry prefix; bounded runs returning `UNKNOWN` cannot show that 69 is the shortest obstructing length.

## Reproduction, novelty, and trust

From the repository root, using Python 3.11 or later, CaDiCaL 1.9.5, and the cited drat-trim revision:

```sh
cd schur_s6_prefix69_extension
python3 -B check.py
python3 -B encode.py --n 339 --output /tmp/schur-prefix69-n339.cnf
python3 -B audit.py /tmp/schur-prefix69-n339.cnf
cadical -q -n /tmp/schur-prefix69-n339.cnf /tmp/schur-prefix69-n339.drat
drat-trim /tmp/schur-prefix69-n339.cnf /tmp/schur-prefix69-n339.drat
cd ../schur_s6_prefix69_extension_review1
sha256sum -c SHA256SUMS
python3 -B audit.py --cnf /tmp/schur-prefix69-n339.cnf \
  --proof /tmp/schur-prefix69-n339.drat --drat-trim /path/to/drat-trim
```

The final independent command prints `PASS prefix=69 witness=338 witness_rows=28561 doublings=169 cnf_clauses=177873 proof_checked=true`. I ran the full check with the named source revisions. The 16.8 MB trace is regenerated locally and is not committed. The trust boundary is the complete public witness and prefix, the finite CNF translation, literal Python audits, and the C proof checker. A solver's UNSAT message or proof hash alone does not establish the exclusion.

Targeted literature searches for the exact prefix and 338/339 extension threshold found no matching primary statement; that is limited evidence of graph-level novelty, not a historical-priority proof. The scoped result is ready to cite with its certificate and explicit prefix. It makes no numerical progress beyond the 536 construction, and a claim about the value of \(S(6)\) would need a complete 537-or-longer word or an exclusion covering every possible prefix.

## Strengthening and improvement opportunities

1. **Resolve the adjacent 68-prefix.** A checked 339-colouring extending its first 68 entries would show that entry 69 is essential to this 339-exclusion; a checker-accepted UNSAT proof would shorten the fixed prefix further. The existing bounded `UNKNOWN` runs decide neither case.
2. **Explain the 339 obstruction more compactly.** Extract a small checked UNSAT core or a human-readable propagation certificate from the full proof. That could identify which of the 69 fixed positions and which Schur equations actually cause the failure. Any claimed smaller core must be checked against the same unrestricted extension semantics.
3. **Use the exclusion in global searches.** A complete 537 search may forbid this prefix and its global colour permutations, but must preserve all other prefixes. A valid full word at 537 would improve \(S(6)\); one fixed-prefix refutation cannot determine it.
