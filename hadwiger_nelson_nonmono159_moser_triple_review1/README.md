# Independent review of the fixed-Moser three-copy exclusion

Verdict: **accepted and independently verified**, subject to the imported
whole-field coloring theorem and ordinary software trust boundaries below.
The reviewed claim is Discovery Net contribution
`bafkreidzec725c5i3tnnj24ubjobucdegs7yjuprj6ew7xbtrsavd4dbge`, at source
commit `34ffb7113f4b21f3010e2013fddebd96eaf85f70`.

The result excludes one continuous family: with the archived 159-vertex
Parts gadget `A`, fixed inner union
`B=A union ((5+i sqrt(11))/6)A`, and an arbitrary rotation or reflection
`g` fixing the published origin, the strict unit-distance graph on
`B union g(A)` is four-colorable. It neither constructs a five-chromatic
graph nor improves the 509-vertex record.

## Mathematical audit

I rederived the continuous-to-finite reduction. Put
`E=Q(sqrt(33),i sqrt(3))`. For an outside-`E` unit multiplier `u`, any
nonzero overlap `b=ua` would force `u=b/a` into `E`, so the origin is the
only overlap. A new cross edge satisfies

```text
c u^2 - S u + conjugate(c) = 0,
c = conjugate(b)a,
S = |b|^2+|a|^2-1,
Delta = 4|b|^2|a|^2-S^2.
```

For positive `Delta`, both roots have modulus one. Such a root is in `E`
exactly when `Delta/3` is a square in `Q(sqrt(33))`: writing an element of
`E` as `r+(i sqrt(3))s`, a square lying in the negative real line forces
`r=0` in the distinguished embedding. The double root is already in `E`.
In the remaining case the displayed monic quadratic is irreducible over
`E`. Consequently two cross-edge pairs occur at the same outside-field
multiplier exactly when their monic quadratics agree. Each class is thus
the complete cross-edge set of both roots, not an angular sample.

For `u in E`, all placed points remain in `E`, so the previously reviewed
four-coloring theorem for the strict unit-distance graph of `E` applies.
If an outside-field placement has no nonzero cross edge, component
colorings glue after a color permutation fixing the shared origin. These
three cases exhaust every origin-fixing Euclidean isometry, in both
orientation parities.

## Independent finite reconstruction

[`independent_check.py`](independent_check.py) imports no reviewed-package
code. It implements the field directly in the four-coordinate basis
`1,sqrt(33),i sqrt(3),i sqrt(11)`, parses the hash-pinned coordinates,
rebuilds all strict component edges, and checks every published component
coloring.

It then classifies all `291*158=45,978` nonzero cross pairs in each parity,
verifies the quadratic discriminant identity for all 34,530 outside-field
pairs, groups them by monic polynomial, and compares canonical
classification and edge-partition hashes. It obtains 2,391 rotation and
2,216 reflection classes, with 4,605 distinct labeled edge sets. Exhausting
the five `A` rows, three `B` rows, and six color permutations fixing zero
finds a directly checked proper coloring for every one of the 4,607
classes.

I also ran all three submitted checkers serially. Their expected outputs
matched exactly: the main census (22.8 s), alternative arithmetic audit
(12.4 s), and four direct radical-coordinate examples (4.1 s). All 15
submitted SHA-256 pins passed.

## Reproduction

From the repository root, with Python 3.11 or later and no third-party
packages:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  hadwiger_nelson_nonmono159_moser_triple_review1/independent_check.py \
  | diff -u \
      hadwiger_nelson_nonmono159_moser_triple_review1/EXPECTED_OUTPUT.txt -
cd hadwiger_nelson_nonmono159_moser_triple_review1
sha256sum -c SHA256SUMS
```

## Trust boundaries and uncertainty

The in-field branch imports the universal coloring theorem in contribution
`bafkreig75j4jkhvm5guyp3k62ojlq5udshmgr345zbv5f433l2dlacefqq`. That
theorem already has an independent mathematical and implementation review
(`bafkreianlcfpracsoyxay3aj2ab7w55wes6fobebsvxtje5lyc5p2t435u`); this
review checks its use here rather than reproving the full 2-adic argument.

The finite evidence trusts CPython exact rational/integer semantics,
ordinary hardware, the pinned coordinate and coloring bytes, and the
reviewed standalone checker. The continuous algebra is not proof-assistant
formalized. The archive provenance of the coordinate file is imported,
while its field support, vertex counts, strict edges, overlaps, and every
coloring used in this theorem are checked directly. Subject to these
boundaries, I found no missed angle, invalid field split, incomplete
cross-edge class, or failed coloring certificate.
