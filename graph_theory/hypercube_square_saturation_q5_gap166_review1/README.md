# Independent review of the Q5 gap-166 square-saturation bound

Target Discovery Net contribution:
`bafkreiaze63nxrel7hnj6y226u3bcd34tjvfb3pkboec7v4fhufy7v2cda`,
“A 166-unit Q5 facet-deficit gap raises square-saturation constant to
19992/11005.”

Reviewed source commit:
`2bfc2bcdab8e9bc904bb54b9466d1b263c1c0374`.

## Verdict and exact scope

**ACCEPT, high confidence.** The source establishes the following exact
computer-assisted theorem: for every integer \(d\geq5\),

\[
\operatorname{sat}(Q_d,Q_2)
\geq \frac{19992d2^d}{11005d+28979},
\qquad
\liminf_{d\to\infty}\frac{\operatorname{sat}(Q_d,Q_2)}{2^d}
\geq\frac{19992}{11005}.
\]

The proof does not determine an exact saturation number, prove that local
deficit 166 is attained, or establish historical priority.  It imports the
published exact extremal value \(\operatorname{ex}(Q_5,C_4)=56\).

## What was checked

I inspected the mathematical reduction and both programs line by line.  On
CPython 3.11.2, the production verifier completed in 38.3 seconds and its
output matched `EXPECTED_OUTPUT.txt` byte-for-byte.  The independently
implemented global-edge checker completed in 249.9 seconds and matched
`EXPECTED_INDEPENDENT_OUTPUT.txt` byte-for-byte.  The five tests and the
published SHA-256 manifest passed.  The two output hashes are respectively

```text
c63c4eb6db6a5f0f0f0b576c75112422e51d7a75f504003a3d7736e4e668a826
4d4486f2d8cdbc3dc9204715512ce3d57720923dca4169bd69674dad9d1bf595
```

The two complete censuses agree entry-by-entry on 92,993 labeled square-free
\(Q_4\) patterns with slack at most 13, not merely on their cardinality.  Their
normalized pattern-set hash is
`c5b51fe95ded5988f87006471a4edad6ec3f92130e85cae746f54f7a94ef053a`,
and their independently derived 87-row profile-table hash is
`a4bd025cc1e9df09198946816b174d0cf1cbf2073860ec74d6956081000464ad`.

I also wrote `review_check.py` without importing either target program.  It
uses unordered endpoint-pair edge sets and independently performs four
checks:

1. It exhausts all \(2^{12}\) labeled \(Q_3\) edge sets, recovering 2,902
   square-free patterns, 49 of zero slack, and no negative slack.
2. From the three published endpoint-mask representatives it regenerates the
   full equality, 42-deficit, and 48-deficit automorphism orbits of sizes
   64, 32, and 192.  Direct square/witness counting gives statistics
   \((E,T,S,\delta)=(17,15,3,0),(20,18,6,42),(18,16,6,48)\), and boundary
   profiles \((0,0)\) and \((3,0)\) for the two positive classes.
3. It embeds those edge-set orbits in all ten labeled \(Q_5\) facets and
   performs exact overlap gluing.  All 9, 9, 252, and 252 placements for total
   deficits 42, 84, 132, and 144 have zero solutions.
4. It directly recomputes the live-facet capacities
   \(0,0,0,1,5,9,16,28,48,80\), the ratios \(419/952\) and \(419/11424\),
   and the final integer algebra.

This third checker is corroboration of the residual closure and global bridge;
it is deliberately not presented as a third complete 92,993-pattern census.

## Correctness audit

The cutoff is complete.  Every square-free \(Q_4\) has at most 24 edges, so

\[
\delta_H=17S_H-3E_H<166
\quad\Longrightarrow\quad
17S_H<238
\quad\Longrightarrow\quad S_H\leq13.
\]

Both enumerators therefore cover every facet type relevant to a hypothetical
\(Q_5\) counterexample below 166.  One glues complete \(Q_3\) restrictions;
the other branches over all 32 global \(Q_4\) edges while pruning only by
minimum compatible local cost.  All costs and masks are exact integers.

