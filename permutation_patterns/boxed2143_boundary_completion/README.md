# Boxed2143 interval boundary composition and a failed root rule

This is a checked **partial research result** by Lyra
(`literature-researcher-2`), with separate internal checks by Sage
(`literature-researcher-1`). The full growth question remains unsolved.

Let a_n count permutations with no selected positions i1<i2<i3<i4 whose
values satisfy p(i2)<p(i1)<p(i4)<p(i3) and whose open bounding rectangle has
no unselected point. The agreed target is to decide whether one finite
constant C satisfies a_n<=C^n for every n>=1, or whether
limsup a_n^(1/n)=infinity. These artifacts establish neither alternative.

The substantive source has two separately checked scopes:

* `BOUNDARY_INTERFACE_LEMMA.md` proves exact composition from the first and
  last three retained values for every global value interval. It proves
  soundness/completeness and canonical witnesses for a mathematical dynamic
  program searching strict odd/even completions with a classical132 scaffold.
  The practical implementation caps inputs at m<=9. Universal root nonemptiness
  is unproved; the recoverable factorial injection is conditional on it.
* `ROOT_ADJACENCY_OBSTRUCTION.md` proves that, for every m>=8, the explicit
  input (2,1,4,3,m-1,m,5,...,m-2) cannot use either largest-even root beside
  the input maximum in that132 grammar, even with all lower subtree choices
  free. A nonadjacent root succeeds for the displayed m8 control.

The first proof also preserves two earlier failed induction rules. Neither
these counterexamples nor the correct search refutes unrestricted completion.
The separately pending guard/signature-entropy claim is outside this version.

The exact immutable proof hashes are
`5faa0cd185933697a5538b158ce7bdf7902864f24a953ab57d77a293442d05da` and
`73b3829a2316eea1dae059806b9071046bbd239696f16c918f10f4ff98d62929`.
Their author status text records when they were written; the later complete
reviews in `review/` accept those unchanged bytes. These are internal team
checks, not external peer review or novelty certification. Sage checks
length5 minimality of the first adjacency rule, not lexicographic firstness
within that length. `PUBLICATION_PROVENANCE.json` records the exact scopes.

Use Python3.11.2 on Linux with the standard library only, from this directory:

```sh
python3 -B check_boundary_completion.py --max-m 5
python3 -B probe_boundary_invariants.py
python3 -B check_root_adjacency.py
python3 -B boundary_completion.py --permutation 1,2,4,5,3
python3 -B review/check_lyra_boundary.py --author-dir . --output /tmp/boxed2143_boundary_review.json
python3 -B review/check_lyra_root_adjacency.py --author-dir . --output /tmp/boxed2143_root_review.json
```

The author finite replay compares every signature/canonical-witness map in
3385 reached subproblems over153 inputs through m5, with state stream
`b0d3c57d6ee50acde2059c812f1e6c3f88d71fbd514b86cb94ca71b1490c7150`.
Sage independently checks these maps, all7415 valid band maps, and8173 generic
merges including sparse labels, empty sides and an omitted root. The separate
root replay checks all70 adjacent-root candidates among429 scaffolds at m8,
312 arbitrary left-band orders and156 after-case labels through20, with
witness stream
`d3d6ba74918896acd1f636cb1e3a9ef8d5f6e1be3e60965e24a231b3e36ce05c`.
Compact original reports are included; runtime and memory fields vary by run.
The written arguments, rather than these finite tests, carry the all-size scope.

`definition_checker.py` is the direct quadruple/shading reference. Reviewer
code independently constructs expected rectangles and signatures and uses the
author algorithm only as an object under test. There is no external solver,
floating-point mathematical comparison or imported dataset.

One public dependency is smaller than the frozen author dependency:
`completion_templates.py` includes only the two used functions, each copied
byte-for-byte; unused exploratory rules are omitted. All proof, algorithm and
reviewer-code bytes are unchanged. `PORTABILITY_EDITS.json` pins the edit and
`PORTABILITY_VERIFICATION.json` records exact deterministic replay comparisons.
`MANIFEST.json` pins the public author sources; `SOURCE_MANIFEST.json` covers
the whole publication except itself. Original review manifests record their
historical author packet identities separately.

Primary context is Kitaev--Qiu--Xu,
[Coincidences and Growth of Boxed Mesh Patterns](https://arxiv.org/html/2609.13764v1),
Theorem3.2 and Conjecture7.4. The value-interval characterization and classical
132 maximum decomposition are known ingredients, credited and reproved for
the precise convention. No general prefix/suffix-automaton priority claim is
made. Downloaded source papers, large search dumps and campaign checkpoints
are not part of this source packet.
