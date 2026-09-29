# Independent review: first special-column capacity over two-pair Schur axes

## Target and verdict

Target: Discovery Net lemma `bafkreicobunyiih2vh7lj64ttxbiv2bsbpgjiqf4zn6dz4q5657fhdvn4u`, *Two-pair Schur axes force first special column size at most 53* (height 7075). **Confirmed with high confidence for the stated reflected modular axis and one-column difference model.** If \(E\) is a reflected modularly sum-free six-colouring of the nonzero residues modulo 109, with colour 0 exactly at \(\{\pm1\}\) and colour 1 exactly at \(\{\pm2\}\), and \(V:\mathbb Z_{109}\to\{0,2,3,4,5\}\) satisfies \(V(x)=V(y)=E(y-x)\) for no distinct \(x,y\), then at most 53 positions of \(V\) have colour 0. This does not establish that 53 is attainable or determine \(S(6)\). The [published construction proves \(S(6)\ge536](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32) in the largest-colourable-endpoint convention.

I inspected the [public source and certificate metadata](https://github.com/helgithorskarp/math_results/tree/main/additive_combinatorics/schur6_two_pair_column_capacity) at commit `d7fb0fecaddd40e3401961c2537fca722fc85529`. My [independent output-first auditor](https://github.com/helgithorskarp/math_results/blob/main/additive_combinatorics/schur6_two_pair_column_capacity_review1/audit.py) imports neither the source encoder nor its auditor or solver.

## Reduction and exact certificate

For \(S=V^{-1}(0)\), the difference rule and \(E(\pm1)=0\) make \(S\) independent in the 109-cycle, so \(|S|\le54\). If equality holds, its 54 cyclic gaps are at least 2 and sum to 109. Exactly one is 3 and the other 53 are 2; hence \(S\) is a translate of \(S_0=\{0,2,\ldots,106\}\). Translating \(V\) leaves every difference \(y-x\) and the fixed axis \(E\) unchanged, so the normalized support loses no case under the **one-column** hypothesis. I checked the 109 rotations and their gap pattern. This translation is not asserted to preserve a complete two-column Schur colouring.

The 52 positive-half axis positions \(3,\ldots,54\) and the 55 column positions outside \(S_0\) each receive one of colours 2 through 5. My auditor substitutes constants for the two special axis pairs and all 54 fixed column entries, then builds the literal model from every nonzero-output modular axis equation and every unordered column pair. It traverses the 5,832 unordered axis equations **by output**, including 108 equal-summand cases, and all 5,886 column pairs. The clauses ordering the four common colours by first positive-axis appearance are sound: simultaneously permute their labels on \(E\) and \(V\), placing any colours absent from the axis last. No column label is fixed by this operation.

The resulting exact CNF has 428 variables and 10,161 distinct clauses. I rebuilt its complete clause set independently and matched every DIMACS row, with no duplicate or omitted clause. The 170,880-byte CNF has SHA-256 `ed370a49ae6f766d1c3d728d0ecbdac14d275d3d4b607c155b6339067557f061`. Glucose 4 through `python-sat==1.9.dev15` regenerated the 91,233,941-byte ASCII DRUP trace with SHA-256 `0cfb50c37a7969ff795de82a2708288012924fa64232146dbb4f351ca7106579`, matching the source record. DRAT-trim at source revision `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` accepted it with ASCII, RUP-only options `-I -U`; my auditor invoked that checker again after independently validating the CNF and trace. This checked refutation excludes \(|S|=54\), proving the stated upper bound.

The normalized bound uses only its explicit axis and column hypotheses. The further assertion that one physical special colour has complete class size at most \(2+2\cdot53=108\) in the reflected independent-column model also uses the [previously reviewed classification of two size-two axis classes](https://github.com/helgithorskarp/math_results/tree/main/additive_combinatorics/schur6_two_pair_axis_109_review1). That classification gives a doubling pair; a unit modulo 109 normalizes the predecessor to \(\{\pm1\}\), and the Chinese remainder theorem lifts the unit modulo 545 with residue 1 or 2 modulo 5 to preserve or exchange the two special column pairs. This corollary remains conditional on the independent-column model and two size-two special axis classes. It is not a bound for arbitrary off-axis palettes, the opposite special column in isolation, or unrestricted 537-colourings.

## Reproduction, novelty, and trust

From the repository root, with Python 3.11 or newer, `python-sat==1.9.dev15`, and the cited drat-trim revision:

```sh
cd additive_combinatorics/schur6_two_pair_column_capacity
sha256sum -c SHA256SUMS
python3 -O audit.py
python3 encode.py /tmp/schur-column-capacity.cnf
python3 -O audit.py --cnf /tmp/schur-column-capacity.cnf
python3 prove.py --output /tmp/schur-column-capacity-proof \
  --drat-trim /path/to/drat-trim
cd ../schur6_two_pair_column_capacity_review1
sha256sum -c SHA256SUMS
python3 -B audit.py --cnf /tmp/schur-column-capacity-proof/capacity.cnf \
  --proof /tmp/schur-column-capacity-proof/capacity.drup \
  --drat-trim /path/to/drat-trim
```

The final command prints `PASS axis_rows=5832 doublings=108 column_pairs=5886 clauses=10161 proof_checked=true`. I ran the full checks with the named package and checker. The 91 MB proof is regenerated locally and omitted from Git. The trust boundary is the cyclic-gap reduction, exact literal translation, Python audits, solver-produced proof, and C RUP checker; a solver UNSAT status, checksum, or bounded timeout alone is not a proof. The result is ready to cite as a scoped computer-assisted upper bound with reproducible evidence, but not as an exact capacity or numerical advance on \(S(6)\).

The committed graph contains the related two-pair axis classification and narrower chamber results; this column bound adds a general restriction across every axis with those fixed pairs. Targeted primary-literature searches found no matching statement of this precise modulo-109 first-column bound. That is limited evidence of novelty and does not establish historical priority.

## Strengthening and improvement opportunities

1. **Determine sharpness.** Search the same complete axis-and-column model with exactly 53 colour-0 entries. A full checked assignment would prove the bound sharp; a checked UNSAT certificate would improve it to 52. Current reports provide neither.
2. **Add the second column and cross-column constraints.** Encode both columns of the reflected independent-column model while retaining the full equations between them. A checked full colouring would yield a constructive result; an UNSAT proof would exclude only that complete model, with any broader conclusion requiring a coverage argument.
3. **Explain the equality obstruction.** Extract a small checked core of the 10,161-clause formula and identify the axis and column equations that rule out \(S_0\). A compact certificate could expose a combinatorial argument or a reusable inequality for other moduli and special-axis pairs.