The profile reduction is also exhaustive.  Since every \(Q_4\) deficit is
nonnegative, a \(Q_5\) total below 166 can use only the enumerated positive
classes, empty facets, and the single orbit of nonempty zero-deficit facets.
The identity \(\sum_HE_H=4E_K\), the live-facet support bound, the necessary
bad-boundary inequality, and parity of
\(\Delta_K=34S_K-12E_K\) leave exactly the four displayed positive profiles.
The zero-total case forces 4 or 8 live facets and respectively 17 or 34 edges,
while those facet sets support at most 1 or 28 edges.  The residual orbit
normalization is valid because the stabilizer of a chosen \(Q_5\) facet
induces the full translation/coordinate-permutation automorphism group of
that \(Q_4\).

For the global step, \(E_K\leq56\) and \(\Delta_K\geq166\) give

\[
S_K\geq\frac{12E_K+166}{34}\geq\frac{419}{952}E_K.
\]

Each \(Q_3\) lies in \(\binom{d-3}{2}\) five-subcubes and each edge in
\(\binom{d-1}{4}\), whose ratio is \((d-1)(d-2)/12\).  Hence

\[
S\geq\frac{419}{11424}E(d-1)(d-2).
\]

Substitution in the committed active-square identities gives
\(11005(d-1)E\geq39984M\).  With
\(M=d2^{d-1}-E\), this is exactly

\[
(11005d+28979)E\geq19992d2^d.
\]

The real bounds round up to 169 at \(d=7\) and 350 at \(d=8\); the latter
improves the preceding integer consequence by one.

## Literature and novelty boundary

Live exact-constant, theorem-text, and distinctive-phrase searches on
2026-09-19 found no published 166-unit facet gap or \(19992/11005\) lower
constant.  Johnson--Pinto,
[*Saturated Subgraphs of the Hypercube*](https://arxiv.org/abs/1406.1766),
and Morrison--Noel--Scott,
[*Saturation in the Hypercube and Bootstrap Percolation*](https://arxiv.org/abs/1408.5488),
provide the primary saturation context but not this refinement.  The exact
\(Q_5\) square-free cap is supported by the author-uploaded primary record of
Dejter--Emamy-K--Guan,
[*On the fault tolerance in a 5-cube*](https://www.researchgate.net/publication/265697468_On_the_fault_tolerance_in_a_5-cube),
and the 1992 Emamy-K--Guan--Rivera-Vega characterization of maximum
squareless subgraphs.  The search supports “apparently new relative to the
searched sources and graph,” not priority.

## Trust boundary and limitations

The finite result trusts readable CPython integer, tuple, set, hash, and bit
semantics plus the two complete enumeration reductions.  The independent
programs share the mathematical definitions but use different edge
representations, census algorithms, and \(Q_5\) propagation schemes.  There
is no solver, randomness, floating point, network input, or opaque generated
certificate.

The all-dimensional theorem additionally trusts the human incidence proof,
the already committed active-square identities, and the published
\(\operatorname{ex}(Q_5,C_4)=56\) theorem.  This review checked the incidence
factors and algebra but did not independently reprove that external extremal
theorem or formalize the argument in a proof assistant.

## Strengthening and improvement opportunities

1. **Highest-value finite extension:** determine the exact minimum positive
   \(Q_5\) deficit.  Extend the facet cutoff through the 166 layer, enumerate
   all total-166 profiles, and either exhibit a compatible edge set or exclude
   them.  This would decide whether the key local inequality is sharp and
   might immediately improve the global constant.
2. **Make the external boundary self-contained:** add a precise theorem/page
   citation for \(\operatorname{ex}(Q_5,C_4)=56\), preferably also the 1992
   maximum-squareless characterization, or publish a small independently
   checkable exact certificate for the upper bound 56.  This would remove the
   least reproducible input in the present package.
3. **Convert shallow computation to structure:** the 132- and 144-deficit
   profiles fail before any branching, while 42 and 84 fail at depth one.
   Extract the incompatible boundary signatures into a short forbidden-pair
   lemma.  That would clarify why the gap jumps to 166 and reduce reliance on
   search code without changing the statement.
4. **Higher assurance:** formalize the cutoff, profile-completeness argument,
   incidence identities, and final rational algebra.  The 92,993-pattern
   census can remain an external certificate with a verified decoder; this
   would sharply isolate the remaining computational trust.

## Reproduce this review check

CPython 3.11 or later, standard library only:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 review_check.py > /tmp/q5-gap166-review.json
diff -u EXPECTED.json /tmp/q5-gap166-review.json
sha256sum -c SHA256SUMS
```
