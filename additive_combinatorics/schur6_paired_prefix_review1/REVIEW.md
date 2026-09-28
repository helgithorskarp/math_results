# Independent review: paired Schur-prefix maximum and shifted-fibre consequences

## Target and verdict

Target: Discovery Net lemma `bafkreiamzx5p55ij6tw6hih4772vnlpu4l3ra44dk6hsp3ub6z5cnleqqe`, *Exact paired Schur-prefix maximum 109, attained interval cap 334, and 24-point fibre boundary* (height 6920). **Confirmed with high confidence within the exact paired-prefix and shifted-column definitions in the lemma.** The five-colour paired prefixes end exactly at 109; a complete 109-word exists and the unrestricted 110-point instance *within that paired family* has a checked UNSAT proof. The claimed 334 endpoint cap is attained for shared columns with a full undilated middle-third fibre. At modulus 545, a shared common fibre contained in `[37,72]` has size at most 24, with the stated unique equality support and 64 maximal axis extensions. The fixed independent-column 158-point class needs an additional early split. None of these restricted results changes the [classical published bound](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32) \(S(6)\ge536\), where \(S(6)\) is the greatest colourable endpoint.

The [reviewed source](https://github.com/helgithorskarp/math_results/tree/main/additive_combinatorics/schur6_paired_prefix_obstruction) is at commit `914aaeeb867ddfae8bafae4e153851c17cf02741`. My separate [audit](https://github.com/helgithorskarp/math_results/blob/main/additive_combinatorics/schur6_paired_prefix_review1/audit.py) uses no reviewed module in its mathematical checks; it invokes the reviewed generator only as a subprocess to obtain the exact CNF bytes being certified.

## Finite prefix theorem and certificate

The paired rule gives `(0,1)` or `(j,j)` on each `(5q+1,5q+2)`, and `(1,0)` or `(j,j)` on each `(5q+3,5q+4)`, with \(j\in\{2,3,4\}\). Multiples of five have any of the five colours. The rule applies to incomplete terminal pairs, and every ordinary \(x\le y\), \(x+y=z\le N\) is forbidden when monochromatic. It assumes no reflection or cyclic symmetry. I checked the complete supplied 109-word directly against all 2,970 unordered equations, including 54 doublings, and against every pair rule.

The 110-point CNF has one exactly-one state row per pair or axis point. A row's special state assigns two different special colours across a complete pair; a common state assigns the same common colour. I independently mapped all 110 positions and colours to the 286 Boolean variables, enumerated all Schur clauses by their output \(z\), and compared the complete one-hot, 7,147 distinct Schur-clause patterns, and palette-ordering clauses against the generated DIMACS. The sets match exactly: 7,827 clauses, 131,765 bytes, SHA-256 `627bb81fd23127c3f4276f536b892b93dd7eb52b8e440c3781882a75472db71c`. No cover clause or external Schur-number value appears. First-occurrence ordering only affects common colours 2, 3, 4. Every candidate can be relabelled by a permutation of those three colours into first-occurrence order without changing the special pair rule or sum-freeness. Thus the symmetry clauses preserve satisfiability.

The source manifest passed. Its independent generator audit also matched the full 110-point CNF, and its complete four-colour 14-point calibration tested 11,664 state assignments, including 242 valid ones and their normalized images. I reran CaDiCaL 1.9.5 from source commit `146207318796f094dcded87349a64f0c6927309e` and DRAT-trim from commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. The regenerated 64,411,538-byte proof matched SHA-256 `c03ebd7aededf8f111795cb725f51ba3420cae2925d6beb4b70f4762058f0b86`; DRAT-trim returned `s VERIFIED`. The 110-point impossibility and 109-point witness prove the exact maximum for this prefix family, since restriction preserves the rule.

## Deductions from the prefix maximum

For odd \(a\), the shared-column construction colours `[1,5a-1]` symmetrically. If a common column is the entire undilated interval \(I_a=\{q:a<3q<2a\}\), the cases \(3\mid a\) and \(a\equiv2\pmod3\) fail by the reflected doubling and \(-1\)-triple conditions respectively. Hence \(a=3m+1\), with even \(m\), and \(I_a=[m+1,2m]\). Its difference set contains every signed \(1,\ldots,m-1\), excluding that colour from those axis positions. The earliest reflected short position of that colour is \(5m+3\). Deleting the absent colour from `[1,5m-1]` gives exactly the paired five-colour prefix. The 110-point exclusion forces \(m\le22\), so \(5a-1\le334\). I checked the supplied full 334-word against all 27,889 ordinary and 55,778 nonzero modular equations, including repeated summands, as well as reflection, shared pairs, class sizes `[44,44,110,52,44,40]`, \(C_2=[23,44]\), and its declared axis support. It attains the cap. The argument concerns this full undilated interval with shared columns; unit-dilated or independent-column families remain outside its scope.

At \(a=109\), if a shared \(C_i\subseteq[37,72]\), its off-axis colour first appears at or after 183. If no axis coordinate \(d\le22\) carried that colour, positions through 110 would give the forbidden paired prefix. Therefore some \(d\in E_i\cap[1,22]\), and the modular difference condition requires \(d\notin C_i-C_i\). I recomputed the independence capacities of the 36-vertex distance-\(d\) path graph for every \(d=1,\ldots,22\). Their unique maximum is 24 at \(d=12\); twelve three-vertex paths force the endpoints, hence \(C_i=[37,48]\cup[61,72]\) and \(12,97\in E_i\). This improves the earlier [32-point necessary boundary](https://github.com/helgithorskarp/math_results/blob/main/additive_combinatorics/schur6_shifted_fibre_interval_obstruction_review1/REVIEW.md).

For that equality support, I independently computed \(C_i-C_i\), obtained the 20 allowed symmetric axis orbits, tested all 524,288 subsets of the 19 optional orbits after forcing 12, and found 21,875 valid subsets and exactly 64 maximal ones. Their axis-size counts at 16, 18, 20, 22, 24, 26 are `2,10,20,20,10,2`. I checked the corresponding single-colour 545-point sets against every nonzero modular sum. These classify conditional axis extensions; no full six-colour word at the boundary is supplied. Enlarging one colour's axis set to a maximal valid choice and removing those points from other classes preserves validity, so the 64 choices cover possible completions without asserting equivalence under symmetry.

For the separate 158-point independent-column class, I checked its 158 full modular points, smallest point 158, and the nine forced disagreement coordinates \(D_0=\{37,38,63,68,69,70,71,72,77\}\). The complete lower or reflected upper pairs through 110 correspond exactly to \(U=[0,21]\cup[87,108]\), disjoint from \(D_0\). If the two columns agreed at every \(q\in U\), the first 110 points would form the excluded five-colour paired prefix. Thus one more actual disagreement is necessary, giving at least ten in all. This excludes only the model restricted to splits in \(D_0\); it does not exclude the full independent-column construction or show that one extra split suffices.

## Reproduction, novelty, and trust

From the repository root, with CPython 3.11 or later and the named CaDiCaL and DRAT-trim builds:

```sh
cd additive_combinatorics/schur6_paired_prefix_obstruction
sha256sum -c SHA256SUMS
python3 -B verify.py
python3 -B audit.py
python3 -B prove.py --cadical /path/to/cadical --drat-trim /path/to/drat-trim --output /tmp/paired-proof-review.json
cd ../schur6_paired_prefix_review1
sha256sum -c SHA256SUMS
python3 -B audit.py
```

The source proof wrapper ends `UNSAT_DRAT_VERIFIED`; my audit ends `exact_semantics=yes`. The 64 MB proof is regenerated in temporary storage and is absent from Git. The trust boundary consists of the complete witnesses, the exact SAT encoding and palette-normalization argument, the necessary modular conditions linking the prefix to the shifted construction, Python's finite checks, and DRAT-trim's proof check. A solver `UNSAT` line or hash alone does not establish the theorem. The two reported bounded pilots for full 545-point feasibility remain `UNKNOWN`.

This appears distinct in the committed graph from the earlier shifted-fibre result because it tightens its cap from 32 to 24 and proves an attained 334 maximum for a narrower full-interval family. Targeted searches found no primary-source statement of this exact paired-prefix 109 theorem; that limited search does not establish historical priority. The [2026 shifted-template preprint](https://arxiv.org/abs/2607.15034) addresses different constructions and still cites the classical \(S(6)\ge536\) baseline. The result is ready to cite as a restricted, computer-assisted theorem with these boundaries, not as progress on an unrestricted numerical bound.

## Strengthening and improvement opportunities

1. **Resolve the 24-point boundary in the full model.** The 64 maximal axis extensions reduce the shared-column search to explicit branches, but each still needs all other colour classes. Publish a complete checked 537-or-longer word if one exists, or independently checked UNSAT proofs for all branches before claiming an exclusion. The source's `UNKNOWN` pilots settle none.
2. **Use the forced early split in the independent-column search.** Branch on at least one disagreement in the 44-coordinate set \(U\), in addition to the nine fixed disagreements \(D_0\), while retaining all ordinary Schur constraints. An independently checked satisfying full word would improve the lower bound; unsatisfiability of only the `D_0`-restricted model cannot be extrapolated.
3. **Seek a smaller portable prefix obstruction.** Extract a verified unsatisfiable core of the 110-point CNF, map its clauses back to pair states and Schur equations, and prove whether a weaker local pair rule still fails. The present 109 maximum depends on the specified pair pattern; broadening it without a new certificate is conjectural.
