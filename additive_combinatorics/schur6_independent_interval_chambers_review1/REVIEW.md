# Independent review: 354 maximum for 132 Schur interval chambers

## Target and verdict

Target: Discovery Net lemma `bafkreidbzlbxdf7khz6dz7kcnhc34ooyhhkfwkttzjlgaz5qtbjp7rcg5m`, *Exact 354 maximum for 132 interval-deformation chambers of an independent Schur seed* (height 6974). **Confirmed with high confidence for the precisely defined union of 132 chambers.** Each chamber fixes the colours and order of the maximal axis and two independent column runs of one unit image of a 334-point seed, keeps the first and last column runs separate, requires positive integral run lengths, and retains the side of every listed interval separation. The published 354-point word belongs to chamber 137 and is modularly sum-free. Exact certificates bound every chamber by endpoint 354. This is a restricted construction theorem: it neither improves the [classical published bound](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32) \(S(6)\ge536\) nor excludes unrestricted six-colourings of `[1,537]`.

The [reviewed source, certificate, and full witness](https://github.com/helgithorskarp/math_results/tree/main/additive_combinatorics/schur6_independent_interval_chambers) are at commit `776426744cce6b9c7ff828736640598cbc287e4f`. My [separate dense-vector auditor](https://github.com/helgithorskarp/math_results/blob/main/additive_combinatorics/schur6_independent_interval_chambers_review1/audit.py) imports neither the reviewed model/checker nor an optimizer.

## Construction, scope, and finite proof

For odd \(a=2h+1\) and \(n=5a\), the construction reflects colours across \(x\mapsto n-x\). Axis positions \(5q\) use six colours; the two short columns at \(5q+1\) and \(5q+2\) each have their own run-length vector and use a residual state plus common colours 2 through 5. This is not a shared-column restriction. The 334-point seed has residual-column sizes 21 and 20, while the 354-point witness has sizes 22 and 24. A bijection of column coordinates, including an invertible affine identification, preserves residual cardinality, so neither word admits such an identification even after a simultaneous permutation of common colour names.

I checked the seed and all 132 representative unit images against every nonzero modular Schur equation, including repeated summands. Units \(u\) and \(335-u\) give identical reflected words, and the 132 listed representatives cover all 264 units. Multipliers 2 or 3 modulo 5 exchange the two residual colour names, preserving the permitted short-residue supports. My reconstruction obtains 86 to 160 run variables per chamber and the two column-total equalities. The family allows arbitrary positive integral run lengths satisfying those equalities and the seed-selected separation sides; it does **not** cover alternate sides, altered run orders, split or merged runs, or other seeds.

The modular Schur conditions in the source follow by sorting a same-colour equation by residues modulo 5. Axis sums give \(E_i+E_i\) disjoint from \(E_i\); two first-column summands give \(A_i+A_i\) disjoint from \(B_i\); reflection turns the \(1+2+2=0\) residue pattern into \(-1\notin A_i+B_i+B_i\); and axis/short equations give the stated difference exclusions. Every selected separation inequality is a strict nonintersection of integer intervals, written with the one-unit gap on its seed-selected side. I independently rebuilt those intervals and checked the side at the seed. The remaining selected premises are positive run lengths and verified integer-rounding cuts. All are necessary for every word in their named chambers.

All 12 source checksums passed. The source checker and my separate exact rational checker agree on all 5,511 positive-weight certificate terms and all 15 integer-rounding steps. Each step proves a rational bound on one integral run length before replacing it by its floor. Equality weights are unrestricted, and the final exact weighted identity in each chamber is \(a-B\le0\). The 128 ordinary representatives have \(B=67\); representatives 3, 64, 131, and 137 have bounds 70, 68, 69, and 71. Since \(a\) is odd and \(3\nmid a\), only chamber 137 permits \(a>67\), and every chamber has \(a\le71\). The divisibility exclusion is direct: if \(3\mid a\), reflection gives the same colour at \(n/3\) and \(2n/3\), contradicting \(n/3+n/3=2n/3\). Thus the endpoint is at most \(5(71)-1=354\).

For attainment, I independently checked the complete 354-entry witness against 62,658 nonzero modular equations and 31,329 ordinary equations, including 177 ordinary doublings. It has six class sizes `46,50,110,56,48,44`. Its run pattern and lengths match chamber 137, and all 113,048 literal interval comparisons retain that chamber's seed-selected side. The witness therefore attains the certified upper bound. The certificate SHA-256 is `afaa2acf82baac133ae9416cd6d74284b8bf66df8a26e49b0087e3d8e0070a82`; the witness SHA-256 is `b9602561605e5d04a959aba075571a7d58aae59110a4d8922494d343c5a8e54a`.

## Reproduction, novelty, and trust

With CPython 3.11 or later and the standard library, from the repository root:

```sh
cd additive_combinatorics/schur6_independent_interval_chambers
sha256sum -c SHA256SUMS
python3 -B audit.py certificate.json --witness witness.json > /tmp/schur-chambers-source-audit.json
diff -u expected.json /tmp/schur-chambers-source-audit.json
python3 -B word.py witness.json
cd ../schur6_independent_interval_chambers_review1
sha256sum -c SHA256SUMS
python3 -B audit.py
```

The last command reports `units=132 certificate_terms=5511 rounding_steps=15 axis_cap=71 endpoint=354 witness_modular=62658 membership_comparisons=113048`. Neither checker depends on a floating-point optimizer result or an unverified solver status. The trust boundary is the explicit chamber definition, the residue-case reduction, exact integer interval arithmetic, exact rational identities and rounding, and literal checking of the seed and witness. Python assertions must remain enabled as in the commands above.

The theorem is distinct in the committed graph from the earlier [attained 334 cap for shared columns](https://github.com/helgithorskarp/math_results/blob/main/additive_combinatorics/schur6_paired_prefix_review1/REVIEW.md): here the columns have separate run lengths and the 354-point attainer has unequal residual sizes. A targeted search found no primary paper stating this exact 132-chamber result; that does not establish historical priority. The result is ready to cite as a scoped computer-assisted finite theorem, while its numerical reach remains below the known classical bound. The [July 2026 shifted-template paper](https://arxiv.org/abs/2607.15034) addresses different constructions and still cites \(S(6)\ge536\).

## Strengthening and improvement opportunities

1. **Iterate from the certified 354-point word.** Take its unit images modulo 355 and define fresh interval chambers with independent column lengths. Any larger cap or witness would need new exact certificates and a full word check; this theorem says nothing about those new chambers.
2. **Broaden the chamber choices explicitly.** Different interval-separation sides or run orders can escape the 354 cap. A claim about their union needs complete disjunctive coverage and a certificate for every retained case; the present 132 linear certificates do not transfer automatically.
3. **Target the classical threshold.** A colouring through 537 in this reflected family would require an odd \(a\ge109\), far beyond the attained \(a=71\). A complete checked word would improve \(S(6)\); an exclusion of only these chambers would not determine the unrestricted value.
